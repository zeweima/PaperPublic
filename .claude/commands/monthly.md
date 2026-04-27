---
description: Aggregate the previous month's weekly digests into a monthly digest, email it.
---

Compose last month's digest. Run on the 1st of each month, covering the previous calendar month. **No fetching, no re-summarizing.**

Read `python_path` from `papers/config.yaml` for any Python invocation.

## Pipeline

### 1. Determine the month
Today is the run date. The target month is the previous calendar month: `<YYYY>-<MM>`. Gather:
- All `papers/weekly/<YYYY>-W<ww>.md` files whose ISO week falls (mostly) in that month.
- Optionally the previous monthly digest `papers/monthly/<prev>.md` for trend comparison.

### 2. Compose
Spawn one `digest-writer` subagent with:
- `window: monthly`
- list of weekly digest paths
- previous monthly digest path (if any)
- output path: `papers/monthly/<YYYY>-<MM>.md`

### 3. Update state
Set `last_monthly` in `papers/state.json` to `<YYYY>-<MM>`.

### 4. Email
```
<python_path> scripts/send_email.py papers/monthly/<YYYY-MM>.md --subject "Monthly papers — <YYYY-MM>"
```

### 5. Log the run

```
<python_path> scripts/log_run.py --type monthly --date <YYYY-MM> \
    --digest papers/monthly/<YYYY-MM>.md \
    --email-status <sent|failed> \
    --note "aggregated <K> weekly digests"
```

### 6. Report
Print: digest path (**relative**, e.g. `papers/monthly/2026-04.md`), # source weekly digests, email status.
