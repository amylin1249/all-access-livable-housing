# All Access Livable Housing

## Abstract

Several cities in the United States are experiencing a homelessness crisis, with San Francisco often cited due to its high housing prices and limited housing supply. Our project aims to examine the relationship between the count of unsheltered persons and housing prices in San Francisco from 2019 to 2023 at the census tract level. Specifically, we aim to compare monthly estimates of unsheltered individuals with average monthly rent, both of which require interpolation and estimation to obtain sufficiently granular, temporal data.

Building on the city’s publicly available encampment location data, we will use statistical methods to integrate quarterly structure-based counts with monthly aggregates of homelessness-related 311 service requests and monthly shelter waitlist totals to generate tract-level monthly estimates of unsheltered homelessness. To obtain monthly rental price estimates, we plan to use ACS 5-year average rent data to establish baseline neighborhood rent levels and combine them with monthly Zillow Observed Rent Index data at the ZIP code level.

Overall, our project will have a strong focus on spatial analysis and mapping, visualizing the relationship between encampments, rent prices, and demographics across neighborhoods. We aim to further complement this analysis with a simulation component to explore how homelessness or encampment counts may potentially change based on changes in housing prices or economic pressures.

## Data Sources

### Data Source #1: DataSF Open Data Portal
#### Data Source #1.1: 311 Cases
Source URL: https://data.sfgov.org/City-Infrastructure/311-Cases/vw6y-z8j6/about_data
Source Type: Bulk data
Approximate Number of Records (rows): 210,804 (Filtered for category: encampment and encampments and dates: 2019-2023)
Approximate Number of Attributes (columns): 25
Current Status: We have downloaded and explored the data -- this one gives us 311 service calls with a specific date of the call and a location of the call (latitude/longitude). We will need to aggregate it by month, which should be simple. 
Challenges: There could be reporting bias (vs. official counts), since this data reflects citizen reporting behavior rather than a verified census. This may lead to higher densities in neighborhoods where residents are more likely to report issues, which might not perfectly align with the actual distribution of the unhoused population. There could also be issues with duplication, as multiple people could call for the same incident. Unfortunately, these challenges are unavoidable, but we still want to include this dataset in order to make sure our estimation of homelessness in SF is as accurate as possible, as there is always a risk of undercounting the population (so potential duplication can, in a way, counterbalance the undercounting).

