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
from typing import Awaitable, Callable

from agents import Agent, MaxTurnsExceeded, ModelBehaviorError, Runner
from dotenv import load_dotenv
from openai import AsyncOpenAI

from . import config, guards, market, periods, report, roles
from .paper_checks import check_paper
from .compare import COULD_NOT_CHECK, NO_SIDE, compare, first_line, impossible, verdict
from .ingest import load_paper
from .ledger import Ledger, ProviderNotAllowed
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
# One sandbox's lifetime. Rounds measured up to 30 min (141 rounds on disk, 28 Oct), so three can outlive it; the
# workbench then reopens the sandbox with the builder's files (held-out 2512.12924 lost round 3 before that).
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
    hosts: list[str] = field(default_factory=list)
    kept_script: str = ""  # the script whose clean re-run produced the kept results
    sandbox_note: str = "not run"
    # the script reviewer (a judgement check), attached by replicate(); None runs without it
    review: Callable[[PaperSpec, str], Awaitable[tuple[str, str] | None]] | None = None
    review_issue: str | None = None
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


class Unreadable(Exception):
    """The paper could not be read: the run ends at could not check, not as a crash."""


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
    return {tests[c["test"]]: c["side"] or NO_SIDE for c in paper
            if c["check"] == "sidedness" and c["test"] in tests}


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
    run.hosts = json.loads(result.files.get("data_sources.json", "[]"))
    run.sandbox_note = f"attempt {attempt}, exit {result.exit_code}, {result.seconds}s"
    return result


def script_check(script: str, previous: str, claims: list[Claim], targets: list[str],
                 totals: list[Claim]) -> tuple[str, str] | None:
    """The first coded check a script fails before it gets sandbox time, as (check, problem), or None."""
    broken = guards.syntax_error(script)
    if broken:
        return "compiles", f"the script does not compile: {broken}."
    leaked = guards.hardcoded_results(script, claims)
    if leaked:
        return "paper's numbers in the code", (
            f"the code that writes these results contains the number the paper reports for them "
            f"({', '.join(leaked)}). Compute each result from the data; the paper's value never goes into it.")
    counts = guards.hardcoded_counts(script, totals, claims)
    if counts:
        return "sample counts in the code", (
            f"the script writes the paper's sample count as a result's count, or cuts its sample to it "
            f"({', '.join(counts)}). Build the sample from the paper's definition and report the count you get; "
            "never trim, cut or pad it to a reported count.")
    planted = guards.planted_counts(script, previous, targets)
    if planted:
        return "counts planted after feedback", (
            f"the script now contains the paper's sample counts as literals ({', '.join(planted)}). "
            "Fix how the sample is built; never filter, trim or pad to reach a number.")
    if guards.bypasses_market_data(script):
        return "market data adapter", "the script imports yfinance directly. Use market_data for all market data."
    if (code := guards.fetches_code(script)) is not None:
        return "authors' code", (f"the script fetches code from a code host ({code}). Build the analysis from "
                                 "the paper; fetch data files only, never the authors' code.")
    return None


def script_problem(script: str, previous: str, claims: list[Claim], targets: list[str],
                   totals: list[Claim]) -> str | None:
    """The coded checks a script must pass before it gets sandbox time."""
    found = script_check(script, previous, claims, targets, totals)
    return found[1] if found else None


def watched_totals(claims: list[Claim], spec: PaperSpec, latex: str) -> tuple[list[Claim], set[str]]:
    """The sample totals a script may not contain, and the values of the counts the paper chooses by rank
    (a top-N cut-off is part of the method, so it is never watched)."""
    chosen = guards.selection_counts(latex, claims)
    totals = [c for c in guards.sample_totals(claims, {p.total for p in spec.partitions}) if c.name not in chosen]
    values = {f"{guards.parse_number(c.value):g}" for c in claims if c.name in chosen}
    return totals, values


