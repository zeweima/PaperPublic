# [Spectral Dynamic Attention Network for Hyperspectral Image Super-Resolution](https://arxiv.org/abs/2604.27326)

**Authors:** Tengya Zhang, Feng Gao, Lin Qi et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-30 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Dynamic sparse channel attention + frequency-enhanced FFN beats prior SOTA on hyperspectral super-resolution across two benchmark datasets.

## Summary

- **Problem:** Hyperspectral image super-resolution (HISR) suffers from spectral redundancy — highly correlated bands disperse Transformer attention onto non-informative channels — and from limited non-linear modeling capacity in standard FFNs.
- **Method:** SDANet (2.67 M params, 9.48 GFLOPs) built around Spectral Dynamic Attention Blocks (SDABs). Each SDAB contains: (1) Dynamic Channel Sparse Attention (DCSA) — computes channel-wise attention then applies a data-driven Top-K gating (Dynamic Sparse Gating) to zero out redundant attention entries, keeping only the most discriminative spectral dependencies; (2) Frequency-Enhanced FFN (FE-FFN) — dual parallel branches apply FFT + depthwise convolution (5×5 and 3×3 kernels) in frequency space, cross-exchange split feature halves, then reconstruct via inverse FFT before spatial refinement. Tested on Chikusei (512×512×128, 4× and 8×) and Pavia Centre (256×256×102, 4× and 8×) with PSNR, SSIM, SAM, CC, and ERGAS metrics.
- **Key result:** On Chikusei ×4: PSNR 40.5060 dB, SSIM 0.9472, SAM 2.2606 — best across all metrics vs. seven baselines (MSDFormer, AS3UNet, CST, HSRMamba, etc.). On Pavia ×4: PSNR 32.2392 dB, SSIM 0.8825, SAM 4.7926 — again best. Ablation confirms removing DCSA reduces PSNR/SSIM and raises SAM; replacing dynamic sparsification with fixed-K (C or C/2) also degrades performance, validating the data-driven gating.
- **Why it matters:** Provides a lightweight, open-source HISR backbone (code at github.com/oucailab/SDANet) directly applicable to precision agriculture, environmental monitoring, and ocean color remote sensing where spatial resolution is the bottleneck for HSI utility.
- **Caveats:** Benchmarks limited to two datasets; no evaluation on satellite-acquired HSI (e.g., PRISMA, DESIS) or cross-sensor generalization. Dynamic K selection strategy is learned end-to-end but sensitivity to hyperparameter λ (loss weight = 0.2) shown only in supplementary. Real-world LR inputs differ from bicubic downsampling assumed here.

## Tags
remote-sensing ML
