---
description: Aggregate the past 7 daily digests into a weekly digest, email it.
---

Compose this week's digest. **No fetching, no re-summarizing** — pure aggregation of existing daily digests.

Read `python_path` from `papers/config.yaml` for any Python invocation.

## Pipeline

### 1. Determine the week
Use the ISO calendar week ending today (Monday–Sunday). Compute `<YYYY>-W<ww>`. The 7 dates of that week are the candidate daily digest filenames in `papers/daily/`. Missing days are fine — just skip them.

### 2. Compose
Spawn one `digest-writer` subagent with:
- `window: weekly`
- list of daily digest paths that exist
- previous weekly digest path (if `papers/weekly/<YYYY>-W<ww-1>.md` exists)
- output path: `papers/weekly/<YYYY>-W<ww>.md`

### 3. Update state
Set `last_weekly` in `papers/state.json` to the week label. Do not touch `seen_ids`.

### 4. Email
```
<python_path> scripts/send_email.py papers/weekly/<YYYY-Www>.md --subject "Weekly papers — <YYYY-Www>"
```

### 5. Log the run

```
<python_path> scripts/log_run.py --type weekly --date <YYYY-Www> \
    --digest papers/weekly/<YYYY-Www>.md \
    --email-status <sent|failed> \
    --note "aggregated <K> daily digests"
```

### 6. Report
Print: digest path (**relative**, e.g. `papers/weekly/2026-W17.md`), # source daily digests included, email status.
