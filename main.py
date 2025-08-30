from data.generator import generate_market
from ui.viz_single_stratergy_with_dropdown import run

from random import randint

def main():
    NUM_STOCKS = 50
    DAYS = 365 * 10
    seed = randint(0, 1_000_000_000)
    df = generate_market(NUM_STOCKS, DAYS, seed)
    run(df, DAYS)

if __name__ == "__main__":
    main()
