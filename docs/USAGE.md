# Using celsus

This guide takes you from a fresh clone to reading a report and checking it yourself. The flags, defaults, file names
and rules in it come from the code: the parsers in `src/paper_replicator/replicate.py` and `cli/__main__.py`, the
matching rules in `compare.py`, and what a run writes in `replicate.py`. A test (`tests/test_usage_doc.py`) fails if a
flag or command named here stops existing.

- [What you need](#what-you-need)
- [Install](#install)
- [See it without a key: the demo](#see-it-without-a-key-the-demo)
- [Check a paper](#check-a-paper)
- [What you see on screen](#what-you-see-on-screen)
- [The four verdicts](#the-four-verdicts)
- [When a number matches](#when-a-number-matches)
- [What a run writes, and how to check it yourself](#what-a-run-writes-and-how-to-check-it-yourself)
- [Replay, sabotage and batch](#replay-sabotage-and-batch)
- [Cost, time and the budget stop](#cost-time-and-the-budget-stop)
- [Which papers it can check](#which-papers-it-can-check)
- [Troubleshooting](#troubleshooting)
- [Tests](#tests)

## What you need

Python 3.11 or later (`requires-python = ">=3.11"` in `pyproject.toml`), uv, which installs the locked dependencies
from `uv.lock` (the project doesn't pin a uv version), and git to clone the repository. That's enough for the demo.

To check a paper live you also need:

- a key for Meta's Model API (Muse Spark, Muse Wonder), from dev.meta.ai under API keys, which goes in `.env` as
  `MODEL_API_KEY`;
- a Modal account and token, since the replication script is written and run in Modal sandboxes, never on your
  machine;
- `SEC_USER_AGENT`, the contact SEC EDGAR asks every automated client to declare, in the form
  `Name email@example.com`. The sandbox sends it to sec.gov and nowhere else. Fill it in before you check a paper
  whose data comes from SEC filings.

## Install

```bash
git clone https://github.com/0ywfe/celsus
cd celsus
uv sync
cp .env.example .env            # then fill in MODEL_API_KEY and SEC_USER_AGENT
uv run modal token new          # links this machine to your Modal account
```

`.env` stays on your machine (it is in `.gitignore`). `.env.example` also lists optional keys for other hosts of Muse
Spark Open, Meta's open-weights model. You don't need them: every run defaults to Meta's own API.

## See it without a key: the demo

```bash
uv run celsus demo
```

This replays a held-out run shipped with the package, labelled as a replay, in about 30 seconds: run 25b01b on arXiv
2610.04221, where 84 of 84 checked results match. It needs no API key, no Modal token and no `runs/` folder. Its
report and the script that produced it are in `src/paper_replicator/cli/demo/`.

`--seconds` sets about how long the replay takes (default 28), `--max-gap` the longest pause between two lines in
seconds (default 1.5), and `--log` shows the full log (every event and command) instead of one plain sentence per
step. A shipped run's ID can follow `demo`; the default is 25b01b.

## Check a paper

```bash
uv run celsus check <arxiv id> [options]
uv run celsus check -h          # lists every option below
```

A worked example:

```bash
uv run celsus check 2604.27287 --effort minimal --budget-usd 1 --require-provider meta
```

It checks arXiv 2604.27287 (*A Levered ETF Anomaly Explained*) on Muse Spark (`muse-spark-1.3`, the default model)
at minimal reasoning effort. It stops if spending passes $1, and stops before any call to a model that isn't Meta's.
Our run of it (run d45c71, 31 Oct 2026) took 3:20 and cost $0.24 for 16 model calls over 2 build rounds. Its verdict
was **partly holds up**: 23 of 25 checked results match within their uncertainty. Its main result is -5.643% in the
paper and -5.691% here, but it isn't judged, because the replication gives it no standard error. These numbers come
from that run's own `summary.json`. Model output varies, so a run of your own can land on other numbers; the batch
command below measures by how much.

Options, from the parser (`uv run celsus check -h` prints the same):

| option | default | what it does |
|---|---|---|
| `arxiv_id` | required | the paper's arXiv ID, for example `2604.27287` |
| `--model` | `muse-spark-1.3` (Muse Spark) | the model for every role; `muse-wonder-1.0` runs Muse Wonder |
| `--effort` | medium | reasoning effort for the extractor, chooser and builder, from minimal to max; the reviewer always runs at high |
| `--provider` | `meta` | the endpoint the model is called on; others are added in `providers.local.json` (format in `src/paper_replicator/local.py`) |
| `--require-provider` | none | stop the run before any call to a model from anyone else; `meta` counts Meta's models wherever they are served |
| `--budget-usd` | $3.00 with the workbench builder | the budget stop for this run, in US dollars of model calls (see [Cost](#cost-time-and-the-budget-stop)) |
| `--builder` | `workbench` | `workbench`: Muse explores in a sandbox with `run` and `write_file` tools and writes the script there; `oneshot`: Muse returns the whole script in one reply per attempt |
| `--attempts` | 3 | audit rounds (workbench) or build attempts (oneshot) |
| `--turns` | 30 | tool turns per workbench round |
| `--timeout-min` | 20 | the time limit, in minutes, for each run of the script and each command in the sandbox |
| `--log` | off | the full log (every event and command) instead of one plain sentence per step |

With the oneshot builder and no `--budget-usd`, the budget is the planned worst case for the model and the paper's
length. `QUICK_PROVIDER` and `QUICK_MODEL` in the environment change the defaults for `--provider` and `--model`.

## What you see on screen

The header names the paper and shows six steps, in the order a run goes through them:

| step | what happens |
|---|---|
| read paper | It fetches the paper's LaTeX from arXiv and inlines its `\input` files. Muse writes a typed spec: the hypothesis, sample, method and every reported number, copied as printed. Code checks that each number is in the LaTeX. |
| check paper | Code checks the paper's own arithmetic: do subgroup counts add up to the total, and which test side does each printed t and p fit? |
| build | Muse writes `replicate.py` in a sandbox, running commands as it goes. Coded checks can send the script back, for example if it types in a number the paper reports. |
| sandbox | Only a clean re-run of the finished script, in a fresh sandbox, counts. Market data the sandbox can't fetch is fetched on the host and the script runs again. |
| audit | The rebuilt sample is compared with the paper's counts, and the script is reviewed twice, independently. A gap or a finding sends it back for another round. |
| verdict | Code compares every number and writes the report. |

Under the steps are the model, the effort, the money spent and the time so far. Once the run ends, a badge says whether
every call went to Meta's models.

Below that is the live log, one plain sentence per step. This is the worked example's log, replayed from its run
folder with `uv run celsus replay d45c71`:

```text
 CELSUS  arXiv 2604.27287 · A Levered ETF Anomaly Explained
 ● read paper ── ● check paper ── ● build ── ● sandbox ── ● audit ── ● verdict
 muse-spark-1.3 · minimal · $0.24 · 3:20 · all on Meta ✓

 ·  Reading the paper with Muse Spark (36,813 characters of LaTeX).
 ·  Found 72 numbers the paper reports.
 ·  Main result: covariance return ratio and index return UPRO annualized = -5.643% in the paper.
 ·  72 of 72 numbers found in the paper exactly as printed.
 ·  Muse is writing code to rebuild the study from public data.
 ·  Running the finished script again in a fresh sandbox.
 !  71 results, but the rebuilt sample doesn't match the paper's counts; Muse tries again.
 ·  Round 2: Muse fixes the script and tries again.
 ·  commands run: 10 · errors hit: 0
 ·  Running the finished script again in a fresh sandbox.
 ✓  71 results, and the rebuilt sample matches the paper's counts.
 ●  Verdict: partly holds up.
```

`--log` shows the full log instead: every event with its step, and every command the builder ran with its output.

The run ends on the verdict card (shortened here):

```text
╭─ 2604.27287 · muse-spark-1.3 ─────────────────────────────────────────────────────────────────────╮
│ The paper's numbers partly hold up: 23 of 25 checked results match within their uncertainty. Its │
│ main result, covariance return ratio and index return UPRO annualized, is -5.643% in the paper   │
│ and -5.691% here (not judged: no standard error).                                                │
│                                                                                                  │
│ claim                                         paper      reproduced                              │
│ winsorized average return ratio VOO           0.983  0.9945 ± 0.011  ✗ paper outside 0.9945 +/-… │
│ winsorized average return ratio UPRO          2.935    2.989 ± 0.03  ✗ paper outside 2.989 +/- … │
│ cumulative return of S&P 500 Index over      0.076%        0.07658%  ✓ 0.8% apart, within 10%    │
│ full sample window                                                                               │
│ ...                                                                                              │
│ … 19 more matched; every row is in the report                                                    │
│                                                                                                  │
│ sample 501/501 · 2 rounds · 16 calls · $0.24 · 3:20                                              │
│ report: runs/run-20261031T141040Z-d45c71/report.md                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Its first line is the verdict in words. The table shows the main result first, then every result that missed, then
the ones that matched. For an estimate, "reproduced" is the value ± its 95% half-width, and the last column is the
rule that decided the row. The footer has the sample size (rebuilt/paper's), rounds, model calls, cost and time, and
the path to the full report.

## The four verdicts

Only results are counted ("checked results"). Sample counts aren't results: they decide whether the results can be
judged at all.

From `compare.verdict`:

A paper **holds up** when every checked result matches, the paper's main result is one of them, and the paper's
sample size could be rebuilt from public data.

It **partly holds up** when some checked results match and some don't. It also partly holds up when all of them
match but the main result wasn't judged (as in the worked example, where it has no standard error), or when the
paper's sample size couldn't be rebuilt from public data.

It **does not hold up** when none of the checked results match and the main result was judged and missed. A paper is
failed only on its main result.

**Could not check** is the checker's own failure, given with its reason. It never counts against the paper.

"Could not check" comes with one of these reasons, all of them in the report's first line:

- the paper's LaTeX source couldn't be read from arXiv;
- no number the extractor reported could be found in the paper;
- the replication never produced results: the data was unavailable, the script failed, or the run stopped at its
  budget or on an error;
- the replication couldn't rebuild the paper's sample (its counts are off by more than the tolerances below), or found
  no observations;
- none of the paper's results could be compared;
- none of the checked results match, but the main result wasn't judged, so the paper isn't failed on the others.

The report's first line starts "We could not check this paper:" and gives the reason.

## When a number matches

Code decides, not a model. The rules (`compare.py`; their published sources are in the README's
[table](../README.md#when-a-number-matches)):

| kind | matches when |
|---|---|
| estimate with a standard error | the paper's value lies inside the replication's 95% interval: value ± 1.96 × se |
| estimate with no sampling error (se 0, such as a return over a fixed period) | it rounds to the value as printed, or else lies within 10% of it |
| estimate with no standard error at all | not judged |
| test statistic | the same conclusion at 5% on the side the paper tested (\|t\| 1.96 two-sided, 1.645 one-sided): a significant result stays significant in the same direction, and a result that isn't significant stays not significant |
| p-value | it is on the same side of 0.05 as the paper's |
| sample total (the largest count, and the totals the paper splits into subgroups) | within 15% of the paper's |
| any other count (a subgroup) | within 15% of the paper's, or else within 1.96 √n; a row this second band passes says so |
| tally (how many tests rejected, breaks found) | as an estimate: inside the 95% interval, or the fixed-number rule when se is 0; not judged without an se |
| a number printed as a bound (< 0.001, > 2) | the replication's value, or its 95% interval, reaches the bound's side |
| parameter (a number the method sets, such as a window length) | not judged |

## What a run writes, and how to check it yourself

Every run writes a folder `runs/<run-id>/`, named `run-<UTC time>-<6 hex>`. The 6-character ending is the short ID
the screens use (d45c71). Start by listing it:

```bash
ls runs/<run-id>
```

For the worked example:

```text
attempt_1.py        calls.jsonl         paper.tex            sandbox_1.log
attempt_1_notes.md  comparison.json     report.md            sandbox_2.log
attempt_2.py        events.jsonl        results.json         spec.json
attempt_2_notes.md  packages.txt        results_attempt.txt  summary.json
```

| file | what it holds |
|---|---|
| `report.md` | The verdict in words on the first line, then every claim with its kind, the paper's value, the replication's value, se, n, whether it matched and why. Then the paper's own arithmetic checks, the guards that fired, the data sources, and the run's calls, tokens and cost. |
| `summary.json` | The verdict, the first line, the main result, the sample counts, how many results were checked and matched, rounds, calls, cost and time. |
| `comparison.json` | Every compared row: name, kind, unit, reported, reproduced, se, n, consistent, why. |
| `spec.json` | The paper as Muse read it: title, hypothesis, data sources, sample, period, method, the main result, and every claim with its value as printed and where it is in the paper. |
| `paper.tex` | The flattened LaTeX the run read. |
| `attempt_N.py`, `attempt_N_notes.md` | Every script the builder wrote, and its notes on each round. |
| `results_attempt.txt` | Which attempt's clean re-run produced the results that were judged. |
| `results.json` | The results that clean re-run wrote. |
| `packages.txt` | Packages the builder installed, which the clean re-run installs at the same versions. |
| `sandbox_N.log` | Each clean re-run's exit code, time, output and errors. |
| `events.jsonl` | The step-by-step log. The screens play this file. |
| `calls.jsonl` | One row per model call: role, provider, model, tokens, cost and request ID. |

To check a verdict yourself:

1. **Read `report.md`.** The first line is the verdict. In the table, the "why" column names the rule behind each
   row. Under "Guards", the caveat lines list every source, proxy or method the replication used in place of the
   paper's: the worked example used public prices in place of the paper's licensed data. "Data sources" says where
   each price series came from and when it was fetched, and every other host the script downloaded from.
2. **Read the script that counted.** `results_attempt.txt` names its attempt:

   ```bash
   cat runs/<run-id>/attempt_$(cat runs/<run-id>/results_attempt.txt).py
   ```

   It is plain Python. Each number should be computed from the data, and the sample built from the paper's
   definition, not cut to the paper's count.
3. **Read its sandbox log**, `sandbox_N.log` for the same N. It has the script's printed counts after each filtering
   step and any errors.
4. **Rerun it.** The script expects the sandbox's layout (`/work`, and the `market_data` module next to it), so the
   way to rerun it as the run did is in a fresh Modal sandbox:

   ```bash
   uv run python - runs/<run-id>/attempt_N.py <<'EOF'
   import sys
   from pathlib import Path
   from dotenv import load_dotenv
   from paper_replicator.replicate import MARKET_CACHE, sandbox_secrets
   from paper_replicator.runs import ROOT
   from paper_replicator.sandbox import run_script

   load_dotenv(ROOT / ".env")
   run = run_script(Path(sys.argv[1]).read_text(), market_cache=MARKET_CACHE, env=sandbox_secrets(),
                    timeout_s=20 * 60)
   print("exit", run.exit_code, "in", run.seconds, "s")
   print(run.files.get("results.json") or run.stderr[-2000:])
   EOF
   ```

   N is the number in `results_attempt.txt`. This makes no model calls; Modal bills the sandbox time. If
   `packages.txt` lists packages, pass them to `run_script` as `packages=(...)`.
5. **Read the cost.** Every model call is a row in `calls.jsonl`:

   ```bash
   uv run python -c "import json, sys; rows = [json.loads(l) for l in open(sys.argv[1])]; print(len(rows), 'calls,', round(sum(r['cost_usd'] or 0 for r in rows), 4), 'USD')" runs/<run-id>/calls.jsonl
   ```

   For the worked example this prints `16 calls, 0.2426 USD`.

The held-out set's 67 runs are in [`receipts/`](../receipts/), with their reports, specs, scripts and call logs, so
you can read real runs without making one. `uv run celsus replay receipts/heldout-set3/<run folder>` plays any of
them.

## Replay, sabotage and batch

### Replay a recorded run

```bash
uv run celsus replay <run-id> --speed 10
```

`<run-id>` is a folder path, or any part of a run ID that matches one folder in `runs/` (the short ID works). The
replay is labelled as one, with the run's ID and the time it was recorded, and ends on its verdict card. `--speed` is
how many times faster than the run took (default 10), `--max-gap` the longest pause in seconds (default 1.5), and
`--log` shows the full log.

### Sabotage

The saboteur takes a finished run of yours, plants one fault at a time, and puts each planted run through the same
checks. There are 14 kinds of plant: broken table arithmetic, a t and p that disagree, a number the paper never
printed, a reference to no result, the paper's result typed into the code, a sample cut or padded to the paper's
count, events outside the paper's period, prices fetched around the market-data module, the authors' code fetched (in
Python or by shell command), a result frozen as a constant, an edited results file, and a secret printed. A session
spends model calls and sandbox time, so give it a budget:

```bash
uv run python -m paper_replicator.sabotage <run-id> --draws 2 --budget-usd 2 --require-provider meta
uv run celsus sabotage <session>
```

The first command writes `runs/sabotage-<UTC time>/` and prints how many plants of each kind were caught. The second
replays that session on screen: each plant, where it was planted, and whether a check caught it ("✓ caught"), it
survived ("✗ survived"), the run failed with no check named ("– run failed"), or it was set aside because the plant
couldn't be applied or changed nothing ("· set aside"). `--types` picks plant kinds (P1, P2, X1, X2, B1 to B7, C1,
R1, K1), and `--no-review` scores the coded checks alone.

### Batch

Many runs of the same paper, and how much the result varies:

```bash
uv run python -m paper_replicator.batch 2604.27287 --n 3 --parallel 3 --effort minimal --budget-usd 1 \
    --require-provider meta
```

Each run is its own process with its own budget stop (`--budget-usd`, default $3 per run). `--batch-budget-usd` stops
launching runs once the next one could take the total past it. The batch writes `runs/batches/<label>.json` and one
log per run, then prints the summary: how often the verdicts agree, how far the main result spreads, and the sample,
guard, round, cost, time and crash figures behind them. To summarise again without running, pass
`--summarise runs/batches/<label>.json`, or `--runs` with run IDs.

## Cost, time and the budget stop

Every run has a budget stop. It is checked after each model call: once spending passes `--budget-usd`, the run stops
at "could not check" with the reason "the run stopped (BudgetExceeded)". The call that crosses the line still
finishes, so a run can end a little over: held-out run 8c6cf6 stopped at $2.0094 of a $2.00 budget. The default is
$3.00 with the workbench builder.

The budget and `calls.jsonl` count model calls only. Modal bills sandbox time to your Modal account.

What runs cost and take (the worked example from its run files, the rest from the README):

- the worked example above: $0.24 and 3:20, Muse Spark at minimal effort;
- one tuning paper, three runs per model: $0.20 a run on Muse Spark at minimal effort, and $1.75 a run on Muse Wonder
  at max effort;
- the held-out set: a median of 35 minutes and $1.34 a run at list prices, on Muse Spark Open at effort xhigh with a
  $2 budget stop. 5 of its 63 finished runs stopped at that budget.

Prices per model are in `src/paper_replicator/pricing.py`, with the date each was read. A model missing from that
table is unpriced, and since every run has a budget stop, a run on it stops after its first call (see
[Troubleshooting](#troubleshooting)).

## Which papers it can check

A paper can be checked when it is on arXiv with its LaTeX source, its data is public and a script can fetch it,
and the analysis fits the time limit.

The run fetches the source from `arxiv.org/src/<id>`. A PDF-only paper ends at "could not check" because the LaTeX
couldn't be read.

In the sandbox the script can get:

- market prices through the `market_data` module (`get_prices`, `get_market_cap`, `get_profile`): the run's
  cache in `data/market/` first, then yfinance in the sandbox, then a fetch on your machine into the cache;
- SEC EDGAR filings from sec.gov, with your `SEC_USER_AGENT`;
- anything else a Python script can download from a public host: macro series, exchange data, data files. The report
  lists every host the script fetched from.

The sandbox has pandas, numpy, scipy, statsmodels, requests, yfinance and pyarrow, and the builder can install other
packages. The time limit is `--timeout-min`, 20 minutes per run of the script by default.

The builder may not fetch the authors' code or any repository: rerunning their code isn't replicating the paper.

When a paper uses licensed data, the builder can substitute public data, and the report lists every substitution as a
caveat (the worked example's paper uses CRSP; the run used public prices). If public data can't give the paper's
sample size, the run declares it, and the paper can at most partly hold up. When the sample can't be rebuilt within
the tolerances, the verdict is "could not check".

The method was tested on finance and economics papers, whose data (prices, filings, macro series) is public. In the
held-out set, 28 of 63 finished runs ended at "could not check", and 5 more at the budget stop.

## Troubleshooting

| what you see | why | what to do |
|---|---|---|
| `the run did not start; see runs/cli_last_run.out`, and that file ends with `MissingKeyError: MODEL_API_KEY is not set: add it to .env` | no Meta API key | Put your key in `.env` as `MODEL_API_KEY=...`. |
| After the paper is read: `The run stopped: AuthError: Token missing. Could not authenticate client. …` | no Modal token on this machine | Run `uv run modal token new`, then check the paper again. |
| `The run stopped: BudgetExceeded: spent $2.0094 of a $2.0000 budget`, and the verdict is "could not check" | the run reached its budget stop | Raise `--budget-usd`, or lower `--effort`. |
| `BudgetExceeded: <model> is unpriced, so the budget cannot be enforced` | the model isn't in the price table | Pick a model from `pricing.py`, or add its prices in `providers.local.json`. |
| `We could not check this paper: this run allows only meta models, and the extractor's call goes to <model> on <provider>.` | `--require-provider meta` with a model that isn't Meta's | Drop `--require-provider`, or choose a Meta model with `--model`. |
| `The run stopped: KeyError: 'SEC_USER_AGENT'` | the `SEC_USER_AGENT` line is missing from `.env` | Copy it from `.env.example` and fill it in. |
| `We could not check this paper: the paper's LaTeX source could not be read from arXiv (…)` | the paper has no LaTeX source, the ID is wrong, or arXiv didn't answer | Check the ID on arxiv.org; a PDF-only paper can't be checked. |
| `celsus check: error: unrecognized arguments: …` | a mistyped option | `uv run celsus check -h` lists them. Nothing was started or spent. |

When a run stops at its budget or on an error, its folder still has everything written up to that point, `report.md`
included. A run that didn't start (the first row) writes no folder.

## Tests

```bash
uv run pytest -q
```

The tests run offline: the agents talk to a fake model endpoint, the sandbox is a fake too, and the guards are tested on
real scripts from live runs (`tests/corpus/`). They need no key and no Modal token.
