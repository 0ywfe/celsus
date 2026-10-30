Fixed: removed 4 tautological claims that violated Rule 1 (constant 1.0/R2=1.0). `/work/replicate.py` now **computes** every reported value from Edge PSE data or omits it with justification:

* `estimate_corr_Ft_PC1_one_factor` (paper 0.9975) → **not reported** – would be tautological `F_t:=PC1=1.0`; requires DFM MLE (Kalman, `n=1,p=3,q=5`). Listed in `not_rebuilt`.
* `estimate_corr_F1t_PC1_two_factor` (0.8982) & `estimate_corr_F2t_PC2_two_factor` (0.8229) → **not reported** – tautological `F1t:=PC1`/`F2t:=PC2`. Require DFM `n=2,p=2,q=5`.
* `estimate_R2_Ft_on_F1tF2t` (0.998) → **not reported** – hard-coded `R2=1.0` previously; requires OLS of DFM `F_t` on `F1t,F2t`.

Remaining `results` (16) are all computed: 66 stocks retained after 1% filter (paper 72 – 6 missing from 2026 PSE directory), PSEi proxied by equal-weighted mean return (stooq CF-blocked, yfinance 1-bar), PCA proxy `PC1/PC2` (`F_t≈PC1` paper 0.9975 justification), correlations/Pearson SE `√((1-r²)/(n-2))`, CAPM beta vs loading. Verified via `grep` zero matches for the 4 names in results; all now in `not_rebuilt` with Rule-1 rationale. Re-ran `python /work/replicate.py` – writes `/work/results.json` cleanly.