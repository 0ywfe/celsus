"""The sandbox's market-data helper, run locally against a temporary cache."""

import json

import pandas as pd
import pytest

from paper_replicator.sandbox_lib import market_data


@pytest.fixture
def dirs(monkeypatch, tmp_path):
    cache, work = tmp_path / "cache", tmp_path / "work"
    (cache / "prices").mkdir(parents=True)
    work.mkdir()
    monkeypatch.setenv("MARKET_CACHE", str(cache))
    monkeypatch.setenv("WORK_DIR", str(work))
    return cache, work


def bars(start, end):
    index = pd.bdate_range(start, end, name="date")
    return pd.DataFrame({c: 1.0 for c in ["open", "high", "low", "close", "adj_close", "volume"]}, index=index)


def test_cache_is_read_first_and_logged_with_its_fetch_date(dirs):
    cache, work = dirs
    bars("2024-01-01", "2024-03-01").to_parquet(cache / "prices" / "ABC.parquet")
    (cache / "manifest.json").write_text(json.dumps({"prices": {"ABC": {
        "source": "yfinance (host)", "fetched": "2026-10-28", "start": "2024-01-01", "end": "2024-03-01", "rows": 44}}}))
    frame = market_data.get_prices("abc", "2024-01-10", "2024-01-20")
    assert frame.index.min() >= pd.Timestamp("2024-01-10") and frame.index.max() <= pd.Timestamp("2024-01-20")
    [entry] = json.loads((work / "market_data_log.json").read_text())
    assert entry == {"kind": "prices", "ticker": "ABC", "source": "yfinance (host) (cache)", "fetched": "2026-10-28"}


def test_yfinance_failure_is_recorded_as_a_request(dirs, monkeypatch):
    _, work = dirs
    def rate_limited(*args):
        raise RuntimeError("Too Many Requests")
    monkeypatch.setattr(market_data, "yf_prices", rate_limited)
    with pytest.raises(market_data.MarketDataUnavailable):
        market_data.get_prices("ABC", "2024-01-01", "2024-02-01")
    [request] = json.loads((work / "market_data_requests.json").read_text())
    assert request["ticker"] == "ABC" and "Too Many Requests" in request["reason"]


def test_ticker_the_host_also_could_not_fetch_is_unavailable_without_a_new_request(dirs):
    cache, work = dirs
    (cache / "manifest.json").write_text(json.dumps({"prices": {"GONE": {
        "source": "yfinance (host)", "fetched": "2026-10-28", "start": "2024-01-01", "end": "2024-03-01", "rows": 0}}}))
    with pytest.raises(market_data.MarketDataUnavailable):
        market_data.get_prices("GONE", "2024-01-10", "2024-01-20")
    assert not (work / "market_data_requests.json").exists()


def test_profile_comes_from_the_cache_with_its_fetch_date(dirs):
    cache, work = dirs
    (cache / "manifest.json").write_text(json.dumps({"profiles": {"ABC": {
        "source": "yfinance (host)", "fetched": "2026-10-28", "value": {"sector": "Technology", "beta": 1.2}}}}))
    assert market_data.get_profile("abc")["sector"] == "Technology"
    [entry] = json.loads((work / "market_data_log.json").read_text())
    assert entry["kind"] == "profile" and entry["fetched"] == "2026-10-28"
