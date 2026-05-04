# [Efficient Spatio-Temporal Vegetation Pixel Classification with Vision Transformers](https://arxiv.org/abs/2605.00296)

**Authors:** Alan Gomes, Anderson Gonçalves, Samuel Felipe dos Santos et al.
**Venue:** arXiv · **Date:** 2026-04-30 · **DOI:** n/a
**Score:** 5/10
**Source:** full text

## TL;DR

Vision Transformers match or beat a multi-temporal CNN for plant species pixel classification while cutting FLOPs 14× and holding parameter count constant regardless of time-series length.

## Summary

- **Problem:** Pixel-wise plant species identification from high-resolution UAV and tower image time series in the Brazilian Cerrado requires models that jointly capture spatial texture and phenological (temporal) signals; the state-of-the-art multi-branch CNN (Nogueira et al. 2019) scales linearly in parameters with time-series length and demands large 25×25 spatial windows, making deployment on edge devices impractical.
- **Method:** Standard ViT encoder (6 layers, 8 heads, D=256) adapted for 1D spatio-temporal token sequences; comprehensive 7-dimension ablation (normalization, spectral band order, boundary handling, context window shape/size, temporal vs. spatial tokenization, positional encoding, feature aggregation). Evaluated on two Brazilian Cerrado datasets: Serra do Cipó (13-timestamp UAV RGB orthomosaics, 4 species, ~147k annotated pixels) and Itirapina (36-timestamp phenocam RGB, 6 species, ~60k annotated pixels). Optimal config: raw data, natural band order (RGBRGB), square context window (13×13 for UAV, 25×25 for tower), temporal tokens, black-padding boundaries, learnable positional encoding, CLS token aggregation.
- **Key result:** Serra do Cipó — ViT 96.79% balanced accuracy vs. CNN 98.90% (−2.11%), with 1.72M vs. 3.84M parameters (−55%) and 0.05 vs. 0.73 GFLOPs (14× reduction). Itirapina — ViT 61.51% vs. CNN 53.62% (+7.89%), with 2.07M vs. 7.95M parameters and 0.16 vs. 2.07 GFLOPs (12× reduction). ViT showed markedly better recall on rare/subtle species (e.g., *A. tomentosum* 59.33% vs. 0%, *P. torta* 88.31% vs. 0% for CNN on Itirapina). Radiometric normalization consistently degraded performance; temporal tokens outperformed spatial tokens; positional encoding mattered (−1.15% BAcc without it on Itirapina).
- **Why it matters:** Demonstrates that ViTs with small spatial context windows are viable for near-surface and UAV phenological monitoring; constant parameter count with time-series length directly enables deployment on resource-constrained edge devices and longer monitoring campaigns without architectural redesign. Better minority-class sensitivity is relevant for biodiversity monitoring in species-rich tropical biomes.
- **Caveats:** RGB only — no multispectral or hyperspectral data; tested exclusively in Brazilian Cerrado (two sites, one biome); 1D tokenization only (no 3D spatio-temporal patches); Itirapina absolute accuracy remains low (61.5%), suggesting the task is genuinely hard and gains may not transfer to other ecosystems; small number of annotated image instances despite large pixel counts.

## Tags

remote-sensing ML agroecosystem climate
