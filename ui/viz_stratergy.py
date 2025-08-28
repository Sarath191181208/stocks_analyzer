import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table

from stratergy.simulate import simulate_strategy


def calc_theoretical_returns(market: pd.DataFrame):
    stock_returns = market.groupby("name").apply(
        lambda df: df["price"].iloc[-1] / df["price"].iloc[0]
    )
    return stock_returns.max(), stock_returns.min()


def run(market: pd.DataFrame, strategy):
    results, portfolio = simulate_strategy(market, strategy, initial_cash=10000)
    best_return, worst_return = calc_theoretical_returns(market)

    initial_cash = results["total_value"].iloc[0]
    final_cash = results["total_value"].iloc[-1]
    return_rate = (final_cash / initial_cash - 1) * 100

    # Market Chart
    fig_market = px.line(
        market, x="day", y="price", color="name", title="Market Prices"
    )

    # Portfolio Chart with theoretical max/min
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
    max_curve = initial_cash * best_return
    min_curve = initial_cash * worst_return
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

    # Decisions table
    df_history = pd.DataFrame(
        portfolio.history, columns=["Day", "Action", "Stock", "Qty", "Price", "Cash"]
    )

    # Build Dash app
    app = Dash(__name__)
    app.layout = html.Div(
        [
            html.H1(f"Strategy Simulation: {strategy.__name__}"),
            html.Div(
                [
                    html.Div(
                        [html.H3("📈 Final Value"), html.P(f"${final_cash:,.2f}")],
                        style={
                            "padding": "10px",
                            "border": "1px solid #ccc",
                            "margin": "5px",
                        },
                    ),
                    html.Div(
                        [html.H3("💰 Return Rate"), html.P(f"{return_rate:.2f}%")],
                        style={
                            "padding": "10px",
                            "border": "1px solid #ccc",
                            "margin": "5px",
                        },
                    ),
                    html.Div(
                        [html.H3("🎯 Strategy"), html.P(strategy.__name__)],
                        style={
                            "padding": "10px",
                            "border": "1px solid #ccc",
                            "margin": "5px",
                        },
                    ),
                ],
                style={"display": "flex", "justifyContent": "space-around"},
            ),
            dcc.Graph(figure=fig_market),
            dcc.Graph(figure=fig_portfolio),
            html.H2("Strategy Decisions"),
            dash_table.DataTable(
                data=df_history.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df_history.columns],
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center"},
            ),
        ]
    )

    return app
