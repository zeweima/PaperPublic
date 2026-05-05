# [Smart Ensemble Learning Framework for Predicting Groundwater Heavy Metal Pollution](https://arxiv.org/abs/2605.00056)

**Authors:** T. Ansah-Narh, G. Y. Afrifa, J. B. Tandoh et al.
**Venue:** arXiv (stat.ML) · **Date:** 2026-04-29 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** abstract

## TL;DR

Gaussian copula transformation with stacked ensemble ML predicts groundwater Heavy Metal Pollution Index more reliably (R²=0.96) than raw or log-transformed models in Ghana's Densu Basin.

## Summary

- **Problem:** Predicting the Heavy Metal Pollution Index (HPI) in groundwater is complicated by skewed distributions and correlated contaminants; naive models produce inflated fits without addressing these distributional issues.
- **Method:** Three response transformations (raw, log, Gaussian copula) applied to HPI from Densu Basin (Ghana) samples, evaluated across six learners — SVM, k-NN, CART, Elastic Net, kernel ridge regression, and a stacked Lasso ensemble — using nested cross-validation. DBSCAN clustering used to identify dominant contaminant contributors.
- **Key result:** Raw-scale models showed deceptively high fits (Elastic Net and stacked ensemble R²≈1.0, indicating over-optimism). Log transformation improved stability (SVM: R²=0.93, RMSE=0.18). Gaussian copula gave the most reliable results: stacked ensemble R²=0.96, RMSE=0.19, with spatially plausible contamination maps. DBSCAN identified Fe and Mn as primary HPI drivers.
- **Why it matters:** Distribution-aware preprocessing is critical before applying ML to skewed geochemical indices; copula-based ensembles produce more interpretable and spatially credible pollution maps than uncorrected models.
- **Caveats:** Cross-validation is random rather than spatial, which can inflate apparent generalization performance; findings are scoped to the Densu Basin and may not transfer to other hydrogeological settings.

## Tags
water-quality ML hydrology
