import numpy as np
import pandas as pd

def generate_single_stock(
    duration: int,
    initial_value: float,
    delta: float,
    base_volatility: float = 0.02,
    jump_prob: float = 0.02,
    jump_size_mean: float = 0.05,
    jump_size_std: float = 0.1,
    seed: int | None = None
) -> pd.Series:
    """
    Generate realistic synthetic stock prices with drift, stochastic volatility, and jumps.

    Parameters
    ----------
    duration : int
        Number of days to simulate.
    initial_value : float
        Starting stock price.
    delta : float
        Expected daily drift (average return) usually quite small (0.00005 = 0.005% per day / 1.8% per year).
    base_volatility : float
        Baseline volatility of daily returns.
    jump_prob : float
        Probability of a jump occurring on a given day.
    jump_size_mean : float
        Mean jump size (as fraction of price).
    jump_size_std : float
        Std deviation of jump size.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    prices : pd.Series
        Simulated stock prices indexed by day.
    """
    if seed is not None:
        np.random.seed(seed)

    prices = np.zeros(duration)
    prices[0] = initial_value
    volatility = base_volatility

    for t in range(1, duration):
        # volatility clustering (ARCH-like)
        shock = np.random.normal(0, 1)
        volatility = 0.9 * volatility + 0.1 * abs(shock) * base_volatility

        # normal GBM increment
        daily_return = delta + volatility * shock

        # jump diffusion
        if np.random.rand() < jump_prob:
            jump = np.random.normal(jump_size_mean, jump_size_std)
            daily_return += jump

        prices[t] = prices[t - 1] * np.exp(daily_return)

    return pd.Series(prices, index=pd.RangeIndex(1, duration + 1), name="Price")
