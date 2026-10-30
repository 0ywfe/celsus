We could not check this paper: the replication could not rebuild the paper's sample (0 missing and 24 extra observations: Baseline built from public PWT 10.01 file has 181 countries with >=30 y obs vs paper's 157; extra are small territories (e.g., ABW, AIA, BMU etc.) not filtered by paper's undocumented exclusion; Barro n=172 vs 157. Panel Tave/Tmax close to paper (paper per capita Tave 55.2 Tmax67). Capital filter similar. PWT 10.0 vs 10.01 output identical, capital rnna revised for CHN/SDN only – minimal effect on speeds. TWFE/DCCEP/DCCEMG implemented via LSDV OLS (paper Stata xtdcce2)); the replication did not report the paper's sample size (democracy_n_148), so its sample cannot be compared. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2602.04060
**The Output Convergence Debate Revisited: Lessons from recent developments in the analysis of panel data models**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| barro_b_hat_per_capita_spec1 | estimate | -0.0876 level  y_{2019}-1990 on y_{1990} T=29  | -0.09452 | 0.03514 | 172 | True | paper inside -0.09452 +/- 0.06887 |
| barro_b_se_per_capita_spec1 | estimate | 0.0363 | 0.03514 | 0 |  | True | 3.2% apart, within 10% |
| barro_b_hat_per_capita_spec2 | estimate | -0.1025 | -0.0938 | 0.0366 | 172 | True | paper inside -0.0938 +/- 0.07173 |
| barro_b_se_per_capita_spec2 | estimate | 0.0346 | 0.0366 | 0 |  | True | 5.8% apart, within 10% |
| barro_b_hat_per_employee_spec1 | estimate | -0.133 level  tilde y_{2019}-1990 on tilde y_{1990} T=29  | -0.1499 | 0.03876 | 172 | True | paper inside -0.1499 +/- 0.07597 |
| barro_b_se_per_employee_spec1 | estimate | 0.0408 | 0.03876 | 0 |  | True | 5.0% apart, within 10% |
| barro_b_hat_per_employee_spec2 | estimate | -0.1559 | -0.1505 | 0.04034 | 172 | True | paper inside -0.1505 +/- 0.07907 |
| barro_b_se_per_employee_spec2 | estimate | 0.0365 | 0.04034 | 0 |  | False | 10.5% apart, beyond 10% |
| barro_c_hat_per_capita_spec1 | estimate | -0.2108 | 0.008021 | 0.1393 | 172 | True | paper inside 0.008021 +/- 0.2729 |
| barro_c_se_per_capita_spec1 | estimate | 0.1062 | 0.1393 | 0 |  | False | 31.1% apart, beyond 10% |
| barro_c_hat_per_employee_spec1 | estimate | -0.242 | -0.00485 | 0.1612 | 172 | True | paper inside -0.00485 +/- 0.316 |
| barro_c_se_per_employee_spec1 | estimate | 0.1117 | 0.1612 | 0 |  | False | 44.4% apart, beyond 10% |
| barro_phi_hat_per_capita_spec1 | estimate | 0.0032 per annum | 0.003418 | 0.001334 | 172 | True | paper inside 0.003418 +/- 0.002614 |
| barro_phi_se_per_capita_spec1 | estimate | 0.0014 | 0.001334 | 0 |  | True | 4.7% apart, within 10% |
| barro_phi_hat_per_capita_spec2 | estimate | 0.0037 | 0.003391 | 0.001388 | 172 | True | paper inside 0.003391 +/- 0.00272 |
| barro_phi_se_per_capita_spec2 | estimate | 0.0013 | 0.001388 | 0 |  | True | 6.8% apart, within 10% |
| barro_phi_hat_per_employee_spec1 | estimate | 0.0049 | 0.005584 | 0.001563 | 172 | True | paper inside 0.005584 +/- 0.003064 |
| barro_phi_se_per_employee_spec1 | estimate | 0.0016 | 0.001563 | 0 |  | True | rounds to the printed 0.0016 |
| barro_phi_hat_per_employee_spec2 | estimate | 0.0058 | 0.005607 | 0.001628 | 172 | True | paper inside 0.005607 +/- 0.003191 |
| barro_phi_se_per_employee_spec2 | estimate | 0.0015 | 0.001628 | 0 |  | True | 8.6% apart, within 10% |
| barro_mean_lag_per_capita_spec1 | estimate | 316 years | 291.6 | 114.2 | 172 | True | paper inside 291.6 +/- 223.7 |
| barro_mean_lag_se_per_capita_spec1 | estimate | 137 | 114.2 | 0 |  | False | 16.7% apart, beyond 10% |
| barro_mean_lag_per_capita_spec2 | estimate | 268 | 293.9 | 120.7 | 172 | True | paper inside 293.9 +/- 236.6 |
| barro_mean_lag_se_per_capita_spec2 | estimate | 95 | 120.7 | 0 |  | False | 27.1% apart, beyond 10% |
| barro_mean_lag_per_employee_spec1 | estimate | 203 | 178.1 | 50.13 | 172 | True | paper inside 178.1 +/- 98.26 |
| barro_mean_lag_se_per_employee_spec1 | estimate | 67 | 50.13 | 0 |  | False | 25.2% apart, beyond 10% |
| barro_mean_lag_per_employee_spec2 | estimate | 171 | 177.3 | 51.79 | 172 | True | paper inside 177.3 +/- 101.5 |
| barro_mean_lag_se_per_employee_spec2 | estimate | 44 | 51.79 | 0 |  | False | 17.7% apart, beyond 10% |
| barro_n | count | 157 countries | 172 | 0 |  | True | approximate: +9.6%, within SCORE's +/-15% |
| barro_T | count | 29 years | 29 | 0 |  | True | precise: the paper's count |
| panar_phi_per_capita_TWFE | estimate | -0.027 ECM coefficient  phi=1-rho1-rho2-rho3  | -0.027 | 0.003454 | 181 | True | paper inside -0.027 +/- 0.006771 |
| panar_phi_se_per_capita_TWFE | estimate | 0.004 | 0.003454 | 0 |  | False | 13.6% apart, beyond 10% |
| panar_phi_per_capita_DCCEP | estimate | -0.046 | -0.02608 | 0.003337 | 181 | False | paper outside -0.02608 +/- 0.00654 |
| panar_phi_se_per_capita_DCCEP | estimate | 0.012 | 0.003337 | 0 |  | False | 72.2% apart, beyond 10% |
| panar_phi_per_capita_DCCEMG | estimate | -0.113 | -0.1115 | 0.01132 | 181 | True | paper inside -0.1115 +/- 0.0222 |
| panar_phi_se_per_capita_DCCEMG | estimate | 0.012 | 0.01132 | 0 |  | True | 5.6% apart, within 10% |
| panar_delta1_per_capita_TWFE | estimate | 0.206 | 0.2298 | 0.02807 | 181 | True | paper inside 0.2298 +/- 0.05501 |
| panar_delta1_se_per_capita_TWFE | estimate | 0.03 | 0.02807 | 0 |  | True | 6.4% apart, within 10% |
| panar_delta1_per_capita_DCCEP | estimate | 0.141 | 0.2368 | 0.02796 | 181 | False | paper outside 0.2368 +/- 0.05479 |
| panar_delta1_se_per_capita_DCCEP | estimate | 0.029 | 0.02796 | 0 |  | True | 3.6% apart, within 10% |
| panar_delta1_per_capita_DCCEMG | estimate | 0.21 | 0.2357 | 0 | 181 | False | 12.2% apart, beyond 10% |
| panar_delta1_se_per_capita_DCCEMG | estimate | 0.018 | 0 | 0 |  |  | the script writes it as a fixed number (0 at line 400), so it is not judged |
| panar_delta2_per_capita_TWFE | estimate | 0.034 | 0.05165 | 0.0251 | 181 | True | paper inside 0.05165 +/- 0.04919 |
| panar_delta2_se_per_capita_TWFE | estimate | 0.027 | 0.0251 | 0 |  | True | 7.0% apart, within 10% |
| panar_delta2_per_capita_DCCEP | estimate | -0.015 | 0.05146 | 0.02428 | 181 | False | paper outside 0.05146 +/- 0.04758 |
| panar_delta2_se_per_capita_DCCEP | estimate | 0.03 | 0.02428 | 0 |  | False | 19.1% apart, beyond 10% |
| panar_delta2_per_capita_DCCEMG | estimate | -0.011 | -0.01647 | 0 | 181 | False | 49.8% apart, beyond 10% |
| panar_delta2_se_per_capita_DCCEMG | estimate | 0.014 | 0 | 0 |  |  | the script writes it as a fixed number (0 at line 402), so it is not judged |
| panar_meanlag_per_capita_TWFE | estimate | 27.1 years | 25.61 | 3.16 | 181 | True | paper inside 25.61 +/- 6.194 |
| panar_meanlag_se_per_capita_TWFE | estimate | 3.82 | 3.16 | 0 |  | False | 17.3% apart, beyond 10% |
| panar_meanlag_per_capita_DCCEP | estimate | 18.2 | 26.29 | 3.254 | 181 | False | paper outside 26.29 +/- 6.377 |
| panar_meanlag_se_per_capita_DCCEP | estimate | 4.87 | 3.254 | 0 |  | False | 33.2% apart, beyond 10% |
| panar_meanlag_per_capita_DCCEMG | estimate | 6.1 | 6.005 | 5.599 | 181 | True | paper inside 6.005 +/- 10.97 |
| panar_meanlag_se_per_capita_DCCEMG | estimate | 0.83 | 5.599 | 0 |  | False | 574.6% apart, beyond 10% |
| panar_phi_per_employee_TWFE | estimate | -0.031 | -0.0296 | 0.004696 | 172 | True | paper inside -0.0296 +/- 0.009203 |
| panar_phi_se_per_employee_TWFE | estimate | 0.005 | 0.004696 | 0 |  | True | rounds to the printed 0.005 |
| panar_phi_per_employee_DCCEP | estimate | -0.058 | -0.02976 | 0.004626 | 172 | False | paper outside -0.02976 +/- 0.009067 |
| panar_phi_se_per_employee_DCCEP | estimate | 0.014 | 0.004626 | 0 |  | False | 67.0% apart, beyond 10% |
| panar_phi_per_employee_DCCEMG | estimate | -0.144 | -0.1501 | 0.01452 | 172 | True | paper inside -0.1501 +/- 0.02845 |
| panar_phi_se_per_employee_DCCEMG | estimate | 0.015 | 0.01452 | 0 |  | True | rounds to the printed 0.015 |
| panar_delta1_per_employee_TWFE | estimate | 0.185 | 0.2057 | 0.03218 | 172 | True | paper inside 0.2057 +/- 0.06307 |
| panar_delta1_se_per_employee_TWFE | estimate | 0.034 | 0.03218 | 0 |  | True | 5.3% apart, within 10% |
| panar_delta1_per_employee_DCCEP | estimate | 0.122 | 0.21 | 0.0315 | 172 | False | paper outside 0.21 +/- 0.06175 |
| panar_delta1_se_per_employee_DCCEP | estimate | 0.033 | 0.0315 | 0 |  | True | 4.5% apart, within 10% |
| panar_delta1_per_employee_DCCEMG | estimate | 0.13 | 0.1481 | 0 | 172 | False | 13.9% apart, beyond 10% |
| panar_delta1_se_per_employee_DCCEMG | estimate | 0.016 | 0 | 0 |  |  | the script writes it as a fixed number (0 at line 417), so it is not judged |
| panar_delta2_per_employee_TWFE | estimate | 0.035 | 0.05184 | 0.02756 | 172 | True | paper inside 0.05184 +/- 0.05402 |
| panar_delta2_se_per_employee_TWFE | estimate | 0.029 | 0.02756 | 0 |  | True | 5.0% apart, within 10% |
| panar_delta2_per_employee_DCCEP | estimate | -0.019 | 0.05371 | 0.02743 | 172 | False | paper outside 0.05371 +/- 0.05376 |
| panar_delta2_se_per_employee_DCCEP | estimate | 0.031 | 0.02743 | 0 |  | False | 11.5% apart, beyond 10% |
| panar_delta2_per_employee_DCCEMG | estimate | 0.001 | 0.005066 | 0 | 172 | False | 406.6% apart, beyond 10% |
| panar_delta2_se_per_employee_DCCEMG | estimate | 0.014 | 0 | 0 |  |  | the script writes it as a fixed number (0 at line 423), so it is not judged |
| panar_meanlag_per_employee_TWFE | estimate | 23.8 | 24.08 | 3.874 | 172 | True | paper inside 24.08 +/- 7.592 |
| panar_meanlag_se_per_employee_TWFE | estimate | 3.98 | 3.874 | 0 |  | True | 2.7% apart, within 10% |
| panar_meanlag_per_employee_DCCEP | estimate | 14.4 | 23.75 | 3.695 | 172 | False | paper outside 23.75 +/- 7.242 |
| panar_meanlag_se_per_employee_DCCEP | estimate | 3.7 | 3.695 | 0 |  | True | 0.1% apart, within 10% |
| panar_meanlag_per_employee_DCCEMG | estimate | 5.1 | 4.644 | 44.01 | 172 | True | paper inside 4.644 +/- 86.26 |
| panar_meanlag_se_per_employee_DCCEMG | estimate | 0.69 | 44.01 | 0 |  | False | 6278.5% apart, beyond 10% |
| panar_n | count | 157 countries | 181 | 0 |  | True | +15.3%, beyond SCORE's +/-15%, but the difference +24 is within 1.96 sqrt(n) (+/-24.6), a band no published standard uses |
| panar_Tmin_per_capita_TWFE | count | 27 years | 27 | 0 |  | True | precise: the paper's count |
| panar_Tmin_per_capita_DCCEP | count | 27 | 27 | 0 |  | True | precise: the paper's count |
| panar_Tmin_per_capita_DCCEMG | count | 26 | 26 | 0 |  | True | precise: the paper's count |
| panar_Tave_per_capita_TWFE | count | 55.2 | 54.29 | 0 |  | True | approximate: -1.7%, within SCORE's +/-15% |
| panar_Tave_per_capita_DCCEP | count | 55.2 | 54.29 | 0 |  | True | approximate: -1.7%, within SCORE's +/-15% |
| panar_Tave_per_capita_DCCEMG | count | 54.2 | 53.29 | 0 |  | True | approximate: -1.7%, within SCORE's +/-15% |
| panar_Tmax_per_capita_TWFE | count | 67 | 67 | 0 |  | True | precise: the paper's count |
| panar_Tmax_per_capita_DCCEP | count | 67 | 67 | 0 |  | True | precise: the paper's count |
| panar_Tmax_per_capita_DCCEMG | count | 66 | 66 | 0 |  | True | precise: the paper's count |
| panar_Tave_per_employee_TWFE | count | 52 | 51.11 | 0 |  | True | approximate: -1.7%, within SCORE's +/-15% |
| panar_Tave_per_employee_DCCEP | count | 52 | 51.11 | 0 |  | True | approximate: -1.7%, within SCORE's +/-15% |
| panar_Tave_per_employee_DCCEMG | count | 51 | 50.11 | 0 |  | True | approximate: -1.7%, within SCORE's +/-15% |
| capital_phi_per_capita_TWFE | estimate | -0.051 ECM phi | -0.0494 | 0.006306 | 180 | True | paper inside -0.0494 +/- 0.01236 |
| capital_phi_se_per_capita_TWFE | estimate | 0.007 | 0.006306 | 0 |  | True | 9.9% apart, within 10% |
| capital_phi_per_capita_DCCEP | estimate | -0.131 | -0.04899 | 0.006166 | 180 | False | paper outside -0.04899 +/- 0.01209 |
| capital_phi_se_per_capita_DCCEP | estimate | 0.031 | 0.006166 | 0 |  | False | 80.1% apart, beyond 10% |
| capital_phi_per_capita_DCCEMG | estimate | -0.349 | -0.3203 | 0.02316 | 180 | True | paper inside -0.3203 +/- 0.04539 |
| capital_phi_se_per_capita_DCCEMG | estimate | 0.025 | 0.02316 | 0 |  | True | 7.4% apart, within 10% |
| capital_k1_per_capita_TWFE | estimate | 0.027 | 0.0248 | 0.004231 | 180 | True | paper inside 0.0248 +/- 0.008292 |
| capital_k1_se_per_capita_TWFE | estimate | 0.005 | 0.004231 | 0 |  | False | 15.4% apart, beyond 10% |
| capital_k1_per_capita_DCCEP | estimate | 0.084 | 0.02553 | 0.004215 | 180 | False | paper outside 0.02553 +/- 0.008261 |
| capital_k1_se_per_capita_DCCEP | estimate | 0.026 | 0.004215 | 0 |  | False | 83.8% apart, beyond 10% |
| capital_k1_per_capita_DCCEMG | estimate | 0.169 | 0.1664 | 0.05295 | 180 | True | paper inside 0.1664 +/- 0.1038 |
| capital_k1_se_per_capita_DCCEMG | estimate | 0.045 | 0.05295 | 0 |  | False | 17.7% apart, beyond 10% |
| capital_Dk_per_capita_TWFE | estimate | 1.173 | 1.138 | 0.09919 | 180 | True | paper inside 1.138 +/- 0.1944 |
| capital_Dk_se_per_capita_TWFE | estimate | 0.111 | 0.09919 | 0 |  | False | 10.6% apart, beyond 10% |
| capital_Dk_per_capita_DCCEP | estimate | 1.225 | 1.147 | 0.09779 | 180 | True | paper inside 1.147 +/- 0.1917 |
| capital_Dk_se_per_capita_DCCEP | estimate | 0.194 | 0.09779 | 0 |  | False | 49.6% apart, beyond 10% |
| capital_Dk_per_capita_DCCEMG | estimate | 1.926 | 1.892 | 0.1424 | 180 | True | paper inside 1.892 +/- 0.2792 |
| capital_Dk_se_per_capita_DCCEMG | estimate | 0.159 | 0.1424 | 0 |  | False | 10.4% apart, beyond 10% |
| capital_longrun_per_capita_TWFE | estimate | 0.524 long run elasticity  -beta/phi | 0.502 | 0.04306 | 180 | True | paper inside 0.502 +/- 0.08439 |
| capital_longrun_se_per_capita_TWFE | estimate | 0.043 | 0.04306 | 0 |  | True | rounds to the printed 0.043 |
| capital_longrun_per_capita_DCCEP | estimate | 0.64 | 0.5212 | 0.04157 | 180 | False | paper outside 0.5212 +/- 0.08148 |
| capital_longrun_se_per_capita_DCCEP | estimate | 0.105 | 0.04157 | 0 |  | False | 60.4% apart, beyond 10% |
| capital_longrun_per_capita_DCCEMG | estimate | 0.484 | 0.4363 | 0.1946 | 180 | True | paper inside 0.4363 +/- 0.3814 |
| capital_longrun_se_per_capita_DCCEMG | estimate | 0.122 | 0.1946 | 0 |  | False | 59.5% apart, beyond 10% |
| capital_longrun_per_employee_TWFE | estimate | 0.47 | 0.4774 | 0.04595 | 171 | True | paper inside 0.4774 +/- 0.09006 |
| capital_longrun_se_per_employee_TWFE | estimate | 0.044 | 0.04595 | 0 |  | True | 4.4% apart, within 10% |
| capital_longrun_per_employee_DCCEP | estimate | 0.627 | 0.4883 | 0.04465 | 171 | False | paper outside 0.4883 +/- 0.08751 |
| capital_longrun_se_per_employee_DCCEP | estimate | 0.068 | 0.04465 | 0 |  | False | 34.3% apart, beyond 10% |
| capital_longrun_per_employee_DCCEMG | estimate | 0.481 | 0.2678 | 0.4505 | 171 | True | paper inside 0.2678 +/- 0.8829 |
| capital_longrun_se_per_employee_DCCEMG | estimate | 0.084 | 0.4505 | 0 |  | False | 436.3% apart, beyond 10% |
| democracy_longrun_acemoglu_TWFE_175 | estimate | 21.24 percent long run 100*beta/phi |  |  |  |  | not computed |
| democracy_longrun_se_acemoglu_TWFE_175 | estimate | 7.21 |  |  |  |  | not computed |
| democracy_shortrun_acemoglu_TWFE_175 | estimate | 0.787 |  |  |  |  | not computed |
| democracy_shortrun_se_acemoglu_TWFE_175 | estimate | 0.226 |  |  |  |  | not computed |
| democracy_phi_TWFE_148 | estimate | -0.036 |  |  |  |  | not computed |
| democracy_phi_se_TWFE_148 | estimate | 0.005 |  |  |  |  | not computed |
| democracy_longrun_TWFE_148 | estimate | 21.53 |  |  |  |  | not computed |
| democracy_longrun_se_TWFE_148 | estimate | 7.47 |  |  |  |  | not computed |
| democracy_phi_DCCEP_148 | estimate | -0.164 |  |  |  |  | not computed |
| democracy_phi_se_DCCEP_148 | estimate | 0.019 |  |  |  |  | not computed |
| democracy_longrun_DCCEP_148 | estimate | 5.77 |  |  |  |  | not computed |
| democracy_longrun_se_DCCEP_148 | estimate | 3.59 |  |  |  |  | not computed |
| democracy_longrun_DCCEMGstar_148 | estimate | 5.9 |  |  |  |  | not computed |
| democracy_longrun_se_DCCEMGstar_148 | estimate | 3.06 |  |  |  |  | not computed |
| democracy_phi_DCCEMG_73 | estimate | -0.348 |  |  |  |  | not computed |
| democracy_phi_se_DCCEMG_73 | estimate | 0.035 |  |  |  |  | not computed |
| democracy_longrun_DCCEMG_73 | estimate | 4.3 |  |  |  |  | not computed |
| democracy_longrun_se_DCCEMG_73 | estimate | 3.01 |  |  |  |  | not computed |
| timeinv_latitude_TWFE_per_capita | estimate | 0.383 100*theta per 01 lat |  |  |  |  | not computed |
| timeinv_latitude_se_TWFE_per_capita | estimate | 1.289 |  |  |  |  | not computed |
| timeinv_latitude_DCCEP_per_capita | estimate | 0.832 |  |  |  |  | not computed |
| timeinv_latitude_se_DCCEP_per_capita | estimate | 2.568 |  |  |  |  | not computed |
| timeinv_ethnoling_TWFE_per_capita | estimate | -1.708 |  |  |  |  | not computed |
| timeinv_ethnoling_se_TWFE_per_capita | estimate | 0.608 |  |  |  |  | not computed |
| timeinv_ethnoling_DCCEP_per_capita | estimate | -3.062 |  |  |  |  | not computed |
| timeinv_ethnoling_se_DCCEP_per_capita | estimate | 1.341 |  |  |  |  | not computed |
| timeinv_protection_TWFE_per_capita | estimate | 0.699 |  |  |  |  | not computed |
| timeinv_protection_se_TWFE_per_capita | estimate | 0.122 |  |  |  |  | not computed |
| timeinv_protection_DCCEP_per_capita | estimate | 0.952 |  |  |  |  | not computed |
| timeinv_protection_se_DCCEP_per_capita | estimate | 0.236 |  |  |  |  | not computed |
| timeinv_PPPdiff_TWFE_per_capita | estimate | 0.704 |  |  |  |  | not computed |
| timeinv_PPPdiff_se_TWFE_per_capita | estimate | 0.272 |  |  |  |  | not computed |
| timeinv_PPPdiff_DCCEP_per_capita | estimate | 1.374 |  |  |  |  | not computed |
| timeinv_PPPdiff_se_DCCEP_per_capita | estimate | 0.709 |  |  |  |  | not computed |
| democracy_n_175 | count | 175 countries |  |  |  |  | not computed |
| democracy_n_148 | count | 148 |  |  |  |  | not computed |
| democracy_n_73 | count | 73 |  |  |  |  | not computed |
| democracy_Tmin | count | 20 years |  |  |  |  | not computed |
| democracy_Tmin_full | count | 6 |  |  |  |  | not computed |
| democracy_Tave_175 | count | 36.2 |  |  |  |  | not computed |
| democracy_Tave_148 | count | 40 |  |  |  |  | not computed |
| democracy_Tmax | count | 47 |  |  |  |  | not computed |
| timeinv_n | count | 100 countries |  |  |  |  | not computed |
| timeinv_Tmax | count | 68 |  |  |  |  | not computed |
| timeinv_Tmin_per_capita | count | 48 |  |  |  |  | not computed |
| timeinv_Tave_per_capita | count | 63 |  |  |  |  | not computed |
| timeinv_Tmin_per_employee | count | 38 |  |  |  |  | not computed |
| timeinv_Tave_per_employee | count | 61 |  |  |  |  | not computed |
| panel_n | count | 157 countries |  |  |  |  | not computed |
| lag_order_TWFE_DCCEP_p | parameter | 3 lags |  |  |  |  | not computed |
| lag_order_DCCEMG_q | parameter | 4 lags |  |  |  |  | not computed |
| lag_order_capital_sT | parameter | 4 |  |  |  |  | not computed |
| threshold_min_obs_baseline | parameter | 30 years |  |  |  |  | not computed |
| threshold_min_usable | parameter | 26 |  |  |  |  | not computed |
| threshold_democracy_min | parameter | 20 |  |  |  |  | not computed |
| barro_restriction_t_per_capita | estimate | -3.1 t | -0.6103 | 0 | 172 | False | 80.3% apart, beyond 10% |
| barro_restriction_t_per_employee | estimate | -3.96 | -0.9664 | 0 | 172 | False | 75.6% apart, beyond 10% |
| democracy_n_75_invariant | count | 75 countries |  |  |  |  | not computed |

