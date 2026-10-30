We could not check this paper: the replication did not report the paper's sample size (RevExactDates), so its sample cannot be compared. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2602.21173
**Bayesian Parametric Portfolio Policies**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|
| SampleStart | parameter | 1963 date |  |  |  |  | not computed |
| OOSStart | parameter | 1973 date |  |  |  |  | not computed |
| OOSEnd | parameter | 2023 date |  |  |  |  | not computed |
| NOOS | count | 605 months | 605 | 0 | 605 | True | precise: the paper's count |
| NBurnIn | count | 121 months | 121 | 0 | 121 | True | precise: the paper's count |
| TimingWindow | parameter | 120 months | 120 | 0 | 120 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| NAnomaly | parameter | 212 predictors | 212 | 0 | 212 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| NTiming | parameter | 30 predictors | 30 | 0 | 30 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| NSignals | parameter | 242 predictors | 242 | 0 | 242 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| NSignalsPolicy | parameter | 243 predictors | 243 | 0 | 243 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| NCoefficientsPolicy | parameter | 1215 coefficients | 1215 | 0 | 1215 |  | a parameter the paper sets in its method, not a result, so it is not judged |
| RiskAversion | parameter | 5 | 5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingCap | parameter | 0.6 | 0.6 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingLeverage | parameter | 1.5 | 1.5 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingPcaRank | parameter | 10 components | 10 |  |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingOmega | parameter | 5.8 | 5.8 | 0 |  |  | a parameter the paper sets in its method, not a result, so it is not judged |
| TimingActive | estimate | 7.05 pp/year | 6.874 | 0.6995 | 605 | True | paper inside 6.874 +/- 1.371 |
| TimingStatic | estimate | 4.97 pp/year | 4.991 |  | 605 |  | no standard error |
| TimingComponent | estimate | 2.08 pp/year | 1.883 | 0.6995 | 605 | True | paper inside 1.883 +/- 1.371 |
| TimingT | p_value | 3 t-stat | 0.007099 |  | 605 | False | opposite sides of 0.05 |
| TimingShare | estimate | 29.5% | 27.39 |  | 605 |  | no standard error |
| TimingGrossSR | estimate | 1.242 | 1.232 |  | 605 |  | no standard error |
| TimingMapTiming | estimate | 1.5 pp/year | 1.418 | 0.9849 | 605 | True | paper inside 1.418 +/- 1.93 |
| TimingMapT | p_value | 1.53 t-stat | 0.15 |  | 605 | True | both >= 0.05 |
| TimingMarketSR | estimate | 0.739 | 0.7393 |  | 605 |  | no standard error |
| TimingConstSR | estimate | 1.193 |  |  |  |  | not computed |
| TimingCmvTiming | estimate | 0.98 pp/year |  |  |  |  | not computed |
| TimingCmvT | p_value | 1.15 t-stat |  |  |  |  | not computed |
| TimingLassoTiming | estimate | 0.82 pp/year |  |  |  |  | not computed |
| TimingLassoT | p_value | 1 t-stat |  |  |  |  | not computed |
| TimingMinvarTiming | estimate | 0.11 pp/year |  |  |  |  | not computed |
| TimingInvvarTiming | estimate | -0.12 pp/year |  |  |  |  | not computed |
| TimingPConst | p_value | 0.953 p |  |  |  |  | not computed |
| TimingPMap | p_value | 0.953 p |  |  |  |  | not computed |
| TimingSeventies | estimate | -0.14 pp/year | -0.06111 | 0.7258 | 77 | True | paper inside -0.06111 +/- 1.423 |
| TimingEighties | estimate | 0.79 pp/year | 0.7209 | 0.8506 | 120 | True | paper inside 0.7209 +/- 1.667 |
| TimingNineties | estimate | 2.93 pp/year | 3.036 | 1.032 | 120 | True | paper inside 3.036 +/- 2.023 |
| TimingThousands | estimate | -0.06 pp/year | -0.5468 | 1.561 | 120 | True | paper inside -0.5468 +/- 3.06 |
| TimingTens | estimate | 0.72 pp/year | 0.5164 | 0.7303 | 120 | True | paper inside 0.5164 +/- 1.431 |
| TimingTwenties | estimate | 1.89 pp/year | 1.555 | 3.079 | 48 | True | paper inside 1.555 +/- 6.035 |
| TimingExNineties | estimate | 1.73 pp/year | 1.467 | 0.8157 | 485 | True | paper inside 1.467 +/- 1.599 |
| TimingExNinetiesT | p_value | 2.13 t-stat | 0.07209 |  | 485 | True | both >= 0.05 |
| TimingExNinetiesMonths | count | 485 months | 485 | 0 | 485 | True | precise: the paper's count |
| TimingRobustLow | estimate | 1.47 pp/year |  |  |  |  | not computed |
| TimingRobustHigh | estimate | 3.02 pp/year |  |  |  |  | not computed |
| TimingRobustTLow | p_value | 2.18 t-stat |  |  |  |  | not computed |
| TimingRobustTHigh | p_value | 4.04 t-stat |  |  |  |  | not computed |
| RevScaleMatched | parameter | 0.375 |  |  |  |  | not computed |
| RevScaledTiming | estimate | 2.04 pp/year |  |  |  |  | not computed |
| RevScaledT | p_value | 2.65 t-stat |  |  |  |  | not computed |
| RevScaledDiffT | p_value | 0.25 t-stat |  |  |  |  | not computed |
| RevMonthlyTiming | estimate | 1.55 pp/year |  |  |  |  | not computed |
| RevMonthlyT | p_value | 2.19 t-stat |  |  |  |  | not computed |
| RevBagTiming | estimate | 1.69 pp/year |  |  |  |  | not computed |
| RevBagT | p_value | 1.95 t-stat |  |  |  |  | not computed |
| RevBagAtLimit | tally | 86.6% months |  |  |  |  | not computed |
| RevRidgeHalfAtLimit | tally | 62.5% months |  |  |  |  | not computed |
| RevRidgeTimingLow | estimate | 1.47 pp/year |  |  |  |  | not computed |
| RevRidgeTimingHigh | estimate | 1.69 pp/year |  |  |  |  | not computed |
| RevPostSD | estimate | 1 |  |  |  |  | not computed |
| RevBootSD | estimate | 0.42 |  |  |  |  | not computed |
| RevAtLimitBPPP | tally | 52.6% months | 51.57 |  | 605 |  | a tally of what the analysis found, with no uncertainty, so it is not judged |
| RevAtLimitMap | tally | 96.4% months | 96.69 |  | 605 |  | a tally of what the analysis found, with no uncertainty, so it is not judged |
| RevContraction | estimate | 0.45 |  |  |  |  | not computed |
| RevContractionLow | estimate | 0.32 |  |  |  |  | not computed |
| RevContractionHigh | estimate | 0.54 |  |  |  |  | not computed |
| RevContractionCorr | estimate | 0.983 |  |  |  |  | not computed |
| RevPeakScaleTiming | parameter | 0.4 |  |  |  |  | not computed |
| RevPeakTiming | estimate | 2.05 pp/year |  |  |  |  | not computed |
| RevPeakScaleSR | parameter | 0.425 |  |  |  |  | not computed |
| RevPeakSR | estimate | 1.245 |  |  |  |  | not computed |
| RevMandateBTLow | p_value | 2.19 t-stat |  |  |  |  | not computed |
| RevMandateBTHigh | p_value | 3.06 t-stat |  |  |  |  | not computed |
| RevMandateMTLow | p_value | 1.39 t-stat |  |  |  |  | not computed |
| RevMandateMTHigh | p_value | 2.18 t-stat |  |  |  |  | not computed |
| RevMandateTimLow | estimate | 1.38 pp/year |  |  |  |  | not computed |
| RevMandateTimHigh | estimate | 3.7 pp/year |  |  |  |  | not computed |
| RevMandateNetLow | estimate | 0.963 |  |  |  |  | not computed |
| RevMandateNetHigh | estimate | 1.107 |  |  |  |  | not computed |
| RevRecTiming | estimate | 1.9 pp/year |  |  |  |  | not computed |
| RevRecT | p_value | 2.64 t-stat |  |  |  |  | not computed |
| RevRecModal | tally | 72% months |  |  |  |  | not computed |
| RevRecCostT | p_value | 1.93 t-stat |  |  |  |  | not computed |
| RevRecCostNetSR | estimate | 1.121 |  |  |  |  | not computed |
| RevRecScaledTiming | estimate | 2 pp/year |  |  |  |  | not computed |
| RevRecScaledT | p_value | 2.46 t-stat |  |  |  |  | not computed |
| RevCostEightyNet | estimate | 1.118 |  |  |  |  | not computed |
| RevCostEightyTurn | estimate | 1.51 annual |  |  |  |  | not computed |
| RevCostEightyTiming | estimate | 1.42 pp/year |  |  |  |  | not computed |
| RevCostEightyT | p_value | 2.25 t-stat |  |  |  |  | not computed |
| RevCostEightyP | p_value | 0.79 p |  |  |  |  | not computed |
| RevCostTLow | p_value | 2.03 t-stat |  |  |  |  | not computed |
| RevRecCostP | p_value | 0.83 p |  |  |  |  | not computed |
| RevRecCostCEDiff | estimate | -0.34 pp/year |  |  |  |  | not computed |
| RevConstNetSR | estimate | 1.136 |  |  |  |  | not computed |
| RevScaleTwoNet | estimate | 1.122 |  |  |  |  | not computed |
| RevScaleTwoT | p_value | 1.78 t-stat |  |  |  |  | not computed |
| RevScaleTwoTiming | estimate | 1.22 pp/year |  |  |  |  | not computed |
| RevScaleTwoTurn | estimate | 1.09 annual |  |  |  |  | not computed |
| RevExcessGrossSR | estimate | 0.96 |  |  |  |  | not computed |
| RevExcessConstGross | estimate | 0.925 |  |  |  |  | not computed |
| RevDropAnomaly | estimate | 0.87 pp/year |  |  |  |  | not computed |
| RevDropAnomalyT | p_value | 1.13 t-stat |  |  |  |  | not computed |
| RevFamilyMax | estimate | 0.05 pp/year |  |  |  |  | not computed |
| RevPub | estimate | 1.22 pp/year |  |  |  |  | not computed |
| RevPubT | p_value | 1.79 t-stat |  |  |  |  | not computed |
| RevPubPost | estimate | 1.75 pp/year |  |  |  |  | not computed |
| RevPubTwo | estimate | 1.17 pp/year |  |  |  |  | not computed |
| RevPubTwoT | p_value | 1.75 t-stat |  |  |  |  | not computed |
| RevPost | estimate | 1.82 pp/year |  |  |  |  | not computed |
| RevPreBPPP | estimate | 1.48 | 1.441 |  | 605 |  | no standard error |
| RevPreMap | estimate | 2.44 | 2.43 |  | 605 |  | no standard error |
| RevExactDates | count | 605 dates |  |  |  |  | not computed |
| RevExactRhatMax | estimate | 1.005 |  |  |  |  | not computed |
| RevExactMcseMax | estimate | 0.0037 |  |  |  |  | not computed |
| RevExactMcseMedian | estimate | 0.0014 |  |  |  |  | not computed |
| RevExactMinRank | count | 113 |  |  |  |  | not computed |
| RevExactAccept | tally | 95% |  |  |  |  | not computed |
| RevExactSdRatio | estimate | 0.996 |  |  |  |  | not computed |
| RevExactMeanShift | estimate | 0.026 SD |  |  |  |  | not computed |
| RevExactMaxDiff | estimate | 0.07 |  |  |  |  | not computed |
| RevExactMeanDiff | estimate | 0.0086 |  |  |  |  | not computed |
| RevExactTiming | estimate | 2.12 pp/year |  |  |  |  | not computed |
| RevExactT | p_value | 2.95 t-stat |  |  |  |  | not computed |
| RevPcaTen | estimate | 4.42 pp/year |  |  |  |  | not computed |
| RevPcaTenT | p_value | 4.51 t-stat |  |  |  |  | not computed |
| RevPcaTenExpl | estimate | 53% |  |  |  |  | not computed |
| RevPcaTurnLow | estimate | 10.6 annual |  |  |  |  | not computed |
| RevPcaTurnHigh | estimate | 15.4 annual |  |  |  |  | not computed |
| RevPcaNetLow | estimate | 0.56 |  |  |  |  | not computed |
| RevPcaNetHigh | estimate | 0.85 |  |  |  |  | not computed |
| RevTurnover | estimate | 5.01 annual | 4.999 |  | 605 |  | no standard error |
| RevBreakEighty | estimate | 51% schedule |  |  |  |  | not computed |
| RevBreakRec | estimate | 51% schedule |  |  |  |  | not computed |
| RevRecAlpha | estimate | 0.83 pp/year |  |  |  |  | not computed |
| RevRecAlphaT | p_value | 0.76 t-stat |  |  |  |  | not computed |
| RevBlendW | parameter | 40% |  |  |  |  | not computed |
| RevBlendSR | estimate | 1.147 |  |  |  |  | not computed |
| BPPP_exposure_Table1 | estimate | 1.31 | 1.296 |  | 605 |  | no standard error |
| RPPP_exposure_Table1 | estimate | 1.49 | 1.495 |  | 605 |  | no standard error |
| Constant_active | estimate | 7.18 pp/year |  |  |  |  | not computed |
| Constant_static | estimate | 7.1 pp/year |  |  |  |  | not computed |
| Constant_timing | estimate | 0.08 pp/year |  |  |  |  | not computed |
| Constant_timing_t | p_value | 0.33 t-stat |  |  |  |  | not computed |
| Performance_BPPP_CE | estimate | 12.68% annual |  |  |  |  | not computed |
| Performance_Constant_CE | estimate | 12.09% annual |  |  |  |  | not computed |
| Diagnostics_BPPP_at_position | tally | 0% |  |  |  |  | not computed |
| Table2_RPPP_prior0.8_timing | estimate | 1.52 pp/year |  |  |  |  | not computed |
| Table3_PC3_timing | estimate | 2.57 pp/year |  |  |  |  | not computed |
| Table3_PC5_timing | estimate | 3.98 pp/year |  |  |  |  | not computed |
| Table4_kappa5_timing | estimate | 1.66 pp/year |  |  |  |  | not computed |
| Table_signals_SMB_Leverage_contrib | estimate | -0.303 pp/year |  |  |  |  | not computed |
| Table_signals_HML_Leverage_contrib | estimate | 0.664 pp/year |  |  |  |  | not computed |
| SMB_total_timing_signals | estimate | 0.625 pp/year |  |  |  |  | not computed |
| HML_total_timing_signals | estimate | 0.758 pp/year |  |  |  |  | not computed |
| CMA_total_timing | estimate | 0.078 pp/year |  |  |  |  | not computed |
| RMW_total_timing | estimate | 0.046 pp/year |  |  |  |  | not computed |
| UMD_total_timing | estimate | 0.573 pp/year |  |  |  |  | not computed |

