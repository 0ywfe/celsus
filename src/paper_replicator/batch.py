"""Run a batch of replications and measure how reliable the result is.

    uv run python -m paper_replicator.batch 2512.06144 --n 4 --model muse-spark-1.3 --effort minimal
    uv run python -m paper_replicator.batch --summarise runs/batches/<label>.json

Each run is its own process with its own budget stop; the batch also stops launching runs once the
next one could take its spend past --batch-budget-usd. The summary turns the runs' summary.json files
into the reliability numbers: how often the verdicts agree, how far the headline number spreads, and
the sample, guard, round, cost, time and crash figures behind them.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

from .runs import ROOT, RUNS_DIR

BATCHES = RUNS_DIR / "batches"
_RUN_ID = re.compile(r"\[ingest\] (run-\S+):")


def log_path(label: str, paper: str, i: int) -> Path:
    """One log per run. The paper is in the name: with only the run index, every paper's first run
    wrote the same file and the run IDs read back from it were wrong (batch dev-spark-min-1)."""
    return BATCHES / f"{label}.{paper}.{i}.out"


async def _one(paper: str, args: argparse.Namespace, gate: asyncio.Semaphore, label: str, i: int) -> str | None:
    command = [sys.executable, "-m", "paper_replicator.replicate", paper, "--budget-usd", str(args.budget_usd),
               "--attempts", str(args.attempts), "--turns", str(args.turns), "--builder", args.builder]
    for flag in ("provider", "model", "effort", "require_provider"):
        if getattr(args, flag):
            command += [f"--{flag.replace('_', '-')}", getattr(args, flag)]
    async with gate:
        log = log_path(label, paper, i)
        with log.open("w") as out:
            process = await asyncio.create_subprocess_exec(*command, cwd=ROOT, stdout=out, stderr=out)
            await process.wait()
        match = _RUN_ID.search(log.read_text())
        return match.group(1) if match else None


async def run_batch(papers: list[str], args: argparse.Namespace, label: str) -> list[str]:
    """Launch in waves of --parallel, checking the batch ceiling before each wave."""
    jobs = [(paper, i) for paper in papers for i in range(args.n)]
    run_ids: list[str] = []
    gate = asyncio.Semaphore(args.parallel)
    while jobs:
        spent = sum(_summary(r).get("cost_usd", 0) for r in run_ids if _summary(r))
        room = int((args.batch_budget_usd - spent) // args.budget_usd) if args.batch_budget_usd else len(jobs)
        wave, jobs = jobs[:max(0, min(args.parallel, room))], jobs[max(0, min(args.parallel, room)):]
        if not wave:
            print(f"batch ceiling: ${spent:.2f} spent, next run could pass ${args.batch_budget_usd}; stopping")
            break
        ids = await asyncio.gather(*(_one(paper, args, gate, label, i) for paper, i in wave))
        run_ids += [r for r in ids if r]
        (BATCHES / f"{label}.json").write_text(json.dumps({"label": label, "args": vars(args), "papers": papers,
                                                           "run_ids": run_ids}, indent=1))
    return run_ids


def _summary(run_id: str) -> dict:
    path = RUNS_DIR / run_id / "summary.json"
    return json.loads(path.read_text()) if path.is_file() else {}


def _g(value) -> str:
    """A number for the table: 4 significant figures, or a dash."""
    return "–" if value is None else f"{value:.4g}"


def _spread(values: list[float]) -> dict:
    if not values:
        return {}
    return {"n": len(values), "min": min(values), "max": max(values), "mean": round(statistics.mean(values), 4),
            "sd": round(statistics.stdev(values), 4) if len(values) > 1 else 0.0}


def summarise(run_ids: list[str]) -> dict:
    """Reliability per paper and model. Headlines are matched across runs by the reported value, which is
    grounded in the LaTeX and stable, while claim names vary from run to run."""
    groups: dict[tuple, list[dict]] = {}
    for run_id in run_ids:
        s = _summary(run_id)
        if s:
            groups.setdefault((s["paper"], s["model"], s["effort"] or "default", s["builder"]), []).append(s)
    out = []
    for (paper, model, effort, builder), runs in sorted(groups.items()):
        verdicts = Counter(r["verdict"] for r in runs)
        mode, mode_count = verdicts.most_common(1)[0]
        headlines = [r["headline"] for r in runs if r.get("headline")]
        reported = Counter(h["reported"] for h in headlines).most_common(1)
        main = reported[0][0] if reported else None
        same = [h for h in headlines if h["reported"] == main]
        totals = [max((c["reproduced"] for c in r["sample"] if c["reproduced"] is not None), default=None)
                  for r in runs]
        out.append({
            "paper": paper, "model": model, "effort": effort, "builder": builder, "n": len(runs),
            "verdicts": dict(verdicts), "agreement": round(mode_count / len(runs), 3), "modal_verdict": mode,
            "headline_reported": main,
            "headline_reproduced": _spread([h["reproduced"] for h in same if h["reproduced"] is not None]),
            "headline_consistent": sum(1 for h in same if h["consistent"]),
            "sample_total": _spread([t for t in totals if t is not None]),
            "rejections": sum(len(r["rejections"]) for r in runs),
            "rounds": _spread([r["rounds"] for r in runs]),
            "cost_usd": _spread([r["cost_usd"] for r in runs]),
            "wall_s": _spread([r["wall_s"] for r in runs]),
            "crashed": sum(1 for r in runs if r["crashed"]),
            "run_ids": [r["run_id"] for r in runs],
        })
    return {"groups": out, "models": by_model(out)}


def by_model(groups: list[dict]) -> list[dict]:
    """Across papers, per model and effort: how many papers, how the verdicts fell, how often the checker could
    not check, how often a paper's runs agreed, and what it cost."""
    models: dict[tuple, list[dict]] = {}
    for g in groups:
        models.setdefault((g["model"], g["effort"]), []).append(g)
    out = []
    for (model, effort), gs in sorted(models.items()):
        verdicts = Counter()
        for g in gs:
            verdicts.update(g["verdicts"])
        runs = sum(g["n"] for g in gs)
        repeated = [g for g in gs if g["n"] > 1]
        out.append({
            "model": model, "effort": effort, "papers": len(gs), "runs": runs, "verdicts": dict(verdicts),
            "could_not_check": round(verdicts.get("could not check", 0) / runs, 3),
            "papers_all_runs_agree": f"{sum(1 for g in repeated if g['agreement'] == 1)}/{len(repeated)}",
            "cost_usd_mean": round(sum(g["cost_usd"].get("mean", 0) * g["n"] for g in gs) / runs, 4),
            "crashed": sum(g["crashed"] for g in gs),
        })
    return out


