# [Foundation AI Models for Aerosol Optical Depth Estimation from PACE Satellite Data](https://arxiv.org/abs/2605.00678)

**Authors:** Zahid Hassan Tushar, Sanjay Purushotham
**Venue:** IGARSS 2026 · **Date:** 2026-05-01 · **DOI:** n/a
**Score:** 6/10
**Source:** full text

## TL;DR

ViTCG, a compact Vision Transformer with channel-wise spectral grouping, retrieves AOD from PACE hyperspectral data with 62% lower MSE than the best foundation model baseline.

## Summary

- **Problem:** Conventional AOD retrieval from satellite data is pixel-wise, ignoring spatial coherence; existing deep-learning and foundation-model approaches either discard long-range spatial context or handle hyperspectral redundancy poorly, yielding noisy, spatially inconsistent fields.
- **Method:** ViTCG reframes AOD estimation as a spatial regression over 96×96-pixel patches of PACE OCI L1B radiance (291 spectral bands). Channel-wise grouping compresses spectral redundancy before patch embedding; a 4-block transformer encoder captures spatial dependencies; a lightweight MLP + upsample decoder recovers full-resolution AOD at 550 nm. Trained on 1,800 patches (2024–2025 global granules), tested on 2,000 held-out patches; validated against 125 collocated AERONET Level-2 sites.
- **Key result:** MSE 0.0141, RMSE 0.1186, MBE 0.0008, IOA 0.8552 — vs. next-best PrithviEO1 (MSE 0.0370, IOA 0.3721). Removing channel-wise grouping raises MSE to 0.0227. Model has 8.82 M parameters (~10× fewer than baselines at 87–102 M); inference 0.0069 s per 96×96 patch vs. 0.0076–0.0309 s for foundation model baselines; pixel-wise DNN is 668× slower at patch scale.
- **Why it matters:** Demonstrates that a purpose-built compact transformer outperforms large geospatial foundation models for atmospheric retrieval from a new hyperspectral sensor (PACE OCI), and does so with substantially lower compute — relevant for operational air-quality and climate-forcing workflows.
- **Caveats:** Training dataset is small (1,800 patches); L2 AOD reference itself carries retrieval uncertainty and was resampled from 8.4 km to 1.2 km. AERONET validation covers only two days (20 Feb and 20 Mar 2025) and shows larger errors over South America and the Indian subcontinent due to spatial representativeness mismatch. No physical constraints embedded; generalization across aerosol regimes and seasons is untested.

## Tags
remote-sensing ML climate
