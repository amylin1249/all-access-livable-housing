# Project: All Access Livable Housing

## Members
- Haeji Ahn <ahaeji925@uchicago.edu>
- Lily Hoffman <lshoffman@uchicago.edu>
- Amy Lin <amsylin@uchicago.edu>
- Amanda Song <amandasong@uchicago.edu>


## Data Documentation
List the sources of data, any gaps or challenges in the data. Explain how data flows through the project. What else would someone picking this project up for the first time need to understand?

Sources of data and any key gaps include:
#1: DataSF Open Data Portal
    #1.1: 311 Cases - Deduplicating data was required
    #1.2: Quarterly count of tents, structures, and lived-in vehicles - Data interpolation was required
    #1.3: Evictions data
#2: Census Data - Manual imputation was required for negative values for rent and household income
    #2.1: ACS data on rental costs and demographic data
    #2.2: Listing and geographic boundaries of census tracts in SF
#3: Zillow Observed Renter Index (ZORI) - Imputation was required to fill missing data
#4: HUD ZIP Code Crosswalks - Data was seaprated across multiple Excel files with inconsistently named columns, and imputation was required to fill missing data
#5: Sacramento 2024 PIT Count Report

The data flows through a centralized pipeline starting with automated API extraction and CSV/XLSX file loading. ZIP-level ZORI data is disaggregated to census tracts using HUD crosswalks and normalized with ACS median rent values to account for local rent variations. Daily 311 service calls, daily eviction records, and quarterly encampment counts are spatially joined to tracts and aggregated to the monthly level. Eviction counts are converted to tract-level monthly rates using census population data. Quarterly encampment counts of tents, structures, and vehicles are interpolated to estimate monthly values. Tract-level street homeless population estimates are then generated using multipliers from the literature applied to encampments. All processed datasets are merged into a single tidy CSV, which feeds into the dashboard supporting multiple visualizations and regression analysis.

In order to understand this project, one should know that we used interpolation and HUD crosswalk calculations to align all data to the same spatial and temporal scale. Although the original data sources were reported at ZIP code or quarterly levels, we normalized everything to the monthly census tract level. It is also important to note that the quarterly encampment counts required direct communication with the SF Open Data Portal to obtain the underlying data. While a PowerBI map of these data is regularly updated, the underlying datasets linked to the map are not.


## Project Structure
The root consists mainly of src (directory containing our source files) and other key directories (tests, raw-data, clean-data).

Tree structure of first level of directories and files in src:
├── __init__.py
├── __main__.py
├── analyze_data.py
├── dashboard.py
├── datatypes.py
├── get_api_data.py
├── process_data.py
├── run_regression.py
├── spatial_join.py
└── visualize.py

Focusing on the src directory, we have 7 main modules spanning 3 key sections that feed into __main__: 1. Data retrieval (get_api_data)
2. Data cleaning and processing (process_data, spatial_join, analyze_data, run_regression)
3. Data visualization (visualize, dashboard)
The above modules are supported by datatypes, which contains global variables used across them.

Our project pipeline begins with data retrieval. The get_api_data module retrieves eviction data from an external API and saves the results to a CSV file for use in subsequent steps.

The next stage focuses on data cleaning and processing, beginning with the process_data module. This module merges ACS data with tract shapefiles, cleans encampments and 311 data, imputes missing Zillow data, processes crosswalks, deduplicates and standardizes key fields, and exports cleaned datasets to CSV and shapefiles in the cleaned-data folder.

The next processing step is implemented in the spatial_join module, which applies the quadtree-based spatial matching algorithm to match point latitude-longitude coordinates to their appropriate census tract polygons. This approach was adapted from PA4 and modified to fit the specifications of our project. We apply this procedure to three cleaned datasets on evictions, quarterly encampments, and 311 reports, outputting three files, each pertaining to a cleaned dataset, with an additional column that has the matched tract ID. 

The analyze_data module then aggregates counts from spatially joined datasets and consolidates metrics for analysis and visualization. run_regression examines the relationship between tract characteristics and monthly 311-reported addresses using OLS regression with year-month fixed effects.

The last section focuses on visualizations and dashboarding. The visualize module generates graphs including a choropleth map, regression graph, and line graphs of rent and encampments over time. The dashboard module integrates these visualizations into an interactive interface with background information, key statistics, and a series of visualizations that illustrate how homelessness trends in SF have evolved over time.

