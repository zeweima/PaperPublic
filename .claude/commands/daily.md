---
description: Fetch new papers, filter, summarize, build daily digest, email it.
---

Run the daily paper-tracking pipeline. Today's date in UTC is the run date.

## Python interpreter

Read `python_path` from `papers/config.yaml` and use that for every Python invocation below. On this machine the correct path is `C:/Users/zeweima2/AppData/Local/miniconda3/python.exe` — bare `python` will hit a Windows Store stub and fail.

## Pipeline

### 1. Fetch
Run `<python_path> scripts/fetch.py` from the project root. Set env `PYTHONIOENCODING=utf-8` to avoid Windows cp1252 issues. The script reads `papers/state.json` for `last_daily` and uses a lookback (default 10 days) on OpenAlex `created_date` to catch papers indexed slightly late; dedup via `seen_ids` prevents repeats. Capture the path it prints on the last line — that is the raw JSON. Note today's date for use later.

### 2. Filter
Read the raw JSON to check the count.
- If empty, write a minimal "no new papers" digest to `papers/daily/<today>.md`, update state, skip emailing? No — still email so the user knows the system ran. Compose a one-line digest and proceed to step 6.
- Otherwise, spawn one `paper-filterer` subagent and pass the raw JSON path. Capture the filtered JSON path it prints.

### 3. Summarize (parallel, capped)
Read `max_summaries_per_run` from `papers/config.yaml` (default 30) and `top_picks_threshold` (default 8).

From the filtered JSON, build a **summarization list**:
- Take all papers with `top_pick: true` (i.e. score >= 8).
- Sort by score descending, then by venue prestige (Nature/Science/Sci Adv/PNAS first), then by date desc.
- Trim to the first `max_summaries_per_run` entries.

For each paper in that summarization list, spawn a `paper-summarizer` subagent. **Run them in parallel** — issue all the Agent tool calls in a single message. If there are more than 10, run them in batches of 10. Each subagent writes to `papers/notes/<id>.md` and prints its path.

Papers that pass the filter but are NOT on the summarization list (score 6-7, plus excess top picks beyond the cap) do **not** get a per-paper note. They will appear in the digest using their OpenAlex abstract directly — `digest-writer` reads the filtered JSON for those.

### 4. Compose digest
Spawn one `digest-writer` subagent with:
- `window: daily`
- the filtered JSON path
- the list of note paths
- output path: `papers/daily/<today>.md`

It will write the markdown file and print the path.

### 5. Update state
Read `papers/state.json`. Set `last_daily` to today's date. Append **every** paper id from the *raw* JSON (not just the filtered ones) to `seen_ids`, and append every non-null `doi` to `seen_dois`. Deduplicate both. We dedup on id+doi to catch the rare case where OpenAlex re-indexes a work under a new id. Write back.

### 6. Email
Run:
```
<python_path> scripts/send_email.py papers/daily/<today>.md --subject "Daily papers — <today>"
```

### 7. Report
Print a tight summary to the user:
- raw fetched / passed filter / top picks
- digest path
- email status (sent / failed)

## Failure handling
- Per-source fetch failures are logged by the script and the run continues — that's fine.
- If `paper-filterer` returns nothing kept, still write a digest stating "0 in-scope papers from N fetched".
- If email fails (e.g. missing SMTP_PASSWORD), continue and clearly print the error — the markdown digest is still saved on disk.
- The Python path comes from `papers/config.yaml` `python_path`. If that path no longer exists, fall back to `py -3` or `python3`.
