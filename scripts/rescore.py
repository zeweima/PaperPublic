#!/usr/bin/env python3
"""Re-evaluate previously-fetched papers without re-fetching.

Useful when you change `keywords` or thresholds in `config.yaml` and
want past papers re-scored under the new criteria. This script:

  1. Reads every `papers/raw/YYYY-MM-DD.json` (the originals, not the .filtered ones)
  2. Concatenates them into one rescore-input file
  3. Tells you the path so you can hand it to the paper-filterer subagent
     in Claude Code (`/rescore` or manually)

It does NOT re-summarize or re-compose digests — that's a separate decision
based on whether the user wants to regenerate prior digests.

Usage:
    python scripts/rescore.py
    python scripts/rescore.py --since 2026-01-01     # only rescore from this date
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "papers" / "raw"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--since", help="YYYY-MM-DD; only include raw files from this date forward")
    args = p.parse_args()

    since = datetime.fromisoformat(args.since).date() if args.since else None

    all_papers = []
    raw_files = sorted(RAW_DIR.glob("*.json"))
    raw_files = [f for f in raw_files if not f.name.endswith(".filtered.json")
                 and not f.name.endswith(".test_sample.json")]
    for f in raw_files:
        try:
            file_date = datetime.fromisoformat(f.stem).date()
        except ValueError:
            continue
        if since and file_date < since:
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8-sig"))
        except Exception as e:
            print(f"  ! skip {f.name}: {e}")
            continue
        all_papers.extend(data)

    # Dedup on id (a paper may appear in multiple raw files because of lookback overlap).
    by_id = {}
    for p in all_papers:
        by_id.setdefault(p["id"], p)
    unique = list(by_id.values())

    out = RAW_DIR / "rescore_input.json"
    out.write_text(json.dumps(unique, indent=2, ensure_ascii=False), encoding="utf-8")
    rel = out.relative_to(ROOT).as_posix()
    print(f"Combined {len(raw_files)} raw files -> {len(unique)} unique papers")
    print(f"Wrote: {rel}")
    print()
    print("Next step (in Claude Code, in this directory):")
    print(f"  Spawn paper-filterer with input = {rel}")
    print("  Then optionally re-summarize / regenerate any digest(s) you care about.")
    print(rel)


if __name__ == "__main__":
    main()