def sample_of(raw: str | None) -> dict:
    """The sample block of a results.json, or {}."""
    try:
        sample = json.loads(raw or "{}").get("sample")
    except (ValueError, AttributeError):
        return {}
    return sample if isinstance(sample, dict) else {}


def sample_checks(spec: PaperSpec, sample: dict, results: list[dict], totals: list[Claim]) -> list[tuple[str, str]]:
    """What stops the replication's sample being compared with the paper's, apart from count gaps, as (check, issue):
    the builder says it is not the paper's sample, a sample total is missing from the results (run 2601.08263
    dropped the counts that disagreed, leaving the audit nothing to compare), or the dates it covers are not the
    paper's."""
    issues = []
    if sample.get("same_as_paper") is False:
        why = str(sample.get("differences") or "").strip().rstrip(".")
        issues.append(("declared not the paper's sample",
                       "the replication could not rebuild the paper's sample" + (f" ({why})" if why else "")))
    reported = {r.get("name") for r in results}
    missing = [c.name for c in totals if c.name not in reported]
    if missing:
        issues.append(("sample size reported", f"the replication did not report the paper's sample size "
                                               f"({', '.join(missing)}), so its sample cannot be compared"))
    if gap := periods.period_gap(spec, sample):
        issues.append(("period", gap))
    return issues


def sample_issues(spec: PaperSpec, sample: dict, results: list[dict], totals: list[Claim]) -> list[str]:
    return [issue for _, issue in sample_checks(spec, sample, results, totals)]


async def reviewed(run: Run, spec: PaperSpec, script: str, when: str) -> str | None:
    """The reviewer's problem with a script whose sample the audit accepted, or None; remembered for the verdict."""
    found = await run.review(spec, script) if run.review else None
    run.review_issue = found[1] if found else None
    if found is None:
        return None
    run.guard_events.append(f"{when}: {found[1]}")
    run.say("review", f"{when}: {found[1].split(';')[0]}; sent back")
    return found[1] + "."


async def review_problem(run: Run, cfg: config.ModelConfig, client: AsyncOpenAI, spec: PaperSpec,
                         script: str) -> tuple[str, str] | None:
    """A judgement check, not a coded one: a reviewer reads the final script against the spec and the four integrity
    rules. A finding counts only when its passage is really in the script, so a reviewer cannot invent one."""
    task = (f"SPEC:\n{spec.model_dump_json(indent=1)}\n\nSCRIPT (/work/replicate.py):\n{script}")
    review = (await Runner.run(roles.reviewer(cfg, client), task, max_turns=1, hooks=run.ledger)).final_output
    found = [f for f in review.findings if f.passage.strip() and f.passage.strip() in script]
    if not found:
        return None
    first = found[0]
    return "script review", (f"a reviewer found {len(found)} breach{'es' if len(found) > 1 else ''} of the "
                             f"integrity rules; first, rule {first.rule}: {first.why} (`{first.passage.strip()[:160]}`)")


def audit_problem(claims: list[Claim], results: list[dict], stdout: str, spec: PaperSpec | None = None,
                  sample: dict | None = None, totals: list[Claim] = ()) -> tuple[str | None, list[str]]:
    """Sample counts that disagree with the paper, or anything else that stops the sample being compared, as
    feedback for the builder, plus the counts to watch."""
    off = [row for row in compare(claims, results) if row["kind"] == "count" and row["consistent"] is False]
    issues = sample_issues(spec, sample or {}, results, list(totals)) if spec else []
    if broken := impossible(claims, results):
        values = {r.get("name"): r.get("value") for r in results}
        return ("The script ran, but some results are values no result of their kind can take:\n" +
                "\n".join(f"- {name} = {values[name]}: {why}" for name, why in broken) +
                "\nFind and fix the computation behind each one; never clip or replace the number."), []
    if not off and not issues:
        return None, []
    gaps = "\n".join([f"- {r['name']}: the paper reports {r['reported']:g}, your run produced {r['reproduced']:g}"
                      for r in off] + [f"- {issue}" for issue in issues])
    problem = ("The script ran, but its sample does not match the paper's:\n" + gaps +
               f"\nYour script's output (end):\n{guards.redact(stdout[-STDOUT_TAIL:], sandbox_secrets())}\n"
               "Find the step where your sample construction departs from the paper's definition (which filings "
               "or observations count, forms, items, dates, deduplication) and fix that step. Never filter, trim "
               "or pad the data to reach a number. If the paper's data is not in your source, look for another "
               "public source; if none has it, say so in the sample block (same_as_paper false, the dates your "
               "data really covers). Always report the sample sizes, even when they differ.")
    return problem, [f"{r['reported']:g}" for r in off]


