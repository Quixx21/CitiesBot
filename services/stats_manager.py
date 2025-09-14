import json
import os

STATS_FILE = "../data/stats.json"


def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def update_stats(user_id: int, result: str, cities_count: int):
    stats = load_stats()
    uid = str(user_id)

    if uid not in stats:
        stats[uid] = {"wins": 0, "losses": 0, "max_cities": 0}

    if result == "win":
        stats[uid]["wins"] += 1
    elif result == "loss":
        stats[uid]["losses"] += 1

    if cities_count > stats[uid]["max_cities"]:
        stats[uid]["max_cities"] = cities_count

    save_stats(stats)


def get_user_stats(user_id: int):
    stats = load_stats()
    uid = str(user_id)
    return stats.get(uid, {"wins": 0, "losses": 0, "max_cities": 0})
