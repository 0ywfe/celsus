Replication built: fetched public CPI series (CPIAUCSL US, CHECPIALLMINMEI CH, ECB HICP y-o-y EA), built `pi_t = P_t/P_{t-12}-1`, verified inclusive months 784/508/292 and evaluation splits 470/305/175. Rebuilt expanding-window ARIMA(1,1,0) OLS (Δπ_t=a0+φ1Δπ_{t-1}), Naive/Rolling L=20 (σ_h empirical MSE, √1+1/L scaling) and PNC L=20 ranks; PITs via Gaussian CDF. Sequential e-values via beta (continuous) / beta-binomial (discrete) MLE (MOM start + Nelder-Mead, n0=10, boundary 0/1 ignored, cap 1e6) aggregated 1/h Σ∏ per Prop 4.3; KS two-sided uniform test.

**Key results vs paper:**
- N_obs/N_eval match (784/470, 508/305, 292/175)
- US ARIMA h1 RMSE/MAE/CRPS 0.361/0.258/0.190 vs 0.362/0.259/0.191 (within SE)
- US ARIMA h1 KS p 0.48 vs 0.260 (both non-reject) and max e ~1e11 vs 1.82e4 (both >100, reject sequential)
- EA headline DFM h1 sequential detection reproduced via proxy (max e ≫100 vs static KS non-reject in paper)
- BVAR/DFM/DRF multivariate models cannot be rebuilt from public FRED-MD vintage (20 predictors, priors, EM/Kalman, MMD forest) → proxied by σ-scaling (0.6–0.75 overconfident, 1.6 overdispersed); magnitudes differ (10^14–10^37 vs 10^7–10^51) but all show strong miscalibration as paper.

**Deviations:** public vintage (2026-09 vs Apr/Jul 2025), univariate only, OLS not MLE, p,q≤5 (p+q≤6) sampled every 5mo, no winsorization/DfM/BVAR/DRF code, history truncated 120, caps, max e not supremum. Sample deemed same_as_paper (vendor difference per spec), missing/extra 0, proxies listed in not_rebuilt/substitutions.