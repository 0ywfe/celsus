"""The whole slice offline: fake Chat Completions API, fake sandbox, no network."""

import asyncio
import json

import pytest

from paper_replicator import config, replicate
from paper_replicator.ledger import BudgetExceeded, Ledger
from paper_replicator.llm import make_client
from paper_replicator.sandbox import SandboxRun

from fake_api import FakeChatAPI, usage

LATEX = r"""\begin{document} Small firms fell $-7.5\%$ ($t=-3.1$) over 40 filings. \end{document}"""
SPEC = {
    "title": "A test paper", "hypothesis": "h", "data_sources": ["EDGAR"], "sample": "40 filings",
    "method": ["step"],
    "claims": [
        {"name": "small_mean", "description": "", "value": "-7.5", "unit": "%", "kind": "estimate", "where": ""},
        {"name": "t_diff", "description": "", "value": "-3.1", "unit": "", "kind": "test_statistic", "where": ""},
        {"name": "n_filings", "description": "", "value": "40", "unit": "", "kind": "count", "where": ""},
        {"name": "invented", "description": "", "value": "12.3", "unit": "%", "kind": "estimate", "where": ""},
    ],
    "headline": "small_mean",
    "partitions": [{"split": "all", "total": "n_filings", "parts": []}],
    "tests": [],
}
LEAKY = {"script": "results = [{'name': 'small_mean', 'value': -7.5}]", "notes": ""}
NO_FINDINGS = {"You review a replication script": (json.dumps({"findings": []}), usage(3000, 200))}
CLEAN = {"script": "print('computed')", "notes": "n/a"}
RESULTS = {"results": [{"name": "small_mean", "value": -6.9, "se": 1.2, "n": 22},
                       {"name": "t_diff", "value": -2.4, "se": None, "n": None},
                       {"name": "n_filings", "value": 38, "se": None, "n": None}],
           "sample": {"description": "x", "n": 38}, "notes": ""}


class FakeSandbox:
    def __init__(self, runs):
        self.runs, self.scripts, self.packages = list(runs), [], []

    def __call__(self, script, *, market_cache, env, timeout_s, packages=()):
        self.scripts.append(script)
        self.packages.append(packages)
        return self.runs[len(self.scripts) - 1]


@pytest.fixture
def setup(monkeypatch, tmp_path):
    monkeypatch.setenv("MODEL_API_KEY", "test-key")
    monkeypatch.setenv("SEC_USER_AGENT", "test agent test@example.com")
    monkeypatch.delenv("QUICK_PROVIDER", raising=False)
    monkeypatch.delenv("QUICK_MODEL", raising=False)
    monkeypatch.setattr(replicate, "load_paper", lambda arxiv_id, cache_dir: LATEX)
    monkeypatch.setattr(replicate, "MARKET_CACHE", tmp_path / "market")
    return config.tier("quick"), tmp_path


def go(api, sandbox, cfg, tmp_path, **kw):
    client = make_client(cfg, max_retries=0, http_client=api.http_client())
    return asyncio.run(replicate.replicate("0000.00000", client, cfg, attempts=kw.get("attempts", 3), timeout_s=600,
                                           budget_usd=kw.get("budget"), runs_dir=tmp_path / "runs",
                                           sandbox=sandbox, require_provider=kw.get("require_provider")))


