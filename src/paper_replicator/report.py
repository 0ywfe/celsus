"""The one-page run report: verdict, reported vs reproduced, guards, data sources, cost."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from . import DISCLAIMER, PRODUCT_NAME


def _fmt(value) -> str:
    return "" if value is None else f"{value:.4g}" if isinstance(value, float) else str(value)


def market_sources(log: list[dict]) -> list[str]:
    counts = Counter((e["kind"], e["source"], e["fetched"]) for e in log)
    tickers = {key: len({e["ticker"] for e in log if (e["kind"], e["source"], e["fetched"]) == key}) for key in counts}
    return [f"- {kind}: {source}, fetched {fetched}, {tickers[(kind, source, fetched)]} tickers"
            for kind, source, fetched in sorted(counts)]


def write(folder: Path, *, arxiv_id: str, title: str, verdict: str, rows: list[dict], rejected: list[dict],
          paper_checks: list[dict],
          guard_events: list[str], market_log: list[dict], calls: list[dict], sandbox_note: str) -> Path:
    providers = sorted({c["provider"] for c in calls})
    lines = [
        f"# {PRODUCT_NAME} report: arXiv {arxiv_id}",
        f"**{title}**", "",
        f"Verdict: **{verdict}**", "",
        "| claim | kind | reported | reproduced | se | n | consistent | why |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| {r['name']} | {r['kind']} | {_fmt(r['reported'])}{r['unit']} | {_fmt(r['reproduced'])} | "
          f"{_fmt(r['se'])} | {_fmt(r['n'])} | {_fmt(r['consistent'])} | {r['why']} |" for r in rows],
        "", "## The paper's own numbers",
        *([f"- {'ok' if c['ok'] else 'FLAG'}: {c['text']}" for c in paper_checks] or ["- nothing to check"]),
        "", "## Guards",
        *([f"- rejected claim {r['name']} = {r['value']}: {r['reason']}" for r in rejected] or ["- no claims rejected"]),
        *[f"- {event}" for event in guard_events], "",
        "## Market data", *(market_sources(market_log) or ["- none used"]), "",
        "## Run",
        f"- sandbox: {sandbox_note}",
        f"- model calls: {len(calls)}, providers: {', '.join(providers) or 'none'}, "
        f"all on Meta: {'yes' if providers == ['meta'] else 'no'}",
        f"- tokens: in {sum(c['input_tokens'] for c in calls)}, out {sum(c['output_tokens'] for c in calls)} "
        f"(reasoning {sum(c['reasoning_tokens'] for c in calls)}); cost ${sum(c['cost_usd'] or 0 for c in calls):.4f}",
        "", "---", DISCLAIMER, "",
    ]
    path = folder / "report.md"
    path.write_text("\n".join(lines))
    (folder / "comparison.json").write_text(json.dumps({"verdict": verdict, "rows": rows}, indent=1))
    return path
