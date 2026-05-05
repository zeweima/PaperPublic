# [Physics-Informed Neural Learning for State Reconstruction and Parameter Identification in Coupled Greenhouse Climate Dynamics](https://arxiv.org/abs/2605.02524)

**Authors:** Sani Biswas, Khursheed J. Ansari, Md. Nasim Akhtar
**Venue:** arXiv (cs.LG) · **Date:** 2026-05-04 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** abstract

## TL;DR

Coupled PINNs jointly reconstruct greenhouse temperature and humidity and recover governing parameters from sparse, noisy data better than pure data-driven baselines.

## Summary

- **Problem:** Greenhouse climate state estimation is hard under sparse and noisy sensor conditions; purely data-driven networks lack physical consistency and struggle with latent humidity dynamics.
- **Method:** Coupled PINN framework embedding a reduced-order physically motivated model (diurnal forcing) into neural network training; simultaneously reconstructs indoor temperature and humidity while identifying key physical parameters. Evaluated on a controlled synthetic benchmark mimicking diurnal cycles.
- **Key result:** Coupled PINN outperforms a data-driven baseline on both channels; improvement is most pronounced in humidity reconstruction where latent moisture dynamics are harder to infer. Physical parameters governing system dynamics successfully recovered alongside state estimates.
- **Why it matters:** Demonstrates that physics-informed learning can deliver interpretable, parameter-aware state reconstruction in data-scarce enclosed agricultural environments — extensible to other environmental monitoring systems with limited sensors.
- **Caveats:** Evaluated only on synthetic benchmark data, not real greenhouse observations; reduced-order model fidelity limits applicability to more complex or poorly characterized greenhouse geometries. Quantitative accuracy numbers are not reported in the abstract.

## Tags
ML agroecosystem LSM
