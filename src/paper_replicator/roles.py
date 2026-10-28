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

ENVIRONMENT = f"""Environment: a Linux sandbox with network access; the script's time limit is {{minutes}} minutes.
- Packages: pandas, numpy, scipy, statsmodels, requests, yfinance, pyarrow.
- SEC EDGAR: send the header User-Agent: os.environ["SEC_USER_AGENT"] on every request, and stay
  under 10 requests per second.
- Market data only through the module next to the script (`import market_data`); never import yfinance:
{market_data.__doc__}
The script writes /work/results.json:
{RESULTS_FORMAT}"""

RULES = """Rules:
- Compute every number from the data. Never write a number the paper reports into the code, not even in a comment.
- One result per claim you can compute, under the claim's exact name. Leave out claims you cannot
  compute and say why in notes.
- Follow the paper's sample definition, period and method exactly. Print the count after each filtering step.
- Catch MarketDataUnavailable only to drop that event, and count the drops. Let every other error propagate."""

BUILDER = f"""You write one Python 3.12 script that replicates a paper's headline results from public data.

{ENVIRONMENT}

{RULES}
- When asked to fix the script, return the whole corrected script."""

WORKBENCH = f"""You replicate a paper's headline results from public data, working inside a Linux sandbox.
Your tools: `run` (a bash command, working directory /work) and `write_file` (a whole file). Nothing
you do leaves the sandbox.

Work like an engineer, and be decisive: you have {{turns}} tool turns in total.
1. Probe each data source on a small sample first: print the fields and formats you will rely on.
2. Write the whole replication as /work/replicate.py with write_file and run it: `python /work/replicate.py`.
3. Read its output, fix what is wrong, run it again.
4. When it runs cleanly and writes /work/results.json, stop calling tools and reply with a short summary:
   the sample you built, each choice the paper leaves open, and each deviation from the paper.
The final /work/replicate.py is re-run from scratch in a fresh sandbox; only that run's results count,
so it must fetch everything it needs itself.

{ENVIRONMENT}

{RULES}"""


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


def workbench_builder(cfg: ModelConfig, client: AsyncOpenAI, minutes: int, turns: int, tools: list) -> Agent:
    """No output_type: as in Meta's cookbook 07, the tool loop ends in plain text (the summary)."""
    instructions = WORKBENCH.replace("{minutes}", str(minutes)).replace("{turns}", str(turns))
    return Agent(name="builder", instructions=instructions, model=make_model(cfg, client), tools=tools,
                 model_settings=_settings("builder"))
