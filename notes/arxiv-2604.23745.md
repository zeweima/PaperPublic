# Bridging the Sensitivity Gap in Precipitation Estimates from Spaceborne Radars using Passive Microwave Observations

**Authors:** Simon Pfreundschuh, Christian D. Kummerow
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-26 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Fusing CloudSat and GPM-DPR reference data in a passive microwave neural retrieval cuts high-latitude precipitation underestimation >50% and improves detection skill 26%.

## Summary

- **Problem:** GPM Dual-Frequency Precipitation Radar (DPR) is insensitive to light (<0.1 mm/hr) and frozen precipitation, so passive microwave (PMW) algorithms trained on DPR inherit systematic underestimation at high latitudes; zonal means diverge up to 80% poleward of 40°.
- **Method:** GPROF-NN XPR — a U-Net encoder-decoder neural network (EfficientNet-V2-style MBConv blocks) trained simultaneously on GMI brightness temperatures collocated with (1) CloudSat CPR reference data for light/frozen precipitation and (2) GPM 2BCMB DPR data for moderate-to-heavy precipitation. A Gaussian-weighted fusion scheme (FWHM = 0.45 mm/hr) blends the two output heads into a single precipitation estimate. Validation uses OceanRAIN shipborne disdrometers (oceanic in situ) and NOAA MRMS ground radar (U.S. East Coast).
- **Key result:** Versus DPR-only GPROF V07: 26% improvement in critical success index for high-latitude detection; >50% reduction in underestimation of high-latitude and frozen precipitation. Instantaneous precision does not improve, attributed to random errors in CloudSat liquid-precipitation reference estimates.
- **Why it matters:** Algorithm is slated for GPROF V08 (next operational GPM PMW product), directly improving oceanic high-latitude precipitation climatology in IMERG and derived water-cycle analyses.
- **Caveats:** CloudSat CPR bimodal rain-rate distribution introduces irregularities in CPR-based output; improvement limited to bias correction of climatological means — instantaneous retrieval precision is unchanged. Oceanic-only; land surfaces not addressed.

## Tags
remote-sensing ML hydrology climate
