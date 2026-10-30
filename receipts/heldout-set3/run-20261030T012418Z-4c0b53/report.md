We could not check this paper: none of the paper's results could be compared. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2601.11201
**Fast Times, Slow Times: Timescale Separation in Financial Timeseries Data**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| n_baskets | count | 3 baskets | 3 |  |  |  | the script writes it as a fixed number (3 at line 274), so it is not judged |
| n_etf_tickers | count | 5 tickers | 5 |  |  |  | the script writes it as a fixed number (5 at line 275), so it is not judged |

## The paper's own numbers
- nothing to check

## Guards
- rejected claim no_quantified_headline_estimate = not stated: not a number
- caveat: the replication used other sources or methods for the paper's observations: G10: yfinance daily spot closes for 9 G10 pairs vs USD (paper G10 list unspecified; using standard 9 USD-crosses covering G10 ex-USD). ETF: LSE listings .L (paper omits exchange; US tickers IFSU have no yfinance history; same iShares products on primary UK listing). TSY: yield indices ^IRX/^FVX/^TNX/^TYX (ETFs TLT/IEF start 2002 cannot cover 1994-1998 fit). X_t demeaned log price levels (FX/ETF) and yield levels (TSY) as primary – paper says prices or returns without per-basket choice; returns reported as robustness. Lag T=1d, sample mean covariance, ridge 1e-10, symmetric whitening, single random init FastICA (paper lag, estimator, init/tol not stated)
- caveat: sample size not rebuilt: the script writes it as a fixed number (5 at line 275), not counted from the data (n_etf_tickers, 5 in the paper); the results are judged without it, so the paper gets at most "partly holds up"

## Data sources
- prices: yfinance (live, sandbox), fetched 2026-10-30, 18 tickers
- other hosts the script fetched from: none

## Run
- sandbox: attempt 1, exit 0, 41.8s
- model calls: 22, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 474139, out 67118 (reasoning 42376); cost $0.4292

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
