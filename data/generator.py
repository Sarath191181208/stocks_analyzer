from faker import Faker
import pandas as pd
import numpy as np
from .stock import generate_single_stock

fake = Faker()

def generate_market(
    n_stocks: int,
    duration: int,
    seed: int | None = None
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    all_data = []

    for i in range(n_stocks):
        stock_name = fake.company()
        stock_seed = None if seed is None else seed + i
        
        # Randomized but realistic parameters
        initial_value = rng.uniform(20, 500)      # stock starting price
        annual_return = rng.uniform(-0.12, 0.28)
        base_volatility = rng.uniform(0.01, 0.05) # daily volatility
        jump_prob = rng.uniform(0.01, 0.05)       # chance of sudden jump
        jump_size_mean = rng.uniform(0.02, 0.08)  # avg jump size
        jump_size_std = rng.uniform(0.05, 0.15)   # jump variability

        prices = generate_single_stock(
            duration=duration,
            initial_value=initial_value,
            annual_return=annual_return,
            base_volatility=base_volatility,
            jump_prob=jump_prob,
            jump_size_mean=jump_size_mean,
            jump_size_std=jump_size_std,
            seed=stock_seed
        )
        
        df = pd.DataFrame({
            "name": stock_name,
            "day": range(duration),
            "price": prices,
            "seed": stock_seed
        })
        all_data.append(df)

    df = pd.concat(all_data, ignore_index=True)
    df.random_seed = seed  # Attach seed as attribute for reference 
    return df

if __name__ == "__main__":
    df = generate_market(n_stocks=5, duration=30, seed=123)
    print(df.head(15))
