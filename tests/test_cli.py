"""The terminal screens, played from a small recorded run folder."""

import json

from rich.console import Console

from paper_replicator.cli.__main__ import replay
from paper_replicator.cli.state import State, apply
from paper_replicator.cli.timeline import Tail, load
from paper_replicator.cli.view import card, screen

T0 = "2026-10-28T15:36:{:02d}+00:00"
EVENTS = [
    {"stage": "ingest", "message": "run-x: arXiv 2512.06144, 15664 chars of LaTeX; muse-spark-1.3 at effort minimal; "
                                   "workbench builder; budget $3.0000"},
    {"stage": "extract", "message": "read: Market Reactions (27 numbers to check)", "title": "Market Reactions"},
    {"stage": "check", "message": "flag: size: 24 + 29 = 53, paper's total 54", "status": "flag",
     "text": "size: 24 + 29 = 53, paper's total 54"},
    {"stage": "build", "message": "round 1: the builder works in the sandbox (up to 30 turns)"},
    {"stage": "tool", "message": "$ python /work/replicate.py\n--more", "tool": "run"},
    {"stage": "tool", "message": "exit 1", "tool": "run", "exit": 1},
    {"stage": "guard", "message": "script rejected: it cuts the sample to a count the paper reports"},
    {"stage": "build", "message": "round 2: the builder works in the sandbox (up to 30 turns)"},
    {"stage": "audit", "message": "round 2: 27 results, sample matches the paper"},
    {"stage": "verdict", "message": "holds up ($0.2872 spent)", "verdict": "holds up"},
]
CALLS = [{"provider": "meta", "model": "muse-spark-1.3", "cost_usd": 0.1},
         {"provider": "meta", "model": "muse-spark-1.3", "cost_usd": 0.1872}]
SUMMARY = {"paper": "2512.06144", "model": "muse-spark-1.3", "verdict": "holds up", "rounds": 2, "calls": 2,
           "cost_usd": 0.2872, "wall_s": 338.2,
           "first_line": "The paper's numbers hold up: 1 of 1 checked results match within their uncertainty.",
           "sample": [{"name": "n", "reported": 54, "reproduced": 53}]}
ROWS = {"rows": [{"name": "small_mean", "kind": "estimate", "unit": "%", "reported": -7.49, "reproduced": -6.52,
                  "se": 2.24, "n": 23, "consistent": True, "why": "paper inside -6.52 +/- 4.39"},
                 {"name": "n", "kind": "count", "unit": "", "reported": 54, "reproduced": 53, "se": None, "n": None,
                  "consistent": True, "why": ""}]}


def recorded(tmp_path, summary=True):
    folder = tmp_path / "run-20261028T153637Z-abcdef"
    folder.mkdir()
    with (folder / "events.jsonl").open("w") as f:
        for i, e in enumerate(EVENTS):
            f.write(json.dumps({"ts": T0.format(i * 2), **e}) + "\n")
    with (folder / "calls.jsonl").open("w") as f:
        for i, c in enumerate(CALLS):
            f.write(json.dumps({"ts": T0.format(i * 6 + 1), **c}) + "\n")
    if summary:
        (folder / "summary.json").write_text(json.dumps(SUMMARY))
        (folder / "comparison.json").write_text(json.dumps(ROWS))
    return folder


def test_a_tail_reads_only_complete_lines(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text('{"a": 1}\n{"b": ')
    tail = Tail(path)
    assert tail.read() == [{"a": 1}]
    with path.open("a") as f:
        f.write('2}\n')
    assert tail.read() == [{"b": 2}] and tail.read() == []


def test_the_state_follows_the_run(tmp_path):
    items = load(recorded(tmp_path))
    assert [i["kind"] for i in items[:3]] == ["event", "call", "event"]   # calls interleave by time
    state = State()
    for item in items[:8]:
        state = apply(state, item)
    assert (state.arxiv_id, state.model, state.effort, state.title) == ("2512.06144", "muse-spark-1.3", "minimal",
                                                                         "Market Reactions")
    assert state.current == "build" and state.status("check paper") == "done" and state.status("audit") == "pending"
    assert state.lines[2].text.startswith("FLAG") and state.lines[2].style == "flag"
    assert state.lines[-1].text == "$ python /work/replicate.py …   exit 1"   # the exit joins its command
    assert state.lines[-1].style == "error"
    for item in items[8:]:
        state = apply(state, item)
    assert state.spent == 0.2872 and state.calls == 2 and state.providers == ("meta",)
    assert state.verdict == "holds up" and all(state.status(s) == "done" for s in ("read paper", "audit"))
    assert any(line.style == "reject" and line.text.startswith("✗ rejected:") for line in state.lines)
    assert state.elapsed == 18


def test_the_screens_render(tmp_path):
    folder = recorded(tmp_path)
    state = State()
    for item in load(folder):
        state = apply(state, item)
    console = Console(record=True, width=150, color_system=None)
    console.print(screen(state, 30))
    console.print(card(folder))
    text = console.export_text()
    assert "arXiv 2512.06144 · Market Reactions" in text
    assert "● read paper" in text and "all on Meta ✓" in text and "$0.29" in text
    assert "FLAG  size: 24 + 29 = 53, paper's total 54" in text
    assert "The paper's numbers hold up" in text and "-7.49%" in text and "-6.52% ± 4.4" in text
    assert "sample 53/54 · 2 rounds · 2 calls · $0.29" in text and "Not financial advice." in text


def test_a_replay_says_it_is_one_and_ends_on_the_card(tmp_path):
    folder = recorded(tmp_path)
    pauses = []
    console = Console(record=True, width=150, color_system=None)
    state = replay(folder, speed=10, max_gap_s=0.3, console=console, sleep=pauses.append)
    text = console.export_text()
    assert text.startswith("replay of run-20261028T153637Z-abcdef, recorded 2026-10-28 15:36 UTC")
    assert state.verdict == "holds up" and "The paper's numbers hold up" in text
    assert max(pauses) <= 0.3 and abs(pauses[0] - 0.1) < 1e-9   # 1 s apart at 10x, capped at 0.3 s


def test_a_run_without_a_summary_still_replays(tmp_path):
    state = replay(recorded(tmp_path, summary=False), 100, 0, Console(record=True, color_system=None),
                   sleep=lambda s: None)
    assert state.verdict == "holds up"
