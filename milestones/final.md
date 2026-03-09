# Project: All Access Livable Housing

## Members
- Haeji Ahn <ahaeji925@uchicago.edu>
- Lily Hoffman <lshoffman@uchicago.edu>
- Amy Lin <amsylin@uchicago.edu>
- Amanda Song <amandasong@uchicago.edu>


## Data Documentation
Sources of data and any key gaps include:
#1: DataSF Open Data Portal
    #1.1: 311 Cases - Deduplicating data was required
    #1.2: Quarterly count of tents, structures, and lived-in vehicles - Data interpolocation was required
    #1.3: Evictions data
#2: Census Data - Negative values were present for rent and household income, requiring us to manually impute these values.
    #2.1: ACS data on rental costs and demographic data
    #2.2: Listing and geographic boundaries of census tracts in SF
#3: Zillow Observed Renter Index (ZORI) - Data was missing and required us to impute these values.
#4: HUD Crosswalks - Columns were inconsistently name; data was separated across Excel files, and there was missing data that required us to impute.
#5: Sacramento 2024 PIT Count Report

The data flows through a centralized pipeline starting with automated API extraction and CSV loading, followed by a transformation stage where ZIP-level ZORI data is crosswalked to tracts and scaled using ACS median rent values to adjust local median rent variations. 311 calls and eviction records are grouped by month and tract to calculate monthly rates. Quarterly encampment data is interpolated to fill monthly gaps for tents, structures, and vehicles. A weighted homelessness estimate is calculated using predefined conservative multipliers for different encampment types. All processed streams are merged into a single Tidy CSV (merged_data.csv) regression analysis, spatial join, visualization and dashboard.

In order to understand this project, one would need to know that our project required interpolation in order to get all of our data onto the same spatial and temporal scale. While the original data sources may be on the zip code or quarterly levels, we normalized all data to the monthly census tract level. In addition, it's important to note that the quarterly encampment counts data required emailing with the SF Open Data Portal to get access to the underlying data. While a PowerBI map is regularly updated, the underlying data linked to the map is not. 


## Project Structure
The roots consists mainly of src (directory containing our source files), and other key directories (tests, raw-data, clean-data).

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

Focusing on the src directory, we have 7 main modules spanning 3 key sections that feed into __main__.py. The 3 key sections are:
1. Retrieving data (get_api_data)
2. Cleaning and processing data (process_data, spatial_join, analyze_data, run_regression)
3. Visualizing data (visualize, dashboard)
The above modules are supported by datatypes, which contain global variables used across them.

Our project pipeline begins with data retrieval. The get_api_data module retrieves eviction data from an external API and saves the results to a CSV file for use in subsequent steps.

The next stage focuses on data cleaning and processing, beginning with the process_data module. This module processes and merges ACS data with census tract shapefiles, cleans encampments and 311 homelessness reports data, filters and imputes missing Zillow data, and processes crosswalks Excel files. More broadly, this module deduplicates key variables, standardizes selected fields, and exports the cleaned datasets as CSV files and shapefiles in the cleaned-data folder.

The next processing step is implemented in the spatial_join module, which applies the quadtree-based spatial matching algorithm to match point latitude-longitude coordinates to their appropriate census tract polygons. This approach was adapted from PA4 and modified to fit the specifications of our project. We apply this procedure to three cleaned datasets on evictions, quarterly encampments, and 311 reports, outputting three files, each pertaining to a cleaned dataset, with an additional column that has the matched tract ID. 

Under data processing, the analyze_data module then aggregates counts from the spatially joined datasets to compute the total counts for each tract. It also combines all calculated metrics into a consolidated dataset, which forms the basis for our analysis and visualizations.

The final module in the data processing stage, run_regression, conducts statistical analysis to further examine the relationship between tract characteristics and the number of unique 311-reported addresses in a given month. This employs ordinary least squares regression with year-month fixed effects to strengthen our analysis. 

The last section focuses on visualizations and dashboarding. The visualize module generates several graphs that provide a visual representation of our data and analysis. These include a choropleth map illustrating tract-level metrics over specified time periods, a regression chart showing the results of our statistical analysis of 311 reports, and scatterplots depicting the temporal trends of monthly rent and encampments within individual tracts. 

