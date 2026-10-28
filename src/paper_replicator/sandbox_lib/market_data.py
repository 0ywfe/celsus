"""Market data for replication scripts: the run's cache first, then yfinance live.

    from market_data import get_prices, get_market_cap, MarketDataUnavailable

    get_prices(ticker, start, end) -> pandas.DataFrame
        Daily bars with start <= date <= end (ISO dates, inclusive). Index: DatetimeIndex
        named "date" (trading days, tz-naive). Columns: open, high, low, close, adj_close, volume.
    get_market_cap(ticker) -> float
        Market capitalisation in USD as of the date the data was fetched (current, not historical).
    get_profile(ticker) -> dict
        Current company profile: {"sector", "industry", "beta", "name"} (any may be None).

All three raise MarketDataUnavailable when there is no data for the ticker. Every call is logged
with its source and fetch date. A request that neither the cache nor yfinance can serve is
recorded, so the host can fetch it once, cache it, and rerun the script.
"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path

import pandas as pd

COLUMNS = {"Open": "open", "High": "high", "Low": "low", "Close": "close", "Adj Close": "adj_close", "Volume": "volume"}


class MarketDataUnavailable(Exception):
    pass


def _cache() -> Path:
    return Path(os.environ.get("MARKET_CACHE", "/data/market"))


def _work() -> Path:
    return Path(os.environ.get("WORK_DIR", "/work"))


def _today() -> str:
    return datetime.date.today().isoformat()


def _iso(day) -> str:
    return pd.Timestamp(day).strftime("%Y-%m-%d")


def _append(name: str, entry: dict) -> None:
    path = _work() / name
    entries = json.loads(path.read_text()) if path.is_file() else []
    path.write_text(json.dumps(entries + [entry], indent=1))


def _manifest() -> dict:
    path = _cache() / "manifest.json"
    return json.loads(path.read_text()) if path.is_file() else {}


def yf_prices(ticker: str, start: str, end: str) -> pd.DataFrame:
    """yfinance daily bars, normalised. Shared by the sandbox and the host's cache fetch."""
    import yfinance as yf

    stop = (pd.Timestamp(end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    raw = yf.Ticker(ticker).history(start=start, end=stop, auto_adjust=False, actions=False)
    if raw.empty:
        return pd.DataFrame(columns=list(COLUMNS.values()))
    frame = raw.rename(columns=COLUMNS)[list(COLUMNS.values())]
    frame.index = pd.DatetimeIndex(frame.index).tz_localize(None).normalize()
    frame.index.name = "date"
    return frame


def yf_market_cap(ticker: str) -> float | None:
    import yfinance as yf

    cap = getattr(yf.Ticker(ticker).fast_info, "market_cap", None)
    return float(cap) if cap else None


def yf_profile(ticker: str) -> dict | None:
    import yfinance as yf

    info = yf.Ticker(ticker).info or {}
    profile = {"sector": info.get("sector"), "industry": info.get("industry"),
               "beta": info.get("beta"), "name": info.get("shortName")}
    return profile if any(v is not None for v in profile.values()) else None


def get_profile(ticker: str) -> dict:
    ticker = ticker.upper().strip()
    entry = _manifest().get("profiles", {}).get(ticker)
    if entry:
        _append("market_data_log.json", {"kind": "profile", "ticker": ticker, "source": f"{entry['source']} (cache)", "fetched": entry["fetched"]})
        if entry["value"] is None:
            raise MarketDataUnavailable(f"{ticker}: {entry['source']} had no profile on {entry['fetched']}")
        return dict(entry["value"])
    try:
        profile, reason = yf_profile(ticker), "empty"
    except Exception as error:
        profile, reason = None, f"{type(error).__name__}: {error}"
    if profile is None:
        _append("market_data_requests.json", {"kind": "profile", "ticker": ticker, "reason": reason})
        raise MarketDataUnavailable(f"{ticker}: no profile from yfinance in the sandbox ({reason})")
    _append("market_data_log.json", {"kind": "profile", "ticker": ticker, "source": "yfinance (live, sandbox)", "fetched": _today()})
    return profile


def get_prices(ticker: str, start, end) -> pd.DataFrame:
    ticker, start, end = ticker.upper().strip(), _iso(start), _iso(end)
    entry = _manifest().get("prices", {}).get(ticker)
    if entry and entry["start"] <= start and entry["end"] >= end:
        _append("market_data_log.json", {"kind": "prices", "ticker": ticker, "source": f"{entry['source']} (cache)", "fetched": entry["fetched"]})
        if not entry["rows"]:
            raise MarketDataUnavailable(f"{ticker}: {entry['source']} had no prices on {entry['fetched']}")
        return pd.read_parquet(_cache() / "prices" / f"{ticker}.parquet").loc[start:end]
    try:
        frame, reason = yf_prices(ticker, start, end), "empty"
    except Exception as error:
        frame, reason = None, f"{type(error).__name__}: {error}"
    if frame is None or frame.empty:
        _append("market_data_requests.json", {"kind": "prices", "ticker": ticker, "start": start, "end": end, "reason": reason})
        raise MarketDataUnavailable(f"{ticker}: no prices from yfinance in the sandbox ({reason})")
    _append("market_data_log.json", {"kind": "prices", "ticker": ticker, "source": "yfinance (live, sandbox)", "fetched": _today()})
    return frame


def get_market_cap(ticker: str) -> float:
    ticker = ticker.upper().strip()
    entry = _manifest().get("market_caps", {}).get(ticker)
    if entry:
        _append("market_data_log.json", {"kind": "market_cap", "ticker": ticker, "source": f"{entry['source']} (cache)", "fetched": entry["fetched"]})
        if entry["value"] is None:
            raise MarketDataUnavailable(f"{ticker}: {entry['source']} had no market cap on {entry['fetched']}")
        return float(entry["value"])
    try:
        cap, reason = yf_market_cap(ticker), "empty"
    except Exception as error:
        cap, reason = None, f"{type(error).__name__}: {error}"
    if cap is None:
        _append("market_data_requests.json", {"kind": "market_cap", "ticker": ticker, "reason": reason})
        raise MarketDataUnavailable(f"{ticker}: no market cap from yfinance in the sandbox ({reason})")
    _append("market_data_log.json", {"kind": "market_cap", "ticker": ticker, "source": "yfinance (live, sandbox)", "fetched": _today()})
    return cap
