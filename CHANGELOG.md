# Changelog

All notable changes to scripts, agents, slash commands, and config schemas. New entries go at the top. Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

The data files (`papers/raw/*.json`, `papers/notes/*.md`, `papers/daily|weekly|monthly/*.md`, `papers/runs.jsonl`) are NOT tracked here — see [`papers/runs.jsonl`](papers/runs.jsonl) for the per-run data log.

---

## 2026-04-27 — R7: raw history retention (60-day cleanup)

### Added
- **`scripts/cleanup_raw.py`** — deletes date-keyed raw fetch JSONs older than `--keep-days` (default 60). Matches `papers/raw/YYYY-MM-DD.json`, `*.filtered.json`, `*.arxiv.json`, etc. Skips non-date-keyed files like `rescore_input.json`. Supports `--dry-run`.
- **`/monthly` step 5: cleanup** — runs `scripts/cleanup_raw.py` at the end of each monthly digest as natural housekeeping.

### Why this design
- Notes (`papers/notes/<id>.md`), full-text PDFs (`papers/fulltext/<id>.pdf`), and digests (`papers/{daily,weekly,monthly}/`) are **kept indefinitely** — they're the persistent value of the system.
- Raw fetch JSONs are intermediate artifacts: they're only re-read by `scripts/rescore.py` if you change `keywords` and want history re-evaluated. After 60 days, that re-evaluation window has limited value (interests don't shift often), so the disk cost outweighs.
- Dedup state (`seen_ids` / `seen_dois` in `state.json`) is unaffected — already-fetched papers stay deduped even after their raw JSON is gone, preventing accidental re-summarization.
- One-time bootstrap raw files (>60 days old at scaffold time) are removed on the first monthly run after deployment.

### Tradeoff
- After cleanup, `scripts/rescore.py` can only re-evaluate the last 60 days of papers. If the user wants longer history (e.g. annual rescore on a pivot to a new research direction), they can bump `--keep-days` in the slash command.

---

## 2026-04-27 — R6: per-agent model selection

### Changed
- **`paper-filterer` → Haiku 4.5** (was Opus 4.7). Bulk classification with a fixed rubric — Haiku is plenty for "is this paper about hydrology / Earth-system science?" Roughly 15× cheaper.
- **`paper-summarizer` → Sonnet 4.6** (was Opus 4.7). Structured extraction from PDFs (pages 1-12) and abstracts. Sonnet is reliable for finding numbers and writing tight bullets; ~5× cheaper.
- **`digest-writer` → Sonnet 4.6** (was Opus 4.7). Composition + theming over a moderate context. Sonnet is fine here. ~5× cheaper.

### Cost model (typical day, 250 fetched / 30 summarized)

| Stage | Before (all Opus) | After (tiered) |
|---|---:|---:|
| Filter | ~$3.75 | ~$0.25 |
| Summarize | ~$13.50 | ~$2.70 |
| Digest-write | ~$0.90 | ~$0.18 |
| **Total** | **~$18 / day** | **~$3 / day** |

~6× reduction in daily run cost (~$1100/yr vs ~$6500/yr if scheduled daily).

### Implementation
One-line addition to each agent's YAML frontmatter (`model: haiku` or `model: sonnet`). Aliases auto-resolve to the latest snapshot of that tier. Override per-call by passing `model:` in the Agent tool call if needed for a specific run.

---

## 2026-04-27 — R5b: interactive browser fallback for Elsevier / ACS

