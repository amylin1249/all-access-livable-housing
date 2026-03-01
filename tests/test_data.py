import pytest
from src.get_data import get_evictions_data
from datetime import datetime




def test_api_fetch():
    results = get_evictions_data()
    assert isinstance(results, list)
    assert len(results)







