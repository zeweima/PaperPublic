# [RAFNet: Region-Aware Fusion Network for Pansharpening](https://arxiv.org/abs/2605.02184)

**Authors:** Jianing Zhang, Zijian Zhou, Kai Sun
**Venue:** arXiv (cs.LG) · **Date:** 2026-05-04 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** abstract

## TL;DR

Region-aware sparse attention with DWT-based frequency separation and K-means clustering outperforms state-of-the-art pansharpening methods on multiple benchmarks.

## Summary
- **Problem:** Standard frequency-based pansharpening uses scaled dot-product attention (quadratic complexity) and static convolution kernels that fail to adapt to the regional and frequency heterogeneity of PAN and MS remote sensing images.
- **Method:** RAFNet combines two modules: (1) Spatial Adaptive Refinement (SAR) — uses discrete wavelet transform for directional frequency separation and K-means clustering to build region-specific adaptive convolution kernels; (2) Clustered Frequency Aggregation (CFA) — sparse attention guided by semantic clusters to cut computational redundancy. Both are integrated into a multi-level spatial-frequency architecture.
- **Key result:** Significantly outperforms state-of-the-art pansharpening methods on multiple benchmark datasets in both reduced- and full-resolution evaluations; specific dB/metric numbers not reported in abstract.
- **Why it matters:** Reduces quadratic attention cost by exploiting regional sparsity, enabling higher-quality HRMS fusion for downstream remote sensing applications (classification, change detection, etc.).
- **Caveats:** Benchmark comparisons and quantitative margins not stated in abstract; generalization to sensor types outside tested datasets unclear; K-means clustering adds a hyperparameter (number of clusters) not discussed.

## Tags
remote-sensing ML
