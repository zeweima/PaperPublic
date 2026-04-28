#!/usr/bin/env python3
"""Fetch new papers from OpenAlex by journal ISSN, dedupe against state, write JSON.

Usage:
    python scripts/fetch.py                      # uses last_daily..today
    python scripts/fetch.py --from 2026-04-20    # override start
    python scripts/fetch.py --to   2026-04-27    # override end
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.yaml"
STATE_PATH = ROOT / "papers" / "state.json"
RAW_DIR = ROOT / "papers" / "raw"
OPENALEX = "https://api.openalex.org/works"


def reconstruct_abstract(idx):
    """OpenAlex returns abstracts as a {word: [positions]} inverted index."""
    if not idx:
        return ""
    pos = []
    for word, locs in idx.items():
        for loc in locs:
            pos.append((loc, word))
    pos.sort()
    return " ".join(w for _, w in pos)


def fetch_source(name, issns, from_date, to_date, contact):
    """Fetch papers by OpenAlex `publication_date`.

    Note: AGU / Wiley monthly titles (WRR, GCB, GBC, JAMES, JGR-BG, One Earth) tag
    every paper with the 1st-of-month issue date, so they appear in a single batch
    on/near month start rather than spread daily. A `lookback_days` of ~35 in
    config.yaml ensures we catch each new month's batch even on a daily cadence;
    dedup via state.seen_ids prevents resummarization. `from_created_date` /
    `from_updated_date` would solve this more elegantly but require a paid OpenAlex
    plan.
    """
    issn_filter = "|".join(issns)
    flt = (
        f"primary_location.source.issn:{issn_filter},"
        f"from_publication_date:{from_date},"
        f"to_publication_date:{to_date}"
    )
    params = {
        "filter": flt,
        "per-page": "200",
        "select": "id,doi,title,authorships,publication_date,abstract_inverted_index,primary_location,open_access",
        "mailto": contact,
    }
    url = f"{OPENALEX}?{urllib.parse.urlencode(params)}"
    # Retry with exponential backoff on rate limits.
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                data = json.loads(resp.read())
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 4:
                time.sleep(5 * (2 ** attempt))   # 5, 10, 20, 40 s
                continue
            print(f"  ! {name}: HTTP {e.code}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"  ! {name}: {e}", file=sys.stderr)
            return []
    out = []
    for w in data.get("results", []):
        oa = w.get("open_access") or {}
        out.append({
            "id": w["id"].rsplit("/", 1)[-1],
            "doi": w.get("doi"),
            "title": (w.get("title") or "").strip(),
            "authors": [a["author"]["display_name"] for a in w.get("authorships", [])][:10],
            "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
            "date": w.get("publication_date"),
            "venue": name,
            "url": w.get("doi") or w["id"],
            "open_access": {
                "is_oa": oa.get("is_oa"),
                "oa_url": oa.get("oa_url"),
                "oa_status": oa.get("oa_status"),  # "gold", "green", "hybrid", "bronze", or null
            },
        })
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from", dest="from_date")
    p.add_argument("--to", dest="to_date")
    p.add_argument("--force", action="store_true",
                   help="Overwrite an existing raw file for --to date")
    args = p.parse_args()

    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    # Dedup by id AND doi — OpenAlex very occasionally re-indexes a work under
    # a new id, so id-only dedup would let the paper through twice.
    seen_ids = set(state.get("seen_ids", []))
    seen_dois = set(state.get("seen_dois", []))

    today = datetime.now(timezone.utc).date()
    to_date = args.to_date or today.isoformat()

    if args.from_date:
        from_date = args.from_date
    elif state.get("last_daily"):
        last = datetime.fromisoformat(state["last_daily"]).date()
        lookback = int(config.get("lookback_days", 10))
        from_date = (last - timedelta(days=lookback)).isoformat()
    else:
        from_date = (today - timedelta(days=int(config.get("lookback_days", 10)))).isoformat()

    contact = config.get("email", {}).get("from_addr", "anonymous@example.com")
    print(f"Fetching {from_date} -> {to_date} ({len(config['sources'])} sources)")

    all_new = []
    total_fetched = 0
    for i, src in enumerate(config["sources"]):
        if i > 0:
            time.sleep(0.15)   # be polite — stay under 10/s for OpenAlex polite pool
        papers = fetch_source(src["name"], src["issns"], from_date, to_date, contact)
        new = [
            p for p in papers
            if p["id"] not in seen_ids
            and (not p.get("doi") or p["doi"] not in seen_dois)
        ]
        total_fetched += len(papers)
        if papers:
            print(f"  {src['name']}: {len(papers)} fetched, {len(new)} new")
        all_new.extend(new)

    # Dedup in case the same paper appears in two journal-result lists.
    by_id = {}
    for p in all_new:
        by_id.setdefault(p["id"], p)
    deduped = list(by_id.values())

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_file = RAW_DIR / f"{to_date}.json"
    rel = out_file.relative_to(ROOT).as_posix()
    if out_file.exists() and not args.force:
        print(f"Total: {total_fetched} fetched, {len(deduped)} new unique papers")
        print(f"REFUSING to overwrite existing {rel} (use --force).")
        print(f"Existing file preserved.")
        # Last line: machine-readable relative path for the orchestrator.
        print(rel)
        return
    out_file.write_text(json.dumps(deduped, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Total: {total_fetched} fetched, {len(deduped)} new unique papers")
    print(f"Wrote: {rel}")
    # Last line: machine-readable relative path for the orchestrator.
    print(rel)


if __name__ == "__main__":
    main()
