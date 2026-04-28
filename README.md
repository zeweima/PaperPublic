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

The system uses **miniconda's base Python** at `C:\Users\zeweima2\AppData\Local\miniconda3\python.exe`. Bare `python` on PATH resolves to a Microsoft Store stub on this machine and won't work — that's why `config.yaml` contains an explicit `python_path`.

1. **Python deps** (already installed; redo only if you reinstall conda):
   ```cmd
   "%LOCALAPPDATA%\miniconda3\python.exe" -m pip install pyyaml markdown
   ```

2. **Gmail app password.** Visit https://myaccount.google.com/apppasswords (2FA must be on). Generate one for "Mail". Then:
   ```cmd
   copy .env.example .env
   :: paste the 16-char password into .env (no spaces)
   ```

3. **Recipients.** Edit `config.yaml` → `email.recipients`. Add other addresses one per line.

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
- `/daily` — fetch, filter, summarize, digest, email (autonomous, scheduled overnight)
- `/elsevier-catchup` — interactive Chrome run to upgrade Elsevier top picks from abstract to full-text. Run in the morning if `/daily` printed the "Elsevier top picks without full text" hint.
- `/weekly` — aggregate the past 7 daily digests, email
- `/monthly` — aggregate last month's weekly digests, email
- `/status` — one-screen health check (state cursors, cache sizes, env-var presence, recent runs, scheduled tasks)

## Schedule on Windows Task Scheduler

Open `taskschd.msc` and create three tasks, or run from cmd as admin:

```cmd
schtasks /create /tn "PaperTracker-Daily" ^
  /tr "cmd /c cd /d \"C:\Users\zeweima2\OneDrive - University of Illinois - Urbana\ClaudeCode\PaperSummarizing\" && claude -p \"/daily\"" ^
  /sc daily /st 02:00

schtasks /create /tn "PaperTracker-Weekly" ^
  /tr "cmd /c cd /d \"C:\Users\zeweima2\OneDrive - University of Illinois - Urbana\ClaudeCode\PaperSummarizing\" && claude -p \"/weekly\"" ^
  /sc weekly /d MON /st 03:00

schtasks /create /tn "PaperTracker-Monthly" ^
  /tr "cmd /c cd /d \"C:\Users\zeweima2\OneDrive - University of Illinois - Urbana\ClaudeCode\PaperSummarizing\" && claude -p \"/monthly\"" ^
  /sc monthly /mo first /d MON /st 04:00
```

(The monthly form above runs on the first Monday — adjust to `/d 1` for the 1st of the month if you prefer; `schtasks` syntax is finicky, the GUI is often easier.)

## Full-text PDFs

