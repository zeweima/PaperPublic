# Bridging the Sensitivity Gap in Precipitation Estimates from Spaceborne Radars using Passive Microwave Observations

**Authors:** Simon Pfreundschuh, Christian D. Kummerow
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-26 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR
Fusing CloudSat and GPM DPR reference data into a single passive-microwave retrieval cuts high-latitude precipitation underestimation by >50% and improves detection skill (CSI) 26%.

## Summary
- **Problem:** GPM DPR misses light (<0.1 mm h⁻¹) and frozen precipitation, causing systematic underestimation at high latitudes (zonal means diverge >80% poleward of 40°); because passive-microwave (PMW) algorithms like GPROF are trained on DPR references, they inherit the same bias.
- **Method:** GPROF-NN eXtended Precipitation Regime (XPR) — a U-Net encoder-decoder (EfficientNet-V2-style MBConv blocks) trained on GMI brightness temperatures plus ancillary surface/met variables. Two output heads share a latent representation: one predicts CPR-based (CloudSat 94 GHz) light-precipitation rates, the other DPR-based moderate-to-heavy rates. A Gaussian-weighted fusion scheme (FWHM = 0.45 mm h⁻¹) combines the two heads into a single estimate. Training uses GMI–CPR collocations (2014–2017, oversampled to balance the sparse CPR dataset) and GMI–DPR collocations. Validation uses OceanRAIN shipborne disdrometers (3436 matchups, March 2014–September 2018) and NOAA MRMS ground radar along the U.S. East Coast.
- **Key result:** vs. DPR-only GPROF-NN: 26% improvement in Critical Success Index for high-latitude precipitation; >50% reduction in underestimation of high-latitude and frozen precipitation. Instantaneous precision does not improve, attributed to large random errors in CloudSat 2C-Rain-Profile liquid precipitation reference.
- **Why it matters:** XPR is slated for integration into GPROF V08 (next operational GPM PMW product), directly improving the global high-latitude precipitation record and water-cycle estimates for regions where light/frozen precipitation dominates accumulation.
- **Caveats:** Improvement is in detection and climatological bias, not instantaneous accuracy; CloudSat reference for liquid rain has a known bimodal distribution artifact that propagates into CPR-head estimates. CloudSat coverage is daytime-only and ascending-pass limited during the validation period. Algorithm covers oceanic surfaces only.

## Tags
remote-sensing, hydrology, ML, climate
