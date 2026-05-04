# [Remote SAMsing: From Segment Anything to Segment Everything](https://arxiv.org/abs/2605.00256)

**Authors:** Osmar Luiz Ferreira de Carvalho, Osmar Abílio de Carvalho Júnior, Anesmar Olino de Albuquerque et al.
**Venue:** arXiv · **Date:** 2026-04-30 · **DOI:** n/a
**Score:** n/a
**Source:** full text

## TL;DR

Multi-pass black-masking pipeline wraps SAM2 to raise large-image segmentation coverage from 30–68% to 91–98% with no retraining, while a parameter-free best-match merge reconstructs cross-tile objects.

## Summary

- **Problem:** SAM2's Automatic Mask Generator (AMG) leaves 30–70% of large remote sensing scenes unsegmented at strict quality thresholds, and tiling fragments objects across boundaries — problems unaddressed by existing tools (SamGeo2 achieves only 6–27% coverage).
- **Method:** Remote SAMsing pipeline applied to seven scenes (5 cm–4.78 m GSD): (1) multi-pass adaptive segmentation — after each SAM2 pass, accepted-mask pixels are painted black to simplify the scene for the next pass; IoU and stability thresholds decay from 0.93 to 0.60 only when per-pass coverage gain stagnates; (2) contextual padding (50 px) per tile edge prevents edge gaps; (3) parameter-free best-match merge (Union-Find) unifies cross-tile fragments by highest-contact neighbor rather than all touching pairs. Evaluated on ISPRS Potsdam (5 cm), Brasília aerial (24 cm), and Agri-BR Planet MNF (4.78 m).
- **Key result:** Coverage rises to 91–98% across all seven scenes (vs. 30–68% single-pass at τ = 0.93). Adaptive threshold decay is the largest single contributor (+3–20 pp). Reducing tile size from 1,000 to 250 px raises Det@0.5 from 56% to 85% on BSB-1 (cars), outperforming SAM2's built-in crop_n_layers multi-scale (+6 pp) at comparable compute. Per-class Det@0.5: buildings 95%, cars 82–93%, pivot irrigation 100%. Boundary IoU (BIoU) 0.18–0.89 vs. SLIC/Felzenszwalb below 0.21. MNF false-color agricultural scene: 99.5% ASA with no retraining. 1.94-billion-pixel Potsdam mosaic: 97% coverage, 81.8% ASA, 60.7% Det@0.5 across 40,618 objects in ~20 h on one GPU.
- **Why it matters:** Enables production-scale, zero-shot, annotation-free OBIA segmentation of arbitrarily large RS images; segments serve as semantically meaningful superpixels (boundaries follow object contours, not spectral gradients) that can feed downstream classifiers. Tile size functions as an interpretable scale parameter — ~50 m per tile is a practical guideline across GSD levels. Pipeline is model-agnostic and can swap in future foundation models.
- **Caveats:** Performance on SAR, thermal, and hyperspectral imagery untested. Amorphous "stuff" classes (impervious surfaces, low vegetation) score low on Det@0.5 (37–43%) though ASA remains moderate (75–77%). Tile sizes below 1,000 px at 5 cm GSD cause merge chaining, degrading large-object BIoU. Processing is sequentially GPU-bound (~18 h for 1,024 tiles at T = 250); parallelization not yet implemented. Threshold decay range may benefit from scene-specific tuning.

## Tags
remote-sensing ML
