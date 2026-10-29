import asyncio

import httpx2
import openai
import pytest

from paper_replicator import config, llm

OK = {"id": "c1", "object": "chat.completion", "created": 0, "model": "m",
      "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
      "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}
LIMITED = {"error": {"message": "rate limit exceeded, please try again later", "code": 429}}


class Clock:
    """A clock that moves only when the transport sleeps, so a five-minute wait takes no time."""

    def __init__(self):
        self.now, self.sleeps = 0.0, []

    def time(self) -> float:
        return self.now

    async def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def provider(statuses: list[int], headers: dict | None = None):
    """A host that answers with each status in turn (429 = rate limited), then 200 for ever; it records every request."""
    seen = []

    def handle(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        status = statuses[len(seen) - 1] if len(seen) <= len(statuses) else 200
        if status == 429:
            return httpx2.Response(429, json=LIMITED, headers=headers or {})
        return httpx2.Response(status, json=OK if status == 200 else {"error": {"message": "boom"}})
    return seen, httpx2.MockTransport(handle)


def client(transport, clock: Clock, max_retries: int = llm.MAX_RETRIES, log: list | None = None) -> openai.AsyncOpenAI:
    waiting = llm.RateLimitRetry(transport, sleep=clock.sleep, clock=clock.time, jitter=lambda: 1.0,
                                 log=(log if log is not None else []).append)
    return openai.AsyncOpenAI(api_key="test", base_url="https://host.test/v1", max_retries=max_retries,
                              http_client=httpx2.AsyncClient(transport=waiting))


def ask(c: openai.AsyncOpenAI):
    return asyncio.run(c.chat.completions.create(model="m", messages=[{"role": "user", "content": "hi"}]))


def test_a_rate_limit_is_waited_out_instead_of_ending_the_run():
    seen, transport = provider([429, 429])
    clock = Clock()

    reply = ask(client(transport, clock))

    assert reply.choices[0].message.content == "ok"
    assert len(seen) == 3
    assert len(clock.sleeps) == 2 and all(0 < s <= llm.RATE_LIMIT_WINDOW_S for s in clock.sleeps)
    assert clock.sleeps[1] > clock.sleeps[0]          # backs off


@pytest.mark.parametrize("headers, wait", [
    ({"retry-after": "7"}, 8.0),                      # the host's wait, plus up to a second of jitter
    ({"retry-after-ms": "2500"}, 3.5),
    ({"retry-after": "0"}, 2.0),                      # never under a second: a zero would resend in a tight loop
    ({"retry-after": "-5"}, 2.0),
    ({"retry-after": "600"}, llm.RATE_LIMIT_WINDOW_S),
])
def test_the_hosts_retry_after_is_obeyed_within_bounds(headers, wait):
    seen, transport = provider([429], headers=headers)
    clock = Clock()

    ask(client(transport, clock))

    assert clock.sleeps == [wait]


@pytest.mark.parametrize("value", ["Wed, 29 Oct 2026 17:00:00 GMT", "nan", "soon"])
def test_a_retry_after_the_client_cant_read_falls_back_to_back_off(value):
    seen, transport = provider([429], headers={"retry-after": value})
    clock = Clock()

    ask(client(transport, clock))

    assert len(clock.sleeps) == 1 and 1.0 <= clock.sleeps[0] <= llm.RATE_LIMIT_WINDOW_S


def test_each_retry_sends_the_same_request_body():
    seen, transport = provider([429, 429])
    clock = Clock()

    ask(client(transport, clock))

    assert len({r.content for r in seen}) == 1 and b'"hi"' in seen[0].content


def test_a_limit_that_outlasts_the_deadline_fails_loudly_without_the_sdks_own_retries():
    seen, transport = provider([429] * 1000)
    clock = Clock()

    with pytest.raises(openai.RateLimitError):
        ask(client(transport, clock, max_retries=4))

    assert clock.now <= llm.RATE_LIMIT_DEADLINE_S
    tries = len(seen)
    assert tries == len(clock.sleeps) + 1             # one transport's worth of tries: the SDK added none


def test_other_errors_are_left_to_the_sdk():
    seen, transport = provider([500])
    clock = Clock()

    reply = ask(client(transport, clock, max_retries=1))

    assert reply.choices[0].message.content == "ok"
    assert clock.sleeps == []                          # the transport waited for nothing; the SDK retried the 500


def test_every_production_client_waits_out_rate_limits(monkeypatch):
    monkeypatch.setenv("FIREWORKS_API_KEY", "test")
    made = llm.make_client(config.ModelConfig(config.PROVIDERS["fireworks"], "accounts/fireworks/models/muse-spark-open"))

    assert isinstance(made._client._transport, llm.RateLimitRetry)


def test_every_wait_and_the_final_failure_are_logged_one_line_each():
    seen, transport = provider([429] * 1000)
    clock, log = Clock(), []

    with pytest.raises(openai.RateLimitError):
        ask(client(transport, clock, log=log))

    waits = [line for line in log if "waiting" in line]
    assert len(waits) == len(clock.sleeps) and waits[0] == "[rate-limit] host.test: 429, waiting 4.0 s (attempt 1)"
    assert log[-1].startswith("[rate-limit] host.test: 429 after") and "failing" in log[-1]
