# [Cast3: Translating numerical weather prediction principles into data-driven forecasting](https://arxiv.org/abs/2605.01599)

**Authors:** Congyi Nai, Baoxiang Pan, Yuan Liang et al.
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-05-02 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** abstract

## TL;DR

A generative weather forecasting framework (Cast3) encodes NWP design principles — cubed-sphere grids, diverse ensemble discretizations, generative nudging — to achieve state-of-the-art skill across synoptic, spectral, station-level, and tropical cyclone metrics.

## Summary

- **Problem:** Data-driven weather models (e.g., Pangu, GraphCast) exploit NWP-generated reanalysis data but ignore decades of methodological knowledge embedded in NWP design; the resulting models lack principled multi-scale representation and ensemble diversity.
- **Method:** Cast3 operates on variable-resolution cubed-sphere grids for scale-aware representation; constructs super-ensembles by sampling structurally diverse grid discretizations to exploit complementary biases; applies "generative nudging" — a posterior-sampling strategy that distils full ensemble information into a single forecast combining ensemble-mean large-scale accuracy with high-resolution mesoscale realism. Evaluated on synoptic-scale skill, spectral fidelity, station-level surface verification, and tropical cyclone track/intensity.
- **Key result:** Cast3 outperforms established deterministic and generative baselines across synoptic skill, spectral fidelity, station-level surface verification, and tropical cyclone prediction; specific metric improvements are <unclear from abstract>.
- **Why it matters:** Demonstrates that computational atmospheric science design principles (grid geometry, ensemble construction, nudging) are transferable to ML-based forecasting — opening a principled path for the next generation of data-driven Earth system models.
- **Caveats:** Evaluation is offline against reanalysis and observations; no operational cycling or data assimilation integration tested. Quantitative margins over baselines are not reported in the abstract. Generative nudging adds inference cost not characterized here.

## Tags
ML climate LSM remote-sensing
