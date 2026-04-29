# Agentic AI for Remote Sensing: Technical Challenges and Research Directions

**Authors:** Muhammad Akhtar Munir, Muhammad Umer Sheikh, Akashah Shabbir et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-27 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Generic agentic AI frameworks fail structurally in Earth observation workflows because geospatial tools are stateful and order-dependent, requiring EO-native agent design.

## Summary

- **Problem:** Agentic AI (tool-using LLMs/VLMs) is increasingly applied to EO, but generic frameworks assume tools are independent, actions are reversible, and errors are locally detectable — assumptions that break in geospatial pipelines where reprojection, resampling, and spatial aggregation irreversibly transform state and silently propagate errors.
- **Method:** Position paper; identifies five implicit assumptions in generic agentic models (tools behave independently, actions are reversible, environment exposes correctness, errors are locally detectable, internal evaluation is sufficient), then characterizes how each fails in EO workflows with concrete failure-mode taxonomy across data selection → preprocessing → reproject/resample → temporal aggregate → model inference → decision steps.
- **Key result:** Demonstrates via worked example (flood-area estimation from pre/post imagery) that a generic agent produces a plausible but geospatially invalid answer (wrong CRS, temporal leakage, unit conversion error) while an EO-native agent enforces geo-valid intermediate state transitions and yields a traceable result; proposes five design principles: structured geospatial state, tool-aware reasoning, verifier-guided execution, validity-aligned learning objectives, and trajectory-level evaluation.
- **Why it matters:** Frames EO as a distinct agentic domain requiring purpose-built benchmarks, hybrid supervised + RL training with externally grounded reward signals, and constrained self-improvement; directly challenges the assumption that attaching geospatial tools to a generic agent is sufficient for scientific correctness.
- **Caveats:** Position/perspective paper — no empirical benchmark results; proposed design principles are not yet implemented or validated; argument relies on illustrative examples rather than systematic empirical failure-mode counts.

## Tags
remote-sensing ML
