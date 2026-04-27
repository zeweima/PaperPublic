#!/usr/bin/env python3
"""Append a structured run record to papers/runs.jsonl.

One JSON object per line — easy to grep, parse with `jq`, or load with pandas
later for statistics. Called by /daily, /weekly, /monthly slash commands at
the end of each pipeline.

Usage:
  python scripts/log_run.py --type daily --date 2026-04-27 \
      --fetched 443 --filtered 158 --top-picks 92 --summarized 30 \
      --fulltext 18 --digest papers/daily/2026-04-27.md \
      --email-status sent
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "papers" / "runs.jsonl"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--type", required=True, choices=["daily", "weekly", "monthly"])
    p.add_argument("--date", required=True, help="Run date / window label (YYYY-MM-DD or YYYY-Www or YYYY-MM)")
    p.add_argument("--fetched", type=int, default=0)
    p.add_argument("--filtered", type=int, default=0)
    p.add_argument("--top-picks", dest="top_picks", type=int, default=0)
    p.add_argument("--summarized", type=int, default=0,
                   help="How many papers got per-paper notes")
    p.add_argument("--fulltext", type=int, default=0,
                   help="How many full-text PDFs were downloaded")
    p.add_argument("--digest", help="Absolute path of the digest .md")
    p.add_argument("--email-status", default="unknown",
                   choices=["sent", "failed", "skipped", "unknown"])
    p.add_argument("--note", default="")
    args = p.parse_args()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "type": args.type,
        "date": args.date,
        "fetched": args.fetched,
        "filtered": args.filtered,
        "top_picks": args.top_picks,
        "summarized": args.summarized,
        "fulltext_downloaded": args.fulltext,
        "digest": args.digest,
        "email_status": args.email_status,
        "note": args.note,
    }
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Logged {args.type} run on {args.date}: "
          f"{args.fetched} fetched, {args.filtered} filtered, "
          f"{args.summarized} summarized, {args.fulltext} fulltext, email={args.email_status}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
