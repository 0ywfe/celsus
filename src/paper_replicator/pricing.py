"""USD per 1M tokens as (cached input, input, output).

Meta: dev.meta.ai/docs/getting-started/pricing-rate-limits, read 26 Oct 2026. Muse Spark Open on Baseten:
baseten.co/library/muse-spark-open, read 28 Oct 2026 (the same rates as Spark on Meta's API). Other endpoints bring their
prices in providers.local.json (see local.py). Reasoning tokens are billed as output. A model missing here is
unpriced, and its cost is None.
"""

from __future__ import annotations

from pathlib import Path

from . import local

PRICES = {
    "muse-spark-1.3": (0.15, 1.25, 4.25),
    "muse-spark-1.3-contributor": (0.002, 0.10, 0.20),
    "muse-wonder-1.0": (0.20, 4.00, 20.00),
    "meta-models/muse-spark-open": (0.15, 1.25, 4.25),
    "meta-models/muse-spark-open-1026": (0.15, 1.25, 4.25),
}


def local_prices(path: Path = local.LOCAL_FILE) -> dict[str, tuple[float, float, float]]:
    return {model: tuple(price) for entry in local.load(path).values()
            for model, price in entry.get("prices", {}).items()}


ALL_PRICES = {**local_prices(), **PRICES}


def cost_usd(model: str, input_tokens: int, cached_tokens: int, output_tokens: int) -> float | None:
    price = ALL_PRICES.get(model)
    if price is None:
        return None
    cached, fresh, output = price
    return (
        (input_tokens - cached_tokens) * fresh + cached_tokens * cached + output_tokens * output
    ) / 1_000_000


def worst_case_usd(model: str, input_tokens: int, max_tokens: int) -> float | None:
    """The most one call can cost: all input uncached and the output cap fully used."""
    return cost_usd(model, input_tokens, 0, max_tokens)
