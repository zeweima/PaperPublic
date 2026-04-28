# From Noisy Historical Maps to Time-Series Oil Palm Mapping Without Annotation in Malaysia and Indonesia (2020-2024)

**Authors:** Nuttaset Kuapanich, Juepeng Zheng, Bohan Shi et al.
**Venue:** arXiv (cs.CV) · **Date:** 2026-04-26 · **DOI:** n/a
**Score:** 9/10<sup> top pick</sup>
**Source:** full text

## TL;DR
A U-Net with DMI loss maps 10 m oil palm plantations across Indonesia and Malaysia 2020–2024 using only coarse 100 m historical labels as supervision, revealing a coverage peak in 2022 and ongoing encroachment into wetlands.

## Summary
- **Problem:** No 10 m resolution oil palm plantation maps exist for Indonesia/Malaysia from 2020 onward; existing products top out at 30–100 m and stop at 2019, hindering deforestation and sustainability monitoring.
- **Method:** U-Net trained on 59,136 balanced 512×512 Sentinel-2 patches (10 spectral bands, 10 m) using 100 m Annual Oil Palm Area Dataset (AOPD, 2016) as noisy labels. Determinant-based Mutual Information (DMI) loss handles the 10× resolution mismatch without explicit noise modeling. Bayesian inference fuses U-Net outputs with AOPD priors in post-processing. Final wall-to-wall maps at 278,789×148,117 pixels cover 2020, 2022, and 2024. Benchmarked against MMSFormer, DeepLabv3+, UNetFormer, HRNet, and PyramidMamba.
- **Key result:** Overall accuracy of 70.64% (2020), 63.53% (2022), and 60.06% (2024) against 2,058 manually verified Google Earth points. U-Net with DMI outperformed all five competing architectures on boundary precision; transformers (UNetFormer, PyramidMamba) over-smoothed boundaries, replicating coarse-label artifacts. Oil palm coverage peaked in 2022 then declined in 2024. Land-cover transition analysis identified increasing oil palm encroachment into flooded vegetation (wetlands), particularly in Kalimantan.
- **Why it matters:** First publicly available 10 m annual oil palm time-series for Indonesia and Malaysia (2020–2024) produced without new manual annotation; directly usable for RSPO compliance monitoring, carbon emission accounting, and deforestation tracking. Dataset released on Zenodo (doi.org/10.5281/zenodo.17768444).
- **Caveats:** Overall accuracy declines over time (70.6% → 60.1%), likely compounding errors as phenological and land-use conditions diverge from the 2016 training labels. Validation set (2,058 points) is modest for a continental-scale binary map. Training labels are from 2016 AOPD, not co-temporal with 2020–2024 imagery, introducing temporal label mismatch. U-Net beats all competitors, but absolute accuracies remain modest for high-stakes monitoring applications.

## Tags
remote-sensing ML agroecosystem biogeochem
