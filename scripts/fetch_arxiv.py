#!/usr/bin/env python3
"""Fetch new arXiv preprints in configured categories, dedupe, append to today's raw JSON.

arXiv is fully open access. Every fetched paper has an `oa_url` pointing at the
arXiv PDF, which the downloader handles in the OpenAlex-oa_url path with no
extra publisher logic.

Usage:
  python scripts/fetch_arxiv.py
  python scripts/fetch_arxiv.py --from 2026-04-20 --to 2026-04-27
  python scripts/fetch_arxiv.py --merge papers/raw/2026-04-27.json   # append into existing
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "papers" / "config.yaml"
STATE_PATH = ROOT / "papers" / "state.json"
RAW_DIR = ROOT / "papers" / "raw"

ARXIV_API = "http://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom",
           "arxiv": "http://arxiv.org/schemas/atom"}


def fetch_category(category, from_date, to_date, max_results, contact):
    """Query arXiv API for papers in `category` updated within [from_date, to_date]."""
    # arXiv query syntax: cat:<category> AND submittedDate:[YYYYMMDDtoYYYYMMDD]
    fd = from_date.replace("-", "") + "0000"
    td = to_date.replace("-", "") + "2359"
    query = f"cat:{category} AND submittedDate:[{fd} TO {td}]"
    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": str(max_results),
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    # arXiv recommends polite usage; on 429 back off generously.
    headers = {"User-Agent": f"Mozilla/5.0 PaperTracker mailto:{contact}"}
    xml_bytes = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                xml_bytes = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                wait = 10 * (attempt + 1)   # 10, 20, 30 s
                print(f"  ! {category}: 429, sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"  ! {category}: HTTP {e.code}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"  ! {category}: {e}", file=sys.stderr)
            return []
    if xml_bytes is None:
        return []

    root = ET.fromstring(xml_bytes)
    out = []
    for entry in root.findall("atom:entry", ATOM_NS):
        arxiv_id_full = entry.findtext("atom:id", default="", namespaces=ATOM_NS)
        # id is like http://arxiv.org/abs/2604.12345v1 — strip the version, prefix with arxiv-
        arxiv_id = arxiv_id_full.rsplit("/", 1)[-1].split("v")[0]
        if not arxiv_id:
            continue
        title = (entry.findtext("atom:title", default="", namespaces=ATOM_NS) or "").strip()
        title = " ".join(title.split())  # collapse whitespace
        abstract = (entry.findtext("atom:summary", default="", namespaces=ATOM_NS) or "").strip()
        abstract = " ".join(abstract.split())
        published = entry.findtext("atom:published", default="", namespaces=ATOM_NS)[:10]
        authors = [a.findtext("atom:name", default="", namespaces=ATOM_NS)
                   for a in entry.findall("atom:author", ATOM_NS)][:10]
        # Look for an arXiv DOI element if present (sometimes posts come with one)
        doi_el = entry.find("arxiv:doi", ATOM_NS)
        doi = doi_el.text if doi_el is not None else None
        # PDF link
        pdf_url = None
        for link in entry.findall("atom:link", ATOM_NS):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href")
                break
        if not pdf_url:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        out.append({
            "id": f"arxiv-{arxiv_id}",
            "doi": (f"https://doi.org/{doi}" if doi else None),
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "date": published,
            "venue": f"arXiv ({category})",
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "open_access": {
                "is_oa": True,
                "oa_url": pdf_url,
                "oa_status": "green",
            },
        })
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from", dest="from_date")
    p.add_argument("--to", dest="to_date")
    p.add_argument("--merge", help="If set, append results into this existing raw JSON file (dedup by id)")
    args = p.parse_args()

    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    arxiv_cfg = config.get("arxiv") or {}
    if not arxiv_cfg.get("enabled"):
        print("arxiv disabled in config; skipping")
        return

    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    seen_ids = set(state.get("seen_ids", []))

    today = datetime.now(timezone.utc).date()
    to_date = args.to_date or today.isoformat()
    if args.from_date:
        from_date = args.from_date
    elif state.get("last_daily"):
        last = datetime.fromisoformat(state["last_daily"]).date()
        lookback = int(config.get("lookback_days", 35))
        from_date = (last - timedelta(days=lookback)).isoformat()
    else:
        from_date = (today - timedelta(days=int(config.get("lookback_days", 35)))).isoformat()

    contact = config.get("email", {}).get("from_addr", "anonymous@example.com")
    cats = arxiv_cfg.get("categories", [])
    per_cat = int(arxiv_cfg.get("per_category_max", 100))
    print(f"arXiv: {from_date} -> {to_date}, {len(cats)} categories, {per_cat}/cat")

    all_new = []
    total = 0
    for i, cat in enumerate(cats):
        if i > 0:
            time.sleep(5.0)   # arXiv polite-rate guideline (3s minimum, 5s safer)
        papers = fetch_category(cat, from_date, to_date, per_cat, contact)
        new = [p for p in papers if p["id"] not in seen_ids]
        total += len(papers)
        if papers:
            print(f"  {cat}: {len(papers)} fetched, {len(new)} new")
        all_new.extend(new)

    # Dedup by id within this run.
    by_id = {p["id"]: p for p in all_new}
    deduped = list(by_id.values())

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if args.merge:
        merge_path = Path(args.merge)
        if not merge_path.is_absolute():
            merge_path = ROOT / merge_path
        if merge_path.exists():
            existing = json.loads(merge_path.read_text(encoding="utf-8"))
            existing_ids = {p["id"] for p in existing}
            new_only = [p for p in deduped if p["id"] not in existing_ids]
            existing.extend(new_only)
            merge_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
            rel = merge_path.relative_to(ROOT).as_posix()
            print(f"arXiv: appended {len(new_only)} of {len(deduped)} new papers into {rel}")
            print(rel)
            return
        # If the merge target doesn't exist, fall through to writing a new file.

    out = RAW_DIR / f"{to_date}.arxiv.json"
    out.write_text(json.dumps(deduped, indent=2, ensure_ascii=False), encoding="utf-8")
    rel = out.relative_to(ROOT).as_posix()
    print(f"arXiv total: {total} fetched, {len(deduped)} new unique papers")
    print(f"Wrote: {rel}")
    print(rel)


if __name__ == "__main__":
    main()
