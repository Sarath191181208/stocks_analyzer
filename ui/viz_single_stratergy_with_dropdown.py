import pandas as pd
from dash import Dash, dcc, html, Input, Output

from .const import DEFAULT_THEME
from .viz_stratergy import run as run_single, viz_run
import plotly.io as pio

from stratergy import registry


def run(market: pd.DataFrame, DAYS: int):
    app = Dash(
        __name__,
        external_stylesheets=[
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        ],
    )

    pio.templates.default = DEFAULT_THEME.plotly_template
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
            "backgroundColor": DEFAULT_THEME.background,
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "flex-start",
            "padding": "40px",
            "color": DEFAULT_THEME.color,
            "fontFamily": "Inter, Arial, sans-serif",
        },
        children=[
            html.Div(
                style={
                    "background": DEFAULT_THEME.background_light,
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
                            html.I(
                                className="fas fa-chart-line",
                                style={"color": "#007bff", "marginRight": "10px"},
                            ),
                            html.Span(
                                "Strategy Dashboard",
                                style={"fontSize": "24px", "fontWeight": "600"},
                            ),
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "marginBottom": "25px",
                        },
                    ),
                    # Dropdown
                    dcc.Dropdown(
                        id="strategy-dropdown",
                        options=[
                            {
                                "label": html.Span(
                                    [
                                        html.I(
                                            className="fas fa-bullseye",
                                            style={"marginRight": "8px"},
                                        ),
                                        s.name,
                                    ],
                                    style={
                                        "display": "inline-flex",
                                        "alignItems": "center",
                                        "gap": "8px",
                                        "padding": "6px 8px",  # small pill look for label text
                                        "borderRadius": "6px",
                                        "color": DEFAULT_THEME.color_light,
                                        # Avoid relying on label background for the whole menu; use CSS for menu bg.
                                    },
                                ),
                                "value": s.name,
                                # when label is a component, set 'search' so the search box can match text
                                "search": s.name,
                            }
                            for s in registry.strategies
                        ],
                        value=default_strategy.name,
                        clearable=False,
                        searchable=True,
                        style={
                            "width": "350px",
                            "marginBottom": "25px",
                            "borderRadius": "8px",
                            "fontSize": "16px",
                            "backgroundColor": DEFAULT_THEME.background_light,
                            "color": DEFAULT_THEME.color,
                            "padding": "6px 10px",
                        },
                        # dropdown sizing helpers provided by Dash:
                        optionHeight=44,  # px per option (default 35)
                        maxHeight=300,  # max height of expanded menu
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
                        ),
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
