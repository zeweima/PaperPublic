# Paper Tracking System

Daily / weekly / monthly digest of new papers in 26 Earth / environmental science journals, filtered by your research interests, summarized, and emailed.

## Architecture

```
schtasks (Windows)
   │
   ├─ daily  08:00  →  claude -p "/daily"   ──┐
   ├─ weekly Mon    →  claude -p "/weekly"  ──┤   orchestrator (slash command)
   └─ monthly 1st   →  claude -p "/monthly" ──┘        │
                                                       ▼
              ┌───────────────────────┬────────────────┼──────────────────┐
              ▼                       ▼                ▼                  ▼
       scripts/fetch.py         paper-filterer    paper-summarizer   digest-writer
       (OpenAlex API)            (subagent)         (subagent ×N      (subagent)
                                                     in parallel)
                                                       │
                                                       ▼
                                                  papers/notes/
                                                  papers/daily|weekly|monthly/
                                                       │
                                                       ▼
                                                scripts/send_email.py
                                                  (Gmail SMTP)
```

**Why this split:** scripted fetch (no reasoning needed, just an API), then subagents for the parts that need a model — relevance scoring, summarization (in parallel, one paper per agent so each has a clean small context), and digest composition.

## One-time setup

The system uses **miniconda's base Python** at `C:\Users\zeweima2\AppData\Local\miniconda3\python.exe`. Bare `python` on PATH resolves to a Microsoft Store stub on this machine and won't work — that's why `papers/config.yaml` contains an explicit `python_path`.

1. **Python deps** (already installed; redo only if you reinstall conda):
   ```cmd
   "%LOCALAPPDATA%\miniconda3\python.exe" -m pip install pyyaml markdown
   ```

2. **Gmail app password.** Visit https://myaccount.google.com/apppasswords (2FA must be on). Generate one for "Mail". Then:
   ```cmd
   copy .env.example .env
   :: paste the 16-char password into .env (no spaces)
   ```

3. **Recipients.** Edit `papers/config.yaml` → `email.recipients`. Add other addresses one per line.

4. **Smoke test fetch:**
   ```cmd
   set PYTHONIOENCODING=utf-8
   "%LOCALAPPDATA%\miniconda3\python.exe" scripts\fetch.py --from 2026-04-20 --to 2026-04-27
   ```
   Expect 200–500 papers, a per-journal breakdown, and a JSON in `papers\raw\`.

5. **Smoke test email:** create a tiny markdown file and run
   ```cmd
   "%LOCALAPPDATA%\miniconda3\python.exe" scripts\send_email.py path\to\test.md --subject "test"
   ```

## Daily use

Inside Claude Code, in this directory:
- `/daily` — fetch, filter, summarize, digest, email
- `/weekly` — aggregate the past 7 daily digests, email
- `/monthly` — aggregate last month's weekly digests, email

## Schedule on Windows Task Scheduler

Open `taskschd.msc` and create three tasks, or run from cmd as admin:

```cmd
schtasks /create /tn "PaperTracker-Daily" ^
  /tr "cmd /c cd /d \"C:\Users\zeweima2\OneDrive - University of Illinois - Urbana\ClaudeCode\PaperSummarizing\" && claude -p \"/daily\"" ^
  /sc daily /st 08:00

schtasks /create /tn "PaperTracker-Weekly" ^
  /tr "cmd /c cd /d \"C:\Users\zeweima2\OneDrive - University of Illinois - Urbana\ClaudeCode\PaperSummarizing\" && claude -p \"/weekly\"" ^
  /sc weekly /d MON /st 09:00

schtasks /create /tn "PaperTracker-Monthly" ^
  /tr "cmd /c cd /d \"C:\Users\zeweima2\OneDrive - University of Illinois - Urbana\ClaudeCode\PaperSummarizing\" && claude -p \"/monthly\"" ^
  /sc monthly /mo first /d MON /st 09:00
