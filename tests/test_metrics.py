import numpy as np
import pandas as pd

from quantlib.metrics import (
    simple_returns,
    log_returns,
    cumulative_return,
    equity_curve,
    annualized_return,
    TRADING_DAYS,
)


def prices(values):
    idx = pd.bdate_range("2020-01-01", periods=len(values))
    return pd.Series(values, index=idx, dtype=float)


def test_simple_returns_known_values():
    r = simple_returns(prices([100, 110, 99]))
    assert np.allclose(r.values, [0.10, -0.10])


def test_log_returns_known_values():
    l = log_returns(prices([100, 110, 99]))
    assert np.allclose(l.values, [np.log(1.1), np.log(0.9)])


def test_log_returns_are_additive_across_time():
    p = prices([100, 110, 99])
    # Sum of daily log returns equals the log of the total price relative.
    assert np.isclose(log_returns(p).sum(), np.log(99 / 100))


def test_log_approximates_simple_for_small_moves():
    p = prices([100.0, 100.1])  # a 0.1% move
    assert np.isclose(log_returns(p).iloc[0], simple_returns(p).iloc[0], atol=1e-6)


def test_simple_and_log_convert():
    p = prices([100, 110, 99])
    # simple = exp(log) - 1, elementwise.
    assert np.allclose(simple_returns(p).values, np.expm1(log_returns(p).values))


def test_cumulative_return_compounds():
    r = pd.Series([0.10, -0.10])
    assert np.isclose(cumulative_return(r), -0.01)


def test_equity_curve_endpoint_matches_cumulative():
    r = simple_returns(prices([100, 110, 99]))
    end = equity_curve(r, start=1000.0).iloc[-1]
    assert np.isclose(end, 1000.0 * (1.0 + cumulative_return(r)))


def test_annualized_return_cagr_identity():
    # A constant daily return over exactly one year: CAGR == total return.
    r = pd.Series([0.001] * TRADING_DAYS)
    assert np.isclose(annualized_return(r), 1.001 ** TRADING_DAYS - 1.0)


def test_annualized_return_scales_with_horizon():
    # Same daily return over two years must give the same annualized figure.
    one = pd.Series([0.001] * TRADING_DAYS)
    two = pd.Series([0.001] * (2 * TRADING_DAYS))
    assert np.isclose(annualized_return(one), annualized_return(two))
