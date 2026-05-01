# [ZAYAN: Disentangled Contrastive Transformer for Tabular Remote Sensing Data](https://arxiv.org/abs/2604.27606)

**Authors:** Al Zadid Sultan Bin Habib, Tanpia Tasnim, Md. Ekramul Islam et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-30 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Feature-level self-supervised contrastive pretraining with redundancy minimization outperforms 31 tabular deep-learning baselines on eight remote-sensing and flood-prediction datasets, achieving average rank 1.06.

## Summary

- **Problem:** Tabular remote sensing and environmental data suffer from high feature redundancy, heterogeneity, scarce labels, and distribution shift — conditions where sample-level contrastive SSL and standard Transformer models underperform.
- **Method:** ZAYAN has two components: (1) ZAYAN-CL, a feature-level contrastive pretraining module that applies a zero-anchor InfoNCE loss over individually augmented feature vectors (Gaussian noise, quantile warping, random masking) plus a redundancy penalty (||Z⊤Z − I||²_F) to push feature embeddings toward orthogonality; (2) ZAYAN-T, a downstream Transformer classifier that receives the disentangled feature embeddings with ZAYAN-aware positional encoding and a structure-preserving loss (γ · L_preserve). Evaluated on eight tabular datasets: six remote-sensing benchmarks (urban land cover, forest type, crop mapping, Wilt, satellite image classification, tree census) and two flood-prediction tables (pluvial flood with 50% label noise, Indian flood risk), via 5-fold cross-validation against 31 baselines tuned with Optuna.
- **Key result:** ZAYAN achieves best or tied-best accuracy on 7/8 datasets (Urban 84.80%, Forest Type 97.21%, Crop Mapping 99.66%, Pluvial Flood 93.61%, RSI-CB256 99.77%) and an average rank of 1.06 ± 0.17 vs. next-best TabICL at 3.38. Ablation shows removing the redundancy penalty drops accuracy by ~9 pp and removing contrastive loss drops it by ~9 pp on Urban Land Cover. Accuracy stable up to 25% shuffled features, dropping only beyond 50% removal.
- **Why it matters:** Provides a label-efficient, deployment-robust framework for environmental and remote sensing tabular classification — relevant to land cover mapping, flood risk, and any tabular sensing pipeline with heterogeneous, redundant features. Feature-level (not sample-level) CL is the key design insight enabling gains over tree ensembles and foundation-model baselines under distribution shift.
- **Caveats:** Redundancy penalty scales as O(m²) in time and memory, causing OOM on very high-dimensional inputs (e.g., 2048-d ResNet embeddings). Purely self-supervised augmentation omits label information. Batch latency ~5.36 ms is acceptable but quadratic complexity limits scaling to very large feature sets.

## Tags
remote-sensing ML agroecosystem
