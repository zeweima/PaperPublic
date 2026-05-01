# [Representative Spectral Correlation Network for Multi-source Remote Sensing Image Classification](https://arxiv.org/abs/2604.27323)

**Authors:** Chuanzheng Gong, Feng Gao, Junyan Lin et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-30 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

RSCNet fuses HSI with SAR/LiDAR by dynamically selecting discriminative spectral bands under cross-source guidance, outperforming 10 state-of-the-art methods on three benchmark datasets with lower computational cost.

## Summary

- **Problem:** Fusing hyperspectral imagery (HSI) with SAR/LiDAR for land-cover classification is hampered by (1) spectral redundancy across hundreds of HSI bands and (2) heterogeneous imaging characteristics between the two source types; conventional PCA-based dimensionality reduction discards task-relevant spectral signatures before fusion.
- **Method:** RSCNet introduces two jointly trained modules. The Key Band Selection Module (KBSM) uses structural/spatial priors from SAR/LiDAR to drive Top-k sparse attention over HSI bands, selecting only the k most discriminative bands (k set to 50% for Augsburg, 20% for Berlin and Houston2013). The Cross-source Adaptive Fusion Module (CAFM) aligns heterogeneous features via cross-source attention weighting followed by local–global dual attention refinement. These modules iterate inside N Representative Spectral Correlation Blocks (N=4 optimal). Evaluated on Augsburg (HSI+SAR, 7 classes), Berlin (HSI+SAR, 8 classes), and Houston2013 (HSI+LiDAR, 15 classes) datasets.
- **Key result:** RSCNet achieves OA/AA/Kappa of 91.50%/67.89%/0.8776 (Augsburg), 78.19%/61.98%/0.6544 (Berlin), and 92.66%/93.76%/0.9204 (Houston2013), topping all 10 competing methods. Multi-source fusion (HSI+SAR/LiDAR) surpasses HSI-only by up to 3.27 OA points (Houston2013). KBSM alone outperforms five established band-selection methods on Berlin (78.19% vs. next-best 77.43% LGCAF). Model size is 2.88 M parameters with 0.33 GFLOPs, substantially lighter than FusAtNet (36.8 M) and CHNet (20.8 M).
- **Why it matters:** Tightly coupling spectral band selection with multi-source fusion — rather than treating them as sequential independent steps — preserves class-specific spectral signatures that PCA-based preprocessing discards. This is directly relevant to land-cover mapping workflows that combine airborne/spaceborne HSI with SAR or LiDAR elevation data (e.g., EnMAP + Sentinel-1, AVIRIS + LiDAR).
- **Caveats:** All three benchmarks are urban scenes; generalization to vegetation-dominated or mixed landscapes is untested. Datasets are relatively small (761–2832 training samples), so gains may not transfer to large-scale operational mapping. The k band-ratio hyperparameter is dataset-dependent and requires tuning.

## Tags
remote-sensing ML