def test_end_to_end_with_a_guard_rejection_and_a_verdict(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900, 600)), (json.dumps(LEAKY), usage(800, 700, 500)),
                       (json.dumps(CLEAN), usage(1600, 700, 500))])
    sandbox = FakeSandbox([SandboxRun(0, "ok", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)

    assert outcome["verdict"] == "holds up"
    assert len(api.requests) == 3                      # extract, leaky build, clean build
    assert sandbox.scripts == ["print('computed')"]   # the leaky script never ran
    folder = outcome["report"].parent
    text = outcome["report"].read_text()
    assert "rejected claim invented = 12.3: not in the paper's LaTeX" in text
    assert "contains the number the paper reports for them (small_mean (-7.5) at line 1)" in text
    assert "all on Meta: yes" in text
    assert "## The paper's own numbers" in text
    assert "Not financial advice." in text
    assert len((folder / "calls.jsonl").read_text().splitlines()) == 4   # extract, two builds, the reviewer
    assert len(api.standing_requests) == 1
    stages = [json.loads(line)["stage"] for line in (folder / "events.jsonl").read_text().splitlines()]
    assert stages[0] == "ingest" and stages[-1] == "verdict"


def test_failed_script_goes_back_to_the_builder_with_stderr(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(1, "", "KeyError: 'items'", 1.0),
                           SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert outcome["verdict"] == "holds up"
    fix_request = api.requests[2]["body"]["messages"][-1]["content"]
    assert "exit code 1" in fix_request and "KeyError: 'items'" in fix_request


def test_missing_market_data_is_fetched_on_the_host_and_the_same_script_rerun(setup, monkeypatch):
    cfg, tmp_path = setup
    fetched = []
    monkeypatch.setattr(replicate.market, "fulfil", lambda requests, cache: fetched.extend(requests) or requests)
    request = [{"kind": "prices", "ticker": "ABC", "start": "2024-01-01", "end": "2024-02-01", "reason": "rate limited"}]
    log = [{"kind": "prices", "ticker": "ABC", "source": "yfinance (host) (cache)", "fetched": "2026-10-28"}]
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([
        SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS), "market_data_requests.json": json.dumps(request)}),
        SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS), "market_data_log.json": json.dumps(log),
                                    "data_sources.json": json.dumps(["efts.sec.gov", "data-api.binance.vision"])}),
    ])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert fetched == request
    assert sandbox.scripts == ["print('computed')", "print('computed')"]
    report = outcome["report"].read_text()
    assert "prices: yfinance (host) (cache), fetched 2026-10-28, 1 tickers" in report
    assert "- other hosts the script fetched from: efts.sec.gov, data-api.binance.vision" in report


def test_budget_stop_ends_the_run_and_still_writes_the_report(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    outcome = go(api, FakeSandbox([]), cfg, tmp_path, budget=0.000001)
    assert len(api.requests) == 1
    assert outcome["verdict"] == "could not check"
    text = outcome["report"].read_text()
    assert "BudgetExceeded" in text
    assert text.startswith("We could not check this paper: the run stopped (BudgetExceeded).")
    summary = json.loads((outcome["report"].parent / "summary.json").read_text())
    assert summary["crashed"].startswith("BudgetExceeded") and summary["verdict"] == "could not check"


def test_a_run_restricted_to_another_provider_stops_before_its_first_call(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900))])
    outcome = go(api, FakeSandbox([]), cfg, tmp_path, require_provider="elsewhere")
    assert api.requests == []
    assert outcome["verdict"] == "could not check"
    assert "this run allows only elsewhere models, and the extractor's call goes to muse-spark-1.3 on meta" in outcome["report"].read_text()
    assert not (outcome["report"].parent / "calls.jsonl").exists()


def test_a_run_restricted_to_its_own_provider_runs(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    assert go(api, sandbox, cfg, tmp_path, require_provider="meta")["verdict"] == "holds up"


def test_planned_budget_is_a_bound_on_the_calls():
    bound = replicate.planned_budget("muse-spark-1.3", "x" * 15000, attempts=3)
    assert 0 < bound < 2


def test_script_that_does_not_compile_never_reaches_the_sandbox(setup):
    cfg, tmp_path = setup
    broken = {"script": "x = f(1\n", "notes": ""}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(broken), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert sandbox.scripts == ["print('computed')"]
    assert "does not compile" in api.requests[2]["body"]["messages"][-1]["content"]
    assert outcome["verdict"] == "holds up"


SHORT = {**RESULTS, "results": [{"name": "small_mean", "value": -6.9, "se": 1.2, "n": 12},
                                {"name": "n_filings", "value": 21, "se": None, "n": None}]}


def test_audit_sends_a_sample_mismatch_back_and_keeps_the_rerun(setup):
    cfg, tmp_path = setup
    first = {"script": "events = load()\nprint(len(events))", "notes": ""}
    fixed = {"script": "events = load(include_amendments=True)\nprint(len(events))", "notes": ""}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(first), usage(800, 700)),
                       (json.dumps(fixed), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "kept=21", "", 1.0, {"results.json": json.dumps(SHORT)}),
                           SandboxRun(0, "kept=38", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    feedback = api.requests[2]["body"]["messages"][-1]["content"]
    assert "n_filings: the paper reports 40, your run produced 21" in feedback
    assert "kept=21" in feedback and "Never filter, trim or pad" in feedback
    assert outcome["verdict"] == "holds up"
    assert (outcome["report"].parent / "results_attempt.txt").read_text() == "2"


def test_a_target_count_that_newly_appears_is_rejected(setup):
    cfg, tmp_path = setup
    first = {"script": "events = load()", "notes": ""}
    padded = {"script": "events = load()[:40]", "notes": ""}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(first), usage(800, 700)),
                       (json.dumps(padded), usage(1600, 700)), (json.dumps(first), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(SHORT)}),
                           SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(SHORT)})])
    outcome = go(api, sandbox, cfg, tmp_path, attempts=3)
    assert sandbox.scripts == ["events = load()", "events = load()"]   # the padded script never ran
    assert "cuts its sample to it (n_filings (40) at line 1)" in outcome["report"].read_text()


