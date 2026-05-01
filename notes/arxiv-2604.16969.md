# [Hyperspectral Unmixing Hierarchies](https://arxiv.org/abs/2604.16969)

**Authors:** Joseph L. Garrett, P. S. Vishnu, Pauliina Salmi et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-18 · **DOI:** n/a
**Score:** n/a
**Source:** full text

## TL;DR

Binary Linear Unmixing Tactile Hierarchies (BLUTHs) impose a hierarchical abundance sum constraint on NMF-based unmixing, matching or exceeding state-of-the-art methods on lab scenes while enabling unsupervised ocean color partitioning from PACE and HYPSO.

## Summary

- **Problem:** Hyperspectral unmixing is hampered by spectral variability across endmembers, ambiguity in the correct number of endmembers, and degrading endmember clarity as more are added — three interrelated problems that flat unmixing architectures cannot simultaneously address.
- **Method:** BLUTH networks impose a Hierarchical Abundance Sum Constraint (HASC) on Deep Nonneg Matrix Factorization, organizing endmembers into a binary tree where each parent abundance equals the sum of its children. A Sparsity Modulation Unmixing Growth (SMUG) algorithm grows BLUTH topology without a pre-specified endmember count, using four alternating sparsity modalities (Equilibrate, Sparsify, Shake, De-sparsify). Evaluated on 8 standard remote sensing scenes (Samson, Jasper Ridge, APEX, Urban, Washington DC), 2 lab Realistic Miniature Mixing Scenes with ground-truth proportions, and ocean color imagery from PACE (200×150 px) and HYPSO-2 (200×200 px) cubesats.
- **Key result:** On lab scenes with true ground truth, BLUTH-AA records the top-2 IoU for every endmember across scenes; on remote sensing scenes BLUTH shows comparable spectral angles to AA-based SoTA (EDAA, SAPPA) with slightly lower IoU. MiSiCNet missed 26 endmembers total across scenes vs. BLUTH-AA's 4. BLUTH storage footprint for a 6-endmember urban scene is 10.4 kB vs. 2.3 MB for conventional methods. On Skagerrak ocean imagery, BLUTHs cleanly separate land, cloud, coccolithophore bloom (blue), and CDOM river runoff (yellow) at the first hierarchy split.
- **Why it matters:** Provides unsupervised, parameter-lean unmixing suited to the data volumes of new hyperspectral satellite constellations (PACE, HYPSO, EMIT, EnMAP); hierarchical structure naturally encodes varying levels of spectral contrast and mitigates spectral variability without manual endmember count selection.
- **Caveats:** Training time is significant (~3 h for Samson, >1 day for Washington DC at ~10⁵ pixels); SMUG requires p copies of the network per split, so compute scales with endmember count. Performance gap between lab and remote sensing scenes suggests sensitivity to sparse abundance failure modes and dark pixels (shadow misassignment). Scalability to full PACE/HYPSO databases (>10⁹ px) remains undemonstrated.

## Tags
remote-sensing ML
