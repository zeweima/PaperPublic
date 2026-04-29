# Synthetic Seismograms from Particle–Bed Interactions and Turbulent River Flow: Modeling and Comparison with Observations

**Authors:** Sara Nicoletti, Giacomo Belli, Omar Morandi et al.
**Venue:** arXiv (physics.flu-dyn) · **Date:** 2026-04-20 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR

A grain-scale DEM model coupled to Rayleigh-wave forward seismics discriminates bedload from turbulence contributions in river seismic noise, validated against a Tuscan Apennines flood event.

## Summary

- **Problem:** River seismometers record both sediment-impact and turbulent-flow signals, but disentangling their spectral contributions lacks a physically rigorous, particle-resolved framework — existing approaches rely on prescribed impact statistics rather than simulated grain trajectories.
- **Method:** 2-D physics-based model over a rough inclined bed: spherical grains transported under gravity, hydrodynamic drag (Schiller–Naumann), soft-sphere DEM collisions, and Langevin-type stochastic near-bed forcing (σ = 10⁻⁸ Ns¹/²). Water forcing combines Kolmogorov-scaling broadband turbulence (f ⁻⁵/³ PSD, 30–90 Hz) with narrow-band vortex-shedding tones (Strouhal St ≈ 0.2). Particle–bed contacts classified dynamically as impact (restitution e = 0.45) or rolling (reduced impulse α = 0.3); each event shaped by a Ricker wavelet with contact-time frequency f₀ = 1/tₒ. Forces propagated to a virtual receiver via analytical Rayleigh-wave Green's function (Tsai 2011) to produce synthetic ground-velocity PSD. Grain-size distribution: lognormal, mode D₀ = 5 cm, σ_log = 0.9 (D₅₀ ≈ 11 cm). Validated against seismometers at two sections of a mountain torrent during a flood.
- **Key result:** Synthetic seismograms reproduce the observed frequency bands from the Tuscan Apennines flood event; size-selective, intermittent sediment transport generates distinct high-frequency spectral signatures separable from lower-frequency turbulent/vortex-shedding contributions. Rolling contacts produce lower characteristic frequencies than impacts, consistent with a clear spectral separation between solid and liquid phase contributions.
- **Why it matters:** Provides a physically self-consistent bridge between grain-scale transport dynamics and seismic monitoring, enabling quantitative inference of bedload flux and grain-size distribution from field seismograms without in-stream instrumentation — important for ungauged or hazardous high-flow conditions.
- **Caveats:** 2-D model geometry; prescribed power-law velocity profile rather than resolved turbulence; bed roughness treated as random Gaussian perturbations (σ_z = 1 mm); single-torrent validation; rolling-contact timescale separation enforced artificially (factor-of-10 duration scaling); model not yet coupled to a full hydraulic solver.

## Tags
geomorphology hydrology remote-sensing
