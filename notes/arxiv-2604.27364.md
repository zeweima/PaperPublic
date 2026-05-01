# [Hyperspectral Image Classification via Efficient Global Spectral Supertoken Clustering](https://doi.org/10.1016/j.isprsjprs.2026.04.041)

**Authors:** Peifu Liu, Tingfa Xu, Jie Wang et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-30 · **DOI:** https://doi.org/10.1016/j.isprsjprs.2026.04.041
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Decoupling clustering from pixel-wise classification via spectral supertokens yields CF1 0.728 at 197.75 FPS on WHU-OHS, the best accuracy-efficiency trade-off among published methods.

## Summary

- **Problem:** Superpixel-based HSI classifiers aggregate pixels into regions for feature extraction but revert to pixel-wise prediction, breaking regional consistency and producing inaccurate boundary delineation.
- **Method:** Dual-stage Spectrum-Constrained Clustering-based Classifier (DSCC). Stage 1: Spectral-Consistent Pixel Aggregation (SCPA) computes global image-level multi-criteria feature distance (spectral bands + spectral derivative + deep semantic features) to assign all pixels to clustering centers in one shot, then Density-Isolation Center Filtering (DICF) retains only high-density, well-separated centers. Stage 2: a hybrid Transformer-Mamba classifier predicts at the token level; a Category Proportion-aware Soft Label encodes within-token class proportions to handle mixed-cover tokens. Evaluated on WHU-OHS (7795 images, 24 classes, 32 bands, 10 m), Indian Pines, KSC, WHU-Hi-HanChuan, and HyRANK-Dioni.
- **Key result:** WHU-OHS: CF1 0.728, OA 0.802, mIoU 0.602 at 197.75 FPS and 34.33 G FLOPs — outperforms next-best S2Mamba (CF1 0.723) at ~2.5× fewer FLOPs. On KSC: AA 0.9985 (+0.0183 vs. DSTC). On IP: OA 0.9885 (+0.0270 vs. DSTC). Ablation: soft-label supervision raises CF1 from 0.716 (dense-CE) to 0.728; combining semantic features and spectral derivative raises CF1 from 0.713 (baseline) to 0.728.
- **Why it matters:** Provides a practical path to region-consistent, boundary-accurate hyperspectral land-cover mapping at real-time inference speed — relevant for operational land-use monitoring, urban mapping, and precision agriculture from satellite/airborne HSI.
- **Caveats:** Global pixel-center distance computation scales as O(N × M); tested only on relatively small/medium HSI scenes. Performance on very large-swath satellite HSI (e.g., DESIS, PRISMA full scenes) is untested. Patch-wise evaluation protocol on smaller benchmark datasets (IP, KSC) may overstate generalization relative to full-scene inference.

## Tags
remote-sensing ML
