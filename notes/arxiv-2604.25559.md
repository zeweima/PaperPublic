# Representing the Surface Ocean in ECMWF's data-driven forecasting system AIFS

**Authors:** Sara Hahner, Lorenzo Zampieri, Jean-Raymond Bidlot et al.
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-28 · **DOI:** n/a
**Score:** 8/10 <sup>top pick</sup>
**Source:** full text

## TL;DR

A single joint ML model (AIFS Marine) simultaneously forecasts atmosphere, surface ocean, ocean waves, and sea ice, gaining ~1 day of lead-time skill over physics-based baselines across nearly all marine variables.

## Summary

- **Problem:** ML weather models (e.g., ECMWF AIFS) treat the atmosphere in isolation; no data-driven system jointly predicts coupled atmosphere–surface ocean–sea ice–wave fields without separate component models.
- **Method:** Encoder–processor–decoder graph neural network / transformer architecture (Anemoi framework) extended with marine variables from ERA5, ORAS6 ocean reanalysis (1993–2023, ~25 km), and an ecWAM wave hindcast (1979–2025, ~9 km). Four model variants tested: AIFS Atmosphere (253 M params), AIFS Waves (253 M), AIFS Ocean (539 M), AIFS Marine (539 M — all components). Training uses two-stage pre-training + rollout fine-tuning; technical solutions include leaky bounding functions for sea-ice variables, directional remapping of wave direction to sin/cos, and per-variable loss scaling to prevent marine components from degrading atmospheric skill.
- **Key result:** AIFS Waves reduces significant wave height (SWH) RMSE by ~10% vs. ecWAM at medium range, equivalent to ~1 day lead-time gain. AIFS Ocean/Marine substantially reduce sea-ice Integrated Ice Edge Error (IIEE) vs. IFS in both hemispheres, with especially large improvements in the Southern Ocean. SST RMSE and bias both improve over IFS; sea surface height (SSH) RMSE is comparable but carries a growing negative bias (attributed to climate-trend drift during training). Adding waves to AIFS has neutral impact on atmospheric scores; adding the full ocean/sea-ice component causes slight degradation in some atmospheric variables, mitigated by halving marine loss weights.
- **Why it matters:** Demonstrates that a single component-agnostic ML architecture can learn physically consistent atmosphere–ocean coupling directly from reanalysis data, without prescribed coupling assumptions—a foundation for fully data-driven Earth system models. Model also correctly simulates tropical-cyclone cold wakes and wave-shadow effects behind islands not resolved at the grid scale.
- **Caveats:** SSH negative bias grows with lead time (global mean sea-level rise in training data not detrended); sea-ice representation is purely surface (no 3-D T/S structure); ORAS6 only from 1993, constraining training window; wave direction underestimation of extreme winds inherited from MSE training; not yet probabilistic.

## Tags
ML remote-sensing climate LSM
