
from typing import TypedDict, Dict, Tuple
import pandas as pd
from stratergy.simulate import RunResult

class Details(TypedDict):
    result: RunResult
    market_df: pd.DataFrame

class Result(TypedDict):
    summary: pd.DataFrame
    details: Dict[Tuple[int, str], Details]
