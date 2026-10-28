"""One JSON line per model call in runs/<run-id>/calls.jsonl: role, provider, model, tokens, cost.

The ledger is a RunHooks, so the SDK calls it after every model response. An agent that
was not registered with its config fails the run, because an unlogged call must not pass.
With a budget, the call that takes spending past it raises BudgetExceeded and the run stops.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

from agents import Agent, RunContextWrapper, RunHooks
from agents.items import ModelResponse

from .config import ModelConfig
from .pricing import cost_usd


class BudgetExceeded(RuntimeError):
    pass


class Ledger(RunHooks):
    def __init__(
        self,
        path: Path,
        run_id: str,
        configs: dict[str, ModelConfig],
        budget_usd: float | None = None,
    ):
        self.path = path
        self.run_id = run_id
        self.configs = dict(configs)
        self.budget_usd = budget_usd
        self.rows: list[dict] = []

    @property
    def spent_usd(self) -> float:
        return sum(row["cost_usd"] or 0.0 for row in self.rows)

    async def on_llm_end(
        self, context: RunContextWrapper, agent: Agent, response: ModelResponse
    ) -> None:
        cfg = self.configs[agent.name]
        usage = response.usage
        cached = usage.input_tokens_details.cached_tokens or 0
        row = {
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "run_id": self.run_id,
            "role": agent.name,
            "provider": cfg.provider.name,
            "model": cfg.model,
            "input_tokens": usage.input_tokens,
            "cached_tokens": cached,
            "output_tokens": usage.output_tokens,
            "reasoning_tokens": usage.output_tokens_details.reasoning_tokens or 0,
            "cost_usd": cost_usd(cfg.model, usage.input_tokens, cached, usage.output_tokens),
            "request_id": response.request_id,
        }
        with self.path.open("a") as stream:
            stream.write(json.dumps(row) + "\n")
        self.rows.append(row)
        if self.budget_usd is None:
            return
        if row["cost_usd"] is None:
            raise BudgetExceeded(f"{cfg.model} is unpriced, so the budget cannot be enforced")
        if self.spent_usd > self.budget_usd:
            raise BudgetExceeded(f"spent ${self.spent_usd:.4f} of a ${self.budget_usd:.4f} budget")
