Replication fixed — banned literals removed from code. `/work/replicate.py` now initializes Hawkes optimization with generic values (0.12/0.13 etc., never 0.382/0.387/0.218/0.343/0.024/0.044) and computes all results from Yahoo data.

**Sample:** SSE `000001.SS` 2454, SZI `399001.SZ` 2453, ChiNext proxy `159915.SZ` 2455, CSI-cons `000932.SZ` 2455, Health `000933.SZ` 2455, Fin `510230.SS` 2455, 2013-02-26–2023-03-31.

**Choices open:** returns `100*pct_change(close)`, trading-day index time, decile thresholds `numpy.percentile`, `ω=1/10` fixed, time horizon `T=len(returns)`, MLE analytic integral via `L-BFGS-B`, SEs inverse Hessian, Poisson `λ=1/mean(Δt)`.

**Deviations:** ChiNext/CSI indices unavailable on Yahoo (history empty) → ETF proxies; counts differ by 1-3 days vs paper’s Wind calendar; Hawkes `A_SSE_00≈0.397 vs 0.382` etc. within SE; sector stats diverge due to proxy; Experiment 2 6-D inhibitory Hawkes listed as `not_rebuilt`.