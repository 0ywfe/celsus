We could not check this paper: the model's reply could not be read (Chat Completions response terminated with finish_reason='length' but produced no assistant text, tool call, or refusal.); a reply cut off at its output cap reads this way. This says nothing about whether its numbers hold.

# paper-replicator report: arXiv 2602.00080
**The GT-Score: A Robust Objective Function for Reducing Overfitting in Data-Driven Trading Strategies**

Verdict: **could not check**

| claim | kind | reported | reproduced | se | n | consistent | why |
|---|---|---|---|---|---|---|---|

## The paper's own numbers
- OK: Loss function - Monte Carlo (out-of-sample by objective): 2250 + 2250 + 2250 + 2250 = 9000, paper's total 9000
- OK: Loss function - Walk-forward validation (out-of-sample by objective): 1335 + 1335 + 1335 + 1335 = 5340, paper's total 5340
- OK: Paired t-test Monte Carlo OOS returns GT-Score vs Sharpe (paired across same asset/strategy/seed, N=2250 each): t = -2.45, paper's p = 0.014 matches two-sided (0.0143); two-sided p would be 0.0143
- OK: Paired t-test Monte Carlo OOS returns GT-Score vs Sortino: t = -5.05, paper's p = 0.001 matches two-sided (0.0000); two-sided p would be 0.0000
- OK: Paired t-test Monte Carlo OOS returns GT-Score vs Simple: t = -5.22, paper's p = 0.001 matches two-sided (0.0000); two-sided p would be 0.0000

## Guards
- rejected claim sig_gt_vs_sharpe = *: not a number
- rejected claim sig_gt_vs_sortino = ***: not a number
- rejected claim sig_gt_vs_simple = ***: not a number
- spec: the headline was written as prose ('Headline is 98% improvement in walk-forward generalization ratio (validation return / training return). Primary evidence'); chosen from the claim names: wf_gt_gen_ratio
- run stopped: ModelBehaviorError: Chat Completions response terminated with finish_reason='length' but produced no assistant text, tool call, or refusal.

## Data sources
- market data: none used
- other hosts the script fetched from: none

## Run
- sandbox: not run
- model calls: 17, providers: baseten, all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)
- tokens: in 450437, out 77232 (reasoning 57019); cost $0.4633

---
Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