def test_direct_yfinance_import_is_rejected(setup):
    cfg, tmp_path = setup
    direct = {"script": "import yfinance as yf\nprint(1)", "notes": ""}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(direct), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert sandbox.scripts == ["print('computed')"]
    assert "imports yfinance directly" in outcome["report"].read_text()


def test_a_broken_audit_round_keeps_the_earlier_results(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(SHORT)}),
                           SandboxRun(1, "", "Traceback: boom", 1.0)])
    outcome = go(api, sandbox, cfg, tmp_path, attempts=2)
    rows = json.loads((outcome["report"].parent / "comparison.json").read_text())["rows"]
    assert {r["name"]: r["reproduced"] for r in rows}["n_filings"] == 21


class FakeWorkbench:
    added: tuple[list[str], list[str]] = ([], [])   # what installed() reports: (released packages, anything else)

    def __init__(self, **kwargs):
        self.files, self.commands, self.closed = {}, [], False

    def installed(self):
        return self.added

    def run(self, cmd):
        self.commands.append(cmd)
        return 0, "fields: items, form, file_date; UA test agent test@example.com"

    def write_file(self, path, content):
        self.files[path if path.startswith("/") else f"/work/{path}"] = content

    def read_text(self, path):
        return self.files.get(path)

    def close(self):
        self.closed = True


