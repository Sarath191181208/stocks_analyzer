from data.stock import generate_single_stock
import plotly.express as px 

def run():
    df = generate_single_stock(365, 100, 0.0002)
    px.line(df, title="Synthetic Stock Price Over One Year").show()

