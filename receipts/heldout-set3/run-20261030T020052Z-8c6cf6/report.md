We could not check this paper: the run stopped (BudgetExceeded). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2601.20169
**United in Currency, Divided in Growth: Dynamic Effects of Euro Adoption - Replication Spec**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|

## The paper's own numbers
- NOTE: Joint pre-trends F (classical TWFE) H0: all tau(k)=0 for k<0: t = 3.13, paper's p = 0.001 matches one-sided (upper tail) (0.0009); two-sided p would be 0.0017
- OK: Average pre-treatment effect t-test (classical TWFE): t = -1.06, paper's p = 0.321 matches two-sided (0.2893); two-sided p would be 0.2893
- NOTE: Placebo fake adoption 1995 on actual adopters (text interpretation): t = -0.02 and p = 0.78 fit no side at the printed precision (two-sided p would be 0.9841); judged two-sided
- NOTE: Placebo fake adoption 1997 on actual adopters (text interpretation): t = 0.01 and p = 0.89 fit no side at the printed precision (two-sided p would be 0.9920); judged two-sided
- NOTE: Placebo non-euro EU members 1999 (Denmark): t = -0.1 and p = 0.01 fit no side at the printed precision (two-sided p would be 0.9220); judged two-sided
- NOTE: Placebo non-euro EU members 1999 (Sweden): t = 0.14 and p = 0.01 fit no side at the printed precision (two-sided p would be 0.9015); judged two-sided
- NOTE: Placebo non-euro EU members 1999 (UK): t = -0.14 and p = 0.07 fit no side at the printed precision (two-sided p would be 0.9015); judged two-sided
- NOTE: Placebo non-euro EU members joint test all placebo =0: t = 0.01 and p = 0.01 fit no side at the printed precision (two-sided p would be 0.9929); judged two-sided

## Guards
- no claims rejected
- spec: the headline was written as prose ('Paper headline rests on claims att_range_low (0.3), att_range_high (0.4), att_k0_point (-0.29), att_k0_CI_low (-0.36), a'); chosen from the claim names: att_k0_point
- spec: the headline was written as prose ('Euro adoption reduced annual real GDP per capita growth by 0.3-0.4 pp on average; CFFE point at adoption k=0 = -0.29 pp '); chosen from the claim names: att_k0_point
- spec problem unresolved: partition 'Heterogeneity by initial GDP per capita (pre-1995 median split, founders + Greece as classified in figure)': part 'High-income founders above-median 1995: Austria, Belgium, Finland, France, Germany, Luxembourg, Netherlands' is not the name of a claim
- spec problem unresolved: partition 'Heterogeneity by initial GDP per capita (pre-1995 median split, founders + Greece as classified in figure)': part 'total count claim = n_high_income = 7' is not the name of a claim
- spec problem unresolved: partition 'Heterogeneity by initial GDP per capita (pre-1995 median split, founders + Greece as classified in figure)': part 'representative estimate high_income_k10 = -0.31 pp SE 0.02, stabilized ~ -0.30 pp' is not the name of a claim
- spec problem unresolved: partition 'Heterogeneity by initial GDP per capita (pre-1995 median split, founders + Greece as classified in figure)': part 'Low-income founders below-median 1995: Greece, Ireland, Italy, Portugal, Spain' is not the name of a claim
- spec problem unresolved: partition 'Heterogeneity by initial GDP per capita (pre-1995 median split, founders + Greece as classified in figure)': part 'total count claim = n_low_income = 5' is not the name of a claim
- spec problem unresolved: partition 'Heterogeneity by initial GDP per capita (pre-1995 median split, founders + Greece as classified in figure)': part 'representative estimate low_income_k10 = -0.54 pp SE 0.03, diff high_low_diff_k10 = 0.23 pp' is not the name of a claim
- spec problem unresolved: partition 'Early (1999 founders) vs late adopters': part 'Early adopters 1999' is not the name of a claim
- spec problem unresolved: partition 'Early (1999 founders) vs late adopters': part 'count claim = n_founders_1999 = 11, country-year count claim N_early_275 = 275, ATE claim early_adopter_ATE = -0.37 pp' is not the name of a claim
- spec problem unresolved: partition 'Early (1999 founders) vs late adopters': part 'Late adopters' is not the name of a claim
- spec problem unresolved: partition 'Early (1999 founders) vs late adopters': part 'count claim = n_late_sufficient = 8, country-year count claim N_late_231 = 231, ATE claim late_adopter_ATE = 0.11 pp' is not the name of a claim
- spec problem unresolved: partition 'Control group composition': part 'EU opt-out controls (Denmark, Sweden, UK)' is not the name of a claim
- spec problem unresolved: partition 'Control group composition': part 'count claim = n_EU_optout = 3' is not the name of a claim
- spec problem unresolved: partition 'Control group composition': part 'Non-EU OECD controls' is not the name of a claim
- spec problem unresolved: partition 'Control group composition': part 'count claim = n_nonEU_OECD = 12' is not the name of a claim
- spec problem unresolved: partition 'Control group composition': part 'EU-only robustness at k0 EUonly_k0 = -0.703 vs baseline baseline_k0_EUcomp = -0.228, avg EUonly_avg = -0.472 vs baseline_avg = -0.261' is not the name of a claim
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (heterogeneity_GDP_importance (0.45) at line 556, heterogeneity_trade_importance (0.19) at line 557, heterogeneity_invest_importance (0.14) at line 558, heterogeneity_event_importance (0.12) at line 559, net_exports_range_low (1.3) at line 566, net_exports_range_high (1.6) at line 567, prod_decline_low (0.23) at line 568, prod_decline_high (0.31) at line 569, TFP_decline_low (-0.15) at line 570, TFP_decline_high (-0.22) at line 571, CA_deterioration_low (1.5) at line 572, CA_deterioration_high (2.5) at line 573, corr_CFFE_SCM (0.68) at line 575, SCM_Germany (1.2) at line 576, alt_CFFE_k10_CI_low (-0.25) at line 631, alt_IFE_k10 (-5.98) at line 635, alt_SA_k10 (-3.52) at line 636). Compute each result from the data; the paper's value never goes into it.
- round 2: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (N_total_obs (2,010) at line 867). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- run stopped: BudgetExceeded: spent $2.0094 of a $2.0000 budget

## Data sources
- market data: none used
- other hosts the script fetched from: none

## Run
- sandbox: not run
- model calls: 71, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 7030584, out 149672 (reasoning 68700); cost $2.0094

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
