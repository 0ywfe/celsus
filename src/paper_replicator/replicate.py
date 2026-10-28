"""One paper end to end: LaTeX -> spec -> grounded claims -> script -> sandbox -> comparison -> verdict.

    uv run python -m paper_replicator.replicate 2512.06144

Everything lands in runs/<run-id>/; events.jsonl is the stage-by-stage log a frontend can follow.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from agents import Agent, MaxTurnsExceeded, Runner
from dotenv import load_dotenv
from openai import AsyncOpenAI

from . import config, guards, market, report, roles
from .paper_checks import check_paper
from .compare import COULD_NOT_CHECK, compare, first_line, verdict
from .ingest import load_paper
from .ledger import Ledger
from .llm import make_client
from .pricing import worst_case_usd
from .runs import ROOT, RUNS_DIR, new_run
from .sandbox import WORK, SandboxRun, Workbench, run_script
from .workbench_tools import make_tools
from .spec import Claim, PaperSpec, reference_problems

# The workshop's cap on a structured reply: one more attempt with the problems fed back.
EXTRACT_ATTEMPTS = 2
CHARS_PER_TOKEN = 3  # conservative: overestimates tokens, so the budget bound stays a bound
SPEC_TOKENS = 4000
STDERR_TAIL, STDOUT_TAIL = 4000, 2000
MARKET_CACHE = ROOT / "data" / "market"
# Generating a whole script with reasoning can take minutes; the SDK default would cut it off.
MODEL_TIMEOUT_S = 600
# The workbench builder's first runs have no measured cost yet: this caps them until the ledger has data.
FIRST_WORKBENCH_BUDGET_USD = 3.0
WORKBENCH_LIFETIME_S = 3600


@dataclass
class Run:
    run_id: str
    folder: Path
    ledger: Ledger
    sandbox: Callable[..., SandboxRun]
    timeout_s: int
    effort: str | None = None
    guard_events: list[str] = field(default_factory=list)
    rejections: list[dict] = field(default_factory=list)
    market_log: list[dict] = field(default_factory=list)
    sandbox_note: str = "not run"
    rounds: int = 0
    failure: str | None = None
    started: float = field(default_factory=time.monotonic)

    def say(self, stage: str, message: str, **data) -> None:
        print(f"[{stage}] {message}", flush=True)
        stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with (self.folder / "events.jsonl").open("a") as stream:
            stream.write(json.dumps({"ts": stamp, "stage": stage, "message": message, **data}) + "\n")

    def reject(self, attempt: int, problem: str) -> None:
        self.rejections.append({"round": attempt, "reason": problem})


def planned_budget(model: str, latex: str, attempts: int) -> float:
    """Upper bound on model spend: every call at its output cap, the builder's history growing each attempt."""
    paper = len(latex) // CHARS_PER_TOKEN
    total = EXTRACT_ATTEMPTS * worst_case_usd(model, paper + SPEC_TOKENS, roles.MAX_TOKENS["extractor"])
    for attempt in range(attempts):
        history = paper + SPEC_TOKENS + attempt * (roles.MAX_TOKENS["builder"] + STDERR_TAIL)
        total += worst_case_usd(model, history, roles.MAX_TOKENS["builder"])
    return round(total, 4)


async def extract(run: Run, cfg: config.ModelConfig, client: AsyncOpenAI, latex: str,
                  effort: str | None) -> PaperSpec:
    """The paper's spec. If its references do not name claims it is asked for once more with the problems;
    whatever is still unresolved goes into the report, so no check is switched off without a word."""
    paper = f"PAPER (LaTeX source):\n{latex}"
    prompt = paper
    for attempt in range(1, EXTRACT_ATTEMPTS + 1):
        run.say("extract", f"reading the paper with {cfg.model}" if attempt == 1 else
                "asking for the spec again, with its references fixed")
        spec = (await Runner.run(roles.extractor(cfg, client, effort), prompt, max_turns=1,
                                 hooks=run.ledger)).final_output
        problems = reference_problems(spec)
        if not problems:
            return spec
        run.say("extract", f"{len(problems)} references in the spec do not name a claim", problems=problems)
        prompt = (f"{paper}\n\nYour previous spec referred to claims that do not exist:\n"
                  + "\n".join(f"- {problem}" for problem in problems)
                  + "\nIts claim names were: " + ", ".join(repr(c.name) for c in spec.claims)
                  + "\nWrite the whole spec again. headline, partitions and tests name claims by their exact name; "
                    "leave out a partition or test whose numbers the paper does not print.")
    run.guard_events.extend(f"spec reference unresolved: {problem}" for problem in problems)
    return spec


