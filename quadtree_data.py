from shapely.geometry import Point, Polygon
from typing import NamedTuple
import pathlib
import shapefile


class Location(NamedTuple):
    id: int
    latitude: float
    longitude: float
### TBD on attributes

class Tract(NamedTuple):
    id: str
    pop: int
    med_rent: int
    med_hh_inc: int
    white_pct: float
    polygon: Polygon


def load_shapefiles(path: pathlib.Path) -> Tract:
    """
    Extract and parse polygons from census shapefiles.
    """
    tracts = []
    with shapefile.Reader(path) as sf:
        for shape_rec in sf.shapeRecords():
            tracts.append(
                Tract(
                    id=shape_rec.record["TRACTCE"],
                    pop=shape_rec.record["population"],
                    med_rent=shape_rec.record["med_rent"],
                    med_hh_inc=shape_rec.record["med_hh_inc"],
                    white_pct=shape_rec.record["white_pct"],
                    polygon=Polygon(shape_rec.shape.points),
                )
            )
    return tracts


### Include code that loads the points data from other sources
