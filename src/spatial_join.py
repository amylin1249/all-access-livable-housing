from typing import NamedTuple, Union
from shapely.geometry import Polygon, box, Point
from pathlib import Path
from process_data import Encampment, EncampmentReport, clean_311, clean_encampment
import shapefile
import csv
import pandas as pd


MERGED_SF_TRACTS_SHP = (
    Path(__file__).parent.parent
    / "clean-data/merged_sf_shapefiles/merged_sf_tracts.shp"
)

SF_EVICTIONS = Path(__file__).parent.parent / "clean-data/evictions_api_data.csv"

SF_EVICTIONS_TRACTS = (
    Path(__file__).parent.parent / "clean-data/evictions_api_data_tracts.csv"
)
ENCAMPMENT_TRACTS = Path(__file__).parent.parent / "clean-data/encampment_tracts.csv"
ENCAMPMENT_REPORT_TRACTS = Path(__file__).parent.parent / "clean-data/311_tracts.csv"

### TEMP ISSUE FILES
SF_EVICTIONS_ISSUES = (
    Path(__file__).parent.parent / "clean-data/evictions_api_issues.csv"
)
ENCAMPMENT_ISSUES = (
    Path(__file__).parent.parent / "clean-data/encampment_tracts_issues.csv"
)
ENCAMPMENT_REPORT_ISSUES = (
    Path(__file__).parent.parent / "clean-data/311_tracts_issues.csv"
)


class Tract(NamedTuple):
    id: str
    pop: int
    med_rent: int
    med_hh_inc: int
    white_pct: float
    polygon: Polygon


def load_shapefiles(path: Path) -> list[Tract]:
    """
    Extract and parse polygons from census shapefiles.
    """
    tracts = []
    with shapefile.Reader(path) as sf:
        for shape_rec in sf.shapeRecords():
            tracts.append(
                Tract(
                    id=shape_rec.record["GEOID"],
                    pop=shape_rec.record["population"],
                    med_rent=shape_rec.record["med_rent"],
                    med_hh_inc=shape_rec.record["med_hh_inc"],
                    white_pct=shape_rec.record["white_pct"],
                    polygon=Polygon(shape_rec.shape.points),
                )
            )
    return tracts


### Include code that loads the points data from other sources


class QuadtreeError(Exception):
    """Exception used within Quadtree for unexpected cases"""


class BBox(NamedTuple):
    """Named tuple for storing bounding box data."""

    min_x: float
    min_y: float
    max_x: float
    max_y: float


class Location(NamedTuple):
    id: int
    lat: float
    lon: float


# Maximum depth of a quadtree.
# Do not subdivide nodes if depth exceeds this value.
MAX_DEPTH = 8


class Quadtree:
    """
    Class that represents a node in the quadtree.

    Each node has:
        - bounding box (bbox)
        - capacity
        - depth (first node is depth=0, children would be depth=1, etc.)
        - either children OR polygons
    """

    def __init__(self, bbox: BBox, capacity: int, depth: int = 0):
        self.bbox = bbox
        self.capacity = capacity
        self.depth = depth
        self.polygons = {}
        self.children = []
        self.bbox_polygon = box(
            self.bbox.min_x, self.bbox.min_y, self.bbox.max_x, self.bbox.max_y
        )

    def is_split(self) -> bool:
        """
        Check if this node in the quadtree is split.

        Returns:
            True if split, False otherwise.
        """
        if self.children and self.polygons:
            raise QuadtreeError("polygons and children on same node")
        if len(self.children) not in (4, 0):
            raise QuadtreeError("a node must always have 0 or 4 children")
        return bool(self.children)

    def __repr__(self) -> str:
        """
        Returns a view of the interior of the node.
        """
        if self.is_split():
            return f"Quadtree{list(self.children)}"
        return f"Quadtree(polygons={len(self.polygons)})"

    def add_polygon(self, id: str, polygon: Polygon) -> bool:
        """
        Add a polygon to the node or its children if the polygon is within the
        bounding box for the node.

        Parameters:
            id: a string that is an id to identify the polygon
            polygon: a Polygon object that represents the polygon itself

        Returns:
            True if the polygon is added to the node or its children,
            False otherwise (if polygon is not within bounding box for the node).
        """
        if not polygon.intersects(self.bbox_polygon):
            return False

        # Add the polygon to the node if it is not split
        if not self.is_split():
            self.polygons[id] = polygon
            if len(self.polygons) > self.capacity and self.depth <= MAX_DEPTH:
                self.split_node()
        # If the node is split, add the polygon to its children
        else:
            for child in self.children:
                child.add_polygon(id, polygon)

        return True

    def split_node(self):
        """
        Split node in the quadtree to create four child nodes and distribute
        polygons in the original node among its child nodes.
        """
        capacity = self.capacity
        depth = self.depth

        min_x = self.bbox.min_x
        min_y = self.bbox.min_y
        max_x = self.bbox.max_x
        max_y = self.bbox.max_y

        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        children = [
            Quadtree(BBox(min_x, min_y, mid_x, mid_y), capacity, depth + 1),
            Quadtree(BBox(mid_x, min_y, max_x, mid_y), capacity, depth + 1),
            Quadtree(BBox(min_x, mid_y, mid_x, max_y), capacity, depth + 1),
            Quadtree(BBox(mid_x, mid_y, max_x, max_y), capacity, depth + 1),
        ]

        for child in children:
            for id, polygon in self.polygons.items():
                child.add_polygon(id, polygon)
            self.children.append(child)

        self.polygons = {}

    def match(self, point: Point) -> set[str]:
        """
        Find the id of all polygons that the given point falls within that are
        within the node or its children.

        Parameters:
            point: a Point object that is checked for whether it falls within
            the polygons

        Returns:
            A set of strings of ids of polygons within which the point falls.
        """
        matching_polygons = set()

        if self.bbox_polygon.contains(point):
            # Add polygon id to the set if the point falls within that polygon
            if not self.children:
                for id, polygon in self.polygons.items():
                    if polygon.contains(point):
                        matching_polygons.add(id)
            # Add polygon id to the set if the point falls within any of its
            # children's polygons
            else:
                for child in self.children:
                    matching_polygons = child.match(point)
                    if matching_polygons:
                        # Break out of loop if the point falls within a child's
                        # polygon(s) as it would not fall within other children
                        break

        return matching_polygons


