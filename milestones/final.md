# Project: All Access Livable Housing

## Members
- Haeji Ahn <ahaeji925@uchicago.edu>
- Lily Hoffman <lshoffman@uchicago.edu>
- Amy Lin <amsylin@uchicago.edu>
- Amanda Song <amandasong@uchicago.edu>


## Data Documentation
Sources of data and any key gaps include:
1. DataSF Open Data Portal - (1) 311 - Deduplicating data was required; (2) Quarterly encampments - Data interpolation was required; (3) Evictions
2. Census - (1) ACS - Imputation was required for negative values; (2) CA and SF tracts
3. Zillow Observed Renter Index (ZORI) - Imputation was required to fill missing data
4. HUD ZIP Code Crosswalks - Data was separated across multiple Excel files with inconsistently named columns; imputation was required to fill missing data
5. Sacramento 2024 PIT Count Report

Our centralized pipeline starts with automated API extraction and CSV/XLSX extraction. ZIP-level ZORI data is disaggregated to census tracts using HUD crosswalks and normalized with ACS median rent values. Daily 311 service calls, daily eviction records, and quarterly encampment counts are spatially joined to tracts and aggregated to the monthly level. Eviction counts are converted to tract-level monthly rates. Quarterly encampment counts are interpolated to estimate monthly values. Tract-level street homeless population estimates are then generated using multipliers from the literature. All processed datasets are merged into a single tidy CSV, used in the dashboard.

To understand this project, one should know that we used interpolation and HUD crosswalk calculations to align data to the same spatial and temporal scale. Quarterly encampment counts required direct communication with the SF Open Data Portal team to obtain the underlying data.


## Project Structure
The root consists mainly of src (directory containing our source files),tests, raw-data, and clean-data. Focusing on src, we have 7 key modules spanning 3 key sections that feed into __main__: 
1. Data retrieval (get_api_data)
2. Data processing (process_data, spatial_join, analyze_data, run_regression)
3. Data visualization (visualize, dashboard)
These are supported by datatypes, which contains global variables used across them.

Our project pipeline begins with data retrieval. The get_api_data module retrieves eviction data from an external API and saves the results to a CSV file.

The next stage focuses on data processing, beginning with process_data. This module merges ACS data with tract shapefiles, cleans encampments and 311 data, imputes missing Zillow data, processes crosswalks, deduplicates and standardizes key fields, and exports cleaned datasets to CSV and shapefiles in the cleaned-data folder. We then implemented spatial_join, which applies quadtrees to match point coordinates from cleaned evictions, encampments, and 311 reports datasets to appropriate census tract polygons. The analyze_data module then aggregates counts from spatially joined datasets and consolidates metrics for analysis and visualization. run_regression examines the relationship between tract characteristics and monthly 311-reported addresses using OLS regression.

The last section focuses on visualizations and dashboarding. The visualize module generates graphs including a choropleth map, regression graph, and line graphs of rent and encampments over time. The dashboard module integrates these visualizations into an interactive interface with background information, key statistics, and a series of visualizations that illustrate how homelessness trends in SF have evolved over time.

The above modules feed into our __main__.py file, which allows the entire pipeline to be executed from the command line. Given that our modules are all interlinked, this enables users to launch the dashboard, or even regenerate clean data files, ensuring the reproducibility of our analysis. 


## Team responsibilities
### Haeji
- Implemented initial filtering of ZORI data for SF zip codes (2020-2024)
- Built API pipeline to retrieve, filter, and save real-time SF eviction records
- Computed eviction rates by normalizing monthly evictions with census populations
- Led dashboard implementation to produce an interactive analytical tool
- Optimized map, plot, and regression code for dashboard interactivity

### Lily
- Developed clean_address and clean_parenthesis to de-duplicate 311 data, and initial cleaning functions for 311 and encampment datasets
- Created run_regression.py to conduct tract-level regression analysis
- Developed regression visualization to support data interpretation
- Built initial line graphs for encampments and street homeless population estimates
- Reviewed interpolation, imputation, and other data processing choices

### Amy
- Co-wrote script (with Amanda) to scrape shelter waitlist datasets (later archived)
- Implemented final cleaning functions for 311 and encampment datasets (Pandas)
- Built ingestion and cleaning pipeline for monthly median rent data: imputed missing ZORI values, processed 20 HUD crosswalk Excel files, and calculated weighted averages to generate tract-level monthly rent estimates
- Interpolated quarterly encampments to estimate monthly counts
- Built final line graphs for encampments and street homeless population estimates, and built line graphs for monthly median rent by ZIP code
- Assisted with dashboard by leading dashboard design and writing textual content

### Amanda
- Co-wrote script (with Amy) to scrape shelter waitlist datasets (later archived)
- Processed Census and ACS data to consolidate key metrics into tract-level outputs
- Implemented geospatial matching to assign point-based data (coordinates) to census tracts, and aggregated encampments and 311 data by month and census tract
- Built choropleth map with interactive tooltip to visualize key metrics across census tracts and time periods
- Built a command-line interface to streamline data processing and analysis workflows


## Final thoughts
Our project set out to examine the relationship between unsheltered homelessness and housing prices in SF from 2020–2024 at the census tract level. To better understand spatial patterns and drivers of homelessness, we incorporated additional datasets such as 311 calls and eviction records. We built a data pipeline to harmonize these sources, created visualizations to explore trends, and developed an interactive dashboard.

Our analysis revealed clear spatial concentrations of homelessness in the Tenderloin and the Mission (areas well known for homelessness). Interestingly, it also suggested a gradual shift further south into India Basin and Bayview-Hunters Point (areas not typically associated with homelessness), with a growing proportion of individuals living in vehicles rather than tents. This shift may reflect recent encampment sweeps in central neighborhoods, which may have displaced individuals toward southern areas and contributed to increases in vehicle-based homelessness. Regression analysis also found a correlation between higher citizen-reported encampments (311 service calls) and tracts with larger White populations. 

Beyond these findings, this project strengthened our technical and analytical skills, including data retrieval, cleaning, spatial analysis, and visualization. Overall, it helped us consolidate these skills while producing analyses related to real-world issues.