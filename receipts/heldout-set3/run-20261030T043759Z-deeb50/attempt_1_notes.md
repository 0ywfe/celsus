**Summary**

*Sample built:* `1997Q1-2019Q4` 4-lag VAR in `log CPI (FRED CPIAUCSL quarterly mean) + log GDPC1` – 88 usable observations after lags (92 quarters raw); post-2019 forecast `2020Q1-2024Q1` (17 quarters, `d=17`) year-ended inflation `p_t-p_{t-4}` forecast errors; illustrative `1988M1-2023M9` 12-lag monthly PCE VAR (429 obs, FRED `PCEPI+DPCERA3M086SBEA` aggregate) instead of 136 BEA UD categories.

*Choices paper leaves open:* quarterly CPI aggregation (mean vs last) – used quarterly mean of CPI level then log (standard); `PeriodIndex Q-DEC` alignment; no risk-free/market data needed.

*Deviations:* Public FRED vintage `2026-10-30` (revisions) vs GP24 private vintage; estimated by OLS point estimate (vs Bayesian Minnesota+soc prior with 10k posterior draws, 10θ/φ =100k). This gives `rho=0.219 (SE 0.10)` vs paper `0.23 [0.13,0.33]` and `FE@2022Q2=6.13pp` vs paper `7.7pp`, `supply IS [0.39,5.35]` vs paper `[0.2,7.3]` – still wide (6%-87% of FE), confirming uninformativeness. Euro-area HICP/GDP quarterly levels and 136 PCE category-price series need BEA/Eurostat vintages not on public FRED – declared in `not_rebuilt` (16 claims). Joint probabilities `0.5/0/0.99` and 55k-trivariate draws are outputs of prior-robust posterior simulation requiring full Minnesota-posterior MCMC – not resimulated.

*Headline:* `est_US_supply_set_high_2022Q2 = 5.35pp` (SE 0, n=17) at OLS estimate, spanning ~87% of the 6.13pp 2022Q2 forecast error – replicate of wide, largely uninformative identified set.