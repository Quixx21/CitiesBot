from src.services import city_api


def test_find_cities_by_letter_with_population(monkeypatch):
    fake_cities = [
        {"name_ru": "Москва", "population": 12000000, "country": "RU"},
        {"name_ru": "Мценск", "population": 38000, "country": "RU"},
        {"name_ru": "Милан", "population": 1300000, "country": "IT"},
        {"name_ru": "Минск", "population": 2000000, "country": "BY"},
        {"name_ru": "Мурманск", "population": 270000, "country": "RU"},
    ]
    monkeypatch.setattr(city_api, "ALL_CITIES", fake_cities)

    res = city_api.find_cities_by_letter("м", limit=10, min_population=200000)
    assert set(res) >= {"Москва", "Милан", "Минск", "Мурманск"}
    assert "Мценск" not in res


def test_city_exists(monkeypatch):
    assert city_api.city_exists("Москва")
    assert city_api.city_exists("Москва")
    assert not city_api.city_exists("НеГород")
