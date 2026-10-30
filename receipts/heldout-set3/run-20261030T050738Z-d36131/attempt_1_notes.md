Replicated what public data allows; Kalshi signal is headline and is **not retrievable**.

**Sample built:** Daily closes Jan 2023–Mar 2026 for BTC-USD, ETH-USD, SOL-USD, ADA-USD, AVAX-USD, LINK-USD via `market_data.get_prices` (Yahoo; cache→live) + VIX `^VIX`/`^GSPC`/`DX-Y.NYB`; 5-day forward realized vol `RVol=sq252*sd(r_{t+1:t+5})` per Eq2; intersecting to trading days (VIX∩SP500∩DXY) gives 813 trading days (30% dropped). Calendar span 2023-01-01–2026-03-31 =1186 days. Descriptives recomputed (BTC mean 0.348 vs paper 0.634, SD/min/max reported with SE=sd/√N).

**Paper leaves open → choice made:**
- Kalshi `Δ_vw` Eq1 volume-weighted probability change: endpoint `https://api.elections.kalshi.com/trade-api/v2/markets` + `/markets/candlesticks?period_interval=1440&start_ts&end_ts` probed live; current API retains only settled markets created ≥2025-08 (KXFED 22, KXCPI 29, KXRECSSNBER 0 vs paper 469/384/569); thus no historical signal rebuild.
- Crypto vendor midnight-UTC CoinGecko → substituted `BTC-USD` etc Yahoo closes (verified coverage, noted caveat).
- Alignment Kalshi 16:00ET vs crypto 19:00ET same date +1-day lag → enforced via trading-index filtering.
- VIX/DXY/SP500 controls → `^VIX`/`^GSPC`/`DX-Y.NYB`; Fed Funds futures/10Y/DVOL not in public cache → omitted.
- HAC 5 lags, block-bootstrap, CW OOS, BH FDR, orthogonalization → would follow paper exactly if signal existed.

**Deviations:**
- Calendar N 1186 vs 1183 (+3 inclusive counting); descriptive N 1181 vs 1178 (+3 windowing); trading N 813 matches implied 30% drop but paper labels merged as 1183 calendar.
- Mean RVol mismatch factor ≈1.83 (BTC 0.348 vs 0.634; ETH 0.466 vs 0.742 etc) despite Eq2 with ddof=1/sqrt252 – unexplained data vintage/definition difference; reported transparently.
- All Kalshi-dependent claims (usable obs 193-569, N=318/264, t=3.63/−3.39, MSFE 0.979/0.959, OOS Noos 144-269, R², CW p, BH adj p, ortho R² 2.3%/7.5%, bootstrap, lead-lag, baseline, GARCH/log/21d, vol-managed 7%/16%) → `not_rebuilt` with API evidence; `same_as_paper:false`.