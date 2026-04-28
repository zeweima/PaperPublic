---
description: Aggregate the previous month's weekly digests into a monthly digest, email it.
---

Compose last month's digest. Run on the 1st of each month, covering the previous calendar month. **No fetching, no re-summarizing.**

Read `python_path` from `config.yaml` and use it for every Python invocation below.

## Pipeline

### 1. Determine the month
Today is the run date. The target month is the previous calendar month: `<YYYY>-<MM>`. Gather:
- **All `papers/daily/<YYYY>-<MM>-<DD>.md` files** in the target month — these are the primary input. The monthly digest synthesizes only papers the user has **checked** in those daily digests (lines starting with `- [x]` in the `## Checklist` section).
- All `papers/weekly/<YYYY>-W<ww>.md` files whose ISO week falls (mostly) in that month — passed only for the navigation appendix at the bottom of the monthly digest.
- Optionally the previous monthly digest `papers/monthly/<prev>.md` for trend comparison.

### 2. Compose
Spawn one `digest-writer-monthly` subagent with:
- **list of daily digest paths in the month** (the primary input; subagent parses checked items from these)
- list of weekly digest paths in the month (for the navigation appendix only)
- previous monthly digest path (if any)
- output path: `papers/monthly/<YYYY>-<MM>.md`

If no daily digests have any checked items, the subagent will produce a minimal "no papers were ticked" stub — that is expected behavior; do not retry.

### 3. Update state
Set `last_monthly` in `papers/state.json` to `<YYYY>-<MM>`.

### 4. Email
```
<python_path> scripts/send_email.py papers/monthly/<YYYY-MM>.md --subject "Monthly papers — <YYYY-MM>"
```

### 5. Cleanup old raw fetches
Run housekeeping to delete stale date-keyed raw JSONs. Notes, PDFs, and digests are preserved — only the raw fetch artifacts are removed.

```
<python_path> scripts/cleanup_raw.py
```

If you want to pre-check what would be deleted, run with `--dry-run` first. Keep-days behavior is controlled by `cleanup_raw.py` (default plus optional `--keep-days N` override).

### 6. Log the run

```
<python_path> scripts/log_run.py --type monthly --date <YYYY-MM> \
    --digest papers/monthly/<YYYY-MM>.md \
    --email-status <sent|failed> \
    --note "aggregated <K> daily digests, <C> checked papers"
```

### 7. Report
Print: digest path (**relative**, e.g. `papers/monthly/2026-04.md`), # source daily digests scanned, # checked papers found, # raw files cleaned up (from step 5 output), email status.
