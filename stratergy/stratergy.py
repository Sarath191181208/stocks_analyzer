from dataclasses import dataclass
from types import FunctionType 


@dataclass(frozen=True) 
class StrategyEntry:
    name: str
    description: str
    function: FunctionType

class StrateryRegistry:
    def __init__(self):
        self.strategies: list[StrategyEntry] = list()
    def add(self, entry: StrategyEntry):
        self.strategies.append(entry)

registry = StrateryRegistry()

def strategy(name: str, description: str):
    def decorator(func):
        entry = StrategyEntry(name, description, func) 
        registry.add(entry)
        return func
    return decorator
