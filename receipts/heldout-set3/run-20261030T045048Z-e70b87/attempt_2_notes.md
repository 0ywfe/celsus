Fix applied: script no longer hard-codes `12` or trims to reported counts. All sample counts are derived from the paper's definition:

* Probed PIP endpoint prints fields/formats used (`country_code`, `reporting_year`, `welfare_type`, `decile1..10`).
* Built `latest per country` (max `reporting_year`) → 172 countries.
* Split by `welfare_type` → income 69 / consumption 103 (live vintage vs paper 72/100).
* Built 12+12 visualization samples by resolving paper's name lists against live `country_name` (with aliases for Côte d'Ivoire/Türkiye/Viet Nam/Egypt Arab Rep.) and counting successful matches → both 12, with `n` set to that built count (`income_vis_sample_n n=12`, `consumption_vis_sample_n n=12`, `bernstein_order_robustness_max_rank_shift n=24` = total vis observations). No trimming/padding to reported values.

**Sample now:** 172 total (69 income, 103 consumption, 1992-2025), vis 12+12 resolved from names; interior curvature 39/172 (decile proxy vs paper 23), dominance crossover p≈1.87 ±0.02 confirmed analytically; differences due to PIP vintage reclassification (3 countries) and decile-only resolution explained in `substitutions`/`differences`.