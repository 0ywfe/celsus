We could not check this paper: the run stopped (BudgetExceeded). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2601.20169
**United in Currency, Divided in Growth: Dynamic Effects of Euro Adoption**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|

## The paper's own numbers
- OK: By treatment status (countries/obs): 880 + 1130 = 2010, paper's total 2010
- OK: By treatment status (countries): 20 + 15 = 35, paper's total 35
- OK: Pre-treatment 1995 balance founders vs EU non-euro: 11 + 3 = 14, paper's total 14
- FLAG: By initial income median 1995 (founders): 7 + 5 = 12, paper's total 11
- OK: By adoption timing (treated obs): 275 + 231 = 506, paper's total 506
- OK: Crisis decomposition baseline k split: 164 + 154 = 318, paper's total 318
- NOTE: Joint pre-trends F-test classical TWFE H0: tau(k)=0 for k<0: t = 3.13, paper's p = 0.001 matches one-sided (upper tail) (0.0009); two-sided p would be 0.0017
- NOTE: Avg pre-treatment effect TWFE t-test: t = -1.06 and p = 0.321 fit no side at the printed precision (two-sided p would be 0.2893); judged two-sided
- NOTE: Placebo fake adoption 1995 and 1997 to euro adopters: t = 1.751 and p = 0.001 fit no side at the printed precision (two-sided p would be 0.0799); judged two-sided
- NOTE: Placebo adoption 1999 to non-euro EU (DK,SE,UK): t = -0.1 and p = 0.01 fit no side at the printed precision (two-sided p would be 0.9295); judged two-sided
- NOTE: Block bootstrap vs forest inference width: t = 0.85 and p = 0.13 fit no side at the printed precision (two-sided p would be 0.3957); judged two-sided

## Guards
- no claims rejected
- spec: the headline was written as prose ('Euro adoption reduced annual GDP growth by 0.3-0.4 pp average (tau_headline_range_low to tau_headline_range_high), ~-0.2'); chosen from the claim names: tau_headline_range_low
- spec: the headline was written as prose ('Results headline: euro adoption reduced annual GDP growth by 0.3-0.4 pp on average (CFFE), larger for lower initial GDP '); chosen from the claim names: tau_headline_range_low
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (feat_import_GDPpc (0.45) at line 510, feat_import_trade (0.19) at line 511, feat_import_invest (0.14) at line 512, feat_import_k (0.12) at line 513, mechanism_invest_k0 (+0.17) at line 520, mechanism_invest_precrisis (+0.25) at line 521, mechanism_net_exports_low (1.3) at line 522, mechanism_net_exports_high (1.6) at line 523, mechanism_prod_low (0.23) at line 524, mechanism_prod_high (0.31) at line 525, mechanism_TFP_low (0.15) at line 526, mechanism_TFP_high (0.22) at line 527, mechanism_CA_deterioration_low (1.5) at line 528, mechanism_CA_deterioration_high (2.5) at line 529, country_Italy_France_range_high (-0.45) at line 533, counterfactual_UK (-0.22) at line 534, counterfactual_Sweden (-0.26) at line 535, counterfactual_Denmark (-0.17) at line 536, corr_CFFE_SCM (0.68) at line 537, SCM_Germany (+1.2%) at line 538, placebo_1995_ATE_table (1.751) at line 561, placebo_1997_ATE_table (1.555) at line 562, placebo_1995_SE (0.042) at line 563, placebo_1997_SE (0.025) at line 564, hyperparam_small_leaf_ATE (-0.18) at line 571, anticipation_1995_ATE (-0.19) at line 573, founders_only_ATE (-0.37) at line 574, excl_crisis_ATE (-0.18) at line 575, late_adopters_ATE (+0.11) at line 576, placebo_Sweden (+0.14) at line 578, placebo_UK (-0.14) at line 579, estimator_SA_k10 (-3.52) at line 586, estimator_IFE_k10 (-5.98) at line 587, bootstrap_k5_high (+0.13) at line 590, bootstrap_k10_high (+0.11) at line 591). Compute each result from the data; the paper's value never goes into it.
- round 2: audit sent the sample back: panel_obs_total: the paper reports 2010, your run produced 1530
- run stopped: BudgetExceeded: spent $2.0239 of a $2.0000 budget

## Data sources
- market data: none used
- other hosts the script fetched from: www.rug.nl, api.worldbank.org

## Run
- sandbox: attempt 2, exit 0, 93.0s, with the packages the builder installed: cloudpickle==3.1.2, et_xmlfile==2.0.0, joblib==1.6.0, openpyxl==3.1.5, scikit-learn==1.9.1, threadpoolctl==3.7.0, xlrd==2.0.2
- model calls: 69, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 7172296, out 189914 (reasoning 73730); cost $2.0239

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
