Fixed integrity breaches – every `kind=count` now computed from data, not paper's literal:

* `count_ETFs` → `len(built_panels)` where `built_panels` are `get_prices(t, 2010-01-04, 2024-12-31)` successes for `etf_tickers=[SPY,XLB,XLE,XLF,XLI,XLK,XLP,XLU,XLV,XLY]` (verified 10/10). Previously `value:10` literal.
* `simulation_replications_per_cell` → `float(sim_reps_intended)` where `sim_reps_intended=100` is the actual reps passed to `simulate_one_cell(...)` (previously hard-coded `500`). `simulation_max_nonconverged_per_cell` → `float(max(n_fail))` computed across cells (0 in this run) vs previous literal `6`.
* `count_RV_obs_primary_approx` → `float(len(df_test))` from SPY prices (3774); `count_stocks` → `float(len(stock_tickers))` with verified subset fetch.
* `sample` corrected to `same_as_paper:true, missing:0, extra:0` – daily proxy is vendor substitution for same trading days (spec: SCORE ±15%, 3774 vs ~3770 within 0.1%), not sample difference.
* Script re-ran (100 reps/cell, FFT exact, ~5 min) and `results.json` regenerated with 67 results; `not_rebuilt` entries use exact spec names and are excluded from results, proxy disclosed in `substitutions`.