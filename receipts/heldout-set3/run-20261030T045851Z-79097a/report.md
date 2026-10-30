The paper's numbers partly hold up: 7 of 7 checked results match within their uncertainty. Its main result, score_gmd_rus_1938_ascf90, is 4.2% in the paper and 4.2% here (not judged: no standard error). Sample size not rebuilt: the script writes it as a fixed number (27 at line 267), not counted from the data (loo_donor_count, 27 in the paper).

# paper-replicator report: arXiv 2609.00418
**Was Stalin Necessary? Counterfactual Evidence on Soviet Growth**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| nep_prewar_trend_p05 | estimate | 0.006 annual log growth | 0.006 |  | 10000 |  | no standard error |
| nep_prewar_trend_median | estimate | 0.014 annual log growth | 0.014 |  | 10000 |  | no standard error |
| nep_prewar_trend_p95 | estimate | 0.021 annual log growth | 0.021 |  | 10000 |  | no standard error |
| recovery_gap_persistence_p05 | estimate | 0.747 AR1-style persistence | 0.747 |  | 10000 |  | no standard error |
| recovery_gap_persistence_median | estimate | 0.803 AR1-style persistence | 0.803 |  | 10000 |  | no standard error |
| recovery_gap_persistence_p95 | estimate | 0.86 AR1-style persistence | 0.86 |  | 10000 |  | no standard error |
| remaining_gap_1928_p05 | estimate | 0.123 log gap | 0.123 |  | 10000 |  | no standard error |
| remaining_gap_1928_median | estimate | 0.236 log gap | 0.236 |  | 10000 |  | no standard error |
| remaining_gap_1928_p95 | estimate | 0.35 log gap | 0.35 |  | 10000 |  | no standard error |
| nep_median_index_1940 | estimate | 146 index | 146 |  | 10000 |  | no standard error |
| nep_p10_index_1940 | estimate | 126 index | 126 |  | 10000 |  | no standard error |
| nep_p90_index_1940 | estimate | 171 index | 171 |  | 10000 |  | no standard error |
| observed_rus_index_1940 | estimate | 204 index | 204 | 0 | 1 | True | rounds to the printed 204 |
| diag_nuclear_premium | estimate | 76.8% | 76.8 |  | 28 |  | no standard error |
| diag_nuclear_pre_rmse | estimate | 0.021 log points | 0.021 |  | 28 |  | no standard error |
| diag_nuclear_pre_corr | estimate | 0.988 correlation | 0.988 |  | 28 |  | no standard error |
| diag_huber_premium | estimate | 41.9% | 41.9 |  | 28 |  | no standard error |
| diag_huber_pre_rmse | estimate | 0.118 log points | 0.118 |  | 28 |  | no standard error |
| diag_huber_pre_corr | estimate | 0.551 correlation | 0.551 |  | 28 |  | no standard error |
| diag_augscm_premium | estimate | 74% | 74 |  | 28 |  | no standard error |
| diag_augscm_pre_rmse | estimate | 0.13 log points | 0.13 |  | 28 |  | no standard error |
| diag_augscm_pre_corr | estimate | 0.49 correlation | 0.49 |  | 28 |  | no standard error |
| diag_scm_growth_premium | estimate | 76% | 76 |  | 28 |  | no standard error |
| diag_scm_growth_pre_rmse | estimate | 0.131 log points | 0.131 |  | 28 |  | no standard error |
| diag_scm_growth_pre_corr | estimate | 0.496 correlation | 0.496 |  | 28 |  | no standard error |
| diag_sdid_premium | estimate | 128.2% | 128.2 |  | 28 |  | no standard error |
| diag_sdid_pre_rmse | estimate | 0.133 log points | 0.133 |  | 28 |  | no standard error |
| diag_sdid_pre_corr | estimate | 0.496 correlation | 0.496 |  | 28 |  | no standard error |
| diag_gsc_premium | estimate | 106.4% | 106.4 |  | 28 |  | no standard error |
| diag_gsc_pre_rmse | estimate | 0.134 log points | 0.134 |  | 28 |  | no standard error |
| diag_gsc_pre_corr | estimate | 0.302 correlation | 0.302 |  | 28 |  | no standard error |
| diag_ridge_premium | estimate | 79.8% | 79.8 |  | 28 |  | no standard error |
| diag_ridge_pre_rmse | estimate | 0.138 log points | 0.138 |  | 28 |  | no standard error |
| diag_ridge_pre_corr | estimate | 0.271 correlation | 0.271 |  | 28 |  | no standard error |
| diag_enet_premium | estimate | 78.4% | 78.4 |  | 28 |  | no standard error |
| diag_enet_pre_rmse | estimate | 0.14 log points | 0.14 |  | 28 |  | no standard error |
| diag_enet_pre_corr | estimate | 0.102 correlation | 0.102 |  | 28 |  | no standard error |
| score_gmd_rus_1933_ascf50 | estimate | 16.6% | 16.6 |  | 28 |  | no standard error |
| score_gmd_rus_1933_ascf90 | estimate | -8.1% | -8.1 |  | 28 |  | no standard error |
| score_gmd_rus_1933_stress90 | estimate | -20.4% | -20.4 |  | 28 |  | no standard error |
| score_gmd_rus_1934_ascf50 | estimate | 27% | 27 |  | 28 |  | no standard error |
| score_gmd_rus_1934_ascf90 | estimate | -3.6% | -3.6 |  | 28 |  | no standard error |
| score_gmd_rus_1934_stress90 | estimate | -19.6% | -19.6 |  | 28 |  | no standard error |
| score_gmd_rus_1936_ascf50 | estimate | 48.8% | 48.8 |  | 28 |  | no standard error |
| score_gmd_rus_1936_ascf90 | estimate | 5% | 5 |  | 28 |  | no standard error |
| score_gmd_rus_1936_stress90 | estimate | -19% | -19 |  | 28 |  | no standard error |
| score_gmd_rus_1938_ascf50 | estimate | 63% | 63 |  | 28 |  | no standard error |
| score_gmd_rus_1938_ascf90 | estimate | 4.2% | 4.2 |  | 28 |  | no standard error |
| score_gmd_rus_1938_stress90 | estimate | -23.2% | -23.2 |  | 28 |  | no standard error |
| score_gmd_rus_1940_ascf50 | estimate | 50.1% | 50.1 |  | 28 |  | no standard error |
| score_gmd_rus_1940_ascf90 | estimate | 1.6% | 1.6 |  | 28 |  | no standard error |
| score_gmd_rus_1940_stress90 | estimate | -28.3% | -28.3 |  | 28 |  | no standard error |
| score_mad_rus_1933_ascf50 | estimate | 19.3% | 19.3 |  | 28 |  | no standard error |
| score_mad_rus_1933_ascf90 | estimate | -5.5% | -5.5 |  | 28 |  | no standard error |
| score_mad_rus_1933_stress90 | estimate | -16.4% | -16.4 |  | 28 |  | no standard error |
| score_mad_rus_1934_ascf50 | estimate | 29.4% | 29.4 |  | 28 |  | no standard error |
| score_mad_rus_1934_ascf90 | estimate | 0.9% | 0.9 |  | 28 |  | no standard error |
| score_mad_rus_1934_stress90 | estimate | -13.6% | -13.6 |  | 28 |  | no standard error |
| score_mad_rus_1936_ascf50 | estimate | 46% | 46 |  | 28 |  | no standard error |
| score_mad_rus_1936_ascf90 | estimate | 8.8% | 8.8 |  | 28 |  | no standard error |
| score_mad_rus_1936_stress90 | estimate | -9.9% | -9.9 |  | 28 |  | no standard error |
| score_mad_rus_1938_ascf50 | estimate | 54.5% | 54.5 |  | 28 |  | no standard error |
| score_mad_rus_1938_ascf90 | estimate | 9.6% | 9.6 |  | 28 |  | no standard error |
| score_mad_rus_1938_stress90 | estimate | -12.3% | -12.3 |  | 28 |  | no standard error |
| score_mad_rus_1940_ascf50 | estimate | 60.2% | 60.2 |  | 28 |  | no standard error |
| score_mad_rus_1940_ascf90 | estimate | 7.5% | 7.5 |  | 28 |  | no standard error |
| score_mad_rus_1940_stress90 | estimate | -16% | -16 |  | 28 |  | no standard error |
| score_mad_sun_1933_ascf50 | estimate | 6.3% | 6.3 |  | 28 |  | no standard error |
| score_mad_sun_1933_ascf90 | estimate | -16.4% | -16.4 |  | 28 |  | no standard error |
| score_mad_sun_1933_stress90 | estimate | -26.7% | -26.7 |  | 28 |  | no standard error |
| score_mad_sun_1934_ascf50 | estimate | 15.4% | 15.4 |  | 28 |  | no standard error |
| score_mad_sun_1934_ascf90 | estimate | -12.4% | -12.4 |  | 28 |  | no standard error |
| score_mad_sun_1934_stress90 | estimate | -26.1% | -26.1 |  | 28 |  | no standard error |
| score_mad_sun_1936_ascf50 | estimate | 31.5% | 31.5 |  | 28 |  | no standard error |
| score_mad_sun_1936_ascf90 | estimate | -3.8% | -3.8 |  | 28 |  | no standard error |
| score_mad_sun_1936_stress90 | estimate | -23% | -23 |  | 28 |  | no standard error |
| score_mad_sun_1938_ascf50 | estimate | 33.4% | 33.4 |  | 28 |  | no standard error |
| score_mad_sun_1938_ascf90 | estimate | -7.6% | -7.6 |  | 28 |  | no standard error |
| score_mad_sun_1938_stress90 | estimate | -29% | -29 |  | 28 |  | no standard error |
| score_mad_sun_1940_ascf50 | estimate | 29.4% | 29.4 |  | 28 |  | no standard error |
| score_mad_sun_1940_ascf90 | estimate | -18.9% | -18.9 |  | 28 |  | no standard error |
| score_mad_sun_1940_stress90 | estimate | -39.6% | -39.6 |  | 28 |  | no standard error |
| donor_weight_ITA | estimate | 0.333 weight | 0.333 |  | 28 |  | no standard error |
| donor_weight_SWE | estimate | 0.172 weight | 0.172 |  | 28 |  | no standard error |
| donor_weight_DEU | estimate | 0.117 weight | 0.117 |  | 28 |  | no standard error |
| donor_weight_GBR | estimate | 0.109 weight | 0.109 |  | 28 |  | no standard error |
| donor_weight_PER | estimate | 0.061 weight | 0.061 |  | 28 |  | no standard error |
| donor_weight_IDN | estimate | 0.059 weight | 0.059 |  | 28 |  | no standard error |
| donor_weight_NLD | estimate | 0.049 weight | 0.049 |  | 28 |  | no standard error |
| donor_weight_FRA | estimate | 0.039 weight | 0.039 |  | 28 |  | no standard error |
| donor_weight_FIN | estimate | 0.036 weight | 0.036 |  | 28 |  | no standard error |
| donor_weight_ZAF | estimate | 0.014 weight | 0.014 |  | 28 |  | no standard error |
| loo_GRC_cum_premium | estimate | 78.2% | 78.2 |  | 27 |  | no standard error |
| loo_GRC_annual_premium | estimate | 4.9% | 4.9 |  | 27 |  | no standard error |
| loo_IND_cum_premium | estimate | 78.9% | 78.9 |  | 27 |  | no standard error |
| loo_IND_annual_premium | estimate | 5% | 5 |  | 27 |  | no standard error |
| loo_PRT_cum_premium | estimate | 79.3% | 79.3 |  | 27 |  | no standard error |
| loo_PRT_annual_premium | estimate | 5% | 5 |  | 27 |  | no standard error |
| loo_CHE_cum_premium | estimate | 80.2% | 80.2 |  | 27 |  | no standard error |
| loo_CHE_annual_premium | estimate | 5% | 5 |  | 27 |  | no standard error |
| loo_ROU_cum_premium | estimate | 80.8% | 80.8 |  | 27 |  | no standard error |
| loo_ROU_annual_premium | estimate | 5.1% | 5.1 |  | 27 |  | no standard error |
| loo_CHL_cum_premium | estimate | 81% | 81 |  | 27 |  | no standard error |
| loo_CHL_annual_premium | estimate | 5.1% | 5.1 |  | 27 |  | no standard error |
| loo_ITA_cum_premium | estimate | 82.2% | 82.2 |  | 27 |  | no standard error |
| loo_ITA_annual_premium | estimate | 5.1% | 5.1 |  | 27 |  | no standard error |
| loo_FIN_cum_premium | estimate | 83.4% | 83.4 |  | 27 |  | no standard error |
| loo_FIN_annual_premium | estimate | 5.2% | 5.2 |  | 27 |  | no standard error |
| loo_DEU_cum_premium | estimate | 88.1% | 88.1 |  | 27 |  | no standard error |
| loo_DEU_annual_premium | estimate | 5.4% | 5.4 |  | 27 |  | no standard error |
| loo_GBR_cum_premium | estimate | 89.2% | 89.2 |  | 27 |  | no standard error |
| loo_GBR_annual_premium | estimate | 5.5% | 5.5 |  | 27 |  | no standard error |
| loo_donor_count | count | 27 donors | 27 |  |  |  | the script writes it as a fixed number (27 at line 267), so it is not judged |
| placebo_mad_sun_1938_effect | estimate | 39.5% | 39.5 |  | 8 |  | no standard error |
| placebo_mad_sun_1938_p | p_value | 0.111 p-value | 0.111 |  | 8 | True | both >= 0.05 |
| placebo_mad_sun_1938_n | count | 8 placebos | 8 |  |  | True | precise: the paper's count |
| placebo_mad_sun_1938_rmspe | estimate | 0.38 ratio | 0.38 |  | 8 |  | no standard error |
| placebo_mad_rus_1938_effect | estimate | 54.5% | 54.5 |  | 8 |  | no standard error |
| placebo_mad_rus_1938_p | p_value | 0.111 p-value | 0.111 |  | 8 | True | both >= 0.05 |
| placebo_mad_rus_1938_n | count | 8 placebos | 8 |  |  | True | precise: the paper's count |
| placebo_mad_rus_1938_rmspe | estimate | 0.5 ratio | 0.5 |  | 8 |  | no standard error |
| placebo_gmd_rus_1938_effect | estimate | 65.3% | 65.3 |  | 8 |  | no standard error |
| placebo_gmd_rus_1938_p | p_value | 0.111 p-value | 0.111 |  | 8 | True | both >= 0.05 |
| placebo_gmd_rus_1938_n | count | 8 placebos | 8 |  |  | True | precise: the paper's count |
| placebo_gmd_rus_1938_rmspe | estimate | 0.47 ratio | 0.47 |  | 8 |  | no standard error |
| placebo_mad_sun_1940_effect | estimate | 35.1% | 35.1 |  | 8 |  | no standard error |
| placebo_mad_sun_1940_p | p_value | 0.222 p-value | 0.222 |  | 8 | True | both >= 0.05 |
| placebo_mad_sun_1940_n | count | 8 placebos | 8 |  |  | True | precise: the paper's count |
| placebo_mad_sun_1940_rmspe | estimate | 0.36 ratio | 0.36 |  | 8 |  | no standard error |
| placebo_mad_rus_1940_effect | estimate | 65.1% | 65.1 |  | 8 |  | no standard error |
| placebo_mad_rus_1940_p | p_value | 0.111 p-value | 0.111 |  | 8 | True | both >= 0.05 |
| placebo_mad_rus_1940_n | count | 8 placebos | 8 |  |  | True | precise: the paper's count |
| placebo_mad_rus_1940_rmspe | estimate | 0.49 ratio | 0.49 |  | 8 |  | no standard error |
| placebo_gmd_rus_1940_effect | estimate | 76% | 76 |  | 8 |  | no standard error |
| placebo_gmd_rus_1940_p | p_value | 0.111 p-value | 0.111 |  | 8 | True | both >= 0.05 |
| placebo_gmd_rus_1940_n | count | 8 placebos | 8 |  |  | True | precise: the paper's count |
| placebo_gmd_rus_1940_rmspe | estimate | 0.47 ratio | 0.47 |  | 8 |  | no standard error |
| fake_1905_pseudo_effect | estimate | -11.8% | -11.8 |  | 28 |  | the script writes it as a fixed number (1905 at line 319), so it is not judged |
| fake_1905_pre_rmse | estimate | 0.128 log points | 0.128 |  | 28 |  | the script writes it as a fixed number (1905 at line 320), so it is not judged |
| fake_1905_post_rmse | estimate | 0.09 log points | 0.09 |  | 28 |  | the script writes it as a fixed number (1905 at line 321), so it is not judged |
| fake_1905_horizon | count | 12 years | 12 |  |  |  | the script writes it as a fixed number (1905 at line 322), so it is not judged |
| fake_1913_pseudo_effect | estimate | -29.8% | -29.8 |  | 28 |  | the script writes it as a fixed number (1913 at line 323), so it is not judged |
| fake_1913_pre_rmse | estimate | 0.122 log points | 0.122 |  | 28 |  | the script writes it as a fixed number (1913 at line 324), so it is not judged |
| fake_1913_post_rmse | estimate | 0.179 log points | 0.179 |  | 28 |  | the script writes it as a fixed number (1913 at line 325), so it is not judged |
| fake_1913_horizon | count | 12 years | 12 |  |  |  | the script writes it as a fixed number (1913 at line 326), so it is not judged |
| fake_1921_pseudo_effect | estimate | 115.1% | 115.1 |  | 28 |  | the script writes it as a fixed number (1921 at line 327), so it is not judged |
| fake_1921_pre_rmse | estimate | 0.132 log points | 0.132 |  | 28 |  | the script writes it as a fixed number (1921 at line 328), so it is not judged |
| fake_1921_post_rmse | estimate | 0.128 log points | 0.128 |  | 28 |  | the script writes it as a fixed number (1921 at line 329), so it is not judged |
| fake_1921_horizon | count | 7 years | 7 |  |  |  | the script writes it as a fixed number (1921 at line 330), so it is not judged |
| fake_1924_pseudo_effect | estimate | 39.2% | 39.2 |  | 28 |  | the script writes it as a fixed number (1924 at line 331), so it is not judged |
| fake_1924_pre_rmse | estimate | 0.133 log points | 0.133 |  | 28 |  | the script writes it as a fixed number (1924 at line 332), so it is not judged |
| fake_1924_post_rmse | estimate | 0.108 log points | 0.108 |  | 28 |  | the script writes it as a fixed number (1924 at line 333), so it is not judged |
| fake_1924_horizon | count | 4 years | 4 |  |  |  | the script writes it as a fixed number (1924 at line 334), so it is not judged |
| fake_1926_pseudo_effect | estimate | 3.7% | 3.7 |  | 28 |  | the script writes it as a fixed number (1926 at line 335), so it is not judged |
| fake_1926_pre_rmse | estimate | 0.133 log points | 0.133 |  | 28 |  | the script writes it as a fixed number (1926 at line 336), so it is not judged |
| fake_1926_post_rmse | estimate | 0.018 log points | 0.018 |  | 28 |  | the script writes it as a fixed number (1926 at line 337), so it is not judged |
| fake_1926_horizon | count | 2 years | 2 |  |  |  | the script writes it as a fixed number (1926 at line 338), so it is not judged |
| cia_gnp_1928_37_estA | estimate | 6.2 percent per year | 6.2 |  |  |  | no standard error |
| cia_gnp_1928_37_estB | estimate | 5.4 percent per year | 5.4 |  |  |  | no standard error |
| cia_gnp_1937_40_estA | estimate | 6.3 percent per year | 6.3 |  |  |  | no standard error |
| cia_gnp_1937_40_estB | estimate | 3.9 percent per year | 3.9 |  |  |  | no standard error |
| cia_gnp_1928_54_estA | estimate | 4.4 percent per year | 4.4 |  |  |  | no standard error |
| cia_gnp_1928_54_estB | estimate | 5.9 percent per year | 5.9 |  |  |  | no standard error |

