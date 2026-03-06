from datetime import datetime
from src.get_data import get_evictions_data


def test_api_fetch():
    results = get_evictions_data()
    assert isinstance(results, list)
    assert len(results)


def test_api_conversion():
    results = get_evictions_data()
    sample = results[0]
    assert len(sample) == 4

    assert isinstance(sample["id"], int)
    assert isinstance(sample["lat"], float)
    assert isinstance(sample["lon"], float)
    assert isinstance(sample["year_mon"], str)


def test_api_year_in_range():
    results = get_evictions_data()
    for date in results:
        year = int(date["year_mon"][:4])
        assert 2020 <= year <= 2024



