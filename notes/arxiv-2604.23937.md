# Multi-scale Dynamic Wake Modeling of Floating Offshore Wind Turbines via Fourier Neural Operators and Physics-Informed Neural Networks

**Authors:** Guodan Dong, Jianhua Qin, Chang Xu
**Venue:** arXiv (physics.flu-dyn) · **Date:** 2026-04-27 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

FNO outperforms PINN for floating offshore wind turbine wake prediction — ~8x faster training and resolves high-frequency coherent structures that PINN smooths away.

## Summary

- **Problem:** Real-time wake prediction for floating offshore wind turbines (FOWTs) under coupled surge-pitch 6-DOF motions requires models that capture multi-scale turbulent structures across Strouhal numbers St = [0, 0.6]; existing analytical and CFD approaches are too costly, and data-driven alternatives had not been tested on high-fidelity FOWT data.
- **Method:** FNO and PINN applied for the first time to FOWT wake reconstruction and prediction; training data from LES + Actuator Line Method (20 million grid cells, Δx = D/64 near-wake resolution) of NREL 5 MW turbine under coupled surge (A = 0.04D) and pitch (5°) oscillations at six St values; PINN uses 2D Navier-Stokes residuals in loss; FNO operates in Fourier spectral domain with quasi-linear computational complexity via FFT.
- **Key result:** FNO training speed ~8x faster than PINN; FNO resolves primary wake meandering frequency (St) plus harmonics 2St and 3St; PINN acts as a spatiotemporal low-pass filter, underestimating high-frequency energy and failing to reproduce small-scale coherent structures or the intensity of wake-center and wake-half-width temporal fluctuations.
- **Why it matters:** FNO-based surrogate enables high-fidelity, real-time-capable wake predictions suitable for wind farm layout optimization and active wake control without repeated CFD runs; spectral fidelity at harmonics is critical for fatigue load estimation of downstream turbines (wake-induced power losses up to 40–80%, fatigue load increases up to 80%).
- **Caveats:** Study limited to uniform inflow (no atmospheric turbulence), prescribed surge-pitch motions only (not full 6-DOF), 2D PINN formulation; generalizability to farm-scale interactions and turbulent inflow untested; FNO trained on single-turbine LES data so out-of-distribution St or motion amplitudes need evaluation.

## Tags
ML climate
