# Hybrid weather prediction using spectral nudging toward machine-learning forecasts

**Authors:** I. Polichtchouk, M. C. A. Clare, M. Chantry et al.
**Venue:** arXiv (physics.ao-ph) · **Date:** 2026-04-24 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR

Spectrally nudging ECMWF IFS toward AIFS-Single ML forecasts at wavenumbers ≤20 gains up to 1.5 forecast days in the tropics and 12–18 h in the extra-tropics while preserving small-scale physics.

## Summary

- **Problem:** Pure ML weather models (e.g., AIFS-Single) excel at large-scale skill but lose small-scale variance; physics-based NWP retains mesoscale structure but lags ML at large scales. A practical hybrid that combines both without duplicating full-model complexity was lacking.
- **Method:** ECMWF IFS (cycle 49r1, TCo1279/9 km, 137 levels) is spectrally nudged toward a custom AIFS-Single-ML model (trained on all 137 model levels, O96/~120 km, MSE loss) during each time step. Nudging targets only virtual temperature (T_v) and vorticity (ζ) at total wavenumbers 0–20 (wavelengths >2000 km) below the lapse-rate tropopause, with a 12-hour relaxation timescale and an 8–12 h temporal ramp-up. Divergence is excluded to avoid semi-diurnal aliasing. Evaluation uses 644 daily 10-day forecasts (1 Jun 2024 – 28 Feb 2026), verified against ECMWF analysis, radiosondes, and SYNOP observations.
- **Key result:** Hybrid IFS (hy-IFS) improves tropical upper-air temperature and wind ACC by up to 33% and RMSE by up to 20% (850–250 hPa). Extra-tropical 500 hPa Z skill gain: ~12–18 h. Surface 10-m wind RMSE improves ~6–12 h equivalent; total precipitation (SEEPS) also improves. Forecast busts (z500 ACC <40% at day 6) cut roughly in half: Europe 6→3, North America 14→9, East Asia 12→5. Tropical cyclone track errors reduced ~50 km (~12 h lead-time equivalent); TC intensity largely unchanged and more physically consistent than pure AIFS-Single. Nudging adds only ~13% computational overhead.
- **Why it matters:** Demonstrates a practical, low-cost pathway to operationally blend ML large-scale guidance into a full-physics NWP model, retaining mesoscale structure and physical consistency (e.g., realistic wind maxima for extratropical cyclones) while closing most of the gap with pure ML skill. The approach is complementary to ensemble hybridization and requires periodic retraining of the ML component (~10% skill sensitivity to training period).
- **Caveats:** AIFS-Single-ML retains a ~1-day advantage over hy-IFS in the tropics (scales <2000 km not constrained); surface thermodynamic variables (2-m T, precipitation) still favor AIFS-Single throughout most lead times, likely because ML predicts them directly from reanalysis. Sensitivity to ML training period (up to 10% impact) means retraining must track analysis system changes. Results are for deterministic (unperturbed) forecasts only; ensemble extension addressed separately.

## Tags
ML climate remote-sensing
