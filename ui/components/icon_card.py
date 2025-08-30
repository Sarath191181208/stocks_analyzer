from dash import html

card_style = {
    "flex": "1",
    "padding": "20px",
    "backgroundColor": "white",
    "borderRadius": "12px",
    "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
    "textAlign": "center",
    "margin": "10px",
}


def IconCard(icon: str, title: str, value: str, color: str) -> html.Div:
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