The above modules feed into our __main__.py file, which allows the entire pipeline to be executed from the command line. Given that our modules are all interlinked, this enables users to launch the dashboard, or even regenerate clean data files, ensuring the reproducibility of our files and analysis. 


## Team responsibilities

### Haeji
- Implemented initial filtering of ZORI data for SF zip codes and dates of interest (2020-2024)
- Built an automated API pipeline to retrieve, filter, and save real-time SF eviction records as standardized CSVs (get_api_data.py)
- Computed tract-level eviction rates by normalizing monthly eviction counts with census tract populations
- Spearheaded dashboard implementation, ensuring smooth integration of processed data into an interactive analytical tool
- Optimized map, plot, and regression code for faster visualizations and seamless dashboard interactivity
- Wrote `pytest` tests for relevant functions (eviction dataset, api datasets, and tidying csv ) to validate dataset and pipeline

### Lily
- Developed clean_address and clean_parenthesis functions to de-duplicate 311 service request data
- Implemented initial cleaning functions for 311 and encampment datasets
- Created run_regression.py to conduct tract-level regression analysis
- Developed regression coefficient visualization (create_reg_chart) in visualize.py to support data interpretation
- Built initial line graph visualizations for encampments and street homeless population estimates
- Reviewed interpolation, imputation, and other data processing choices, ensuring accuracy of derived metrics
- Wrote `pytest` tests for relevant functions (de-duplication, 311 and encampment datasets) to validate dataset and pipeline

### Amy
- Co-wrote script (with Amanda) to web-scrape publicly available shelter waitlist datasets (this was later archived due to limitations in upstream data availability)
- Implemented final cleaning functions for 311 and encampment datasets (converted to Pandas)
- Built the complete ingestion and cleaning pipeline for monthly median rent data (aside from Haeji's initial filtering step): imputed missing ZORI values, processed 20 HUD crosswalk Excel files (including imputation), and calculated weighted averages to generate tract-level monthly rent estimates
- Interpolated quarterly encampment data to estimate monthly counts for tents, structures, and vehicles 
- Built final line graph visualizations for encampments and street homeless population estimates
- Built line graph visualization for monthly median rent by ZIP code
- Assisted Haeji with dashboard by leading dashboard design (determining layout, visual structure, and interactive flow)
- Wrote textual content for dashboard
- Wrote `pytest` tests for relevant functions (ZORI dataset, HUD crosswalks) to validate dataset and pipeline

### Amanda
- Co-wrote script (with Amy) to web-scrape publicly available shelter waitlist datasets (this was later archived due to limitations in upstream data availability)
- Cleaned and processed Census and ACS data to consolidate key metrics into tract-level CSV and shapefile outputs
- Implemented geospatial matching to assign point-based data (coordinates) to census tracts
- Aggregated encampment reports and 311 service call data by month and census tract 
- Developed choropleth map using Altair to visualize housing and homelessness metrics across census tracts and time periods
- Built a command-line interface (CLI) to streamline execution of the data processing and analysis workflows
- Wrote `pytest` tests for relevant functions (census and ACS data processing, spatial join) to validate datasets and pipeline


## Final thoughts
Our project initially set out to examine the relationship between the number of unsheltered individuals and housing prices in San Francisco from 2020 to 2024 at the census tract level. We aimed to better understand the spatial patterns of homelessness across the city and the factors driving variation across tracts.

As we explored the problem, we identified additional relevant datasets (311 calls, eviction records) that enriched our analysis. We built a comprehensive data pipeline to harmonize these diverse sources, applying cleaning and processing techniques learned in class, including string standardization and quadtree-based spatial joins. Using Altair, we created visualizations to explore trends, and we developed an interactive dashboard through independent research.

Our analysis revealed clear spatial concentrations of homelessness in the Tenderloin and the Mission (areas well known for homelessness). Interestingly, it also suggested a gradual shift further south into India Basin and Bayview-Hunters Point (areas not typically associated with homelessness), with a growing proportion of individuals living in vehicles rather than tents. This shift may reflect recent encampment sweeps in central neighborhoods, which may have displaced individuals toward southern areas and contributed to increases in vehicle-based homelessness. Regression analysis also found a correlation between higher citizen-reported encampments (311 service calls) and tracts with larger White populations. 

Beyond these findings, this project strengthened the technical and analytical skills we developed in CAPP30121 and CAPP30122, including data retrieval, cleaning, spatial analysis, and visualization. Overall, it helped us consolidate these skills while producing analyses related to real-world issues.