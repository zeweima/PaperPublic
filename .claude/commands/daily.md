---
description: Fetch new papers, filter, summarize, build daily digest, email it.
---

Run the daily paper-tracking pipeline. Today's date in UTC is the run date.

## Python interpreter

Read `python_path` from `config.yaml` and use it for every Python invocation below.

## Pipeline

### 1. Fetch
Run `<python_path> scripts/fetch.py` from the project root with env `PYTHONIOENCODING=utf-8`. The script reads `papers/state.json` for `last_daily` and uses `lookback_days` from `config.yaml` on OpenAlex `publication_date`; dedup via `seen_ids` + `seen_dois` prevents repeats. Capture the **relative path** it prints on the last line — that is the raw JSON (typically `papers/raw/<date>.json`). Note today's date for use later.

### 1b. Fetch arXiv preprints (append into the same raw JSON)
If `arxiv.enabled` is true in config, run:

```
<python_path> scripts/fetch_arxiv.py --merge papers/raw/<today>.json
```

This pulls preprints in the configured arXiv categories and appends them into today's raw JSON (deduped by id). arXiv papers carry `is_oa: true` and an `oa_url`, so the downloader will fetch their PDFs for free.

Skip silently if arxiv is disabled.

### 2. Filter

**HARD RULE — relevance scoring MUST be done by the `paper-filterer` subagent.** Do **not**, under any circumstance:
- write a local `filter_*.py` / `score_*.py` / `do_filter.*` script at the project root (or anywhere) that re-implements the scoring rubric in Python keyword lists,
- shell out to a one-off Python `-c "..."` that scores papers,
- bypass the subagent because the input "feels too big" — use the chunking recipe below instead,
- generate any other ad-hoc helper script. The only legitimate Python scripts in this pipeline are the ones already in `scripts/` (`fetch.py`, `fetch_arxiv.py`, `download_fulltext.py`, `send_email.py`, `log_run.py`, `cleanup_raw.py`, `rescore.py`). Do not add new ones from inside `/daily`.

If you find yourself reaching for `Write` to create a `.py` file during this step, STOP — that is the failure mode this rule exists to prevent. Spawn the subagent instead.

#### 2a. Always chunk the raw JSON
Run:

```
<python_path> scripts/chunk_papers.py split papers/raw/<today>.json --max 30
```

The script writes `papers/raw/<today>.chunk.000.json`, `<today>.chunk.001.json`, … (max 30 papers each) and prints one chunk path per line on stdout. Capture them.

If stdout is empty (raw file had `[]`), skip filtering. Write a minimal "no new papers" digest to `papers/daily/<today>.md`, update state, still proceed to email so the user knows the system ran. Jump to step 5.

#### 2b. Filter each chunk (parallel subagents)
Spawn **one `paper-filterer` subagent per chunk, all in parallel** — issue all the Agent tool calls in a single message. Each subagent:
- receives the path to its chunk
- applies the rubric in `.claude/agents/paper-filterer.md`
- writes its filtered output to `<chunk-path>.filtered.json` (e.g. `papers/raw/<today>.chunk.000.filtered.json`)
- prints that path on its last line

The 30-paper cap means even Haiku has plenty of context headroom, and parallel filtering keeps wall-clock time roughly equal to one chunk's runtime.

#### 2c. Merge and clean
Combine the per-chunk filterer outputs into one filtered JSON:

```
<python_path> scripts/chunk_papers.py merge papers/raw/<today>.filtered.json "papers/raw/<today>.chunk.*.filtered.json"
```

