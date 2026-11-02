# quant-backtester

An event-driven backtesting engine built to be honest, not impressive: it tracks transaction costs,
tests out-of-sample, and logs every parameter variant tried so results can't be silently cherry-picked.

**Status:** Week 1 in progress (data layer).

## Design rules
1. A signal may only use data up to the close of day `t` (no lookahead).
2. All P&L goes through the engine or `strategy_returns()`, never a signal multiplied by same-day returns.
3. Two fill modes: `next_close` (correctness check against a vectorized backtest) and `next_open` (realistic).
4. Every result is reported through `summarize()`.
5. The test period is touched once, at the end, and the run is logged.
6. Every variant tried is logged to `trial_log.json`; the trial count `N` is reported here.
7. `HYPOTHESES.md` is written before looking at the test period.

## Repo layout
```
quantlib/      core library (data, metrics, events, engine, research, trials)
tests/         pytest unit tests
notebooks/     exploratory notebooks (not the source of truth for results)
data/          cached price CSVs + manifest.json (source, date, SHA-256 hashes)
HYPOTHESES.md  hypotheses and parameter ranges, frozen before the test run
trial_log.json log of every variant tried
```

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Run tests
```bash
pytest -q
```

## Data
- Source: Yahoo Finance via `yfinance`, adjusted close prices.
- Every download is validated with `check_prices()` and hashed into `data/manifest.json`.
- **Limitation:** the ticker universe is not point-in-time, so it has survivorship bias. This is a
  known limitation of free data, not a claim of point-in-time accuracy.

## Results
_Not yet produced — strategies land in Week 3-4._

## Limitations
_To be filled in as the project progresses. See the plan's design rules above for what "honest" means here._