For top picks the pipeline tries to download the open-access PDF before summarizing. The summarizer reads the PDF directly (Claude's Read tool supports PDFs natively; we read `pages: "1-12"` covering abstract / intro / methods / key results) — much richer than abstract-only.

### When PDFs are retrieved

**Only for top picks** — that is, papers with score ≥ `top_picks_threshold` (default 8) that also fall within `max_summaries_per_run` (default 30). These are the papers that get a per-paper note, so they're the ones that benefit from richer source text. Score 6–7 papers stay abstract-only; the cost/benefit doesn't justify the download time.

The download happens between the filter step and the summarize step in `/daily`. PDFs are cached in [`papers/fulltext/<id>.pdf`](papers/fulltext/) — re-runs skip already-cached papers.

### How OA papers are retrieved

The downloader tries strategies in order, stopping at the first success:

1. **Copernicus DOI transform** — for DOI prefix `10.5194/`, build the direct PDF URL (`https://<journal>.copernicus.org/articles/.../<journal>-X-Y-Z.pdf`). No API call needed.
2. **Publisher cookie session** — for OA papers from Wiley AGU (`10.1029/`), Wiley general (`10.1111/`, `10.1002/`), and AAAS (`10.1126/`), visit the article landing page first to seed a session cookie, then request `/doi/pdfdirect/<doi>` (Wiley) or `/doi/pdf/<doi>` (AAAS). This is what unlocks WRR / GRL / GBC / JAMES / JGR-BG / GCB / Sci Adv even though they "look paywalled" to a naive script.
3. **OpenAlex `oa_url`** — already populated in fetched data; works for many smaller OA journals.
4. **Unpaywall API fallback** — by DOI; walks all `oa_locations` (publisher + repository copies) for a `url_for_pdf`.

Each downloaded blob is verified for the `%PDF` magic-byte signature, so paywall HTML pages don't pollute the cache.

### Realistic hit-rate by publisher (your sources)

The numbers below assume the script runs from a **subscribing IP** — i.e. on UIUC campus or via UIUC VPN. From a non-campus connection, paywalled-but-IP-accessible papers (Nature, IOP, etc.) drop substantially; OA papers (Wiley AGU, Sci Adv, Copernicus, arXiv) are unaffected.

| Publisher / journal group | DOI prefix | Strategy that works | Hit rate (campus) |
|---|---|---|---|
| Copernicus (HESS, GMD) | 10.5194 | Copernicus transform | ~95% |
| Wiley AGU (GRL, WRR, GBC, JAMES, JGR-BG, Earth's Future, JGR ML&C) | 10.1029 | Wiley two-step cookies | ~95% |
| Wiley general (Global Change Biology) | 10.1111 | Wiley two-step cookies | ~80% |
| AAAS (Science Advances) | 10.1126/sciadv | AAAS two-step cookies | ~80% |
| AAAS (Science) | 10.1126/science | AAAS two-step cookies | ~30% (most still paywalled even on campus) |
| **Nature family (Nature, Sustainability, Climate, Food, Geoscience, Water)** | 10.1038 | **Nature direct URL** | **~95% on campus, ~25% off-campus** |
| IOP (ERL) | 10.1088 | OpenAlex / Unpaywall | ~70% |
| PNAS | 10.1073 | OpenAlex / Unpaywall | ~50% |
| arXiv preprints | n/a | OpenAlex `oa_url` direct | 100% |
| Elsevier (AgrForMet, FCR, Geoderma, S&TR, Water Research, Soil Biol Biochem, One Earth) | 10.1016 | — | ~5% (ScienceDirect / Radware bot block, even on campus) |
| ACS (ES&T) | 10.1021 | — | ~5% (similar bot block) |
| Springer (Biogeochemistry) | 10.1007 | OpenAlex / Unpaywall | ~30% |

When no OA / accessible copy is found, the summarizer falls back to the abstract. The note's `Source:` field records which source was used (`full text` vs `abstract`).

### Notes on access

- **Campus IP for paywalled journals** — when running this on UIUC campus (or via UIUC VPN), the system gets institutional access automatically because the publisher sees the request from `*.illinois.edu`. The Nature direct-URL strategy specifically depends on this. Off-campus, fewer Nature-family papers will succeed.
- **Wiley OA journals** — WRR, GRL, JAMES, GBC, JGR-BG, Earth's Future, JGR ML&C are all gold-OA. They previously failed because Wiley's Cloudflare layer blocks scripted PDF requests until a session cookie is present. The cookie-seeded two-step fetch now handles this; these download reliably.
- **Elsevier — needs API key + Institutional Token for full text.** ScienceDirect's web layer uses Radware Bot Manager (JS fingerprinting); it rejects scripted requests **regardless of IP or wait time**, so slowing the pipeline does *not* help. The Elsevier API can bypass Radware, but a free `dev.elsevier.com` key alone returns only a 1-page teaser (cover page) — not the full article. Full text requires a `X-ELS-Insttoken` header issued by your institution.
  - **What you have now** (`ELSEVIER_API_KEY` set, no Insttoken): the downloader tries the API, gets a teaser, detects it (1 page, no References), rejects it, and falls back to abstract-only.
  - **To unlock full text**: contact a UIUC science librarian or open a support request at Elsevier and ask them to associate your API key with the UIUC institution (they'll issue an Insttoken). Add it to `.env` as `ELSEVIER_INSTTOKEN=...`. The downloader picks it up automatically.
  - **Without Insttoken**: Elsevier journals (`10.1016/*` — AgrForMet, FCR, Geoderma, S&TR, Water Research, SBB, One Earth) stay abstract-only. That's still useful — abstracts for these journals are usually substantive 200-300 word summaries.
  - **Manual escape hatch**: if there's a particular Elsevier paper you want full-text on, download it from your browser into `papers/fulltext/<id>.pdf`. The summarizer will pick it up automatically.
- **ACS** — same JS bot-detection story as Elsevier, but ACS doesn't have a free public API equivalent. ACS papers stay abstract-only.

## Sources

The system pulls from two sources, deduped against each other and against state:

- **OpenAlex** — 29 journals (see `config.yaml` `sources` list). Includes the Earth-system stack (Copernicus, AGU/Wiley, Elsevier env titles, Nature/Science family), the new AGU OA journals (Earth's Future, JGR ML&C, Nature Water), and the rest.
- **arXiv** — preprints in 6 categories (`physics.ao-ph`, `physics.flu-dyn`, `cs.LG`, `stat.ML`, `eess.IV`, `cs.CV`). Always OA, always with full-text PDFs available. Caught by the same filterer / summarizer / digest pipeline as journal articles. arXiv preprints often appear weeks before journal publication, so this is the leading edge of the digest.

The arXiv fetcher (`scripts/fetch_arxiv.py`) runs after the OpenAlex fetcher in `/daily`, appending its results into the same raw JSON. To disable arXiv, set `arxiv.enabled: false` in config.

## Run log

Every `/daily`, `/weekly`, `/monthly` invocation appends one JSON line to [`papers/runs.jsonl`](papers/runs.jsonl):

```json
{"timestamp":"2026-04-27T13:00:00+00:00","type":"daily","date":"2026-04-27","fetched":443,"filtered":158,"top_picks":92,"summarized":30,"fulltext_downloaded":18,"digest":"papers/daily/2026-04-27.md","email_status":"sent","note":""}
```

Quick views:
```cmd
:: last 10 runs
"%LOCALAPPDATA%\miniconda3\python.exe" -c "from pathlib import Path; [print(l) for l in Path('papers/runs.jsonl').read_text(encoding='utf-8').splitlines()[-10:]]"

:: weekly summary (totals by month)
"%LOCALAPPDATA%\miniconda3\python.exe" -c "import json; from collections import Counter; from pathlib import Path; d=[json.loads(l) for l in Path('papers/runs.jsonl').read_text(encoding='utf-8').splitlines() if l]; c=Counter((r['date'][:7], r['type']) for r in d); [print(k, v) for k,v in sorted(c.items())]"
```

If you prefer `jq`-style filtering, the format is one-object-per-line standard JSONL.

## Script changelog

See [CHANGELOG.md](CHANGELOG.md) for what changed in scripts, agents, and slash commands over time, with context on *why*.

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

If you change `keywords` or thresholds in `config.yaml` and want past papers re-evaluated under the new criteria — without re-hitting OpenAlex:

```cmd
"%LOCALAPPDATA%\miniconda3\python.exe" scripts\rescore.py
```

This concatenates every `papers/raw/YYYY-MM-DD.json` into `rescore_input.json`. Then in Claude Code:
- Spawn the `paper-filterer` subagent on `rescore_input.json`
- Optionally re-summarize any newly-promoted papers and regenerate the relevant digest

Use `--since 2026-01-01` to limit the rescore window.

## Model selection

Each subagent has an explicit `model:` line in its YAML frontmatter so heavy work doesn't go to Opus by default:

| Agent | Model | Why |
|---|---|---|
| `paper-filterer` | `haiku` | Bulk 0–10 scoring against a fixed rubric — pattern matching, not deep reasoning. Roughly 15× cheaper than Opus, no quality cliff. |
| `paper-summarizer` | `sonnet` | Structured extraction from 12-page PDFs and abstracts. Quality matters because notes feed the digest. ~5× cheaper than Opus and reliably captures numbers. |
| `digest-writer` | `sonnet` | Composition + theming over ~30 notes + 150 abstracts. ~5× cheaper, single call per digest so cost impact is small either way. |

**Cost comparison** (typical day: 250 fetched, 30 summarized, 1 digest):

| Stage | All Opus | Tiered (current) |
|---|---:|---:|
| Filter | ~$3.75 | ~$0.25 |
| Summarize | ~$13.50 | ~$2.70 |
| Digest-write | ~$0.90 | ~$0.18 |
| **Total / day** | **~$18** | **~$3** |
| **Annual (daily run)** | **~$6,500** | **~$1,100** |

The aliases (`haiku`, `sonnet`, `opus`) auto-resolve to the latest snapshot of each tier — no need to bump version IDs when Anthropic ships new models. To change, edit the `model:` line in [`.claude/agents/<name>.md`](.claude/agents/). For a one-off run at higher quality (e.g. monthly digest), pass `model: opus` to the specific Agent invocation.

## Tuning

| Symptom | Fix |
|---|---|
| Too many low-relevance papers | Raise `relevance_threshold` in `config.yaml` (e.g. 6 → 7) |
| Too few papers | Lower threshold, or add more keywords |
| Want fewer or more full notes per day | Adjust `max_summaries_per_run` (default 30) |
| Want stricter "top pick" bar | Raise `top_picks_threshold` (e.g. 8 → 9) |
| Add a journal | Look up its ISSN at https://portal.issn.org and add to `sources` |
| Missed papers indexed weeks late | Raise `lookback_days` (default 35) |
| Want to re-process a specific day | Delete that day's ids from `seen_ids` in `state.json` and re-run `/daily` |
| Changed `keywords` and want history rescored | Run `scripts/rescore.py` (see above) |
| Want richer summaries on Elsevier papers | After `/daily`, run `/elsevier-catchup` (interactive, opens visible Chrome) |
| Filter feels too lenient / strict | Try a different model for `paper-filterer` (`sonnet` for more nuance, default `haiku` for speed) |
| Digest reads too dry / too verbose | Tune `digest-writer.md` prompt, or bump its model to `opus` for a richer voice |
| `papers/raw/` is bloating | Default 60-day retention runs at end of `/monthly`; force-run with `python scripts/cleanup_raw.py --keep-days 30` |
| Want to keep raw history longer | Edit `--keep-days` in `.claude/commands/monthly.md` step 5, or pass a different value when running manually |

## File layout

```
config.yaml                  # journals, keywords, thresholds, email, arxiv, python_path

papers/
  state.json                 # cursors + dedup sets (seen_ids, seen_dois)
  runs.jsonl                 # one JSON line per /daily, /weekly, /monthly run
  raw/<date>.json            # fetched paper lists (gitignored)
  raw/<date>.filtered.json   # filterer output (gitignored)
  raw/<date>.arxiv.json      # arXiv-only fetch output (gitignored)
  raw/rescore_input.json     # produced by scripts/rescore.py (gitignored)
  notes/<id>.md              # per-paper summaries (gitignored)
  fulltext/<id>.pdf          # cached open-access / authorized PDFs (gitignored)
  daily/<date>.md
  weekly/<YYYY-Www>.md
  monthly/<YYYY-MM>.md

scripts/
  fetch.py                   # OpenAlex fetcher (29 journals)
  fetch_arxiv.py             # arXiv preprint fetcher (6 categories)
  download_fulltext.py       # OA PDF downloader (Copernicus, Wiley, AAAS, Nature, Elsevier API)
  download_fulltext_browser.py  # Interactive Selenium fallback for Elsevier / ACS
  send_email.py              # Gmail SMTP sender
  rescore.py                 # Re-filter all stored raw JSONs after a config change
  log_run.py                 # Append a structured entry to papers/runs.jsonl
  cleanup_raw.py             # Delete raw JSONs older than --keep-days (default 60)
  chunk_papers.py            # split / merge / clean for parallel filter subagents (max 50/chunk)

.claude/
  agents/
    paper-filterer.md        # model: haiku
    paper-summarizer.md      # model: sonnet
    digest-writer.md         # model: sonnet
  commands/
    daily.md                 # /daily — fetch → filter → fulltext → summarize → digest → email → log
    weekly.md                # /weekly — aggregate 7 daily digests
    monthly.md               # /monthly — aggregate 4 weekly digests
    elsevier-catchup.md      # /elsevier-catchup — interactive Elsevier full-text run
    status.md                # /status — one-screen health check (state, cache, env, scheduled tasks)

.browser-downloads/           # Chrome staging folder for the interactive downloader (gitignored)
.env                         # SMTP_PASSWORD, ELSEVIER_API_KEY, ELSEVIER_INSTTOKEN (gitignored)
CHANGELOG.md                 # Per-round changes (R0 through R6)
README.md                    # This file
```

## What runs where

| Step | Where | Model | Why |
|---|---|---|---|
| Fetch from OpenAlex (29 journals) | `scripts/fetch.py` | n/a | Pure I/O, no reasoning |
| Fetch from arXiv (6 categories) | `scripts/fetch_arxiv.py` | n/a | Pure I/O, polite rate limits |
| Download OA PDFs | `scripts/download_fulltext.py` | n/a | Strategy ladder over publisher APIs / cookie sessions |
| Score 0–10 relevance | Subagent (filterer) | Haiku 4.5 | Pattern matching against a fixed rubric |
| Per-paper summary | Subagent ×N parallel (summarizer) | Sonnet 4.6 | Structured extraction from PDFs / abstracts |
| Compose digest | Subagent (digest-writer) | Sonnet 4.6 | Theming + composition over notes + abstracts |
| Send email | `scripts/send_email.py` | n/a | Pure SMTP |
| Log run metrics | `scripts/log_run.py` | n/a | One JSON line to `papers/runs.jsonl` |
| Schedule | Windows Task Scheduler | n/a | Local, no remote infra |
| Manual Elsevier catch-up | `scripts/download_fulltext_browser.py` | n/a | Selenium + undetected-chromedriver, real Chrome, interactive |
