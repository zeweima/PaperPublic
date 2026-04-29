# Assessing Emulator Design and Training for Modal Aerosol Microphysics Parameterizations in E3SMv2

**Authors:** Shady E. Ahmed, Hui Wan, Saad Qadeer et al.
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-23 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Systematic FNN design-space sweep for MAM4 aerosol microphysics emulation shows power-transformed 3×256 networks reach R² ≈ 0.99 across all 20 target mixing ratios.

## Summary

- **Problem:** ML emulators for aerosol microphysics in global ESMs (E3SMv2 MAM4) show R² ranging 0.48–0.99 across studies; no baseline explains why, and no principled design guide exists.
- **Method:** Feedforward neural networks (ReLU, residual connections) trained on 6.6×10⁶ samples from a boreal-winter E3SMv2 control simulation (ne30pg2 grid, ~165 km, 30-min timestep); grid search over depths {1,2,3,5,8} and widths {32,64,128,256,512}; compared z-score vs. power transformation (exponent 1/5) for variable normalization; Adan optimizer, lr=3×10⁻⁴, 5000 epochs, batch size 4096; target variables are 30-min changes in 18 interstitial aerosol mixing ratios + H₂SO₄ + SOAG under cloud-free conditions.
- **Key result:** With power transformation and full convergence, a 3-hidden-layer × 256-neuron FNN achieves R² ≈ 0.982–1.000 on all 20 target variables (test set). Without proper scaling or convergence, accuracy degrades sharply; shallowest/narrowest networks (depth 1 or width 32) plateau at R² ~0.725–0.868. Hardest variables: marine organic matter (mom), sea salt (ncl), secondary organic aerosol (soa/SOAG), and Aitken-mode particle number (num_a2).
- **Why it matters:** Establishes a reproducible baseline and identifies power-based variable transformation and training convergence monitoring as the critical bottlenecks—not architecture depth—for aerosol microphysics emulation; lessons generalize to other ODE-based parameterizations with multiscale variability.
- **Caveats:** Single season (boreal winter) only; cloud-free interstitial aerosols only; cloud-borne aerosols and stratospheric layers excluded; no online in-model testing; generalizability across seasons and forcing scenarios deferred.

## Tags
ML climate
