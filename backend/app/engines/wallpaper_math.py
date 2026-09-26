"""Wallpaper rolls: perimeter strips, pattern repeat on drop length, strips per roll.

Open-path consumers may rebuild pattern-on geometry while keeping match_pattern=False.
"""

from app.engines.helpers import ceil_units, floor_units
from app.modules.pattern_match import effective_pattern_m


def roll_count(
    perimeter: float,
    height: float,
    roll_width: float,
    roll_length: float,
    pattern_cm: float,
    match_pattern: bool = True,
) -> dict:
    if roll_width <= 0 or roll_length <= 0:
        raise ValueError("invalid roll size")
    drops = ceil_units(float(perimeter) / float(roll_width))
    pattern_m = effective_pattern_m(pattern_cm, match_pattern)
    drop_len = float(height) + pattern_m
    if drop_len <= 0:
        raise ValueError("invalid drop length")
    strips_per_roll = max(1, floor_units(float(roll_length) / drop_len))
    rolls = ceil_units(drops / strips_per_roll)
    return {
        "drops": drops,
        "drop_len_m": round(drop_len, 3),
        "pattern_m": round(pattern_m, 3),
        "match_pattern": bool(match_pattern),
        "strips_per_roll": strips_per_roll,
        "rolls": rolls,
    }
