"""Loading, caching, validating prices, and the data manifest."""
import hashlib
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

FIELDS = ["Open", "High", "Low", "Close", "Volume"]


def load_prices(ticker, start, end, cache_dir="data", refresh=False):
    """Daily adjusted OHLCV for one ticker. Downloads once, then reads the cache."""
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / f"{ticker}.csv"
    if refresh or not path.exists():
        import yfinance as yf  # imported here so tests never need the network

        df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
        if isinstance(df.columns, pd.MultiIndex):  # newer yfinance returns (field, ticker)
            df.columns = df.columns.get_level_values(0)
        df[FIELDS].to_csv(path)
    return pd.read_csv(path, index_col=0, parse_dates=True)


def check_prices(df, max_abs_return=0.40, max_gap_days=5):
    """Return a list of problems found. An empty list means the data passed."""
    problems = []
    if not df.index.is_monotonic_increasing:
        problems.append("index is not sorted")
    if df.index.has_duplicates:
        problems.append("duplicate dates")
    if df[FIELDS].isna().any().any():
        problems.append(f"missing values: {int(df[FIELDS].isna().sum().sum())}")
    if (df[["Open", "High", "Low", "Close"]] <= 0).any().any():
        problems.append("non-positive price")
    if (df["High"] < df[["Open", "Low", "Close"]].max(axis=1) - 1e-9).any():
        problems.append("High below Open/Low/Close")
    if (df["Low"] > df[["Open", "High", "Close"]].min(axis=1) + 1e-9).any():
        problems.append("Low above Open/High/Close")
    big = np.log(df["Close"]).diff().abs() > max_abs_return
    if big.any():
        problems.append(f"{int(big.sum())} daily moves above {max_abs_return:.0%}")
    gaps = df.index.to_series().diff().dt.days
    if (gaps > max_gap_days).any():
        problems.append(f"{int((gaps > max_gap_days).sum())} calendar gaps over {max_gap_days} days")
    return problems


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_manifest(tickers, cache_dir="data"):
    """Record source, download date and a hash of every cached file."""
    cache = Path(cache_dir)
    manifest = {
        "source": "Yahoo Finance via yfinance, auto_adjust=True",
        "written": date.today().isoformat(),
        "files": {t: _sha256(cache / f"{t}.csv") for t in tickers},
    }
    (cache / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def verify_manifest(cache_dir="data"):
    """True if every cached file still matches its recorded hash."""
    cache = Path(cache_dir)
    manifest = json.loads((cache / "manifest.json").read_text())
    return all(_sha256(cache / f"{t}.csv") == h for t, h in manifest["files"].items())
