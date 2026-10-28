# paper-replicator

Give it an arXiv paper. It reads the paper's LaTeX, writes down every number the paper reports, rebuilds the analysis on public data in a sandbox, and tells you in plain words whether the published numbers hold up.

```
The paper's numbers partly hold up: 14 of 15 checked results match within their uncertainty.
Its main result, overall_mean_return, is -3.07% in the paper and -3.086% here (consistent).
```

Built during the Meta AI Developer Hackathon (Oct–Nov 2026). Every model call goes to Meta's Muse models.

## How it checks a paper

1. **Read.** The arXiv source is fetched and its `\input` files inlined. Muse writes a typed spec: the hypothesis, sample, method steps and every reported number, each copied exactly as printed.
2. **Ground.** Code checks that every number in the spec appears in the LaTeX, and that every cross-reference names a real claim. A spec with bad references gets one more attempt with the problems listed.
3. **Check the paper's own arithmetic.** Do the subgroup counts add up to the total? Which p-value does each printed t actually give, at the precision both are printed to? (This is how one-tailed tests are found.)
4. **Build.** Muse works inside a Modal sandbox with `run` and `write_file` tools: it explores the data, writes `replicate.py` and runs it.
5. **Re-run clean.** Only an independent run of the final script, in a fresh sandbox, counts.
6. **Audit.** If the rebuilt sample doesn't match the paper's counts, the builder gets the gap back and tries again. It is never told to hit a number.
7. **Judge.** Code, not a model, compares each number (rules below) and writes the report.

### When a number "matches"

The tolerances come from the data and from published replication practice, not from a chosen percentage:

| kind | consistent when | source |
|---|---|---|
| estimate with a standard error | the paper's value lies inside the reproduction's 95% interval | the "original inside replication CI" criterion |
| number with no sampling error (a return over a fixed period, a ratio) | it rounds to the value as printed, or else lies within 10% of it | exact reproduction: Baek & Pradel, arXiv 2602.10046; 10% threshold: Hans & Bilionis, arXiv 2607.02134 |
| test statistic | the same conclusion at 5% on the side the paper tested: significant results stay significant in the same direction, null results stay null whatever their sign | Open Science Collaboration (2015) |
| p-value | same side of 0.05 | |
| count | within 1.96 √n | Poisson |

### Honest verdicts

- **holds up / partly holds up / does not hold up**: the share of checked numbers that match.
- **could not check**: the checker's own failure, given with its reason: the data was unavailable, the sample couldn't be rebuilt, or the code crashed. The checker never blames a paper for its own failure.

### Guards that keep it honest

- Numbers the paper reports may not appear in the code, and the sample may not be trimmed or padded to a reported count.
- Market data goes through one logged module (cache, then yfinance, then a host-side fetch), and the report says which source and fetch date each series came from.
- The builder may not fetch the authors' code: re-running their code isn't replicating the paper. Data files are fine.
- Secrets are redacted from everything the model sees, and every run has a budget stop.

## Use

```bash
uv sync
cp .env.example .env            # MODEL_API_KEY, SEC_USER_AGENT
uv run modal token new          # the sandbox runs on Modal

# check a paper and watch it live: stage tracker, live log, verdict card
uv run python -m paper_replicator.cli check 2512.06144 --model muse-spark-1.3 --builder workbench

# replay a recorded run (labelled as a replay, with its run ID and date)
uv run python -m paper_replicator.cli replay <run-id> --speed 10

# many runs, and how reliable the result is
uv run python -m paper_replicator.batch 2512.06144 --n 5 --parallel 5 --model muse-spark-1.3 --effort minimal
```

Each run writes `runs/<run-id>/`: `report.md` (the first line is the plain-words verdict), `comparison.json`, the spec, every script the builder wrote, sandbox logs, `events.jsonl`, and `calls.jsonl` (provider, model, tokens and cost of every call).

## Tests

```bash
uv run pytest
```

Offline only: a real OpenAI client on a fake transport, and a fake sandbox. Guards are regression-tested on real scripts from live runs (`tests/corpus/`).

---

Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
