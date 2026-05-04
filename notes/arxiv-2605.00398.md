# [M-CaStLe: Uncovering Local Causal Structures in Multivariate Space-Time Gridded Data](https://arxiv.org/abs/2605.00398)

**Authors:** J. Jake Nichol, Michael Weylandt, G. Matthew Fricke et al.
**Venue:** arXiv preprint · **Date:** 2026-05-01 · **DOI:** n/a
**Score:** <unclear from abstract>/10
**Source:** full text

## TL;DR

Multivariate CaStLe jointly discovers within- and cross-variable causal structure in high-dimensional gridded space-time data by pooling spatial replicates, reducing search complexity from O(2^{N²V}) to O(2^{9V}).

## Summary

- **Problem:** Causal discovery in multivariate gridded Earth system data is intractable when grid cells vastly outnumber time steps per cell; applying univariate methods variable-by-variable misses cross-variable confounding and spatial coupling.
- **Method:** M-CaStLe extends the CaStLe meta-algorithm to V variables per grid cell. Phase 1 (LENS) pools all V time series from every 3×3 Moore neighborhood into a shared tensor (R^{3×3×V×L}), yielding effective sample size L = T(N−2)². Phase 2 (PIP) jointly identifies parents of all V center variables from the 9V lag-1 candidates using any time-series causal discovery algorithm (PC, PCMCI, or DYNOTEARS). The resulting multivariate stencil graph decomposes into a spatial graph and a reaction graph for interpretability. Evaluated on: multivariate VAR benchmarks (V=1–6, 4×4 grids, 31,140 simulations), advection-diffusion-reaction (ADR) PDEs (two chemical species), Mt. Pinatubo E3SMv2-SPA output (T=7, N=30, four aerosol/radiative variables), and ERA5 ENSO reanalysis (SST + OLR).
- **Key result:** VAR benchmarks — M-CaStLe F1 ≈ 0.96 at V=1, degrades moderately to V=6 (still exceeds Cartesian-CaStLe and non-spatial baselines which remain near chance); precision >0.9 across all V. ADR PDE — median advection-angle error 4.76°; reaction-graph F1 median 1.0 (mean 0.912, n=672). Mt. Pinatubo — F1=0.95 with FSDS link assumption vs. F1=0.00 for PCMCI on spatially aggregated data. ENSO — recovers phase-dependent SST→OLR coupling consistent with known El Niño vs. La Niña asymmetry. Spatial pooling in the Pinatubo case converts T=7 samples per location into L_eff ≈ 5,384 effective samples (≈769×), reducing per-edge error ≈27.7×.
- **Why it matters:** Enables joint causal discovery over multiple co-located variables (e.g., temperature + soil moisture, aerosol species) in high-dimensional gridded systems where PCMCI and other standard methods fail outright; directly applicable to Earth system model output and reanalysis with coarse temporal sampling. Stencil decomposition preserves grid-level interpretability.
- **Caveats:** Assumes spatial and temporal stationarity within the analysis window — inapplicable to teleconnections or regime-change boundaries. Only lag-1 parents considered. Recall degrades in dense, high-V stable systems because stability constraints force coefficients toward zero (piranha constraint). Highly correlated spatial replicates reduce effective sample size below the Θ(N²) ideal. Current implementation restricted to rectangular grids.

## Tags
ML remote-sensing climate biogeochem
