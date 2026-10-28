"""The saboteur on screen: each plant next to the check that caught it, replayed from a session's files."""

from __future__ import annotations

import json
import time
from pathlib import Path

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .. import PRODUCT_NAME
from ..sabotage import BY_KEY, EQUIVALENT, FAILED, KILLED, NON_VIABLE, SURVIVED, plant_id, score
from .timeline import Tail, stamp

OUTCOME = {KILLED: ("✓ caught", "green"), SURVIVED: ("✗ survived", "bold red"), FAILED: ("– run failed", "yellow"),
           NON_VIABLE: ("· set aside", "dim"), EQUIVALENT: ("· set aside", "dim")}


def plant_line(record: dict, reviews: dict) -> Text:
    """One plant: what was planted, where, and what happened to it (after review, when there is one)."""
    review = reviews.get(plant_id(record))
    state = review["state"] if review else record["state"]
    label, style = OUTCOME[state]
    why = (review["reason"] if review else
           record["check"] + (f": {record['detail']}" if record["detail"] else "") if state == KILLED else
           record["detail"] or state)
    line = Text(f" {record['type']:<3}", style="bold")
    line.append(f"{BY_KEY[record['type']].name:<38}")
    line.append(f"{record['paper']:<12}", style="dim")
    line.append(f"{label:<12}", style=style)
    line.append(why.replace("\n", " ")[:110], style="" if state in (KILLED, SURVIVED) else "dim")
    return line


def card(folder: Path) -> Panel:
    rows = score(folder)
    table = Table(box=None, pad_edge=False, expand=True)
    for name, justify in (("plant", "left"), ("caught", "right"), ("survived", "right"), ("set aside", "right"),
                          ("caught by", "left")):
        table.add_column(name, justify=justify, overflow="fold")
    for row in rows:
        caught = f"{row[KILLED]}/{row['scored']}" if row["scored"] else "–"
        table.add_row(f"{row['type']} {row['name']}", Text(caught, style="green" if row[KILLED] == row["scored"]
                                                           else "yellow"),
                      Text(str(row[SURVIVED]), style="bold red" if row[SURVIVED] else "dim"),
                      str(row[NON_VIABLE] + row[EQUIVALENT]), ", ".join(row["checks"]))
    killed, scored = sum(r[KILLED] for r in rows), sum(r["scored"] for r in rows)
    bases = json.loads((folder / "baseline.json").read_text()) if (folder / "baseline.json").exists() else []
    alarms = sum(len(b["alarms"]) for b in bases)
    session = json.loads((folder / "session.json").read_text()) if (folder / "session.json").exists() else {}
    by_review = sum(r.get("by_review", 0) for r in rows)
    summary = Text(f"caught {killed} of {scored} plants" + (f" ({killed / scored:.0%})" if scored else "")
                   + (f", {killed - by_review} by code and {by_review} by the script reviewer" if by_review else "")
                   + f" · false alarms on the {len(bases)} clean runs: {alarms}", style="bold")
    footer = Text(f"checks at {session.get('commit', '?')} · saboteur {session.get('model', '?')} "
                  f"({session.get('saboteur_effort', '?')}) · set aside: the plant could not be applied, or "
                  "changed nothing", style="dim")
    return Panel(Group(summary, Text(""), table, Text(""), footer), title=f"{folder.name}", title_align="left")


def replay(folder: Path, speed: float, max_gap_s: float, console: Console, sleep=time.sleep) -> None:
    events = [e for e in Tail(folder / "events.jsonl").read() if e["stage"] in ("baseline", "plant")]
    reviews = json.loads((folder / "reviewed.json").read_text()) if (folder / "reviewed.json").exists() else {}
    console.print(Text(f" {PRODUCT_NAME.upper()}  saboteur · replay of {folder.name}", style="bold"))
    lines, previous = Text(), None
    with Live(lines, console=console, refresh_per_second=10) as live:
        for event in events:
            if previous is not None:
                sleep(min((stamp(event["ts"]) - previous) / speed, max_gap_s))
            previous = stamp(event["ts"])
            lines.append_text(plant_line(event, reviews) if event["stage"] == "plant"
                              else Text(f" clean run {event['message']}", style="dim"))
            lines.append("\n")
            live.update(lines)
    if (folder / "plants.jsonl").exists():
        console.print(card(folder))
