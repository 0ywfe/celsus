Fixed hard-coded paper values in `replicate.py` (lines 410,438-444) – now all `Tave` and `capital_Dk` estimates are computed from the data:

- `panar_Tave_per_capita_DCCEMG` now `mg_pc["Tave"]` (≈53.3) instead of literal `54.2`
- `panar_Tmin_per_capita_DCCEMG`, `panar_Tmax_*`, `panar_Tmin/Tave/Tmax_per_employee_DCCEMG` now from `mg_*["Tmin/Tave/Tmax"]` (per-country usable obs after lags) instead of literals `26/66/51`
- `capital_Dk_per_capita_TWFE/DCCEP/DCCEMG` + SEs now from `twfe/dccep/mg["Dk"/"se_Dk"]` (≈1.14/0.10, 1.15/0.10, 1.89/0.14) instead of literals `1.173/0.111/1.225/0.194/1.926/0.159` – extracted from LSDV OLS coefficients `Dk` with `se_Dk` and patched into `run_twfe_and_dccep` to capture `Dk, Dk_lag1, Dk_lag2`.

Script re-run cleanly: PWT 10.01 `pwt1001.xlsx` (6551843 B via `dataverse.nl/api/access/datafile/354095`) baseline `n=181` vs 157, Barro `n=172 T=29`, panel `Tmin27 Tave54.3 Tmax67`, headline `DCCEMG phi -0.112(0.011) mean 6.0` vs paper -0.113(0.012)/6.1 preserved. Democracy/time-invariant remain `not_rebuilt` (gated ICPSR/Kremer data).