# [Evaluating the Alignment Between GeoAI Explanations and Domain Knowledge in Satellite-Based Flood Mapping](https://arxiv.org/abs/2604.26051)

**Authors:** Hyunho Lee, Wenwen Li
**Venue:** arXiv · **Date:** 2026-04-28 · **DOI:** n/a
**Score:** <unclear from abstract>/10
**Source:** full text

## TL;DR

ADAGE framework uses Channel-Group SHAP and mAP@k scoring to quantitatively assess whether deep learning flood-mapping explanations agree with established remote sensing domain knowledge.

## Summary

- **Problem:** Deep learning semantic segmentation models for satellite flood mapping show strong predictive performance, but no systematic method existed to verify whether their pixel-level explanations align with established spectral domain knowledge (e.g., SAR penetrates clouds; NIR outperforms RGB for water under thin cloud cover). Shortcut learning vs. physically grounded reasoning could not be distinguished.
- **Method:** ADAGE (Alignment between Domain Knowledge And GeoAI Explanation Evaluation) five-stage framework: (1) define input channels and encode domain knowledge as reference explanations; (2–3) train and evaluate a DLSS-RS model (U-Net / U-Net++ with ResNet-50); (4) compute Channel-Group SHAP values — a pixel-level extension of GroupSHAP that attributes predictions to predefined sensor/band groups (e.g., SAR={VV,VH}, RGB={R,G,B}, NIR={NIR}); (5) score alignment via mean Average Precision at k (mAP@k). Validated on two datasets: C2S-MS Floods (900 SAR+MSI image pairs, 18 flood events 2016–2020) for multimodal post-flood water extent mapping, and UrbanSARFloods (8,879 SAR+InSAR coherence pairs, 18 events 2016–2023) for open and urban flood detection.
- **Key result:** Framework successfully quantifies alignment scores (mAP@k) per pixel class and reference explanation set; domain-knowledge-inconsistent explanations (e.g., model over-relying on RGB under cloud cover) are identifiable and distinguishable from correct, knowledge-grounded explanations. Specific mAP@k values are in Table 3 (beyond page 12 cutoff), but the framework demonstrated reliable detection of misaligned explanations across both U-Net and U-Net++ architectures.
- **Why it matters:** Provides the first quantitative workflow for auditing GeoAI model trustworthiness against remote sensing domain knowledge, directly addressing shortcut-learning risks before operational deployment. mAP@k is robust to SHAP approximation errors because it ranks rather than compares absolute values.
- **Caveats:** Channel-Group SHAP assumes channel group independence and local linearity (first-order Taylor expansion), both approximations; alignment scores are evaluated only on True Positives, so misaligned reasoning behind false predictions is not characterized. Framework applicability depends on availability of well-defined, physics-grounded reference explanations, which may not exist for all mapping tasks.

## Tags
remote-sensing ML
