"""Model clients for the Agents SDK, one recipe for every provider.

Tracing is switched off on import, so a run sends nothing anywhere except its model calls.
"""

from __future__ import annotations

import os

import httpx2
from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI

from .config import ModelConfig

set_tracing_disabled(True)

MAX_RETRIES = 4  # the SDK retries only 429 and 5xx
TIMEOUT_SECONDS = 180


class MissingKeyError(RuntimeError):
    pass


def make_client(
    cfg: ModelConfig,
    *,
    max_retries: int = MAX_RETRIES,
    timeout_s: float = TIMEOUT_SECONDS,
    http_client: httpx2.AsyncClient | None = None,
) -> AsyncOpenAI:
    key = os.environ.get(cfg.provider.key_env, "")
    if not key:
        raise MissingKeyError(f"{cfg.provider.key_env} is not set: add it to .env")
    return AsyncOpenAI(
        api_key=key,
        base_url=cfg.provider.base_url,
        max_retries=max_retries,
        timeout=timeout_s,
        http_client=http_client,
    )


def make_model(cfg: ModelConfig, client: AsyncOpenAI) -> OpenAIChatCompletionsModel:
    return OpenAIChatCompletionsModel(model=cfg.model, openai_client=client)