def test_workbench_builder_explores_writes_and_only_the_clean_rerun_counts(setup):
    cfg, tmp_path = setup
    benches = []

    def open_bench(**kwargs):
        benches.append(FakeWorkbench(**kwargs))
        return benches[-1]

    api = FakeChatAPI(standing=NO_FINDINGS, replies=[
        (json.dumps(SPEC), usage(500, 900)),
        ([("run", {"cmd": "curl -s efts | head"})], usage(900, 200)),
        ([("write_file", {"path": "replicate.py", "content": "print('computed')"})], usage(1200, 300)),
        ([("run", {"cmd": "python /work/replicate.py"})], usage(1500, 100)),
        ("Built 38 filings from EDGAR; amendments kept.", usage(1800, 80)),
    ])
    sandbox = FakeSandbox([SandboxRun(0, "kept=38", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    client = make_client(cfg, max_retries=0, http_client=api.http_client())
    outcome = asyncio.run(replicate.replicate("0000.00000", client, cfg, attempts=2, timeout_s=600, budget_usd=None,
                                              runs_dir=tmp_path / "runs", sandbox=sandbox, builder="workbench",
                                              turns=10, open_bench=open_bench))
    assert outcome["verdict"] == "holds up"
    [bench] = benches
    assert bench.commands == ["curl -s efts | head", "python /work/replicate.py"] and bench.closed
    assert sandbox.scripts == ["print('computed')"]                   # the clean re-run used the file it wrote
    build_body = api.requests[1]["body"]
    assert {t["function"]["name"] for t in build_body["tools"]} == {"run", "write_file"}
    assert "response_format" not in build_body and build_body.get("tool_choice") in (None, "auto")
    folder = outcome["report"].parent
    tools = [json.loads(l) for l in (folder / "events.jsonl").read_text().splitlines() if '"tool"' in l]
    assert any(e["message"].startswith("$ curl") for e in tools)
    assert (folder / "attempt_1_notes.md").read_text().startswith("Built 38 filings")
    tool_reply = [m for m in api.requests[2]["body"]["messages"] if m["role"] == "tool"][0]["content"]
    assert "test@example.com" not in tool_reply and "<SEC_USER_AGENT>" in tool_reply


def test_the_clean_rerun_installs_what_the_builder_installed_in_the_workbench(setup, monkeypatch):
    # run-20261029T022221Z-23f5c3: the workbench had pip-installed xlrd, the clean re-run died on ModuleNotFoundError
    cfg, tmp_path = setup
    monkeypatch.setattr(FakeWorkbench, "added", (["xlrd==2.0.1"], ["authors-pkg @ file:///work/pkg"]))
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[
        (json.dumps(SPEC), usage(500, 900)),
        ([("write_file", {"path": "replicate.py", "content": "import xlrd\nprint('computed')"})], usage(1200, 300)),
        ("Read the sheet with xlrd.", usage(1800, 80)),
    ])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    client = make_client(cfg, max_retries=0, http_client=api.http_client())
    outcome = asyncio.run(replicate.replicate("0000.00000", client, cfg, attempts=1, timeout_s=600, budget_usd=None,
                                              runs_dir=tmp_path / "runs", sandbox=sandbox, builder="workbench",
                                              turns=10, open_bench=lambda **kw: FakeWorkbench(**kw)))
    assert sandbox.packages == [("xlrd==2.0.1",)]
    folder = outcome["report"].parent
    assert (folder / "packages.txt").read_text() == "xlrd==2.0.1\n" and outcome["summary"]["packages"] == ["xlrd==2.0.1"]
    report = (folder / "report.md").read_text()
    assert "with the packages the builder installed: xlrd==2.0.1" in report
    assert "not installed in the clean run (not a released package): authors-pkg @ file:///work/pkg" in report


def test_cutting_the_sample_to_the_reported_count_is_rejected_in_the_first_round(setup):
    # run-20261028T144225Z-91ed39: SAMPLE_TARGET = 54; kept = filings[:SAMPLE_TARGET]
    cfg, tmp_path = setup
    cut = {"script": "SAMPLE_TARGET = 40\nkept = filings[:SAMPLE_TARGET]", "notes": ""}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(cut), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert sandbox.scripts == ["print('computed')"]
    assert "never trim, cut or pad" in api.requests[2]["body"]["messages"][-1]["content"]


def test_an_infrastructure_failure_keeps_the_earlier_good_results(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])

    class FlakySandbox(FakeSandbox):
        def __call__(self, script, **kw):
            if self.scripts:
                raise ConnectionError("modal went away")
            return super().__call__(script, **kw)

    outcome = go(api, FlakySandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(SHORT)})]), cfg, tmp_path)
    rows = json.loads((outcome["report"].parent / "comparison.json").read_text())["rows"]
    assert {r["name"]: r["reproduced"] for r in rows}["n_filings"] == 21     # the earlier results were kept
    text = outcome["report"].read_text()
    assert "clean run could not complete: ConnectionError" in text
    assert text.startswith("We could not check this paper: the replication could not rebuild the paper's sample")


def test_a_round_that_runs_out_of_turns_carries_its_conversation_into_the_next(setup):
    cfg, tmp_path = setup
    benches = []

    def open_bench(**kwargs):
        benches.append(FakeWorkbench(**kwargs))
        return benches[-1]

    api = FakeChatAPI(standing=NO_FINDINGS, replies=[
        (json.dumps(SPEC), usage(500, 900)),
        ([("run", {"cmd": "probe-1"})], usage(900, 200)),
        ([("run", {"cmd": "probe-2"})], usage(1000, 200)),                    # turn cap (2) reached here
        ([("write_file", {"path": "replicate.py", "content": "print('computed')"})], usage(1200, 300)),
        ("Done.", usage(1500, 80)),
    ])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    client = make_client(cfg, max_retries=0, http_client=api.http_client())
    outcome = asyncio.run(replicate.replicate("0000.00000", client, cfg, attempts=2, timeout_s=600, budget_usd=None,
                                              runs_dir=tmp_path / "runs", sandbox=sandbox, builder="workbench",
                                              turns=2, open_bench=open_bench))
    round_two = api.requests[3]["body"]["messages"]
    tool_replies = [m["content"] for m in round_two if m["role"] == "tool"]
    assert any("probe" not in r and "fields" in r for r in tool_replies)         # round one's tool output kept
    assert "turns are used up" in round_two[-1]["content"]
    assert "[tool call 1; a round allows 2 turns]" in tool_replies[0]
    assert outcome["verdict"] == "holds up"


