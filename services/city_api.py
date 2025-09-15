import json
import random

with open("data/cities_ru.json", "r", encoding="utf-8") as f:
    ALL_CITIES = json.load(f)

CITY_DICT = {c["name_ru"].lower(): c for c in ALL_CITIES}


def find_cities_by_letter(letter: str, limit: int = 20, min_population: int = 200000):
    letter = letter.lower()
    filtered = [
        c["name_ru"]
        for c in ALL_CITIES
        if c["name_ru"].lower().startswith(letter)
        and int(c.get("population", 0)) >= min_population
    ]

    if not filtered:
        return []

    random.shuffle(filtered)
    return filtered[:limit]


def city_exists(name: str, min_population: int = 10000):
    city = CITY_DICT.get(name.lower())
    if city and int(city.get("population", 0)) >= min_population:
        return city
    return None
