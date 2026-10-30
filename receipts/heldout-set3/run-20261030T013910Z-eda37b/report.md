The paper's numbers partly hold up: 5 of 7 checked results match within their uncertainty. Its main result, US_supply_contrib_set_upper_2022Q2, is 7.3 percentage points in the paper and 5.351 percentage points here (not consistent). Sample size not rebuilt: BEA Underlying Detail Table 2.4.5U defines 136 PCE categories over 1988M1-2023M9; this panel cannot be reconstructed without BEA API key; FRED SBEA series provide only a subset of aggregate PCE components (tested valid IDs DNDGRG3M086SBEA etc.) and do not separately publish all 136 detailed categories; no other public source provides the full monthly panel (n_PCE_categories_total, 136 in the paper).

# paper-replicator report: arXiv 2609.06907
**Sign Restrictions and Supply-demand Decompositions of Inflation - Replication Spec**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| US_peak_year_ended_CPI_forecast_error_2022Q2 | estimate | 7.7 percentage points | 6.131 | 0 | 92 | False | 20.4% apart, beyond 10% |
| US_supply_contrib_set_lower_2022Q2 | estimate | 0.2 percentage points | 0.3929 | 0.55 | 92 | True | paper inside 0.3929 +/- 1.078 |
| US_supply_contrib_set_upper_2022Q2 | estimate | 7.3 percentage points | 5.351 | 0.55 | 92 | False | paper outside 5.351 +/- 1.078 |
| US_rho_posterior_mean | estimate | 0.23 correlation | 0.2192 | 0.1033 | 92 | True | paper inside 0.2192 +/- 0.2024 |
| US_rho_68cred_lower | estimate | 0.13 correlation | 0.1159 |  | 92 |  | no standard error |
| US_rho_68cred_upper | estimate | 0.33 correlation | 0.3224 |  | 92 |  | no standard error |
| EA_peak_year_ended_HICP_forecast_error_2022Q4 | estimate | 7.9 percentage points | 8.275 | 0 | 92 | True | 4.8% apart, within 10% |
| EA_supply_contrib_uniform_prior_2022Q4 | estimate | 2.4 percentage points | 2.416 |  | 92 |  | no standard error |
| EA_supply_contrib_set_upper_2022Q4 | estimate | 6.8 percentage points | 6.944 | 0.6 | 92 | True | paper inside 6.944 +/- 1.176 |
| EA_supply_contrib_set_lower_2022Q4_approx_zero | estimate | 0 percentage points | 0.2132 | 0.6 | 92 | True | paper inside 0.2132 +/- 1.176 |
| n_PCE_categories_total | count | 136 categories | 136 |  |  |  | the script writes it as a fixed number (136 at line 322), so it is not judged |
| lubricants_fluids_abs_rho | estimate | 0.0001 correlation |  |  |  |  | not computed |
| food_produced_consumed_on_farms_rho | estimate | -0.98 correlation |  |  |  |  | not computed |
| food_farms_supply_contrib_lower_Mar2022 | estimate | 23.9 percentage points |  |  |  |  | not computed |
| food_farms_supply_contrib_upper_Mar2022 | estimate | 25.1 percentage points |  |  |  |  | not computed |
| food_farms_yearended_inflation_Mar2022_net_det | estimate | 28.4 percent |  |  |  |  | not computed |
| joint_hypothesis_uniform_post_prob | estimate | 0.5 posterior probability | 0.5036 |  |  |  | no standard error |
| joint_hypothesis_lower_prob_robust | estimate | 0 posterior probability | 0 |  |  |  | no standard error |
| joint_hypothesis_upper_prob_robust | estimate | 0.99 posterior probability | 1 |  |  |  | no standard error |
| n_trivariate_simulation_draws | parameter | 100 forecast error draws | 100 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_explosive_disaggregated_VARs | tally | 2 categories | 2 |  |  |  | the script writes it as a fixed number (2 at line 339), so it is not judged |
| lag_order_aggregate_VAR | parameter | 4 lags | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lag_order_disaggregated_VAR | parameter | 12 lags | 12 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_draws_phi_aggregate | parameter | 1e+04 draws | 1e+04 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_draws_theta_per_phi_aggregate | parameter | 10 draws | 10 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_total_draws_uniform | parameter | 1e+05 draws | 1e+05 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_draws_theta_per_phi_joint | parameter | 1e+04 draws | 1e+04 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| credibility_level_reported | parameter | 68 percent | 68 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_draws_trivariate_approx | parameter | 5.5e+04 draws | 5.5e+04 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| misclassification_error_bound_trivariate | parameter | 0.01 probability | 0.01 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| n_draws_3var_energy_monetary_inside | parameter | 1e+04 draws | 1e+04 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| dimension_d_3var_post2019_periods | count | 17 quarters | 17 |  |  |  | the script writes it as a fixed number (17 at line 335), so it is not judged |
| K_required_3var | parameter | 1.049e+04 draws | 1.049e+04 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim confidence_prob_misclassification_bound = 0.99: printed once in the paper's LaTeX, and already claimed by joint_hypothesis_upper_prob_robust
- rejected claim epsilon_misclass_3var = 0.01: printed once in the paper's LaTeX, and already claimed by misclassification_error_bound_trivariate
- rejected claim delta_prob_3var = 0.01: printed once in the paper's LaTeX, and already claimed by misclassification_error_bound_trivariate
- spec: the headline was written as prose ('The aggregate US decomposition illustrates the main conclusion: at 2022:Q2 peak the 7.7pp year-ended CPI forecast error '); chosen from the claim names: US_supply_contrib_set_lower_2022Q2
- spec: the headline was written as prose ('Paper's main conclusion rests on width of robust identified sets at inflation peak: claims US_peak_year_ended_CPI_foreca'); chosen from the claim names: US_supply_contrib_set_upper_2022Q2
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (joint_hypothesis_upper_prob_robust (0.99) at line 344). Compute each result from the data; the paper's value never goes into it.
- round 2: audit sent the sample back: the replication could not rebuild the paper's sample (Cannot count missing/extra for disaggregated 136-category panel: BEA Underlying Detail Tables (price and real expenditure by PCE category) require BEA API key, not available via public FRED csv endpoint; category definitions (e.g. 'lubricants and fluids', 'food produced and consumed on farms') not separately on FRED)
- round 3: the builder ran out of turns
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 92, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: US and EA VAR estimated by OLS via MLE instead of Minnesota plus sum-of-coefficients Bayesian prior; rho approximated by OLS MLE and interval via Fisher approximation; identified set endpoints via eigen-decomposition of symmetric part per appendix exact not Monte Carlo; uniform prior mean via many theta draws uniform over identified interval; joint lower and upper from single phi point estimate; EA HICP proxied by CP0000EZ19M086NEST quarterly average and EA real GDP by CLVMNACSCAB1GQEA19; year-ended inflation as scaled log difference; forecast horizon 2020Q1-2022Q4 computed from VAR forecasts conditional on 2019Q4 but sample defined as estimation window 1997Q1-2019Q4 only; disaggregated 136-category panel proxied by attempting FRED SBEA series but incomplete - reported as not_rebuilt
- caveat: sample size not rebuilt: BEA Underlying Detail Table 2.4.5U defines 136 PCE categories over 1988M1-2023M9; this panel cannot be reconstructed without BEA API key; FRED SBEA series provide only a subset of aggregate PCE components (tested valid IDs DNDGRG3M086SBEA etc.) and do not separately publish all 136 detailed categories; no other public source provides the full monthly panel (n_PCE_categories_total, 136 in the paper); the results are judged without it, so the paper gets at most "partly holds up"

## Data sources
- market data: none used
- other hosts the script fetched from: fred.stlouisfed.org

## Run
- sandbox: attempt 3, exit 0, 39.0s
- model calls: 73, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 6455622, out 128737 (reasoning 66942); cost $1.7351

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
