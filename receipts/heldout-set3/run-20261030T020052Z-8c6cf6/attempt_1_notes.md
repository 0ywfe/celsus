Replication completed. Summary:

**Sample built:** Unbalanced country-year panel of 35 countries (20 eurozone: 11 founders 1999 + 9 late; 15 controls = 3 EU opt-out + 12 OECD) 1970-2023 (PWT 10.0 rgdpe/pop to 2019 + WDI NY.GDP.PCAP.KD.ZG 2020-2023). Growth = log-diff rgdpe/pop ×100, winsorized 1/99. Country+year TWFE event study (k=-10..20, ref -1, clustered SE) + RF proxy for CFFE (global FE residualization + RandomForest 200 trees depth 5 leaf 20 on pseudo-outcome y_res/D_res).

**Key choices the paper leaves open:** ticker not relevant (macro panel); trade openness proxied via PWT csh_x-csh_m, investment csh_i, human capital hc; initial features measured 1998 (1995 for heterogeneity median split); MEX/TUR added to reach 12 non-EU OECD (paper lists 10 names but claims 12); CFFE approximated via RF (causalfe not on pip); alternative estimators approximated by TWFE; compounding via ∏(1+τ/100)-1.

**Deviations / findings:**
- Paper claims negative euro effect -0.3 to -0.4pp; public PWT+WDI TWFE shows **positive** pre-trends (avg +1.49pp, F 2.58 p0.02) and post effects mixed (k0 +2.24pp, k5 -0.84pp), ATE -0.78pp (se 0.41). RF proxy also positive at k0 (+1.56). Data do not reproduce headline negative effect.
- Counts: N_total 1764 vs paper 2010, N_euro 954 vs 880, N_control 810 vs 1130, N_full treated 395 vs 506, N_late 120 vs 231 (late sum 23+17+16+16+15+13+10+9+1=120), placebo N 185/145 vs 92/68 (includes all treated cohorts). Early 275 matches, median split 6+6 vs paper 7+5 (ITA above median but paper classes as low).
- EU-only k0 +2.40 vs paper -0.703; cumulative compounding reflects mixed signs.
All numbers computed from data; no reported values hard-coded. `/work/replicate.py` fetches PWT/WDI and writes `/work/results.json` reproducibly.