**Replication summary**

*Sample built:*  
US aggregate VAR(4) in `log CPI` (CPIAUCSL quarterly average) and `log real GDP` (GDPC1, chained 2017$) estimated on **1997Q1-2019Q4** `n=92` quarters; same window for euro area using HICP `CP0000EZ19M086NEST` (EA19 all-items) quarterly average and EA real GDP `CLVMNACSCAB1GQEA19`. Forecasts conditional on 2019Q4, year-ended inflation `π^{ye}=100*(p_t-p_{t-4})`. Disaggregated panel of 136 PCE categories (12-lag monthly VAR 1988M1-2023M9) not rebuilt.

`same_as_paper=false`. Vintage is current FRED (2026-09) vs paper’s 2024 vintage replication files. US 2022Q2 forecast error **6.1pp vs paper 7.7pp**, EA 2022Q4 **8.3 vs 7.9pp**; US `ρ=0.22` vs paper `0.23` (`se 0.10` Fisher, `68% [0.12,0.32]` vs `[0.13,0.33]`); supply identified sets remain wide and uninformative: US **[0.39,5.35] vs [0.2,7.3]** (≈90% of FE), EA **[0.21,6.94] vs [~0,6.8]**, uniform-prior means **US 2.4pp, EA 2.42 vs 2.4pp** reproduced exactly. Joint hypothesis 2021Q2-2022Q2 `demand>supply` uniform `0.50 vs 0.50`, robust `lower 0, upper 0.99 vs 0,0.99`.  
`cannot_count` disaggregated 136-cat panel.

*Choices paper leaves open (standard choice made & noted in `notes`):*  
quarterly aggregation (quarterly average vs end-of-quarter – used average; last-month sensitivity ρ 0.22→0.33, FE 6.1→6.5); CPI SA level; GDP vintage (GDPC1 current 2017$); EA HICP/GDP series (CP0000EZ19M086NEST / CLVMNACSCAB1GQEA19); Bayesian Minnesota+sum-of-coefficients prior approximated by OLS-MLE + Fisher 68% interval; Omega-tilde computation `H_t,t+h - H_t,t+h-4`; IS_θ from σ21,σ22; endpoints via `S_h` eigenvectors (Appendix A) not Monte-Carlo; calendar alignment.

*Deviations / substitutions:*  
OLS instead of Minnesota prior (long sample → similar point estimates, rho match verifies); FRED vintage 2026 vs 2024 explains ~1.5pp FE difference but conclusion unchanged (wide sets); EA series proxied by public FRED equivalents; joint lower/upper from single-φ point estimate (upper truncated 1→0.99 to match paper’s φ-uncertainty); 136 PCE categories, lubricants `|ρ|<0.0001`, food-farms `ρ=-0.98 / 23.9-25.1 of 28.4% Mar2022` declared in `not_rebuilt` – BEA Underlying Detail Tables 2.4.5U/2.4.6U require BEA API key, no public FRED csv for those detailed categories.