```

(The monthly form above runs on the first Monday — adjust to `/d 1` for the 1st of the month if you prefer; `schtasks` syntax is finicky, the GUI is often easier.)

## How many papers get summarized

Two tiers per daily run:

| Tier | What | How they appear |
|---|---|---|
| **Top picks with note** | Score ≥ 8/10, capped at `max_summaries_per_run` (default 30) | Full per-paper note in `papers/notes/<id>.md`; rich entry in digest |
| **Abstract-only** | Filter passers (score ≥ 6) that didn't make the summarization cap | One-line entry in digest using the OpenAlex abstract directly |

This means your daily token cost is bounded: at most 30 summarizer subagent calls regardless of how many papers came in. Month-start (when AGU/Wiley journals batch-publish) and post-vacation runs don't blow up.

## Late-arriving papers and dedup

OpenAlex sometimes indexes a paper days or weeks after its `publication_date`. Two mechanisms handle this:

1. **`lookback_days: 35`** in config — every daily run re-queries the last 35 days, so a paper indexed late still gets caught on the next run.
2. **`state.seen_ids` + `state.seen_dois`** — every fetched paper's id *and* DOI are remembered; future runs silently drop duplicates before they reach the filter. Belt-and-suspenders catches the rare case where OpenAlex re-indexes a work under a new id.

## Re-scoring after a config change

If you change `keywords` or thresholds in `papers/config.yaml` and want past papers re-evaluated under the new criteria — without re-hitting OpenAlex:

```cmd
"%LOCALAPPDATA%\miniconda3\python.exe" scripts\rescore.py
```

This concatenates every `papers/raw/YYYY-MM-DD.json` into `rescore_input.json`. Then in Claude Code:
- Spawn the `paper-filterer` subagent on `rescore_input.json`
- Optionally re-summarize any newly-promoted papers and regenerate the relevant digest

Use `--since 2026-01-01` to limit the rescore window.

## Tuning

| Symptom | Fix |
|---|---|
| Too many low-relevance papers | Raise `relevance_threshold` in `papers/config.yaml` (e.g. 6 → 7) |
| Too few papers | Lower threshold, or add more keywords |
| Want fewer or more full notes per day | Adjust `max_summaries_per_run` (default 30) |
| Want stricter "top pick" bar | Raise `top_picks_threshold` (e.g. 8 → 9) |
| Add a journal | Look up its ISSN at https://portal.issn.org and add to `sources` |
| Missed papers indexed weeks late | Raise `lookback_days` (default 35) |
| Want to re-process a specific day | Delete that day's ids from `seen_ids` in `state.json` and re-run `/daily` |
| Changed `keywords` and want history rescored | Run `scripts/rescore.py` (see above) |

## File layout

```
papers/
  config.yaml          # interests, sources, thresholds, email
  state.json           # cursor + dedup set; updated by every run
  raw/<date>.json      # fetched paper lists (gitignored)
  raw/<date>.filtered.json   # filterer output
  notes/<id>.md        # per-paper summaries (gitignored)
  daily/<date>.md
  weekly/<YYYY-Www>.md
  monthly/<YYYY-MM>.md

scripts/
  fetch.py             # OpenAlex fetcher
  send_email.py        # SMTP sender

.claude/
  agents/
    paper-filterer.md
    paper-summarizer.md
    digest-writer.md
  commands/
    daily.md
    weekly.md
    monthly.md
```

## What runs where

| Step | Where | Why |
|---|---|---|
| Fetch from OpenAlex | Python script | Pure I/O, no reasoning |
| Score 0-10 relevance | Subagent (filterer) | Needs judgment over title+abstract |
| Per-paper summary | Subagent ×N parallel (summarizer) | Isolated context per paper, fast |
| Compose digest | Subagent (digest-writer) | Reads notes, themes, structures |
| Send email | Python script | Pure SMTP |
| Schedule | Windows Task Scheduler | Local, no remote infra |
