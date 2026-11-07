import numpy as np
import pandas as pd
from quantlib.metrics import annualized_volatility, sharpe_ratio, annualized_return, TRADING_DAYS


def test_annualized_volatility_scales_by_sqrt_time():
    r = pd.Series([0.01, -0.01, 0.01, -0.01])
    assert np.isclose(annualized_volatility(r), r.std() * np.sqrt(TRADING_DAYS))


def test_annualized_volatility_doubles_when_daily_vol_doubles():
    r1 = pd.Series([0.01, -0.01] * 50)
    r2 = pd.Series([0.02, -0.02] * 50)
    assert np.isclose(annualized_volatility(r2), 2 * annualized_volatility(r1))


def test_sharpe_ratio_zero_when_return_equals_risk_free():
    r = pd.Series([0.0005] * TRADING_DAYS)
    rf = annualized_return(r)
    assert np.isclose(sharpe_ratio(r, risk_free_rate=rf), 0.0, atol=1e-10)


def test_sharpe_ratio_decreases_with_higher_risk_free_rate():
    r = pd.Series([0.001] * TRADING_DAYS)
    assert sharpe_ratio(r, risk_free_rate=0.05) < sharpe_ratio(r, risk_free_rate=0.0)


def test_sharpe_ratio_on_spy_is_reasonable():
    df = pd.read_csv("data/SPY.csv", index_col=0, parse_dates=True)
    from quantlib.metrics import simple_returns
    r = simple_returns(df["Close"])
    s = sharpe_ratio(r)
    assert 0.5 < s < 1.2
