import plotly.express as px
from dash import dcc, html
import pandas as pd

from ui.const import DEFAULT_THEME


def plot_market(market):
    fig_market = px.line(
        market, x="day", y="price", color="name", title="Market Prices"
    )

    # add index line from the data
    market_index = market.groupby("day")["price"].mean().reset_index()
    fig_market.add_scatter(
        x=market_index["day"],
        y=market_index["price"],
        mode="lines",
        name="Market Index",
        line=dict(color="black", dash="dash"),
    )

    return fig_market


def MarketChart(market: pd.DataFrame) -> html.Div:
    fig_market = plot_market(market)
    return html.Div(
        [dcc.Graph(figure=fig_market)],
        style={
            "backgroundColor": DEFAULT_THEME.background_light,
            "borderRadius": "12px",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
            "padding": "20px",
            "margin": "20px 0",
        },
    )
