# Rules for coding agents in this repo

- Same treatment for every paper: nothing in `src/` may be special-cased for one paper. Anything that only helps one paper is overfitting.
- A checker never blames a paper for its own failure: when the run, the data or the rebuilt sample fails, the verdict is "could not check", with the reason.
- The product name lives in one place: `name` in `pyproject.toml` plus `PRODUCT_NAME` in `src/paper_replicator/__init__.py`. Never hard-code it anywhere else.
- Never print, log or commit API keys. `.env` is gitignored.
- Tests never call a live API: they use the fake endpoint in `tests/fake_api.py`. Every live run has a budget stop.
- Every model call is logged (provider, model, tokens, cost) to `runs/<run-id>/calls.jsonl`.
- Reports say whether a paper's published numbers reproduce, never what to trade.
