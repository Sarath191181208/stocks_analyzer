from dataclasses import dataclass

import pandas as pd
import plotly.express as px
from dash import dcc, html

from stratergy import portfolio
from stratergy.simulate import simulate_strategy
from stratergy.stratergy import StrategyEntry

from .const import DEFAULT_THEME

from .components import (
    PortfolioWithReturnLimits,
    HistoryActionsTable,
    MarketChart,
    IconCard,
)


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
    portfolio: portfolio.Portfolio
    results: pd.DataFrame
    stratergy: StrategyEntry
    stats: RunStats


def calc_theoretical_returns(market: pd.DataFrame) -> tuple[float, float]:
    stock_returns = market.groupby("name").apply(
        lambda df: df["price"].iloc[-1] / df["price"].iloc[0]
    )
    return stock_returns.max(), stock_returns.min()


def StatsTitle(strat_name: str) -> html.H1:
    return html.H1(
        [
            html.I(
                className="fas fa-chart-bar",
                style={"marginRight": "10px", "color": "#007bff"},
            ),
            f"Strategy Simulation: {strat_name}",
        ],
        style={"textAlign": "center", "marginBottom": "30px"},
    )


def StatsRow(res: RunResult) -> html.Div:
    return html.Div(
        [
            IconCard(
                "fa-chart-line",
                "Final Value",
                f"${res.stats.final_value:,.2f}",
                "#28a745",
            ),
            IconCard(
                "fa-percent",
                "Return Rate",
                f"{res.stats.return_rate:.2f}%",
                "#007bff",
            ),
            IconCard("fa-percent", "CAGR", f"{res.stats.return_cagr:.2f}%", "#007bff"),
            IconCard("fa-bullseye", "Strategy", res.stratergy.name, "#fd7e14"),
        ],
        style={"display": "flex", "justifyContent": "space-around"},
    )


def find_cagr(initial, final, days):
    return_percentage = final / initial
    years = days / 365
    return ((return_percentage ** (1 / years)) - 1) * 100


def viz_run(res: RunResult, market: pd.DataFrame):

    results = res.results

    print("creating portfolio chart ...")

    # Portfolio Chart with theoretical max/min
    portfolio_card = PortfolioWithReturnLimits(
        results,
        res.stats.initial_cash,
        res.stats.best_return_possible,
        res.stats.worst_return_possible,
    )

    layout = html.Div(
        style={
            "fontFamily": "Arial, sans-serif",
            "backgroundColor": DEFAULT_THEME.background,
            "padding": "20px",
        },
        children=[
            StatsTitle(res.stratergy.name),
            StatsRow(res),
            html.Div(
                [
                    MarketChart(market),
                    portfolio_card,
                ]
            ),
            HistoryActionsTable(res.portfolio),
        ],
    )

    return layout


def run(market: pd.DataFrame, strategy: StrategyEntry, days: int) -> RunResult:
    print("running markets ......")
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
