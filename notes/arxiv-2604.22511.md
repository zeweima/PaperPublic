# Optimal sensor placement for the reconstruction of ocean states using differentiable Gumbel-Softmax sampling operator

**Authors:** Oscar Chapron, Ronan Fablet, Yann Stéphan
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-24 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Differentiable Gumbel-Softmax sensor placement jointly optimizing observation mask and Optimal Interpolation parameters halves SSH reconstruction RMSE versus random sampling at 0.1% sensor budget.

## Summary

- **Problem:** Adaptive in situ sensor placement for ocean field reconstruction is intractable with classical methods (EOF, greedy, Gaussian process) at high resolution under evolving dynamics and strict deployment budgets.
- **Method:** Gumbel-Softmax relaxation of Bernoulli sensor selection enables end-to-end gradient-based co-optimization of (1) a probabilistic spatial sampling mask and (2) OI correlation-length parameters. Training uses spatially perturbed ensemble forecasts from NATL60/eNATL60 NEMO simulations (12°×12° Gulf Stream region, 1/20° resolution, daily timesteps) as proxies for operational forecast uncertainty. Sensor budget fixed at 0.1% of grid points (~100 observations on a 14°×14° domain). Monte Carlo approximation over 45 ensemble realizations; temperature annealing on the Gumbel-Softmax; Adam optimizer, 1000 iterations.
- **Key result:** Optimized mask RMSE = 0.0908 m vs. 0.1750 m for uniform random (48% reduction in MSE); explained variance 93.1% vs. 74.4% (+18.7 pp). Robust to spatially coherent forecast displacement up to 1° (~110 km): trained masks still outperform all baselines (random, block-stratified, regularized-grid) in 70–80% of realizations at 1° displacement and 95% at 0.5°. Optimized masks concentrate on high-gradient, high-curvature SSH regions (eddies, fronts, saddle points) versus random strategies.
- **Why it matters:** Provides a practical, scalable framework for designing adaptive observation networks for gliders/drifters without ground-truth supervision during training; learned placements are physically interpretable and transferable across forecast regimes.
- **Caveats:** Tested only on SSH in one Gulf Stream subdomain; OI reconstruction is linear and assumes stationarity within the correlation length; no real in situ validation; performance at 1.5° displacement shows detectable skill degradation.

## Tags
remote-sensing ML hydrology climate
