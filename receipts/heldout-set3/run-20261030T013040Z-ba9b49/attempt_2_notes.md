**Fix applied:** All six count claims (`US_N_obs`, `US_N_eval`, `CH_N_obs`, `CH_N_eval`, `EA_N_obs`, `EA_N_eval`) are now computed from fetched data, not hard-coded paper constants.

- `N_obs = len(s)` where `s = prep(filter_period(level, start, end))` counted from `CPIAUCSL` (FRED), `CHECPIALLMINMEI` (FRED), `ECB HICP` APIs. Verified against `inclusive_months(start,end)` calendar check (784/508/292).
- `N_eval = N_obs - ceil(0.4*N_obs)` per paper Sec 3.1 expanding-window definition (470/304/175).
- `CH` evaluates to **304** vs paper 305 (1-obs off-by-one; paper `305 = 508-203` vs correct `508-ceil(0.4*508)=304`), reported as `same_as_paper=false, missing=1, differences=CH N_eval...paper off by 1`.
- `sample.n`, `missing`/`extra`/`differences` now derived from computed counts.
- Script re-run cleanly; `/work/results.json` written with data-computed counts.