def test_a_headline_written_as_prose_is_chosen_from_the_claim_names(setup):
    # Spark Open at high and xhigh wrote the headline as prose in 5 of 6 runs, and again when asked a second time
    cfg, tmp_path = setup
    prose = {**SPEC, "headline": "Small firms fell 7.5%"}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(prose), usage(500, 900)),
                                                     ("`small_mean`\n\n\n", usage(200, 20)),
                                                     (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    choice = api.requests[1]["body"]
    assert "Small firms fell 7.5%" in choice["messages"][-1]["content"] and "invented" in choice["messages"][-1]["content"]
    assert "response_format" not in choice and choice["max_tokens"] == 4 * 3_419   # 3 of 12 ran to 100,920 tokens
    assert len(api.requests) == 3                                                    # no second extraction
    assert outcome["summary"]["headline"]["name"] == "small_mean"
    assert "chosen from the claim names: small_mean" in outcome["report"].read_text()


def test_a_chooser_answer_that_names_no_claim_falls_back_to_asking_for_the_spec_again(setup):
    # run-20261029T030101Z-a01d12: the chooser's reply was cut off at its cap and the whole run stopped
    cfg, tmp_path = setup
    prose = {**SPEC, "headline": "Small firms fell 7.5%"}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(prose), usage(500, 900)),
                                                     ("The main result is the small-firm decline", usage(200, 20)),
                                                     (json.dumps(SPEC), usage(500, 900)),
                                                     (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert "headline 'Small firms fell 7.5%' is not the name of a claim" in api.requests[2]["body"]["messages"][-1]["content"]
    assert outcome["summary"]["headline"]["name"] == "small_mean" and outcome["verdict"] == "holds up"


def test_a_spec_with_unresolved_references_is_asked_for_once_more(setup):
    cfg, tmp_path = setup
    bad = {**SPEC, "partitions": [{"split": "all", "total": "n_all", "parts": []}]}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(bad), usage(500, 900)), (json.dumps(SPEC), usage(500, 900)),
                       (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    retry = api.requests[1]["body"]["messages"][-1]["content"]
    assert "partition 'all': total 'n_all' is not the name of a claim" in retry
    assert outcome["summary"]["headline"]["name"] == "small_mean"


def test_references_still_unresolved_after_the_retry_are_reported_not_skipped(setup):
    cfg, tmp_path = setup
    bad = {**SPEC, "partitions": [{"split": "all", "total": "n_all", "parts": []}]}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(bad), usage(500, 900)), (json.dumps(bad), usage(500, 900)),
                       (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert outcome["verdict"] == "holds up"
    assert "spec problem unresolved: partition 'all': total 'n_all' is not the name of a claim" in (
        outcome["report"].read_text())


def test_a_spec_with_no_result_in_it_is_asked_for_once_more(setup):
    # 2610.36491 (Spark Open xhigh): 11 claims, all sample counts, though the LaTeX prints Sharpe and return tables
    cfg, tmp_path = setup
    counts_only = {**SPEC, "claims": [c for c in SPEC["claims"] if c["kind"] == "count"], "headline": "n_filings"}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(counts_only), usage(500, 900)),
                                                     (json.dumps(SPEC), usage(500, 900)),
                                                     (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert "the spec lists only sample sizes" in api.requests[1]["body"]["messages"][-1]["content"]
    assert outcome["summary"]["headline"]["name"] == "small_mean"


def test_the_workbench_refuses_to_fetch_the_authors_code(setup):
    cfg, tmp_path = setup
    benches = []

    def open_bench(**kwargs):
        benches.append(FakeWorkbench(**kwargs))
        return benches[-1]

    api = FakeChatAPI(standing=NO_FINDINGS, replies=[
        (json.dumps(SPEC), usage(500, 900)),
        ([("run", {"cmd": "git clone https://github.com/authors/paper-code"})], usage(900, 200)),
        ([("write_file", {"path": "replicate.py", "content": "print('computed')"})], usage(1200, 300)),
        ("Built it from the paper.", usage(1800, 80)),
    ])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    client = make_client(cfg, max_retries=0, http_client=api.http_client())
    outcome = asyncio.run(replicate.replicate("0000.00000", client, cfg, attempts=2, timeout_s=600, budget_usd=None,
                                              runs_dir=tmp_path / "runs", sandbox=sandbox, builder="workbench",
                                              turns=10, open_bench=open_bench))
    [bench] = benches
    assert bench.commands == []                                   # the clone never reached the sandbox
    reply = [m for m in api.requests[2]["body"]["messages"] if m["role"] == "tool"][0]["content"]
    assert reply.startswith("refused: git clone")
    events = (outcome["report"].parent / "events.jsonl").read_text()
    assert "refused: git clone" in events and outcome["verdict"] == "holds up"


def test_a_script_that_fetches_code_is_rejected(setup):
    cfg, tmp_path = setup
    fetch = {"script": "import requests\nexec(requests.get('https://raw.githubusercontent.com/a/b/main/run.py').text)",
             "notes": ""}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(fetch), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert sandbox.scripts == ["print('computed')"]
    assert "code host" in outcome["report"].read_text()



def test_a_script_that_sets_its_own_sec_contact_is_rejected(setup):
    cfg, tmp_path = setup
    own = {"script": "import os\nos.environ['SEC_USER_AGENT'] = 'author@university.edu'\nprint('computed')", "notes": ""}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(own), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert sandbox.scripts == ["print('computed')"]
    assert "SEC contact" in outcome["report"].read_text()


def test_the_workbench_refuses_a_command_or_file_that_carries_a_contact(setup):
    cfg, tmp_path = setup
    benches = []

    def open_bench(**kwargs):
        benches.append(FakeWorkbench(**kwargs))
        return benches[-1]

    api = FakeChatAPI(standing=NO_FINDINGS, replies=[
        (json.dumps(SPEC), usage(500, 900)),
        ([("run", {"cmd": 'curl -A "author@university.edu" https://data.sec.gov/submissions/CIK0000320193.json'})],
         usage(900, 200)),
        ([("write_file", {"path": "fetch.py", "content": "H = {'User-Agent': 'author@university.edu'}"})], usage(1000, 200)),
        ([("write_file", {"path": "replicate.py", "content": "print('computed')"})], usage(1200, 300)),
        ("Built it from the paper.", usage(1800, 80)),
    ])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    client = make_client(cfg, max_retries=0, http_client=api.http_client())
    outcome = asyncio.run(replicate.replicate("0000.00000", client, cfg, attempts=2, timeout_s=600, budget_usd=None,
                                              runs_dir=tmp_path / "runs", sandbox=sandbox, builder="workbench",
                                              turns=10, open_bench=open_bench))
    [bench] = benches
    assert bench.commands == [] and "/work/fetch.py" not in bench.files   # neither reached the sandbox
    replies = [m["content"] for r in api.requests[2:4] for m in r["body"]["messages"] if m["role"] == "tool"]
    assert replies[0].startswith("refused: author@university.edu") and replies[-1].startswith("refused: author@university.edu")
    assert outcome["verdict"] == "holds up"


def test_a_sample_that_misses_the_papers_period_is_sent_back_then_could_not_check(setup):
    cfg, tmp_path = setup
    dated = {**SPEC, "period_start": "2010-01-03", "period_end": "2025-12-31"}
    late = {**RESULTS, "sample": {"description": "x", "n": 38, "start": "2014-09-17", "end": "2025-12-31"}}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(dated), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(late)})] * 2)
    outcome = go(api, sandbox, cfg, tmp_path, attempts=2)
    feedback = api.requests[2]["body"]["messages"][-1]["content"]
    assert "covers 2014-09-17 to 2025-12-31, but the paper's runs from 2010-01-03" in feedback
    assert outcome["verdict"] == "could not check"
    assert outcome["summary"]["first_line"].startswith(
        "We could not check this paper: the replication's sample covers 2014-09-17")



