# [A generalised pre-training strategy for deep learning networks in semantic segmentation of remotely sensed images](https://arxiv.org/abs/2604.27704)

**Authors:** Yuan Fang, Yuanzhi Cai, Jagannath Aryal et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-30 · **DOI:** n/a
**Score:** 8/10 <sup>top pick</sup>
**Source:** full text

## TL;DR

Channel Shuffling Pre-training (CSP) on ImageNet alone achieves SOTA segmentation across RGB, multispectral, and multimodal remote sensing datasets by suppressing spectral-specific feature learning.

## Summary

- **Problem:** Domain gap between ImageNet RGB images and remotely sensed images (diverse modalities, spectral bands) degrades fine-tuned segmentation models; collecting large domain-specific pre-training datasets is costly and transfers poorly across scenarios.
- **Method:** Channel Shuffling Pre-training (CSP) — duplicate ImageNet channels to match target channel count *n*, randomly shuffle channel order, then pre-train on the shuffled inputs. Prevents models from learning fixed spectral cues, forcing emphasis on spatial and structural features. Tested with ConvNeXt-T and Swin-T (UperNet decoder) fine-tuned on four datasets: iSAID (RGB aerial, 16 classes), MFNet (RGB+thermal autonomous driving, 9 classes), PST900 (RGB+thermal subterranean, 5 classes), Potsdam (RGB+IR+DSM aerial, 6 classes). Pre-training on ImageNet-1K only (1.28 M images, 300 epochs).
- **Key result:** CSP achieved SOTA on all four benchmarks — 67.4% mIoU on iSAID (+0.8–1.6% over IM-RGB baseline), 56.9% mIoU on MFNet (+6.6% average), 84.22% mIoU on PST900 (+13.83% average), 91.88% mF1 on Potsdam. ImageNet-1K Top-1 accuracy drops 1.4–3.8% vs. standard pre-training (expected, as spectral cues are intentionally suppressed). CSP-trained Swin-T is robust to BGR channel reversal; IM-RGB model misclassifies visually similar classes under spectral perturbations.
- **Why it matters:** Eliminates need for domain-specific RS pre-training datasets while generalising across RGB, multispectral, and multimodal imagery; provides a path toward a unified foundation model spanning computer vision and remote sensing without retraining or domain-specific data collection.
- **Caveats:** Tested only with tiny-scale backbones (ConvNeXt-T, Swin-T) due to GPU memory limits; edge detection quality is reduced (blurred boundaries), suggesting CSP should be combined with edge-aware losses; performance gains are modest for 3-channel RGB datasets (iSAID) compared to multi-channel ones.

## Tags
remote-sensing ML
