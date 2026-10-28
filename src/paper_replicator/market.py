"""Host side of market data: serve what the sandbox could not fetch, once, into data/market/.

Prices go to data/market/prices/<TICKER>.parquet; manifest.json records source, fetch date and
range for each ticker, and market caps with their fetch date. The sandbox reads this cache.
A fetch that fails is cached as unavailable with its error, so the script drops that event; one bad
ticker never stops the run.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

import pandas as pd

from .sandbox_lib import market_data

SOURCE = "yfinance (host)"


def _load(path: Path) -> dict:
    manifest = json.loads(path.read_text()) if path.is_file() else {}
    return {"prices": {}, "market_caps": {}, "profiles": {}, **manifest}


def _try(fetch, *args):
    try:
        return fetch(*args), None
    except Exception as error:  # yfinance raises KeyError, HTTPError, ... for delisted or unknown symbols
        return None, f"{type(error).__name__}: {error}"


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
        frame, error = _try(market_data.yf_prices, ticker, start, end)
        frame = frame if frame is not None else pd.DataFrame(columns=list(market_data.COLUMNS.values()))
        frame.to_parquet(cache_dir / "prices" / f"{ticker}.parquet")
        manifest["prices"][ticker] = {"source": SOURCE, "fetched": today, "start": start, "end": end,
                                      "rows": len(frame), "error": error}
        fetched.append({"kind": "prices", "ticker": ticker, "rows": len(frame), "fetched": today, "error": error})
    for ticker in {r["ticker"] for r in requests if r["kind"] == "market_cap"}:
        value, error = _try(market_data.yf_market_cap, ticker)
        manifest["market_caps"][ticker] = {"source": SOURCE, "fetched": today, "value": value, "error": error}
        fetched.append({"kind": "market_cap", "ticker": ticker, "value": value, "fetched": today, "error": error})
    for ticker in {r["ticker"] for r in requests if r["kind"] == "profile"}:
        value, error = _try(market_data.yf_profile, ticker)
        manifest["profiles"][ticker] = {"source": SOURCE, "fetched": today, "value": value, "error": error}
        fetched.append({"kind": "profile", "ticker": ticker, "value": value, "fetched": today, "error": error})
    manifest_path.write_text(json.dumps(manifest, indent=1, sort_keys=True))
    return fetched
