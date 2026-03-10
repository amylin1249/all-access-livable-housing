import pytest
import pandas as pd
from src.spatial_join import Quadtree, BBox, quadtree_spatial_join
from shapely.geometry import box, Point
from src.spatial_join import Location, Tract, load_shapefiles, load_points_csv
from src.datatypes import (
    MERGED_SF_TRACTS_SHP,
    CLEAN_EVICTIONS,
    CLEAN_ENCAMP,
    CLEAN_311,
    JOINED_EVICTIONS_TRACTS,
    JOINED_ENCAMP_TRACTS,
    JOINED_311_TRACTS,
)

# Tests below have been adapted from CAPP122 Winter 2026 PA4 (instructor James
# Turk), with modifications and additional tests to customize to our dataset.

POLYGON_OUTSIDE = box(-122.45, 37.6, -122.43, 37.65)
POLYGON_NW = box(-122.48, 37.77, -122.46, 37.79)
POLYGON_NE = box(-122.34, 37.76, -122.31, 37.78)
POLYGON_SW = box(-122.45, 37.72, -122.42, 37.74)
POLYGON_SE = box(-122.37, 37.71, -122.34, 37.73)


@pytest.fixture
def real_tracts():
    return load_shapefiles(MERGED_SF_TRACTS_SHP)


@pytest.fixture
def locations():
    return [
        Location(id=1, lat=37.786986977, lon=-122.419110401),
        Location(id=2, lat=37.821671, lon=-122.419110401),
        Location(id=3, lat=37.730109341, lon=-122.393489943),
    ]
    # Location 1 is within T-X
    # Location 2 is not within any tract
    # Location 3 is within T-Y


@pytest.fixture
def tracts():
    return [
        Tract(
            id="T-X",
            pop=3000,
            med_rent=2800,
            med_hh_inc=100000,
            white_pct=0.3,
            polygon=box(-122.43, 37.76, -122.39, 37.79),
        ),  # northern box
        Tract(
            id="T-Y",
            pop=3000,
            med_rent=2500,
            med_hh_inc=90000,
            white_pct=0.7,
            polygon=box(-122.43, 37.71, -122.39, 37.74),
        ),  # southern box
        Tract(
            id="T-Z",
            pop=3000,
            med_rent=3000,
            med_hh_inc=110000,
            white_pct=0.8,
            polygon=box(-122.5, 35.2, -122.4, 35.8),
        ),  # far away
    ]


@pytest.fixture
def empty():
    # Similar to SF bounds
    return Quadtree(BBox(-122.5, 37.7, -122.3, 37.8), capacity=2)


@pytest.fixture
def four(empty):
    empty.add_polygon("NW", POLYGON_NE)
    empty.add_polygon("NE", POLYGON_NE)
    empty.add_polygon("SW", POLYGON_SW)
    empty.add_polygon("SE", POLYGON_SE)
    return empty


def test_spatial_join_is_split_no(empty):
    assert not empty.is_split(), "Node should not be split."


def test_spatial_join_add_polygon_basic(empty):
    # Add a single polygon
    added_node = empty.add_polygon("SE", POLYGON_SE)
    assert len(empty.polygons) == 1, "Polygon was not added"
    assert added_node, "add_polygon should return True if the polygon is added"
    assert not empty.is_split(), "Polygon should not be split yet"


def test_spatial_join_add_polygon_not_inside(empty):
    # Add a single polygon that is not within the bbox
    added_node = empty.add_polygon("OUT", POLYGON_OUTSIDE)
    assert added_node is False, "add_polygon should return false if not inside bbox"
    assert len(empty.polygons) == 0, "Polygon should not have been added, outside bbox"
    assert not empty.is_split(), "Polygon should not have been added, outside bbox"


def test_spatial_join_add_polygon_two_quads(empty):
    # Node should not split with the addition of only two polygons
    empty.add_polygon("SW", POLYGON_SW)
    empty.add_polygon("NE", POLYGON_NE)
    assert not empty.is_split(), "Node should not have split"
    assert len(empty.polygons) == 2, (
        "2 polygons should be present, only {len(empty.polygons)}"
    )


