import pandas as pd 
from dash import Dash, dcc, html, Input, Output

from .viz_stratergy import run as run_single, viz_run
from stratergy import registry

def run(market: pd.DataFrame, DAYS: int):
    app = Dash(
        __name__,
        external_stylesheets=[
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        ],
    )

    # Pick the first strategy by default
    print(registry.strategies)
    default_strategy = registry.strategies[1]

    print("Creating layouts ....")
    res = run_single(market, default_strategy, DAYS)
    dashboard_layout = viz_run(res, market)

    print("Creating app layout")

    # ===== Layout =====
    app.layout = html.Div(
        style={
            "minHeight": "100vh",
            "backgroundColor": "#f4f6f9",
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "flex-start",
            "padding": "40px",
            "fontFamily": "Inter, Arial, sans-serif",
        },
        children=[
            html.Div(
                style={
                    "background": "white",
                    "padding": "30px",
                    "borderRadius": "16px",
                    "boxShadow": "0 4px 20px rgba(0,0,0,0.05)",
                    "width": "100%",
                    "maxWidth": "1200px",
                },
                children=[
                    # Header
                    html.Div(
                        [
                            html.I(className="fas fa-chart-line",
                                   style={"color": "#007bff", "marginRight": "10px"}),
                            html.Span("Strategy Dashboard",
                                      style={"fontSize": "24px", "fontWeight": "600"})
                        ],
                        style={"display": "flex", "alignItems": "center", "marginBottom": "25px"},
                    ),

                    # Dropdown
                    dcc.Dropdown(
                        id="strategy-dropdown",
                        options=[
                            {
                                "label": html.Span([
                                    html.I(className="fas fa-bullseye",
                                           style={"marginRight": "8px", "color": "#555"}),
                                    s.name
                                ], style={"display": "flex", "alignItems": "center"}),
                                "value": s.name,
                            }
                            for s in registry.strategies
                        ],
                        value=default_strategy.name,  # default selection
                        clearable=False,
                        style={
                            "width": "350px",
                            "marginBottom": "25px",
                            "borderRadius": "8px",
                            "fontSize": "16px",
                        },
                    ),

                    # Graph area with loading spinner
                    dcc.Loading(
                        id="loading",
                        type="circle",
                        color="#007bff",
                        children=html.Div(
                            id="strategy-container",
                            style={"marginTop": "20px"},
                            children=dashboard_layout,  # show default immediately
                        )
                    ),
                ],
            )
        ],
    )

    # ===== Callback =====
    @app.callback(
        Output("strategy-container", "children"),
        Input("strategy-dropdown", "value"),
    )
    def update_strategy(selected_name):
        strat = next(s for s in registry.strategies if s.name == selected_name)
        res = run_single(market, strat, DAYS)
        layout = viz_run(res, market)
        return layout

    print("running the app")

    app.run(debug=True)

