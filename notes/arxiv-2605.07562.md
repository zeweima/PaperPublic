# [Beyond GSD-as-Token: Continuous Scale Conditioning for Remote Sensing VLMs](https://arxiv.org/abs/2605.07562)

**Authors:** Song Zhang, Yanlong Chen, Yilin Li et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-05-08 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** abstract

## TL;DR

Treating ground sampling distance as a continuous conditioning variable rather than a discrete token yields state-of-the-art remote sensing VLM performance across diverse Earth-system benchmarks.

## Summary

- **Problem:** Remote sensing vision-language models (RS-VLMs) handle imagery spanning orders-of-magnitude variation in ground sampling distance (GSD) with a single static parameter set, discarding or discretizing scale information and degrading scale-sensitive interpretation.
- **Method:** ScaleEarth, a QLoRA-finetuned 8B Qwen3-VL backbone, adds CS-HLoRA (Continuous Scale-Conditioned Hyper-LoRA) which modulates LoRA low-rank subspaces via a GSD-driven gate for dynamic scale routing; SSE-U predicts GSD and uncertainty from visual features alone (no sensor metadata required at inference); supervised on GeoScale-VQA, a 1.5M-sample scale-layered RS-VQA corpus whose QA generation is conditioned on the same physical GSD scalar.
- **Key result:** State-of-the-art on XLRS-Bench and OmniEarth-Bench covering diverse Earth-system tasks; specific numeric margins not reported in abstract.
- **Why it matters:** Continuous scale conditioning closes the mismatch between multi-resolution RS imagery and fixed-scale VLMs, enabling more reliable automated interpretation for land cover, change detection, and related Earth-observation workflows without requiring sensor metadata at deployment.
- **Caveats:** Benchmark gains not quantified in abstract; evaluation limited to two RS-VQA benchmarks; generalization to sensor types or spectral ranges beyond what's in GeoScale-VQA is unverified.

## Tags
remote-sensing ML
