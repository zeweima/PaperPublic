# Open-Vocabulary Semantic Segmentation Network Integrating Object-Level Label and Scene-Level Semantic Features for Multimodal Remote Sensing Images

**Authors:** Jinkun Dai, Yuanxin Ye, Peng Tang et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-27 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR
TSMNet fuses optical, SAR, and textual modalities via dual-branch CLIP-based text encoding to enable open-vocabulary pixel-wise land-cover segmentation.

## Summary
- **Problem:** Multi-modal remote sensing segmentation methods fuse optical and SAR imagery but ignore textual data, locking models to predefined class taxonomies and limiting generalization across geographic domains.
- **Method:** TSMNet combines a pseudo-Siamese ViT backbone (optical + SAR) with a CLIP-based dual-branch text encoder that extracts both object-level label features (category names via prompt templates) and scene-level semantic features (free-text descriptions). A multi-modal feature rectification module (MFRM) corrects channel/spatial heterogeneity between modalities; a multi-modal feature fusion module (MFFM) applies cross-modal attention at multiple scales. A dual-branch image-text fusion module (DITF) integrates text embeddings into the segmentation decoder. Three losses are trained jointly: object-level label loss (cross-entropy), scene-level semantic loss (contrastive), and segmentation task loss. Two new datasets were constructed: one from Gaofen (GF) satellite optical+SAR pairs with manual text descriptions, and one by adding detailed text annotations to an existing multi-modal dataset.
- **Key result:** TSMNet achieves state-of-the-art segmentation accuracy on both new datasets and demonstrates robust generalization to unseen categories and diverse geographic/sensor scenarios; specific mIoU numbers are in later sections not covered by pages 1–12.
- **Why it matters:** Opens a path to user-defined, open-vocabulary land-use/land-cover mapping without retraining — particularly relevant for disaster response, environmental monitoring, and precision Earth observation where category needs shift rapidly.
- **Caveats:** Quantitative benchmark comparisons (mIoU tables) are in later sections not yet reviewed; computational cost of the three-stage pipeline with dual text encoders is not assessed here; dataset size and geographic diversity of the new GF dataset are not fully detailed in the first 12 pages.

## Tags
remote-sensing, ML, water-resources, geology
