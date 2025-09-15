import json
from src.services import stats_manager


def test_stats_update_and_read(tmp_path, monkeypatch):
    tmp_stats = tmp_path / "stats.json"
    monkeypatch.setattr(stats_manager, "STATS_FILE", tmp_stats)

    uid = 777
    s0 = stats_manager.get_user_stats(uid)
    assert s0 == {"wins": 0, "losses": 0, "max_cities": 0}

    stats_manager.update_stats(uid, "win", 3)
    stats_manager.update_stats(uid, "loss", 5)
    stats_manager.update_stats(uid, "win", 4)  # max_cities должно стать 5

    s1 = stats_manager.get_user_stats(uid)
    assert s1["wins"] == 2
    assert s1["losses"] == 1
    assert s1["max_cities"] == 5

    data = json.loads(tmp_stats.read_text(encoding="utf-8"))
    assert str(uid) in data