Lastly, the dashboard module integrates all our visualizations into an interactive interface. The dashboard provides users with background information on our project, highlights key statistics observed, and presents a series of visualizations that illustrate how homelessness trends in SF have evolved over time.

The above modules feed into our __main__.py file, which allows the entire pipeline to be executed from the command line. Given that our modules are all interlinked, this enables users to launch the dashboard, or even regenerate clean data files, ensuring the reproducibility of our files and analysis. 


## Team responsibilities

### Haeji
- Processed and filtered Zillow Observed Renter Index (ZORI) data to analyze longitudinal rental trends across SF ZIP codes
- Built an automated API pipeline to retrieve, filter, and store real-time eviction records of SF into standardized CSV formats.
- Defined a weighted estimation logic using PIT data to calculate unsheltered population counts across various housing types
- Calculated tract-level eviction rates by merging multi-source datasets and structuring results into a unified data dictionary
- Wrote `pytest` tests to validate the accuracy of data extraction, filtering, and mathematical calculations
- Refactored core map, plots, regression codes of visualizing to optimize visualization performance and ensure seamless interactivity within the dashboard
- Spearheaded the development of a dashboard, designing the main interface and logic to synthesize housing and homelessness metrics 

### Lily
- Wrote the initial draft of the clean encampment process and clean 311 process
- The code for the clean encampment process includes helper code for address deduplication (clean_address and clean_parenthesis)
- Wrote pytest code for test_clean_address, test_generate_311_csv, test_generate_encampments_csv
- Wrote run_regression.py to merge necessary datasets and run regression results
- Wrote code for the regression coefficient visualization (create_reg_chart) in visualize.py 
- Wrote early versions code for two scatterplots - create_encampments_scatterplot, create_homeless_scatterplot (Amy finalized and embellished)

### Amy
- 

### Amanda
- Co-wrote script (with Amy) to web-scrape publicly available shelter waitlist datasets (this was later archived due to limitations in upstream data availability)
- Cleaned and processed Census and ACS data to consolidate key metrics into tract-level CSV and shapefile outputs
- Implemented geospatial matching to assign point-based data (coordinates) to census tracts
- Aggregated encampment reports and 311 service call data by month and census tract 
- Developed choropleth map using Altair to visualize housing and homelessness metrics across census tracts and time periods
- Built a command-line interface (CLI) to streamline execution of the data processing and analysis workflows
- Wrote `pytest` tests for relevant functions (mainly census and ACS data processing, and spatial join) to validate datasets and pipeline


## Final thoughts
Our project set out to examine the relationship between the number of unsheltered individuals and housing prices in San Francisco from 2020 to 2024 at the census tract level. Specifically, we sought to have a better understanding on the spatial patterns of homelessness across the city, and  the drivers that affect variation in homelessness across tracts. 

Through this project, we constructed our data pipeline from the ground up, retrieving data from multiple sources (including bulk datasets from the DataSF Open Data Portal, ACS data, and API for evictions data). We then cleaned and processed these datasets using skills that we learnt in class, such as string cleaning to standardize data formats, interpolation to increase temporal granularity, and quadtrees to improve data efficiency. We also created visualizations using tools introduced in class and developed an interactive dashboard using additional tools that we independently researched.

We managed to produce several intersting insights and observed clear spatial concentrations of homelessness in certain tracts, such as in the Tenderloin and the Mission. At the same time, our analysis showed that the distribution of homelessness has gradually shifted South toward areas such as India Basin in Bayview Hunters Point, with a growing proportion of individuals residing in vehicles rather than tents. This shift could be due to policy changes in recent years that targeted tents but led to increases in vehicle-based homelessness. 

We also conducted statistical analyses examining correlations between demographics, official encampment counts, and citizen-reported encampments. One key observation was that tracts with a higher percentage of White residents seemed to have higher numbers of citizen-reported encampments. 

Beyond these findings, this project enabled us to further develop our technical and analytical skills that we learnt in CAPP30121 and CAPP30122. These included retrieving data, cleaning and processing data, spatial analysis, and visualizing data. Overall, this project has truly helped us consolidate technical skills that we have developed over the last two quarters and produce analyses related to real-world issues. 
