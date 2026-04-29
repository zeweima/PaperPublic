# Observation-Guided Neural Surrogate Learning for Scientific Simulation Emulation: A Single-Gauge Flood-Inundation Proof of Concept

**Authors:** Marzieh Alireza Mirhoseini
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-28 · **DOI:** n/a
**Score:** 9/10 <sup>top pick</sup>
**Source:** full text

## TL;DR

A two-stage EnsCGP + U-Net-ASPP surrogate emulates LISFLOOD-FP urban flood maps with R² ≈ 0.99, MAE < 0.01 m, anchored by a single gauge observation as a pointwise training target.

## Summary

- **Problem:** High-fidelity hydrodynamic simulators (e.g., LISFLOOD-FP) are too slow for real-time ensemble flood forecasting; purely data-driven surrogates lack gauge-consistent local accuracy and poorly constrain worst-case spatial errors.
- **Method:** Two-stage hybrid over a 256 × 256 grid centered on Gauge L, Chicago metro area. Stage 1: ensemble-approximated Gaussian-process / local-analogue surrogate (EnsCGP) uses up to K = 100 analogue historical events (SVD-reduced) to produce a coarse flood-depth map plus uncertainty proxy. Stage 2: U-Net with Atrous Spatial Pyramid Pooling (ASPP) takes EnsCGP depth, uncertainty, gridded rainfall, and spatial coordinates as five-channel input and applies a gated delta-correction to refine the map. A single USGS stage record (Gauge L) is converted to datum-consistent local water depth and used only as a pointwise training loss at the gauge pixel; all other pixels are supervised against LISFLOOD-FP simulation targets. Rolling-year protocol: trained on events prior to each held-out year, tested on ~32–42 events per year, 2013–2019.
- **Key result:** Outside the gauge-constrained pixel, R² ≈ 0.99, overall MAE ≈ 0.005 m; worst-case per-event pixel error never exceeds ~0.4 m across seven held-out years. At the gauge pixel, R² = 1.00 (rounded), MAE ≈ 0.01 m against the converted gauge-depth target, vs. LISFLOOD-FP simulation errors at the same pixel often reaching ~0.2–0.4 m. U-Net refinement consistently reduces EnsCGP worst-case errors across all 2015 and 2017 test events.
- **Why it matters:** Demonstrates that a single stream gauge can anchor a neural flood emulator to reduce local simulator bias without passing the gauge value as an inference-time input — relevant for operational settings where gauges exist but real-time observations cannot be directly fed to the model. Offers a practical pathway to fast, observation-corrected inundation maps for urban basins.
- **Caveats:** Proof of concept limited to one gauge and one 256 × 256 spatial crop in Chicago; coordinate channels specialize the emulator to a fixed domain (no transfer without retraining). No independent satellite or field-observed inundation validation; ablation suite (no-gauge-loss, shuffled targets, EnsCGP-only baselines), storm-grouped temporal splits, wet-area/extent metrics, and runtime benchmarks are all absent and required before operational claims. High gauge-pixel R² should be interpreted as training-objective enforcement, not independent observational skill.

## Tags
hydrology ML water-resources remote-sensing
