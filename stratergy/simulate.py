from typing import Tuple
from dataclasses import dataclass

import numpy as np
import pandas as pd

from .stratergy import StrategyEntry
from .market import Market
from .portfolio import Portfolio


@dataclass(frozen=True)
class RunStats:
    initial_cash: float
    final_value: float
    return_rate: float
    return_cagr: float
    best_return_possible: float
    worst_return_possible: float


@dataclass(frozen=True)
class RunResult:
    portfolio: Portfolio
    results: pd.DataFrame
    stratergy: StrategyEntry
    stats: RunStats


def calc_theoretical_returns(market: pd.DataFrame) -> tuple[float, float]:
    first = market.groupby("name")["price"].first()
    last = market.groupby("name")["price"].last()
    stock_returns = last / first
    return stock_returns.max(), stock_returns.min()

def find_cagr(initial, final, days):
    return_percentage = final / initial
    years = days / 365
    return ((return_percentage ** (1 / years)) - 1) * 100

def run(market: pd.DataFrame, strategy: StrategyEntry, days: int) -> RunResult:
    results, portfolio = simulate_strategy(
        market, strategy.function, initial_cash=10000
    )
    best_return, worst_return = calc_theoretical_returns(market)

    initial_cash = results["total_value"].iloc[0]
    final_cash = results["total_value"].iloc[-1]
    return_rate = (final_cash / initial_cash - 1) * 100
    return_cagr = find_cagr(initial_cash, final_cash, days)

    return RunResult(
        portfolio=portfolio,
        results=results,
        stratergy=strategy,
        stats=RunStats(
            initial_cash=initial_cash,
            final_value=final_cash,
            return_rate=return_rate,
            return_cagr=return_cagr,
            best_return_possible=best_return,
            worst_return_possible=worst_return,
        ),
    )


def simulate_strategy(
    market: pd.DataFrame, strategy, initial_cash: float = 10000.0
) -> Tuple[pd.DataFrame, Portfolio]:
    """
    market: DataFrame with columns [name, day, price]
    strategy: function(portfolio: Portfolio, day: int, prices: dict) -> None
    """
    m = Market(market)
    return _simulate(m, strategy, initial_cash)


def _simulate(
    market: Market, strategy, initial_cash: float = 10_000.0
) -> Tuple[pd.DataFrame, Portfolio]:
    portfolio = Portfolio(cash=initial_cash)
    n_days = len(market.days)

    # Preallocate arrays for results
    days_arr = np.empty(n_days, dtype=np.int64)
    cash_arr = np.empty(n_days, dtype=np.float64)
    holdings_arr = np.empty(n_days, dtype=np.float64)
    total_arr = np.empty(n_days, dtype=np.float64)

    for i, day in enumerate(market.days):
        prices_today = market.get_prices_on_day(day)

        # Strategy decides what to do
        strategy(portfolio, day, prices_today, market)

        # Precompute holdings value with numpy dot product
        if portfolio.holdings:
            stocks = np.fromiter(portfolio.holdings.keys(), dtype=object)
            qtys = np.fromiter(portfolio.holdings.values(), dtype=np.float64)

            prices = np.array(
                [prices_today.get(s, 0.0) for s in stocks], dtype=np.float64
            )
            holdings_value = np.dot(qtys, prices)
        else:
            holdings_value = 0.0

        # Store results (avoids building dicts each iteration)
        days_arr[i] = day
        cash_arr[i] = portfolio.cash
        holdings_arr[i] = holdings_value
        total_arr[i] = portfolio.portfolio_value(prices_today)

    # Build DataFrame once at the end
    df = pd.DataFrame(
        {
            "day": days_arr,
            "cash": cash_arr,
            "holdings_value": holdings_arr,
            "total_value": total_arr,
        }
    )

    return df, portfolio
