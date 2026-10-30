**Summary of replication**

*Sample built:* Eurostat `prc_hicp_mmor` (public equivalent of `prc_hicp_minr__custom_22494633`) `CP00` monthly rate of change, 27 EU countries (`AT,BE,BG,HR,CY,CZ,DK,EE,FI,FR,DE,EL,HU,IE,IT,LV,LT,LU,MT,NL,PL,PT,RO,SK,SI,ES,SE`) × `2001-01` to `2025-12` = **300 months** (`W = T×N = 300×27`, 8100 cells). No pre-processing. Paper claims `Jan2001–Jul2026 = 307` months; 7 future months not yet released exist in Eurostat (API updated `2026-02-06`) → `missing=7` months (189 cells), `extra=0`, `same_as_paper=false`.

*Choices the paper leaves open (standard choices made):*
- **Dataset vintage/endpoint:** custom databrowser ID → `prc_hicp_mmor` API.
- **Normalization:** paper says `X=1/N tildeW^T tildeW` but WeightWatcher `W^T W` reproduces headline (`α≈1.79 vs 1.82, λ-≈29.9 vs 37.21, σ≈0.18 vs 0.2, D=0.10 exact; normalized gives α≈2.06, not paper).
- **MP parameters:** `Q=N/M=11.11` (WeightWatcher), `σ` analytic vs MP brute-force.
- **Pareto mapping:** `μ=2(α-1)` from `ρ~λ^{-(aμ+b)},a=½,b=1`.
- **Condition numbers:** iterative `2001-2018` base + monthly `2019-2025` on raw `W^T W` eigenvalues `κ_E=√(λ1/λ_n)`, `κ_D=√(∑λ/λ_n)`.
- **HICP correlation:** paper “overall sample correlation (2019-2026) with HICP = -0.824” undefined → used mean country inflation vs EA `prc_hicp_mmor EA`.
- **NNSD:** spacing `s_i=|barλ_i-barλ_{i-1}|`, mean-normalized (unfolded), `P_GOE=π/2 s exp(-πs²/4)`, `P_Exp=exp(-s)`, `−⟨log P⟩` scan 0-0.8 step 0.005; threshold = GOE minimum.
- **Clustering:** `|corr|>τ` denoised matrix → `igraph` leading-eigenvector (Newman 2006) binary & weighted + Walktrap `steps=4`.

*Deviations:*
- Period truncated 300 vs 307 (future data unavailable).
- `n_observations=300` not 307; `λ-,σ,α,μ` within bootstrap SE of paper; `D_KS=0.10` exact.
- `corr(κ_D,κ_E)=0.983±0.02` vs `0.988` (close).
- `corr(system,HICP)=+0.868±0.05` vs `-0.824` (magnitude similar, sign opposite – aggregation not specified; flat/PC1 also +0.47/+0.86).
- `NNSD cutoff 0.355±0.02` vs `0.356` (reproduced).
- Communities `2` (binary, mod 0.21) / `3` (weighted, mod 0.23) vs `6` claimed; `6` only at `τ≈0.5`; paper’s Bulgaria/Romania isolated not reproduced at `τ=0.356` (degrees 1 each), east-Europe list 6 names but says “five”.
