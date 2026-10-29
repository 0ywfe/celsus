# paper-replicator

Give it an arXiv paper. It reads the paper's LaTeX, writes down every number the paper reports, rebuilds the analysis on public data in a sandbox, and tells you in plain words whether the published numbers hold up.

```
The paper's numbers partly hold up: 14 of 15 checked results match within their uncertainty.
Its main result, overall_mean_return, is -3.07% in the paper and -3.086% here (consistent).
```

Built during the Meta AI Developer Hackathon (Oct–Nov 2026). It runs on any OpenAI-compatible endpoint; the defaults, and every number in this README, are Meta's Muse models.

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

# many runs, and how reliable the result is
uv run python -m paper_replicator.batch 2512.06144 --n 5 --parallel 5 --model muse-spark-1.3 --effort minimal \
    --require-provider meta
```

### Models

A run defaults to Meta's Muse Spark (`muse-spark-1.3`) in every role; `--model muse-wonder-1.0` runs it on Muse Wonder, and `--effort` sets the reasoning effort (minimal to max). Any other OpenAI-compatible endpoint can be added in a local `providers.local.json` (format in `src/paper_replicator/local.py`) and chosen with `--provider`. `--require-provider meta` stops a run before any call that would go elsewhere; every benchmark here ran with it.

Each run writes `runs/<run-id>/`: `report.md` (the first line is the plain-words verdict), `comparison.json`, the spec, every script the builder wrote, sandbox logs, `events.jsonl`, and `calls.jsonl` (provider, model, tokens and cost of every call).

## Tests

```bash
uv run pytest
```

Offline only: the Agents SDK talks to a fake OpenAI-compatible endpoint, and the sandbox is a fake too. Guards are regression-tested on real scripts from live runs (`tests/corpus/`).

---

Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
