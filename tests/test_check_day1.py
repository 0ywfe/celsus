import asyncio
import json

import pytest

from paper_replicator import check_day1, config
from paper_replicator.llm import MissingKeyError, make_client
from paper_replicator.pricing import cost_usd

from fake_api import FakeChatAPI, usage


@pytest.fixture
def spark(monkeypatch):
    monkeypatch.setenv("MODEL_API_KEY", "test-key")
    monkeypatch.delenv("QUICK_PROVIDER", raising=False)
    monkeypatch.delenv("QUICK_MODEL", raising=False)
    return config.tier("quick")


def run(api, cfg, tmp_path):
    client = make_client(cfg, max_retries=0, http_client=api.http_client())
    return asyncio.run(check_day1.run_check(client, cfg, tmp_path))


def ledger_rows(report):
    return [json.loads(line) for line in report["ledger"].read_text().splitlines()]


def test_correct_structured_answer_passes_and_is_logged(spark, tmp_path):
    api = FakeChatAPI([('{"product": 391}', usage(50, 300, reasoning=250))])
    report = run(api, spark, tmp_path)

    assert report["ok"], report["reason"]
    assert len(api.requests) == 1
    request = api.requests[0]
    assert request["path"].endswith("/chat/completions")
    body = request["body"]
    assert body["model"] == spark.model
    assert body["response_format"]["type"] == "json_schema"
    assert body["response_format"]["json_schema"]["strict"] is True
    assert body["max_tokens"] == check_day1.MAX_TOKENS
    assert body["reasoning_effort"] == check_day1.EFFORT
    assert "store" not in body

    [row] = ledger_rows(report)
    assert row["provider"] == "meta"
    assert row["model"] == spark.model
    assert row["role"] == "day1"
    assert (row["input_tokens"], row["output_tokens"], row["reasoning_tokens"]) == (50, 300, 250)
    assert row["cost_usd"] == cost_usd(spark.model, 50, 0, 300)


def test_wrong_answer_fails_in_code(spark, tmp_path):
    api = FakeChatAPI([('{"product": 390}', usage(50, 40))])
    report = run(api, spark, tmp_path)
    assert not report["ok"]
    assert "391" in report["reason"]
    assert len(ledger_rows(report)) == 1


def test_empty_content_fails_after_one_call(spark, tmp_path):
    # A reasoning model returns empty content when reasoning uses the whole budget.
    api = FakeChatAPI([("", usage(50, check_day1.MAX_TOKENS, reasoning=check_day1.MAX_TOKENS))])
    report = run(api, spark, tmp_path)
    assert not report["ok"]
    assert len(api.requests) == 1
    assert len(ledger_rows(report)) == 1


def test_missing_key_names_the_variable_only(monkeypatch, spark):
    monkeypatch.delenv("MODEL_API_KEY")
    with pytest.raises(MissingKeyError, match="MODEL_API_KEY"):
        make_client(spark)