def test_spatial_join_add_polygon_three_quads(four):
    # Node should split with the addition of three polygons as capacity has exceeded
    assert four.is_split(), "Node should have split, capacity exceeded"
    assert len(four.polygons) == 0, "Polygons should not exist on root node anymore"

    has_polygons = 0
    for child in four.children:
        assert not child.is_split(), "Only root level should have split"
        if child.polygons:
            has_polygons += 1
    assert has_polygons == 3, (
        f"Expected polygons in 3 of the subquads, but had {has_polygons}"
    )


def test_spatial_join_inherit_parent_capacity(four):
    assert four.children, "Expecting children on fixture 'four'"
    for child in four.children:
        assert child.capacity == four.capacity, (
            "Children should inherit parent capacity"
        )


def test_spatial_join_match_single_item(empty):
    empty.add_polygon("SE", POLYGON_SE)
    point = Point(-122.36, 37.72)  # inside POLYGON_SE
    matches = empty.match(point)
    assert len(matches) == 1
    assert "SE" in matches


def test_spatial_join_match_single_split(four):
    point = Point(-122.36, 37.72)  # inside POLYGON_SE
    matches = four.match(point)
    assert len(matches) == 1
    assert "SE" in matches


def test_spatial_join_match_max_depth_split(empty):
    # Add the same polygon 3 times to the bbox to force max depth split
    empty.add_polygon("A", POLYGON_SE)
    empty.add_polygon("B", POLYGON_SE)
    empty.add_polygon("C", POLYGON_SE)
    point = Point(-122.36, 37.72)  # inside POLYGON_SE
    matches = empty.match(point)
    assert matches == {"A", "B", "C"}, "All three polygons should contain point"


def test_spatial_join_match_no_matches(empty):
    empty.add_polygon("SE", POLYGON_SE)
    matches = empty.match(Point(-122.43, 37.73))
    assert len(matches) == 0


def test_spatial_join_match_empty_tree(empty):
    matches = empty.match(Point(-122.43, 37.73))
    assert len(matches) == 0


def test_spatial_join_match_point_outside_bbox(empty):
    empty.add_polygon("SE", POLYGON_SE)
    matches = empty.match(Point(-122.3, 37))  # Outside SF bbox
    assert len(matches) == 0


def test_spatial_join_join_polygons(locations, tracts):
    results = quadtree_spatial_join(locations, tracts)
    expected = {1: "T-X", 3: "T-Y"}
    # Location 1 is within T-X
    # Location 2 is not within any tract
    # Location 3 is within T-Y
    assert results == expected, f"Expected {expected}, got {results}"


def test_spatial_join_join_real_polygons(locations, real_tracts):
    results = quadtree_spatial_join(locations, real_tracts)
    expected = {1: "06075012002", 3: "06075023003"}
    assert results == expected, f"Expected {expected}, got {results}"


def test_spatial_join_load_csv():
    evictions_locations = load_points_csv(CLEAN_EVICTIONS)
    encamp_locations = load_points_csv(CLEAN_ENCAMP)
    encamp_311_locations = load_points_csv(CLEAN_311)

    assert len(evictions_locations) == 4765
    assert len(encamp_locations) == 9721
    assert len(encamp_311_locations) == 104512


def test_spatial_join_csv_cols():
    clean_evictions_df = pd.read_csv(CLEAN_EVICTIONS)
    clean_encamp_df = pd.read_csv(CLEAN_ENCAMP)
    clean_311_df = pd.read_csv(CLEAN_311)

    joined_evictions_df = pd.read_csv(JOINED_EVICTIONS_TRACTS)
    joined_encamp_df = pd.read_csv(JOINED_ENCAMP_TRACTS)
    joined_311_df = pd.read_csv(JOINED_311_TRACTS)

    # Test that joined datasets have exactly one more column than the clean datasets for the matched tract ID
    assert len(joined_evictions_df.columns) == len(clean_evictions_df.columns) + 1
    assert len(joined_encamp_df.columns) == len(clean_encamp_df.columns) + 1
    assert len(joined_311_df.columns) == len(clean_311_df.columns) + 1
