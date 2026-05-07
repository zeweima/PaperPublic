# [Interpretable Neural Networks to Predict Momentum Fluxes of Orographic Gravity Waves](https://arxiv.org/abs/2605.05052)

**Authors:** Elias Haslauer, Mierk Schwabe, Andreas Dörnbrack et al.
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-05-06 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** abstract

## TL;DR

Neural networks trained on ERA5 achieve R² 0.56–0.72 for orographic gravity wave momentum fluxes at coarse ESM resolution, with SHAP analysis confirming physically meaningful learned relationships.

## Summary

- **Problem:** Orographic gravity waves are subgrid in current Earth system models (ESMs); existing physics-based parameterisations (e.g., Lott & Miller) are approximate, and ML-based replacements have lacked interpretability.
- **Method:** NNs trained on one full year of ERA5 reanalysis; inertia-gravity waves extracted via the MODES software (linear-theory wave filtering); input features coarse-grained to target ESM resolution. Four cases tested: full vs. subgrid-scale spectrum × all land vs. mountainous terrain only. Offline evaluation on a held-out year; SHAP values used for explainability.
- **Key result:** Global R² ranges from 0.72 (full spectrum, all land) to 0.56 (subgrid-scale, mountainous terrain) in offline evaluation; SHAP analysis indicates networks recovered physically meaningful predictors.
- **Why it matters:** Provides a proof-of-concept ML parameterisation pathway for gravity waves in climate models; interpretability via SHAP helps build trust and diagnose learned physics before online deployment.
- **Caveats:** Offline evaluation only — no online coupling to an ESM demonstrated; performance on the most policy-relevant subgrid-scale mountainous case (R² = 0.56) is notably lower; single reanalysis product (ERA5) limits training diversity; generalisation to other ESM resolutions untested.

## Tags
ML LSM climate
