from app.engines.wallpaper_math import roll_count


def test_plain_master_bed():
    r = roll_count(16.0, 2.7, 0.53, 10.0, 0)
    assert r["drops"] == 31
    assert r["drop_len_m"] == 2.7
    assert r["strips_per_roll"] == 3
    assert r["rolls"] == 11


def test_pattern_wall():
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64)
    assert r["drops"] == 38
    assert r["drop_len_m"] == 3.44
    assert r["strips_per_roll"] == 2
    assert r["rolls"] == 19


def test_match_default_on():
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64)
    assert r["match_pattern"] is True
    assert r["pattern_m"] == 0.64


def test_match_off_equals_zero_pattern():
    off = roll_count(20.0, 2.8, 0.53, 10.0, 64, match_pattern=False)
    plain = roll_count(20.0, 2.8, 0.53, 10.0, 0)
    assert off["match_pattern"] is False
    assert off["drop_len_m"] == 2.8
    for k in ("drops", "drop_len_m", "pattern_m", "strips_per_roll", "rolls"):
        assert off[k] == plain[k]
