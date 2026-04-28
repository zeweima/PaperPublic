#!/usr/bin/env python3
"""Split / merge / clean JSON-array files of papers, for parallel filter subagents.

The paper-filterer agent runs on bounded chunks rather than the full daily fetch
so each subagent has a manageable context window and we can score papers in
parallel.

Subcommands
-----------
  split <input> [--max 30] [--out-prefix <prefix>]
      Split <input> (a JSON array) into chunks of at most --max items each.
      Writes <prefix>.000.json, <prefix>.001.json, ... and prints relative paths,
      one per line, to stdout (so the orchestrator can capture them).
      Default --out-prefix: <input-stem>.chunk

  merge <output> <chunk1.json|glob> [<chunk2.json|glob> ...]
      Concatenate JSON arrays from each chunk path (globs accepted) into a
      single output array. Dedupes on `id`. Useful for combining filterer
      outputs back into one filtered.json.

  clean <pattern>
      Delete files matching the glob (relative to project root).
      Used at the end of a chunked run to remove the per-chunk artifacts.

Usage examples
--------------
  python scripts/chunk_papers.py split papers/raw/2026-04-27.json --max 50
  python scripts/chunk_papers.py merge papers/raw/2026-04-27.filtered.json \\
      "papers/raw/2026-04-27.chunk.*.filtered.json"
  python scripts/chunk_papers.py clean "papers/raw/2026-04-27.chunk.*"
"""
import argparse
import glob as glob_mod
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _resolve(path_str: str) -> Path:
    """Resolve a path relative to project root if not absolute."""
    p = Path(path_str)
    return p if p.is_absolute() else (ROOT / p)


def _expand_globs(patterns):
    """Expand glob patterns and plain paths. Returns sorted unique resolved paths."""
    out = []
    seen = set()
    for pat in patterns:
        full = _resolve(pat).as_posix()
        if any(ch in pat for ch in "*?["):
            for m in sorted(glob_mod.glob(full)):
                if m not in seen:
                    seen.add(m); out.append(Path(m))
        else:
            if full not in seen:
                seen.add(full); out.append(Path(full))
    return out


def cmd_split(args):
    inp = _resolve(args.input)
    if not inp.exists():
        print(f"ERROR: input not found: {inp}", file=sys.stderr); sys.exit(1)

    data = json.loads(inp.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        print(f"ERROR: input must be a JSON array, got {type(data).__name__}", file=sys.stderr)
        sys.exit(1)

    if args.out_prefix:
        prefix = args.out_prefix
    else:
        # e.g. papers/raw/2026-04-27.json -> papers/raw/2026-04-27.chunk
        prefix = inp.with_suffix("").as_posix() + ".chunk"

    n = max(1, args.max)
    paths = []
    for i in range(0, len(data), n):
        chunk_idx = i // n
        chunk_data = data[i:i + n]
        path = Path(f"{prefix}.{chunk_idx:03d}.json")
        path.write_text(
            json.dumps(chunk_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        paths.append(path)

    rels = []
    for p in paths:
        try:
            rels.append(p.relative_to(ROOT).as_posix())
        except ValueError:
            rels.append(p.as_posix())

    print(f"Split {len(data)} papers into {len(paths)} chunk(s) of <= {n}:", file=sys.stderr)
    for r in rels:
        print(f"  {r}", file=sys.stderr)
    # Machine-readable on stdout: one path per line.
    for r in rels:
        print(r)


def cmd_merge(args):
    output = _resolve(args.output)
    chunk_paths = _expand_globs(args.chunks)
    if not chunk_paths:
        print(f"ERROR: no chunks matched any of {args.chunks}", file=sys.stderr)
        sys.exit(1)

    merged = []
    seen_ids = set()
    for p in chunk_paths:
        if not p.exists():
            print(f"  ! skip missing: {p}", file=sys.stderr); continue
        try:
            chunk = json.loads(p.read_text(encoding="utf-8-sig"))
        except Exception as e:
            print(f"  ! skip unreadable {p.name}: {e}", file=sys.stderr); continue
        for item in chunk:
            iid = item.get("id") if isinstance(item, dict) else None
            if iid and iid in seen_ids:
                continue
            if iid:
                seen_ids.add(iid)
            merged.append(item)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(merged, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    try:
        rel = output.relative_to(ROOT).as_posix()
    except ValueError:
        rel = output.as_posix()
    print(f"Merged {len(chunk_paths)} chunk(s) -> {len(merged)} unique papers", file=sys.stderr)
    print(f"Wrote: {rel}", file=sys.stderr)
    print(rel)


def cmd_clean(args):
    matches = _expand_globs([args.pattern])
    deleted = 0
    for m in matches:
        try:
            m.unlink()
            deleted += 1
        except Exception as e:
            print(f"  ! {m}: {e}", file=sys.stderr)
    print(f"Cleaned {deleted} file(s) matching {args.pattern}", file=sys.stderr)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("split", help="Split a JSON array into chunks of <= --max items")
    sp.add_argument("input", help="Path to JSON array (e.g. papers/raw/<date>.json)")
    sp.add_argument("--max", type=int, default=50, help="Max items per chunk (default 50)")
    sp.add_argument("--out-prefix", help="Output prefix; default <input-stem>.chunk")
    sp.set_defaults(fn=cmd_split)

    sm = sub.add_parser("merge", help="Concatenate chunk JSON arrays into one (dedup by id)")
    sm.add_argument("output", help="Output JSON path")
    sm.add_argument("chunks", nargs="+",
                    help="Chunk paths or globs (e.g. 'papers/raw/<date>.chunk.*.filtered.json')")
    sm.set_defaults(fn=cmd_merge)

    sc = sub.add_parser("clean", help="Delete files matching a glob")
    sc.add_argument("pattern", help="Glob relative to project root")
    sc.set_defaults(fn=cmd_clean)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
