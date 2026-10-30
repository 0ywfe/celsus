"""What the screen shows at one moment of a run: built by applying the timeline one item at a time."""

from __future__ import annotations

import re
from dataclasses import dataclass, replace

STAGES = ("read paper", "check paper", "build", "sandbox", "audit", "verdict")
TRACKER = {"ingest": "read paper", "extract": "read paper", "guard": "read paper", "check": "check paper",
           "build": "build", "tool": "build", "sandbox": "sandbox", "data": "sandbox", "audit": "audit",
           "verdict": "verdict", "error": "verdict"}
# Runs recorded before the ingest event carried fields say it in the message.
INGEST = re.compile(r"arXiv (?P<arxiv_id>\S+), .*?; (?P<model>\S+) at effort (?P<effort>\S+);")
ROUND = re.compile(r"^(?:round|attempt) (\d+)")
NUMBERS = re.compile(r"\((\d+) numbers to check\)")


@dataclass(frozen=True)
class Line:
    stage: str
    text: str
    style: str = ""


@dataclass(frozen=True)
class State:
    arxiv_id: str = ""
    title: str = ""
    model: str = ""
    effort: str = ""
    started: float | None = None
    now: float | None = None
    spent: float = 0.0
    calls: int = 0
    providers: tuple[str, ...] = ()
    makers: tuple[str, ...] = ()
    current: str | None = None
    done: tuple[str, ...] = ()
    round: int = 0
    lines: tuple[Line, ...] = ()
    verdict: str | None = None
    plain: tuple[Line, ...] = ()   # the plain view's sentences (cli/plain.py)
    numbers: int = 0               # numbers the paper reports, once read
    commands: int = 0              # commands the builder ran
    errors: int = 0                # of those, how many failed

    @property
    def elapsed(self) -> float:
        return 0.0 if self.started is None or self.now is None else self.now - self.started

    def status(self, stage: str) -> str:
        if self.verdict is not None or (stage in self.done and stage != self.current):
            return "done"
        return "active" if stage == self.current else "pending"


def apply(state: State, item: dict) -> State:
    state = replace(state, now=item["t"], started=item["t"] if state.started is None else state.started)
    if item["kind"] == "call":
        providers = state.providers if item["provider"] in state.providers else (*state.providers, item["provider"])
        made_by = item.get("maker", item["provider"])
        makers = state.makers if made_by in state.makers else (*state.makers, made_by)
        return replace(state, spent=state.spent + (item.get("cost_usd") or 0), calls=state.calls + 1,
                       providers=providers, makers=makers, model=state.model or item["model"])
    stage, message = item["stage"], item["message"]
    tracked = TRACKER.get(stage, state.current)
    done = state.done if state.current in (None, tracked) or state.current in state.done else (*state.done, state.current)
    state = replace(state, current=tracked, done=done)
    if stage == "ingest":
        found = INGEST.search(message)
        fields = {k: item.get(k) or (found[k] if found else "") for k in ("arxiv_id", "model", "effort")}
        state = replace(state, **{k: v for k, v in fields.items() if v})
    if item.get("title"):
        state = replace(state, title=item["title"])
    if (number := ROUND.match(message)) and stage in ("build", "sandbox", "audit"):
        state = replace(state, round=int(number[1]))
    if stage == "verdict":
        state = replace(state, verdict=item.get("verdict") or message)
    if stage == "extract" and (found := NUMBERS.search(message)):
        state = replace(state, numbers=int(found[1]))
    if stage == "tool":
        state = replace(state, commands=state.commands + message.startswith("$ "),
                        errors=state.errors + (item.get("exit", 0) != 0))
    from .plain import told   # here, not at the top: plain.py imports Line from this module
    return replace(state, lines=log(state.lines, item), plain=told(state.plain, item, state.model, state.numbers))


def log(lines: tuple[Line, ...], item: dict) -> tuple[Line, ...]:
    """The log with this event added. A command's exit code joins the command's own line."""
    stage, message = item["stage"], item["message"]
    if stage == "tool" and "exit" in item and lines and lines[-1].text.startswith("$ "):
        code = item["exit"]
        return (*lines[:-1], replace(lines[-1], text=f"{lines[-1].text}   exit {code}",
                                     style="tool" if code == 0 else "error"))
    return (*lines, line(item))


def line(item: dict) -> Line:
    stage, message = item["stage"], item["message"]
    if stage == "check":
        status = item.get("status", "ok")
        label = {"flag": "FLAG", "note": "NOTE"}.get(status, "ok")
        return Line(stage, f"{label:<5} {item.get('text', message)}", {"flag": "flag", "note": "note"}.get(status, "ok"))
    if stage == "tool":
        first, *rest = message.splitlines() or [""]
        return Line(stage, first + (" …" if rest else ""), "tool" if first.startswith("$ ") else "dim")
    if stage == "guard" and "rejected:" in message:
        return Line(stage, "✗ " + message.replace("script rejected:", "rejected:"), "reject")
    if stage == "audit":
        good = "sent back" not in message
        return Line(stage, ("✓ " if good else "✗ ") + message, "ok" if good else "flag")
    if stage == "extract" and item.get("problems"):
        return Line(stage, message, "flag")
    style = {"error": "error", "verdict": "verdict", "data": "note"}.get(stage, "")
    return Line(stage, message, style)
