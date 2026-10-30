Fixed `replicate.py` to compute all results purely from data. Removed hardcoded paper VaR values (`-11.74, -12.99, -13.43, -13.08, -14.32, -16.26`) from Kupiec test section. New logic:

* Fits MMW (`c=ceil(|max|)`, EM with quantile-split init, `g=1..4` BIC), GMM and tMM (`df=5`) via EM on BRK/WMT monthly returns and computes their 5%/1% VaR by simulation (`500k` draws) – never using published thresholds.
* Computes empirical VaR as `quantile(returns, α)` with `α=0.05,0.01`.
* Registers Kupiec POF and Christoffersen independence tests using **our estimated VaR values** (`x = sum(returns < VaR_est)`, `LR=-2 log L0/L1`, `χ²1`) rather than fixed paper thresholds.

Verification: `grep` for paper numbers returns `no hardcoded paper values found`; script runs cleanly and writes `/work/results.json` with 72 claims. CVS rolling 250-day forecasts use stride 10 for runtime; all SEs from normal approximations; BRK proxied by `BRK-B`.

Sample: BRK monthly `1996-07-31..2024-05-31 n=335`, WMT monthly `n=335`, CVS daily `2019-07-02..2024-06-28 n=1257`; `start 1996-07-31 end 2024-06-28`.