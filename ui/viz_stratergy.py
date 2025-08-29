import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, dash_table

from stratergy.simulate import simulate_strategy


def calc_theoretical_returns(market: pd.DataFrame):
    stock_returns = market.groupby("name").apply(
        lambda df: df["price"].iloc[-1] / df["price"].iloc[0]
    )
    return stock_returns.max(), stock_returns.min()


card_style = {
    "flex": "1",
    "padding": "20px",
    "backgroundColor": "white",
    "borderRadius": "12px",
    "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
    "textAlign": "center",
    "margin": "10px",
}


def stat_card(icon, title, value, color):
    return html.Div(
        [
            html.H4(
                [html.I(className=f"fas {icon}", style={"marginRight": "8px"}), title],
                style={"color": "#6c757d"},
            ),
            html.H2(value, style={"color": color}),
        ],
        style=card_style,
    )

def find_cagr(initial, final, days):
    return_percentage = final/initial
    years = days / 365
    return ((return_percentage ** (1/years)) - 1)*100


def run(market: pd.DataFrame, strategy, days: int):
    print("running markets ......")
    results, portfolio = simulate_strategy(market, strategy, initial_cash=10000)
    best_return, worst_return = calc_theoretical_returns(market)

    initial_cash = results["total_value"].iloc[0]
    final_cash = results["total_value"].iloc[-1]
    return_rate = (final_cash / initial_cash - 1) * 100
    return_cagr = find_cagr(initial_cash, final_cash, days)

    print("creating market chart ....")

    # Market Chart
    fig_market = px.line(
        market, x="day", y="price", color="name", title="Market Prices"
    )

    print('creating portfolio chart ...')

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

    print("created desicitions table")

    layout = html.Div(
        style={
            "fontFamily": "Arial, sans-serif",
            "backgroundColor": "#f8f9fa",
            "padding": "20px",
        },
        children=[
            html.H1(
                [
                    html.I(
                        className="fas fa-chart-bar",
                        style={"marginRight": "10px", "color": "#007bff"},
                    ),
                    f"Strategy Simulation: {strategy.__name__}",
                ],
                style={"textAlign": "center", "marginBottom": "30px"},
            ),
            # Stats row
            html.Div(
                [
                    stat_card(
                        "fa-chart-line", "Final Value", f"${final_cash:,.2f}", "#28a745"
                    ),
                    stat_card(
                        "fa-percent", "Return Rate", f"{return_rate:.2f}%", "#007bff"
                    ),
                    stat_card(
                        "fa-percent", "CAGR", f"{return_cagr:.2f}%", "#007bff"
                    ),
                    stat_card("fa-bullseye", "Strategy", strategy.__name__, "#fd7e14"),
                ],
                style={"display": "flex", "justifyContent": "space-around"},
            ),
            # Graphs
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(figure=fig_market)],
                        style={
                            "backgroundColor": "white",
                            "borderRadius": "12px",
                            "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                            "padding": "20px",
                            "margin": "20px 0",
                        },
                    ),
                    html.Div(
                        [dcc.Graph(figure=fig_portfolio)],
                        style={
                            "backgroundColor": "white",
                            "borderRadius": "12px",
                            "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                            "padding": "20px",
                            "margin": "20px 0",
                        },
                    ),
                ]
            ),
            # Table
            html.Div(
                [
                    html.H2(
                        [
                            html.I(
                                className="fas fa-table",
                                style={"marginRight": "10px", "color": "#17a2b8"},
                            ),
                            "Strategy Decisions",
                        ],
                        style={"marginBottom": "15px"},
                    ),
                    dash_table.DataTable(
                        data=df_history.to_dict("records"),
                        columns=[{"name": i, "id": i} for i in df_history.columns],
                        style_table={
                            "overflowX": "auto",
                            "borderRadius": "10px",
                            "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                            "marginTop": "10px",
                        },
                        style_header={
                            "backgroundColor": "#007bff",
                            "color": "white",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "textAlign": "center",
                            "border": "none",
                        },
                        style_cell={
                            "textAlign": "center",
                            "padding": "12px 8px",
                            "fontSize": "14px",
                            "border": "none",
                        },
                        style_data={
                            "whiteSpace": "normal",
                            "height": "auto",
                        },
                        style_data_conditional=[
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "#f9f9f9",
                            },
                            {
                                "if": {"state": "active"},  # highlight selected cell
                                "backgroundColor": "#e9ecef",
                                "border": "1px solid #007bff",
                            },
                            {
                                "if": {"state": "selected"},  # when row is clicked
                                "backgroundColor": "#d6e9f9",
                                "color": "black",
                            },
                        ],
                        fixed_rows={"headers": True},  # sticky headers
                        style_as_list_view=True,  # removes default borders for modern flat look
                    ),
                ],
                style={
                    "backgroundColor": "white",
                    "borderRadius": "12px",
                    "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                    "padding": "20px",
                    "marginTop": "20px",
                },
            ),
        ],
    )

    print("returning layout....")

    return layout
