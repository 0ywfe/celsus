"""Day-1 check: one Agents SDK agent, one call to the quick tier, a structured answer checked in code.

    uv run python -m paper_replicator.check_day1

Prints DAY1 OK with the model id, tokens and cost of the call, or DAY1 FAIL and why.
Exactly one model call: max_turns=1 and no client retries.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import openai
from agents import Agent, AgentsException, ModelSettings, Runner
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.shared import Reasoning
from pydantic import BaseModel

from . import config
from .ledger import Ledger
from .llm import MissingKeyError, make_client, make_model
from .runs import ROOT, RUNS_DIR, new_run

QUESTION = "What is 17 multiplied by 23?"
EXPECTED = 17 * 23
# A reasoning model returns empty content when reasoning uses the whole budget, so the cap
# leaves room. Per-role caps get set later from the reasoning tokens the ledger records.
MAX_TOKENS = 4096
EFFORT = "low"


class Product(BaseModel):
    product: int


async def run_check(client: AsyncOpenAI, cfg: config.ModelConfig, runs_dir: Path) -> dict:
    run_id, folder = new_run(runs_dir)
    agent = Agent(
        name="day1",
        instructions="Answer the arithmetic question exactly.",
        model=make_model(cfg, client),
        output_type=Product,
        model_settings=ModelSettings(max_tokens=MAX_TOKENS, reasoning=Reasoning(effort=EFFORT)),
    )
    ledger = Ledger(folder / "calls.jsonl", run_id, {agent.name: cfg})
    report = {"run_id": run_id, "ledger": ledger.path, "rows": ledger.rows, "ok": False}
    try:
        result = await Runner.run(agent, QUESTION, max_turns=1, hooks=ledger)
    except (AgentsException, openai.APIError) as error:
        return {**report, "reason": f"{type(error).__name__}: {error}"}
    answer = result.final_output.product
    if answer != EXPECTED:
        return {**report, "reason": f"answered {answer}, expected {EXPECTED}"}
    return {**report, "ok": True, "reason": ""}


def summary(cfg: config.ModelConfig, report: dict) -> str:
    verdict = "DAY1 OK" if report["ok"] else f"DAY1 FAIL ({report['reason']})"
    lines = [verdict, f"  model     {cfg.model} ({cfg.provider.name}, {cfg.provider.base_url})"]
    for row in report["rows"]:
        cost = "unpriced" if row["cost_usd"] is None else f"${row['cost_usd']:.6f}"
        lines += [
            f"  tokens    in {row['input_tokens']} (cached {row['cached_tokens']}), "
            f"out {row['output_tokens']} (reasoning {row['reasoning_tokens']})",
            f"  cost      {cost}",
        ]
    lines.append(f"  calls     {len(report['rows'])}, logged to {report['ledger'].relative_to(ROOT)}")
    return "\n".join(lines)


def main() -> int:
    load_dotenv(ROOT / ".env")
    cfg = config.tier("quick")
    try:
        client = make_client(cfg, max_retries=0)
    except MissingKeyError as error:
        print(f"DAY1 FAIL ({error})")
        return 1
    report = asyncio.run(run_check(client, cfg, RUNS_DIR))
    print(summary(cfg, report))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
