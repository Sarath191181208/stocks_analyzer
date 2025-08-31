import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

from ui.data_loader import details
from ui.components.plot_market import MarketChart

dash.register_page(__name__, path_template='/market/<market_id>')

def layout(market_id=None):
    if market_id is None:
        return html.Div(["Select a market from the main page."])

    market_id = int(market_id)
    
    # Get all results for the selected market
    market_results = {key: value for key, value in details.items() if key[0] == market_id}

    if not market_results:
        return html.Div([f"No data found for market {market_id}"])

    # Create a combined plot of all strategy performances
    all_perf = []
    for (mid, strat_name), result_data in market_results.items():
        perf = result_data['result'].results[['day', 'total_value']].copy()
        perf['strategy'] = strat_name
        all_perf.append(perf)
    
    all_perf_df = pd.concat(all_perf)

    fig = px.line(all_perf_df, x='day', y='total_value', color='strategy', title=f'Strategy Performance on Market {market_id}')

    # Get the market_df from the first result
    first_result = next(iter(market_results.values()))
    market_df = first_result['market_df']
    
    return html.Div([
        dcc.Location(id='location-market-view', refresh=True),
        html.H2(f'Market {market_id} Analysis'),
        dcc.Graph(figure=fig),
        html.H2('Market: '),
        MarketChart(market_df),
        dcc.Link("Back to Summary", href="/")
    ])