`merge` dedupes by `id` (defensive — chunks shouldn't overlap, but if a paper somehow appears twice we keep one copy).

Delete the per-chunk artifacts so `papers/raw/` stays tidy:

```
<python_path> scripts/chunk_papers.py clean "papers/raw/<today>.chunk.*"
```

The final filtered path used by the rest of the pipeline is always `papers/raw/<today>.filtered.json`.

### 3. Summarize (parallel, capped)
Read `max_summaries_per_run` and `top_picks_threshold` from `config.yaml`.

From the filtered JSON, build a **summarization list**:
- Take all papers with `top_pick: true` (i.e. score >= `top_picks_threshold`).
- Sort by score descending, then by venue prestige (Nature/Science/Sci Adv/PNAS first), then by date desc.
- Trim to the first `max_summaries_per_run` entries.

### 3a. Download full text (best-effort)
Before summarizing, run:

```
<python_path> scripts/download_fulltext.py papers/raw/<today>.filtered.json
```

Capture the success count from the last line of output for the run log. This step is best-effort; when no OA PDF is available, summarization falls back to abstract-only.

### 3b. Summarize
For each paper in the summarization list, spawn a `paper-summarizer` subagent. **Run them in parallel** — issue all the Agent tool calls in a single message. If there are more than 10, run them in batches of 10. Each subagent automatically reads `papers/fulltext/<id>.pdf` if present, otherwise uses the abstract. Each writes to `papers/notes/<id>.md` and prints its path.

Papers that pass the filter but are NOT on the summarization list do **not** get a per-paper note. They appear in the digest from filtered JSON data.

### 4. Compose digest
Spawn one `digest-writer-daily` subagent with:

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

### 7. Log the run
Append a structured entry to `papers/runs.jsonl`:

```
<python_path> scripts/log_run.py --type daily --date <today> \
    --fetched <N> --filtered <M> --top-picks <T> \
    --summarized <S> --fulltext <F> \
    --digest papers/daily/<today>.md \
    --email-status <sent|failed>
```

### 8. Report
Print a tight summary to the user. **Always show file paths as relative to the project root** (e.g. `papers/daily/2026-04-27.md`, never the full Windows absolute path):
- raw fetched / passed filter / top picks / summarized / fulltext-downloaded
- digest path (relative)
- email status (sent / failed)

### 8b. Suggest /elsevier-catchup if useful
After the report, scan the filtered JSON for top picks (`top_pick: true`) whose DOI starts with `10.1016/` and do not yet have a cached PDF at `papers/fulltext/<id>.pdf`. If any exist, print a one-line hint:

```
{N} Elsevier top pick(s) without full text. Run `/elsevier-catchup` (interactive, ~2 min) to upgrade them.
```

Skip the hint when N=0. You can compute this with a small inline counter:

```
<python_path> -c "import json,os,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));pending=[p for p in d if p.get('top_pick') and (p.get('doi') or '').replace('https://doi.org/','').startswith('10.1016/') and not os.path.exists(f'papers/fulltext/{p[\"id\"]}.pdf')];print(len(pending))" papers/raw/<today>.filtered.json
```

## Failure handling
- Per-source fetch failures are logged by the script and the run continues — that's fine.
- If `paper-filterer` returns nothing kept, still write a digest stating "0 in-scope papers from N fetched".
- If a `paper-filterer` subagent fails or times out, **re-spawn the subagent** (possibly on a smaller chunk per the recipe in step 2b). Do NOT replace it with a local Python scoring script — the rubric lives in `.claude/agents/paper-filterer.md` and must be applied by the model, not by hand-coded keyword lists.
- If `paper-summarizer` fails on a particular paper, skip that paper and continue — the digest will fall back to its abstract. Do not write a local summarizer script.
- If email fails (e.g. missing SMTP_PASSWORD), continue and clearly print the error — the markdown digest is still saved on disk.
- The Python path comes from `config.yaml` key `python_path`.

## Responsibility split
- API I/O, file I/O, dedup, SMTP, logging: `scripts/*.py`.
- Relevance scoring: `paper-filterer` subagent.
- Per-paper summarization: `paper-summarizer` subagents.
- Theming + digest composition: `digest-writer-daily` subagent.

Do not add ad-hoc scoring or summarizing scripts to replace subagents.
