"""Model clients for the Agents SDK, one recipe for every provider.

Tracing is switched off on import, so a run sends nothing anywhere except its model calls.
"""

from __future__ import annotations

import asyncio
import math
import os
import random
import sys
import time
from collections.abc import Awaitable, Callable

import httpx2
from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI, DefaultAsyncHttpxClient

from .config import ModelConfig

set_tracing_disabled(True)

MAX_RETRIES = 4  # the SDK retries only 429 and 5xx
TIMEOUT_SECONDS = 180

# Rate limits are per minute (Fireworks: 56,250 generated tokens a minute, read from its x-ratelimit headers on
# 29 Oct), so one wait never needs to be longer than the window. The SDK's own back-off tops out at 8 s, and its
# four retries ended six held-out runs on 29 Oct while a burst cleared, which took about a minute
# (16:36:46-16:37:48). Five windows covers a burst several times that; past it, the run fails loudly.
RATE_LIMIT_WINDOW_S = 60.0
RATE_LIMIT_DEADLINE_S = 5 * RATE_LIMIT_WINDOW_S


class MissingKeyError(RuntimeError):
    pass


class RateLimitRetry(httpx2.AsyncBaseTransport):
    """Waits out a 429 instead of handing it to the SDK: the host's retry-after when it gives one, else an
    exponential back-off with full jitter (the AWS form), capped at the window. After the deadline the 429 goes
    back marked `x-should-retry: false`, so the SDK raises it at once instead of retrying it four more times.
    Every other response, 5xx included, is the SDK's to handle as before. Each wait is one line on stderr, which
    a batch's .out keeps, so the rate-limit pressure a batch ran under can be counted."""

    def __init__(self, inner: httpx2.AsyncBaseTransport, *, deadline_s: float = RATE_LIMIT_DEADLINE_S,
                 window_s: float = RATE_LIMIT_WINDOW_S, sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
                 clock: Callable[[], float] = time.monotonic, jitter: Callable[[], float] = random.random,
                 log: Callable[[str], None] = lambda line: print(line, file=sys.stderr, flush=True)):
        self.inner, self.deadline_s, self.window_s = inner, deadline_s, window_s
        self.sleep, self.clock, self.jitter, self.log = sleep, clock, jitter, log

    def _wait(self, response: httpx2.Response, attempt: int) -> float:
        """At least a second, at most the window. A retry-after gets up to a second of jitter, so clients limited
        in the same burst don't all come back at the same instant."""
        for header, divisor in (("retry-after-ms", 1000), ("retry-after", 1)):
            try:
                asked = float(response.headers[header]) / divisor
            except (KeyError, ValueError):
                continue
            if math.isfinite(asked):
                return min(max(asked, 1.0) + self.jitter(), self.window_s)
        return max(1.0, self.jitter() * min(self.window_s, 2.0 ** (attempt + 2)))

    async def handle_async_request(self, request: httpx2.Request) -> httpx2.Response:
        await request.aread()   # the body is sent again on each try
        start, attempt = self.clock(), 0
        while True:
            response = await self.inner.handle_async_request(request)
            if response.status_code != 429:
                return response
            wait = self._wait(response, attempt)
            if self.clock() - start + wait > self.deadline_s:
                self.log(f"[rate-limit] {request.url.host}: 429 after {self.clock() - start:.0f} s of waits, "
                         f"past the {self.deadline_s:.0f}-s deadline; failing")
                response.headers["x-should-retry"] = "false"
                return response
            self.log(f"[rate-limit] {request.url.host}: 429, waiting {wait:.1f} s (attempt {attempt + 1})")
            await response.aclose()
            await self.sleep(wait)
            attempt += 1

    async def aclose(self) -> None:
        await self.inner.aclose()


def _proxy() -> str | None:
    """The proxy the environment names: a client given its own transport no longer reads it (NO_PROXY isn't read)."""
    for name in ("HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy"):
        if os.environ.get(name):
            return os.environ[name]
    return None


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
    if http_client is None:   # the SDK's own client settings, with rate limits waited out
        http_client = DefaultAsyncHttpxClient(transport=RateLimitRetry(httpx2.AsyncHTTPTransport(proxy=_proxy())))
    return AsyncOpenAI(
        api_key=key,
        base_url=cfg.provider.base_url,
        max_retries=max_retries,
        timeout=timeout_s,
        http_client=http_client,
    )


def make_model(cfg: ModelConfig, client: AsyncOpenAI) -> OpenAIChatCompletionsModel:
    return OpenAIChatCompletionsModel(model=cfg.model, openai_client=client)
