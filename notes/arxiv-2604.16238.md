# [Enhancing AI and Dynamical Subseasonal Forecasts with Probabilistic Bias Correction](https://arxiv.org/abs/2604.16238)

**Authors:** Hannah Guan, Soukayna Mouatadid, Paulo Orenstein et al.
**Venue:** arXiv · **Date:** 2026-04-17 · **DOI:** arxiv-2604.16238
**Score:** n/a/10
**Source:** full text

## TL;DR

A lightweight ML post-processing framework (PBC) applied to ECMWF dynamical and AI subseasonal forecasts doubles-to-triples skill at weeks 3–4 and won the 2025 ECMWF AI Weather Quest competition.

## Summary

- **Problem:** Subseasonal (2–6 week) forecasts degrade sharply beyond two weeks due to compounding systematic model errors; even state-of-the-art dynamical and AI ensembles routinely underperform climatology at these lead times, especially for precipitation.
- **Method:** Probabilistic bias correction (PBC) — two complementary ML modules (Debias++, which subtracts location/date/quantile-specific probability bias over adaptively selected training windows, and Persistence++, which blends lagged observations and climatology) applied in probability space rather than observation space, then ensembled. Tested on ECMWF ENS, AIFS-SUBS, and the hybrid PoET model; evaluated via ranked probability skill score (RPSS) against ERA5 reanalysis on a 1.5° global grid, 2016–2024.
- **Key result:** Applied to ECMWF: PBC beats debiased ECMWF RPSS by 26–38% for temperature and 16–33% for pressure; 98% of grid cells show precipitation skill gains, 91–92% for temperature, 89–91% for pressure. Applied to AIFS-SUBS: triples positive precipitation skill (week 3) and doubles sea-level pressure skill (week 4). Extreme-event BSS gains over debiased ECMWF: 44–54% temperature, 35–95% pressure, >100% precipitation. In the 2025 ECMWF AI Weather Quest real-time competition, PBC ensemble (MicroDuet) placed 1st across all variables and lead times against 34 teams and six operational forecasting centers.
- **Why it matters:** Demonstrates that lightweight probabilistic post-processing can close most of the subseasonal "predictability desert" gap without retraining physics models; direct implications for agricultural planning, flood early warning, and energy management. Open-source code released.
- **Caveats:** PBC corrects predictable systematic errors but cannot recover unpredictable atmospheric variability; gains depend on quality of the input ensemble signal. Evaluated primarily on temperature, precipitation, and sea-level pressure — extension to other variables (soil moisture, wind) not demonstrated. Operational deployment relies on continuous reanalysis data availability.

## Tags
ML climate remote-sensing
