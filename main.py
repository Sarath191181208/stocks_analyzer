from data.generator import generate_market
from stratergy.buy_and_hold import buy_and_hold
from ui.viz_stratergy import run 

def main():
    NUM_STOCKS = 50
    DAYS = 365
    df = generate_market(NUM_STOCKS, DAYS)
    app = run(df, buy_and_hold)
    app.run(debug=False)


if __name__ == "__main__":
    main()
