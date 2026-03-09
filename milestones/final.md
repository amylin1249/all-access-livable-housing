# Project: All Access Livable Housing

## Members

- Haeji Ahn <ahaeji925@uchicago.edu>
- Lily Hoffman <lshoffman@uchicago.edu>
- Amy Lin <amsylin@uchicago.edu>
- Amanda Song <amandasong@uchicago.edu>


## Data Documentation
List the sources of data, any gaps or challenges in the data. Explain how data flows through the project. What else would someone picking this project up for the first time need to understand?


## Project Structure
Write a page or so describing the structure of your project. What modules exist? What do they do? A diagram may be helpful here.



## Team responsibilities

### Haeji
- 

### Lily
- 

### Amy
- 

### Amanda
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
