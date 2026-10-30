Replication now builds sample strictly from definition and reports observed counts:

**Fix applied:** `obs_*` values are no longer set to paper's `N*Tbar = 672/392/672/280`. Instead `obs_advanced_ps=696`, `obs_high_em_ps=406`, `obs_middle_em_ps=696`, `obs_low_em_ps=290` are computed as `sum(~isnan(inv_cyc))` per group after WDI fetch and quadratic-filter transformations. `Tbar_panel_estimation` likewise reported as observed median usable years =29 (actual usable per country 29, vs paper's 28) with calculation `median(usable_counts)`. All `N_*` values derived via `len()` on Table 1 lists (`72/24/14/24/10`) and exclusion lists (`6/4`), not hard-coded to match paper at expense of trimming.

**Verification:** No `672/392/280` literals control sample slicing; grep shows only explanatory note text. Script still fetches WDI `1993-2022` via `api.worldbank.org`, constructs deflated `ΔINV/Ytrend_{t-1}` cyclical component, and computes median volatilities/correlations relative to paper within <0.02.

Re-run clean: `python /work/replicate.py` produces `/work/results.json` with corrected observed counts.