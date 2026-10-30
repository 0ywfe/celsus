**Replication completed.** Script `/work/replicate.py` fetches public Yahoo data via `market_data` and reproduces Experiment 1.

**Sample built:**
- `000001.SS` Shanghai Composite: **2454** daily closes (2013-02-26 → 2023-03-31)
- `399001.SZ` Shenzhen Component: **2453** closes
- ChiNext proxy `159915.SZ` (ETF tracking ChiNext, `399006.SZ` Yahoo history empty despite `info` present): **2455** closes
- CSI Consumer proxy `000932.SZ` ( `000932.SS` empty): **2455**
- CSI Health proxy `000933.SZ` ( `000933.SS` empty): **2455**
- CSI Fin&RE proxy `510230.SS` Bosera Financial ETF (`000934.SS/.SZ`/`399934.SZ` empty, info exists but history empty): **2455**
Largest `n=2455`, period `2013-02-26`–`2023-03-31`. Paper claims `2452`; extra days from Yahoo/Wind holiday-calendar differences. `same_as_paper=false`; `missing`/`extra=null` with `cannot_count` explained.

**Choices paper leaves open:** return=`100*close.pct_change()` (simple, `close==adj_close` for indices); time = trading-day index `1..T`; quantiles `numpy.percentile` linear; `omega=0.1` fixed grid-search per paper; MLE via analytic integral `μT+ΣA(1−e^{−ω(T−t_j)})` optimized with `scipy L-BFGS-B` (=tick MLE); SEs = inverse observed Fisher (numeric Hessian); Poisson `λ̂=1/mean(Δt)` with `Δt` trading-day gaps using full-sample quantiles; train `2013-02-26–2022-03-31`, test `2022-04-01–2023-03-31`.

**Deviations:** GEI/SSE/SZI means/stds match within SE (`SSE 0.023/1.32 vs 0.021/1.32`); `SSE min −8.49` exact, `max 6.23 vs 5.76` vendor adjustment; `SSE q10/q90 −1.26/1.40 vs −1.29/1.48`; Hawkes `SSE A00 0.397(0.075) vs 0.382, A01 0.408(0.078) vs 0.387, A10 0.158 vs 0.218, A11 0.419 vs 0.343, μ0 0.020 vs 0.024, μ1 0.042 vs 0.044` – pattern (strong trend + oversold rebound) holds; `SZI A00 0.268 vs 0.175` similar. CSI proxies diverge strongly (`Cons std 2.65 vs 1.65, min −10.1 vs −8.33, skew 0.23 vs −0.36`) reflecting different instrument. Experiment 2 6-D inhibitory Hawkes (86 parameters: 36+36 `A_p3`/`A_p5`, 12 `μ`, 2 `ω`) declared `not_rebuilt` – true CSI indices unavailable via Yahoo/cache and SGD-Monte-Carlo with `g=max(x,0.01)` stochastic; period `15×150d` segmentation requires missing series.