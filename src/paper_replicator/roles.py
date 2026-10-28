"""The agents. Each role is an Agents SDK agent with a typed output; plain code checks what it returns."""

from __future__ import annotations

from agents import Agent, ModelSettings
from openai import AsyncOpenAI
from openai.types.shared import Reasoning
from pydantic import BaseModel, Field

from .config import ModelConfig
from .llm import make_model
from .sandbox_lib import market_data
from .spec import PaperSpec

# Output caps leave room for reasoning (a reasoning model returns empty content when it uses
# the whole cap). Set from the ledger's measured reasoning tokens once runs exist.
MAX_TOKENS = {"extractor": 32000, "builder": 32000}
EFFORT = {"extractor": "medium", "builder": "medium"}

EXTRACTOR = """You read a research paper's LaTeX source and write its replication spec.
- claims: every headline number the paper reports as a result: estimates, test statistics,
  p-values and sample sizes. Copy each value exactly as printed. Never compute, round or convert one.
- sample: the exact sample or event definition, the period, every filter, and the sample sizes.
- method: ordered steps precise enough to code, including windows, return definitions and tests.
- Report only what the paper says. Where it does not say, write "not stated"."""

RESULTS_FORMAT = """{"results": [{"name": "<claim name from the spec>",
               "value": <number, in the same unit the paper prints it in>,
               "se": <standard error of value, or null>,
               "n": <observations behind value, or null>}],
 "sample": {"description": "<the sample you built>", "n": <its size>},
 "notes": "<every choice the paper leaves open, and every deviation>"}"""

BUILDER = f"""You write one Python 3.12 script that replicates a paper's headline results from public data.

Environment: a fresh Linux sandbox with network access and a time limit of {{minutes}} minutes.
- Packages: pandas, numpy, scipy, statsmodels, requests, yfinance, pyarrow.
- SEC EDGAR: send the header User-Agent: os.environ["SEC_USER_AGENT"] on every request, and stay
  under 10 requests per second.
- Market data only through the module next to the script (`import market_data`):
{market_data.__doc__}
Write /work/results.json:
{RESULTS_FORMAT}

Rules:
- Compute every number from the data. Never write a number the paper reports into the code, not even in a comment.
- One result per claim you can compute, under the claim's exact name. Leave out claims you cannot
  compute and say why in notes.
- Follow the paper's sample definition, period and method exactly. Print the count after each filtering step.
- Catch MarketDataUnavailable only to drop that event, and count the drops. Let every other error propagate.
- When asked to fix the script, return the whole corrected script."""


class Script(BaseModel):
    script: str = Field(description="the whole Python file")
    notes: str = Field(description="assumptions, and every deviation from the paper's method")


def _settings(role: str) -> ModelSettings:
    return ModelSettings(max_tokens=MAX_TOKENS[role], reasoning=Reasoning(effort=EFFORT[role]))


def extractor(cfg: ModelConfig, client: AsyncOpenAI) -> Agent:
    return Agent(name="extractor", instructions=EXTRACTOR, model=make_model(cfg, client),
                 output_type=PaperSpec, model_settings=_settings("extractor"))


def builder(cfg: ModelConfig, client: AsyncOpenAI, minutes: int) -> Agent:
    return Agent(name="builder", instructions=BUILDER.replace("{minutes}", str(minutes)), model=make_model(cfg, client),
                 output_type=Script, model_settings=_settings("builder"))
