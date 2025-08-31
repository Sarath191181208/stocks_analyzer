
import pickle
from ui.types import Result

with open("results.pkl", "rb") as f:
    data: Result = pickle.load(f)

summary_df = data["summary"]
details = data["details"]
