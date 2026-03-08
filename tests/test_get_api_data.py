import pytest
from datetime import datetime
from src.get_api_data import get_evictions_data


@pytest.fixture(scope="module")
def eviction_results():
    return get_evictions_data()


def test_api_fetch(eviction_results):
    assert isinstance(eviction_results, list)
    assert len(eviction_results) > 0


def test_api_conversion(eviction_results):
    sample = eviction_results[0]
    assert len(sample) == 4

    assert isinstance(sample["id"], int)
    assert isinstance(sample["lat"], float)
    assert isinstance(sample["lon"], float)
    assert isinstance(sample["year_mon"], str)
    assert len(sample["year_mon"]) == 7


def test_api_year_in_range(eviction_results):
    for date in eviction_results:
        year = int(date["year_mon"][:4])
        assert 2020 <= year <= 2024


def test_api_coordinates_valid(eviction_results):
    for record in eviction_results:
        # lat and lon of SF
        assert 37.0 <= record["lat"] <= 38.5
        assert -123.0 <= record["lon"] <= -122.0
