Replication completed. Script `/work/replicate.py` fetches PIP decile data via World Bank API, fits Bernstein M=20 convex Lorenz curves, computes indices and synthesizes crossover.

**Sample:** PIP latest-year per country (N=172, income 69 vs consumption 103 in 2026 vintage vs paper 72/100), 12+12 visualization subsamples, years 1992-2025. `same_as_paper=false` – public API provides only 10 decile aggregates not 100 percentiles (proxy with 11 Lorenz points normalized). Cannot count exact missing percentile observations.

**Choices left open (standardized):** Bernstein order 20, 11-point decile normalization, 2001-point dense grid trapezoidal integration, analytic Bernstein derivatives for L', L'', κ, I1 via endpoint derivatives, pseudospectral approximation via analytic derivatives.

**Deviations:** Decile proxy causes tail-sensitive I1 ranking shifts (e.g., SWE/POL/FRA) and interior-maxima count 38 vs 23, vintage reclassification shifts income/consumption counts. Crossover p≈1.87 computed numerically (5001-point integration, ε=1e-3, brentq) without hard-coding; robustness metrics computed from data (max shift 6, pairs switch 15 from operational vs Bernstein inversion count).

No paper numbers are hard-coded; all values computed from fetched data.
