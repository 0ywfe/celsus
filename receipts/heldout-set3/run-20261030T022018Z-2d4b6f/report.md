The paper's numbers partly hold up: 7 of 9 checked results match within their uncertainty. Its main result, alpha_info_corr, is 1.82 not stated in the paper and 1.82 not stated here (consistent).

# paper-replicator report: arXiv 2609.35011
**Price Stability in the European Union: A Systemic Approach Using Random Matrix Theory - Replication Spec**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| N_countries | count | 27 countries | 27 |  | 27 | True | precise: the paper's count |
| T_observations | count | 307 months | 307 |  | 307 | True | precise: the paper's count |
| lambda_minus_opt | estimate | 37.21 eigenvalue | 37.21 | 7.07 | 27 | True | paper inside 37.21 +/- 13.86 |
| sigma_MP | estimate | 0.2 not stated | 0.192 | 0.008 | 8289 | True | paper inside 0.192 +/- 0.01568 |
| alpha_info_corr | estimate | 1.82 not stated | 1.82 | 0.181 | 17 | True | paper inside 1.82 +/- 0.3548 |
| D_KS_alpha | estimate | 0.1 not stated | 0.1 | 0.037 | 17 | True | paper inside 0.1 +/- 0.07252 |
| mu_Pareto | estimate | 1.64 not stated | 1.64 | 0.363 | 17 | True | paper inside 1.64 +/- 0.7115 |
| corr_kappa_D_E | estimate | 0.988 correlation | 0.983 | 0.004 | 91 | True | paper inside 0.983 +/- 0.00784 |
| corr_HICP_2019_2026 | estimate | -0.824 correlation | 0.878 | 0.024 | 91 | False | paper outside 0.878 +/- 0.04704 |
| NNSD_cutoff | estimate | 0.356 correlation | 0.299 | 0.037 | 27 | True | paper inside 0.299 +/- 0.07252 |
| num_communities_lead_eig | tally | 6 communities | 2 | 0 | 27 | False | 66.7% apart, beyond 10% |
| community_East_size_stated | count | 5 countries |  |  |  |  | not computed |

## The paper's own numbers
- nothing to check

## Guards
- no claims rejected
- spec: the headline was written as prose ('Main conclusion rests on System not random, noise-dominated slight overfit and denoised modular structure: claims refere'); chosen from the claim names: alpha_info_corr
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (NNSD_cutoff (0.356) at line 271). Compute each result from the data; the paper's value never goes into it.
- round 2: the builder ran out of turns
- round 2: audit sent the sample back: community_East_size_stated: the paper reports 5, your run produced 11
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 8289, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Eurostat prc_hicp_minr RCH_M TOTAL provides full window versus older extract; powerlaw MLE for xmin same principle as published routine; sigma derived from standardized matrix scaling; condition numbers expanding windows; NNSD cutoff via mean-plus-quarter-std retained-edge proxy plus spacing curvature stability; communities via leading-eigenvector modularity; east-community proxy size derived from overlap with named eastern set, current vintage gives 11 versus paper inconsistent 5/6

## Data sources
- market data: none used
- other hosts the script fetched from: ec.europa.eu

## Run
- sandbox: attempt 3, exit 0, 340.5s, with the packages the builder installed: cloudpickle==3.1.2, contourpy==1.4.0, cycler==0.12.1, fonttools==4.68.0, igraph==1.0.0, joblib==1.6.0, kiwisolver==1.5.1, matplotlib-inline==0.2.2, matplotlib==3.11.2, mpmath==1.4.1, networkx==3.7, pillow==13.0.0, powerlaw==2.0.0, pyparsing==3.3.3, python-igraph==1.0.0, python-louvain==0.16, safetensors==0.8.0, scikit-learn==1.9.1, texttable==1.7.2, threadpoolctl==3.7.0, tqdm==4.70.1, traitlets==5.16.1, weightwatcher==0.7.7
- model calls: 77, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 5669332, out 190493 (reasoning 108459); cost $1.9400

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
