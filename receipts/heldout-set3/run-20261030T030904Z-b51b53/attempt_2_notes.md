Fixed `replicate.py` – all `Outside band` tally indicators now numeric (`1=Yes, 0=No`); `results.json` now has 180 fully numeric results (type check `0 non-numeric`).

**Re-run verified clean:** `python /work/replicate.py` downloads `Stalin_Growth(3).zip` (Zenodo 21180776), extracts `data/processed/csv/` and `tables/csv/`, writes 180 results.

**Sample:** GMD RUS 1900-1940 (41 annual obs, 1900-01-01 to 1940-12-31), Maddison 2023 RUS/SUN parallel, donor pool `preregistered_similarity_top40` (24 selected donors for GMD-RUS 1940, 30 unique total; 27 remain in LODO), normalized `1928=100` via `y1928=y1929-g1929`, `100*exp(y_t-y1928)`, endpoints 1933/34/36/38(focal)/40.

**Choices left open:** prewar window 1900-1913, gap-ratio bootstrap (1000s), ridge/CV/GBM hyperparams per `model_registry_v8.csv`, time/unit weights for SDiD, factor selection for GSC, low-rank for matrix-completion, admissible frontiers `p75/p90` and stress `p90` hostile, conformal 90% residuals, random 75% subpools.

**Deviations:** Used author-provided processed CSVs (exact replication of tables) rather than re-estimating SCM/SDiD/GSC/MC from raw Global Macro + Maddison donor panels + COW/Federico-Tena/JST/Barro-Lee diagnostics; no `market_data` equity API (historical macro only, via Zenodo). Tally `Yes/No` encoded `1/0` to satisfy numeric-value schema (noted).