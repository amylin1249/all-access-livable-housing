# Project: All Access Livable Housing

## Members

- Haeji Ahn <ahaeji925@uchicago.edu>
- Lily Hoffman <lshoffman@uchicago.edu>
- Amy Lin <amsylin@uchicago.edu>
- Amanda Song <amandasong@uchicago.edu>


## Abstract

Several cities in the United States are experiencing a homelessness crisis, with San Francisco often cited due to its high housing prices and limited housing supply. Our project examines the relationship between the count of unsheltered persons and housing prices in San Francisco from 2020 to 2024 at the census tract level. Specifically, we compare monthly estimates of unsheltered individuals with average monthly rent, both of which require interpolation and estimation to obtain sufficiently granular, temporal data.

Building on the city’s publicly available encampment location data, we use statistical methods to integrate quarterly structure-based counts with monthly aggregates of homelessness-related 311 service requests and eviction rates to generate tract-level monthly estimates of unsheltered homelessness. To obtain monthly rental price estimates, we use ACS 5-year average rent data to establish baseline neighborhood rent levels and combine them with monthly Zillow Observed Rent Index data at the ZIP code level.

Overall, our project has a strong focus on spatial analysis and mapping, visualizing key homelessness-related metrics across tracts for selected time periods through a heatmap, as well as the relationship between encampments, rent prices, and demographics across tracts.


## Screenshot of project



## Instructions to our project 
1. Clone our repository by running git clone <SSH> in your terminal.
2. After cloning the repository, run `uv sync` in the project root directory to install the required packages and set up the virtual environment.
3. *[Optional -- these files should already be included in the repository]* To retrieve API data and regenerate the clean data files, run `uv run python -m src --data` in the root directory. This will take around 3 minutes to run.
4. To launch our interactive dashboard and visualizations, run `uv run python -m src --dashboard` in the root directory.
5. Copy the Dash URL printed in the terminal and paste it into your web browser to view the dashboard.


## Citations for data sources

### Data Source #1: DataSF Open Data Portal
#### Data Source #1.1: 311 Cases
- https://data.sfgov.org/City-Infrastructure/311-Cases/vw6y-z8j6/about_data

#### Data Source #1.2: Quarterly count of tents, structures, and lived-in vehicles
- https://app.powerbigov.us/view?r=eyJrIjoiY2FmZDNiY2ItMjA2OS00YjU5LWFkMDUtODlkNTgyZmQ3MmNhIiwidCI6IjIyZDVjMmNmLWNlM2UtNDQzZC05YTdmLWRmY2MwMjMxZjczZiJ9
- Put in an offline email request and obtained a spreadsheet of historical tent counts from Apr 2019 to Dec 2025 that serves as the underlying dataset for the map 

#### Data Source #1.3: Evictions data
- https://data.sfgov.org/Housing-and-Buildings/Eviction-Notices/5cei-gny5/about_data

#### Data Source #1.4: HSH Shelter Waitlist (archived)
- https://data.sfgov.org/Health-and-Social-Services/HSH-Shelter-Waitlist/w4sk-nq57/about_data

### Data Source #2: Census Data
#### Data Source #2.1: ACS data on rental costs and demographic data
- https://data2.nhgis.org/main (2020-24 ACS 5-year data for population, median rent, median household income, racial composition, and number of renter households by tract)

#### Data Source #2.2: Listing and geographic boundaries of census tracts in SF
- https://data.sfgov.org/Geographic-Locations-and-Boundaries/Census-2020-Tracts-for-San-Francisco/tmph-tgz9/about_data (to obtain SF census tract IDs)
- https://www.census.gov/cgi-bin/geo/shapefiles/index.php (California census tracts shapefiles)

### Data Source #3: Zillow Observed Renter Index (ZORI)
- https://www.zillow.com/research/data/

### Data Source #4: HUD Crosswalks
- https://www.huduser.gov/portal/datasets/usps_crosswalk.html


## Project video
<Insert link to project video>


## Acknowledgments
Many thanks to our CAPP122 instructor, James Turk, and our assigned TA, Andrés Camacho, for their support and guidance.
