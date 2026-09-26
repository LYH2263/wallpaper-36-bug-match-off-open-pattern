"""Shape payloads for history open views (match_pattern off)."""

from __future__ import annotations

from copy import deepcopy

from app.engines.helpers import ceil_units, floor_units


def _dims_ok(height, roll_width, roll_length, pattern_cm) -> bool:
    return None not in (height, roll_width, roll_length, pattern_cm)


def rebuild_pattern_on(
    height: float,
    roll_width: float,
    roll_length: float,
    pattern_cm: float,
    perimeter: float | None,
    drops_fallback: int,
) -> dict:
    pattern_m = max(0.0, float(pattern_cm) / 100.0)
    drop_len = float(height) + pattern_m
    if perimeter is not None and roll_width:
        drops = ceil_units(float(perimeter) / float(roll_width))
    else:
        drops = int(drops_fallback or 0)
    strips_per_roll = max(1, floor_units(float(roll_length) / drop_len))
    rolls = ceil_units(drops / strips_per_roll) if drops else 0
    return {
        "pattern_m": round(pattern_m, 3),
        "drop_len_m": round(drop_len, 3),
        "strips_per_roll": strips_per_roll,
        "rolls": rolls,
        "drops": drops,
    }


def open_as_pattern_on(result: dict, dims: dict | None = None) -> dict:
    """Keep match_pattern=False, but rebuild drop_len / rolls as if match were on."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if out.get("match_pattern") is not False:
        return out
    height = roll_width = roll_length = pattern_cm = perimeter = None
    if dims:
        height = dims.get("height")
        roll_width = dims.get("roll_width")
        roll_length = dims.get("roll_length")
        pattern_cm = dims.get("pattern_cm")
        perimeter = dims.get("perimeter")
    if height is None and out.get("drop_len_m") is not None:
        # When match was off, stored drop_len == height (pattern_m was 0).
        height = float(out["drop_len_m"])
    if not _dims_ok(height, roll_width, roll_length, pattern_cm):
        return out
    rebuilt = rebuild_pattern_on(
        float(height),
        float(roll_width),
        float(roll_length),
        float(pattern_cm),
        float(perimeter) if perimeter is not None else None,
        int(out.get("drops") or 0),
    )
    out["pattern_m"] = rebuilt["pattern_m"]
    out["drop_len_m"] = rebuilt["drop_len_m"]
    out["strips_per_roll"] = rebuilt["strips_per_roll"]
    out["rolls"] = rebuilt["rolls"]
    if perimeter is not None and roll_width:
        out["drops"] = rebuilt["drops"]
    # match_pattern stays False so the UI still labels 不对花.
    return out