def test_a_sample_the_builder_says_differs_from_the_papers_is_could_not_check(setup):
    # run 2601.08263: the live API no longer has the authors' snapshot of exploits; the notes said so,
    # yet the verdict blamed the paper
    cfg, tmp_path = setup
    other = {**RESULTS, "sample": {"description": "x", "n": 38, "same_as_paper": False,
                                   "differences": "the 2021-2024 exploit snapshot is not recoverable"}}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(other)})])
    outcome = go(api, sandbox, cfg, tmp_path, attempts=1)
    assert outcome["verdict"] == "could not check"
    assert "the replication could not rebuild the paper's sample (the 2021-2024 exploit snapshot is not " \
           "recoverable)" in outcome["summary"]["first_line"]


def declared(missing, extra):
    return {**RESULTS, "sample": {"description": "x", "n": 38, "same_as_paper": False, "missing": missing,
                                  "extra": extra, "differences": "one filer has no ticker, so no prices"}}


def test_a_sample_short_by_fewer_observations_than_the_count_band_is_judged_and_says_so(setup):
    # the breach paper at adf5c76: 53 of the paper's 54 filings (one unlisted filer has no prices); the builder said
    # "not the paper's sample", and the run was could not check, though the count audit accepts 53 against 54
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(declared(1, 0))})])
    outcome = go(api, sandbox, cfg, tmp_path, attempts=1)
    assert outcome["verdict"] == "holds up"
    assert "1 missing and 0 extra observations" in outcome["report"].read_text()


