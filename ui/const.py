# typed dict for colors 
from typing import TypedDict 

class Colors(TypedDict):
    background: str
    bg_1 : str 
    bg_2 : str 

DARK_THEME: Colors = { 
    "background": "#121212",
    "bg_1": "#1E1E1E",
    "bg_2": "#2C2C2C",
}

LIGHT_THEME: Colors = { 
    "background": "#F8F9FA",
    "bg_1": "#FFFFFF",
    "bg_2": "#E9ECEF",
}
DEFAULT_THEME = LIGHT_THEME

