
import dash
from dash import dcc, html
from ui.data_loader import details
from ui.viz_stratergy import viz_run

dash.register_page(__name__, path_template='/strategy-market/<market_id>/<strategy_name>')

def layout(market_id=None, strategy_name=None):
    if market_id is None or strategy_name is None:
        return html.Div(["Select a market and strategy from the main page."])

    market_id = int(market_id)
    decoded_strategy_name = strategy_name.replace('-', ' ')
    stored_data = details.get((market_id, decoded_strategy_name))

    if stored_data is None:
        return html.Div([f"No data found for market {market_id} and strategy {decoded_strategy_name}"])
    
    result = stored_data['result']
    market_df = stored_data['market_df']

    layout = viz_run(result, market_df)

    return html.Div([
        html.H2(f'Strategy: {decoded_strategy_name} on Market: {market_id}'),
        layout,
        dcc.Link("Back to Summary", href="/")
    ])
