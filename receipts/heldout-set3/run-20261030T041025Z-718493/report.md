The paper's numbers partly hold up: 2 of 3 checked results match within their uncertainty. Its main result, surgery_curvature_0, is 0 curvature in the paper and 0 curvature here (not judged: a parameter the paper sets in its method, not a result). Sample size not rebuilt: the script writes it as a fixed number (101 at line 302), not counted from the data (n_total_100, 100 in the paper).

# paper-replicator report: arXiv 2510.15942
**Intrinsic Geometry of the Stock Market from Graph Ricci Flow - Replication Spec**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| n_total_100 | count | 100 stocks/nodes | 101 |  | 101 |  | the script writes it as a fixed number (101 at line 302), so it is not judged |
| period_window_5_years | parameter | 5 years | 5 |  | 1231 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| corr_38_percent | estimate | 38% | 37.99 | 0.2165 | 4753 | True | paper inside 37.99 +/- 0.4244 |
| avg_edge_weight_1_11 | estimate | 1.11 distance | 1.105 | 0.002023 | 4753 | False | paper outside 1.105 +/- 0.003964 |
| median_edge_weight_1_11 | estimate | 1.11 distance | 1.111 | 0.002023 | 4753 | True | paper inside 1.111 +/- 0.003964 |
| alpha_lazy_1_2 | parameter | 1 probability | 0.5 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_complete_0_505 | parameter | 0.505 curvature | 0.5051 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lin_lu_yau_limit_n_over_n_minus1 | parameter | -1 curvature/(1-alpha) | 1.01 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| laplacian_eigenvalue_0 | parameter | 0 eigenvalue | 0 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| laplacian_eigenvalue_n_over_n_minus1 | parameter | -1 eigenvalue | 1.01 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| curvature_lower_theoretical_minus2 | parameter | -2 curvature | -2 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| curvature_upper_theoretical_1 | parameter | 1 curvature | 1 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_min_formula | parameter | 2 curvature | -1.96 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_min_equal_weights | parameter | 2 curvature | -1.96 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| kappa_min_nasdaq_minus1_96 | parameter | -1.96 curvature | -1.96 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| edge_length_theoretical_2_96 | parameter | 2.96 distance | 2.96 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ricci_iter_5 | parameter | 5 iterations | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ricci_iter_10 | parameter | 10 iterations | 10 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| ricci_iter_20 | parameter | 20 iterations | 20 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| surgery_curvature_0 | parameter | 0 curvature | 0 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| postflow_edge_weight_3 | estimate | 3 distance |  |  |  |  | not computed |
| level1_cluster_66 | tally | 66 stocks |  |  |  |  | not computed |
| level1_cluster_35_a | tally | 35 stocks |  |  |  |  | not computed |
| level2_parent_50 | tally | 50 stocks |  |  |  |  | not computed |
| level2_semicond_16 | tally | 16 stocks |  |  |  |  | not computed |
| level3_outlier_10 | tally | 10 stocks |  |  |  |  | not computed |
| level3_remainder_40 | tally | 40 stocks |  |  |  |  | not computed |
| level4_biotech_4 | tally | 4 stocks |  |  |  |  | not computed |
| level4_supermicro_1 | tally | 1 stocks |  |  |  |  | not computed |
| level5_parent_35_b | tally | 35 stocks |  |  |  |  | not computed |
| level5_bigtech_17 | tally | 17 stocks |  |  |  |  | not computed |
| level5_tesla_18 | tally | 18 stocks |  |  |  |  | not computed |
| other_branch_level2_healthstaples_10 | tally | 10 stocks |  |  |  |  | not computed |
| other_branch_level3_industrials_17 | tally | 17 stocks |  |  |  |  | not computed |

## The paper's own numbers
- FLAG: Level1 Ricci flow + surgery on full NASDAQ-100 (100 nodes) after 20 iterations along zero-curvature neckpinch. Note 66+35=101 as printed vs total 100 due to source count; preserved as printed; total claim is n_total_100=100.: 66 + 35 = 101, paper's total 100
- OK: Level2 split of 66-stock tech branch into 16 semiconductors and 50 remainder.: 16 + 50 = 66, paper's total 66
- OK: Level3 split of 50-stock parent into 10 outliers and 40 remainder.: 10 + 40 = 50, paper's total 50
- OK: Level4 split of 40-stock remainder into 4 biotech +1 Supermicro +35 remainder to be further split (40=4+1+35).: 4 + 1 + 35 = 40, paper's total 40
- OK: Level5 split of remaining 35-stock branch into 17 Big Tech and 18 Tesla group (17+18=35).: 17 + 18 = 35, paper's total 35

## Guards
- rejected claim other_branch_level3_staplesenergy_8 = 8: not in the paper's LaTeX
- spec problem unresolved: headline 'surgery_curvature_0' is a parameter the paper sets in its method, not a result
- round 1: the builder ran out of turns
- round 1: a reviewer found 1 breach of the integrity rules; first, rule 1: claim postflow_edge_weight_3 is kind estimate (observed edge-weight ~3 of flat zero-curvature links after 20 Ricci-flow iterations). Code never runs the 20-iteration Ricci flow (only sample_curvature_distribution for 15 edges, no w^{(l+1)}=(1-kappa)*d update). Value is set to theoretical 1-kappa_min_100 = 2.96 computed in compute_theoretical() from formula 2*(3-n)/(n-1), not from data flow, i.e. set to paper's ~3/theoretical bound. (`results.append({"name":"postflow_edge_weight_3","value":float(theo["edge_len_100"]),"se":None,"n":None})`)
- sample: the sample differs from the paper's by 3 missing and 1 extra observations (4.0% of the paper's 100, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Universe from Wikipedia Nasdaq-100 old revision 2024-11-15 (revid1257470804) HTML table 101 securities (Table 4, 102 rows inc header) which exactly matches all tickers in paper Appendix tables (101 vs paper claimed 100). Price source: market_data.get_prices cache first then yfinance live (adj_close). Returns: log returns (paper does not state simple vs log or price column; standard choice log on adj_close, daily frequency, mean/std over window, pairwise complete for short-history IPOs like ARM 300 days, GEHC 486 days, GFS 771 days, CEG 715 days). Correlation Pearson as defined. Edge weight w sqrt(2(1-C)). Curvature sampling uses uniform mass (1-alpha)/(n-1) with alpha=0.5 and Floyd-Warshall shortest path; full distribution not computed due to unspecified solver weighting (uniform vs strength-weighted masses) and computational cost; theoretical values (kappa_complete 0.505, bounds -2/1, kappa_min -1.96, edge length 2.96) computed via formulas
- caveat: sample size not rebuilt: the script writes it as a fixed number (101 at line 302), not counted from the data (n_total_100, 100 in the paper); the results are judged without it, so the paper gets at most "partly holds up"
- caveat: the sample block's not_rebuilt: other_branch_level3_staplesenergy_8 is no claim's name, so it excused nothing

## Data sources
- prices: yfinance (host) (cache), fetched 2026-10-29, 1 tickers
- prices: yfinance (host) (cache), fetched 2026-10-30, 3 tickers
- prices: yfinance (live, sandbox), fetched 2026-10-30, 97 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 2, exit 0, 55.5s
- model calls: 42, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 1500934, out 103998 (reasoning 76916); cost $0.8158

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
