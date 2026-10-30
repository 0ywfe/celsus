We could not check this paper: the run stopped (BudgetExceeded). This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2610.04221
**Robust enhanced index tracking portfolio selection under distributional uncertainty**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|

## The paper's own numbers
- OK: sector (5 stocks each): 5 + 5 + 5 + 5 + 5 = 25, paper's total 25

## Guards
- rejected claim count_OutSampleMonths_60 = 60: printed once in the paper's LaTeX, and already claimed by count_InSampleMonths_60
- rejected claim count_TotalMonths_120 = 120: not in the paper's LaTeX
- spec: the headline was written as prose ('not stated as single number - central conclusion is that minimizing convex combination of worst-case mean loss + downsid'); chosen from the claim names: TM_NSS_MTSV_Sharpe
- round 1: the builder ran out of turns
- round 1: rejected before the clean run: the code that writes these results contains the number the paper reports for them (estimate_kappaStar_MV_Sharpe_WS_M_20_9 (20.9) at line 571). Compute each result from the data; the paper's value never goes into it.
- round 2: rejected before the clean run: the script writes the paper's sample count as a result's count, or cuts its sample to it (count_TotalStocks_25 (25) at line 47, count_InSampleMonths_60 (60) at line 456). Build the sample from the paper's definition and report the count you get; never trim, cut or pad it to a reported count.
- run stopped: BudgetExceeded: spent $2.0056 of a $2.0000 budget

## Data sources
- market data: none used
- other hosts the script fetched from: none

## Run
- sandbox: not run
- model calls: 60, providers: fireworks, all on Meta: yes (Meta models; accounts/fireworks/models/muse-spark-open on fireworks)
- tokens: in 6734149, out 170183 (reasoning 89381); cost $2.0056

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
