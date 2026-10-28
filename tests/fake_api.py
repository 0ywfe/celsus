"""An offline Chat Completions API for the tests: a real AsyncOpenAI client on an httpx
mock transport, so requests never leave the machine. Nothing here is part of the product."""

from __future__ import annotations

import json

import httpx2


def chat_completion(model: str, content, usage: dict, turn: int = 0) -> dict:
    """content is the reply text, or a list of (tool name, arguments) for a tool-calling turn."""
    if isinstance(content, list):
        calls = [{"id": f"call_{turn}_{i}", "type": "function",
                  "function": {"name": name, "arguments": json.dumps(args)}}
                 for i, (name, args) in enumerate(content)]
        message, finish = {"role": "assistant", "content": None, "tool_calls": calls}, "tool_calls"
    else:
        message, finish = {"role": "assistant", "content": content}, "stop"
    return {
        "id": "chatcmpl-fake",
        "object": "chat.completion",
        "created": 0,
        "model": model,
        "choices": [{"index": 0, "message": message, "finish_reason": finish}],
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
    """Answers each request with the next scripted (content, usage) reply and records it. A standing reply answers
    every request whose instructions start with its prefix (a role a test does not script, such as the reviewer);
    those requests are recorded apart, so the scripted ones keep their order."""

    def __init__(self, replies: list[tuple[str, dict]], standing: dict[str, tuple[str, dict]] | None = None):
        self.replies = list(replies)
        self.standing = dict(standing or {})
        self.requests: list[dict] = []
        self.standing_requests: list[dict] = []

    def _handle(self, request: httpx2.Request) -> httpx2.Response:
        body = json.loads(request.content)
        system = next((str(m.get("content") or "") for m in body.get("messages", [])
                       if m.get("role") in ("system", "developer")), "")
        prefix = next((p for p in self.standing if system.startswith(p)), None)
        if prefix is not None:
            self.standing_requests.append({"path": request.url.path, "body": body})
            content, reply_usage = self.standing[prefix]
        else:
            self.requests.append({"path": request.url.path, "body": body})
            content, reply_usage = self.replies[len(self.requests) - 1]
        turn = len(self.requests) + len(self.standing_requests)
        return httpx2.Response(200, json=chat_completion(body["model"], content, reply_usage, turn))

    def http_client(self) -> httpx2.AsyncClient:
        return httpx2.AsyncClient(transport=httpx2.MockTransport(self._handle))
