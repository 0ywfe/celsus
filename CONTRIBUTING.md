# Contributing to celsus

Pull requests are welcome, from small bug fixes to new checks. Here is how to set up the project, what the tests expect, and the rules every change has to follow.

## Before you start

For anything bigger than a small fix, open an issue first and describe the change, so we can agree on the approach before you put time into it. For a bug report, include the command you ran, the run ID, and the relevant lines from `runs/<run-id>/report.md` or `events.jsonl`. Never paste API keys.

## Setup

```bash
git clone https://github.com/0ywfe/celsus.git
cd celsus
uv sync
uv run pytest
```

The test suite runs offline. Model calls go to a fake endpoint (`tests/fake_api.py`), and the sandbox and market data are faked too, so you need no API key and no Modal token to run it. CI runs the same suite on every push and pull request.

A live run (`uv run celsus check ...`) needs a model key and a Modal token; [`docs/USAGE.md`](docs/USAGE.md) explains both. Set `--budget-usd` on every live run.

## Rules for every change

These come from [`AGENTS.md`](AGENTS.md) and apply to people and coding agents alike.

- Every paper gets the same treatment. Nothing in `src/` may be special-cased for one paper.
- A checker never blames a paper for its own failure. When the run, the data or the rebuilt sample fails, the verdict is "could not check", with the reason.
- Code judges the numbers, not a model. A new tolerance needs a source in published replication practice, cited next to it in the code.
- Tests never call a live API.
- Never print, log or commit API keys. `.env` is gitignored.
- The product name appears only in `name` in `pyproject.toml` and `PRODUCT_NAME` in `src/paper_replicator/__init__.py`.
- Reports say whether a paper's published numbers reproduce, never what to trade.

## Tests

- Every change comes with a test. A bug fix comes with a test that fails without the fix.
- A change to a guard should add the real script that triggered it to `tests/corpus/` where possible, so the guard is tested on real output.

## The regression gate

Before a change merges, we re-score every stored run and re-check every stored sabotage plant. Most stored runs are not in this repository, so this step runs on our side after you open the pull request. If your change moves a verdict, we will tell you which one and why, and that change lands in its own commit with the reason in the message.

## Pull requests

- Branch from `main` and keep one change per pull request.
- Write commit messages as `type: description`, where the type is feat, fix, docs, test, refactor or chore.
- In the description, say what changed, why, and how you tested it. If you ran a live check, include the run ID and its cost.
- Sign the [Contributor License Agreement](CLA.md) before your first pull request can merge. A bot posts the sentence to reply with; you sign once and it covers every later pull request.

## Licensing

The project is released under [AGPL-3.0-only](LICENSE), and your contribution is too. The CLA also lets the maintainer offer the project under other terms, such as a commercial licence. You keep the copyright in your work.