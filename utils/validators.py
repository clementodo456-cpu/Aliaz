import re

HEX_COLOR_REGEX = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")

COLOR_MAP = {
    "white": "#FFFFFF",
    "black": "#000000",
    "light_gray": "#D3D3D3",
    "dark_gray": "#333333",
    "red": "#FF0000",
    "blue": "#0000FF",
    "green": "#008000",
}

def validate_hex_color(color_str: str) -> str | None:
    """Validates and returns a normalized HEX color string or None."""
    if not color_str:
        return None
    color_str = color_str.strip()
    if color_str.lower() in COLOR_MAP:
        return COLOR_MAP[color_str.lower()]
    if not color_str.startswith("#"):
        color_str = f"#{color_str}"
    if HEX_COLOR_REGEX.match(color_str):
        return color_str.upper()
    return None

def parse_spacing(spacing_str: str) -> int:
    """Maps spacing text choices to pixel values."""
    mapping = {
        "none": 0,
        "small": 10,
        "medium": 20,
        "large": 35
    }
    return mapping.get(spacing_str.lower(), 15)
