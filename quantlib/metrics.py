"""Return mathematics: simple vs log returns, compounding, annualizing."""
import numpy as np
import pandas as pd

TRADING_DAYS = 252


def simple_returns(prices):
    """Daily simple returns P_t / P_{t-1} - 1."""
    return prices.pct_change().dropna()


def log_returns(prices):
    """Daily log returns ln(P_t / P_{t-1}). These add across time."""
    return np.log(prices / prices.shift(1)).dropna()


def cumulative_return(returns):
    """Total compounded return over the whole period, from simple returns."""
    return (1.0 + returns).prod() - 1.0


def equity_curve(returns, start=1.0):
    """Compounded growth of `start` units of capital, from simple returns."""
    return start * (1.0 + returns).cumprod()


def annualized_return(returns, periods_per_year=TRADING_DAYS):
    """Geometric (CAGR) annualized return from simple returns. The honest number."""
    total = (1.0 + returns).prod()
    years = len(returns) / periods_per_year
    return total ** (1.0 / years) - 1.0


def annualized_volatility(returns, periods_per_year=TRADING_DAYS):
    """Annualized volatility: how much the strategy's returns bounce around, scaled to a year.
    Used as the risk denominator in the Sharpe ratio — the thing that turns a raw return into a
    risk-adjusted one. See Theory 1.1 for the sqrt(time) derivation.
    """
    # TODO: implement
    return returns.std() * (periods_per_year ** 0.5)

def sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=TRADING_DAYS):
    """Risk-adjusted return: how much return you earned per unit of volatility taken on.
    Used to compare two strategies with different risk levels on equal footing — a strategy
    with a higher Sharpe delivered more return for the risk it carried, not necessarily more
    raw return. See Theory 1.2 for the formula.
    """
    # TODO: implement
    return (annualized_return(returns, periods_per_year) - risk_free_rate) / annualized_volatility(returns)