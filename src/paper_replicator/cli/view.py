"""The three screens from the sketch: the stage tracker, the live log and the verdict card."""

from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console, ConsoleOptions, Group, RenderResult
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .. import DISCLAIMER, PRODUCT_NAME
from ..compare import COULD_NOT_CHECK, Z95, with_unit
from .state import STAGES, TRACKER, State

GLYPH = {"done": "●", "active": "◐", "pending": "○"}
LINE_STYLES = {"flag": "bold yellow", "note": "dim", "ok": "green", "reject": "bold red", "error": "red",
               "verdict": "bold", "tool": "", "dim": "dim"}
# Red means the paper's numbers did not hold; a run that could not check is grey, never red.
VERDICT_STYLES = {"holds up": "green", "partly holds up": "yellow", "does not hold up": "red", COULD_NOT_CHECK: "grey62"}
TAG = 1 + max(8, *map(len, TRACKER))   # the log's stage column: a margin, then the longest stage tag
GAP = 2                                # the least space between the stages and the badge on one line


def clock(seconds: float) -> str:
    minutes, rest = divmod(int(seconds), 60)
    return f"{minutes}:{rest:02d}"


def model_name(model: str | None) -> str:
    """A host's model path shows as the model's own name: accounts/fireworks/models/muse-spark-open as muse-spark-open."""
    return (model or "").rsplit("/", 1)[-1]


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
    meta = Text(f"{model_name(state.model)}{' · ' + state.effort if state.effort else ''} · ${state.spent:.2f} · "
                f"{clock(state.elapsed)}")
    if state.verdict is not None and state.providers:
        on_meta = state.makers == ("meta",)
        badge = (" · all on Meta ✓" if state.providers == ("meta",) else
                 f" · all Meta models ✓ (on {', '.join(state.providers)})" if on_meta else
                 f" · providers: {', '.join(state.providers)}")
        meta.append(badge, style="green" if on_meta else "yellow")
    return Group(title, StageBar(stages, meta))


class StageBar:
    """The stages with the model and cost on the right; where both don't fit, the model and cost go on the next line."""

    def __init__(self, stages: Text, meta: Text) -> None:
        self.stages, self.meta = stages, meta

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        if self.stages.cell_len + GAP + self.meta.cell_len <= options.max_width:
            row = Table.grid(expand=True)
            row.add_column(ratio=1, no_wrap=True, overflow="ellipsis")
            row.add_column(justify="right", no_wrap=True)
            row.add_row(self.stages, self.meta)
            yield row
            return
        for part in (self.stages.copy(), Text(" ") + self.meta):
            part.no_wrap, part.overflow = True, "ellipsis"
            yield part


def log(state: State, height: int) -> Table:
    """One row per line: the stage in a fixed column, the text beside it, wrapping under itself."""
    grid = Table.grid(expand=True)
    grid.add_column(width=TAG, no_wrap=True)
    grid.add_column(ratio=1, overflow="fold")
    for line in state.lines[-max(height, 1):]:
        grid.add_row(Text(f" {line.stage}", style="dim"),
                     Text(line.text.replace("\n", " ")[:160], style=LINE_STYLES.get(line.style, "")))
    return grid


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


def shown_rows(judged: list[dict], main: str | None, limit: int) -> tuple[list[dict], int]:
    """The rows that fit: the main result, then every mismatch, then matches; and how many were left out."""
    ordered = sorted(judged, key=lambda r: (r["name"] != main, bool(r["consistent"])))
    return ordered[:limit], max(len(ordered) - limit, 0)


def card(folder: Path, max_rows: int = 12) -> Panel:
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
        main = (summary.get("headline") or {}).get("name")
        shown, hidden = shown_rows(judged, main, max_rows)
        for r in shown:
            mark = Text("✓ ", style="green") if r["consistent"] else Text("✗ ", style="red")
            table.add_row(r["name"], with_unit(f"{r['reported']:.4g}", r["unit"] if r["kind"] == "estimate" else ""),
                          _reproduced(r),
                          mark + Text(r["why"], style="dim"))
        parts += [Text(""), table]
        if hidden:
            parts.append(Text(f"… {hidden} more matched; every row is in the report", style="dim"))
    counts = [s for s in summary.get("sample") or [] if s.get("reported")]
    total = max(counts, key=lambda s: s["reported"]) if counts else None
    footer = [f"sample {_count(total['reproduced'])}/{_count(total['reported'])}" if total else None, f"{summary['rounds']} rounds", f"{summary['calls']} calls",
              f"${summary['cost_usd']:.2f}", clock(summary["wall_s"])]
    parts += [Text(""), Text(" · ".join(p for p in footer if p)), Text(DISCLAIMER, style="dim"),
              Text(f"report: {_shown(folder / 'report.md')}", style="dim")]
    return Panel(Group(*parts), border_style=style, title=f"{summary['paper']} · {model_name(summary['model'])}",
                 title_align="left")
