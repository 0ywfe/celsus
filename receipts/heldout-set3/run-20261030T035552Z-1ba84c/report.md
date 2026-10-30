We could not check this paper: the run stopped (BudgetExceeded). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2601.10279
**Selecting and Testing Asset Pricing Models: A Stepwise Approach (Management Science, first draft Apr 2023 this draft Jan 2026)**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|

## The paper's own numbers
- OK: 97 candidate factors into 23 core (FF6/Q5/DHS3/BS6/BAB/QMJ etc) and 74 HXZ factors: 23 + 74 = 97, paper's total 97
- OK: 285 basis portfolios by 11 bivariate sorts on size + characteristic: 25 + 25 + 25 + 25 + 25 + 25 + 25 + 25 + 25 + 35 + 25 = 285, paper's total 285
- FLAG: individual factor testing 96 two-factor baselines MKT+row (97-1) and 94 four-factor baselines FF3+row (97-3): 96 + 94 = 190, paper's total 97
- NOTE: HDA for expanded efficient CAPM^F H0 alpha=0 for remaining N1=89 unselected factors, HDA 1.28 p 0.101 not rejected at 5% (also GRS 1.60 p 0.001, FF3^F HDA 1.28 p 0.100, FF6^F HDA 1.12 p 0.131 etc Panel B all not rejected at 5% HDA): t = 1.28, paper's p = 0.101 matches one-sided (upper tail) (0.1003); two-sided p would be 0.2005
- NOTE: Pairwise equality of SR2 Barillas et al.2020, nested case GRS, non-nested SR2 diff test, models sorted by SR2; CAPM vs M8 SR2 diff 0.60 p 0.01 *** , FF3 vs M8 0.59 ***, Q5 vs M8 0.27 *** all significant at 1%, Table model_comparison_sr; M8 99.8% Best OOS bootstrap vs Q5 0.2%: t = 0.6 and p = 0.01 fit no side at the printed precision (two-sided p would be 0.5487); judged two-sided
- NOTE: Q5 vs M8 SR2 diff 0.27 p 0.01 *** confirms M8 spans investment opportunity set best, OOS M-SR2 0.56 vs Q5 0.32 INS 0.65 vs 0.36: t = 0.27 and p = 0.01 fit no side at the printed precision (two-sided p would be 0.7872); judged two-sided

## Guards
- rejected claim T_minus_N_491_count = 491: not in the paper's LaTeX
- rejected claim T_Time2_196_count = 196: printed once in the paper's LaTeX, and already claimed by T_Time1_196_count
- rejected claim T_Time3_196_count = 196: printed once in the paper's LaTeX, and already claimed by T_Time1_196_count
- rejected claim z_1.645_parameter = 1.645: not in the paper's LaTeX
- spec: the headline was written as prose ('Expanded efficient CAPM^F with 8 factors MKT REG PEAD HMLM STR ILR SMB EPRD is not rejected by HDA (HDA 1.28 p 0.101) ve'); chosen from the claim names: CAPM_F_pHDA_0.101
- round 1: the builder ran out of turns
- round 1: rejected before the clean run: the script does not compile: line 979: unmatched ')': w_train = w_train / np.sum(np.abs(w_train)) if np.sum(np.abs(w_train))!=0 else 1).
- run stopped: BudgetExceeded: spent $2.0194 of a $2.0000 budget

## Data sources
- market data: none used
- other hosts the script fetched from: none

## Run
- sandbox: not run
- model calls: 64, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 7465317, out 149943 (reasoning 77349); cost $2.0194

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
