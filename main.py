from random import randint
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

from tqdm import tqdm
import pandas as pd

from data.generator import generate_market
from ui.viz_single_stratergy_with_dropdown import run
from stratergy.simulate import run as run_stratergy
from stratergy import registry


def main():
    NUM_STOCKS = 50
    DAYS = 365 * 10
    NUM_MARKETS = 100

    # generate markets
    partial_generate_market = partial(generate_market, NUM_STOCKS, DAYS)
    seeds = seeds = [randint(0, 1_000_000_000) for _ in range(NUM_MARKETS)]
    with ProcessPoolExecutor() as executor:
        markets = list(executor.map(partial_generate_market, seeds))

    # run markets
    res = run_markets(markets, DAYS)
    print(res)


def run_single_task(market_idx, market, strat, DAYS):
    res = run_stratergy(market, strat, DAYS)
    return {
        "market": f"Market {market_idx+1}",
        "strategy": strat.name,
        "cagr": res.stats.return_cagr,
    }


def run_markets(markets, DAYS, max_workers=None):
    tasks = []
    for i, market in enumerate(markets):
        for strat in registry.strategies:
            tasks.append((i, market, strat, DAYS))

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_single_task, *task) for task in tasks]
        for f in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Running strategies on markets",
        ):
            results.append(f.result())

    results_df = pd.DataFrame(results)
    summary_df = (
        results_df.groupby("strategy")
        .agg(mean_cagr=("cagr", "mean"), std_cagr=("cagr", "std"))
        .reset_index()
    )
    return summary_df


if __name__ == "__main__":
    main()
