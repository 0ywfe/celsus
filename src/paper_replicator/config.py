"""Which endpoint and model each tier runs on.

Any OpenAI-compatible endpoint works. Every tier defaults to Meta's API. Muse Spark Open, Meta's open-weights
model, is served on Baseten (QUICK_PROVIDER=baseten QUICK_MODEL=meta-models/muse-spark-open-1026) and on Fireworks
(QUICK_PROVIDER=fireworks QUICK_MODEL=accounts/fireworks/models/muse-spark-open). A run can
point a tier at another endpoint with <TIER>_PROVIDER and <TIER>_MODEL in the environment, once that endpoint
is added in the gitignored providers.local.json (see local.py).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from . import local


@dataclass(frozen=True)
class Provider:
    name: str
    base_url: str
    key_env: str
    json_schema: bool = True  # strict json_schema structured output; otherwise json_object plus the schema in the prompt
    reasoning_effort: bool = True  # accepts reasoning_effort


@dataclass(frozen=True)
class ModelConfig:
    provider: Provider
    model: str


META = Provider("meta", "https://api.meta.ai/v1", "MODEL_API_KEY")
# Strict json_schema output and reasoning_effort both checked live on 28 Oct; the reasoning comes back in its own
# field (reasoning_content), so the answer is the message content as everywhere else.
BASETEN = Provider("baseten", "https://inference.baseten.co/v1", "BASETEN_API_KEY")
# The same Hugging Face weights (meta-models/Muse-Spark-Open-816B-A42B). Checked live on 29 Oct: strict json_schema
# output, cached tokens in usage, and reasoning_effort passed to the model's own chat template (xhigh renders as
# "Reasoning strength: 512", as the default does; high as 256; a value the model doesn't define is refused).
FIREWORKS = Provider("fireworks", "https://api.fireworks.ai/inference/v1", "FIREWORKS_API_KEY")

# Meta's models, wherever they are served. A run held to Meta (--require-provider meta) counts the model, not the
# host: Muse Spark Open on Baseten or Fireworks is a Meta model, and the report says where it ran.
META_MODELS = frozenset({"muse-spark-1.3", "muse-spark-1.3-contributor", "muse-wonder-1.0",
                         "meta-models/muse-spark-open", "meta-models/muse-spark-open-1026",
                         "accounts/fireworks/models/muse-spark-open"})


def maker(cfg: ModelConfig) -> str:
    """Whose model a tier runs: "meta" for Meta's models on any host, else the endpoint's name."""
    return "meta" if cfg.model in META_MODELS else cfg.provider.name


def providers(path: Path = local.LOCAL_FILE) -> dict[str, Provider]:
    """Meta, Baseten and Fireworks, plus whatever the local file adds."""
    added = {name: Provider(name, entry["base_url"], entry["key_env"], entry.get("json_schema", True),
                            entry.get("reasoning_effort", True))
             for name, entry in local.load(path).items()}
    return {"meta": META, "baseten": BASETEN, "fireworks": FIREWORKS, **added}


PROVIDERS = providers()

# quick: extraction, analysts, reports. deep: builder and auditor.
DEFAULT_TIERS = {
    "quick": ("meta", "muse-spark-1.3"),
    "deep": ("meta", "muse-wonder-1.0"),
}


def tier(name: str) -> ModelConfig:
    default_provider, default_model = DEFAULT_TIERS[name]
    provider = os.environ.get(f"{name.upper()}_PROVIDER") or default_provider
    model = os.environ.get(f"{name.upper()}_MODEL") or default_model
    if provider not in PROVIDERS:
        raise ValueError(f"unknown provider {provider!r} for tier {name!r}: one of {sorted(PROVIDERS)}")
    return ModelConfig(PROVIDERS[provider], model)
