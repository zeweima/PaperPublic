# [HQ-UNet: A Hybrid Quantum-Classical U-Net with a Quantum Bottleneck for Remote Sensing Image Segmentation](https://arxiv.org/abs/2604.27206)

**Authors:** Md Aminur Hossain, Ayush V. Patel, Ikshwaku Vanani et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-29 · **DOI:** n/a
**Score:** <unclear from abstract>/10
**Source:** full text

## TL;DR

Replacing the classical U-Net bottleneck with a compact quantum convolutional circuit yields mIoU 0.8050 and 94.76% accuracy on land-cover segmentation, beating the classical U-Net by 0.1599 mIoU.

## Summary

- **Problem:** Classical U-Net architectures for remote sensing semantic segmentation are parameter-heavy; prior hybrid quantum-classical models for segmentation performed poorly (mIoU ~0.15–0.20), leaving the quantum bottleneck concept underexplored for dense prediction.
- **Method:** HQ-UNet inserts a non-pooling Quantum Convolutional Neural Network (QCNN) at the U-Net bottleneck. A spectral-aware encoding maps 3-channel encoder features (reduced to 4×4 spatial grids via AdaptiveAvgPool2d) to 16 qubits via RX/RY/RZ rotation gates. A 2D separable quanvolution applies parameterized 2-qubit filters (horizontal then vertical passes) across encoded features. Pauli-Z and Pauli-X expectation values are extracted and projected back to classical feature maps before decoding. Evaluated on LandCover.ai (aerial RGB orthophotos of Poland, 5 classes, 128×128 patches). Simulated on a noise-free quantum simulator; circuit kept shallow for NISQ compatibility.
- **Key result:** mIoU = 0.8050, overall accuracy = 94.76% on LandCover.ai test set — +0.1599 mIoU and +12.33% OA over classical U-Net (mIoU 0.6451, OA 82.43%); outperforms best prior hybrid quantum model (FQCNN, mIoU 0.2000) by 0.6050 mIoU.
- **Why it matters:** Demonstrates that a shallow, parameter-efficient quantum circuit at the compression point of a segmentation network can improve feature representation for land-cover mapping; relevant for Earth observation where parameter-efficient models on future NISQ hardware are desirable.
- **Caveats:** Evaluated on a single dataset (LandCover.ai, Poland aerial imagery only); all quantum operations run on a noiseless simulator — real NISQ hardware noise not tested; no ablation quantifying contribution of the quantum bottleneck vs. the depthwise separable convolution redesign; generalization to multispectral or SAR data undemonstrated.

## Tags
remote-sensing ML
