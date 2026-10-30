"""The plain view: one sentence per step of a run, built by code from its recorded events, for people who don't read
logs. Numbers are the ones recorded; an event with no plain sentence is left out here and stays in the log (--log)."""

from __future__ import annotations

import re

from .state import NUMBERS, Line

# The models' own names, as people say them; any other model shows as its short name.
SPOKEN = {"muse-spark-open": "Muse Spark Open", "muse-spark-1.3": "Muse Spark", "muse-wonder-1.0": "Muse Wonder"}
CHARS = re.compile(r"(\d+) chars of LaTeX")
PROBLEMS = re.compile(r"^(\d+) problems in the spec")
GROUNDED = re.compile(r"^(\d+) claims grounded in the LaTeX")
ROUND = re.compile(r"^(?:round|attempt) (\d+): ")
RESULTS = re.compile(r"(\d+) results")
SUMS = re.compile(r": (?P<sums>[\d.]+(?: \+ [\d.]+)+ = [\d.]+), paper's total (?P<total>[\d.]+)$")
SIDE = re.compile(r"t = (?P<t>\S+),? (?:and )?(?:paper's )?p = (?P<p>[^\s,]+)(?: matches (?P<side>[\w-]+))?")
# Lines whose text the view fills in at render time: the main result (needs the spec) and the command counter.
HEADLINE, COUNTER = "headline", "counter"


def spoken(model: str) -> str:
    short = (model or "").rsplit("/", 1)[-1]
    return SPOKEN.get(short, short)


def told(lines: tuple[Line, ...], item: dict, model: str, numbers: int) -> tuple[Line, ...]:
    """The plain lines with this event told, if it has a plain sentence."""
    stage, message = item["stage"], item["message"]
    if stage == "tool":   # every command is counted on one line that stays under the latest step
        return (*(line for line in lines if line.style != COUNTER), Line("build", "", COUNTER))
    said = sentence(stage, message, item, model, numbers)
    return (*lines, *said) if said else lines


def sentence(stage: str, message: str, item: dict, model: str, numbers: int) -> tuple[Line, ...]:
    round_ = ROUND.match(message)
    rest = message[round_.end():] if round_ else message
    if stage == "ingest" and (chars := CHARS.search(message)):
        return (Line("read", f"Reading the paper with {spoken(model)} ({int(chars[1]):,} characters of LaTeX)."),)
    if stage == "extract":
        if found := PROBLEMS.match(message):
            return (Line("read", f"{found[1]} problems in the first reading; Muse reads the paper again.", "flag"),)
        if found := NUMBERS.search(message):
            return (Line("read", f"Found {found[1]} numbers the paper reports."), Line("read", "", HEADLINE))
        return ()
    if stage == "guard":
        if found := GROUNDED.match(message):
            of = f" of {numbers}" if numbers else ""
            return (Line("check", f"{found[1]}{of} numbers found in the paper exactly as printed."),)
        if message.startswith("script rejected: "):
            reason = re.sub(r" \([^()]*(?:\([^()]*\)[^()]*)*\)$", "", message.removeprefix("script rejected: "))
            return (Line("build", f"Sent back by a coded check: {reason}.", "reject"),)
        return ()
    if stage == "check":
        return checked(item.get("status", "ok"), item.get("text", message))
    if stage == "build":
        if round_ and int(round_[1]) > 1:
            return (Line("build", f"Round {round_[1]}: Muse fixes the script and tries again."),)
        return (Line("build", "Muse is writing code to rebuild the study from public data."),)
    if stage == "sandbox":
        if rest.startswith("clean re-run") or rest.startswith("running in the sandbox"):
            return (Line("sandbox", "Running the finished script again in a fresh sandbox."),)
        return (Line("sandbox", f"The clean re-run failed: {rest}", "flag"),)
    if stage == "data" and (count := re.match(r"sandbox could not fetch (\d+) market-data items", message)):
        return (Line("sandbox", f"Fetching {count[1]} market-data series from the host instead."),)
    if stage == "audit" and (results := RESULTS.search(rest)):
        if "sample matches the paper" in rest:
            return (Line("audit", f"{results[1]} results, and the rebuilt sample matches the paper's counts.", "ok"),)
        return (Line("audit", f"{results[1]} results, but the rebuilt sample doesn't match the paper's counts; "
                              "Muse tries again.", "flag"),)
    if stage == "review":
        return (Line("audit", f"A review sent the script back: {rest.removesuffix('; sent back')}.", "flag"),)
    if stage == "error":
        return (Line("verdict", f"The run stopped: {message}", "error"),)
    if stage == "verdict":
        return (Line("verdict", f"Verdict: {item.get('verdict') or message.split(' ($')[0]}.", "verdict"),)
    return ()


def checked(status: str, text: str) -> tuple[Line, ...]:
    if found := SUMS.search(text):
        if status == "ok":
            return (Line("check", f"The paper's own sums add up: {found['sums']}.", "ok"),)
        return (Line("check", f"The paper's own sums don't add up: {found['sums']}, but its total is "
                              f"{found['total']}.", "flag"),)
    if found := SIDE.search(text):
        t, p = found["t"], found["p"]
        if found["side"] == "two-sided":
            return (Line("check", f"Its t = {t} and p = {p} agree.", "ok"),)
        if found["side"]:
            return (Line("check", f"Its t = {t} and p = {p} fit only a {found['side']} test.", "note"),)
        return (Line("check", f"Its t = {t} and p = {p} don't fit each other as printed; judged two-sided.",
                     "note"),)
    return ()
