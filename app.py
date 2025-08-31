
import dash
from dash import Dash, html

app = Dash(__name__, use_pages=True, pages_folder="ui/pages")

app.layout = html.Div([
    html.H1('Multi-Market Strategy Analysis'),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True, port=8051)
