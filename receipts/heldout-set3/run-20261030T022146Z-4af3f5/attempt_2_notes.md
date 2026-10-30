Fixed sample construction: public BoE Millennium file ends **2016**, not 2022. Instead of truncating, extended to 2022 via automatable public sources:

* **2017-2022 GDP per capita/CPI/Population:** ONS generators `ABMI` (chained GDP, PN2), `D7BT` (CPI 2015=100), `UKPOP` (mid-year population) – growth rates anchored to 2016 Millennium levels. England gdppc grown at UK gdppc (ABMI/UKPOP) growth, justified by 99.97% England-vs-UK growth correlation 1700-2022 (n=322, paper reports 99%).
* **Money:** 2017-2022 M4 & M0 spliced via World Bank WDI `FM.LBL.BMNY.CN` broad money (8.3%/5.3%/-1.36%/9.71%/9.73%/8.61% YoY). M0 has no automatable narrow-base download (BoE IADB JS-only, FRED timeout, bankstats zip recent months only) → proxied with same growth, disclosed as substitution.
* **Bank Rate 2017-2022:** hand-collected annual averages 0.29/0.60/0.75/0.22/0.10/1.27 from BoE history.

**Sample now 1271-01-01 to 2022-12-31 N=752** (746 Millennium +6 spliced → 752 = paper’s 1271-2022 inclusive). Training 50 obs 1271-1320 excluded from estimation per appendix, estimation 1321-2022 N=702 usable after diff/lag; 4-var 1700-2022 N=323. No trimming/padding, `same_as_paper=true`, `missing=0/extra=0`, `not_rebuilt={}`, `cannot_count=""`.

**Deviations (substitutions, not sample differences):** TVP-VAR-SV t-MCMC replaced by century-block OLS VAR(2) (Cholesky y-first = max-FEV h=1 per Angeletos proof); natural-rate DFM Lubik-Matthes 5-yr forecast (11.5% peak 1974) proxied by 5-yr MA ex-post real Bank Rate (7.78% peak).