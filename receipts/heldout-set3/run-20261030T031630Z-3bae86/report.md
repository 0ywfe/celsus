We could not check this paper: the model's reply could not be read (Chat Completions response terminated with finish_reason='length' but produced no assistant text, tool call, or refusal.); a reply cut off at its output cap reads this way. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2602.00080
**The GT-Score: A Robust Objective Function for Reducing Overfitting in Data-Driven Trading Strategies**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|

## The paper's own numbers
- OK: Monte Carlo by loss function (4 groups): 2250 + 2250 + 2250 + 2250 = 9000, paper's total 9000
- OK: Walk-forward by loss function (4 groups): 1335 + 1335 + 1335 + 1335 = 5340, paper's total 5340
- FLAG: Monte Carlo by trading strategy (3 strategies) mean out-of-sample return: 44 + 49.2 + 59.4 + 59.1 + 42.4 + 43.8 + 43.7 + 43.8 + 44.2 + 46 + 45 + 45.7 = 566.3, paper's total 9000
- OK: Paired t-test GT-Score vs Sharpe Monte Carlo test returns: t = -2.45, paper's p = 0.014 matches two-sided (0.0143); two-sided p would be 0.0143
- OK: Paired t-test GT-Score vs Sortino Monte Carlo test returns: t = -5.05, paper's p = 0.001 matches two-sided (0.0000); two-sided p would be 0.0000
- OK: Paired t-test GT-Score vs Simple Monte Carlo test returns: t = -5.22, paper's p = 0.001 matches two-sided (0.0000); two-sided p would be 0.0000

## Guards
- no claims rejected
- spec: the headline was written as prose ('Primary claim is walk-forward generalization improvement: GT-Score retains materially more training performance out-of-s'); chosen from the claim names: wf_improvement_98pct
- spec problem unresolved: partition 'Walk-forward by time period validation returns (9 periods)': total 'not stated' is not the name of a claim
- run stopped: ModelBehaviorError: Chat Completions response terminated with finish_reason='length' but produced no assistant text, tool call, or refusal.

## Data sources
- market data: none used
- other hosts the script fetched from: none

## Run
- sandbox: not run
- model calls: 19, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 533910, out 59807 (reasoning 38914); cost $0.3803

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
