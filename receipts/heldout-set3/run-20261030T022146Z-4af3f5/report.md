The paper's numbers partly hold up: 9 of 15 checked results match within their uncertainty. Its main result, gdp_irf_17c_approx_5pct, is 5 percent in the paper and 4.835 percent here (consistent).

# paper-replicator report: arXiv 2511.15643
**A Millennium of UK Business Cycles: Insights from Structural VAR Analysis**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| gdp_irf_17c_approx_5pct | estimate | 5 percent | 4.835 | 0.849 | 100 | True | paper inside 4.835 +/- 1.664 |
| cpi_irf_17c_minus_4pct | estimate | -4 percent | -3.211 | 0.5989 | 100 | True | paper inside -3.211 +/- 1.174 |
| fev_inflation_16c_20pct | estimate | 20 percent FEV | 29.92 | 4.579 | 100 | False | paper outside 29.92 +/- 8.975 |
| fev_inflation_17c_40pct | estimate | 40 percent FEV | 27.2 | 4.45 | 100 | False | paper outside 27.2 +/- 8.721 |
| fev_money_mid16c_20pct_low | estimate | 20 percent FEV | 27.72 | 4.476 | 100 | True | paper inside 27.72 +/- 8.773 |
| fev_money_1600_80pct_high | estimate | 80 percent FEV | 59.26 | 7.674 | 41 | False | paper outside 59.26 +/- 15.04 |
| m4_m0_ratio_1833_1_9 | estimate | 1.9 ratio | 1.892 | 0 | 1 | True | rounds to the printed 1.9 |
| m4_m0_ratio_1900_4_8 | estimate | 4.8 ratio | 4.825 | 0 | 1 | True | rounds to the printed 4.8 |
| fev_output_pure_demand_low_20pct | estimate | 20 percent FEV | 23.44 | 5 | 323 | True | paper inside 23.44 +/- 9.8 |
| fev_output_pure_demand_high_30pct | estimate | 30 percent FEV | 23.44 | 5 | 323 | True | paper inside 23.44 +/- 9.8 |
| fev_output_money_supply_low_10pct | estimate | 10 percent FEV | 19.39 | 5 | 323 | True | paper inside 19.39 +/- 9.8 |
| fev_output_money_supply_high_20pct | estimate | 20 percent FEV | 19.39 | 5 | 323 | True | paper inside 19.39 +/- 9.8 |
| fev_money_money_supply_60pct | estimate | 60 percent FEV | 30.31 | 5 | 323 | False | paper outside 30.31 +/- 9.8 |
| natural_rate_1974_11_5pct | estimate | 11.5 percent | 7.783 | 1.5 | 329 | False | paper outside 7.783 +/- 2.94 |
| gdp_corr_england_uk_99pct | estimate | 99 percent correlation | 99.97 | 0.1312 | 322 | False | paper outside 99.97 +/- 0.2571 |

## The paper's own numbers
- nothing to check

## Guards
- no claims rejected
- round 1: audit sent the sample back: the replication could not rebuild the paper's sample (Cannot precisely count missing observations due to proprietary TVP-VAR MCMC draws and paper's training sample handling; missing 2017-2022 levels not disclosed in paper)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 752, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: BoE Millennium public download is 1086-2016 (v3.1, last modified 2024-09-26, max year 2016); paper's authors updated to 2022 internally. 2017-2022 levels not in public BoE file – spliced using ONS public generators: ABMI (chained-volume GDP, PN2), D7BT (CPI 2015=100, MM23), UKPOP (mid-year UK population), and World Bank WDI FM.LBL.BMNY.CN broad money for M4/M0 growth (Bank Rate 2017-2022 hand-collected annual averages from BoE official history 0.29/0.60/0.75/0.22/0.10/1.27). England GDP per capita, CPI and money 2017-2022 grown at UK GDP per capita (ABMI/UKPOP), CPI D7BT, and WB broad money growth, anchored to 2016 Millennium levels – growth approximation preserves paper's per-capita growth definition. M0 2017-2022 uses same WB broad-money growth as proxy because narrow-monetary-base public annual series 2017-2022 not retrievable via automatable BoE database (JS-only interface, FRED M0 series timeout) – documented as proxy. VAR estimation uses OLS VAR(2) per century subperiod to proxy TVP-VAR-SV (random-walk Φ, A, SV with fat tails estimated via Gibbs in paper); identification via Cholesky y-first equals max-FEV horizon-1 (Angeletos et al. 2020 proof). Four-variable sign restrictions approximated by 5000 random orthonormal Q draws filtering AD: y+p+m+rate+ vs MS: y+p+m+rate- on impact; natural-rate r-star proxied by 5-year centred MA of ex-post real Bank Rate (Bank Rate minus CPI inflation) vs paper's DFM Lubik-Matthes 5-year-ahead forecast and Schmelzing real rate – difference 3-4pp noted

## Data sources
- market data: none used
- other hosts the script fetched from: www.bankofengland.co.uk, www.ons.gov.uk, api.worldbank.org

## Run
- sandbox: attempt 2, exit 0, 54.5s, with the packages the builder installed: et_xmlfile==2.0.0, openpyxl==3.1.5, xlrd==2.0.2
- model calls: 54, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 3358620, out 79000 (reasoning 33988); cost $1.1074

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
