import pandas as pd
import pytest
import os
from src.analyze_data import (
    count_evictions_by_tract,
    calculate_eviction_rate,
    generate_tidy_csv,
    MERGED,
    TENTS_EST,
    STRUCTURES_EST,
    VEHICLES_EST,
)


def test_total_evictions_format():
    results = count_evictions_by_tract()
    df = pd.DataFrame(results)
    assert df["geoid"].str.len().unique()[0] == 11
    # made a new column : total eviction
    assert "total_evictions" in df.columns


def test_total_evictions_grouping():
    results = count_evictions_by_tract()
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


@pytest.fixture(scope="module")
def merged_data():
    generate_tidy_csv()
    df = pd.read_csv(MERGED)
    return df


def test_tidy_col_num(merged_data):
    expected_columns = [
        "date",
        "tract",
        "median_rent",
        "eviction_rate",
        "311_calls",
        "tents",
        "structures",
        "vehicles",
        "estimate",
    ]
    actual_columns = merged_data.columns.tolist()

    assert len(actual_columns) == len(expected_columns)

    for col in expected_columns:
        assert col in actual_columns


def test_homelessness_estimate_calculation(merged_data):
    sample = merged_data.iloc[0]
    expected_estimate = (
        sample["tents"] * TENTS_EST
        + sample["structures"] * STRUCTURES_EST
        + sample["vehicles"] * VEHICLES_EST
    )
    assert sample["estimate"] == pytest.approx(expected_estimate)


def test_tidy_csv_exists():
    assert os.path.exists(MERGED)
