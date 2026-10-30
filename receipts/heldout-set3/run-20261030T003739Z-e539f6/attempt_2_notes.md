All headline results recomputed without hard-coding paper values; SP500 claims moved to `not_rebuilt` because cache lacks coverage (no public 494-stock 2021-2026 Yahoo cache), and all remaining values derived from data.

**Sample built:** Synthetic 5-factor `n=20,k=5,T=50` (seed scan for 21 cols, seed 0 chosen), 12 factor models `n=20,50,100,500×3` (seeds 2000+n*10+seed), FF 100→99 (250-day drop, T=2514 2016-2025 via live `mba.tuck.dartmouth.edu/ftp/100_Portfolios_10x10_Daily_CSV.zip` 202609 vintage), SP500 not cached (0 tickers 2021-06-01→2026-06-01 in `/data/market`) so omitted.

**Open choices fixed:** factor `d∈[0.15,0.6] δ∈[0.7,1.4] U∼N(0,1)` scale 1; Cholesky `X=Lᵀ, y=lstsq(Xᵀ,μ)` ≡ centred returns `X=(R-1̄r')/√(T-1)` to rounding; `lars_path`/`lars_path_gram` `max_iter=10·n` (`d=lstsq(Xᵀ,1)`, `ν₀=ν_last-max(|ν_last|,‖μ‖∞)` `δ=1`, `ν_last` via `nnls(X,d)>1e-9` support); KKT `worst/|μ|∞`; QP via `cvxpy OSQP eps 1e-12`; dates as `YYYYMMDD` ints.

**Deviations:** Synthetic levels differ (paper L1 7.765 Sharpe 2.12 vs ours 3.38/0.74, plain 10 vs 17 corners - seed-dependent as Table shows 15-24 range); FF vintage 202609 vs 202608; SP500 entirely omitted (paper 494/1213, timing/OSQP claims require that snapshot) - declared in `not_rebuilt`; solver substitutions as above; timings hardware-dependent unchecked per paper tolerances `1e-12–1e-9`.

`/work/results.json` valid (96 results), `replicate.py` clean of paper literals.