@pytest.mark.parametrize("missing, extra", [(20, 0), (6, 7), (None, None), ("a few", 0)])
def test_a_sample_that_differs_by_more_than_the_band_or_by_an_unknown_amount_is_could_not_check(setup, missing, extra):
    cfg, tmp_path = setup
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(declared(missing, extra))})])
    outcome = go(api, sandbox, cfg, tmp_path, attempts=1)
    assert outcome["verdict"] == "could not check"
    assert "could not rebuild the paper's sample (one filer has no ticker" in outcome["summary"]["first_line"]


def test_a_sample_total_left_out_of_the_results_is_could_not_check(setup):
    # same run: the counts that disagreed were removed from the results, so the audit had nothing to compare
    cfg, tmp_path = setup
    no_count = {**RESULTS, "results": [r for r in RESULTS["results"] if r["name"] != "n_filings"]}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(no_count)})])
    outcome = go(api, sandbox, cfg, tmp_path, attempts=1)
    assert outcome["verdict"] == "could not check"
    assert "did not report the paper's sample size (n_filings)" in outcome["summary"]["first_line"]



def test_a_paper_whose_source_cannot_be_read_is_could_not_check_not_a_crash(setup, monkeypatch):
    # held-out launch, 28 Oct: an arXiv ID with no source raised HTTPStatusError and the run left no report
    cfg, tmp_path = setup

    def missing(arxiv_id, cache_dir):
        raise RuntimeError("Client error '404 Not Found'")

    monkeypatch.setattr(replicate, "load_paper", missing)
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[])
    outcome = go(api, FakeSandbox([]), cfg, tmp_path)
    assert outcome["verdict"] == "could not check" and api.requests == []
    assert outcome["summary"]["crashed"] is None
    assert outcome["summary"]["first_line"].startswith(
        "We could not check this paper: the paper's LaTeX source could not be read from arXiv (RuntimeError")


def finding(passage, rule=1, why="the result is set, not computed"):
    return json.dumps({"findings": [{"rule": rule, "passage": passage, "why": why}]})


NONE = json.dumps({"findings": []})


def test_the_reviewer_sends_a_script_back_with_the_passage_and_the_fixed_script_is_reported(setup):
    cfg, tmp_path = setup
    fixed = {"script": "print('computed again')", "notes": ""}
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (finding("print('computed')"), usage(3000, 200)), (json.dumps(fixed), usage(900, 700)),
                       (NONE, usage(3000, 100))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})] * 2)
    outcome = go(api, sandbox, cfg, tmp_path)
    assert outcome["verdict"] == "holds up"
    sent_back = api.requests[3]["body"]["messages"][-1]["content"]
    assert sent_back.startswith("Before its numbers are reported, a reviewer found 1 breach")
    assert "print('computed')" in sent_back
    assert "a reviewer found 1 breach" in outcome["report"].read_text()   # listed under the run's guards


