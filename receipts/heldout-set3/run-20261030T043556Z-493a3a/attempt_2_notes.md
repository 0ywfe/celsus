Re-run complete. Fixed sample-count handling:

**Validator issue (line 491 old):** `train_obs = train_counts['SPY'] if ... else 1259` – fallback wrote paper count `1259` (and `791` in metric `n` fields). **Fix:** all `n`/`value` for `training_observations`/`testing_observations_per_instrument` and all metric `n`/`se` denominators are now **computed strictly from `market_data.get_prices` date filtering** (`len(data[T].loc[TRAIN_START:TRAIN_END])`, `len(df_test)`, `len(diff)`), with fallback `0`. No literal `1259`/`791` remains in `replicate.py` (verified via grep). No trimming/cutting to paper counts – sample is built from definition `2018-01-01→2022-12-31` and `2023-01-01→2026-02-28` windows.

**Current results (from data-driven counts):**
- Training per instrument: `1259` (2018-01-02→2022-12-30), Testing: `791` (2023-01-03→2026-02-27) – matches paper by coincidence, but now derived, not hard-coded.
- Full per-instrument: `2050`, sample `start=2018-01-02 end=2026-02-27 n=2050 same_as_paper=true`.
- Headline `qqq_vpmacd_total_pnl = 43119.46` (own VP-MACD with `N=20 σ=(H-L)/C` choice; paper `88324` divergent due to unstated `N`/`σ` window – noted in `substitutions`/`notes`).
- Baseline/MACD+λ VP differences documented; `t`/`NW`/`bootstrap` all computed from `diff = ret_new-ret_old` with data-driven `n_diff=790`.

Script re-executed successfully and rewrote `/work/results.json` cleanly.