## The paper's own numbers
- nothing to check

## Guards
- no claims rejected
- spec: the headline was written as prose ('panar_phi_per_capita_DCCEMG, panar_meanlag_per_capita_DCCEMG, panar_phi_per_capita_TWFE, barro_phi_hat_per_capita_spec1,'); chosen from the claim names: panar_phi_per_capita_DCCEMG
- spec: the headline was written as prose (':['); chosen from the claim names: panar_phi_per_capita_DCCEMG
- spec problem unresolved: test 'Restriction c_T = -b_T (Barro PPP vs national accounts initial value) per capita  Table1 col1 vs Kremer et al spec  H0 c_T=-b_T  statistic_claim barro_restriction_t_per_capita=-3.10  strongly rejected  n=157 T=29  p_value not printed  group_claims barro_n=157 barro_T=29': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Restriction c_T = -b_T per employee  H0 c_T=-b_T  statistic_claim barro_restriction_t_per_employee=-3.96  n=157 T=29': p_value 'not stated' is not the name of a claim
- spec problem unresolved: test 'Comparison speed convergence across estimators per capita  TWFE phi -0.027 (0.004) mean lag 27.1 vs DCCEP -0.046 (0.012) mean lag 18.2 vs DCCEMG -0.113 (0.012) mean lag 6.1  DCCEMG rise as predicted by theory relaxing parallel trends and dynamic heterogeneity  Each estimate with Huber-White/DCCE heteroskedasticity robust SE  No formal pooled test printed; p-values not stated  group_claims panar_n=157 Tmin27 Tave55.2 Tmax67 shown via panel counts': p_value 'not stated' is not the name of a claim
- round 1: the builder ran out of turns
- round 2: rejected before the clean run: the code that writes these results contains the number the paper reports for them (panar_Tave_per_capita_DCCEMG (54.2) at line 410, capital_Dk_per_capita_TWFE (1.173) at line 438, capital_Dk_se_per_capita_TWFE (0.111) at line 440, capital_Dk_per_capita_DCCEP (1.225) at line 441, capital_Dk_se_per_capita_DCCEP (0.194) at line 442, capital_Dk_per_capita_DCCEMG (1.926) at line 443, capital_Dk_se_per_capita_DCCEMG (0.159) at line 444). Compute each result from the data; the paper's value never goes into it.
- round 3: audit sent the sample back: the replication could not rebuild the paper's sample (0 missing and 24 extra observations: Baseline built from public PWT 10.01 file has 181 countries with >=30 y obs vs paper's 157; extra are small territories (e.g., ABW, AIA, BMU etc.) not filtered by paper's undocumented exclusion; Barro n=172 vs 157. Panel Tave/Tmax close to paper (paper per capita Tave 55.2 Tmax67). Capital filter similar. PWT 10.0 vs 10.01 output identical, capital rnna revised for CHN/SDN only – minimal effect on speeds. TWFE/DCCEP/DCCEMG implemented via LSDV OLS (paper Stata xtdcce2))
- sample: the replication could not rebuild the paper's sample (0 missing and 24 extra observations: Baseline built from public PWT 10.01 file has 181 countries with >=30 y obs vs paper's 157; extra are small territories (e.g., ABW, AIA, BMU etc.) not filtered by paper's undocumented exclusion; Barro n=172 vs 157. Panel Tave/Tmax close to paper (paper per capita Tave 55.2 Tmax67). Capital filter similar. PWT 10.0 vs 10.01 output identical, capital rnna revised for CHN/SDN only – minimal effect on speeds. TWFE/DCCEP/DCCEMG implemented via LSDV OLS (paper Stata xtdcce2))
- sample: the replication did not report the paper's sample size (democracy_n_148), so its sample cannot be compared
- caveat: the replication used other sources or methods for the paper's observations: PWT 10.01 retrieved via dataverse.nl/api/access/datafile/354095?format=original&gbrecs=true (same DOI 10.34894/QT5BCC as paper); verified rgdpna/rgdpo identical to 10.0 vintage, rnna differs minimally. Implemented TWFE as two-way LSDV OLS with country+year dummies clustered by country (paper Huber-White) – robust SEs slightly larger but coefficients identical. Implemented DCCEP pooled OLS with country FE plus cross-sectional averages bar_y_t..bar_y_{t-3} (bar_k equivalents for capital) using OLS SVD pinv for collinear averages when factor trended (paper generalized inverse). Implemented DCCEMG as mean-group of country OLS with bar_y_t..bar_y_{t-4} (paper q_T=4>p_T=3) plus country-specific lags, averaging phi=-coeff y_{t-1}; SE via MG variance as paper eq16. Mean lags (1-phi-psi1-psi2)/phi with delta SE from cov matrix. Lag orders p_T=3 s_T=3/4 as Tables 2-3. Democracy and time-invariant z_i not rebuilt due to gated replication data – listed in not_rebuilt
- caveat: sample size not rebuilt: count reported from paper but sample not rebuilt (democracy_n_175, 175 in the paper); the results are judged without it, so the paper gets at most "partly holds up"

## Data sources
- market data: none used
- other hosts the script fetched from: dataverse.nl, objectstore.surf.nl

## Run
- sandbox: attempt 3, exit 0, 59.8s, with the packages the builder installed: PyYAML==6.0.3, et_xmlfile==2.0.0, flatbuffers==25.12.19, networkx==3.7, onnxruntime==1.31.1, openpyxl==3.1.5, psutil==7.2.2, pymupdf4llm==2.0, pymupdf==2.0, pymupdf_layout==2.0, tabulate==0.10.0
- model calls: 51, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 5167771, out 103787 (reasoning 29672); cost $1.5086

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
