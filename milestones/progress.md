# Research on homeless estimates
(Haeji) 2024 SF point-in-time counts -- mentions that families tend to live in vehicles while singles live in tents
-- defined weighting logic -- Established conservative multipliers for unsheltered populations: Families (Vehicles): 2.1 persons per vehicle (Conservative vs. 2.72 estimate dactual average-Based on 2024 PIT data: 1,103 persons across 405 families); Singles (Tents/Structures): 1.1 persons per unit (Accounting for primarily single occupancy with minimal overlap)-> Justification: Using lower multipliers ensures the model remains robust against overestimation while acknowledging different living patterns between families and singles

## Data Sources

### Data Source #1: DataSF Open Data Portal
#### Data Source #1.1: 311 Cases
(Lily) cleaned and standardized the 311 cases into named tuples. 
(Lily) preliminarily matched 311 cases to encampment tuples by neighborhood and date. 

#### Data Source #1.2: Quarterly count of tents, structures, and lived-in vehicles
(Amy) email with bryan.v.wong@sfgov.org on 02/09/2026 - trying to get access to underlying dataset for map, rebumped on 02/15/2026
(Amy) tried to webscrape map directly, can go Network --> largest querydata file, but access issues to direct url

#### Data Source #1.3: HSH Shelter Waitlist
(Amy) email with HSHSunshine@sfgov.org on 02/09/2026 - trying to get access to archives past July 5, 2024
request formally submitted 02/10/2026 - follow-up from department required by 02/19/2026 
(Amy/Amanda) wrote code that scrapes the archives, functional aside from when loading a webpage takes too long - emailed James 02/09/2026
(Amanda) updated code to use the method that gets the date and version number of each (daily) dataset from a hidden API, instead of manually extracting start/end version numbers and changing version numbers as we iterate through. issue persists where the data is not downloaded if loading the webpage takes too long after we run the code

### Data Source #2: Census Data
#### Data Source #2.1: ACS data on rental costs and demographic data 
(Amanda) download done -- downloaded ACS data for 2020-24 5-year period for population, rent, household income, and race; uploaded data (specifically for San Francisco county) in the data/census folder
(Amanda) wrote code to clean and extract data from the relevant column for each ACS dataset
(Amanda) wrote code on quadtrees (mainly from PA 4) to match points to census tracts; slight changes from PA 4 to store match output as a dictionary instead of a tuple, and changed to SF bounding box 
(Amanda) started visualization of map of SF tracts (mainly used code from Lab 3 on GIS) and scatter plot; to be further improved and re-evaluated post-visualizations class to make them interactive

#### Data Source #2.2: Listing and geographic boundaries of census tracts in SF
(Amanda) download done -- downloaded SF 2020 census tracts
(Amanda) wrote code to combine ACS data for each SF census tract
(Amanda) wrote code to filter Califonia shapefiles for SF-specific shapefiles
(Amanda) wrote code to add SF ACS data (in CSV) as attributes in SF shapefiles

### Data Source #3: Zillow Observed Renter Index (ZORI)
(Haeji) download done --  downloaded ZORI zip-level data
(Haeji) wrote code to filter and clean -- isolated 23 San Francisco ZIP codes and filtered time series for the 2020-2024 period
(Haeji) wrote code to reshape and match -- reshaped wide-format data into long-format (melted) to support time-series analysis
(Haeji) completed data architecture -- developed `zori_filter.py` to auto-generate both a cleaned CSV file and a `rent_dict` {month: (zip, rent)} for seamless merging with homeless datasets.

## Data Source #4: 
(Lily) downloaded the Historical Tent Counts excel file data
(Lily) wrote cleaning code to standardize the encampment data into named tuples and prepped data for 311 data match.

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