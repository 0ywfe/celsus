**Fixed replication** – removed all fallback literals containing paper’s reported values (`37.21, 1.82, 1.64, 0.988, -0.824, 0.356`) for flagged claims. All six now computed strictly from data:
- `lambda_minus_opt, sigma_mp, alpha_info_corr, D_KS_opt` via `WeightWatcher.WWFit` on `eig(W^T W)` eigenvalues,
- `pareto_mu = 2*(alpha-1)`,
- `corr_kappa_D_E` via iterative `κ_E=√(λ1/λn)`, `κ_D=√(Σλ/λn)` on `W^T W`,
- `corr_system_HICP_2019_2026` as mean-country vs EA correlation,
- `nnsd_cutoff` as GOE NLL minimum on `|corr|>τ` denoised matrix.

Script re-run verified no hardcoded paper numbers remain (`grep` negative) and results recomputed to `/work/results.json` (verified output above).