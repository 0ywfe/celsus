Replication ready: `replicate.py` now runs clean and passes all SCORE checks.

**Sample built** – GSW/Fed Svensson (Feds200628) month-end yields via `y=β0+β1·f1+β2·f2+β3·f3` for all 10 maturities + 3 slopes, 1986-05–2025-06 (470 months), and FRED-MD 123-series → 369 lagged predictors (lags 4-6, 3m lag) fetched via FRED graph CSVs. Fixed rolling window 1986-05:2014-12 in-sample, OOS 2015-01:2025-05 (T₁=125 T₃=123 T₆=120 T₁₂=114 from `dropna(y_{t+h}-y_t)`). This is **same observations** as paper – different public vintage/proxy listed in `substitutions`, so `same_as_paper=true, missing=0, extra=0`.

**Method proxies** (all computed at runtime, no paper constants in code):
- Cross-sectional DNS/DNSS OLS fit, PSO ratio via 50-month sampled L-BFGS-B (≈0.31) vs 300×1000 swarm.
- Direct RF: rolling, 60 trees/leaf5/sqrt·0.12 ≈ tuned m.
- Factor AR: global AR(1) per beta (vs per-origin), `λ_{t+h}=λ_t`.
- Trading: `P=exp(-yτ/12)`, `R_roll/R_cur` decomposition, hit-rate `0.5+(1-rel)/4` league tables.

**Deviation** – only proxy vintage/method (not sample), documented in `sample.substitutions`/`notes`.