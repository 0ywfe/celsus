Fixed sample period and `not_rebuilt` per review, re-ran `/work/replicate.py`:

* **Period corrected:** Searched paper window `2015-01-01` to `2022-12-31` (per `period_end` spec). Public `fastquant/data/merged_stock_data.zip` actually covers `2010-01-04` to `2021-12-15` (max date in zip), so `2022-01-01` to `2022-12-31` (≈252 trading days, 4 quarterly GDP quarters) missing. `sample.start=2015-01-01, end=2022-12-31, same_as_paper=false, missing=0, extra=0` with `differences` stating 2022 missing due cache, out-of-sample truncated `2021Q1-2021Q4` vs paper `2021Q1-2022Q4`. Verified via `df_raw.index.max()` logged.
* **Invalid not_rebuilt removed:** Deleted `count_parameters_not_stated_T_GDP` (no claim name; paper prints it as “not stated”). Kept only exact claim names:
  * `estimate_loading_beta_i_sigma_i_one_factor_table` (144 values, authors’ Kalman MLE)
  * `estimate_loading_beta1i_beta2i_sigma_i_two_factor_table` (216 values)
  Proxy loadings under `substitutions`, not `results`.
* **Log compliance:** `market_data` PSEi attempts (`PSEI.PS/^PSEI/^PSE`, `AC.PS` etc) logged as `MarketDataUnavailable` in `market_data_requests.json`; yfinance `^PSE` fallback logged in `market_data_log.json`; stooq JS proof-of-work documented as blocked.

**Verification:** `python /work/replicate.py` → `Wrote 46 results end 2022-12-31 actual 2021-12-15`, `sample 2015-01-01 2022-12-31 False`, `not_rebuilt keys 2`.

This is the **fixed version**.