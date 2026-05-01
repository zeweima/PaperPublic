# [PINN-Cast: Exploring the Role of Continuous-Depth NODE in Transformers and Physics Informed Loss as Soft Physical Constraints in Short-term Weather Forecasting](https://arxiv.org/abs/2604.27313)

**Authors:** Hira Saleem, Flora Salim, Cormac Purcell
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-30 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Replacing discrete residual updates in a transformer weather encoder with Neural ODE layers plus physics-informed loss penalties outperforms both discrete and continuous-ODE baselines on ERA5 short-term forecasts.

## Summary

- **Problem:** Transformer-based weather forecasters are physics-agnostic and evolve latent representations via discrete residual steps, poorly suited to the smooth, continuously evolving atmospheric dynamics they aim to model.
- **Method:** PINN-Cast replaces discrete residual updates in each transformer encoder block with Neural ODE (NODE) layers solved via adaptive numerical integration (dopri5). A two-branch attention module fuses standard patch-wise self-attention with a derivative-based branch that applies finite differences to attention logits, adding a change-sensitive interaction signal. Training loss combines latitude-weighted MSE with two soft physics penalties: kinetic energy error (|KE_pred − KE_true|) and a thermodynamic advection residual (∂T/∂t + u∂T/∂x + v∂T/∂y ≈ 0). Evaluated on WeatherBench ERA5 at 5.625° (32×64 grid), 1979–2015 train, 2017–2018 test, against non-pretrained ClimaX and ClimODE baselines.
- **Key result:** PINN-Cast outperforms both baselines at all lead times (6–36 h). For T2m at 36 h: RMSE 1.42 K (PINN-Cast) vs. 1.70 K (ClimODE) vs. 2.85 K (ClimaX); ACC 0.96 vs. 0.94 vs. 0.84. For 10-m winds at 36 h: RMSE ~1.89–1.92 m/s vs. 2.25–2.29 m/s (ClimODE). Ablations confirm each component (two-branch attention, NODE updates, physics loss) individually improves over the vanilla ViT baseline, with full combination giving best results.
- **Why it matters:** Shows that lightweight NODE residuals inside a transformer encoder — without expensive full-ODE rollout — combined with thermodynamic soft constraints meaningfully close the gap between data-driven and physics-based short-term forecasting while training in ~2 days on 4 V100 GPUs.
- **Caveats:** Evaluation limited to coarse 5.625° resolution and restricted baselines (no pretrained ClimaX, no Pangu-Weather or GraphCast comparisons). Physics penalties use unscaled finite differences without latitude-dependent grid spacing, so they encourage directional consistency rather than dimensionally exact conservation. Generalization to higher resolutions and longer lead times untested.

## Tags
ML climate remote-sensing
