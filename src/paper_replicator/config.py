"""Which provider and model each tier runs on.

Every tier defaults to Meta. A dev run can point a tier elsewhere with <TIER>_PROVIDER and
<TIER>_MODEL in the environment (e.g. QUICK_PROVIDER=deepseek); the demo runs on the defaults.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Provider:
    name: str
    base_url: str
    key_env: str


@dataclass(frozen=True)
class ModelConfig:
    provider: Provider
    model: str


PROVIDERS = {
    "meta": Provider("meta", "https://api.meta.ai/v1", "MODEL_API_KEY"),
    "deepseek": Provider("deepseek", "https://api.deepseek.com", "DEEPSEEK_API_KEY"),
}

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
