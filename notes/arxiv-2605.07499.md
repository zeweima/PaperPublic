# [Cloud-top infrared observations reveal the four-dimensional precipitation structure](https://arxiv.org/abs/2605.07499)

**Authors:** Tianchi Xu, Ziqiang Ma, Andrea Marinoni et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-05-08 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** abstract

## TL;DR

Geostationary infrared cloud-top radiances encode sub-cloud precipitation structure; a physics-constrained deep learning model (4DPrecipNet) reconstructs full 4D precipitation fields from them.

## Summary

- **Problem:** Global-scale, continuous 4D precipitation profiling is unresolved — radar provides vertical structure only regionally and intermittently, while geostationary IR was thought limited to cloud-top properties with no sensitivity below cloud base.
- **Method:** 4DPrecipNet — a deep learning framework trained on multi-channel geostationary IR radiances paired with radar-derived precipitation profiles. A "moisture-first" constraint forces the latent space to reproduce precipitable water vapor, anchoring the model to thermodynamic consistency rather than pure pattern matching.
- **Key result:** Framework reconstructs vertical and temporal evolution of precipitation systems including deep convective structures; robust performance demonstrated across large independent radar comparison samples (specific skill metrics not provided in abstract).
- **Why it matters:** Establishes that sub-cloud precipitation is physically encoded in cloud-top IR, opening a path to continuous global 4D precipitation monitoring from existing geostationary satellites — no additional hardware required.
- **Caveats:** Validation is radar-relative (not independent ground truth); performance for shallow/stratiform precipitation and high-latitude or data-sparse regions is unclear; generalizability beyond training domain not yet demonstrated.

## Tags
remote-sensing hydrology ML climate
