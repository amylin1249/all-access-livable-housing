from .get_api_data import get_evictions_data, save_evictions_to_csv
from .process_data import (
    process_acs_data,
    create_sf_shapefiles,
    add_sf_tract_data,
    generate_311_csv,
    generate_encampments_csv,
    generate_zillow_csv,
    generate_crosswalks_csv,
)
from .spatial_join import join_tracts_csv
from .analyze_data import generate_tidy_csv
from .dashboard import app

from .datatypes import (
    CLEAN_EVICTIONS,
    CLEAN_ENCAMP,
    CLEAN_311,
    JOINED_EVICTIONS_TRACTS,
    JOINED_ENCAMP_TRACTS,
    JOINED_311_TRACTS,
)


def main():
    # # Run functions from get_api_data module to retrieve data from the relevant API
    # result = get_evictions_data()
    # if result:
    #     save_evictions_to_csv(result)
    # print("Pulled data from relevant API")

    # # Run functions from process_data module to generate intermediate data files from raw data
    # process_acs_data()
    # create_sf_shapefiles()
    # add_sf_tract_data()
    # generate_311_csv()
    # generate_encampments_csv()
    # generate_zillow_csv()
    # generate_crosswalks_csv()
    # print("Generated all intermediate clean data files required for further analysis")

    # # Run functions from spatial_join module to match location points to their respective tracts
    # join_tracts_csv(CLEAN_EVICTIONS, JOINED_EVICTIONS_TRACTS)
    # join_tracts_csv(CLEAN_ENCAMP, JOINED_ENCAMP_TRACTS)
    # join_tracts_csv(CLEAN_311, JOINED_311_TRACTS)
    # print("Matched all point data to tracts for those that fall within a matching SF tract")

    # # Run function from analyze module to generate a consolidated data file with key metrics for visualization
    # generate_tidy_csv()
    # print("Generated a consolidated CSV to be used in visualization")

    # Run dashboard with interactive visualizations
    print(
        "Copy the link below from Dash and paste it into your web browser to view our interactive visualizations."
    )
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    print("Hello from Project All Access Livable Housing!")
    print("Our application is now starting.")
    main()
    print("Our application has finished running.")
