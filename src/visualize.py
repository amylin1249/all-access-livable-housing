import pandas as pd
import geopandas as gpd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from pyproj import Transformer, CRS
from shapely import geometry
from shapely.ops import transform
from dash import Dash, html
import dash_vega_components as dvc

from .datatypes import (
    MERGED_SF_TRACTS_SHP,
    MERGED
)


# def visualize_sf_tracts():
#     """
#     Visualize SF tracts using MatPlotLib
#     """
#     sf_tracts = gpd.read_file(MERGED_SF_TRACTS_SHP)
#     sf_tracts.plot()
#     plt.show()


# def load_shapefile(
#     filename: str,
# ) -> list[tuple]:
#     """
#     Load a shapefile using pyshp, returning Shapely geometries.
#     """
#     # this will be a list of (geometry, feature_dict) tuples
#     geometries = []

#     # opens the file (expects a file that ends in .shp)
#     sf = shapefile.Reader(filename, encodingErrors="replace")

#     fields = [field[0] for field in sf.fields[1:]]

#     for record in sf.shapeRecords():
#         # a `.shape.__geo_interface__` (essentially a list of points)
#         # This is passed to the `shapely.shape` function to create
#         # an instance of the appropriate geometry class.
#         geom = geometry.shape(record.shape.__geo_interface__)

#         # these objects also have a `.record` attribute
#         # which is a list-like object with all attributes
#         # we'll keep the shape in a tuple with its record data
#         geometries.append((geom, dict(zip(fields, record.record))))

#     return geometries


# def quick_map(shapefile_data: list[tuple]):
#     """
#     Given shapefile data (returned from load_shapefile)
#     create a folium map with all geometries for quick visualization.
#     """
#     centroid = shapefile_data[0][0].centroid
#     map = folium.Map(location=[centroid.y, centroid.x], zoom_start=6)
#     for geom, feat in shapefile_data:
#         folium.GeoJson(geom.__geo_interface__).add_to(map)
#     map.save("map.html")
#     print("created map.html, trying to open browser...")
#     webbrowser.open("file://" + str(Path.cwd() / "map.html"))


# def reproject_geometries(
#     shapefile_data: list[tuple], from_epsg: str, to_epsg: str
# ) -> list[tuple]:
#     """Reproject geometries from one CRS to another."""
#     transformer = Transformer.from_crs(from_epsg, to_epsg, always_xy=True)

#     reprojected = [
#         (transform(transformer.transform, geom), feat) for geom, feat in shapefile_data
#     ]
#     return reprojected


# def get_epsg_from_file(filename: str):
#     """
#     This function should read in the text from the PRJ file parameter
#     and uses
#     """
#     with open(filename, "r") as f:
#         prj_text = f.read()
#     return CRS.from_wkt(prj_text).to_epsg()


def create_tract_map(
    source_file: Path, start_date: str, end_date: str, col_name: str, agg:str ="mean"
):
    """
    Add docstring
    """
    METRIC_NAMES = {
    "311_calls": "311 calls",
    "eviction_rate": "Eviction rate",
    "median_rent": "Median rent",
    "tents": "Tents",
    "structures": "Structures",
    "vehicles": "Vehicles",
    "estimate": "Homelessness estimate",
    }

    df = pd.read_csv(source_file)
    sf_tracts = gpd.read_file(MERGED_SF_TRACTS_SHP)
    ### TBD ON WHETHER THIS SHOULD BE INSIDE OR OUTSIDE FUNCTION

    df["tract"] = df["tract"].astype(str).str.zfill(11)
    df["date"] = pd.to_datetime(df["date"])
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)

    filtered_df = (
        df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        .groupby("tract")
        .agg(metric=(col_name, "mean"))
        .reset_index()
    )

    chart = (
        alt.Chart(sf_tracts)
        .mark_geoshape()
        .encode(
            color=alt.Color("metric:Q", title={METRIC_NAMES[col_name]}),
            tooltip=[
                alt.Tooltip("GEOID:N", title="Tract ID"),
                alt.Tooltip("population:Q", title="Population"),
                alt.Tooltip("med_hh_inc:Q", title="Median annual household income"),
                alt.Tooltip("white_pct:Q", title="% white population"),
                alt.Tooltip("metric:Q", title=f"Monthly average {METRIC_NAMES[col_name].lower()}"),
            ],
        )
        .transform_lookup(
            lookup="GEOID",
            from_=alt.LookupData(filtered_df, ("tract"), ["metric"]),
        )
        .project(type="albersUsa")
        .interactive()
    )

    return chart


def create_scatterplot(
    source_file: Path, x_var: str, x_agg: str, y_var: str, y_agg: str
):
    """
    Docstring
    """
    sns.set_theme(style="whitegrid")

    # Load dataset
    df = pd.read_csv(source_file)
    filtered_df = (
        df.groupby("tract")
        .agg(x_axis=(x_var, x_agg), y_axis=(y_var, y_agg))
        .reset_index()
    )

    # Draw a scatter plot while assigning point colors and sizes to different
    # variables in the dataset
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    sns.despine(f, left=True, bottom=True)
    sns.scatterplot(
        x="x_axis",
        y="y_axis",
        # hue="white_pct",
        # size="population",  ### To update these to the right metrics once dataset finalized
        palette="ch:r=-.2,d=.3_r",
        sizes=(1, 100),
        linewidth=0,
        data=filtered_df,
        ax=ax,
    )
    plt.xlabel("Average homelessness counts", fontsize=12)
    plt.ylabel("Median monthly rent ($)", fontsize=12)
    #plt.title(
    #    "Median rent by tract vs. Average homelessness counts",
    #    fontsize=14,
    #    fontweight="bold",
    #)
    plt.show()


if __name__ == "__main__":
    create_tract_map(MERGED, "2020-01", "2024-12", "estimate")
    # create_scatterplot(
    #     MERGED,
    #     "estimate",
    #     "mean",
    #     "median_rent",
    #     "mean",
    # )
