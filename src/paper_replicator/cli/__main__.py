"""The terminal front end.

  python -m paper_replicator.cli check <arxiv_id> [replicate options]   run a check and watch it live
  python -m paper_replicator.cli replay <run id or folder> [--speed 10]  replay a recorded run at its own pace
  python -m paper_replicator.cli demo [run id]                          replay a run shipped with the package, no key

Both play the same files (events.jsonl and calls.jsonl in the run folder) through the same screens.
A replay is labelled as one, with the run's ID and date, so it is never passed off as live."""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.text import Text

from ..runs import RUNS_DIR
from . import sabotage_view
from .state import State, apply
from .timeline import Tail, load, merge
from .view import card, screen

POLL_S = 0.25  # how often a live run's folder is read
RUN_ID = re.compile(r"run-\d{8}T\d{6}Z-[0-9a-f]{6}")
# Runs shipped with the package so the screens can be seen with no API key, Modal token or runs/ folder: the files
# a replay reads (events, calls, summary, comparison), the report and the kept script, copied unchanged.
DEMO_RUNS = Path(__file__).parent / "demo"
DEMO_DEFAULT = "25b01b"   # held-out set 3, 2610.04221 draw 2: holds up, 84/84, main result consistent
DEMO_SECONDS = 28.0       # the README's "30 seconds", the verdict card included


def _folder(name: str) -> Path:
    path = Path(name)
    if path.is_dir():
        return path
    found = sorted(RUNS_DIR.glob(f"*{name}*"))
    if len(found) != 1:
        raise SystemExit(f"no single run matches {name!r} ({len(found)} found)")
    return found[0]


def replay(folder: Path, speed: float, max_gap_s: float, console: Console, sleep=time.sleep) -> State:
    """Plays the run at its own pace, `speed` times faster, with no pause longer than max_gap_s."""
    items = load(folder)
    console.print(Text(f"replay of {folder.name}, recorded {items[0]['ts'][:16].replace('T', ' ')} UTC"
                       f" · {speed:.3g}× speed", style="dim") if items else Text("empty run", style="red"))
    state, previous = State(), None
    with Live(screen(state, console.height), console=console, refresh_per_second=10) as live:
        for item in items:
            if previous is not None:
                sleep(min((item["t"] - previous) / speed, max_gap_s))
            previous, state = item["t"], apply(state, item)
            live.update(screen(state, console.height))
    if (folder / "summary.json").exists():
        console.print(card(folder, max_rows=max(console.height - 16, 6)))
    return state


def pace(items: list[dict], seconds: float, max_gap_s: float) -> float:
    """The speed at which the run's own pauses, each capped at max_gap_s, add up to `seconds`: the run keeps its
    rhythm (a long build reads as long) and still fits the time given."""
    gaps = [b["t"] - a["t"] for a, b in zip(items, items[1:])]
    played = lambda speed: sum(min(g / speed, max_gap_s) for g in gaps)
    if seconds <= 0 or not gaps:
        return math.inf
    slow, fast = 1e-6, 1e9
    for _ in range(100):   # played() falls as the speed rises: bisect on a log scale
        mid = math.sqrt(slow * fast)
        slow, fast = (mid, fast) if played(mid) > seconds else (slow, mid)
    return fast


def demo(run: str | None, seconds: float, max_gap_s: float, console: Console, sleep=time.sleep) -> State:
    """Replays a run shipped with the package (the default when run is None) in about `seconds`, labelled as a replay
    like any other, and ends on its verdict card."""
    shipped = sorted(p for p in DEMO_RUNS.iterdir() if p.is_dir())
    found = [p for p in shipped if p.name.endswith(run or DEMO_DEFAULT)]
    if len(found) != 1:
        raise SystemExit(f"no shipped run matches {run!r}; shipped: {', '.join(p.name[-6:] for p in shipped)}")
    return replay(found[0], pace(load(found[0]), seconds, max_gap_s), max_gap_s, console, sleep)


def check(args: list[str], console: Console) -> State:
    """Starts a run as its own process and follows its folder until the verdict."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    log = RUNS_DIR / "cli_last_run.out"
    with log.open("w") as out:
        process = subprocess.Popen([sys.executable, "-m", "paper_replicator.replicate", *args], stdout=out,
                                   stderr=subprocess.STDOUT)
    folder = None
    while folder is None:  # the run names itself on its first line; other runs may be starting too
        found = RUN_ID.search(log.read_text())
        folder = RUNS_DIR / found.group(0) if found else None
        if folder is None and process.poll() is not None:
            raise SystemExit(f"the run did not start; see {log}")
        time.sleep(POLL_S)
    events, calls, state = Tail(folder / "events.jsonl"), Tail(folder / "calls.jsonl"), State()
    with Live(screen(state, console.height), console=console, refresh_per_second=10) as live:
        while True:
            finished = process.poll() is not None
            for item in merge(events.read(), calls.read()):
                state = apply(state, item)
            if state.started is not None and state.verdict is None:
                state = replace(state, now=time.time())  # the clock runs between events
            live.update(screen(state, console.height))
            if finished:
                break
            time.sleep(POLL_S)
    if (folder / "summary.json").exists():
        console.print(card(folder, max_rows=max(console.height - 16, 6)))
    return state


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m paper_replicator.cli", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    play = sub.add_parser("replay", help="replay a recorded run")
    play.add_argument("run")
    play.add_argument("--speed", type=float, default=10.0, help="times faster than the run took")
    play.add_argument("--max-gap", type=float, default=1.5, help="longest pause between two lines, in seconds")
    shown = sub.add_parser("demo", help="replay a held-out run shipped with the package (no API key needed)")
    shown.add_argument("run", nargs="?", help=f"a shipped run's ID (default {DEMO_DEFAULT})")
    shown.add_argument("--seconds", type=float, default=DEMO_SECONDS, help="how long the replay takes, about")
    shown.add_argument("--max-gap", type=float, default=1.5, help="longest pause between two lines, in seconds")
    plants = sub.add_parser("sabotage", help="replay a saboteur session: each plant and the check that caught it")
    plants.add_argument("session")
    plants.add_argument("--speed", type=float, default=10.0, help="times faster than the session took")
    plants.add_argument("--max-gap", type=float, default=1.0, help="longest pause between two lines, in seconds")
    live = sub.add_parser("check", help="check a paper, live", add_help=False)
    live.add_argument("rest", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    console = Console()
    if args.command == "replay":
        replay(_folder(args.run), args.speed, args.max_gap, console)
    elif args.command == "demo":
        demo(args.run, args.seconds, args.max_gap, console)
    elif args.command == "sabotage":
        sabotage_view.replay(_folder(args.session), args.speed, args.max_gap, console)
    else:
        check(args.rest, console)


if __name__ == "__main__":
    main()