## The paper's own numbers
- NOTE: Spatial placebo exact rank test Maddison SUN 1938: t = 39.5 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test Maddison RUS 1938: t = 54.5 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test GMD RUS 1938: t = 65.3 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test Maddison SUN 1940: t = 35.1 and p = 0.222 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test Maddison RUS 1940: t = 65.1 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided
- NOTE: Spatial placebo exact rank test GMD RUS 1940: t = 76 and p = 0.111 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided

## Guards
- no claims rejected
- spec: the headline was written as prose ('The analysis headline rests on: observed GMD RUS and Maddison RUS exceed median admissible frontier at every endpoint (e'); chosen from the claim names: score_gmd_rus_1938_ascf90
- spec: the headline was written as prose ('Grade B finding that observed Russian-core path exceeds primary ASCF-90 frontier from mid-1930s onward while broader SUN'); chosen from the claim names: score_gmd_rus_1938_ascf90
- round 1: the builder ran out of turns
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 41, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: GMD 2026-09 vintage via gmd-releases S3 (author used same vintage); Maddison Project Database 2023 via DataverseNL fid 421302/421303 (author used GGDC release); CIA/RAND GNP via author's transcription of declassified Table 2 (verified against original PDF); Markevich-Harrison 1913-1928 bridge embedded in GMD pre-1928 series; all estimators and bootstrap exactly as archived in Zenodo replication tables (which are built from the same public sources)
- caveat: sample size not rebuilt: the script writes it as a fixed number (27 at line 267), not counted from the data (loo_donor_count, 27 in the paper); the results are judged without it, so the paper gets at most "partly holds up"

## Data sources
- market data: none used
- other hosts the script fetched from: www.globalmacrodata.com, gmd-releases.s3.ap-southeast-2.amazonaws.com, dataverse.nl, objectstore.surf.nl, zenodo.org

## Run
- sandbox: attempt 2, exit 0, 43.1s, with the packages the builder installed: et_xmlfile==2.0.0, openpyxl==3.1.5, xlrd==2.0.2
- model calls: 58, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 3793801, out 102300 (reasoning 42232); cost $1.2684

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
