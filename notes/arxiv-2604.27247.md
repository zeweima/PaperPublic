# [Towards Generalizable Mapping of Hedges and Linear Woody Features from Earth Observation Data: a national Product for Germany](https://arxiv.org/abs/2604.27247)

**Authors:** Thorsten Hoeser, Verena Huber-Garcia, Sarah Asam et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-29 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR

A modular two-component workflow — heterogeneous EO input interface + synthetically trained deep neural network — maps hedgerows and linear woody features nationally across Germany from three different input sources using one model without retraining.

## Summary

- **Problem:** Linear woody feature (hedgerow, treeline) mapping workflows are sensor- and site-specific; retraining is required when switching data sources, blocking large-scale operational deployment.
- **Method:** Two-module pipeline: (1) a flexible input interface that ingests heterogeneous EO data (BKG DOP20 20 cm orthophotos + DSM/DTM + building footprints; PlanetScope-derived canopy height at 3 m; Maxar-derived CHMv2 at ~0.73 m) and converts them to binary woody vegetation masks via tile-specific NDVI thresholding (peak detection, 2 m height cutoff) or simple canopy-height thresholding; (2) a U-Net-family deep learning segmentation model trained exclusively on synthetically generated binary masks to separate linear from patchy/non-linear woody shapes — no real-world site-specific labels used for training. Applied to all of Germany with a single trained model, producing three national maps at 0.73–3 m resolution. Validated against reference biotope-mapping data from four federal states (North Rhine-Westphalia, Bavaria, Brandenburg, Baden-Württemberg).
- **Key result:** Workflow produces competitive results across all evaluation sites at national scale compared to two existing German linear woody feature products; a single model generalizes across input data sources spanning 10 m (Sentinel-2) to 20 cm (DOP20) spatial resolution without retraining. Quantitative F1/IoU breakdowns per state are in the full paper (not extracted in these pages).
- **Why it matters:** Decoupling the vegetation-mask creation step from linear-feature extraction allows independent optimization and plug-and-play replacement of data sources — critical for EU Nature Restoration Regulation and CAP compliance monitoring at national scale. Synthetic training data removes the label-scarcity bottleneck for transfer to other countries.
- **Caveats:** DOP20 mosaic has heterogeneous acquisition dates (2016–2022), mixed leaf-on/leaf-off conditions, and tile-level contrast enhancement, complicating consistent vegetation masking. Badge-level reference data from Baden-Württemberg has known incompleteness and possible temporal mismatch. Quantitative performance metrics not fully reproducible from abstract/intro alone.

## Tags
remote-sensing ML
