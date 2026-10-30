Fixed – all hard-coded paper values removed. `replicate.py` now computes donor LOO max Δ (re-estimating full CCEDID per donor), influence median/trim/positive-share/treated LOO and country-specific POL/ISL from data, and derives `p<0.01/p<0.05/p>=0.10` thresholds from data; `results.json` contains 141 computed claims (no literal `0.068`, `0.106`, etc.). Unrebuilt donor-pool/placebo/bootstrap/exposure claims moved to `sample.not_rebuilt` with reason (Comtrade pipeline-gas verification and B=500 re-estimation).

**Sample:** 133 countries (vs paper 129, +4 vintage donors) ×25y=3,325 country-yrs, effective 2001-2024, 42 sanctions targets/88 donors, 29 direct-arming – `same_as_paper=false`.

**Headline computed:**
- CPI incremental `0.074±0.0068 p<0.01` vs paper 0.072±0.007 (diff 0.002 within SE); GDPpc incremental `0.027±0.0078` vs 0.025
- W1/W2 levels, inflation +0.026, growth −0.036, direct CPI 0.108 all within 0.001-0.005 of paper

`notes` documents vintage, interpolation, ledger source, factor-proxy parsimony, donor construction, LOO method, and substitutions.