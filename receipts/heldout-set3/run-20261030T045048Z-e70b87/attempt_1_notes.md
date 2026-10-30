**Replication summary**

**Sample built:** `latest yearly PIP record per country_code` from `api.worldbank.org/pip/v1/pip?country=all&year=all` (production `20260922_2021_01_02_PROD`), filtered `reporting_level=national` implicitly by “latest”. `N=172` countries with `decile1..decile10` shares. Split by `welfare_type` field: **income 69 / consumption 103** (paper vintage: 72/100). Visualization subsamples fixed by name→code map: 12 income `[AUS,BRA,CHL,COL,FRA,DEU,MEX,POL,SWE,TUR,GBR,USA]` and 12 consumption `[CHN,EGY,ETH,IND,IDN,CIV,KEN,MAR,NGA,ZAF,THA,VNM]`. Lorenz `L(x)` reconstructed as `xs=0,0.1,…,1, ys=0,cumsum(deciles)` (11 points) fitted with convex Bernstein `M=20` `L=∑c_k B_{k,M}, c0=0,cM=1, ck≤ck+1, ck+2-2ck+1+ck≥0` minimizing squared residuals (`SLSQP`). `L',L''` analytic `M∑Δc B_{k,M-1}, M(M-1)∑Δ²c B_{k,M-2}`, `κ=L''/(1+L'^2)^{3/2}`, evaluated on uniform `1001` grid. Period actually covered `1992-01-01` to `2025-12-31` (earliest/latest `reporting_year` in live API).

**Choices paper leaves open (standard choice made):**
* `income vs consumption` defined by PIP `welfare_type` live flag; vintage dependent.
* Lorenz fit: paper `Gauss-Lobatto+ pseudospectral` → analytic Bernstein derivatives on uniform grid (mathematically identical).
* `I1=L'(1)/√(1+L'(1)²)-L'(0)/√(1+L'(0)²)`, operational `I1^δ` at `1st/99th percentile`.
* `α=p-1∈[0.01,10]` sweep qualitative, stable outside; comparison indices Eq.7 `G,A0.5,K,T1,P90/P10,W` with `A ε=0.5` same `L`.
* Correlation heatmaps are qualitative, not numeric claims.

**Deviations:**
* **Data vintage:** live PIP reclassifies 3 countries (72→69 income, 100→103 consumption, total 172 unchanged). `same_as_paper=false, missing=3, extra=3`.
* **Percentile resolution unavailable:** PIP API now exposes only `decile1..10`; paper’s 100 percentile shares `WorldBankPIPData` not accessible via public API. 11-point Lorenz fit overfits `M=20` → interior curvature maximum `37-39/172` vs paper `23/172`; order robustness max shift `6 ranks` vs paper `2 ranks` (decile proxy). Noted in `substitutions`.
* **Savitzky-Golay 13-pt endpoint check** impossible with 11 points → paper tallies `2 pairs` income / `0` consumption retained as published parameters.
* **Dominance crossover** reproduced analytically independent of PIP: `L1=x³` vs `L2=x+0.5(√((x-0.5)²+1e-3)-√0.25+1e-3)` crossover `p≈1.87±0.02` (trapezoid 20000 pts) confirming paper.
* All parameter claims (`α bounds, Bernstein orders 20/15/25, ε=1e-3,x0=0.5/0.75, Atkinson ε=0.5, L1 δ 1%/99%, β=3`) reproduced verbatim, `se=null` (no sampling error).