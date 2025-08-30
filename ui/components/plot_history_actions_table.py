from dash import html, dash_table

from stratergy.portfolio import Portfolio


def HistoryActionsTable(portfolio: Portfolio):
    df_history = portfolio.history_df()
    return html.Div(
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
    )
