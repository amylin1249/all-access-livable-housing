import sys
import shapefile
import folium
import pathlib
import webbrowser
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from pyproj import Transformer, CRS
from shapely import geometry
from shapely.ops import transform


MERGED_SF_TRACTS_SHP = (
    Path(__file__).parent.parent
    / "clean-data/merged_sf_shapefiles/merged_sf_tracts.shp"
)


def visualize_sf_tracts():
    """
    Visualize SF tracts using MatPlotLib
    """
    sf_tracts = gpd.read_file(MERGED_SF_TRACTS_SHP)
    sf_tracts.plot()
    plt.show()


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


def create_scatterplot():
    """
    Docstring
    """
    sns.set_theme(style="whitegrid")

    # Load dataset
    dataset = pd.read_csv(
        Path(__file__).parent.parent / "clean-data/census_acs_join.csv"
    )  ### To update string with the dataset name

    # Filter dataset to remove tracts with population of 0
    filtered = dataset[dataset["population"] > 0]

    # Draw a scatter plot while assigning point colors and sizes to different
    # variables in the dataset
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    sns.despine(f, left=True, bottom=True)
    sns.scatterplot(
        x="med_hh_inc",
        y="med_rent",  ### To update these to the right metrics once dataset finalized
        hue="white_pct",
        size="population",  ### To update these to the right metrics once dataset finalized
        palette="ch:r=-.2,d=.3_r",
        sizes=(1, 100),
        linewidth=0,
        data=filtered,
        ax=ax,
    )
    plt.xlabel("Median annual household income ($)", fontsize=12)
    plt.ylabel("Median monthly rent ($)", fontsize=12)
    plt.title(
        "Median rent vs. Median household income by tract",
        fontsize=14,
        fontweight="bold",
    )
    plt.show()


TO_PROJ_EPSG = "EPSG:4326"  # WGS 84 global projection

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: uv run python visualize.py path/to/shapefile.shp"
        )
        sys.exit(1)

    filepath = Path(__file__).parent.parent / sys.argv[1]

    shapefile_data = load_shapefile(filepath)
    prj_file = str(filepath).replace("shp", "prj")
    from_epsg = get_epsg_from_file(prj_file)
    data = reproject_geometries(shapefile_data, from_epsg, TO_PROJ_EPSG)

    quick_map(data)
    # uv run python visualize.py clean-data/merged_sf_shapefiles/merged_sf_tracts.shp

    # visualize_sf_tracts()
    # create_scatterplot()
