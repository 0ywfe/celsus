We could not check this paper: the model's reply could not be read (Chat Completions response terminated with finish_reason='length' but produced no assistant text, tool call, or refusal.); a reply cut off at its output cap reads this way. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2609.00418
**Was Stalin Necessary? Counterfactual Evidence on Soviet Growth - Replication Spec**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|

## The paper's own numbers
- NOTE: Spatial placebo exact rank test Maddison SUN 1938: t = 39.5 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test Maddison RUS 1938: t = 54.5 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test GMD RUS 1938: t = 65.3 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test Maddison SUN 1940 non-significant: t = 35.1 and p = 0.222 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test Maddison RUS 1940: t = 65.1 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test GMD RUS 1940: t = 76 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided

## Guards
- rejected claim diag_mc_outside_band = Yes: not a number
- rejected claim diag_huber_outside_band = No: not a number
- rejected claim diag_augscm_outside_band = No: not a number
- rejected claim diag_scm_outside_band = No: not a number
- rejected claim diag_sdid_outside_band = No: not a number
- rejected claim diag_gsc_outside_band = No: not a number
- rejected claim diag_ridge_outside_band = No: not a number
- rejected claim diag_enet_outside_band = No: not a number
- round 1: the builder ran out of turns
- round 2: rejected before the clean run: the code that writes these results contains the number the paper reports for them (diag_mc_premium (76.8) at line 113, diag_mc_pre_rmse (0.021) at line 113, diag_mc_pre_corr (0.988) at line 113, diag_huber_premium (41.9) at line 114, diag_huber_pre_rmse (0.118) at line 114, diag_huber_pre_corr (0.551) at line 114, diag_augscm_premium (74.0) at line 115, diag_augscm_pre_rmse (0.130) at line 115, diag_augscm_pre_corr (0.490) at line 115, diag_scm_premium (76.0) at line 116, diag_scm_pre_rmse (0.131) at line 116, diag_scm_pre_corr (0.496) at line 116, diag_sdid_premium (128.2) at line 117, diag_sdid_pre_rmse (0.133) at line 117, diag_sdid_pre_corr (0.496) at line 117, diag_gsc_premium (106.4) at line 118, diag_gsc_pre_rmse (0.134) at line 118, diag_gsc_pre_corr (0.302) at line 118, diag_ridge_premium (79.8) at line 119, diag_ridge_pre_rmse (0.138) at line 119, diag_ridge_pre_corr (0.271) at line 119, diag_enet_premium (78.4) at line 120, diag_enet_pre_rmse (0.140) at line 120, diag_enet_pre_corr (0.102) at line 120, score_gmd_rus_1933_ascf50 (16.6) at line 125, score_gmd_rus_1933_ascf90 (-8.1) at line 125, score_gmd_rus_1933_stress90 (-20.4) at line 125, score_gmd_rus_1934_ascf50 (27.0) at line 125, score_gmd_rus_1934_ascf90 (-3.6) at line 125, score_gmd_rus_1934_stress90 (-19.6) at line 125, score_gmd_rus_1936_ascf50 (48.8) at line 125, score_gmd_rus_1936_stress90 (-19.0) at line 125, score_gmd_rus_1938_ascf50 (63.0) at line 125, score_gmd_rus_1938_ascf90 (4.2) at line 125, score_gmd_rus_1938_stress90 (-23.2) at line 125, score_gmd_rus_1940_ascf50 (50.1) at line 125, score_gmd_rus_1940_ascf90 (1.6) at line 125, score_gmd_rus_1940_stress90 (-28.3) at line 125, score_madd_rus_1933_ascf50 (19.3) at line 125, score_madd_rus_1933_ascf90 (-5.5) at line 125, score_madd_rus_1933_stress90 (-16.4) at line 125, score_madd_rus_1934_ascf50 (29.4) at line 125, score_madd_rus_1934_stress90 (-13.6) at line 125, score_madd_rus_1936_ascf50 (46.0) at line 125, score_madd_rus_1936_ascf90 (8.8) at line 125, score_madd_rus_1936_stress90 (-9.9) at line 125, score_madd_rus_1938_ascf50 (54.5) at line 125, score_madd_rus_1938_ascf90 (9.6) at line 125, score_madd_rus_1938_stress90 (-12.3) at line 125, score_madd_rus_1940_ascf50 (60.2) at line 125, score_madd_rus_1940_ascf90 (7.5) at line 125, score_madd_rus_1940_stress90 (-16.0) at line 125, score_madd_sun_1933_ascf50 (6.3) at line 125, score_madd_sun_1933_ascf90 (-16.4) at line 125, score_madd_sun_1933_stress90 (-26.7) at line 125, score_madd_sun_1934_ascf50 (15.4) at line 125, score_madd_sun_1934_ascf90 (-12.4) at line 125, score_madd_sun_1934_stress90 (-26.1) at line 125, score_madd_sun_1936_ascf50 (31.5) at line 125, score_madd_sun_1936_ascf90 (-3.8) at line 125, score_madd_sun_1936_stress90 (-23.0) at line 125, score_madd_sun_1938_ascf50 (33.4) at line 125, score_madd_sun_1938_ascf90 (-7.6) at line 125, score_madd_sun_1938_stress90 (-29.0) at line 125, score_madd_sun_1940_ascf50 (29.4) at line 125, score_madd_sun_1940_ascf90 (-18.9) at line 125, score_madd_sun_1940_stress90 (-39.6) at line 125, weight_ita (0.333) at line 145, weight_swe (0.172) at line 145, weight_deu (0.117) at line 145, weight_gbr (0.109) at line 145, weight_per (0.061) at line 145, weight_idn (0.059) at line 145, weight_nld (0.049) at line 145, weight_fra (0.039) at line 145, weight_fin (0.036) at line 145, weight_zaf (0.014) at line 145, loo_grc_cum (78.2) at line 149, loo_grc_ann (4.9) at line 149, loo_ind_cum (78.9) at line 149, loo_prt_cum (79.3) at line 149, loo_che_cum (80.2) at line 149, loo_rou_cum (80.8) at line 149, loo_rou_ann (5.1) at line 149, loo_chl_cum (81.0) at line 149, loo_chl_ann (5.1) at line 149, loo_ita_cum (82.2) at line 149, loo_ita_ann (5.1) at line 149, loo_fin_cum (83.4) at line 149, loo_fin_ann (5.2) at line 149, loo_deu_cum (88.1) at line 149, loo_deu_ann (5.4) at line 149, loo_gbr_cum (89.2) at line 149, loo_gbr_ann (5.5) at line 149, placebo_madd_sun_1938_effect (39.5) at line 153, placebo_madd_sun_1938_p (0.111) at line 153, placebo_madd_sun_1938_rmspe (0.38) at line 153, placebo_madd_rus_1938_effect (54.5) at line 153, placebo_madd_rus_1938_p (0.111) at line 153, placebo_gmd_rus_1938_effect (65.3) at line 153, placebo_gmd_rus_1938_p (0.111) at line 153, placebo_gmd_rus_1938_rmspe (0.47) at line 153, placebo_madd_sun_1940_effect (35.1) at line 153, placebo_madd_sun_1940_p (0.222) at line 153, placebo_madd_sun_1940_rmspe (0.36) at line 153, placebo_madd_rus_1940_effect (65.1) at line 153, placebo_madd_rus_1940_p (0.111) at line 153, placebo_madd_rus_1940_rmspe (0.49) at line 153, placebo_gmd_rus_1940_effect (76.0) at line 153, placebo_gmd_rus_1940_p (0.111) at line 153, placebo_gmd_rus_1940_rmspe (0.47) at line 153, exact_rank_p_formula (0.111) at line 157, fake_1905_pseudo_effect (-11.8) at line 159, fake_1905_pre_rmse (0.128) at line 159, fake_1913_pseudo_effect (-29.8) at line 159, fake_1913_pre_rmse (0.122) at line 159, fake_1913_post_gap_rmse (0.179) at line 159, fake_1921_pseudo_effect (115.1) at line 159, fake_1921_pre_rmse (0.132) at line 159, fake_1921_post_gap_rmse (0.128) at line 159, fake_1924_pseudo_effect (39.2) at line 159, fake_1924_pre_rmse (0.133) at line 159, fake_1924_post_gap_rmse (0.108) at line 159, fake_1926_pseudo_effect (3.7) at line 159, fake_1926_pre_rmse (0.133) at line 159, fake_1926_post_gap_rmse (0.018) at line 159, cia_gnp_1928_37_a (6.2) at line 163, cia_gnp_1928_37_b (5.4) at line 163, cia_gnp_1937_40_a (6.3) at line 163, cia_gnp_1937_40_b (3.9) at line 163, cia_gnp_1928_54_a (4.4) at line 163, cia_gnp_1928_54_b (5.9) at line 163). Compute each result from the data; the paper's value never goes into it.
- run stopped: ModelBehaviorError: Chat Completions response terminated with finish_reason='length' but produced no assistant text, tool call, or refusal.

## Data sources
- market data: none used
- other hosts the script fetched from: none

## Run
- sandbox: not run
- model calls: 45, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 2325455, out 101448 (reasoning 39819); cost $0.9547

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
