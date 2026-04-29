# Connecting the forward problem to the inverse problem in uncertainty quantification of Earth system models using fast emulators

**Authors:** Ethan YoungIn Shin, Baris Kale, Michael F. Howland
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-21 · **DOI:** n/a
**Score:** 8/10 <sup>top pick</sup>
**Source:** full text

## TL;DR

Forward Sobol' sensitivity indices projected onto observation space non-iteratively identify which atmospheric observations most efficiently constrain WRF turbulence parameterization parameters in Bayesian calibration.

## Summary

- **Problem:** Bayesian parameter calibration of ESMs can be ill-posed if chosen observations weakly constrain parameters — a condition unknowable before running inference — yet forward sensitivity analysis requires prior parameter distributions learnable only from observations; neither approach alone closes the loop.
- **Method:** Gaussian process emulators trained on ~O(10²) WRF simulations replace O(10⁵) direct model evaluations for both global Sobol' sensitivity analysis and MCMC-based Bayesian inversion of 6 YSU PBL / SFCLAY parameters. Two nondimensional diagnostics — a signal-to-noise ratio (SNR, total-effect sensitivity variance / observational noise variance ≥ 1) and a main-to-interaction ratio (MIR, S_i / (S_Ti − S_i) ≥ 1) — identify observation-space regions where parameter signals are detectable and independently interpretable. Applied to idealized stable and convective dry PBL simulations in WRF v4.6.1.
- **Key result:** Observations satisfying both SNR ≥ 1 and MIR ≥ 1 serve as a strong proxy for reduced posterior uncertainty in emulator-aided Bayesian inversion with synthetic observations; parameter uncertainty was systematically reduced using sensitivity-selected observations compared to uninformed observation choices. Sensitivity indices vary substantially with atmospheric stability regime, time-averaging length, and spatial location.
- **Why it matters:** Provides a computationally cheap, non-iterative pre-screening step that replaces iterative Bayesian optimal experimental design for chaotic dynamical systems; applicable beyond ESMs to any UQ problem in chaotic models.
- **Caveats:** Tested only with synthetic (noise-free) observations; GP emulator interpolation not guaranteed outside sampled parameter space; diagnostic regions may be empty or disjoint for multi-parameter calibration; results demonstrated on idealized horizontally homogeneous PBL, not full mesoscale simulations.

## Tags

ML LSM climate
