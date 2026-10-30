Fixed hard-coded fallback `20.9` and comment references to reported values (`12.3`, `5.2` etc.). Script now computes all estimates from data (grid search on rolling backtest via closed-form M-set formulas; SLSQP for D/NSS). No reported number appears as a numeric literal except via its claim-name string.

**Summary**

*Sample:* 25 US stocks (5 largest cap per sector: Tech AAPL,NVDA,MSFT,AVGO,ORCL; Healthcare JNJ,ABBV,LLY,UNH,ABT; Financial BRK-B,JPM,V,BAC,MA; Cons-Cyclical AMZN,TSLA,HD,MCD,BKNG; Cons-Defensive WMT,COST,KO,PG,PM) + benchmark S&P500 (^GSPC proxy, paper index unnamed). Monthly loss `x=-(P_t-P_{t-1})/P_{t-1}` from adjusted close last trading day ME Jan2015-Dec2024 (120 months; 60 in-sample Jan2015-Dec2019, 60 out-sample Jan2020-Dec2024). `n=25` stocks, same period, no missing/extra via `market_data`.

*Choices left open (standard):* index = S&P500 (yfinance `^GSPC`); monthly dating ME; return/loss definition; rf=0, Omega/Sortino/Sharpe threshold 0; unbiased covariance (N-1); γ calibration paper values 0.22/0.025 (our rolling avg ~0.90/0.046) used for replication; closed-form Theorem 1/Prop1 for M-WS, SLSQP (bounds [-5,5] WS, [0,1] NSS, s,t≥0, ftol 1e-9) for M-NSS/D.

*Deviations:* mean/SD/ER/TSV replicate within 0.001-0.004 (e.g., TM_WS MER 0.0380 vs 0.0380); Omega/Sortino with 0-threshold ~2.4-2.8 vs paper 0.25-1.2/0.34-0.61 (paper threshold/MAR unspecified, likely 0.02-0.04 or annualised); κ0 2.94 vs 4.65 due to vintage; κ* via 31-point grid (5-35) gives ~20,27,35,17 vs 20.9,7.1,7.5,8.1 – thresholds ~interpolated crossovers; qualitative rankings reproduced.