async def build_and_run(run: Run, builder: Agent, latex: str, spec: PaperSpec, claims: list[Claim],
                        attempts: int) -> list[dict] | None:
    """Write, check and run the script; send failures and sample mismatches back. Returns the last results
    that ran, so an audit round that breaks the script never loses an earlier good run."""
    task = f"PAPER (LaTeX source):\n{latex}\n\nSPEC:\n{spec.model_dump_json(indent=1)}\n\nWrite the replication script."
    history: list = [user(task)]
    previous, targets, kept = "", [], None
    totals, chosen = watched_totals(claims, spec, latex)
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
        kept, run.kept_script, run.review_issue = results, script.script, None   # not reviewed yet
        (run.folder / "results.json").write_text(sandbox_run.files["results.json"])
        (run.folder / "results_attempt.txt").write_text(str(attempt))
        problem, watch = audit_problem(claims, results, sandbox_run.stdout, spec,
                                       sample_of(sandbox_run.files.get("results.json")), totals)
        if problem is None:
            if (review := await reviewed(run, spec, script.script, f"attempt {attempt}")) is None:
                run.say("audit", f"attempt {attempt}: {len(results)} results, sample matches the paper")
                return kept
            history.append(user(f"Before its numbers are reported, {review} Return the whole corrected script."))
            continue
        targets = sorted((set(targets) | set(watch)) - chosen)
        run.guard_events.append(f"attempt {attempt}: audit sent the sample back: {problem.splitlines()[1][2:]}")
        run.say("audit", f"attempt {attempt}: {len(results)} results, but the sample disagrees with the paper's; sent back")
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
        totals, chosen = watched_totals(claims, spec, latex)
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
            kept, run.kept_script, run.review_issue = results, script, None   # not reviewed yet
            (run.folder / "results.json").write_text(sandbox_run.files["results.json"])
            (run.folder / "results_attempt.txt").write_text(str(round_))
            problem, watch = audit_problem(claims, results, sandbox_run.stdout, spec,
                                       sample_of(sandbox_run.files.get("results.json")), totals)
            if problem is None:
                if (review := await reviewed(run, spec, script, f"round {round_}")) is None:
                    run.say("audit", f"round {round_}: {len(results)} results, sample matches the paper")
                    return kept
                history.append(user(f"Before its numbers are reported, {review} Fix /work/replicate.py so every "
                                    "reported result is computed from the data by the paper's definition, and run it "
                                    "again."))
                continue
            targets = sorted((set(targets) | set(watch)) - chosen)
            run.guard_events.append(f"round {round_}: audit sent the sample back: {problem.splitlines()[1][2:]}")
            run.say("audit", f"round {round_}: {len(results)} results, but the sample disagrees with the paper's; sent back")
            history.append(user(f"{problem} Fix /work/replicate.py in the sandbox and run it again."))
        return kept
    finally:
        await asyncio.to_thread(bench.close)


