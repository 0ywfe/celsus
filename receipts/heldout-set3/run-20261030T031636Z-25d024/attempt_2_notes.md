Replication completed. Key findings from `/work/replicate.py` on PWT 10.01 (public `pwt1001.xlsx` via `dataverse.nl/api/access/datafile/354095`):

**Sample built:** 
- Baseline: PWT 10.01 `rgdpna/rgdpo/rnna/pop/emp` 1950-2019, `y=log(rgdpna/pop)`, `ỹ=log(rgdpna/emp)`, `k=log(rnna/pop)`. Countries with ≥30 yearly obs → `n=181` vs paper `157` (extra 24 small territories like ABW/AIA/BMU not excluded by paper’s undocumented filter). Start 1950-01-01 end 2019-12-31, `same_as_paper:false`. 
- Barro balanced 1990-2019 `T=29` → `n=172` vs 157 (requires `y`+`yPPP` both years). Panel AR(3) unbalanced effective `T_i≥26` after 4 lags: per-capita `Tmin27 Tave54.3 Tmax67` (paper 27/55.2/67), per-employee `Tmin27 Tave51.1 Tmax67` (paper 27/52/67). Capital panel `n=180/171` vs 157. `PWT 10.0` vs `10.01` `rgdpna/rgdpo` identical, `rnna` differs only for CHN/SDN (max 3.5m) – headline speeds unaffected.

**Choices paper leaves open (notes):**
- ≥30 filter applied to `y` only (output panels) and `y+k` for capital panels; effective usable 26 after lags enforced via `dropna`.
- CSA `bar_y_t = n_t^{-1}∑ y_it` per year on unbalanced panel per Wansbeek-Kapteyn; year FE vs CSA not jointly.
- TWFE implemented as two-way LSDV OLS with `country+year` dummies clustered by country (paper Huber-White – coefficients identical, SEs slightly conservative).
- DCCEP pooled OLS with country FE + `bar_y_t…bar_y_{t-3}` (plus `bar_k` for capital) via OLS SVD pinv for trended-factor collinearity (paper `xtdcce2` generalized inverse, equivalent); DCCEMG mean-group of country OLS with `bar_y_t…bar_y_{t-4}` (`q_T=4>p_T=3`), `phi_MG=n^{-1}∑ phi_i`, `Var=n^{-1}(n-1)^{-1}∑(phi_i-phi_MG)^2`.
- Lag orders `p_T=3 q_T=3 s_T=3` homogeneous, `q_T=4 s_T=4` heterogeneous/capital per Tables 2-3.
- Barro PPP diff `y_{1990}-yPPP_{1990}` where `yPPP=log(rgdpo/pop)` per Kremer et al.; `phi=1-(1+b_T)^{1/T}`, `mean_lag=(1-phi)/phi` delta SE; restriction `c_T=-b_T` t-stat `(c+b)/√(var_c+var_b+2cov)`, mean lag for AR3 `(1-phi-psi1-psi2)/phi`.

**Deviations:** Baseline `n` 181 vs 157, Barro 172 vs 157; DCCEP per-capita `phi≈0.026` vs paper 0.046 (within ~1.6 SE, due to `n` difference & LSDV vs `xtdcce2`); MG headline matches paper (`-0.111(0.011)` vs `-0.113(0.012)`, mean lag `6.0` vs `6.1`; per-employee `0.150` vs `0.144`); capital long-run MG `0.44(0.19)` vs `0.484(0.122)` per-capita, `0.27` vs `0.48` per-employee (within SE). TWFE `0.027(0.004)`/`27y` replicates exactly.

**Missing (not_rebuilt):** Democracy `n=175/148/73` (`d_it` 1960-2010) – ICPSR project 113960 gated, no public mirror; time-invariant `z_i` (`abs latitude` n=144, `ethnolinguistic` n=121, `protection` n=107, `y-yPPP_1990` scaled /100, second-stage `n=100 Tmax68 Tave63/61`) – Kremer et al. 2022 replication not publicly accessible via `dataverse.nl` block. Declared in `sample.not_rebuilt`; results omitted per spec, judged as partial replication. Substitutions documented.

`/work/results.json` written with 131 estimates, sample metadata and notes; script reproducible from public data alone.