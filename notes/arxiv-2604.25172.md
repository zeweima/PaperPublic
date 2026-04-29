# Conditional Flow Matching for Probabilistic Downscaling of Maximum 3-day Snowfall in Alaska

**Authors:** Douglas Brinkerhoff, Elizabeth Fischer
**Venue:** arXiv (cs.LG) · **Date:** 2026-04-28 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Conditional flow matching downscales 64 km climate output to 4 km probabilistic snowfall ensembles 87.8% better spectrally than bicubic lapse-rate correction, in seconds on a laptop.

## Summary

- **Problem:** Orographic precipitation in complex terrain requires km-scale resolution, but dynamical downscaling (WRF) costs months of compute per scenario, blocking large ensembles for uncertainty quantification in climate adaptation.
- **Method:** WxFlow — a 23M-parameter conditional U-Net with self-attention trained via flow matching — maps coarse (64 km) climate forcing + high-resolution topography to 4 km precipitation fields over southeast Alaska. Training uses 120 time steps of WRF max-3-day snowfall (CFSR 1981–2010 baseline + GFDL CM3/CCSM4 2031–2060 projections); evaluation on 30+ held-out steps. Generates 50-member ensembles via ODE integration (~10 function evaluations per sample) in seconds on an RTX 4070 laptop GPU.
- **Key result:** 87.8% improvement in mean absolute log-spectral error vs. lapse-rate-corrected bicubic baseline (0.141 vs. 1.152); spectral bias −0.065 vs. −1.148 for WxFlow vs. bicubic. CRPS also markedly lower, especially over high-relief terrain. Ensemble spread is spatially coherent, tracking topographic uncertainty (rain-shadow, orographic enhancement).
- **Why it matters:** Enables probabilistic, physically plausible precipitation ensembles at 4 km for hazard assessment, water resources, and avalanche risk without WRF's compute cost; generalizable to other complex-terrain regions and CMIP-class forcings.
- **Caveats:** Small high-frequency spectral deficit (<0.3 dB, 1–3 pixel wavelengths) common to generative models. Validated only as WRF emulation — not independently verified against in-situ observations. Training dataset is modest (120 time steps). Domain limited to southeast Alaska; transferability untested.

## Tags

ML remote-sensing climate hydrology
