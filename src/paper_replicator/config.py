"""Which endpoint and model each tier runs on.

Any OpenAI-compatible endpoint works. Every tier defaults to Meta; a run can point a tier at another
endpoint with <TIER>_PROVIDER and <TIER>_MODEL in the environment, once that endpoint is added in the
gitignored providers.local.json (see local.py). Demo and benchmark runs use the defaults.
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


def providers(path: Path = local.LOCAL_FILE) -> dict[str, Provider]:
    """Meta, plus whatever the local file adds."""
    added = {name: Provider(name, entry["base_url"], entry["key_env"], entry.get("json_schema", True),
                            entry.get("reasoning_effort", True))
             for name, entry in local.load(path).items()}
    return {"meta": META, **added}


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
