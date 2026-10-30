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



def test_the_card_shows_the_main_result_and_mismatches_first():
    from paper_replicator.cli.view import shown_rows
    rows = [{"name": f"m{i}", "consistent": True} for i in range(10)] + [
        {"name": "bad", "consistent": False}, {"name": "main", "consistent": True}]
    shown, hidden = shown_rows(rows, "main", 4)
    assert [r["name"] for r in shown][:2] == ["main", "bad"] and len(shown) == 4 and hidden == 8


def test_a_sabotage_session_replays_each_plant_next_to_the_check_that_caught_it(tmp_path):
    import json as _json
    from rich.console import Console as _Console
    from paper_replicator.cli import sabotage_view
    folder = tmp_path / "sabotage-x"
    folder.mkdir()
    plants = [{"type": "B6", "run": "r", "paper": "2512.06144", "draw": 1, "state": "killed", "check": "authors' code",
               "detail": "github.com/a/b"},
              {"type": "B7", "run": "r", "paper": "2512.06144", "draw": 1, "state": "survived", "check": "",
               "detail": "verdict holds up with overall_mean_return changed"},
              {"type": "P2", "run": "r", "paper": "2512.06144", "draw": 2, "state": "survived", "check": "",
               "detail": "no new flag on the paper"}]
    events = [{"ts": f"2026-10-28T18:00:0{i}+00:00", "stage": "plant", "message": "m", **p} for i, p in enumerate(plants)]
    (folder / "events.jsonl").write_text("".join(_json.dumps(e) + "\n" for e in events))
    (folder / "plants.jsonl").write_text("".join(_json.dumps(p) + "\n" for p in plants))
    (folder / "baseline.json").write_text(_json.dumps([{"run": "r", "alarms": []}]))
    (folder / "reviewed.json").write_text(_json.dumps({"P2#r#2": {"state": "equivalent", "reason": "same test"}}))
    console = _Console(record=True, width=200)
    sabotage_view.replay(folder, 10, 0, console, sleep=lambda s: None)
    out = console.export_text()
    assert "✓ caught" in out and "authors' code" in out
    assert "✗ survived" in out and "overall_mean_return" in out
    assert "same test" in out                                  # the review's reason, not the raw "survived"
    assert "caught 1 of 2 plants (50%)" in out and "false alarms on the 1 clean runs: 0" in out


def test_the_demo_replays_a_stored_held_out_run_with_no_key(monkeypatch):
    """`paper-replicator demo` needs no API key, no Modal token and no runs/ folder: it replays a run shipped
    with the package (25b01b, held-out set 3, holds up) and ends on its verdict card."""
    from paper_replicator.cli.__main__ import DEMO_RUNS, demo
    for key in ("MODEL_API_KEY", "FIREWORKS_API_KEY", "BASETEN_API_KEY", "MODAL_TOKEN_ID", "SEC_USER_AGENT"):
        monkeypatch.delenv(key, raising=False)
    assert [p.name[-6:] for p in sorted(DEMO_RUNS.iterdir()) if p.is_dir()] == ["25b01b"]
    console = Console(record=True, width=160, color_system=None)
    state = demo(None, seconds=0, max_gap_s=0, console=console, sleep=lambda s: None)
    text = console.export_text()
    assert text.startswith("replay of run-20261030T045321Z-25b01b, recorded 2026-10-30 04:53 UTC")
    assert state.verdict == "holds up" and "The paper's numbers hold up" in text
    assert state.providers == ("fireworks",)


def test_the_demo_names_its_runs_when_asked_for_one_it_does_not_ship():
    import pytest
    from paper_replicator.cli.__main__ import demo
    with pytest.raises(SystemExit, match="25b01b"):
        demo("ffffff", seconds=0, max_gap_s=0, console=Console(record=True), sleep=lambda s: None)


def test_the_demo_paces_the_whole_run_to_about_thirty_seconds():
    """The README promises 30 seconds: the demo finds the speed at which the run's own pauses, each capped, add up
    to its target, and keeps the run's rhythm instead of an even tick."""
    from paper_replicator.cli.__main__ import DEMO_RUNS, demo, pace
    from paper_replicator.cli.timeline import load
    items = load(next(p for p in DEMO_RUNS.iterdir() if p.is_dir()))
    speed = pace(items, seconds=28, max_gap_s=1.5)
    total = sum(min((b["t"] - a["t"]) / speed, 1.5) for a, b in zip(items, items[1:]))
    assert abs(total - 28) < 0.5
    pauses = []
    demo(None, seconds=28, max_gap_s=1.5, console=Console(record=True, width=160, color_system=None),
         sleep=pauses.append)
    assert abs(sum(pauses) - 28) < 0.5
