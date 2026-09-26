"""对花开关解析（匹配模块）。

设置默认 ``default_match_pattern`` 与当次测算入参 ``match_pattern`` 是两个
独立字段：当次入参为 None 时才回落到设置默认，设置缺失再回落到开。
关闭时生效花高为 0，drop_len 等于层高，与花高为 0 的无花口径一致。
"""

DEFAULT_MATCH_PATTERN = True
SETTING_KEY = "default_match_pattern"

_TRUTHY = {"1", "true", "yes", "on"}


def resolve_match_pattern(match_pattern, settings: dict | None = None) -> bool:
    """当次入参优先；为 None 时读设置默认；都没有则为开。"""
    if match_pattern is not None:
        return bool(match_pattern)
    raw = (settings or {}).get(SETTING_KEY)
    if raw is None:
        return DEFAULT_MATCH_PATTERN
    return str(raw).strip().lower() in _TRUTHY


def effective_pattern_m(pattern_cm: float, match_pattern: bool) -> float:
    """关闭时忽略卷材花高返回 0；开启时返回 pattern_cm/100（米）。"""
    if not match_pattern:
        return 0.0
    return max(0.0, float(pattern_cm) / 100.0)
