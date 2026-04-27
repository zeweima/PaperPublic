---
description: Open a visible Chrome to download Elsevier (ScienceDirect) full-text PDFs for today's top picks. Runs interactively — solve any captchas as they appear.
---

Run the interactive browser-based downloader for today's pending Elsevier (and optionally ACS) top picks.

This is an **interactive** command — it opens a visible Chrome window and may ask you to solve captchas. Run it when you have 1-3 minutes to babysit it (typically morning, after `/daily` ran overnight). Not safe to run from the scheduler.

## Pipeline

### 1. Identify the filtered JSON for today
Default: `papers/raw/<today>.filtered.json`. If a more recent date exists, use that instead. If no filtered JSON exists, exit with a clear message ("run /daily first").

### 2. Run the browser downloader
Read `python_path` from `papers/config.yaml`. Run:

```
<python_path> scripts/download_fulltext_browser.py papers/raw/<today>.filtered.json --max 10
```

By default this attempts only Elsevier (`10.1016/`). To also try ACS (`10.1021/`), pass `--publishers 10.1016 10.1021`.

The script:
- Skips papers already in `papers/fulltext/<id>.pdf`
- Sorts by score descending and stops after `--max` (default 10)
- Opens a visible Chrome window via undetected-chromedriver
- For each paper: navigates → waits → if a Press & Hold/captcha appears, prompts the user (5 min timeout per paper) → clicks View PDF → moves the downloaded file into `papers/fulltext/<id>.pdf`

### 3. Re-summarize
After the browser run, the new PDFs are in `papers/fulltext/`. To get richer notes for those specific papers, re-run the summarizer subagents *only* on the papers whose `<id>.pdf` was just added (don't re-run all of them — that wastes tokens).

You can do this by:
- Listing PDFs added since the script started (compare directory listing before / after)
- Spawning `paper-summarizer` for each, in parallel
- The summarizer agent already prefers the PDF over the abstract, so notes will upgrade automatically

### 4. Re-compose the digest (optional)
If you want the daily digest's "top picks" to reflect the upgraded notes, spawn `digest-writer` again with the same inputs and overwrite `papers/daily/<today>.md`. Otherwise leave the digest as-is and the upgrades will surface in the weekly digest.

### 5. Report
Print:
- # papers attempted / downloaded / failed (from the script's output)
- # notes regenerated
- whether the daily digest was refreshed

## Failure handling

- If `undetected-chromedriver` is not installed: tell the user to run `<python_path> -m pip install undetected-chromedriver`
- If Chrome isn't found: undetected-chromedriver auto-detects; if it fails, the user may need a `version_main` override in `setup_driver()` matching their Chrome major version
- If the bot block appears and the user doesn't press Enter within 5 min, the script skips that paper and moves on — don't retry within the same run
