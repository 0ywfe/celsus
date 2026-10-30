We could not check this paper: the replication's sample covers 1996-06-01 to 2024-06-30, but the paper's runs from June 1996 (Table says mid-1997; text says June 1996 for BRK/WMT; July 2019 for CVS) to May 2024 (monthly BRK/WMT); Jun 2024 (daily CVS) (Table says 2024). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2605.20142
**Mining Financial Data using Mixtures of Mirrored Weibull Distributions - Replication Spec**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| stocks_Brk_min | estimate | -15.39 log return % | -15.39 | 0 | 335 | True | rounds to the printed -15.39 |
| stocks_Wmt_min | estimate | -23.24 log return % | -23.31 | 0 | 335 | True | 0.3% apart, within 10% |
| stocks_Cvs_min | estimate | -10.34 log return % | -10.34 | 0 | 1257 | True | rounds to the printed -10.34 |
| stocks_Brk_max | estimate | 23.42 log return % | 23.42 | 0 | 335 | True | rounds to the printed 23.42 |
| stocks_Wmt_max | estimate | 23.58 log return % | 23.45 | 0 | 335 | True | 0.5% apart, within 10% |
| stocks_Cvs_max | estimate | 18.44 log return % | 18.44 | 0 | 1257 | True | rounds to the printed 18.44 |
| stocks_Brk_mean | estimate | 0.89 log return % | 0.8951 | 0.2974 | 335 | True | paper inside 0.8951 +/- 0.5829 |
| stocks_Wmt_mean | estimate | 0.93 log return % | 0.9552 | 0.3296 | 335 | True | paper inside 0.9552 +/- 0.646 |
| stocks_Cvs_mean | estimate | 0 log return % | -0.01735 | 0.05193 | 1257 | True | paper inside -0.01735 +/- 0.1018 |
| stocks_Brk_sd | estimate | 5.44 log return % | 5.444 | 0.2103 | 335 | True | paper inside 5.444 +/- 0.4122 |
| stocks_Wmt_sd | estimate | 6.01 log return % | 6.033 | 0.2331 | 335 | True | paper inside 6.033 +/- 0.4568 |
| stocks_Cvs_sd | estimate | 1.85 log return % | 1.841 | 0.03672 | 1257 | True | paper inside 1.841 +/- 0.07197 |
| stocks_Brk_skew | estimate | -0.01 | -0.008894 | 0.1338 | 335 | True | paper inside -0.008894 +/- 0.2623 |
| stocks_Wmt_skew | estimate | -0.16 | -0.1654 | 0.1338 | 335 | True | paper inside -0.1654 +/- 0.2623 |
| stocks_Cvs_skew | estimate | 1.32 | 1.312 | 0.06909 | 1257 | True | paper inside 1.312 +/- 0.1354 |
| stocks_Brk_kurt | estimate | 4.22 | 4.221 | 0.2677 | 335 | True | paper inside 4.221 +/- 0.5246 |
| stocks_Wmt_kurt | estimate | 4.45 | 4.41 | 0.2677 | 335 | True | paper inside 4.41 +/- 0.5246 |
| stocks_Cvs_kurt | estimate | 17.36 | 17.89 | 0.1382 | 1257 | False | paper outside 17.89 +/- 0.2708 |
| Brk_empirical_VaR_5 | estimate | -13.46 log return % | -13.46 | 0 | 335 | True | rounds to the printed -13.46 |
| Brk_empirical_VaR_1 | estimate | -8.66 log return % | -8.623 | 0 | 335 | True | 0.4% apart, within 10% |
| Brk_VaR_5_GMM | estimate | -11.74 log return % | -11.74 | 0 | 335 | True | rounds to the printed -11.74 |
| Brk_LR_POF_5_GMM | estimate | 3.06 | 3.058 |  | 335 |  | no standard error |
| Brk_p_POF_5_GMM | estimate | 0.08 | 0.08036 |  | 335 |  | no standard error |
| Brk_LR_IND_5_GMM | estimate | 0.3 | 0.2997 |  | 335 |  | no standard error |
| Brk_p_IND_5_GMM | estimate | 0.58 | 0.5841 |  | 335 |  | no standard error |
| Brk_VaR_5_tMM | estimate | -12.99 log return % | -12.02 | 0 | 335 | True | 7.4% apart, within 10% |
| Brk_LR_POF_5_tMM | estimate | 0.71 | 3.058 |  | 335 |  | no standard error |
| Brk_p_POF_5_tMM | estimate | 0.4 | 0.08036 |  | 335 |  | no standard error |
| Brk_LR_IND_5_tMM | estimate | 0.15 | 0.2997 |  | 335 |  | no standard error |
| Brk_p_IND_5_tMM | estimate | 0.7 | 0.5841 |  | 335 |  | no standard error |
| Brk_VaR_5_MMW | estimate | -13.43 log return % | -14.1 | 0 | 335 | True | 5.0% apart, within 10% |
| Brk_LR_POF_5_MMW | estimate | 0.12 | 0.03828 |  | 335 |  | no standard error |
| Brk_p_POF_5_MMW | estimate | 0.73 | 0.8449 |  | 335 |  | no standard error |
| Brk_LR_IND_5_MMW | estimate | 0.1 | 0.05438 |  | 335 |  | no standard error |
| Brk_p_IND_5_MMW | estimate | 0.76 | 0.8156 |  | 335 |  | no standard error |
| Brk_VaR_1_GMM | estimate | -8.08 log return % | -8.046 | 0 | 335 | True | 0.4% apart, within 10% |
| Brk_LR_POF_1_GMM | estimate | 0.63 | 0.6267 |  | 335 |  | no standard error |
| Brk_p_POF_1_GMM | estimate | 0.43 | 0.4286 |  | 335 |  | no standard error |
| Brk_LR_IND_1_GMM | estimate | 8.41 | 8.389 |  | 335 |  | no standard error |
| Brk_p_IND_1_GMM | estimate | 0 | 0.003776 |  | 335 |  | no standard error |
| Brk_VaR_1_tMM | estimate | -7.81 log return % | -7.818 | 0 | 335 | True | 0.1% apart, within 10% |
| Brk_LR_POF_1_tMM | estimate | 0.63 | 0.6267 |  | 335 |  | no standard error |
| Brk_p_POF_1_tMM | estimate | 0.43 | 0.4286 |  | 335 |  | no standard error |
| Brk_LR_IND_1_tMM | estimate | 8.41 | 8.389 |  | 335 |  | no standard error |
| Brk_p_IND_1_tMM | estimate | 0 | 0.003776 |  | 335 |  | no standard error |
| Brk_VaR_1_MMW | estimate | -8.66 log return % | -8.457 | 0 | 335 | True | 2.3% apart, within 10% |
| Brk_LR_POF_1_MMW | estimate | 0 | 0.3055 |  | 335 |  | no standard error |
| Brk_p_POF_1_MMW | estimate | 0.95 | 0.5805 |  | 335 |  | no standard error |
| Brk_LR_IND_1_MMW | estimate | 3.81 | 5.666 |  | 335 |  | no standard error |
| Brk_p_IND_1_MMW | estimate | 0.05 | 0.0173 |  | 335 |  | no standard error |
| Wmt_empirical_VaR_1 | estimate | -16.31 log return % | -16.31 | 0 | 335 | True | rounds to the printed -16.31 |
| Wmt_VaR_1_GMM | estimate | -13.08 log return % | -13.05 | 0 | 335 | True | 0.2% apart, within 10% |
| Wmt_LR_POF_1_GMM | estimate | 3.06 | 3.058 |  | 335 |  | no standard error |
| Wmt_p_POF_1_GMM | estimate | 0.08 | 0.08036 |  | 335 |  | no standard error |
| Wmt_LR_IND_1_GMM | estimate | 0.3 | 0.2997 |  | 335 |  | no standard error |
| Wmt_p_IND_1_GMM | estimate | 0.58 | 0.5841 |  | 335 |  | no standard error |
| Wmt_VaR_1_tMM | estimate | -14.32 log return % | -13.29 | 0 | 335 | True | 7.2% apart, within 10% |
| Wmt_LR_POF_1_tMM | estimate | 1.71 | 1.715 |  | 335 |  | no standard error |
| Wmt_p_POF_1_tMM | estimate | 0.19 | 0.1904 |  | 335 |  | no standard error |
| Wmt_LR_IND_1_tMM | estimate | 0.22 | 0.2195 |  | 335 |  | no standard error |
| Wmt_p_IND_1_tMM | estimate | 0.64 | 0.6394 |  | 335 |  | no standard error |
| Wmt_VaR_1_MMW | estimate | -16.26 log return % | -16.97 | 0 | 335 | True | 4.3% apart, within 10% |
| Wmt_LR_POF_1_MMW | estimate | 0.12 | 0.03828 |  | 335 |  | no standard error |
| Wmt_p_POF_1_MMW | estimate | 0.73 | 0.8449 |  | 335 |  | no standard error |
| Wmt_LR_IND_1_MMW | estimate | 0.1 | 0.05438 |  | 335 |  | no standard error |
| Wmt_p_IND_1_MMW | estimate | 0.76 | 0.8156 |  | 335 |  | no standard error |
| Cvs_MSE_GMM | estimate | 1.21 | 0.8322 | 0 | 1007 | False | 31.2% apart, beyond 10% |
| Cvs_MSE_tMM | estimate | 0.6 | 1.507 | 0 | 1007 | False | 151.2% apart, beyond 10% |
| Cvs_MSE_MMW | estimate | 0.18 | 1.55 | 0 | 1007 | False | 761.2% apart, beyond 10% |
| Cvs_failure_rate_GMM | tally | 0.25 | 0.01291 | 0 | 1007 | False | 94.8% apart, beyond 10% |
| Cvs_failure_rate_tMM | tally | 0.03 | 0.008937 | 0 | 1007 | False | 70.2% apart, beyond 10% |
| Cvs_failure_rate_MMW | tally | 0 | 0.01192 | 0 | 1007 | False | inf% apart, beyond 10% |