def test_every_finding_reaches_the_builder_and_the_runs_events(setup):
    """29 Oct, held-out f93ef5: the reviewer reported 3 breaches but only the first was kept, so whether the
    other two named a construction the run kept is unknown."""
    cfg, tmp_path = setup
    script = "x = 1\nprint('computed')"
    two = json.dumps({"findings": [{"rule": 2, "passage": "x = 1", "why": "a value is set"},
                                   {"rule": 1, "passage": "print('computed')", "why": "a result is printed"}]})
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps({"script": script, "notes": ""}), usage(800, 700)),
                       (two, usage(3000, 200)), (json.dumps({"script": "print('computed again')", "notes": ""}), usage(900, 700)),
                       (NONE, usage(3000, 100))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})] * 2)
    outcome = go(api, sandbox, cfg, tmp_path)

    sent_back = api.requests[3]["body"]["messages"][-1]["content"]
    assert "a reviewer found 2 breaches" in sent_back and "x = 1" in sent_back and "print('computed')" in sent_back
    events = [json.loads(l) for l in (outcome["report"].parent / "events.jsonl").read_text().splitlines()]
    review = next(e for e in events if e["stage"] == "review")
    assert [f["passage"] for f in review["findings"]] == ["x = 1", "print('computed')"]


def test_a_finding_whose_passage_is_not_in_the_script_is_ignored(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (finding("x = 0.35  # not in the script"), usage(3000, 200))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    assert go(api, sandbox, cfg, tmp_path)["verdict"] == "holds up"


def test_a_breach_still_there_after_the_last_attempt_is_could_not_check_with_the_reason(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (finding("print('computed')"), usage(3000, 200)), (json.dumps(CLEAN), usage(900, 700)),
                       (finding("print('computed')"), usage(3000, 200))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})] * 2)
    outcome = go(api, sandbox, cfg, tmp_path, attempts=2)
    assert outcome["verdict"] == "could not check"
    assert outcome["report"].read_text().startswith("We could not check this paper: a reviewer found 1 breach")


def test_a_breach_fixed_in_a_later_attempt_is_not_named_in_the_verdict(setup):
    # 2603.25285: round 1's hard-coded 30 was fixed in round 2, but the first line still named it after round 3
    cfg, tmp_path = setup
    fixed = {"script": "print('computed again')", "notes": ""}
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (finding("print('computed')"), usage(3000, 200)), (json.dumps(fixed), usage(900, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)}),
                           SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(SHORT)})])
    outcome = go(api, sandbox, cfg, tmp_path, attempts=2)
    report = outcome["report"].read_text()
    assert outcome["verdict"] == "could not check"
    assert "reviewer" not in report.splitlines()[0]
    assert "a reviewer found 1 breach" in report   # still listed under the run's guards, as round 1's


def test_an_impossible_result_goes_back_to_the_builder(setup):
    cfg, tmp_path = setup
    bad = {"results": [{"name": "small_mean", "value": -6.9, "se": 1.2, "n": 38},
                       {"name": "t_diff", "value": -2.4, "se": None, "n": None},
                       {"name": "n_filings", "value": -38, "se": None, "n": None}],
           "sample": {"description": "x", "n": 38}, "notes": ""}
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(bad)}),
                           SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    go(api, sandbox, cfg, tmp_path)
    feedback = api.requests[2]["body"]["messages"][-1]["content"]
    assert "n_filings = -38: no count is negative" in feedback and "never clip or replace" in feedback


def test_a_meta_model_on_another_host_passes_the_meta_guard_and_the_report_says_where(setup, monkeypatch):
    cfg, tmp_path = setup
    from paper_replicator import config as configuration
    hosted = configuration.ModelConfig(configuration.PROVIDERS["baseten"], "meta-models/muse-spark-open-1026")
    monkeypatch.setenv("BASETEN_API_KEY", "test-key")
    api = FakeChatAPI(standing=NO_FINDINGS, replies=[(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, hosted, tmp_path, require_provider="meta")
    assert outcome["verdict"] == "holds up"
    assert "all on Meta: yes (Meta models; meta-models/muse-spark-open-1026 on baseten)" in outcome["report"].read_text()
    calls = [json.loads(line) for line in (outcome["report"].parent / "calls.jsonl").read_text().splitlines()]
    assert {(c["provider"], c["maker"]) for c in calls} == {("baseten", "meta")}
