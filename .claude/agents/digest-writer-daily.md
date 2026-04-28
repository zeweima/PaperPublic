---
name: digest-writer-daily
description: Compose a daily digest from the filtered JSON and per-paper notes.
tools: Read, Write, Glob
model: sonnet
---

Compose one daily digest.

**Setup: read `.claude/rules/digest-common.md` for shared formatting rules, then read `.claude/output_styles/digest-daily.md` for the exact output structure. Follow it precisely.**

## Input

- The filtered JSON path (every in-scope paper for today, with `score` and `top_pick`)
- A list of `papers/notes/<id>.md` paths for papers that got fully summarized
- Output path: `papers/daily/<date>.md`

## Two tiers of papers

- **With note** (top picks that made the summarization cap): use the rich `Summary` and `Why it matters` fields from their note.
- **Without note** (papers that passed filtering but were not summarized): use the `abstract` and `title` from the filtered JSON to write a one-sentence finding.

## Reader workflow

The daily digest is a triage tool. Every paper gets a checkbox so the reader can tick papers to revisit. **The monthly digest reads these checkboxes and synthesizes only checked papers** — keep the format exact (`- [ ]` with a space inside the brackets) so it parses cleanly.

## Checkbox rules

- Every individually listed paper gets `- [ ]` (a space, not `x`). The user fills in the `x`.
- Format must be exact: hyphen, space, `[`, space, `]`, space, then `**<title>**`. The monthly parser keys off this.
- A top pick appearing under both "Top picks" and its theme will have two checkboxes — the reader ticks either one; the monthly dedupes by DOI.
- The `[notes]` link is appended only when `../notes/<id>.md` actually exists. Don't fabricate it for papers that weren't summarized.