def load_evictions_csv(path: Path) -> list[Location]:
    """
    Given a CSV containing eviction locations data, return a list of Location objects.
    """
    evictions = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            evictions.append(
                Location(
                    id=row["id"],
                    lat=row["lat"],
                    lon=row["lon"],
                )
            )
    return evictions


def quadtree_spatial_join(
    locations: list[Union[Location, Encampment, EncampmentReport]],
    tracts: list[Tract],
) -> dict:
    """
    Given a list of Location and Tract NamedTuples, compute a spatial join
    between the Location point and the Tract polygon using Quadtree class.

    Returns:
        A dictionary of location.id as keys and tract.id as values.
    """
    sf_bbox = BBox(-122.517724, 37.708182, -122.357071, 37.833227)
    # Westernmost (not incl. Farallon): 37.780436, -122.517724
    # Easternmost: Bayview Hunters Point 37.728650, -122.357071
    # Northernmost: Treasure Island 37.833227, -122.372522
    # Southernmost: 37.708182, -122.485839

    capacity = 10
    quadtree = Quadtree(sf_bbox, capacity)

    join_dict = {}

    for tract in tracts:
        quadtree.add_polygon(tract.id, tract.polygon)

    for location in locations:
        location_point = Point(location.lon, location.lat)

        for tract_id in quadtree.match(location_point):
            join_dict[location.id] = tract_id

        ### TRYING TO TEMPORARILY FIX WHILE DEBUGGING (but not working - seems like the point just doesn't fall in any polygon)
        # if location.id not in join_dict:
        #     for tract in tracts:
        #         if tract.polygon.contains(location_point):
        #             join_dict[location.id] = tract.id

    return join_dict


### NOTE: The last parameter is a temporary parameter to analyze how many ID's are not in the file
def add_evictions_tracts_csv(
    source_file: Path, dest_file: Path, missing_key_file: Path
):
    """
    Add docstring
    """
    missing_keys = []  ### TO REMOVE ONCE FIXED

    match_tracts = quadtree_spatial_join(
        load_evictions_csv(SF_EVICTIONS), load_shapefiles(MERGED_SF_TRACTS_SHP)
    )

    with open(source_file, "r") as source_file, open(dest_file, "w") as dest_file:
        reader = csv.DictReader(source_file)

        #
        headers = reader.fieldnames
        writer_headers = tuple(headers + ["geoid"])

        writer = csv.DictWriter(dest_file, fieldnames=writer_headers)
        writer.writeheader()

        # Iterate over each row in source file, add tract geoid, and write it to destination file
        for row in reader:
            ### TO REMOVE THIS "IF" STATEMENT ONCE FIXED
            if row["id"] not in match_tracts:
                missing_keys.append((row["id"], row["lat"], row["lon"]))
            else:
                row["geoid"] = match_tracts[row["id"]]
                writer.writerow(row)

    ### TO REMOVE ONCE FIXED
    with open(missing_key_file, "w") as issue_file:
        writer = csv.writer(issue_file)
        writer.writerows(missing_keys)


def add_encampments_tracts_csv(
    data: list[tuple], dest_file: Path, match_tracts: dict, missing_key_file: Path
):
    """
    ADD DOCSTRING
    """
    missing_keys = []  ### TO REMOVE ONCE FIXED

    headers = data[0]._fields + ("geoid",)

    with open(dest_file, "w") as dest_file:
        writer = csv.DictWriter(dest_file, fieldnames=headers)
        writer.writeheader()

        for row in data:
            if row.id not in match_tracts:
                missing_keys.append((row.id, row.lat, row.lon))
            else:
                row_dict = row._asdict()
                row_dict["geoid"] = match_tracts[row.id]
                writer.writerow(row_dict)

    ### TO REMOVE ONCE FIXED
    with open(missing_key_file, "w") as issue_file:
        writer = csv.writer(issue_file)
        writer.writerows(missing_keys)


if __name__ == "__main__":
    tracts_shp = load_shapefiles(MERGED_SF_TRACTS_SHP)

    add_evictions_tracts_csv(SF_EVICTIONS, SF_EVICTIONS_TRACTS, SF_EVICTIONS_ISSUES)

    clean_311 = clean_311()
    add_encampments_tracts_csv(
        clean_311,
        ENCAMPMENT_REPORT_TRACTS,
        quadtree_spatial_join(clean_311, tracts_shp),
        ENCAMPMENT_REPORT_ISSUES,
    )

    clean_encampment = clean_encampment()
    add_encampments_tracts_csv(
        clean_encampment,
        ENCAMPMENT_TRACTS,
        quadtree_spatial_join(clean_encampment, tracts_shp),
        ENCAMPMENT_ISSUES,
    )