def sides_by_statistic(spec: PaperSpec, paper: list[dict]) -> dict[str, str]:
    """Which side each test statistic was tested on, from the paper-sidedness check."""
    tests = {t.test: t.statistic for t in spec.tests}
    return {tests[c["test"]]: c["side"] for c in paper if c["check"] == "sidedness" and c["test"] in tests}


async def clean_run(run: Run, script: str, attempt: int) -> SandboxRun | None:
    """The sandbox round, or None when the infrastructure failed (Modal, host fetch): the builder
    cannot fix that, so the caller stops and keeps its last good results."""
    try:
        return await asyncio.to_thread(sandbox_round, run, script, attempt)
    except Exception as error:
        run.failure = f"the clean run could not complete ({type(error).__name__})"
        run.guard_events.append(f"attempt {attempt}: clean run could not complete: {type(error).__name__}: {error}")
        run.say("error", f"attempt {attempt}: clean run could not complete: {type(error).__name__}: {error}")
        return None


def carried_over(error: MaxTurnsExceeded, task: str) -> list:
    """The conversation so far from a round that ran out of turns, so the next round keeps what it learned."""
    data = error.run_data
    if data is None:
        return [user(task)]
    start = [user(data.input)] if isinstance(data.input, str) else list(data.input)
    return start + [item.to_input_item() for item in data.new_items]


def sandbox_secrets() -> dict[str, str]:
    return {"SEC_USER_AGENT": os.environ["SEC_USER_AGENT"]}


def user(text: str) -> dict:
    return {"role": "user", "content": text}


def read_results(sandbox_run: SandboxRun) -> tuple[list[dict] | None, str | None]:
    """The results the sandbox wrote, or the problem to send back to the builder (secrets redacted)."""
    tail = f"STDERR (end):\n{sandbox_run.stderr[-STDERR_TAIL:]}\nSTDOUT (end):\n{sandbox_run.stdout[-STDOUT_TAIL:]}"
    tail = guards.redact(tail, sandbox_secrets())
    if sandbox_run.exit_code != 0:
        return None, f"The script failed with exit code {sandbox_run.exit_code}.\n{tail}"
    raw = sandbox_run.files.get("results.json")
    if raw is None:
        return None, f"The script exited 0 but wrote no /work/results.json.\n{tail}"
    try:
        results = json.loads(raw)["results"]
        if not all(isinstance(r.get("value"), (int, float)) for r in results):
            raise ValueError("every result needs a numeric value")
    except (ValueError, KeyError, TypeError, AttributeError) as error:
        return None, f"/work/results.json does not match the format: {error}"
    return results, None


def sandbox_round(run: Run, script: str, attempt: int) -> SandboxRun:
    """Run the script; if market data was missing, fetch it on the host once and rerun the same script."""
    env = sandbox_secrets()
    result = run.sandbox(script, market_cache=MARKET_CACHE, env=env, timeout_s=run.timeout_s)
    requests = json.loads(result.files.get("market_data_requests.json", "[]"))
    if requests:
        run.say("data", f"sandbox could not fetch {len(requests)} market-data items; fetching on the host and caching")
        fetched = market.fulfil(requests, MARKET_CACHE)
        run.guard_events.append(f"attempt {attempt}: {len(fetched)} market-data items fetched on the host into data/market")
        result = run.sandbox(script, market_cache=MARKET_CACHE, env=env, timeout_s=run.timeout_s)
    (run.folder / f"sandbox_{attempt}.log").write_text(
        f"exit {result.exit_code} in {result.seconds}s\n--- stdout\n{result.stdout}\n--- stderr\n{result.stderr}")
    run.market_log = json.loads(result.files.get("market_data_log.json", "[]"))
    run.sandbox_note = f"attempt {attempt}, exit {result.exit_code}, {result.seconds}s"
    return result


