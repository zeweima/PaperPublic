This is a agent system that used to provide paper summarize and update at daily weekly, and monthly step. Help to check the whole project.

However, I found there are lots of redundance. For instance, user should provide the meta infor for extraction in `config.yaml`. However, corresponding items frequently appears in other places like:
- In `digest-writer-daily` agent file : "*Without note** (score 6–7, plus excess"

Besides, I am not sure some explanation words in `commands/` is helpful or waste of resources, like:
- In `digest-writer`:
"Before summarizing, run:

```
<python_path> scripts/download_fulltext.py papers/raw/<today>.filtered.json
```

This iterates over the top picks, tries the OpenAlex `open_access.oa_url` first, falls back to Unpaywall by DOI, and saves verified PDFs to `papers/fulltext/<id>.pdf` (skipping cached ones, discarding non-PDF responses). Capture the success count from the last line of output for the run log.

Best-effort — some publishers (Wiley AGU, Elsevier, ACS) routinely return 0 OA hits and that's expected. The summarizer falls back to the abstract when no PDF is available."

Help to revise and comment first.

NOTE: Skip 'papers/' as its the output.