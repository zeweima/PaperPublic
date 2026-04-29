# climt-paraformer: Stable Emulation of Convective Parameterization using a Temporal Memory-aware Transformer

**Authors:** Shuochen Wang, Nishant Yadav, Joy Merwin Monteiro et al.
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-22 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

A temporal memory-aware Transformer emulating the Emanuel convective parameterization outperforms MLP and LSTM baselines offline and sustains stable coupled simulation for 10 years, with optimal convective memory of ~100 minutes (T_w = 5 × 10-min steps).

## Summary

- **Problem:** NN-based convective parameterization emulators are typically memory-less, ignoring that convection depends on prior atmospheric states; incorporating past states as concatenated features does not explicitly model temporal ordering or interactions among them.
- **Method:** Transformer encoder with causal masking trained on 400,000 single-column radiative-convective equilibrium samples from the Emanuel scheme in the climt single-column model (SCM); inputs are T_w consecutive atmospheric profiles (temperature, humidity, surface fluxes, 28 vertical levels); outputs are heating tendency dT/dt, moistening tendency dQ/dt, and convective precipitation. Compared against unconstrained MLP, physically-constrained MLP (zero tendencies above level k_0 = 19, ~268 hPa), and LSTM. 10-year online (coupled) simulations run to assess stability.
- **Key result:** Transformer with T_w = 5 (50-min memory) achieves ~5× lower nRMSE than unconstrained MLP for both dT/dt and dQ/dt, and lower error than constrained MLP and LSTM at nearly all vertical levels. Physical constraints alone reduce MLP nRMSE by >50% (from 0.55 to 0.15 for dT/dt). Extending memory beyond T_w = 10 (100 min) degrades offline performance; T_w = 20 (200 min) performs worst. In online simulation, constrained MLP crashes at 2620 steps, LSTM at 1388 steps, while the Transformer remains stable for the full 10-year run. Moistening tendencies (dQ/dt) are consistently harder to emulate than heating tendencies; convective precipitation shows the largest offline-to-online discrepancy.
- **Why it matters:** Demonstrates that explicit sequential modeling of convective memory via Transformer attention is needed for both offline accuracy and long-term online stability, and that an optimal memory window (~1 hour) exists — providing a practical design rule for next-generation ML parameterizations in GCMs.
- **Caveats:** Tested only in an idealized single-column SCM under radiative-convective equilibrium; the Emanuel scheme is one parameterization among many; full 3D GCM integration and generalization to other convective regimes not demonstrated. Convective precipitation regime-dependent behavior remains difficult to capture stably online.

## Tags
ML LSM climate
