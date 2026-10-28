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
}
LEAKY = {"script": "print(-7.5)", "notes": ""}
CLEAN = {"script": "print('computed')", "notes": "n/a"}
RESULTS = {"results": [{"name": "small_mean", "value": -6.9, "se": 1.2, "n": 22},
                       {"name": "t_diff", "value": -2.4, "se": None, "n": None},
                       {"name": "n_filings", "value": 38, "se": None, "n": None}],
           "sample": {"description": "x", "n": 38}, "notes": ""}


class FakeSandbox:
    def __init__(self, runs):
        self.runs, self.scripts = list(runs), []

    def __call__(self, script, *, market_cache, env, timeout_s):
        self.scripts.append(script)
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
    return asyncio.run(replicate.replicate("0000.00000", client, cfg, attempts=3, timeout_s=600,
                                           budget_usd=kw.get("budget"), runs_dir=tmp_path / "runs",
                                           sandbox=sandbox))


def test_end_to_end_with_a_guard_rejection_and_a_verdict(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900, 600)), (json.dumps(LEAKY), usage(800, 700, 500)),
                       (json.dumps(CLEAN), usage(1600, 700, 500))])
    sandbox = FakeSandbox([SandboxRun(0, "ok", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)

    assert outcome["verdict"] == "reproduced"
    assert len(api.requests) == 3                      # extract, leaky build, clean build
    assert sandbox.scripts == ["print('computed')"]   # the leaky script never ran
    folder = outcome["report"].parent
    text = outcome["report"].read_text()
    assert "rejected claim invented = 12.3: not in the paper's LaTeX" in text
    assert "paper numbers in the code: small_mean (-7.5)" in text
    assert "all on Meta: yes" in text
    assert "Not financial advice." in text
    assert len((folder / "calls.jsonl").read_text().splitlines()) == 3
    stages = [json.loads(line)["stage"] for line in (folder / "events.jsonl").read_text().splitlines()]
    assert stages[0] == "ingest" and stages[-1] == "verdict"


def test_failed_script_goes_back_to_the_builder_with_stderr(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(1, "", "KeyError: 'items'", 1.0),
                           SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert outcome["verdict"] == "reproduced"
    fix_request = api.requests[2]["body"]["messages"][-1]["content"]
    assert "exit code 1" in fix_request and "KeyError: 'items'" in fix_request


def test_missing_market_data_is_fetched_on_the_host_and_the_same_script_rerun(setup, monkeypatch):
    cfg, tmp_path = setup
    fetched = []
    monkeypatch.setattr(replicate.market, "fulfil", lambda requests, cache: fetched.extend(requests) or requests)
    request = [{"kind": "prices", "ticker": "ABC", "start": "2024-01-01", "end": "2024-02-01", "reason": "rate limited"}]
    log = [{"kind": "prices", "ticker": "ABC", "source": "yfinance (host) (cache)", "fetched": "2026-10-28"}]
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    sandbox = FakeSandbox([
        SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS), "market_data_requests.json": json.dumps(request)}),
        SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS), "market_data_log.json": json.dumps(log)}),
    ])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert fetched == request
    assert sandbox.scripts == ["print('computed')", "print('computed')"]
    assert "prices: yfinance (host) (cache), fetched 2026-10-28, 1 tickers" in outcome["report"].read_text()


def test_budget_stop_ends_the_run_and_still_writes_the_report(setup):
    cfg, tmp_path = setup
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps(CLEAN), usage(800, 700))])
    outcome = go(api, FakeSandbox([]), cfg, tmp_path, budget=0.000001)
    assert len(api.requests) == 1
    assert outcome["verdict"] == "no verdict"
    assert "BudgetExceeded" in outcome["report"].read_text()


def test_planned_budget_is_a_bound_on_the_calls():
    bound = replicate.planned_budget("muse-spark-1.3", "x" * 15000, attempts=3)
    assert 0 < bound < 2


def test_script_that_does_not_compile_never_reaches_the_sandbox(setup):
    cfg, tmp_path = setup
    broken = {"script": "x = f(1\n", "notes": ""}
    api = FakeChatAPI([(json.dumps(SPEC), usage(500, 900)), (json.dumps(broken), usage(800, 700)),
                       (json.dumps(CLEAN), usage(1600, 700))])
    sandbox = FakeSandbox([SandboxRun(0, "", "", 1.0, {"results.json": json.dumps(RESULTS)})])
    outcome = go(api, sandbox, cfg, tmp_path)
    assert sandbox.scripts == ["print('computed')"]
    assert "does not compile" in api.requests[2]["body"]["messages"][-1]["content"]
    assert outcome["verdict"] == "reproduced"
