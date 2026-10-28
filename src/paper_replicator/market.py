"""Host side of market data: serve what the sandbox could not fetch, once, into data/market/.

Prices go to data/market/prices/<TICKER>.parquet; manifest.json records source, fetch date and
range for each ticker, and market caps with their fetch date. The sandbox reads this cache.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

from .sandbox_lib import market_data

SOURCE = "yfinance (host)"


def _load(path: Path) -> dict:
    return json.loads(path.read_text()) if path.is_file() else {"prices": {}, "market_caps": {}}


def fulfil(requests: list[dict], cache_dir: Path) -> list[dict]:
    """Fetch every requested ticker on the host and cache it. Returns what was fetched."""
    (cache_dir / "prices").mkdir(parents=True, exist_ok=True)
    manifest_path = cache_dir / "manifest.json"
    manifest = _load(manifest_path)
    today = datetime.date.today().isoformat()
    fetched = []
    spans: dict[str, tuple[str, str]] = {}
    for request in (r for r in requests if r["kind"] == "prices"):
        start, end = spans.get(request["ticker"], (request["start"], request["end"]))
        spans[request["ticker"]] = (min(start, request["start"]), max(end, request["end"]))
    for ticker, (start, end) in spans.items():
        frame = market_data.yf_prices(ticker, start, end)
        frame.to_parquet(cache_dir / "prices" / f"{ticker}.parquet")
        manifest["prices"][ticker] = {"source": SOURCE, "fetched": today, "start": start, "end": end, "rows": len(frame)}
        fetched.append({"kind": "prices", "ticker": ticker, "rows": len(frame), "fetched": today})
    for ticker in {r["ticker"] for r in requests if r["kind"] == "market_cap"}:
        value = market_data.yf_market_cap(ticker)
        manifest["market_caps"][ticker] = {"source": SOURCE, "fetched": today, "value": value}
        fetched.append({"kind": "market_cap", "ticker": ticker, "value": value, "fetched": today})
    manifest_path.write_text(json.dumps(manifest, indent=1, sort_keys=True))
    return fetched
