import pytest
from src.get_data import get_evictions_data
from datetime import datetime




def test_api_fetch():
    results = get_evictions_data()
    assert isinstance(results, list)
    assert len(results)

def test_api_conversion():
    results = get_evictions_data()
    sample = results[0]
    assert len(sample) == 4
    
    assert isinstance(sample[0], int)
    assert isinstance(sample[1], float)
    assert isinstance(sample[2], float)
    assert isinstance(sample[3], str)


