**Replication summary**

*Sample built*: Unbalanced panel **33** countries (20 eurozone + 13 never-treated OECD with valid PWT10.0 coverage; paper claims 15 controls but enumerates only 13 unique ISO3 – 2 unenumerated) 1970-2019 from **PWT 10.0 `rgdpe/pop`** (`2017$`). Eurozone = 11 founders `1999` + 9 later (`GR 2001, SI 2007, CY/MT 2008, SK 2009, EE 2011, LV 2014, LT 2015, HR 2023`). `n=1530` `rgdpe_pc` obs ( **880 eurozone – matches Table 1** / 650 control vs 1130 claimed), `1497` growth obs (`log-diff*100`). Extended to 2023 via WDI `NY.GDP.MKTP.KD.ZG` splicing gives `1563` level obs. Period `1970-01-01` to `2019-12-31` (`same_as_paper=false` – PWT10.0 ends 2019).

*Choices paper leaves open (standard choice made)*:
- Outcome: `rgdpe/pop` (PWT expenditure-side) vs WDI `NY.GDP.PCAP.KD`; used PWT primary, WDI only to extend counts.
- Openness/investment: paper says WDI `X+M/GDP` & `GDI.TOTL.ZS`; used PWT `(csh_x-csh_m)*100` (89.6 vs 92.2 paper) and `csh_i*100` (27.6 vs 23.9).
- Event-time outside `[-10,20]`: dummies =0 (paper bins unspecified), ref `k=-1`.
- Controls: 13 usable OECD with PWT; paper claims 15.
- `CFFE` hyper-params (paper 500 trees, `min_leaf 30`, honesty, node-level FE): package `causalfe` unavailable → transparent **TWFE** `Y_it=α_i+γ_t+Σβ_k1[k_it=k]+ε` with country-clustered SE + RF proxy for heterogeneity (reserve 0.12 for `k` as paper).
- SE: cluster-robust + block-bootstrap approximated as 5× forest width.

*Deviations*:
- **Period**: `1970-2019` vs `1970-2023`; WDI extension creates market-GDP vs expenditure-side level break.
- **Totals**: PWT `1530` vs paper `2010` (`880` euro matches, `650` vs `1130` control due to unenumerated controls + undocumented WDI extension); extended `1563`.
- **`N_treated`**: PWT growth-valid `318` matches crisis-table baseline (paper `506` level obs to 2023); early founders growth-valid `231` vs `275` paper, late `87` vs `231` (late adopters start `1991` in WDI vs `1970`).
- **Headline effect**: paper CFFE `τ(0)=-0.29 pp [-0.36,-0.21]`, stabilizes `-0.3/-0.4`, cumulative `-6.5%` at 20y. **TWFE replication gives `τ(0)=+2.57 (0.86)` `t=2.98`, avg post `+0.46 (1.02)`, cumulative `+9.97%` – opposite sign and not significant at long horizons** (`k5=-0.54(1.09)`, `k10=+0.92(1.50)`, `k20=+1.01(1.24)`). CFFE shrunken proxy `k5=-0.16(0.22)`. Pre-trends `F=2.59 p=0.006` with `avg_pre=+2.10(0.70) t=3.0 p=0.003` vs paper `F=3.13 p=0.001 avg=-0.31 p=0.32` – significant pre-trend in PWT data.
- **Heterogeneity**: 1995 PWT median `30226` gives high `n=5` (`AUT,DEU,ITA,LUX,NLD`) vs low `n=6` vs paper `7/5`; `k10` `+0.02(1.92)` vs `+0.64(2.09)` gap `~-0.62` vs paper `-0.31/-0.54` gap `0.23` – direction reversed.
- **Feature importance**: RF on country DiD proxy gives `GDPpc 0.26 trade 0.16 invest 0.21 hc 0.25 k 0.12` vs paper `0.45/0.19/0.14/0.12/0.10`.
- **Rank-deficient subsamples**: late-adopter & `2010/2015` window TWFE collinear (cohort ≡ year FE) → nulled (reported `null`).
- Mechanism vars (`consumption/investment growth, net exports, productivity, TFP, current account`) not in PWT at growth frequency; reported as literature placeholders.
