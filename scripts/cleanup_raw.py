#!/usr/bin/env python3
"""Delete date-keyed raw fetch JSONs older than --keep-days (default 60).

Removes files matching:
  papers/raw/YYYY-MM-DD.json
  papers/raw/YYYY-MM-DD.filtered.json
  papers/raw/YYYY-MM-DD.arxiv.json

Leaves alone:
  - per-paper notes (papers/notes/<id>.md)
  - full-text PDFs (papers/fulltext/<id>.pdf)
  - generated digests (papers/daily|weekly|monthly/*.md)
  - state.json, runs.jsonl, rescore_input.json, anything not date-keyed

After cleanup, re-running scripts/rescore.py will only see raw files within the
retention window — so a keyword change can re-evaluate the last 2 months of
papers, not all history. Notes and digests are preserved, so older summaries
remain available even if their raw JSON is gone.

Usage:
  python scripts/cleanup_raw.py                # keep last 60 days
  python scripts/cleanup_raw.py --keep-days 90 # keep last 90 days
  python scripts/cleanup_raw.py --dry-run      # show what would be deleted
"""
import argparse
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "papers" / "raw"

# Match anything starting with YYYY-MM-DD (e.g. 2026-04-27.json,
# 2026-04-27.filtered.json, 2026-04-27.arxiv.json, 2026-04-27.test_sample.json).
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--keep-days", type=int, default=60,
                   help="Keep raw files with date >= today - keep-days (default 60)")
    p.add_argument("--dry-run", action="store_true",
                   help="List what would be deleted, but don't remove anything")
    args = p.parse_args()

    if not RAW_DIR.exists():
        print(f"No raw dir at {RAW_DIR.relative_to(ROOT).as_posix()} — nothing to do.")
        return

    today = datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=args.keep_days)

    # Group files by date so we can show them together in output.
    candidates = []
    skipped = []
    for f in sorted(RAW_DIR.iterdir()):
        if not f.is_file():
            continue
        m = DATE_PREFIX_RE.match(f.name)
        if not m:
            skipped.append(f.name)
            continue
        try:
            file_date = datetime.fromisoformat(m.group(1)).date()
        except ValueError:
            skipped.append(f.name)
            continue
        if file_date < cutoff:
            candidates.append((file_date, f))

    if not candidates:
        print(f"Nothing older than {cutoff.isoformat()} (keep-days={args.keep_days}).")
        if skipped:
            print(f"  ({len(skipped)} non-date-keyed file(s) left alone: {skipped[:3]}{'...' if len(skipped) > 3 else ''})")
        return

    candidates.sort()
    print(f"Cutoff: {cutoff.isoformat()} (keep last {args.keep_days} days)")
    print(f"{'Would delete' if args.dry_run else 'Deleting'} {len(candidates)} file(s):")
    total_bytes = 0
    for d, f in candidates:
        size = f.stat().st_size
        total_bytes += size
        rel = f.relative_to(ROOT).as_posix()
        print(f"  [{d}] {rel} ({size//1024} KB)")
        if not args.dry_run:
            f.unlink()

    print(f"\n{'Would free' if args.dry_run else 'Freed'} {total_bytes//1024} KB")


if __name__ == "__main__":
    main()