#### Data Source #1.2: Quarterly count of tents, structures, and lived-in vehicles
Source URL: https://app.powerbigov.us/view?r=eyJrIjoiY2FmZDNiY2ItMjA2OS00YjU5LWFkMDUtODlkNTgyZmQ3MmNhIiwidCI6IjIyZDVjMmNmLWNlM2UtNDQzZC05YTdmLWRmY2MwMjMxZjczZiJ9
Source Type: Webscraping
Approximate Number of Records (rows): 20
Approximate Number of Attributes (columns): TBD (see explanation below)
Current Status: This map shows the location of different encampments in SF on a quarterly basis. We were initially planning to use what is allegedly the underlying dataset for this map (https://data.sfgov.org/Housing-and-Buildings/Quarterly-count-of-tents-structures-and-lived-in-v/w9ip-yrij/about_data), but it actually only has data from 2024 and 2025 (despite the map clearly having data from April 2019 through Dec 2025). Now, we will have to extract this historical encampment data by webscraping JSON responses from Power BI network traffic. We know there are 20 quarterly time points between our target range of 2019 to 2023, but the number of attributes is unknown at this point since each scrape of the website (20 in total) will have all of the latitudes and longitudes of the encampment locations as well as the type (tent vs. structure vs. large vehicle vs. small vehicle). This is exactly what we will need to extract to estimate the number of street homeless individuals in each census tract. 
Challenges: One challenge is the temporal mismatch between this dataset and the others. While the 311 service requests provide daily, high-frequency data, as do the shelter counts, the official tent counts are only released every three months (quarterly). This discrepancy means we will need to make a strategic decision about how to align the data, as failing to reconcile these different time scales could lead to inaccurate correlations between rising rents and homelessness counts. We plan to use statistical interpolation to estimate monthly trends. In addition, because the counts are based on the number of tents or structures rather than an individual census, there are inherent limitations in accurately estimating the actual size of the unhoused population.

#### Data Source #1.3: HSH Shelter Waitlist
Source URL: https://data.sfgov.org/Health-and-Social-Services/HSH-Shelter-Waitlist/w4sk-nq57/about_data
Source Type: API
Approximate Number of Records (rows): 426 (per day)
Approximate Number of Attributes (columns): 6
Current Status: We have explored the data -- this one in particular is updated every day with the current shelter waitlist. We will need to write code that loops through hundreds of daily API endpoints to systematically extract and consolidate the data.
Challenges: The primary technical challenge here is the high volume of API requests that we will need to make to reconstruct the historical trend. Fetching hundreds of individual files increases the risk of API rate-limiting and potential data gaps if certain daily files are missing or corrupted. In addition, since this data has no geographic fields, we will need to use the geographic distribution of the homeless population according to data sources 1.1 and 1.2 to estimate the shelter waitlist count for each census tract (so, some accuracy is lost through estimation).

### Data Source #2: Census Data
#### Data Source #2.1: ACS data on rental costs and demographic data
Source URL: https://data2.nhgis.org/main
Source Type: Bulk data
Approximate Number of Records (rows): 244 (filtered for census tracts in SF)
Approximate Number of Attributes (columns): >10, included census tract identifiers (GEOID), geographic coordinates (latitude, longitude), median gross rent by tract, total population by tract, racial composition breakdown by tract, household income measures by tract
Current Status: We have downloaded the relevant ACS datasets for our analysis. We will be using the 5-year estimate from 2019 to 2023. Apart from median rent which will be used as a proxy for housing prices, we have identified several demographic indicators such as population density, racial composition, and income levels to observe if they have any correlation with housing costs and homelessness counts across tracts. While we have these datasets available for use, we are still refining the structure of our analysis to determine how these demographic variables can complement homelessness indicators to provide more insights into the homelessness landscape in SF.
Challenges: While we do not have any major concerns about the data, the main challenge that we are currently facing is on how to spatially integrate different datasets. Census and ACS data are available at the tract level (identified by GEOIDs as well as their coordinates), while data from our other sources (e.g., encampment data) are often provided as observations with individual latitude and longitude coordinates. We plan to spatially match these point-based data to census tracts for tract-level comparison. We previously conducted similar matching using ArcGIS, but we will have to implement this in Python to integrate it with overall data cleaning, analysis, and visualization. 

#### Data Source #2.2: Listing and geographic boundaries of census tracts in SF
Source URL: https://data.sfgov.org/Geographic-Locations-and-Boundaries/Census-2020-Tracts-for-San-Francisco/tmph-tgz9/about_data
Source Type: Bulk data
Approximate Number of Records (rows): 244
Approximate Number of Attributes (columns): 15
Current Status: We will use this dataset to limit our analysis to the census tracts of San Francisco. 
Challenges: See above, data source #2.1.

### Data Source #3: Zillow Observed Renter Index (ZORI)
Source URL: https://www.zillow.com/research/data/
Source Type: Bulk data
Approximate Number of Records (rows): 23 (after filtering for San Francisco)
Approximate Number of Attributes (columns): 60 (after filtering for 2019-2023)
Current Status: We have explored this dataset -- it provides a monthly estimate of average rent in each zip code of SF. 
Challenges: One challenge is missing data. SF has over 40 zip codes, but this dataset only includes 23. In addition, certain months are missing for certain zip codes. The second challenge is that this dataset is at the zip code level, but we plan to do our overall analysis at the census tract level. We plan to reconcile this by combining the ACS data (which will provide one monthly rent estimate for each census tract over the 2019-2023 period) with this dataset (which provides a monthly rent estimate for each zip code for every month from 2019 to 2023), to overall get an estimate of the monthly rent in each census tract for every month from 2019 t0 2023. 

## Data Reconciliation Plan

Source 1.1 (311 calls): location = lat, long; date = requested_datetime
Source 1.2 (Tents): location = lat, long; date = quarterly
Source 1.3 (HSH shelter): date = data_as_of
Source 2 (ACS): location = GEOID
Source 3 (ZORI): location = RegionName; date = individual columns (there is a column for every month)

## Project Plan

1. Finish extracting all data. (Week 5)
- We currently have data sources 1.1, 2.1, 2.2, and 3 downloaded as CSV files.
- We will need to webscrape to get the data we need from 1.2. (Lily/Haeji)
- We will need to use get requests to get the data we need from 1.3. (Amy/Amanda)

2. Clean and process data across all sources, including addressing missing values and doing interpolations as needed to estimate locations and dates. (Week 6)
- Data source 1.1: This is daily data with specific latitudes/longitudes. We will need to aggregate it into monthly counts. (Amanda)
- Data source 1.2: This is quarterly data with specific latitudes/longitudes. We will need to interpolate it so that it is monthly. (Lily)
- Data source 1.3: This is daily data with no location. We will need to aggregate it into monthly counts and then estimate its geographic distribution based on data sources 1.2 and 1.3. (Haeji)
- Data sources 2.1 and 2.2: We need to combine these so that we have the census data for the census tracts specifically within SF. (Amanda)
- Data source 3: This is monthly data with zip code for location. We will need to combine it with data sources 2.1 and 2.2 to estimate its geographic distribution within census tracts. (Amy)

3. ⁠Integrate data sources via spatial joins, matching point-level data to SF census tracts. (Week 7) (Amanda/Amy)

4. ⁠Conduct statistical analysis to assess correlations between homelessness measures, housing prices, and demographic indicators across census tracts over time. (Week 7) (Lily/Haeji)

5. ⁠Develop a predictive or simulation model to examine potential changes in homelessness measures against changes in rent prices. (Week 8) (Amanda/Amy/Lily/Haeji)

6. ⁠Create map-based and time-series visualizations to communicate patterns and relationships in homelessness, housing costs, and demographics. (Week 9) (Amanda/Amy/Lily/Haeji)

## Questions

1. Getting what we need from data source #1.2 will probably be the most challenging part of this project. We wanted to double check with you that you also cannot find the raw dataset for the map dashboard (for 2019 to 2023) before we proceed with figuring out how to scrape the map. 