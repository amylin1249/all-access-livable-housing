import os
import pandas as pd
import pytest
from src.analyze_data import (
    generate_rent_by_zip_dict,
    generate_crosswalks_dict,
    weight_to_census_tract,
    generate_acs_df,
    count_evictions_by_tract,
    calculate_eviction_rate,
    generate_tidy_csv,
    MERGED,
    TENTS_EST,
    STRUCTURES_EST,
    VEHICLES_EST,
)


def test_generate_rent_by_zip_dict():
    rents = generate_rent_by_zip_dict()

    # Test it's a dictionary
    assert isinstance(rents, dict)

    # Test start and end date
    dates = sorted(rents.keys())
    assert dates[0] == "2020-01"
    assert dates[-1] == "2024-12"

    # Test rent is in reasonable range
    for _, zips in rents.items():
        for _, rent in zips.items():
            assert 0 < rent < 6000


def test_generate_crosswalks_dict():
    crosswalks = generate_crosswalks_dict()

    # Test it's a dictionary
    assert isinstance(crosswalks, dict)

    # Test start and end date
    dates = sorted(crosswalks.keys())
    assert dates[0] == "2020-01"
    assert dates[-1] == "2024-12"

    # Test weight is in reasonable range
    for _, zips in crosswalks.items():
        for _, tract_weights in zips.items():
            for _, weight in tract_weights:
                assert 0 <= weight <= 1


def test_weight_to_census_tract():
    rent_by_zip = generate_rent_by_zip_dict()
    crosswalks = generate_crosswalks_dict()
    rent_by_tract = weight_to_census_tract(crosswalks, rent_by_zip)

    # Test it's a dictionary
    assert isinstance(rent_by_tract, dict)

    # Test start and end date
    dates = sorted(rent_by_tract.keys())
    assert dates[0] == "2020-01"
    assert dates[-1] == "2024-12"

    # Test final calculated rent is in reasonable range
    for _, tracts in rent_by_tract.items():
        for _, rent in tracts.items():
            assert 0 < rent < 6000


def test_generate_acs_df():
    acs_df = generate_acs_df()

    # Confirm each tract ID has 11 numbers
    for tract in acs_df["TL_GEO_ID"]:
        assert len(tract) == 11


def test_total_evictions_format():
    results = count_evictions_by_tract()
    assert results["geoid"].str.len().unique()[0] == 11
    # made a new column : total eviction
    assert "total_evictions" in results.columns


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


def test_no_missing_or_negative_values(merged_data):
    numeric_cols = [
        "median_rent",
        "eviction_rate",
        "311_calls",
        "tents",
        "structures",
        "vehicles",
        "estimate",
    ]

    # Test that numeric columns don't have missing or negative values
    for col in numeric_cols:
        assert merged_data[col].notnull().all()
        assert (merged_data[col] >= 0).all()


def test_merged_dates(merged_data):
    assert merged_data["date"].min() == "2020-01"
    assert merged_data["date"].max() == "2024-12"


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
