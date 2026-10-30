# paper-replicator

[![tests](https://github.com/0ywfe/paper-replicator/actions/workflows/tests.yml/badge.svg)](https://github.com/0ywfe/paper-replicator/actions/workflows/tests.yml)

Give it an arXiv paper. It reads the paper's LaTeX, writes down every number the paper reports, rebuilds the analysis on public data in a sandbox, and tells you in plain words whether the published numbers hold up.

```
The paper's numbers partly hold up: 14 of 15 checked results match within their uncertainty.
Its main result, overall_mean_return, is -3.07% in the paper and -3.086% here (consistent).
```

Built during the Meta AI Developer Hackathon (Oct–Nov 2026). It runs on any OpenAI-compatible endpoint; the defaults, and every number in this README, are Meta's Muse models.

**See it in 30 seconds, with no API key:**

```bash
uv sync
uv run paper-replicator demo     # replays a held-out run shipped with the package, labelled as a replay
```

The demo is run 25b01b from the held-out set below (arXiv 2610.04221, robust enhanced index tracking): 84 of 84 checked results match, its main result 0.4531 in the paper and 0.4482 ± 0.2654 here. Its report and the script that produced it are in `src/paper_replicator/cli/demo/`.

## How we know it works

### A held-out set nobody had looked at

32 finance and economics papers from arXiv (Sep 2025 to Oct 2026), drawn by a rule written down before any run: public data a script can fetch, LaTeX source, about 30 minutes of compute, no paper seen during development. Abstracts were read with their numbers masked, and every paper whose results someone had glimpsed was dropped. The list was frozen before the first run.

Each paper ran twice on Muse Spark Open at effort xhigh, with a $2 budget stop per run. 63 runs finished, with a median of 35 minutes and $1.34 at list prices. Four runs the host cut off were set aside as infrastructure; three were run again, and one paper's second run stopped after its second cut. The headline, as run, on the code frozen for the test:

| verdict | runs |
|---|---|
| holds up | 1 |
| partly holds up | 26 |
| does not hold up | 3 |
| could not check | 28 |
| could not check (the $2 budget stop) | 5 |

"Could not check" is the checker's own failure, given with its reason: the data was unavailable, the sample couldn't be rebuilt, the code broke a rule, or nothing comparable came out. It never counts against the paper.

Replay of the same stored attempts under the post-headline scorer: holds up 1, partly holds up 27, does not hold up 0, could not check 30, could not check (budget) 5. This is not a fresh test, as the fixes were written after reading these runs. The three "does not hold up" each missed every number checked while the paper's main result was never computed; a paper now fails only on its main result. One compound sample period was misread. One run lost to a false alarm (8dd383) has no results to re-score.

### Two independent reviews, read finding by finding

Every script is reviewed twice, independently, and a finding from either review sends it back. In the held-out set, 46 findings came from only one of the two reviews; each was read against the script by hand: 43 true, 2 borderline, 1 false. No false or borderline finding decided a verdict.

### A saboteur

The sabotage battery plants faults into honest runs (results typed in from the paper, samples cut or padded to the paper's count, synthetic data, altered paper numbers) and counts what the checks catch. Of 116 viable plants, the coded checks alone catch 94; with one review, 106 (91.4%); with the union of two reviews, 108 (93.1%). The reviews raised no false alarm in 12 reviews of honest scripts. Ten secret-leak plants are equivalent mutants (the sandbox only ever gets a stand-in for the secret) and are left out of the 116.

### Tests and a regression gate

The test suite runs offline on every push (the badge above): model calls, the sandbox and market data are faked, and the guards are tested on real scripts from live runs. Before any change merges, a regression gate re-scores every stored run (215) and re-checks every stored plant (130); a verdict that changes has to be named, with its reason, in its own commit. The stored runs themselves are not in this repository.

### Open weights

Every model call in the held-out set, 3,172 of them ($84.11 at list prices), ran on Muse Spark Open, Meta's open-weights model, served by Fireworks and Baseten: the reading of the paper, the build, and both reviews.

## The judging criteria, and where to see each

| criterion | evidence |
|---|---|
| Impact | Published results that don't replicate cost the people who build on them: Amgen reproduced 6 of 53 landmark cancer studies (Begley & Ellis, Nature 2012), and about two-thirds of 452 published asset-pricing anomalies fail to replicate (Hou, Xue & Zhang 2020). This checks a paper end to end, from its LaTeX to a verdict in plain words, in a median of 35 minutes and $1.34. The held-out headline above is what it does on papers nobody had looked at. |
| Use of Meta AI tooling | Muse reads the paper into a typed spec, chooses the main result, builds the replication as an agent with tools in a sandbox, and reviews its own script twice. Muse Spark Open did every call of the held-out set; Muse Spark and Muse Wonder run behind the same flag (`--model`). |
| Technical depth | Code, not a model, judges every number, with tolerances from published replication practice (table below). Coded guards stop typed-in results, samples trimmed or padded to a count, and fetching the authors' code; the saboteur measures them; the regression gate pins them. |
| Demo | `uv run paper-replicator demo` replays a held-out run with no key. `paper-replicator check <arxiv id>` runs a paper live, with each role on screen. |

## How it checks a paper

1. **Read.** The arXiv source is fetched and its `\input` files inlined. Muse writes a typed spec: the hypothesis, sample, method steps and every reported number, each copied exactly as printed.
2. **Ground.** Code checks that every number in the spec appears in the LaTeX, and that every cross-reference names a real claim. A spec with bad references gets one more attempt with the problems listed.
3. **Check the paper's own arithmetic.** Do the subgroup counts add up to the total? Which p-value does each printed t actually give, at the precision both are printed to? (This is how one-tailed tests are found.)
4. **Build.** Muse works inside a Modal sandbox with `run` and `write_file` tools: it explores the data, writes `replicate.py` and runs it.
5. **Re-run clean.** Only an independent run of the final script, in a fresh sandbox, counts.
6. **Audit.** If the rebuilt sample doesn't match the paper's counts, the builder gets the gap back and tries again. It is never told to hit a number.
7. **Judge.** Code, not a model, compares each number (rules below) and writes the report.

### When a number "matches"

The tolerances come from published replication practice, not from a chosen percentage. The one that doesn't, an allowance for small subgroup counts, says so in every report row it passes:

| kind | consistent when | source |
|---|---|---|
| estimate with a standard error | the paper's value lies inside the reproduction's 95% interval | the "original inside replication CI" criterion |
| number with no sampling error (a return over a fixed period, a ratio) | it rounds to the value as printed, or else lies within 10% of it | exact reproduction: Baek & Pradel, arXiv 2602.10046; 10% threshold: Hans & Bilionis, arXiv 2607.02134 |
| test statistic | the same conclusion at 5% on the side the paper tested: significant results stay significant in the same direction, null results stay null whatever their sign | Open Science Collaboration (2015) |
| p-value | same side of 0.05 | |
| sample total (the largest count, and the totals of the paper's partitions) | within ±15% of the paper's | SCORE's tolerance for sample size: Miske et al. (2026), Nature 652:126–134 |
| any other count (a subgroup) | within ±15% of the paper's, or else within 1.96 √n | SCORE, as above; the √n band, an allowance for small subgroups (the wider of the two below about 171), has no published source |

### Honest verdicts

- **holds up / partly holds up / does not hold up**: the share of checked numbers that match.
- **could not check**: the checker's own failure, given with its reason: the data was unavailable, the sample couldn't be rebuilt, or the code crashed. The checker never blames a paper for its own failure.

### Guards that keep it honest

- Numbers the paper reports may not appear in the code, and the sample may not be trimmed or padded to a reported count.
- Market data goes through one logged module (cache, then yfinance, then a host-side fetch), and the report says which source and fetch date each series came from. Anything else the script downloads in Python (filings, macro series, exchange prices) is recorded by host, and the report lists those hosts too.
- The builder may not fetch the authors' code: re-running their code isn't replicating the paper. Data files are fine.
- Secrets are redacted from everything the model sees, and every run has a budget stop.

### Limitations

- Papers that report no standard error anywhere can't have their estimates judged: 357afb's 170 estimates (148 of them exactly the paper's) were all left unjudged, and the run could not check the paper.
- Two coded checks raised false alarms that decided held-out verdicts: a minimum-length check read as cutting the sample to the paper's count (8dd383), and a sample period printed as two dates read as the first (dcb75d). Both were fixed after the headline.
- A count written as the paper's value passes the coded checks when it can't be told from a design count (a number of draws, sectors or windows). Of 97 such counts in the stored runs, the reviews named 13.
- The coded checks don't trace random draws into the sample, so a synthetic sample declared as the paper's is the reviews' to catch: in 07f67a one of the two reviews caught it.

- A result built from the paper's own numbers (another claim times a constant, or draws that cancel to a constant) is caught when the script writes it as arithmetic on names and literals, including numbers spelled as text or string lengths. It is not yet caught through dict or list constants, `max`, `np.where` or helper functions, or `**` and `+` forms.
- Counts that are not the sample total pass within SCORE's 15%, or else within 1.96 √n. That band has no published source; it is kept for small subgroups until an off subgroup count leaves only its own results unjudged.

## Use

```bash
uv sync
cp .env.example .env            # MODEL_API_KEY, SEC_USER_AGENT
uv run modal token new          # the sandbox runs on Modal

# check a paper and watch it live: stage tracker, live log, verdict card
uv run python -m paper_replicator.cli check 2512.06144 --model muse-spark-1.3 --require-provider meta

# replay a recorded run (labelled as a replay, with its run ID and date)
uv run python -m paper_replicator.cli replay <run-id> --speed 10

# replay the held-out run shipped with the package: no API key, no Modal token
uv run paper-replicator demo

# many runs, and how reliable the result is
uv run python -m paper_replicator.batch 2512.06144 --n 5 --parallel 5 --model muse-spark-1.3 --effort minimal \
    --require-provider meta
```

### Models

A run defaults to Meta's Muse Spark (`muse-spark-1.3`) in every role; `--model muse-wonder-1.0` runs it on Muse Wonder, and `--effort` sets the reasoning effort (minimal to max) of the extractor, chooser and builder; the script is reviewed twice, independently, always at high whatever the run's effort, and a finding from either review sends it back. Any other OpenAI-compatible endpoint can be added in a local `providers.local.json` (format in `src/paper_replicator/local.py`) and chosen with `--provider`. `--require-provider meta` stops a run before any call that would go elsewhere; every benchmark here ran with it.

Each run writes `runs/<run-id>/`: `report.md` (the first line is the plain-words verdict), `comparison.json`, the spec, every script the builder wrote, sandbox logs, `events.jsonl`, and `calls.jsonl` (provider, model, tokens and cost of every call).

## Tests

```bash
uv run pytest
```

Offline only: the Agents SDK talks to a fake OpenAI-compatible endpoint, and the sandbox is a fake too. Guards are regression-tested on real scripts from live runs (`tests/corpus/`).

---

Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
