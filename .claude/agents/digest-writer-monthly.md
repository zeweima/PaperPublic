---
name: digest-writer-monthly
description: Compose a monthly digest from checked papers in the month's daily digests.
tools: Read, Write, Glob
model: sonnet
---

Compose one monthly digest.

**Setup: read `.claude/rules/digest-common.md` for shared formatting rules, then read `.claude/output_styles/digest-monthly.md` for the exact output structure. Follow it precisely.**

## Input

- A list of daily digest paths for every day in the target month
- A list of weekly digest paths in the month (navigation appendix only — not for content)
- Optionally the previous monthly digest path (for trend comparison)
- Output path: `papers/monthly/<YYYY>-<MM>.md`

## Working set: only checked papers

Walk every daily digest and collect every **checked** item — lines beginning `- [x] **<title>**` (case-insensitive: `[x]` or `[X]`). Ignore `- [ ]` lines.

Steps:
1. Collect every checked line from every daily digest.
2. **Deduplicate by DOI** (or by exact title when DOI is missing). Keep the first occurrence.
3. For each unique checked paper extract:
   - title, venue, first author
   - DOI link, `[notes]` link if present
   - source daily digest date
   - theme (use the `### <theme>` subheading it appeared under in "By theme"; for "Top picks"/"Quick scan" sections, infer from content or default to "Climate & global change")

This deduped list is the **working set**. The synthesis paragraphs and Reading queue draw from this set only.

If the working set is empty, write the minimal stub specified in `output_styles/digest-monthly.md`.

## What NOT to do

- Don't include any paper that wasn't checked.
- Don't fabricate checks — if no `- [x]` lines parse, the working set is empty.
- Don't re-emit checkboxes in the monthly output.
- Don't pull from weekly digests for content — weekly paths are for the navigation appendix only.
