
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

from ui.data_loader import details

dash.register_page(__name__, path_template='/stock/<market_id>/<stock_name>')

def layout(market_id=None, stock_name=None):
    if market_id is None or stock_name is None:
        return html.Div(["Select a market and stock from the market view page."])

    market_id = int(market_id)
    
    # Get the market_df from the first result for the given market_id
    market_results = {key: value for key, value in details.items() if key[0] == market_id}
    if not market_results:
        return html.Div([f"No data found for market {market_id}"])

    first_result = next(iter(market_results.values()))
    market_df = first_result['market_df']

    stock_df = market_df[market_df['name'] == stock_name].copy()

    if stock_df.empty:
        return html.Div([f"No data found for stock {stock_name} in market {market_id}"])

    # Add moving average
    stock_df['moving_average'] = stock_df['price'].rolling(window=20).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_df['day'], y=stock_df['price'], mode='lines', name='Price'))
    fig.add_trace(go.Scatter(x=stock_df['day'], y=stock_df['moving_average'], mode='lines', name='20-Day MA'))

    fig.update_layout(title=f'Price of {stock_name} in Market {market_id}')

    return html.Div([
        html.H2(f'Stock: {stock_name} in Market: {market_id}'),
        dcc.Graph(figure=fig),
        dcc.Link("Back to Market View", href=f"/market/{market_id}")
    ])
