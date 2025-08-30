import plotly.express as px
from dash import dcc, html
import pandas as pd

def plot_market(market):
    fig_market = px.line(
        market, x="day", y="price", color="name", title="Market Prices"
    )
    return fig_market


def MarketChart(market: pd.DataFrame) -> html.Div:
    fig_market = plot_market(market)
    return html.Div(
        [dcc.Graph(figure=fig_market)],
        style={
            "backgroundColor": "white",
            "borderRadius": "12px",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
            "padding": "20px",
            "margin": "20px 0",
        },
    )
