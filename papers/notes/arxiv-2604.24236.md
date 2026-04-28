# Deep Learning-Enabled Dissolved Oxygen Sensing in Biofouling Environments for Ocean Monitoring

**Authors:** Nikolaos Salaris, Adrien Desjardins, Manish K. Tiwari
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-27 · **DOI:** n/a
**Score:** 8/10 <sup>top pick</sup>
**Source:** full text

## TL;DR
A Vision Transformer PINN embedding the Stern-Volmer equation into its loss function cuts dissolved oxygen MAE by 92% versus standard calibration under 14-day algal biofouling.

## Summary
- **Problem:** Camera-based optical DO sensors (phosphorescence quenching) fail under marine biofouling because algal growth creates spatiotemporally heterogeneous signal corruption that fixed-pixel averaging and static calibration strategies cannot handle; current DO models can deviate from observed deoxygenation rates by up to 100%.
- **Method:** Low-cost Raspberry Pi + UV LED + PtOEP–polystyrene phosphorescent film sensor submerged in an algae-laden tank for 14 days (accelerated biofouling). A hierarchy of methods was evaluated via Leave-One-(Day)-Out Cross-Validation: global pixel averaging (GA), per-pixel best-pixel selection, physics-reinforced LightGBM (LGA), CNN (ResNet-18 + CBAM), and a Vision Transformer-based Physics-Informed Neural Network (ViT-PINN / PCNN) with the Stern-Volmer equation embedded directly in the loss function. A deep ensemble quantified predictive uncertainty. An optional biofouling supervision term (crystal violet UV-Vis measurements) was also tested.
- **Key result:** Global averaging baseline MAE = 28.2 µmol/L; best pixel-selection MAE = 23.4 µmol/L; physics-reinforced LightGBM MAE = 18.5 µmol/L; CNN MAE = 8.1 µmol/L; ViT-PINN (PCNN) MAE = 5.5 µmol/L (~2 µmol/L in best-case scenario with biofouling supervision at 5.4 µmol/L). The PINN achieves 92% MAE reduction vs. GA and 58% vs. best LightGBM baseline. Physics loss weighting (λ_physics) was the single most important hyperparameter for convergence.
- **Why it matters:** Establishes a blueprint for self-diagnosing, drift-resilient optical ocean sensors deployable on simple hardware; pixel-wise physics residual maps serve as real-time "Physical Consistency Maps" flagging biofouled regions without manual inspection. Directly relevant to monitoring ocean deoxygenation and climate tipping points at scale.
- **Caveats:** Validated only in a controlled tank with algae; real ocean deployment involves additional fouling agents (bacteria, invertebrates, sediment), varying turbidity, pressure, and illumination changes. Dataset spans only 14 days and one sensor film. The ViT still shows attention maps misaligned with known film boundaries, suggesting further architectural improvement is possible. Biofouling supervision (UV-Vis) adds hardware complexity.

## Tags
water-quality, ML, remote-sensing, climate
