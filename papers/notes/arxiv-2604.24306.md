# SolarTformer: A Transformer Based Deep Learning Approach for Short Term Solar Power Forecasting

**Authors:** Ankan Basu, Jyotiraditya Roy, Aditya Datta et al.
**Venue:** arXiv (cs.LG) · **Date:** 2026-04-27 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR
A causal transformer with cyclic time encoding and station metadata achieves 1.73% percentage error on 15-min PV power forecasting, beating all prior benchmarks on the same dataset.

## Summary
- **Problem:** Short-term PV power forecasting is unreliable across diverse weather conditions and station configurations; most prior models train separate models for sunny vs. cloudy days and do not generalize across stations.
- **Method:** SolarTformer ingests 15-min meteorological time series (NWP + local measurements, 96 steps/day) from 10 PV stations in Hubei Province, China (2018–2019, 2515 records). Cyclic sin/cos encoding of time-of-day and day-of-year prevents discontinuities at midnight/year-end. Station-specific metadata (panel size, angle, capacity, location) is projected into the same 64-d embedding space and concatenated with weather embeddings. A causal multi-head self-attention transformer encoder (4 heads, 16-d subspaces, N=2 blocks) with skip connections and elastic-net regularization (L1+L2 = 1e-4) forecasts power output at t+15 min. Training used AdamW (lr=0.01), MSE loss, 5-fold stratified cross-validation, 300 epochs.
- **Key result:** Test-set PE = 1.73%, MSE = 1.6438, CCC = 0.9764, KL divergence = 0.0232. Mean PE is ~29% lower than the next-best published model (GRU+MFA at 2.41%) on the same dataset; the abstract claims ~60% reduction in mean percentage error vs. prior literature overall. A single unified model covers all seasons and weather conditions.
- **Why it matters:** A single generalizable model that handles both clear and overcast days without retraining per season/station would simplify operational solar grid management. The metadata-embedding approach is transferable to new stations without full retraining.
- **Caveats:** Dataset is one region (Hubei, China, 2018–2019), two years only; no leap years. Hyperparameters (attention heads, embedding dimensions) were not exhaustively searched. Model is computationally heavy for edge/embedded deployment. Only 15-min ahead horizon tested; no multi-horizon (hourly, daily) evaluation. Interpretability of attention weights unexplored.

## Tags
ML remote-sensing climate water-resources
