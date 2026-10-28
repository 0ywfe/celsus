"""Host-side cache: a failed fetch is recorded, never raised."""

import json

from paper_replicator import market
from paper_replicator.sandbox_lib import market_data


def test_a_fetch_that_raises_is_cached_as_unavailable(tmp_path, monkeypatch):
    def broken(*args):
        raise KeyError("currentTradingPeriod")   # what yfinance raised in run 51e7e9
    monkeypatch.setattr(market_data, "yf_prices", broken)
    monkeypatch.setattr(market_data, "yf_market_cap", broken)
    requests = [{"kind": "prices", "ticker": "GONE", "start": "2024-01-01", "end": "2024-02-01"},
                {"kind": "market_cap", "ticker": "GONE"}]
    fetched = market.fulfil(requests, tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    assert manifest["prices"]["GONE"]["rows"] == 0 and "currentTradingPeriod" in manifest["prices"]["GONE"]["error"]
    assert manifest["market_caps"]["GONE"]["value"] is None
    assert len(fetched) == 2
