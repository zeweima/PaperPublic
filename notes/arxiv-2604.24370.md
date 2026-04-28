# Multispectral airborne laser scanning dataset for tree species classification: MS-ALS-SPECIES

**Authors:** Matti Hyyppä, Klaara Salolahti, Eric Hyyppä et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-27 · **DOI:** n/a
**Score:** 8/10<sup> top pick</sup>
**Source:** full text

## TL;DR
First open multispectral ALS dataset for individual-tree species classification: 6326 trees across 9 species in Southern Finland, with field-validated labels and dual-system point clouds.

## Summary
- **Problem:** No publicly available multispectral ALS dataset with high-quality field-validated reference data existed for individual-tree species classification, bottlenecking deep learning development for this task.
- **Method:** Two multispectral ALS systems flown over a peri-urban site in Espoonlahti, Finland: helicopter-borne HeliALS (3 wavelengths: 1550, 905, 532 nm; ~1300 pts/m²) and fixed-wing Optech Titan (1550, 1064, 532 nm; ~35 pts/m²). Field reference labels collected via a custom crowdsourcing app using GNSS positioning for 6326 segment-level individual-tree point clouds covering 9 species (pine, spruce, birch, maple, aspen, rowan, oak, linden, alder). Classification benchmarked using point transformer (FGI-PointTransformer-DL-3D) and random forest on clean vs. all segments, and as a function of tree height.
- **Key result:** Point transformer on HeliALS data reached 92.0% overall accuracy across 9 species (vs. 83.7% on the sparser Optech Titan data). Restricting evaluation to clean segments (single tree, non-"smaller tree next to larger tree") improved accuracy by 2–3 percentage points without changing classifier rankings. Point transformer outperformed machine learning classifiers particularly for small trees and minority species.
- **Why it matters:** Releases the first open multispectral lidar benchmark for tree species classification at individual-tree level, enabling systematic deep learning development; crowdsourcing app methodology provides a scalable template for large-scale ground-truth collection in forest inventories.
- **Caveats:** Single peri-urban study site in Southern Finland limits geographic generalizability; species distribution is imbalanced (pine and birch dominate); HeliALS data collected without gyro-stabilized platform under turbulent conditions, introducing some strip gaps; green-channel ALS data susceptible to atmospheric noise.

## Tags
remote-sensing, ML, geology