async def replicate(arxiv_id: str, client: AsyncOpenAI, cfg: config.ModelConfig, *, attempts: int,
                    timeout_s: int, budget_usd: float | None, runs_dir: Path = RUNS_DIR,
                    sandbox: Callable[..., SandboxRun] = run_script, builder: str = "oneshot",
                    turns: int = 30, open_bench: Callable[..., Workbench] = Workbench,
                    effort: str | None = None, require_provider: str | None = None) -> dict:
    run_id, folder = new_run(runs_dir)
    try:
        latex, unreadable = load_paper(arxiv_id, ROOT / "data" / "arxiv"), None
    except Exception as error:  # no source, a PDF-only paper, arXiv down: the checker's failure, not the paper's
        latex = ""
        unreadable = (f"the paper's LaTeX source could not be read from arXiv "
                      f"({type(error).__name__}: {str(error)[:160]})")
    (folder / "paper.tex").write_text(latex)
    if budget_usd is not None:
        budget = budget_usd
    elif builder == "workbench":
        budget = FIRST_WORKBENCH_BUDGET_USD
    else:
        budget = planned_budget(cfg.model, latex, attempts)
    ledger = Ledger(folder / "calls.jsonl", run_id, {"extractor": cfg, "builder": cfg, "reviewer": cfg}, budget_usd=budget,
                    require_provider=require_provider)
    run = Run(run_id, folder, ledger, sandbox, timeout_s, effort=effort)
    run.review = lambda spec, script: review_problem(run, cfg, client, spec, script)
    run.say("ingest", f"{run_id}: arXiv {arxiv_id}, {len(latex)} chars of LaTeX; {cfg.model} at effort "
                      f"{effort or 'default'}; {builder} builder; budget ${budget:.4f}",
            arxiv_id=arxiv_id, provider=cfg.provider.name, model=cfg.model, effort=effort or "default",
            builder=builder, budget_usd=budget)

    spec, rows, rejected, paper, results, crashed = None, [], [], [], None, None
    try:
        if unreadable:
            raise Unreadable(unreadable)
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
        rows = compare(claims, results or [], sides=sides_by_statistic(spec, paper),
                       fixed=guards.fixed_results(run.kept_script, claims))
    except (Unreadable, ProviderNotAllowed) as error:
        run.failure = str(error)
        run.say("error", str(error))
    except Exception as error:  # the report still gets written, with the reason
        crashed = f"{type(error).__name__}: {error}"
        run.failure = (f"the model's reply could not be read ({error}); a reply cut off at its output cap reads "
                       f"this way" if isinstance(error, ModelBehaviorError) else
                       f"the run stopped ({type(error).__name__})")
        run.guard_events.append(f"run stopped: {crashed}")
        run.say("error", crashed)
    kept = folder / "results.json"
    issues = (sample_issues(spec, sample_of(kept.read_text()), results, watched_totals(claims, spec, latex)[0])
              if spec and results and kept.exists() else [])
    issues += [run.review_issue] if run.review_issue and results else []
    run.guard_events.extend(f"sample: {issue}" for issue in issues if issue != run.review_issue)
    outcome, reason = verdict(rows, results, run.failure, "; ".join(issues) or None)
    headline = spec.headline if spec else None
    headline_text = first_line(outcome, reason, rows, headline)
    path = report.write(folder, arxiv_id=arxiv_id, title=spec.title if spec else arxiv_id, verdict=outcome,
                        rows=rows, rejected=rejected, paper_checks=paper, headline_text=headline_text,
                        guard_events=run.guard_events, market_log=run.market_log, hosts=run.hosts, calls=ledger.rows,
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
    parser.add_argument("--require-provider", default=None,
                        help="stop the run before any call to another provider (demo and benchmark runs: meta)")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    cfg = config.tier("quick")
    if args.provider or args.model:
        cfg = config.ModelConfig(config.PROVIDERS[args.provider or cfg.provider.name], args.model or cfg.model)
    outcome = asyncio.run(replicate(args.arxiv_id, make_client(cfg, timeout_s=MODEL_TIMEOUT_S), cfg,
                                    attempts=args.attempts, timeout_s=args.timeout_min * 60,
                                    budget_usd=args.budget_usd, builder=args.builder, turns=args.turns,
                                    effort=args.effort, require_provider=args.require_provider))
    print(outcome["summary"]["first_line"])
    print(f"report: {outcome['report'].relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
