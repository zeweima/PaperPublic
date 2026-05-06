# [Towards accurate extreme event likelihoods from diffusion model climate emulators](https://arxiv.org/abs/2605.03802)

**Authors:** Peter Manshausen, Noah Brenowitz, Julius Berner et al.
**Venue:** arXiv (cs.LG) · **Date:** 2026-05-05 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** abstract

## TL;DR

Probability densities from the cBottle diffusion climate emulator yield importance-sampled odds ratios for tropical cyclone likelihood under guidance, cutting TC probability estimate standard error versus naive Monte Carlo.

## Summary

- **Problem:** ML climate emulators enable cheap scenario sampling, but extracting calibrated extreme-event probabilities — not just plausible samples — from generative models remains undemonstrated.
- **Method:** Uses Climate in a Bottle (cBottle), a diffusion model conditioned on boundary conditions (solar position, SSTs), to generate atmospheric states. Guided generation steers the model toward tropical cyclone (TC)-containing states over specified locations; the ratio of guided to unguided probability densities yields odds ratios for TC occurrence. Importance sampling with these ratios is compared to standard Monte Carlo for probability estimation.
- **Key result:** Odds ratios from guided vs. unguided cBottle densities quantify how much more likely guidance has made a TC; importance sampling with these ratios reduces the standard error of TC probability estimates relative to simple Monte Carlo sampling. Early extreme-event attribution-like experiments are demonstrated.
- **Why it matters:** Opens a pathway for computationally cheap probabilistic extreme-event attribution and return-period estimation using diffusion-model emulators, without running expensive GCM ensembles.
- **Caveats:** Results are described as "early but encouraging"; accuracy of the probability density estimates from the diffusion model is unvalidated against observations or full GCM output; scope is limited to TCs with cBottle's training distribution; attribution-like experiments have unresolved limitations noted by the authors.

## Tags
ML climate remote-sensing
