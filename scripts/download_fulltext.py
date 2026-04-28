#!/usr/bin/env python3
"""Download open-access full-text PDFs for top-pick papers.

Strategy:
  1. Try the OpenAlex `open_access.oa_url` field (already in the filtered JSON).
  2. If absent, query Unpaywall by DOI for any OA location they know about.
  3. Sanity-check the response is a real PDF (magic bytes %PDF) before saving;
     otherwise discard — paywall HTML pages would mislead the summarizer.

Saves to `papers/fulltext/<id>.pdf`. Skips papers whose PDF is already cached.

Usage:
  python scripts/download_fulltext.py papers/raw/2026-04-27.filtered.json
  python scripts/download_fulltext.py <filtered.json> --all   # not just top picks
"""
import argparse
import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.yaml"
FT_DIR = ROOT / "papers" / "fulltext"
UNPAYWALL = "https://api.unpaywall.org/v2/{doi}?email={email}"

# Wiley/AGU/etc. block scripted requests unless the User-Agent looks like a real
# browser AND a session cookie is present. We use a per-paper cookie jar that
# visits the landing page first to seed cookies, then requests the PDF.
BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
BROWSER_HEADERS = {
    "User-Agent": BROWSER_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
}

# Copernicus journals (open access) expose PDFs at a predictable URL derived from the DOI.
# DOI of form 10.5194/<journal>-<vol>-<page>-<year> maps to
#   https://<journal>.copernicus.org/articles/<vol>/<page>/<year>/<journal>-<vol>-<page>-<year>.pdf
COPERNICUS_RE = re.compile(r"^10\.5194/([a-z]+)-(\d+)-(\d+)-(\d{4})$")


def copernicus_pdf_url(doi):
    """If the DOI is a Copernicus journal article, return its direct PDF URL."""
    if not doi:
        return None
    raw = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    m = COPERNICUS_RE.match(raw)
    if not m:
        return None
    journal, vol, page, year = m.groups()
    return f"https://{journal}.copernicus.org/articles/{vol}/{page}/{year}/{journal}-{vol}-{page}-{year}.pdf"


def nature_pdf_url(doi):
    """Nature-family papers expose PDFs at https://www.nature.com/articles/<id>.pdf

    Works directly when the request originates from a subscribing IP (e.g. UIUC
    campus). For non-OA Nature articles, this is the main path that succeeds.
    DOI prefix `10.1038/` covers Nature, Nature Sustainability, Nature Climate
    Change, Nature Food, Nature Geoscience, Nature Water, Nature Comms, etc.
    """
    if not doi:
        return None
    raw = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    if not raw.startswith("10.1038/"):
        return None
    article_id = raw.split("/", 1)[1]
    return f"https://www.nature.com/articles/{article_id}.pdf"


def elsevier_api_fetch(doi, api_key, insttoken, dest):
    """Fetch a ScienceDirect PDF via Elsevier's Article Retrieval API.

    With a *free* dev.elsevier.com API key, this typically returns only a
    1-page teaser (cover/abstract page) — not the full article. To get the
    full text, you need an institutional `Insttoken` from your library, which
    is sent as the `X-ELS-Insttoken` header. UIUC researchers can request one
    via the library's e-resources team.

    This function:
      - sends both X-ELS-APIKey and (if available) X-ELS-Insttoken
      - downloads the PDF
      - VALIDATES the page count: if the result is 1 page and very small,
        treats it as a teaser-only failure so the caller can fall through
    """
    if not api_key or not doi:
        return False, "no api key"
    raw = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    if not raw.startswith("10.1016/"):
        return False, "not Elsevier"
    url = f"https://api.elsevier.com/content/article/doi/{urllib.parse.quote(raw, safe='')}"
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/pdf",
    }
    if insttoken:
        headers["X-ELS-Insttoken"] = insttoken
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        body = e.read()[:200]
        return False, f"HTTP {e.code}: {body!r}"
    except Exception as e:
        return False, f"{e}"
    if not data[:5].startswith(b"%PDF"):
        return False, f"not a PDF (got {data[:60]!r})"
    if len(data) < 10_000:
        return False, f"PDF too small ({len(data)} bytes)"

    # Detect teaser PDFs: free-key responses are 1-page covers without
    # References / Abstract markers. Don't cache these — let the caller fall
    # through to other strategies (e.g. abstract-only summarization).
    page_count_match = re.search(rb"/Count\s+(\d+)", data)
    page_count = int(page_count_match.group(1)) if page_count_match else None
    has_refs = b"References" in data or b"references" in data
    if page_count == 1 and not has_refs:
        return False, ("teaser only (1 page, no References) — your API key is the free tier; "
                       "request an institutional Insttoken from your library for full text")

    dest.write_bytes(data)
    suffix = " (full)" if has_refs else ""
    return True, f"{len(data)//1024} KB{suffix}"


