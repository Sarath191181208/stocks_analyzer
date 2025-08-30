from dataclasses import dataclass


@dataclass(frozen=True)
class Colors:
    plotly_template: str
    background: str
    background_light: str
    background_dark: str
    color: str
    color_light: str


DARK_THEME: Colors = Colors(
    background="#121212",
    background_light="#1E1E1E",
    background_dark="#2C2C2C",
    color="white",
    color_light="#555",
    plotly_template="plotly_dark"
)

LIGHT_THEME: Colors = Colors(
    background="#f4f6f9",
    background_light="#FFFFFF",
    background_dark="#E9ECEF",
    color="black",
    color_light="#555",
    plotly_template="plotly_white"
)
DEFAULT_THEME = LIGHT_THEME