## The paper's own numbers
- nothing to check

## Guards
- no claims rejected
- spec: the headline was written as prose ('Paper's conclusion rests on MMW being closest to empirical and lowest error:\n - stocks_Brk_mean etc are descriptive, he'); chosen from the claim names: Brk_VaR_1_MMW
- spec: the headline was written as prose ('Brk_VaR_1_MMW (example: MMW VaR 1% passes both tests and matches empirical; alternative headline claims are Wmt_VaR_1_MM'); chosen from the claim names: Brk_VaR_1_MMW
- round 1: the builder ran out of turns
- round 1: rejected before the clean run: the script does not compile: line 255: expected '(': def fit_gmm VaR(returns, alphas):.
- round 2: audit sent the sample back: the replication could not rebuild the paper's sample (Paper does not print per-stock n; period ambiguity prevents exact missing/extra count)
- round 3: audit sent the sample back: the replication's sample covers 1996-06-01 to 2024-06-30, but the paper's runs from June 1996 (Table says mid-1997; text says June 1996 for BRK/WMT; July 2019 for CVS) to May 2024 (monthly BRK/WMT); Jun 2024 (daily CVS) (Table says 2024)
- sample: the replication's sample covers 1996-06-01 to 2024-06-30, but the paper's runs from June 1996 (Table says mid-1997; text says June 1996 for BRK/WMT; July 2019 for CVS) to May 2024 (monthly BRK/WMT); Jun 2024 (daily CVS) (Table says 2024)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 1927, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: BRK proxied by BRK-B (Berkshire Hathaway Inc. Class B, yfinance BRK-B; BRK.A/BRK.B tickers have no full history via yfinance; BRK-B summary stats match paper exactly: min -15.39 max 23.42 etc.); monthly via ME resample last adj_close; log returns as 100*log(Pt/Pt-1); kurtosis Pearson (paper reports biased version used for matching); CVS sign in table appears as loss=-return, replication reports negated series to match magnitude; GMM via sklearn GaussianMixture BIC 1..4, tMM via weighted t per component, MMW via EM implementing paper eq (5)-(7) with KMeans init, BIC selection, quantile via CDF inversion

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 3 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 3, exit 0, 272.2s, with the packages the builder installed: cloudpickle==3.1.2, joblib==1.6.0, scikit-learn==1.9.1, threadpoolctl==3.7.0
- model calls: 54, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 2860174, out 115564 (reasoning 53635); cost $1.0746

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
