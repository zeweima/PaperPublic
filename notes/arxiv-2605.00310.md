# [Beyond Visual Fidelity: Benchmarking Super-Resolution Models for Large-Scale Remote Sensing Imagery via Downstream Task Integration](https://arxiv.org/abs/2605.00310)

**Authors:** Zhili Li, Kangyang Chai, Zhihao Wang et al.
**Venue:** arXiv · **Date:** 2026-05-01 · **DOI:** n/a
**Score:** <unclear from abstract>/10
**Source:** full text

## TL;DR

PSNR/SSIM rankings for satellite SR models frequently anti-correlate with downstream task performance, exposing a fundamental misalignment in how SR is evaluated for Earth observation.

## Summary

- **Problem:** Remote sensing SR research optimizes and ranks models by PSNR/SSIM, but whether higher fidelity translates to better land cover mapping, infrastructure detection, or biophysical estimation is untested at scale.
- **Method:** GeoSR-Bench — ~36,000 spatially co-located, same-day image pairs from MODIS (500 m) → Landsat-8 (30 m) and Sentinel-2 (10 m) → NAIP (0.6 m), stratified by urban/non-urban land cover. Ten pixel-level downstream tasks (land cover segmentation, building/road detection, GPP regression, canopy height estimation). Nine SR models (transformer: ATD, RGT, CFAT, CAMixer; neural operator: SRNO; GAN: ESRGAN, SeD; diffusion: BiDiff, UPSR) evaluated across 270 experimental settings with U-Net, SegFormer, and Swin Transformer as downstream models. Pearson and Spearman top-k correlation analyses link SR metric rankings to task metric rankings.
- **Key result:** Transformer/neural-operator SR models lead on PSNR/SSIM; GAN and diffusion models lag. Yet in the Sentinel-2→NAIP task, the GAN model SeD outperforms all others on building and road detection (F1 gains of 4–>30% over Sentinel-2 baseline), while achieving lower PSNR/SSIM. Pearson correlations between PSNR/SSIM and downstream F1 are negative or near-zero for the top-3 to top-5 competitive models in the majority of dataset–model combinations, particularly in the Sentinel-2→NAIP setting. The best SR models (ATD, SRNO) recover <⅓ of the Landsat-8 vs. MODIS performance gap on classification tasks. For sub-pixel targets (individual tree mortality, crown 5–10 m vs. 10 m Sentinel-2 pixels), SR improves F1 by only 0–4% over the Sentinel-2 baseline (F1 ≈ 0.001 for S2 raw).
- **Why it matters:** Practitioners selecting SR models for land cover mapping, GPP estimation, or infrastructure mapping cannot rely on PSNR/SSIM to identify the best model; task-integrated benchmarking is necessary. GeoSR-Bench provides the dataset, labels, and evaluation protocol to do this, and is publicly released.
- **Caveats:** Coverage limited to continental US for medium-to-high SR task (NAIP footprint); downstream labels sourced from existing products with known errors; spectral misalignment between satellite and aerial platforms (NAIP is not atmospherically corrected) partially mitigated but not eliminated; evaluation restricted to pixel-level tasks, excluding object detection or scene classification.

## Tags
remote-sensing ML agroecosystem