def script_problem(script: str, previous: str, claims: list[Claim], targets: list[str],
                   totals: list[Claim]) -> str | None:
    """The coded checks a script must pass before it gets sandbox time."""
    broken = guards.syntax_error(script)
    if broken:
        return f"the script does not compile: {broken}."
    leaked = guards.hardcoded_results(script, claims)
    if leaked:
        return (f"the script contains numbers the paper reports ({', '.join(leaked)}). "
                "Compute them from data and remove them from the code and comments.")
    counts = guards.hardcoded_counts(script, totals)
    if counts:
        return (f"the script contains sample counts the paper reports ({', '.join(counts)}). Build the sample from "
                "the paper's definition and report the count you get; never trim, cut or pad it to a reported "
                "count. If a number is a coincidence, write it another way.")
    planted = guards.planted_counts(script, previous, targets)
    if planted:
        return (f"the script now contains the paper's sample counts as literals ({', '.join(planted)}). "
                "Fix how the sample is built; never filter, trim or pad to reach a number.")
    if guards.bypasses_market_data(script):
        return "the script imports yfinance directly. Use market_data for all market data."
    return None


def audit_problem(claims: list[Claim], results: list[dict], stdout: str) -> tuple[str | None, list[str]]:
    """Sample counts that disagree with the paper, as feedback for the builder, plus the counts to watch."""
    off = [row for row in compare(claims, results) if row["kind"] == "count" and row["consistent"] is False]
    if not off:
        return None, []
    gaps = "\n".join(f"- {r['name']}: the paper reports {r['reported']:g}, your run produced {r['reproduced']:g}"
                     for r in off)
    problem = ("The script ran, but its sample does not match the paper's:\n" + gaps +
               f"\nYour script's output (end):\n{guards.redact(stdout[-STDOUT_TAIL:], sandbox_secrets())}\n"
               "Find the step where your sample construction departs from the paper's definition (which filings "
               "or observations count, forms, items, dates, deduplication) and fix that step. Never filter, trim "
               "or pad the data to reach a number.")
    return problem, [f"{r['reported']:g}" for r in off]


async def build_and_run(run: Run, builder: Agent, latex: str, spec: PaperSpec, claims: list[Claim],
                        attempts: int) -> list[dict] | None:
    """Write, check and run the script; send failures and sample mismatches back. Returns the last results
    that ran, so an audit round that breaks the script never loses an earlier good run."""
    task = f"PAPER (LaTeX source):\n{latex}\n\nSPEC:\n{spec.model_dump_json(indent=1)}\n\nWrite the replication script."
    history: list = [user(task)]
    previous, targets, kept = "", [], None
    totals = guards.sample_totals(claims, {p.total for p in spec.partitions})
    for attempt in range(1, attempts + 1):
        run.rounds = attempt
        run.say("build", f"attempt {attempt}: writing the script")
        result = await Runner.run(builder, history, max_turns=1, hooks=run.ledger)
        script = result.final_output
        (run.folder / f"attempt_{attempt}.py").write_text(script.script)
        (run.folder / f"attempt_{attempt}_notes.md").write_text(script.notes)
        history = result.to_input_list()
        problem = script_problem(script.script, previous, claims, targets, totals)
        previous = script.script
        if problem:
            run.guard_events.append(f"attempt {attempt}: rejected before the sandbox: {problem}")
            run.reject(attempt, problem)
            run.say("guard", f"script rejected: {problem.split('. ')[0]}")
            history.append(user(f"Rejected: {problem} Return the whole corrected script."))
            continue
        run.say("sandbox", f"attempt {attempt}: running in the sandbox")
        sandbox_run = await clean_run(run, script.script, attempt)
        if sandbox_run is None:
            return kept
        results, problem = read_results(sandbox_run)
        if problem is not None:
            run.say("sandbox", f"attempt {attempt}: {problem.splitlines()[0]}")
            history.append(user(problem))
            continue
        kept = results
        (run.folder / "results.json").write_text(sandbox_run.files["results.json"])
        (run.folder / "results_attempt.txt").write_text(str(attempt))
        problem, watch = audit_problem(claims, results, sandbox_run.stdout)
        if problem is None:
            run.say("audit", f"attempt {attempt}: {len(results)} results, sample counts match the paper")
            return kept
        targets = sorted(set(targets) | set(watch))
        run.guard_events.append(f"attempt {attempt}: audit sent back {len(watch)} sample counts that disagree")
        run.say("audit", f"attempt {attempt}: {len(results)} results, but {len(watch)} sample counts disagree; sent back")
        history.append(user(f"{problem} Return the whole corrected script."))
    return kept


