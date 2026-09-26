from app import seed
from app.modules import pattern_match
from app.repositories import history, settings_repo
from app.services import estimate_service


def test_resolve_request_wins_over_default():
    assert pattern_match.resolve_match_pattern(False, {"default_match_pattern": "1"}) is False
    assert pattern_match.resolve_match_pattern(True, {"default_match_pattern": "0"}) is True


def test_resolve_falls_back_to_settings_then_default():
    assert pattern_match.resolve_match_pattern(None, {"default_match_pattern": "0"}) is False
    assert pattern_match.resolve_match_pattern(None, {"default_match_pattern": "1"}) is True
    assert pattern_match.resolve_match_pattern(None, {}) is True
    assert pattern_match.resolve_match_pattern(None, None) is True


def test_effective_pattern_m():
    assert pattern_match.effective_pattern_m(64, False) == 0.0
    assert pattern_match.effective_pattern_m(64, True) == 0.64


def _fresh_db(monkeypatch, tmp_path):
    monkeypatch.setattr("app.db.DB_PATH", tmp_path / "t.db")
    seed.init_db()


def test_saved_run_pins_toggle_and_drop_len(monkeypatch, tmp_path):
    _fresh_db(monkeypatch, tmp_path)
    on = estimate_service.run_estimate(2, 2, True, "", True)
    assert on["match_pattern"] is True
    assert on["drop_len_m"] == 3.44
    off = estimate_service.run_estimate(2, 2, True, "", False)
    assert off["match_pattern"] is False
    assert off["drop_len_m"] == 2.8
    runs = {r["id"]: r for r in history.list_runs()}
    assert runs[on["run_id"]]["result"]["match_pattern"] is True
    assert runs[on["run_id"]]["result"]["drop_len_m"] == 3.44
    assert runs[on["run_id"]]["result"]["rolls"] == 19
    assert runs[off["run_id"]]["result"]["match_pattern"] is False
    assert runs[off["run_id"]]["result"]["drop_len_m"] == 2.8
    assert runs[off["run_id"]]["result"]["rolls"] == 13


def test_default_change_does_not_touch_old_runs(monkeypatch, tmp_path):
    _fresh_db(monkeypatch, tmp_path)
    before = estimate_service.run_estimate(2, 2, True, "", None)
    assert before["match_pattern"] is True
    settings_repo.set_value("default_match_pattern", "0")
    after = estimate_service.run_estimate(2, 2, True, "", None)
    assert after["match_pattern"] is False
    runs = {r["id"]: r for r in history.list_runs()}
    old = runs[before["run_id"]]["result"]
    assert old["match_pattern"] is True
    assert old["drop_len_m"] == 3.44
    assert old["rolls"] == 19


def test_off_run_stays_off_when_default_flips_on(monkeypatch, tmp_path):
    _fresh_db(monkeypatch, tmp_path)
    settings_repo.set_value("default_match_pattern", "0")
    off = estimate_service.run_estimate(2, 2, True, "", None)
    assert off["match_pattern"] is False
    assert off["drop_len_m"] == 2.8
    settings_repo.set_value("default_match_pattern", "1")
    runs = {r["id"]: r for r in history.list_runs()}
    old = runs[off["run_id"]]["result"]
    assert old["match_pattern"] is False
    assert old["drop_len_m"] == 2.8
    assert old["rolls"] == 13