def publisher_two_step(doi):
    """For a known publisher, return (label, landing_url, pdf_url) for cookie-seeded fetch.

    Many publishers (Wiley, AAAS, etc.) reject scripted PDF requests unless a
    session cookie is present. Visiting the article landing page first seeds
    the cookie; the PDF endpoint then returns successfully.

    Covered DOI prefixes:
      10.1029/  Wiley AGU imprint (GRL, WRR, GBC, JAMES, JGR-BG)
      10.1111/  Wiley general (GCB, etc.)
      10.1002/  Wiley general
      10.1126/  AAAS (Science, Science Advances)
    """
    if not doi:
        return None
    raw = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    if raw.startswith("10.1029/"):
        host = "agupubs.onlinelibrary.wiley.com"
        return ("wiley-agu", f"https://{host}/doi/{raw}", f"https://{host}/doi/pdfdirect/{raw}")
    if raw.startswith("10.1111/") or raw.startswith("10.1002/"):
        host = "onlinelibrary.wiley.com"
        return ("wiley", f"https://{host}/doi/{raw}", f"https://{host}/doi/pdfdirect/{raw}")
    if raw.startswith("10.1126/"):
        host = "www.science.org"
        return ("aaas", f"https://{host}/doi/{raw}", f"https://{host}/doi/pdf/{raw}")
    return None


def fetch_with_cookie_session(landing_url, pdf_url, dest):
    """Visit landing to seed cookies, then download the PDF. Returns (ok, msg)."""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = list(BROWSER_HEADERS.items())
    try:
        with opener.open(landing_url, timeout=30) as r:
            r.read(1)  # discard, we just need the cookies
    except Exception as e:
        return False, f"landing: {e}"
    pdf_req = urllib.request.Request(pdf_url, headers={
        **BROWSER_HEADERS,
        "Referer": landing_url,
        "Accept": "application/pdf,*/*",
    })
    try:
        with opener.open(pdf_req, timeout=90) as r:
            data = r.read()
    except Exception as e:
        return False, f"pdf: {e}"
    if not data[:5].startswith(b"%PDF"):
        return False, f"not a PDF (got {data[:48]!r})"
    if len(data) < 10_000:
        return False, f"PDF too small ({len(data)} bytes)"
    dest.write_bytes(data)
    return True, f"{len(data)//1024} KB"


def get_unpaywall_candidates(doi, email):
    """Query Unpaywall and return ordered list of candidate PDF URLs.

    Walks all oa_locations (publisher + repository copies), prefers explicit
    `url_for_pdf`, then transforms PMC landing pages to PDF URLs.
    """
    if not doi:
        return []
    raw = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    api_url = UNPAYWALL.format(doi=urllib.parse.quote(raw, safe=""), email=email)
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": BROWSER_UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
    except Exception:
        return []

    candidates = []
    locations = data.get("oa_locations") or []
    # Move best_oa_location to the front if present and not already in the list.
    best = data.get("best_oa_location")
    if best and best not in locations:
        locations = [best] + locations

    for loc in locations:
        if not loc:
            continue
        # Prefer explicit PDF URL.
        if loc.get("url_for_pdf"):
            candidates.append(loc["url_for_pdf"])
        # PMC landing page → PDF URL (PMC exposes PDFs at <article-url>pdf/).
        url = loc.get("url") or ""
        if "pmc.ncbi.nlm.nih.gov/articles/PMC" in url:
            base = url.rstrip("/")
            candidates.append(f"{base}/pdf/")
        # Bare landing page (last resort — most publishers gate this with HTML).
        if loc.get("url") and not loc.get("url_for_pdf"):
            candidates.append(loc["url"])

    # Dedup, preserving order.
    seen = set()
    deduped = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            deduped.append(c)
    return deduped


