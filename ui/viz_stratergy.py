import pandas as pd
from dash import html

from stratergy.simulate import RunResult

from .const import DEFAULT_THEME

from .components import (
    PortfolioWithReturnLimits,
    HistoryActionsTable,
    MarketChart,
    IconCard,
)


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
