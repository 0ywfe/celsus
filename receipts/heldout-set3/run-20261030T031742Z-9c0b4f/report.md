The paper's numbers partly hold up: 36 of 36 checked results match within their uncertainty. Its main result, kappa_X7_Lithuania_2024, is -39.2 PPS in the paper and -33.44 PPS here (not judged: no standard error).

# paper-replicator report: arXiv 2510.04211
**Panel regression for the GDP of the Central and Eastern European countries using time-varying coefficients**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| count_total_pooled_n | count | 319 observations | 319 | 0 | 319 | True | precise: the paper's count |
| count_N_countries | count | 11 countries | 11 |  | 11 | True | precise: the paper's count |
| count_T_years | count | 29 years | 29 |  | 29 |  | the script writes it as a fixed number (29 at line 451), so it is not judged |
| count_d_regressors | parameter | 7 regressors | 7 |  | 7 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| param_df | parameter | 3 degrees of freedom | 3 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| VIF_threshold | parameter | 5 VIF threshold | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| resid_normal_IQR_SD_benchmark | parameter | 1.35 ratio | 1.35 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| resid_normal_RMSE_MAE_benchmark | parameter | 1.25 ratio | 1.25 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| desc_raw_X1_mean | estimate | 62.49 PPS EU27=100 | 62.49 | 0.9538 | 319 | True | paper inside 62.49 +/- 1.869 |
| desc_raw_X1_SD | estimate | 17.04 PPS | 17.03 |  | 319 |  | no standard error |
| desc_raw_X1_Min | estimate | 26 PPS EU27=100 | 26 |  | 319 |  | no standard error |
| desc_raw_X1_Median | estimate | 63 PPS EU27=100 | 63 |  | 319 |  | no standard error |
| desc_raw_X1_Max | estimate | 96 PPS EU27=100 | 96 |  | 319 |  | no standard error |
| desc_raw_X1_Skew | estimate | -0.209 skewness | -0.2102 |  | 319 |  | no standard error |
| desc_raw_X1_Kurt | estimate | 2.129 kurtosis | 2.134 |  | 319 |  | no standard error |
| desc_raw_X2_mean | estimate | 59.91 EU27=100 | 59.91 | 0.7673 | 319 | True | paper inside 59.91 +/- 1.504 |
| desc_raw_X2_SD | estimate | 13.7 EU27=100 | 13.7 |  | 319 |  | no standard error |
| desc_raw_X2_Min | estimate | 20.3 EU27=100 | 20.3 |  | 319 |  | no standard error |
| desc_raw_X2_Median | estimate | 60.5 EU27=100 | 60.5 |  | 319 |  | no standard error |
| desc_raw_X2_Max | estimate | 91.8 EU27=100 | 91.8 |  | 319 |  | no standard error |
| desc_raw_X3_mean | estimate | 77.06 cum. %GDP | 78.41 | 3.721 | 319 | True | paper inside 78.41 +/- 7.293 |
| desc_raw_X3_SD | estimate | 66.44 cum. %GDP | 66.46 |  | 319 |  | no standard error |
| desc_raw_X4_mean | estimate | 115%GDP | 115 | 1.953 | 319 | True | paper inside 115 +/- 3.828 |
| desc_raw_X4_SD | estimate | 34.87%GDP | 34.88 |  | 319 |  | no standard error |
| desc_raw_X5_mean | estimate | 378.2 cum. %GDP | 378.2 | 12.15 | 319 | True | paper inside 378.2 +/- 23.81 |
| desc_raw_X5_SD | estimate | 216.9 cum. %GDP | 216.9 |  | 319 |  | no standard error |
| desc_raw_X6_mean | estimate | 38.37%GDP | 38.76 | 1.356 | 319 | True | paper inside 38.76 +/- 2.657 |
| desc_raw_X6_SD | estimate | 21.71%GDP | 24.22 |  | 319 |  | no standard error |
| desc_raw_X7_mean | estimate | 70%GDP | 70 | 1.598 | 319 | True | paper inside 70 +/- 3.131 |
| desc_raw_X7_SD | estimate | 28.55%GDP | 28.54 |  | 319 |  | no standard error |
| country_Bulgaria_X1_mean | estimate | 43.59 PPS EU27=100 | 43.59 | 1.929 | 29 | True | paper inside 43.59 +/- 3.78 |
| country_Bulgaria_X1_SD | estimate | 10.39 PPS EU27=100 | 10.39 |  | 29 |  | no standard error |
| country_Czechia_X1_mean | estimate | 84.1 PPS EU27=100 | 84.1 | 1.2 | 29 | True | paper inside 84.1 +/- 2.351 |
| country_Estonia_X1_mean | estimate | 64.55 PPS EU27=100 | 64.55 | 3.099 | 29 | True | paper inside 64.55 +/- 6.073 |
| country_Lithuania_Delta_y_mean | estimate | 1.86 PPS EU27=100 change | 1.862 | 0.4403 | 29 | True | paper inside 1.862 +/- 0.8631 |
| country_Poland_Delta_y_mean | estimate | 1.21 PPS EU27=100 change | 1.207 | 0.2644 | 29 | True | paper inside 1.207 +/- 0.5182 |
| corr_X1_X2 | estimate | 0.801 correlation | 0.8007 |  | 319 |  | no standard error |
| corr_X1_X3 | estimate | 0.349 correlation | 0.358 |  | 319 |  | no standard error |
| corr_X4_X5 | estimate | 0.638 correlation | 0.6381 |  | 319 |  | no standard error |
| corr_X6_X7 | estimate | 0.054 correlation | 0.0398 |  | 319 |  | no standard error |
| VIF_low | estimate | 1.1 VIF | 1.072 |  |  |  | no standard error |
| VIF_high | estimate | 4 VIF | 4.101 |  |  |  | no standard error |
| VIF_mean | estimate | 2.6 VIF | 2.679 |  |  |  | no standard error |
| resid_pooled_mean | estimate | 0 residual | 4.458e-15 | 0.0436 | 319 | True | paper inside 4.458e-15 +/- 0.08545 |
| resid_pooled_SD | estimate | 0.747 residual | 0.7787 |  | 319 |  | no standard error |
| resid_pooled_median | estimate | 0.013 residual | 0.005205 |  | 319 |  | no standard error |
| resid_pooled_skew | estimate | 0.037 skewness | -0.09719 |  | 319 |  | no standard error |
| resid_pooled_kurt | estimate | 4.549 kurtosis | 4.911 |  | 319 |  | no standard error |
| resid_pooled_Q25 | estimate | -0.359 residual | -0.3341 |  | 319 |  | no standard error |
| resid_pooled_Q75 | estimate | 0.372 residual | 0.3856 |  | 319 |  | no standard error |
| resid_pooled_IQR | estimate | 0.731 residual | 0.7196 |  | 319 |  | no standard error |
| resid_pooled_RMSE_MAE | estimate | 1.402 ratio | 1.416 |  | 319 |  | no standard error |
| resid_pooled_IQR_SD_ratio | estimate | 0.98 ratio | 0.9242 |  | 319 |  | no standard error |
| JB_pvalue | p_value | 0.0172 p-value | 7.596e-11 |  | 319 | True | both < 0.05 |
| resid_Czechia_mean | estimate | 0.192 residual | 0.2222 | 0.08891 | 29 | True | paper inside 0.2222 +/- 0.1743 |
| resid_Czechia_SD | estimate | 0.492 residual | 0.4788 |  | 29 |  | no standard error |
| resid_Latvia_mean | estimate | -0.207 residual | -0.1846 | 0.1185 | 29 | True | paper inside -0.1846 +/- 0.2322 |
| resid_Latvia_SD | estimate | 0.654 residual | 0.638 |  | 29 |  | no standard error |
| resid_Poland_SD | estimate | 1.275 residual | 1.299 |  | 29 |  | no standard error |
| resid_Hungary_SD | estimate | 0.407 residual | 0.4242 |  | 29 |  | no standard error |
| resid_variance_ratio | estimate | 9.8 variance ratio | 9.376 |  |  |  | no standard error |
| bartlett_B | estimate | 193.1 Bartlett B statistic | 186.2 |  | 319 |  | no standard error |
| bartlett_df | parameter | 28 degrees of freedom | 28 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| bartlett_p | p_value | 0.001 p-value | 0 |  |  | True | both < 0.05 |
| median_deviation_percent_SD | estimate | 1.7 percent of SD | 0.6685 |  | 319 |  | no standard error |
| alpha_1997 | estimate | -5.799 α coefficient | -5.833 | 0.5141 | 11 | True | paper inside -5.833 +/- 1.008 |
| alpha_1997_SE | estimate | 0.407 SE | 0.5141 |  | 11 |  | no standard error |
| alpha_2002 | estimate | 0.3 α coefficient | 0.1305 | 2.24 | 11 | True | paper inside 0.1305 +/- 4.391 |
| alpha_2009 | estimate | 12.08 α coefficient | 12.14 | 5.844 | 11 | True | paper inside 12.14 +/- 11.45 |
| alpha_2013 | estimate | 3.788 α coefficient | 4.378 | 3.537 | 11 | True | paper inside 4.378 +/- 6.932 |
| alpha_2018 | estimate | 7.586 α coefficient | 7.767 | 0.7632 | 11 | True | paper inside 7.767 +/- 1.496 |
| alpha_2021 | estimate | 16.15 α coefficient | 16.31 | 3.281 | 11 | True | paper inside 16.31 +/- 6.431 |
| alpha_2024 | estimate | 4.713 α coefficient | 4.771 | 4.482 | 11 | True | paper inside 4.771 +/- 8.784 |
| beta_X1_1997 | estimate | -0.128 β coefficient | -0.128 | 0.00951 | 11 | True | paper inside -0.128 +/- 0.01864 |
| beta_X1_2002 | estimate | -0.105 β coefficient | -0.1086 | 0.02602 | 11 | True | paper inside -0.1086 +/- 0.051 |
| beta_X1_2009 | estimate | 0.125 β coefficient | 0.1116 | 0.1087 | 11 | True | paper inside 0.1116 +/- 0.213 |
| beta_X1_2013 | estimate | -0.186 β coefficient | -0.1859 | 0.06917 | 11 | True | paper inside -0.1859 +/- 0.1356 |
| beta_X2_1997 | estimate | 0.149 β coefficient | 0.1479 | 0.009975 | 11 | True | paper inside 0.1479 +/- 0.01955 |
| beta_X2_2009 | estimate | -0.526 β coefficient | -0.5667 | 0.2354 | 11 | True | paper inside -0.5667 +/- 0.4613 |
| beta_X2_2013 | estimate | 0.512 β coefficient | 0.5399 | 0.1561 | 11 | True | paper inside 0.5399 +/- 0.3059 |
| beta_X7_1997 | estimate | -0.082 β coefficient | -0.08262 | 0.006814 | 11 | True | paper inside -0.08262 +/- 0.01336 |
| beta_X7_2002 | estimate | 0.069 β coefficient | 0.07113 | 0.03922 | 11 | True | paper inside 0.07113 +/- 0.07687 |
| beta_X7_2013 | estimate | -0.125 β coefficient | -0.127 | 0.03892 | 11 | True | paper inside -0.127 +/- 0.07629 |
| beta_X7_2018 | estimate | -0.068 β coefficient | -0.06931 | 0.00521 | 11 | True | paper inside -0.06931 +/- 0.01021 |
| beta_X7_2024 | estimate | 0.039 β coefficient | 0.03925 | 0.03424 | 11 | True | paper inside 0.03925 +/- 0.06711 |
| R2_1997 | estimate | 0.999 R2 | 0.9991 |  | 11 |  | no standard error |
| R2_2009 | estimate | 0.886 R2 | 0.8897 |  | 11 |  | no standard error |
| R2_2024 | estimate | 0.642 R2 | 0.6319 |  | 11 |  | no standard error |
| AdjR2_1997 | estimate | 0.997 Adjusted R2 | 0.9971 |  | 11 |  | no standard error |
| AdjR2_2024 | estimate | -0.193 Adjusted R2 | -0.2269 |  | 11 |  | no standard error |
| ResidSD_1997 | estimate | 0.162 Residual SD | 0.1683 |  | 11 |  | no standard error |
| ResidSD_2009 | estimate | 2.109 Residual SD | 2.071 |  | 11 |  | no standard error |
| ResidSD_2024 | estimate | 1.021 Residual SD | 1.035 |  | 11 |  | no standard error |
| Fstat_1997 | estimate | 428.1 F-statistic | 496.8 |  | 11 |  | no standard error |
| Fstat_2009 | estimate | 3.331 F-statistic | 3.458 |  | 11 |  | no standard error |
| Fstat_2024 | estimate | 0.769 F-statistic | 0.7358 |  | 11 |  | no standard error |
| kappa_Total_Bulgaria_2024 | estimate | 64.2 PPS EU27=100 component | 65.6 |  |  |  | no standard error |
| kappa_X2_Bulgaria_2024 | estimate | 143 PPS | 129 |  |  |  | no standard error |
| kappa_X7_Bulgaria_2024 | estimate | -84.7 PPS | -73.3 |  |  |  | no standard error |
| kappa_X1_Bulgaria_2024 | estimate | -78.2 PPS | -69.52 |  |  |  | no standard error |
| kappa_X7_Czechia_2024 | estimate | -52.7 PPS | -46.11 |  |  |  | no standard error |
| kappa_X7_Estonia_2024 | estimate | -93 PPS | -82.25 |  |  |  | no standard error |
| kappa_X7_Latvia_2024 | estimate | -75.8 PPS | -65.42 |  |  |  | no standard error |
| kappa_X7_Lithuania_2024 | estimate | -39.2 PPS | -33.44 |  |  |  | no standard error |
| kappa_X7_Poland_2024 | estimate | -41.3 PPS | -34.9 |  |  |  | no standard error |
| kappa_X7_Romania_2024 | estimate | -42.7 PPS | -36.61 |  |  |  | no standard error |
| kappa_X7_Slovenia_2024 | estimate | -66.2 PPS | -56.43 |  |  |  | no standard error |
| kappa_X7_Slovakia_2024 | estimate | -48.3 PPS | -42.55 |  |  |  | no standard error |
| kappa_Total_Lithuania_2024 | estimate | 86.5 PPS | 85.1 |  |  |  | no standard error |
| kappa_Total_Estonia_2024 | estimate | 79.8 PPS | 79.15 |  |  |  | no standard error |
| accum_error_Bulgaria_2024 | estimate | 1.8 PPS | 0.4013 |  |  |  | no standard error |
| accum_error_Czechia_2024 | estimate | 5.6 PPS | 6.443 |  |  |  | no standard error |
| accum_error_Latvia_2024 | estimate | -6 PPS | -5.353 |  |  |  | no standard error |
| accum_error_Lithuania_2024 | estimate | 1.5 PPS | 2.902 |  |  |  | no standard error |

