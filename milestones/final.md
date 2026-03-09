# Project: All Access Livable Housing

## Members

- Haeji Ahn <ahaeji925@uchicago.edu>
- Lily Hoffman <lshoffman@uchicago.edu>
- Amy Lin <amsylin@uchicago.edu>
- Amanda Song <amandasong@uchicago.edu>


## Data Documentation
List the sources of data, any gaps or challenges in the data. Explain how data flows through the project. What else would someone picking this project up for the first time need to understand?

Source of Data
#1: DataSF Open Data Portal
    #1.1: 311 Cases
    #1.2: Quarterly count of tents, structures, and lived-in vehicles
    #1.3: Evictions data
#2: Census Data
    #2.1: ACS data on rental costs and demographic data
    #2.2: Listing and geographic boundaries of census tracts in SF
#3: Zillow Observed Renter Index (ZORI)
#4: HUD Crosswalks
#5: Sacramento 2024 PIT Count Report

The data flows through a centralized pipeline starting with automated API extraction and CSV loading, followed by a transformation stage where ZIP-level ZORI data is crosswalked to Census Tracts and scaled using ACS median rent values to adjust local median rent variations. 311 calls and eviction records are grouped by month and tract to calculate monthly rates. Quarterly encampment data is interpolated to fill monthly gaps for tents, structures, and vehicles. A weighted homelessness estimate is calculated using predefined conservative multipliers for different encampment types. All processed streams are merged into a single Tidy CSV (merged_data.csv) regression analysis, spatial join, visualization and dashboard.




## Project Structure
Write a page or so describing the structure of your project. What modules exist? What do they do? A diagram may be helpful here.

Tree structure of first level of directories and files in root:
├── README.md
├── __pycache__
├── clean-data
├── milestones
├── pyproject.toml
├── raw-data
├── scratch
├── src
├── tests
└── uv.lock

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

Focusing on the src directory where we have our source code, we have 7 main modules spanning 3 key sections that later feed into __main__.py. The 3 key sections are as follows:
1. Retrieving data (get_api_data)
2. Cleaning and processing data (process_data, spatial_join, analyze_data, run_regression)
3. Visualizing data (visualize, dashboard)
The above modules are supported by datatypes, which contain global variables used across them.

Starting from the first stage of retrieving data, the get_api_data module retrieves data from the evictions data API, which is saved to a CSV file.

Under data cleaning and processing, we begin with process_data. This module processes and merges ACS data and census shapefiles, cleans and generates encampments and 311 homelessness reports data, filters and imputes missing Zillow data, and processes crosswalks excel files. Processing the ACS files requires imputing negative values. Cleaning the 311 encampment reports requires additional processing of address strings and the removal of duplicate latitude–longitude–month combinations. This step ensures that we measure the unique number of encampments reported in a given month, rather than simply counting the total number of reports submitted. Processing crosswalks also requires interpolation and matching of data from zip codes to tracts to get numbers for each tract. More generally, this module deduplicates key variables, standardizes selected fields, and exports the cleaned output to CSV files and shapefiles in the cleaned-data folder.

spatial_join is the next module under data processing, which implements the quadtree-based spatial matching algorithm to match point lat/lon coordinates to their appropriate census tract polygons. This has been adapted from PA4 and modified to fit the specifications of our model. We apply this procedure to three cleaned datasets: evictions (api_evictions_data.csv), quarterly encampments (clean_encampments_data.csv), and 311 reports (clean_311_data.csv). It then outputs 3 files, one pertaining to each of the cleaned files, with an additional column with the matched tract ID. 

Under data processing, we also have the analyze_data module, where we aggregate counts from the joined files (with tract IDs) to get the total counts for each tract, and combine all calculated metrics into a consolidated file. This file forms the basis of our analysis and subsequent visualizations.

The final module under data processing is run_regression, whose primary purpose is to run a regression model to deepen understanding of the relationship between tract features and the unique number of reported 311 addresses in a given month with available point estimates. This employs statistical analysis, including ordinary least squares and year-month fixed effects to strengthen our analysis. 

The last section is focused on visualizations and dashboarding. The visualize module forms the basis of the graphs that provide a visual representation of our data and analysis. These include a choropleth map representing different metrics across tracts over specified time periods, a regression chart that shows the results of regression analysis on 311 reports, and  



## Team responsibilities

### Haeji
- Processed and filtered Zillow Observed Renter Index (ZORI) data to analyze longitudinal rental trends across 23 San Francisco ZIP codes from 2020 to 2024
- Built an automated API pipeline to retrieve, filter, and store real-time eviction records of SF into standardized CSV formats.
- Defined a weighted estimation logic using PIT data to calculate unsheltered population counts across various housing types
- Calculated tract-level eviction rates by merging multi-source datasets and structuring results into a unified data dictionary
- Wrote `pytest` tests to validate the accuracy of data extraction, filtering, and mathematical calculations.
- Refactored core plotting code of visualizing to optimize visualization performance and ensure seamless interactivity within the dashboard
- Spearheaded the development of a dashboard, designing the main interface and logic to synthesize housing and homelessness metrics into a functional user experience

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
Reflect on what the project intended to accomplish and what it did.

Our project set out to examine the relationship between the number of unsheltered individuals and housing prices in San Francisco from 2020 to 2024 at the census tract level. Specifically, we sought to have a better understanding on the spatial patterns of homelessness across the city, and  the drivers that affect variation in homelessness across tracts. 

Through this project, we constructed our data pipeline from the ground up, retrieving data from multiple sources (including bulk datasets from the DataSF Open Data Portal, ACS data, and API for evictions data). We then cleaned and processed these datasets using skills that we learnt in class, such as string cleaning to standardize data formats, interpolation to increase temporal granularity, and quadtrees to improve data efficiency. We also created visualizations using tools introduced in class and developed an interactive dashboard using additional tools that we independently researched.

We managed to produce several intersting insights on the relationship between homelessness and rent prices patterns, as well as individual trends in both variables during the period of analysis, such as during the COVID-19 pandemic. We also observed clear spatial concentrations of homelessness in certain tracts, particularly in the Tenderloin and the Mission. At the same time, our analysis showed that the distribution of homelessness has gradually shifted South toward areas such as India Basin in Bayview Hunters Point, with a growing proportion of individuals residing in vehicles rather than tents. This shift could be due to policy changes in recent years that targeted tents but led to increases in vehicle-based homelessness. 

We also conducted statistical analyses examining correlations between demographics, official encampment counts, and citizen-reported encampments. One key observation was that tracts with a higher percentage of White residents seemed to have higher numbers of citizen-reported encampments. 

Beyond these findings, this project enabled us to further develop our technical and analytical skills. We applied foundational skills that we learnt in CAPP30121, while building on the more advanced skills introduced in CAPP30122 through lectures and assignments. These included retrieving data, cleaning and processing data, spatial analysis, and visualizing data. Overall, this project has truly helped us consolidate technical skills that we have developed over the last two quarters and produce analyses related to real-world issues. 
