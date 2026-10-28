"""An offline Chat Completions API for the tests: a real AsyncOpenAI client on an httpx
mock transport, so requests never leave the machine. Nothing here is part of the product."""

from __future__ import annotations

import json

import httpx2


def chat_completion(model: str, content: str, usage: dict) -> dict:
    return {
        "id": "chatcmpl-fake",
        "object": "chat.completion",
        "created": 0,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": usage,
    }


def usage(prompt: int, completion: int, reasoning: int = 0, cached: int = 0) -> dict:
    return {
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "total_tokens": prompt + completion,
        "prompt_tokens_details": {"cached_tokens": cached},
        "completion_tokens_details": {"reasoning_tokens": reasoning},
    }


class FakeChatAPI:
    """Answers each request with the next scripted (content, usage) reply and records it."""

    def __init__(self, replies: list[tuple[str, dict]]):
        self.replies = list(replies)
        self.requests: list[dict] = []

    def _handle(self, request: httpx2.Request) -> httpx2.Response:
        body = json.loads(request.content)
        self.requests.append({"path": request.url.path, "body": body})
        content, reply_usage = self.replies[len(self.requests) - 1]
        return httpx2.Response(200, json=chat_completion(body["model"], content, reply_usage))

    def http_client(self) -> httpx2.AsyncClient:
        return httpx2.AsyncClient(transport=httpx2.MockTransport(self._handle))
