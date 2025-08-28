import plotly.express as px

from data.generator import generate_market

def run():
    df = generate_market(50, 365)
    fig = px.line(
        df,
        x="day",
        y="price",
        color="name",
        title="Simulated Stock Prices",
        labels={"day": "Day", "price": "Stock Price", "name": "Company"}
    )

    fig.update_layout(
        template="plotly_white",
        legend_title="Company",
        hovermode="x unified"
    )

    fig.show()
