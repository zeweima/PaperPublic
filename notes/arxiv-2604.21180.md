# Uncertainty-Aware Spatiotemporal Super-Resolution Data Assimilation with Diffusion Models

**Authors:** Aditya Sai Pranith Ayapilla, Kazuya Miyashita, Yuki Yasuda et al.
**Venue:** arXiv (physics.flu-dyn) · **Date:** 2026-04-23 · **DOI:** n/a
**Score:** 8/10
**Source:** full text

## TL;DR

DiffSRDA uses denoising diffusion models to produce ensemble HR analyses from cheap LR forecasts + sparse observations, matching EnKF-HR accuracy at a fraction of the cost.

## Summary

- **Problem:** Probabilistic data assimilation at high resolution (HR) requires large ensembles of expensive HR model runs; existing super-resolution DA (SRDA) operators are deterministic and provide no uncertainty estimates.
- **Method:** DiffSRDA — a conditional denoising diffusion model trained offline on a barotropic ocean jet instability testbed (LR: 32×16, HR: 128×64, UHR reference: 1024×512). The model takes a short LR forecast window + sparse HR observations (Gaussian noise σ=0.1, sampled every g=8 grid points) as conditioning inputs and generates a 5-frame HR analysis window via reverse diffusion. Ensemble uncertainty comes from repeating sampling with B=30 draws. Score-based observation-consistency guidance handles deployment-time sensor-layout changes without retraining.
- **Key result:** DiffSRDA point-estimate MAER tracks EnKF-HR (the gold standard using HR forecasts + 100-member ensemble) throughout the 24-time-unit simulation, and outperforms deterministic SRDA-YO2023 on both MAER and Laplacian RMSE (fine-scale structure). Wall-clock time: DiffSRDA 562.6 s vs. EnKF-HR 1040.2 s vs. EnKF-SR 44.5 s for one full cycling run; full-chain accuracy is largely retained with only a small number of reverse steps (K ≪ T=1000), making repeated cycling practical. Ensemble spread concentrates in dynamically active regions, consistent with EnKF-HR behavior.
- **Why it matters:** Enables uncertainty-aware HR analyses from cheap LR forecasts — relevant for geophysical DA where HR ensemble cycling is prohibitively expensive (NWP, ocean modeling). Training-free guidance mechanism allows adapting to shifted sensor networks at deployment without retraining.
- **Caveats:** Evaluated only on an idealized 2D barotropic jet; generalization to 3D operational models (atmosphere, ocean) is untested. Computational comparison favors EnKF-SR (44.5 s) over DiffSRDA (562.6 s) when uncertainty is not needed. Ensemble size of 30 samples may underestimate uncertainty tails compared to EnKF-HR's 100 members.

## Tags
ML remote-sensing climate
