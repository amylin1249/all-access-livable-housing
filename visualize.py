import sys
import shapefile
import folium
import pathlib
import webbrowser
from pyproj import Transformer, CRS
from shapely import geometry
from shapely.ops import transform


def load_shapefile(
    filename: str,
) -> list[tuple]:
    """
    Load a shapefile using pyshp, returning Shapely geometries.
    """
    # this will be a list of (geometry, feature_dict) tuples
    geometries = []

    # opens the file (expects a file that ends in .shp)
    sf = shapefile.Reader(filename, encodingErrors="replace")

    fields = [field[0] for field in sf.fields[1:]]

    for record in sf.shapeRecords():
        # a `.shape.__geo_interface__` (essentially a list of points)
        # This is passed to the `shapely.shape` function to create
        # an instance of the appropriate geometry class.
        geom = geometry.shape(record.shape.__geo_interface__)

        # these objects also have a `.record` attribute
        # which is a list-like object with all attributes
        # we'll keep the shape in a tuple with its record data
        geometries.append((geom, dict(zip(fields, record.record))))

    return geometries


def quick_map(shapefile_data: list[tuple]):
    """
    Given shapefile data (returned from load_shapefile)
    create a folium map with all geometries for quick visualization.
    """
    centroid = shapefile_data[0][0].centroid
    map = folium.Map(location=[centroid.y, centroid.x], zoom_start=6)
    for geom, feat in shapefile_data:
        folium.GeoJson(geom.__geo_interface__).add_to(map)
    map.save("map.html")
    print("created map.html, trying to open browser...")
    webbrowser.open("file://" + str(pathlib.Path.cwd() / "map.html"))


def reproject_geometries(
    shapefile_data: list[tuple], from_epsg: str, to_epsg: str
) -> list[tuple]:
    """Reproject geometries from one CRS to another."""
    transformer = Transformer.from_crs(from_epsg, to_epsg, always_xy=True)

    reprojected = [
        (transform(transformer.transform, geom), feat) for geom, feat in shapefile_data
    ]
    return reprojected


def get_epsg_from_file(filename: str):
    """
    This function should read in the text from the PRJ file parameter
    and uses
    """
    with open(filename, "r") as f:
        prj_text = f.read()
    return CRS.from_wkt(prj_text).to_epsg()


def shapefile_stats(shapefile_data: list[tuple]):
    """
    Given a shapefile, print some basic stats:

    Number of records:
    Feature attributes:

    Note: Every feature in a dataset will have the same attributes,
    you can use a single one of the feature dictionaries & do not need
    to compare/combine keys from multiple features.
    """    
    print(f"Number of records: {len(shapefile_data)}")
    print("Feature attributes:")
    for key in shapefile_data[0][1]:
        print(key)


TO_PROJ_EPSG = "EPSG:4326"  # WGS 84 global projection

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: uv run python visualize.py (stats|map) path/to/shapefile.shp"
        )
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    shapefile_data = load_shapefile(filename)
    prj_file = filename.replace("shp", "prj")
    from_epsg = get_epsg_from_file(prj_file)
    data = reproject_geometries(shapefile_data, from_epsg, TO_PROJ_EPSG)

    match command:
        case "stats":
            print(f"Filename: {filename}")
            shapefile_stats(data)
        case "map":
            quick_map(data)
    # uv run python visualize.py map clean-data/merged_sf_shapefiles/merged_sf_tracts.shp
