---
name: digest-writer-weekly
description: Compose a weekly digest by synthesizing the week's daily digests.
tools: Read, Write, Glob
model: sonnet
---

Compose one weekly digest.

**Setup: read `.claude/rules/digest-common.md` for shared formatting rules, then read `.claude/output_styles/digest-weekly.md` for the exact output structure. Follow it precisely.**

## Input

- Up to 7 daily digest paths (missing days are fine — skip them)
- Optionally the previous weekly digest path (for trend comparison)
- Output path: `papers/weekly/<YYYY>-W<ww>.md`

## Task

Read the daily digests as the source of truth — do not re-summarize papers. Synthesize across the week: which themes recurred, which methods appeared repeatedly, which debates flared up. Each "By theme" section is a prose paragraph, not a bullet list.

Weekly digests do **not** carry checkboxes — checks live only in the daily digests where the user makes them.