async def build_with_workbench(run: Run, cfg: config.ModelConfig, client: AsyncOpenAI, latex: str,
                               spec: PaperSpec, claims: list[Claim], *, turns: int, rounds: int,
                               open_bench: Callable[..., Workbench] = Workbench) -> list[dict] | None:
    """Cookbook 07's form: the builder explores and writes /work/replicate.py in a persistent sandbox with
    `run` and `write_file`; only a clean re-run of that file in a fresh sandbox produces results. The same
    checks and the audit loop apply between rounds."""
    env = sandbox_secrets()
    bench = await asyncio.to_thread(open_bench, market_cache=MARKET_CACHE, env=env,
                                    command_timeout_s=run.timeout_s, lifetime_s=WORKBENCH_LIFETIME_S)
    task = (f"PAPER (LaTeX source):\n{latex}\n\nSPEC:\n{spec.model_dump_json(indent=1)}\n\n"
            "Replicate the paper's headline results as /work/replicate.py.")
    try:
        agent = roles.workbench_builder(cfg, client, run.timeout_s // 60, turns, make_tools(bench, run.say, env, turns),
                                        run.effort)
        history: list = [user(task)]
        previous, targets, kept = "", [], None
        totals = guards.sample_totals(claims, {p.total for p in spec.partitions})
        for round_ in range(1, rounds + 1):
            run.rounds = round_
            run.say("build", f"round {round_}: the builder works in the sandbox (up to {turns} turns)")
            ran_out = False
            try:
                result = await Runner.run(agent, history, max_turns=turns, hooks=run.ledger)
                history, summary = result.to_input_list(), str(result.final_output)
            except MaxTurnsExceeded as error:
                ran_out = True
                summary = "(ran out of turns)"
                history = carried_over(error, task) + [user(
                    "This round's turns are used up. Write /work/replicate.py now from what you have learned, "
                    "run it, and finish.")]
                run.guard_events.append(f"round {round_}: the builder ran out of turns")
            script = await asyncio.to_thread(bench.read_text, f"{WORK}/replicate.py")
            (run.folder / f"attempt_{round_}_notes.md").write_text(summary)
            if script is None and ran_out:
                continue  # not a guard event: the next round is told to write the script now
            if script is None:
                problem = "there is no /work/replicate.py."
            else:
                (run.folder / f"attempt_{round_}.py").write_text(script)
                problem = script_problem(script, previous, claims, targets, totals)
                previous = script
            if problem:
                run.guard_events.append(f"round {round_}: rejected before the clean run: {problem}")
                run.reject(round_, problem)
                run.say("guard", f"script rejected: {problem.split('. ')[0]}")
                history.append(user(f"Rejected: {problem} Fix /work/replicate.py in the sandbox and run it again."))
                continue
            run.say("sandbox", f"round {round_}: clean re-run in a fresh sandbox")
            sandbox_run = await clean_run(run, script, round_)
            if sandbox_run is None:
                return kept
            results, problem = read_results(sandbox_run)
            if problem is not None:
                run.say("sandbox", f"round {round_}: {problem.splitlines()[0]}")
                history.append(user(f"The clean re-run in a fresh sandbox failed. {problem}\n"
                                    "Fix /work/replicate.py and run it again."))
                continue
            kept = results
            (run.folder / "results.json").write_text(sandbox_run.files["results.json"])
            (run.folder / "results_attempt.txt").write_text(str(round_))
            problem, watch = audit_problem(claims, results, sandbox_run.stdout)
            if problem is None:
                run.say("audit", f"round {round_}: {len(results)} results, sample counts match the paper")
                return kept
            targets = sorted(set(targets) | set(watch))
            run.guard_events.append(f"round {round_}: audit sent back {len(watch)} sample counts that disagree")
            run.say("audit", f"round {round_}: {len(results)} results, but {len(watch)} sample counts disagree; sent back")
            history.append(user(f"{problem} Fix /work/replicate.py in the sandbox and run it again."))
        return kept
    finally:
        await asyncio.to_thread(bench.close)