def download_pdf(url, dest):
    """Download a URL, verify %PDF magic bytes, save to dest. Returns (ok, msg)."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": BROWSER_UA,
            "Accept": "application/pdf,*/*",
        })
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        return False, f"download error: {e}"
    if not data:
        return False, "empty response"
    if not data[:5].startswith(b"%PDF"):
        return False, f"not a PDF (got {data[:64]!r})"
    if len(data) < 10_000:
        return False, f"PDF too small ({len(data)} bytes) — likely a stub"
    dest.write_bytes(data)
    return True, f"{len(data)//1024} KB"


def load_env_var(name):
    """Read VAR from os.environ or from .env file."""
    v = os.environ.get(name)
    if v:
        return v
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("filtered", help="Path to filtered JSON (output of paper-filterer)")
    p.add_argument("--all", action="store_true",
                   help="Try every filter-passer (default: top picks only)")
    p.add_argument("--limit", type=int, default=0,
                   help="Cap number of papers to attempt (0 = no cap)")
    args = p.parse_args()

    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    email = cfg.get("email", {}).get("from_addr", "anonymous@example.com")
    elsevier_key = load_env_var("ELSEVIER_API_KEY")
    elsevier_insttoken = load_env_var("ELSEVIER_INSTTOKEN")

    # Read with utf-8-sig in case the filterer wrote a BOM.
    papers = json.loads(Path(args.filtered).read_text(encoding="utf-8-sig"))
    if not args.all:
        papers = [p for p in papers if p.get("top_pick")]
    # Process highest-scoring first so --limit picks a meaningful subset.
    papers.sort(key=lambda p: (-p.get("score", 0), p.get("date", "")), reverse=False)
    if args.limit:
        papers = papers[: args.limit]

    FT_DIR.mkdir(parents=True, exist_ok=True)

    ok = skipped = failed = 0
    for paper in papers:
        pid = paper["id"]
        doi = paper.get("doi") or ""
        oa = paper.get("open_access") or {}

        dest = FT_DIR / f"{pid}.pdf"
        if dest.exists() and dest.stat().st_size > 10_000:
            skipped += 1
            continue

        # Try strategies in order:
        # 1. Copernicus DOI → direct PDF URL (HESS, GMD, ESS, ESurf, etc.)
        # 2. Wiley two-step (cookie-seeded landing then /doi/pdfdirect/<doi>) —
        #    handles AGU titles (GRL, WRR, GBC, JAMES, JGR-BG) on 10.1029
        #    and Wiley general (GCB on 10.1111, others on 10.1002)
        # 3. OpenAlex `oa_url` — usually direct PDFs for Copernicus / preprint hosts
        # 4. Unpaywall fallback (publisher + repo copies)
        success = False
        last_msg = "no candidates"
        attempts = 0

        # Strategy 1: Copernicus
        cop = copernicus_pdf_url(doi)
        if cop:
            attempts += 1
            ok_dl, msg = download_pdf(cop, dest)
            if ok_dl:
                print(f"  ok (copernicus): {pid} {msg}")
                success = True
            else:
                last_msg = f"copernicus: {msg}"

        # Strategy 1b: Nature family direct PDF (works from subscribing IP — e.g. UIUC campus)
        if not success:
            nat = nature_pdf_url(doi)
            if nat:
                attempts += 1
                ok_dl, msg = download_pdf(nat, dest)
                if ok_dl:
                    print(f"  ok (nature): {pid} {msg}")
                    success = True
                else:
                    last_msg = f"nature: {msg}"

        # Strategy 1c: Elsevier API (when ELSEVIER_API_KEY is set in .env).
        # Free-tier keys return a 1-page teaser; full text requires an
        # institutional Insttoken. The fetcher detects teasers and rejects them
        # so the cache stays clean and the orchestrator falls through to abstract.
        if not success and elsevier_key and doi and doi.replace("https://doi.org/", "").startswith("10.1016/"):
            attempts += 1
            ok_dl, msg = elsevier_api_fetch(doi, elsevier_key, elsevier_insttoken, dest)
            if ok_dl:
                print(f"  ok (elsevier-api): {pid} {msg}")
                success = True
            else:
                last_msg = f"elsevier-api: {msg}"

        # Strategy 2: publisher two-step (Wiley, AAAS) — only for OA papers
        if not success and (oa.get("is_oa") or oa.get("oa_status") in ("gold", "hybrid", "green", "bronze")):
            two_step = publisher_two_step(doi)
            if two_step:
                attempts += 1
                label, landing, pdf = two_step
                ok_dl, msg = fetch_with_cookie_session(landing, pdf, dest)
                if ok_dl:
                    print(f"  ok ({label}): {pid} {msg}")
                    success = True
                else:
                    last_msg = f"{label}: {msg}"

        # Strategy 3: OpenAlex oa_url
        if not success and oa.get("oa_url"):
            attempts += 1
            ok_dl, msg = download_pdf(oa["oa_url"], dest)
            if ok_dl:
                print(f"  ok (openalex): {pid} {msg}")
                success = True
            else:
                last_msg = f"openalex: {msg}"

        # Strategy 4: Unpaywall fallback
        if not success and doi:
            time.sleep(0.4)  # polite to Unpaywall
            for u in get_unpaywall_candidates(doi, email):
                attempts += 1
                ok_dl, msg = download_pdf(u, dest)
                if ok_dl:
                    print(f"  ok (unpaywall): {pid} {msg}")
                    success = True
                    break
                last_msg = f"unpaywall: {msg}"

        if success:
            ok += 1
        elif attempts == 0:
            failed += 1
            print(f"  fail: {pid} — no OA URL ({(paper.get('title') or '')[:60]!r})", file=sys.stderr)
        else:
            failed += 1
            print(f"  fail: {pid} — tried {attempts}, last: {last_msg}", file=sys.stderr)

    total = len(papers)
    print()
    print(f"Full-text: {ok} downloaded, {skipped} cached, {failed} unavailable (of {total})")
    print(f"Saved to: {FT_DIR.relative_to(ROOT).as_posix()}/")


if __name__ == "__main__":
    main()
