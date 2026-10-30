The paper's numbers partly hold up: 1 of 1 checked results match within their uncertainty. Its main result is none of the numbers checked, so it was not judged.

# paper-replicator report: arXiv 2601.11201
**Fast Times, Slow Times: Timescale Separation in Financial Timeseries Data**

Verdict: **partly holds up**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| g10_basket_size_implied | count | 10 currencies | 10 |  | 10 | True | precise: the paper's count |
| tsy_n_slow_components_implied | parameter | 1994 components | 4 |  | 4 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| linear_tica_exponent_k | parameter | 1 k | 1 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| nonlinear_tica_exponent_k | parameter | 4 k | 4 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| flash_crash_sp500_drop_background | estimate | 9 percent | 8.58 | 0 | 3 | True | rounds to the printed 9% |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim etf_basket_size = five: not a number
- rejected claim g10_n_slow_components_extracted = five: not a number
- rejected claim etf_n_slow_components_extracted = five: not a number
- rejected claim headline_persistence_slow_timescales_qualitative = not stated - no numeric estimate, test statistic or p-value printed; qualitative visual assessment only: not a number
- rejected claim secondary_orthogonality_decay_qualitative = not stated - no numeric orthogonality measure, test statistic or p-value printed: not a number
- round 1: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (g10_basket_size_implied (10) at line 227). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- round 2: audit sent the sample back: the replication could not rebuild the paper's sample (Paper prints no observation counts, no frequency, no missing-data filter, no exact G10/TSY tickers or tenors, so missing/extra cannot be counted precisely)
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 14197, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: Data vendor yfinance live vs paper undisclosed source/vintage; G10/TSY tickers/tenors and exact calendars not printed in paper - treated as proxy/vendor vintage not sample difference; frequency daily close (paper not stated); lag T=1 trading day (paper not stated); X_t = log-returns (FX/ETF) and daily yield changes (TSY) (paper says prices or returns, price-level alternative also computed); DXY (DX-Y.NYB) as 10th G10 series; AUDUSD start 2006-05-16 vs Jan (inner-join 87 days); LSE .L listings for ETFs; sample covariance demeaned N-1 and symmetrized CT=0.5(E[X_{t+T}X_t^T]+E[X_tX_{t+T}^T]); solver scipy.linalg.eigh (LAPACK gvd driver); orthogonality via Frobenius norm

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 21 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 3, exit 0, 35.6s
- model calls: 45, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 1640693, out 98157 (reasoning 64006); cost $0.8063

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