async def replicate(arxiv_id: str, client: AsyncOpenAI, cfg: config.ModelConfig, *, attempts: int,
                    timeout_s: int, budget_usd: float | None, runs_dir: Path = RUNS_DIR,
                    sandbox: Callable[..., SandboxRun] = run_script, builder: str = "oneshot",
                    turns: int = 30, open_bench: Callable[..., Workbench] = Workbench,
                    effort: str | None = None) -> dict:
    run_id, folder = new_run(runs_dir)
    latex = load_paper(arxiv_id, ROOT / "data" / "arxiv")
    (folder / "paper.tex").write_text(latex)
    if budget_usd is not None:
        budget = budget_usd
    elif builder == "workbench":
        budget = FIRST_WORKBENCH_BUDGET_USD
    else:
        budget = planned_budget(cfg.model, latex, attempts)
    ledger = Ledger(folder / "calls.jsonl", run_id, {"extractor": cfg, "builder": cfg}, budget_usd=budget)
    run = Run(run_id, folder, ledger, sandbox, timeout_s, effort=effort)
    run.say("ingest", f"{run_id}: arXiv {arxiv_id}, {len(latex)} chars of LaTeX; {cfg.model} at effort "
                      f"{effort or 'default'}; {builder} builder; budget ${budget:.4f}",
            arxiv_id=arxiv_id, provider=cfg.provider.name, model=cfg.model, effort=effort or "default",
            builder=builder, budget_usd=budget)

    spec, rows, rejected, paper, results, crashed = None, [], [], [], None, None
    try:
        spec = await extract(run, cfg, client, latex, effort)
        run.say("extract", f"read: {spec.title} ({len(spec.claims)} numbers to check)", title=spec.title)
        (folder / "spec.json").write_text(spec.model_dump_json(indent=1))
        claims, rejected = guards.ground_claims(spec.claims, latex)
        run.say("guard", f"{len(claims)} claims grounded in the LaTeX, {len(rejected)} rejected",
                rejected=rejected)
        paper = check_paper(spec, claims)
        for check in paper:
            run.say("check", f"{check['status']}: {check['text']}", **check)
        if not claims:
            run.failure = "no number the extractor reported could be found in the paper"
        elif builder == "workbench":
            results = await build_with_workbench(run, cfg, client, latex, spec, claims, turns=turns,
                                                 rounds=attempts, open_bench=open_bench)
        else:
            results = await build_and_run(run, roles.builder(cfg, client, timeout_s // 60, effort), latex, spec,
                                          claims, attempts)
        rows = compare(claims, results or [], sides=sides_by_statistic(spec, paper))
    except Exception as error:  # the report still gets written, with the reason
        crashed = f"{type(error).__name__}: {error}"
        run.failure = f"the run stopped ({type(error).__name__})"
        run.guard_events.append(f"run stopped: {crashed}")
        run.say("error", crashed)
    outcome, reason = verdict(rows, results, run.failure)
    headline = spec.headline if spec else None
    headline_text = first_line(outcome, reason, rows, headline)
    path = report.write(folder, arxiv_id=arxiv_id, title=spec.title if spec else arxiv_id, verdict=outcome,
                        rows=rows, rejected=rejected, paper_checks=paper, headline_text=headline_text,
                        guard_events=run.guard_events, market_log=run.market_log, calls=ledger.rows,
                        sandbox_note=run.sandbox_note)
    summary = run_summary(run, arxiv_id, cfg, builder, outcome, reason, headline_text, rows, headline, crashed)
    (folder / "summary.json").write_text(json.dumps(summary, indent=1))
    run.say("verdict", f"{outcome} (${ledger.spent_usd:.4f} spent)", verdict=outcome)
    return {"run_id": run_id, "verdict": outcome, "report": path, "spent_usd": ledger.spent_usd, "summary": summary}


def run_summary(run: Run, arxiv_id: str, cfg: config.ModelConfig, builder: str, outcome: str, reason: str,
                headline_text: str, rows: list[dict], headline: str | None, crashed: str | None) -> dict:
    """One record per run, the unit of the reliability and model-ladder tables."""
    calls = run.ledger.rows
    main = next((r for r in rows if r["name"] == headline), None)
    return {
        "run_id": run.run_id, "paper": arxiv_id, "provider": cfg.provider.name, "model": cfg.model,
        "effort": run.effort, "builder": builder, "verdict": outcome, "reason": reason, "first_line": headline_text,
        "headline": main,
        "sample": [{"name": r["name"], "reported": r["reported"], "reproduced": r["reproduced"],
                    "consistent": r["consistent"]} for r in rows if r["kind"] == "count"],
        "judged": sum(1 for r in rows if r["kind"] != "count" and r["consistent"] is not None),
        "matched": sum(1 for r in rows if r["kind"] != "count" and r["consistent"]),
        "rejections": run.rejections, "rounds": run.rounds, "calls": len(calls),
        "cost_usd": round(run.ledger.spent_usd, 4),
        "tokens_in": sum(c["input_tokens"] for c in calls), "tokens_out": sum(c["output_tokens"] for c in calls),
        "wall_s": round(time.monotonic() - run.started, 1), "crashed": crashed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("arxiv_id")
    parser.add_argument("--provider", default=None, help="default: the quick tier's provider (Meta)")
    parser.add_argument("--model", default=None, help="default: the quick tier's model")
    parser.add_argument("--effort", default=None, help="reasoning effort for every role (minimal ... max)")
    parser.add_argument("--builder", choices=["workbench", "oneshot"], default="workbench")
    parser.add_argument("--attempts", type=int, default=3, help="build attempts (oneshot) or audit rounds (workbench)")
    parser.add_argument("--turns", type=int, default=30, help="tool turns per workbench round")
    parser.add_argument("--timeout-min", type=int, default=20)
    parser.add_argument("--budget-usd", type=float, default=None,
                        help="budget stop for this run; default: the planned worst case (oneshot) or the "
                             "first-measurement cap (workbench)")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    cfg = config.tier("quick")
    if args.provider or args.model:
        cfg = config.ModelConfig(config.PROVIDERS[args.provider or cfg.provider.name], args.model or cfg.model)
    outcome = asyncio.run(replicate(args.arxiv_id, make_client(cfg, timeout_s=MODEL_TIMEOUT_S), cfg,
                                    attempts=args.attempts, timeout_s=args.timeout_min * 60,
                                    budget_usd=args.budget_usd, builder=args.builder, turns=args.turns,
                                    effort=args.effort))
    print(outcome["summary"]["first_line"])
    print(f"report: {outcome['report'].relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
