import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

from ui.const import DEFAULT_THEME


def PortfolioWithReturnLimits(
    results: pd.DataFrame,
    initial_cash: float,
    best_return_possible: float,
    worst_return_possible: float,
) -> html.Div:
    gph = plot_portfolio_with_best_and_worst_possible_return(
        results,
        initial_cash,
        best_return_possible,
        worst_return_possible,
    )

    return html.Div(
        [dcc.Graph(figure=gph)],
        style={
            "backgroundColor": DEFAULT_THEME.background_light,
            "borderRadius": "12px",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
            "padding": "20px",
            "margin": "20px 0",
        },
    )


def plot_portfolio_with_best_and_worst_possible_return(
    results: pd.DataFrame,
    initial_cash: float,
    best_return_possible: float,
    worst_return_possible: float,
):
    fig_portfolio = go.Figure()
    fig_portfolio.add_trace(
        go.Scatter(
            x=results["day"],
            y=results["total_value"],
            mode="lines+markers",
            name="Portfolio Value",
            line=dict(color="blue", width=2),
        )
    )

    # Theoretical benchmarks
    max_curve = initial_cash * best_return_possible
    min_curve = initial_cash * worst_return_possible
    fig_portfolio.add_hline(
        y=max_curve,
        line_dash="dash",
        line_color="green",
        annotation_text="Theoretical Max",
    )
    fig_portfolio.add_hline(
        y=min_curve,
        line_dash="dash",
        line_color="red",
        annotation_text="Theoretical Min",
    )

    fig_portfolio.update_layout(title="Portfolio Value vs Theoretical Bounds")
    return fig_portfolio
