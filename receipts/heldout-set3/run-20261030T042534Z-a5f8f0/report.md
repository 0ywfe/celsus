We could not check this paper: the replication's sample covers 2001-01 to 2025-12, but the paper's runs from January 2001 to July 2026. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2609.35011
**Price Stability in the European Union: A Systemic Approach Using Random Matrix Theory**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| n_countries | count | 27 countries | 27 |  | 27 | True | precise: the paper's count |
| n_observations | count | 307 monthly observations | 300 |  | 300 | True | approximate: -2.3%, within SCORE's +/-15% |
| lambda_minus_opt | estimate | 37.21 eigenvalue units | 29.87 | 9.547 | 27 | True | paper inside 29.87 +/- 18.71 |
| sigma_mp | estimate | 0.2 not stated | 0.1819 | 0.02563 | 27 | True | paper inside 0.1819 +/- 0.05024 |
| alpha_info_corr | estimate | 1.82 not stated | 1.793 | 0.0594 | 27 | True | paper inside 1.793 +/- 0.1164 |
| D_KS_opt | estimate | 0.1 distance | 0.1003 | 0.01135 | 27 | True | paper inside 0.1003 +/- 0.02224 |
| pareto_mu | estimate | 1.64 not stated | 1.585 | 0.1188 | 27 | True | paper inside 1.585 +/- 0.2328 |
| corr_kappa_D_E | estimate | 0.988 correlation | 0.9829 | 0.02021 | 85 | True | paper inside 0.9829 +/- 0.03962 |
| corr_system_HICP_2019_2026 | estimate | -0.824 correlation | 0.8678 | 0.05488 | 84 | False | paper outside 0.8678 +/- 0.1076 |
| nnsd_cutoff | estimate | 0.356 correlation | 0.355 | 0.02 | 27 | True | paper inside 0.355 +/- 0.0392 |
| n_communities_leading_eig | tally | 6 communities | 2 |  | 27 |  | a tally of what the analysis found, with no uncertainty, so it is not judged |
| n_eastEurope_claimed | tally | 5 countries | 5 |  |  |  | a tally of what the analysis found, with no uncertainty, so it is not judged |
| n_eastEurope_listed | tally | 6 countries | 6 |  |  |  | a tally of what the analysis found, with no uncertainty, so it is not judged |
| price_stability_target | parameter | 2 year-on-year HICP | 2 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| alpha_ideal_benchmark | parameter | 2 alpha units | 2 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| alpha_underfit_low | parameter | 2 alpha units | 2 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| alpha_underfit_high | parameter | 6 alpha units | 6 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| alpha_overfit_threshold | parameter | 2 alpha units | 2 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| lambda_minus_underfit_thresh | parameter | 200 eigenvalue units | 200 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim lambda_minus_perf_low = 100: not in the paper's LaTeX
- rejected claim lambda_minus_perf_high = 160: not in the paper's LaTeX
- rejected claim p_KS = not stated: not a number
- rejected claim p_NNSD = not stated: not a number
- spec: the headline was written as prose ('Main conclusion rests on alpha_info_corr = 1.82 (slightly overfitted vs benchmark alpha_ideal_benchmark =2), D_KS_opt =0'); chosen from the claim names: alpha_info_corr
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (lambda_minus_opt (37.21) at line 395, alpha_info_corr (1.82) at line 397, pareto_mu (1.64) at line 399, corr_kappa_D_E (0.988) at line 400, corr_system_HICP_2019_2026 (-0.824) at line 401, nnsd_cutoff (0.356) at line 402). Compute each result from the data; the paper's value never goes into it.
- round 3: audit sent the sample back: the replication's sample covers 2001-01 to 2025-12, but the paper's runs from January 2001 to July 2026
- sample: the replication's sample covers 2001-01 to 2025-12, but the paper's runs from January 2001 to July 2026
- sample: the sample differs from the paper's by 7 missing and 0 extra observations (2.3% of the paper's 307, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Used Eurostat API dataset prc_hicp_mmor as public equivalent of paper custom dataset; WeightWatcher/powerlaw for MP Power-law fit; condition numbers on raw W^T W; NNSD denoising via absolute correlation threshold and GOE/Exp NLL; community detection via igraph leading eigenvector

## Data sources
- market data: none used
- other hosts the script fetched from: ec.europa.eu

## Run
- sandbox: attempt 3, exit 0, 39.8s, with the packages the builder installed: cloudpickle==3.1.2, contourpy==1.4.0, cycler==0.12.1, fonttools==4.68.0, igraph==1.0.0, joblib==1.6.0, kiwisolver==1.5.1, matplotlib-inline==0.2.2, matplotlib==3.11.2, mpmath==1.4.1, networkx==3.7, pillow==13.0.0, powerlaw==2.0.0, pyparsing==3.3.3, python-igraph==1.0.0, safetensors==0.8.0, scikit-learn==1.9.1, texttable==1.7.2, threadpoolctl==3.7.0, tqdm==4.70.1, traitlets==5.16.1, weightwatcher==0.7.7
- model calls: 44, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 2089576, out 74037 (reasoning 36662); cost $0.7452

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
