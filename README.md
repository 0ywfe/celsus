# paper-replicator

Give it a research paper. It reads the paper, rebuilds the method, reruns it on public data, and reports whether the published numbers reproduce.

Status: under construction, built during the Meta AI Developer Hackathon (Oct to Nov 2026).

## Setup

```bash
uv sync
cp .env.example .env    # add MODEL_API_KEY
uv run python -m paper_replicator.check_day1
```

---

Not financial advice. It checks what academics published. AI can make mistakes: check the code and data in the report.
