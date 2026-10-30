Replication complete. Script builds 72-country balanced panel 1993-2022 from WDI (fetched via api.worldbank.org with pagination), groups per paper Table 1, deflates inventories by implicit GDP deflator, obtains GDP trend via log-quadratic regression, constructs ratio ΔINV/Ytrend_{t-1}, extracts cyclical component via country-specific quadratic filter in levels, and computes per-capita log-differences for aggregates; correlations/relative volatilities/autocorrelations are median across countries per group (Appendix C), volatilities as SD of cyclical component.

Headline result `corr_inv_y_advanced_0_48` replicated as 0.51 (SE 0.05, n=696) vs 0.48 paper; other stylized facts similarly close (advanced median vol 0.72% vs 0.70%, high 1.18% vs 1.13%, middle 1.24% vs 1.22%, low 1.07% vs 1.09%; ratio EM/advanced 1.70 vs 1.7; Singapore 2.36% vs 2.28%, Botswana 3.49% vs 3.55%; autocorr 0.16/0.18/0.25/0.22 vs 0.13/0.17/0.24/0.24).

**Deviations/choices:**
- WDI vintage 2026-10-08 vs paper 2023 vintage; current vintage missing RUS private consumption constant 1993-1995 and exports/imports constant 2022 → imputed via current-price series deflated by GDP_C/GDP_K to preserve 72 balance (noted in `substitutions`).
- GDP trend t=0..29 (1993 base) equivalent to paper's t in years; lagged trend as exp(beta0+beta1*(t-1)+beta2*(t-1)^2).
- Group statistics as median country-level moments (paper Table 2); pooled correlations shown as comparison are lower.
- SEs as std(country estimates)/√n; n per claim as pooled obs (29×countries for correlations) or countries for volatilities.
- LP shocks/variance shares/unit-root tests not rebuilt (require Fed futures/Ludvigson instruments and panel cointegration code) – noted in `notes`.

Sample in `results.json` is 72 countries (24/14/24/10) covering 1993-2022; `same_as_paper:true` after imputation, vintage differences documented.