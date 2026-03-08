import pandas as pd
import pytest
from src.analyze_data import total_evictions_by_tract, calculate_eviction_rate


def test_total_evictions_format():
    results = total_evictions_by_tract()
    df = pd.DataFrame(results)
    assert df["geoid"].str.len().unique()[0] == 11
    # made a new column : total eviction
    assert "total_evictions" in df.columns


def test_total_evictions_grouping():
    results = total_evictions_by_tract()
    # Nan
    assert not results["total_evictions"].isnull().any()
    # total num of eviction
    assert (results["total_evictions"] >= 0).all()
    # if it is dupicated
    assert not results.duplicated(subset=["geoid", "year_mon"]).any()


def test_calculate_eviction_rate_merge():
    results = calculate_eviction_rate()
    df = pd.DataFrame(results)
    assert (df["geoid"].str.len() == 11).all()
    assert not df["geoid"].isnull().any()
    assert "rent_units" in df.columns


def test_calculate_eviction_rate_math():
    results = calculate_eviction_rate()
    sample = results[0]
    assert "eviction_rate" in sample
    if sample["rent_units"] > 0:
        expected_rate = sample["total_evictions"] / sample["rent_units"]
        assert sample["eviction_rate"] == pytest.approx(expected_rate)
    else:
        assert (
            pd.isna(sample["eviction_rate"])
            or sample["eviction_rate"] == 0
            or sample["eviction_rate"] == float("inf")
        )