## The paper's own numbers
- OK: by_country_pooled319: 29 + 29 + 29 + 29 + 29 + 29 + 29 + 29 + 29 + 29 + 29 = 319, paper's total 319
- OK: by_year_crosssection_N11: 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 + 11 = 319, paper's total 319
- NOTE: Bartlett heteroskedasticity equal variances across 29 yearly cross-sections: t = 193.09, paper's p = 0.001 matches one-sided (upper tail) (0.0000); two-sided p would be 0.0000
- NOTE: Jarque-Bera normality pooled residuals: t = 4.549 and p = 0.0172 fit no side at the printed precision (two-sided p would be 0.0000); judged two-sided

## Guards
- no claims rejected
- spec: the headline was written as prose ('kappa_X7_Estonia_2024, kappa_X7_Bulgaria_2024, kappa_X7_Lithuania_2024, kappa_X7_Poland_2024, kappa_Total_Lithuania_2024'); chosen from the claim names: kappa_X7_Estonia_2024
- round 1: the builder ran out of turns
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 319, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Eurostat prc_ppp_ind for X1 X2; World Bank BX.KLT.DINV.WD.GD.ZS cumulated for X3, NE.TRD.GNFS.ZS for X4, NE.GDI.TOTL.ZS cumulated for X5; Eurostat gov_10dd_edpt1 S13 general gov debt for X6 (paper says central but S13 matches most means); Eurostat tipspd20 for X7. Current Eurostat vintage has BG gov outlier; SK FDI revision

## Data sources
- market data: none used
- other hosts the script fetched from: ec.europa.eu, api.worldbank.org

## Run
- sandbox: attempt 1, exit 0, 57.7s
- model calls: 35, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 2270673, out 103343 (reasoning 46073); cost $0.9949

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