def markdown(summary: dict) -> str:
    lines = ["| paper | model | effort | n | verdicts | agreement | headline paper → reproduced (min–max, sd) | "
             "consistent | sample total (min–max) | rejections | rounds (mean) | cost mean (max) | wall mean | crashed |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for g in summary["groups"]:
        h, t, c, w, r = g["headline_reproduced"], g["sample_total"], g["cost_usd"], g["wall_s"], g["rounds"]
        verdicts = ", ".join(f"{k} {v}" for k, v in g["verdicts"].items())
        lines.append(
            f"| {g['paper']} | {g['model']} | {g['effort']} | {g['n']} | {verdicts} | {g['agreement']:.0%} | "
            f"{_g(g['headline_reported'])} → {_g(h.get('min'))}–{_g(h.get('max'))} (sd {_g(h.get('sd'))}) | "
            f"{g['headline_consistent']}/{h.get('n', 0)} | {_g(t.get('min'))}–{_g(t.get('max'))} | "
            f"{g['rejections']} | {r.get('mean', '–')} | ${c.get('mean', 0):.2f} (${c.get('max', 0):.2f}) | "
            f"{w.get('mean', 0):.0f}s | {g['crashed']} |")
    if len(summary.get("models", [])) and len(summary["groups"]) > 1:
        lines += ["", "| model | effort | papers | runs | verdicts | could not check | papers whose runs agree | "
                  "cost per run | crashed |", "|---|---|---|---|---|---|---|---|---|"]
        for m in summary["models"]:
            verdicts = ", ".join(f"{k} {v}" for k, v in m["verdicts"].items())
            lines.append(f"| {m['model']} | {m['effort']} | {m['papers']} | {m['runs']} | {verdicts} | "
                         f"{m['could_not_check']:.0%} | {m['papers_all_runs_agree']} | ${m['cost_usd_mean']:.2f} | "
                         f"{m['crashed']} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("papers", nargs="*")
    parser.add_argument("--n", type=int, default=3, help="runs per paper")
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--require-provider", help="stop any run before a call to another provider")
    parser.add_argument("--builder", default="workbench")
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--turns", type=int, default=30)
    parser.add_argument("--budget-usd", type=float, required=False, default=3.0, help="budget stop per run")
    parser.add_argument("--batch-budget-usd", type=float, default=None, help="stop launching past this total")
    parser.add_argument("--label")
    parser.add_argument("--summarise", help="a batch file to summarise instead of running")
    parser.add_argument("--runs", nargs="*", help="run IDs to summarise instead of running")
    args = parser.parse_args()
    BATCHES.mkdir(parents=True, exist_ok=True)
    if args.summarise or args.runs:
        run_ids = args.runs or json.loads(Path(args.summarise).read_text())["run_ids"]
    else:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        label = args.label or f"batch-{stamp}-{args.model or 'default'}-{args.effort or 'default'}"
        run_ids = asyncio.run(run_batch(args.papers, args, label))
    summary = summarise(run_ids)
    print(markdown(summary))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