## The paper's own numbers
- nothing to check

## Guards
- no claims rejected
- spec: the headline was written as prose ('BPPP earns TimingComponent=2.08 pp per year from timing Cov(w,F) with TimingT=3.00 Newey-West t, out of active return Ti'); chosen from the claim names: TimingComponent
- round 1: the builder ran out of turns
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (TimingCmvTiming (0.98) at line 637). Compute each result from the data; the paper's value never goes into it.
- round 2: audit sent the sample back: TimingT = 2.6921475566343274: no p-value lies outside 0 to 1
- round 3: audit sent the sample back: the replication did not report the paper's sample size (RevExactDates), so its sample cannot be compared
- sample: the replication did not report the paper's sample size (RevExactDates), so its sample cannot be compared
- sample: the sample differs from the paper's by 0 missing and 0 extra observations (0.0% of the paper's 605, missing and extra together), within 15%, SCORE's tolerance for sample size, so its results are judged
- caveat: the replication used other sources or methods for the paper's observations: French data live from Ken French library (2026-09 CRSP vintage) vs paper's 2023 vintage; OSAP CrossSection Data Release 2026.10 (huggingface) vs paper's OSAP vintage; factor-specific predictors recomputed per Appendix A definitions with expanding standardisation as described; learning rate fixed at median 5.80 rather than diagonal heuristic per window; HMC exact posterior check omitted; trading costs, publication-lag, PCA, bagging, turnover penalty and comparator rules not rebuilt

## Data sources
- market data: none used
- other hosts the script fetched from: mba.tuck.dartmouth.edu, huggingface.co, us.gcp.cdn.hf.co

## Run
- sandbox: attempt 3, exit 0, 37.6s
- model calls: 57, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 4844052, out 143427 (reasoning 98635); cost $1.5877

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