### Added
- **`scripts/download_fulltext_browser.py`** — interactive browser-based fallback for publishers that resist scripted scraping. Uses **undetected-chromedriver** + real Chrome via Selenium. The undetected-chromedriver patches the `navigator.webdriver` flag and other automation signatures that Playwright doesn't, which gets ScienceDirect to render the View PDF anchor in the DOM (Playwright's CDP signature does not).
- **`/elsevier-catchup` slash command** — wraps the browser script, runs after `/daily`. Picks up only top-pick Elsevier (and optionally ACS) papers whose `<id>.pdf` isn't cached yet. Sorts by score, caps at `--max` (default 10).
- **Manual captcha bypass** — when ScienceDirect's "Press & Hold" / Reference-number block appears, the script prompts the user to solve it in the visible Chrome window and press Enter. 5-minute timeout per paper so a forgotten run doesn't hang forever.
- **Download monitoring** — uses Chrome's native PDF download (with `plugins.always_open_pdf_externally: True`) routed to `.browser-downloads/`, then moves the completed `.pdf` (skipping `.crdownload` partials) to `papers/fulltext/<id>.pdf`.
- **`undetected-chromedriver`** dependency (~5 MB pip install; uses the user's existing Chrome installation, no separate Chromium download).

### Why a separate script and not part of `/daily`
Interactive (uses `input()` for captcha bypass), so it can't run from Windows Task Scheduler at midnight. Designed for "5 minutes in the morning while you sip coffee" — Chrome opens, you solve the occasional captcha, the rest is automated. Net effect: top-pick Elsevier coverage jumps from ~0% (abstract-only without Insttoken) to ~80% (full text via real Chrome session).

### Why undetected-chromedriver and not Playwright real-Chrome
Tested both extensively in R5: Playwright with `channel="chrome"` (real Chrome binary) still fails to get ScienceDirect to render View PDF, even with `playwright-stealth`. Selenium-via-undetected-chromedriver passes the same check because (a) ChromeDriver's automation signature differs from Playwright's CDP, (b) undetected-chromedriver actively patches the remaining detection points.

### Limitations
- Requires real Chrome installed (it is, on this machine, at `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`)
- If Chrome auto-updates ahead of undetected-chromedriver's patches, may need to pin `version_main=<your_chrome_major_version>` in `setup_driver()`
- ACS support is opt-in via `--publishers 10.1016 10.1021`; ACS bot detection is similar to Elsevier and the same approach should work, but unverified

---

## 2026-04-27 — R5: Elsevier API integration (with caveats)

### Investigated and rejected
- **Slowing the pipeline down to bypass Elsevier**. Won't work: ScienceDirect's `Radware Bot Manager` is **JS fingerprinting** (canvas, behavior), not rate-limiting. Long inter-request waits don't help — the very first scripted request gets a 403 with a captcha page.
- **Headless Playwright** against ScienceDirect. Installed `playwright-stealth` and tried multiple anti-detection tweaks (`--disable-blink-features=AutomationControlled`, hidden `navigator.webdriver`, real viewport, real UA). Page loads, but ScienceDirect doesn't render the View PDF anchor in the DOM for any non-interactive browser — `pdfft` link count = 0 in headless rendered HTML, vs. visible in a real browser. (Visible-browser Playwright would work but is invasive — would pop a Chrome window every midnight.)
- **playwright-stealth on headless Chromium** — installed and tested; insufficient against ScienceDirect's specific detection.

### Added
- **Elsevier API path** in `scripts/download_fulltext.py` — `elsevier_api_fetch()`. Calls `https://api.elsevier.com/content/article/doi/{doi}` with `X-ELS-APIKey` and (if available) `X-ELS-Insttoken`.
- **Teaser detection** — free-tier keys return a 1-page cover PDF (not the full article). Confirmed empirically: 270 KB, 1 page, no "References" / "Conclusion" / "Acknowledgement" markers. The fetcher now parses `/Count` from the PDF dictionary and rejects `count==1 && no References` as a teaser, so the cache stays clean and the summarizer falls through to abstract.
- **`X-ELS-Insttoken` support** — `ELSEVIER_INSTTOKEN` env var, sent alongside the API key when present. This is the header that unlocks full text via the institution's Elsevier subscription.
- **`load_env_var()` helper** in `download_fulltext.py` — reads from `os.environ` first, then `.env` file. Same pattern as `send_email.py`.
- **`.env.example`** documents both `ELSEVIER_API_KEY` and `ELSEVIER_INSTTOKEN`, with the actual UIUC procurement steps (contact a UIUC science librarian or open an Elsevier API support request asking for institutional association).
- **README "Notes on access"** section — honest explanation of teaser-vs-fulltext distinction and the manual-PDF escape hatch (drop a file at `papers/fulltext/<id>.pdf` and the summarizer picks it up).

### Strategy chain (final)
The downloader now tries strategies in this order, stopping at first success:

1. **Copernicus DOI transform** (`10.5194/`) → direct PDF URL
2. **Nature family direct URL** (`10.1038/`) → `nature.com/articles/<id>.pdf` (works on subscribing IP)
3. **Elsevier API** (`10.1016/`, requires `ELSEVIER_API_KEY` env var) → `api.elsevier.com`
4. **Publisher cookie session** (Wiley `10.1029/`/`10.1111/`/`10.1002/`, AAAS `10.1126/`) → seed cookies via landing page, then `pdfdirect`/`pdf` endpoint
5. **OpenAlex `oa_url`** — direct PDFs for many smaller OA journals
6. **Unpaywall API fallback** — by DOI; tries all `oa_locations` (publisher + repository copies)

### Still hard
- **ACS Publications** (`10.1021/`, ES&T) — same JS bot-detection as Elsevier but no free public API. Stays abstract-only.
- **Some non-OA Springer / IOP** — depends on per-article subscription state. Stays abstract-only when paywalled.

---

## 2026-04-27 — R4: campus IP, arXiv, 3 new journals

### Added
- **Nature direct-URL strategy** in `scripts/download_fulltext.py`. DOIs with prefix `10.1038/` are mapped to `https://www.nature.com/articles/<id>.pdf` and fetched directly. From a subscribing IP (e.g. UIUC campus) this covers Nature, Nature Sustainability, Nature Climate Change, Nature Food, Nature Geoscience, **Nature Water**, and Nature Comms — verified 8/8 on smoke test.
- **Three new journals** added to `papers/config.yaml`:
  - **Nature Water** (ISSN 2731-6084)
  - **Earth's Future** (ISSN 2328-4277, AGU OA)
  - **JGR: Machine Learning and Computation** (ISSN 2993-5210, AGU OA)
- **`scripts/fetch_arxiv.py`** — arXiv preprint fetcher. Queries 6 configurable categories (`physics.ao-ph`, `physics.flu-dyn`, `cs.LG`, `stat.ML`, `eess.IV`, `cs.CV` by default), parses the Atom feed, normalizes to the same JSON schema as OpenAlex output, and appends to today's raw JSON via `--merge`. arXiv papers always carry `is_oa: true` with a working `oa_url`, so the downloader fetches their PDFs in the OpenAlex direct path with no extra logic. Polite-rate (5s between categories) and 429 retry with exponential backoff.
- **`arxiv:` config block** in `papers/config.yaml` — `enabled`, `categories[]`, `per_category_max`. Can be turned off entirely by setting `enabled: false`.

### Changed
- **`.claude/commands/daily.md` step 1b** — runs `scripts/fetch_arxiv.py --merge papers/raw/<today>.json` after the OpenAlex fetch when `arxiv.enabled` is true.
- **`README.md` hit-rate table** — adjusted Nature family from "~25%" to "~95% on campus" (Nature direct URL works from UIUC IP). Added arXiv at 100%. Added new "Sources" section explaining the OpenAlex + arXiv split. Added a "Notes on access" section explaining the campus-IP dependency for Nature family.

### Investigated
- **Elsevier ScienceDirect (10.1016/)** even from UIUC campus IP returns a Radware Bot Manager challenge. Bypassing requires executing JavaScript (headless browser). Out of scope for now — these journals (AgrForMet, FCR, Geoderma, S&TR, Water Research, SBB, One Earth) fall back to abstract-only.
- **ACS (10.1021/)** same story — bot detection independent of IP. Falls back to abstract.
- **EZproxy (UIUC library proxy)** — viable in principle but requires Shibboleth-authenticated session cookies that would need to be extracted from the user's browser manually. Not implemented; can be added as an opt-in later if needed.

### Diagnostic
- Confirmed outward IP from this machine is `128.174.177.204` (`CPSC-P10E53341.ad.uillinois.edu`) — i.e. UIUC campus. Nature/IOP/Wiley benefit; Elsevier/ACS still blocked by behavioral bot detection.

---

## 2026-04-27 — R3: better OA hit-rate + relative paths

### Added
- **Publisher cookie-session fetch** in `scripts/download_fulltext.py`. Wiley AGU (DOI prefix `10.1029/`), Wiley general (`10.1111/`, `10.1002/`), and AAAS (`10.1126/`) reject scripted PDF requests unless a session cookie is present. The downloader now visits the article landing page first to seed cookies, then requests `/doi/pdfdirect/<doi>` (Wiley) or `/doi/pdf/<doi>` (AAAS). Browser-realistic User-Agent and headers (`Accept-Language`, `Sec-Fetch-*`, `Upgrade-Insecure-Requests`).
- **Score-descending sort** inside `download_fulltext.py` so `--limit N` picks the most-relevant N rather than the first N in input order.
- **Generalized `publisher_two_step()`** helper — easy to extend to other publishers if they follow the same cookie-then-PDF pattern.

### Changed
- **All scripts now print relative paths**, not absolute Windows paths, when reporting where files were saved (`scripts/fetch.py`, `scripts/download_fulltext.py`, `scripts/rescore.py`). The orchestrator captures these from the script's stdout and passes them through to the user.
- **Slash commands** (`daily.md`, `weekly.md`, `monthly.md`) explicitly require relative paths when reporting back to the user. Example phrasing: `papers/daily/2026-04-27.md`, never `c:\Users\…\PaperSummarizing\papers\daily\2026-04-27.md`.
- **README.md full-text section** rewritten with: when PDFs are retrieved (top picks only), the strategy ladder (Copernicus → publisher cookie session → OpenAlex → Unpaywall), and a measured hit-rate table per publisher group.

### Fixed
- **Wiley AGU papers (WRR, GRL, GBC, JAMES, JGR-BG) were failing despite being OA.** Root cause: Wiley/Cloudflare returns a `cookieAbsent` redirect to scripted requests. Now handled by the publisher two-step. WRR top picks should download reliably going forward.
- **Sci Advances papers were failing** for the same reason — same fix unlocks them via `science.org`.
- **R2 hit rate on a 30-paper sample**: 2/30 (7%) → **R3: 10/30 (33%)**. Most remaining failures are Elsevier (ScienceDirect) and ACS, which use more aggressive bot detection than cookie-seeding alone can defeat.

---

## 2026-04-27 — R2: full-text + run logging

### Added
- **`scripts/download_fulltext.py`** — downloads open-access PDFs for top-pick papers. Tries OpenAlex `open_access.oa_url` first (already in fetched data), falls back to Unpaywall API by DOI. Verifies `%PDF` magic bytes before saving; rejects paywall HTML stubs. Caches to `papers/fulltext/<id>.pdf`.
- **`scripts/log_run.py`** — appends one JSON line to `papers/runs.jsonl` per run with timestamp, type (daily/weekly/monthly), date, fetched/filtered/top-picks/summarized/fulltext counts, digest path, email status, optional note.
- **`papers/runs.jsonl`** — append-only run log; one JSON object per line. Created lazily on first write.
- **`papers/fulltext/<id>.pdf`** — full-text cache for top picks.

### Changed
- **`scripts/fetch.py`** — fetched papers now include an `open_access` object (`is_oa`, `oa_url`, `oa_status`) so the downloader can hit OpenAlex's known OA URL without an extra API call.
- **`.claude/agents/paper-summarizer.md`** — when summarizing a paper, first checks for `papers/fulltext/<id>.pdf`. If present, reads it via the Read tool with `pages: "1-12"` (concentrates on abstract / intro / methods / key results) for a richer summary than the abstract alone. Falls back silently if the PDF is corrupt or absent. Notes now record `Source: full text | abstract`.
- **`.claude/commands/daily.md`** — added step 3a (download_fulltext after filter, before summarize) and step 7 (log_run after email).
- **`.claude/commands/weekly.md`** and **`monthly.md`** — added log_run step at end.
- **`README.md`** — documented full-text behaviour, OA hit-rate expectations by publisher, and how to inspect `runs.jsonl`.

---

## 2026-04-27 — R1: refinement (cap, dedup, rescore)

### Added
- **`max_summaries_per_run: 30`** in `papers/config.yaml` — bounds daily summarization cost. Only top picks (≥8/10) get full per-paper notes; if more top picks than the cap, take the highest-scoring N. Score 6-7 papers and overflow top picks appear in the digest with abstract-only entries.
- **`seen_dois`** field in `papers/state.json` — second dedup key alongside `seen_ids` to catch the rare case of OpenAlex re-indexing a paper under a new id.
- **`scripts/rescore.py`** — concatenates every `papers/raw/YYYY-MM-DD.json` into `papers/raw/rescore_input.json` so the user can re-run the filterer after changing `keywords` or thresholds in config, without re-fetching from OpenAlex. Supports `--since YYYY-MM-DD` to limit the rescore window.

### Changed
- **`scripts/fetch.py`** — dedup now uses `id` AND `doi` (paper survives only if neither matches state). Refuses to overwrite an existing `papers/raw/<date>.json` unless `--force` is passed (prevents history loss when re-running fetch for the same date).
- **`.claude/commands/daily.md`** — step 3 now reads the cap from config and trims the summarization list before parallel dispatch. Step 5 (state update) appends DOIs as well as ids.
- **`.claude/agents/digest-writer.md`** — explicit two-tier input (papers with notes vs. papers in filtered JSON only). Distinguishes how to render each tier in the digest.

### Fixed
- Fetch overwriting raw file with `[]` on same-date re-runs because dedup made the result empty (destroyed history needed by `rescore.py`).

---

## 2026-04-27 — Initial scaffold

### Added
- **Config-driven journal list** — 26 Earth/environmental journals with ISSNs in `papers/config.yaml` (Nature, Science, Sci Adv, PNAS, Nature Climate/Sustainability/Food/Geoscience, GCB, AgrForMet, FCR, ES&T, Geoderma, One Earth, ERL, GRL, Biogeochemistry, Soil & Tillage, JGR-BG, Soil Biol Biochem, JAMES, WRR, Water Research, HESS, GBC, GMD).
- **`scripts/fetch.py`** — OpenAlex fetcher with ISSN filter, polite pacing, exponential backoff on 429, abstract reconstruction from inverted index. Initially used `from_created_date`; reverted to `from_publication_date` on discovering the former is paid-tier only — see below.
- **`scripts/send_email.py`** — Gmail SMTP delivery with HTML rendering via `markdown` lib; reads `SMTP_PASSWORD` from env or `.env`.
- **`.claude/agents/`** — `paper-filterer`, `paper-summarizer`, `digest-writer` subagents with prompts tailored to Earth/env science context.
- **`.claude/commands/`** — `/daily`, `/weekly`, `/monthly` slash commands orchestrating the pipeline.
- **State management** — `papers/state.json` tracks `last_daily/weekly/monthly` cursors and `seen_ids` for dedup. Lookback default 35 days to catch monthly journals.

### Discovered / decided
- OpenAlex `from_created_date` and `from_updated_date` filters require a paid plan. Reverted to `from_publication_date` and bumped `lookback_days: 10 → 35` to catch AGU/Wiley monthly titles (WRR, GCB, GBC, JAMES, JGR-BG, One Earth) that batch-attribute all papers to issue date (1st of month).
- Subagents in `.claude/agents/` are loaded at session start; they cannot be referenced by custom name within the session that *creates* them. Test harness uses `general-purpose` agents with the same prompt inlined.

### Environment fixes (one-time)
- Repaired miniconda base by copying `libexpat.dll` from `pkgs/libexpat-2.6.3-he0c23c2_0/Library/bin/` to `Library/bin/` (was missing, broke `pip` and `xmlrpc`).
- Installed `pyyaml` (6.0.3) and `markdown` (3.10.2) into miniconda base.
- Added `python_path` to config.yaml pointing at the miniconda Python (bare `python` on PATH is a Microsoft Store stub on this machine).
