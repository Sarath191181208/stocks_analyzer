
import dash
from dash import dcc, html, dash_table, Input, Output, callback
import pandas as pd

from ui.data_loader import summary_df, details

dash.register_page(__name__, path='/')

pivot_df = summary_df.pivot(index='market_id', columns='strategy_name', values='cagr').reset_index()

columns = [{"name": i, "id": i} for i in pivot_df.columns]

# Summary Statistics
num_markets = len(pivot_df)
num_strategies = len(summary_df['strategy_name'].unique())
best_strategy = summary_df.groupby('strategy_name')['cagr'].mean().idxmax()
worst_strategy = summary_df.groupby('strategy_name')['cagr'].mean().idxmin()

summary_layout = html.Div([
    html.H2('Overall Summary'),
    html.P(f"Total Markets Simulated: {num_markets}"),
    html.P(f"Total Strategies Evaluated: {num_strategies}"),
    html.P(f"Best Performing Strategy (on average): {best_strategy}"),
    html.P(f"Worst Performing Strategy (on average): {worst_strategy}"),
])

layout = html.Div([
    dcc.Location(id='location', refresh=True),
    summary_layout,
    html.H2('Performance Summary'),
    dash_table.DataTable(
        id='summary-table',
        columns=columns,
        data=pivot_df.to_dict('records'),
        cell_selectable=True,
        row_selectable='single',
    ),
])

@callback(
    Output('location', 'href'),
    Input('summary-table', 'active_cell'),
    Input('summary-table', 'selected_rows')
)
def update_location(active_cell, selected_rows):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'summary-table' and active_cell:
        row = active_cell['row']
        col_id = active_cell['column_id']
        market_id = pivot_df.iloc[row]['market_id']
        if col_id != 'market_id':
            encoded_strat_name = col_id.replace(' ', '-')
            return f"/strategy-market/{int(market_id)}/{encoded_strat_name}"

    if trigger_id == 'summary-table' and selected_rows:
        market_id = pivot_df.iloc[selected_rows[0]]['market_id']
        return f"/market/{int(market_id)}"

    return dash.no_update
