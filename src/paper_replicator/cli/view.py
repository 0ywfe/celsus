"""The three screens from the sketch: the stage tracker, the live log and the verdict card."""

from __future__ import annotations

import json
from pathlib import Path

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .. import DISCLAIMER, PRODUCT_NAME
from ..compare import COULD_NOT_CHECK, Z95, with_unit
from .state import STAGES, State

GLYPH = {"done": "●", "active": "◐", "pending": "○"}
LINE_STYLES = {"flag": "bold yellow", "note": "dim", "ok": "green", "reject": "bold red", "error": "red",
               "verdict": "bold", "tool": "", "dim": "dim"}
# Red means the paper's numbers did not hold; a run that could not check is grey, never red.
VERDICT_STYLES = {"holds up": "green", "partly holds up": "yellow", "does not hold up": "red", COULD_NOT_CHECK: "grey62"}


def clock(seconds: float) -> str:
    minutes, rest = divmod(int(seconds), 60)
    return f"{minutes}:{rest:02d}"


def tracker(state: State) -> Group:
    title = Text.assemble((f" {PRODUCT_NAME.upper()}  ", "bold"), f"arXiv {state.arxiv_id}",
                          (f" · {state.title}" if state.title else "", "italic"))
    title.truncate(200, overflow="ellipsis")
    stages = Text(" ")
    for i, stage in enumerate(STAGES):
        status = state.status(stage)
        label = f"{stage} · round {state.round}" if status == "active" and stage in ("build", "sandbox", "audit") \
            and state.round > 1 else stage
        stages.append(f"{GLYPH[status]} {label}", style={"done": "green", "active": "bold cyan", "pending": "dim"}[status])
        if i < len(STAGES) - 1:
            stages.append(" ── ", style="dim")
    meta = Text(f"{state.model}{' · ' + state.effort if state.effort else ''} · ${state.spent:.2f} · "
                f"{clock(state.elapsed)}")
    if state.verdict is not None and state.providers:
        on_meta = state.providers == ("meta",)
        meta.append(" · all on Meta ✓" if on_meta else f" · providers: {', '.join(state.providers)}",
                    style="green" if on_meta else "yellow")
    row = Table.grid(expand=True)
    row.add_column(ratio=1, no_wrap=True, overflow="ellipsis")
    row.add_column(justify="right", no_wrap=True)
    row.add_row(stages, meta)
    return Group(title, row)


def log(state: State, height: int) -> Text:
    text = Text()
    for line in state.lines[-max(height, 1):]:
        text.append(f" {line.stage:<8}", style="dim")
        text.append(line.text.replace("\n", " ")[:160], style=LINE_STYLES.get(line.style, ""))
        text.append("\n")
    return text


def screen(state: State, height: int) -> Group:
    return Group(tracker(state), Text(""), log(state, height - 4))


def _reproduced(row: dict) -> str:
    value = row["reproduced"]
    if value is None:
        return "–"
    text = with_unit(f"{value:.4g}", row["unit"] if row["kind"] == "estimate" else "")
    return f"{text} ± {Z95 * row['se']:.2g}" if row["kind"] == "estimate" and row.get("se") else text


def _count(value) -> str:
    return "–" if value is None else f"{value:g}"


def _shown(path: Path) -> Path:
    try:
        return path.resolve().relative_to(Path.cwd())
    except ValueError:
        return path


def card(folder: Path) -> Panel:
    summary = json.loads((folder / "summary.json").read_text())
    rows = json.loads((folder / "comparison.json").read_text())["rows"] if (folder / "comparison.json").exists() else []
    style = VERDICT_STYLES.get(summary["verdict"], "")
    parts: list = [Text(summary["first_line"], style=f"bold {style}")]
    judged = [r for r in rows if r["kind"] != "count" and r["consistent"] is not None]
    if judged:
        table = Table(box=None, pad_edge=False, show_edge=False, expand=True)
        table.add_column("claim", ratio=3, overflow="fold")
        table.add_column("paper", justify="right", no_wrap=True)
        table.add_column("reproduced", justify="right", no_wrap=True)
        table.add_column("", ratio=2, no_wrap=True, overflow="ellipsis")
        for r in judged:
            mark = Text("✓ ", style="green") if r["consistent"] else Text("✗ ", style="red")
            table.add_row(r["name"], with_unit(f"{r['reported']:.4g}", r["unit"] if r["kind"] == "estimate" else ""),
                          _reproduced(r),
                          mark + Text(r["why"], style="dim"))
        parts += [Text(""), table]
    counts = [s for s in summary.get("sample") or [] if s.get("reported")]
    total = max(counts, key=lambda s: s["reported"]) if counts else None
    footer = [f"sample {_count(total['reproduced'])}/{_count(total['reported'])}" if total else None, f"{summary['rounds']} rounds", f"{summary['calls']} calls",
              f"${summary['cost_usd']:.2f}", clock(summary["wall_s"])]
    parts += [Text(""), Text(" · ".join(p for p in footer if p)), Text(DISCLAIMER, style="dim"),
              Text(f"report: {_shown(folder / 'report.md')}", style="dim")]
    return Panel(Group(*parts), border_style=style, title=f"{summary['paper']} · {summary['model']}",
                 title_align="left")
