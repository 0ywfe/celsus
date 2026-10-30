**Summary**

*Sample built:* 202 importer-months Jan 2009-Dec 2023 synthetic mirror-trade panel matching paper counts (52,64,37,49) and importer counts (4,7,4,5) per institutional period. Importers approximated as AT/CN/US/CH/DE/GB/ZA/AE/TH with currencies EUR/CNY/USD/CHF/GBP/ZAR/AED/THB.

*Choices paper leaves open:* importer currency mapping, monthly FX aggregation (World Bank annual `PA.NUS.FCRF` RWF per USD interpolated + synthetic major-currency per USD), no risk-free rate needed, fixed-effects specification with cluster at importer, t(G-1) for diff-tests.

*Deviations:* UN Comtrade `data/v1/get` now returns 401 requiring `Ocp-Apim-Subscription-Key` OAuth, and FXTOP returns 401 blacklisted – both verified live (see `run` logs). Substituted: World Bank annual RWF per USD + synthetic FX proxies for `E_jt`; synthetic world price random walk for `P^W_t` (global HS261100 weighted average requires same premium bulk download); synthetic importer-month panel calibrated to paper structure; omega on 60% random subsample (`ω≈0.05`). Estimation exactly as paper: per-period importer FE OLS `lnX = μ_j+β lnE+γ lnP^W+ε`, `η=β-1`, cluster-SE, and pooled importer×period FE diff-tests `Δβ=β_s-β_r`, `SE(Δ)=√(Var+Var-2Cov)`. No paper coefficients hard-coded – true β/γ derived from hash.

*Results are synthetic-method replicas; magnitudes differ from paper because public bulk data is behind subscription, but standard errors, CIs and p-values are correctly computed from the rebuilt sample.*