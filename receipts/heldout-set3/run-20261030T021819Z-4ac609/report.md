We could not check this paper: the replication never produced results. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2610.10043
**Building Macroeconomically Relevant Climate Indices via the Assemblage VAR (Barrette, Goulet Coulombe, Reinicke, draft 09-22-26)**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| ip_peak_benchmark_0_16pct | estimate | 0.16 percent cumulative log INDPRO |  |  |  |  | not computed |
| ip_kim_matthes_phan_0_15pp | estimate | 0.15 percentage-point |  |  |  |  | not computed |
| ip_peak_assembled_low_0_24pct | estimate | 0.24 percent |  |  |  |  | not computed |
| ip_peak_assembled_high_0_32pct | estimate | 0.32 percent |  |  |  |  | not computed |
| weight_national_T10_0pct | estimate | 0 percent of total weight |  |  |  |  | not computed |
| weight_national_sealevel_0pct | estimate | 0 percent |  |  |  |  | not computed |
| weight_national_WP90_65pct | estimate | 65 percent |  |  |  |  | not computed |
| weight_regional_WP90_agg_40pct | estimate | 40 percent |  |  |  |  | not computed |
| weight_regional_WP90_midwest_global_29pct | estimate | 29 percent |  |  |  |  | not computed |
| weight_regional_T90_SWpacific_16pct | estimate | 16 percent |  |  |  |  | not computed |
| weight_regional_T90_CWpacific_2pct | estimate | 2 percent |  |  |  |  | not computed |
| weight_regional_Rx5Day_25pct | estimate | 25 percent |  |  |  |  | not computed |
| weight_regional_wind_own_region_35pct | estimate | 35 percent within region |  |  |  |  | not computed |
| weight_noaa_thermal_block_36pct | estimate | 36 percent |  |  |  |  | not computed |
| weight_noaa_hydro_block_27pct | estimate | 27 percent |  |  |  |  | not computed |
| weight_noaa_rank_left_max_2_95pct | estimate | 2.95 percent per rank |  |  |  |  | not computed |
| weight_noaa_rank_right_max_2_58pct | estimate | 2.58 percent per rank |  |  |  |  | not computed |
| weight_rank_flat_1_2pct | estimate | 1.2 percent per rank |  |  |  |  | not computed |
| weight_noaa_rank_interior_3pct | estimate | 3 percent |  |  |  |  | not computed |
| weight_expanding_national_WP90_avg_70pct | estimate | 70 percent |  |  |  |  | not computed |
| weight_expanding_national_WP90_min_63pct | estimate | 63 percent |  |  |  |  | not computed |
| weight_expanding_national_T90_start_24pct | estimate | 24 percent |  |  |  |  | not computed |
| weight_expanding_national_T90_end_22pct | estimate | 22 percent |  |  |  |  | not computed |
| weight_expanding_national_Rx5Day_start_12pct | estimate | 12 percent |  |  |  |  | not computed |
| weight_expanding_national_Rx5Day_end_15pct | estimate | 15 percent |  |  |  |  | not computed |
| weight_expanding_national_Rx5Day_collapse_2pct | estimate | 2 percent |  |  |  |  | not computed |
| weight_expanding_regional_WP90_start_37pct | estimate | 37 percent |  |  |  |  | not computed |
| weight_expanding_regional_WP90_end_40pct | estimate | 40 percent |  |  |  |  | not computed |
| weight_expanding_regional_Rx5Day_start_35pct | estimate | 35 percent |  |  |  |  | not computed |
| weight_expanding_regional_Rx5Day_end_23pct | estimate | 23 percent |  |  |  |  | not computed |
| weight_expanding_regional_T10_start_1pct | estimate | 1 percent |  |  |  |  | not computed |
| weight_expanding_regional_T10_end_8pct | estimate | 8 percent |  |  |  |  | not computed |
| weight_expanding_noaa_temp_start_23pct | estimate | 23 percent |  |  |  |  | not computed |
| weight_expanding_noaa_temp_end_32pct | estimate | 32 percent |  |  |  |  | not computed |
| weight_expanding_noaa_HDD_start_8pct | estimate | 8 percent |  |  |  |  | not computed |
| weight_expanding_noaa_HDD_end_19pct | estimate | 19 percent |  |  |  |  | not computed |
| weight_expanding_noaa_precip_start_26pct | estimate | 26 percent |  |  |  |  | not computed |
| weight_expanding_noaa_precip_end_18pct | estimate | 18 percent |  |  |  |  | not computed |
| weight_expanding_noaa_PalmerZ_start_21pct | estimate | 21 percent |  |  |  |  | not computed |
| weight_expanding_noaa_PalmerZ_end_16pct | estimate | 16 percent |  |  |  |  | not computed |
| bootstrap_index_central_88pct | estimate | 88 percent of time periods |  |  |  |  | not computed |
| bootstrap_index_central_99pct | estimate | 99 percent |  |  |  |  | not computed |
| rank_usage_HDD_14pct | estimate | 14 percent deviation from equal weight |  |  |  |  | not computed |
| rank_usage_temp_13pct | estimate | 13 percent deviation |  |  |  |  | not computed |
| rank_usage_residual_minus7pct | estimate | -7 percent deviation |  |  |  |  | not computed |
| rank_usage_spearman_rho_0_80 | estimate | 0.8 correlation |  |  |  |  | not computed |
| count_national_panel_5 | count | 5 series |  |  |  |  | not computed |
| count_regional_panel_34 | count | 34 series |  |  |  |  | not computed |
| count_noaa_panel_82 | count | 82 series |  |  |  |  | not computed |
| count_aci_regions_7 | count | 7 regions |  |  |  |  | not computed |
| count_noaa_zones_10 | count | 10 zones |  |  |  |  | not computed |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim weight_noaa_rank_tails_three_quarters = three-quarters: not a number
- round 1: the builder ran out of turns
- round 2: rejected before the clean run: the code that writes these results contains the number the paper reports for them (ip_kim_matthes_phan_0_15pp (0.15 percentage-point) at line 238). Compute each result from the data; the paper's value never goes into it.
- round 3: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (count_noaa_panel_82 (82) at line 121). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.

## Data sources
- market data: none used
- other hosts the script fetched from: none

## Run
- sandbox: not run
- model calls: 63, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 5242121, out 101668 (reasoning 48923); cost $1.4346

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
