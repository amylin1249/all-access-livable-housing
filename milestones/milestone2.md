# All Access Livable Housing

## Abstract

{Update your project abstract from Milestone 1 with any changes.}

{ORIGINAL ABSTRACT}
Several cities in the US are experiencing a homelessness crisis, with San Francisco often cited due to its high housing prices and low supply. Our project aims to analyze homelessness patterns in San Francisco (and potentially the nearby cities of Oakland and Berkeley). 

Some questions we have are: 
-	How have homelessness rates changed in relation to housing prices over time?
-	Are there spatial patterns for where homeless encampments are located, especially compared with indicators like income levels, property values, and rent burden?
-	Are the locations and concentrations of homeless shelters aligned with encampments?
-	How have encampment locations shifted as the frequency of enforcement actions, like sweeps, increased?

Our project focus lends itself naturally to mapping. Since the city already publishes a map with the locations of encampments, we plan to use statistical analysis to improve the accuracy of estimates, and to pair these preexisting known locations with other relevant information (e.g., neighborhood composition, shelter locations). We want to include a time component, where the user could specify a date, and it will return multiple maps and relevant statistics. 

{NEW ABSTRACT IDEAS}
Finding the relationship between homelessness and housing prices, to demonstrate how the housing crisis has exacerbated homelessness in San Francisco. This one is pretty straightforward -- we would use the shelter waitlist size and tent locations/counts as a measure of homelessness and combine those with housing pricing data from the census (e.g., median rent) to see the relationship between the two. We'll also probably pull in demographic data. As you mentioned, there is an option for simulation here where we can see how changing one variable affects the others.
*** Also wanting to add in something about encampement volatility-how encampment locations shift over time in response to economic pressures or enforcement action.

## Data Sources

### Data Source #1: DataSF Open Data Portal
#### Data Source #1.1: 311 Cases
Source URL: {https://data.sfgov.org/City-Infrastructure/311-Cases/vw6y-z8j6/about_data}
Source Type: {API}
Approximate Number of Records (rows): 8,829(Filtered for category : encampment and encampments) 
Approximate Number of Attributes (columns): 25
Current Status: {Explored the data, GPS coordinates(lat/long) and address might be used as reconciliation key. Started writing an initial code to convert api into a Pandas DataFrameata.}
Challenges: {There could be reporting bias (vs. official counts), since this data reflects citizen reporting behavior rather than a verified census. This may lead to higher densities in neighborhoods where residents are more likely to report issues, which might not perfectly align with the actual distribution of the unhoused population. There could also be issues with duplication, as multiple people could call for the same incident. Also, the data provides provides specific GPS coordinates (lat/long), a major technical hurdle will be the spatial join required to aggregate these points into Census Tracts or Zip Codes to match from Zillow and the Census data.}

#### Data Source #1.2: Quarterly count of tents, structures, and lived-in vehicles
Source URL: {https://data.sfgov.org/Housing-and-Buildings/Quarterly-count-of-tents-structures-and-lived-in-v/w9ip-yrij/about_data}
Source Type: {API}
Approximate Number of Records (rows): 1,747
Approximate Number of Attributes (columns): 13
Current Status: {Explored the data, GPS coordinates(lat/long). Started writing a code to extract data. }
Challenges: {The most significant challenge is the temporal mismatch between datasets. While the 311 service requests provide daily, high-frequency data, the official tent counts are only released every three months (quarterly). This discrepancy requires a strategic data alignment approach; we must decide whether to aggregate the 311 and Zillow rental data into quarterly averages or use statistical interpolation to estimate monthly tent trends. Failing to reconcile these different time scales could lead to inaccurate correlations between rising rents and homelessness counts. Furthermore, because the counts are based on the number of tents or structures rather than an individual census, there are inherent limitations in accurately estimating the actual size of the unhoused population.}

#### Data Source #1.3: HSH Shelter Waitlist
Source URL: {https://data.sfgov.org/Health-and-Social-Services/HSH-Shelter-Waitlist/w4sk-nq57/about_data}
Source Type: {API}
Approximate Number of Records (rows): 426(per day)
Approximate Number of Attributes (columns): 6
Current Status: {Explored the data, which contains daily data. So, writing a loop scode that iterates through hundreds of daily API endpoints to systematically extract and consolidate the data.}
Challenges: {The primary technical challenge is the high volume of API requests required to reconstruct the historical trend. Fetching hundreds of individual files increases the risk of API rate-limiting and potential data gaps if certain daily files are missing or corrupted.}

[OLD INFO]
-	Summary: This data portal, published by the City of San Francisco, contains many datasets of interest. In particular, “311 Cases” provides a comprehensive list of 311 service calls (non-emergency municipal service requests) in SF, and there is a filtering category for “Encampments.” Because each call includes location (latitude and longitude), we will be able to map the calls to their respective tracts within the city. “Quarterly count of tents, structures, and lived-in vehicles” includes a quarterly count and locations of the tents, structures, and vehicles (both passenger + non-passenger) that seem to be lived in, which will enable us to analyze how their counts and locations have evolved over time, especially with external factors (e.g., raids). “HSH Shelter Waitlist” contains the current San Francisco adult shelter reservation waitlist. This dataset could be used to see trends in shelter demand. 
 

### Data Source #2: Census Data
Source URL: {https://...}
Source Type: {Scraped/Bulk Data/API}
Approximate Number of Records (rows):
Approximate Number of Attributes (columns): 
Current Status: {At this point, you should have interacted with your data, describe the current status. Have you written code for an API or web scraper yet, explored the data, etc.?}
Challenges: {Any challenges or uncertainty about the data at this point?}

[OLD INFO]
-	Summary: The National Historical Geographic Information System (NHGIS) is a popular source for census data. Usually going all the way down to the census tract, it includes demographic information and housing information, including median rent, median property value, and rent burden. It is published by IPUMS at the University of Minnesota.
-	Source URL: https://data2.nhgis.org/main
-	Source Type: Bulk data
-	Challenges: Since some of us have worked with census data before, we don’t have any major concerns about it. We will just need to be thoughtful about how we spatially join it to the other data that we have. 

### Data Source #3: Zillow Renter Index
Source URL: {https://...}
Source Type: {Scraped/Bulk Data/API}
Approximate Number of Records (rows):
Approximate Number of Attributes (columns): 
Current Status: {At this point, you should have interacted with your data, describe the current status. Have you written code for an API or web scraper yet, explored the data, etc.?}
Challenges: {Any challenges or uncertainty about the data at this point?}

[OLD INFO]
-	Summary: This is a smoothed measure of the typical observed market rate of rent across a given region. ZORI is a repeat-rent index that is weighted to the rental housing stock to ensure representativeness across the entire market, not just those homes currently listed for-rent. The index is dollar-denominated by computing the mean of listed rents that fall into the 35th to 65th percentile range for all homes and apartments in a given region, which is weighted to reflect the rental housing stock. It comes from Zillow.
-	Source URL: https://www.zillow.com/research/data/ 
-	Source Type: Bulk data
-	Challenges: The data is only available at the zip code level, which may not be granular enough for our analysis. In addition, it is only an approximation of rental price over a band. Alternatively, we may scrape rental data from Zillow to get a neighborhood index of renter affordability and develop a clearer sense of the rental price distribution. 

## Data Reconciliation Plan

One of the most important steps for this milestone is to have a plan as to how your data sources will connect.

For each data set, you will need to identify the "unique key" that will allow you to connect it to other data sets.
- key
1.1 311 : address, street, supervisor district, neighbor, police district, lat, long
1.2 quarterly : observed month, police district, lat/long
1.3 HSH shelter : x (useing for the total num of size)

Example 1: You have two data sets: healthcare costs on a zip code level & employment figures on a county level. You will need to determine a mapping between zip code & county. You aren't sure how you'll go about joining them-- figuring that gap out now helps us identify that this will require a third data set available from the US Census so you can plan accordingly.

Example 2: You have three data sets: a list of companies that were fined for illegal emissions, a list of companies that have government contracts, and a list of company addresses. You identify that there won't be a perfect match between the three data sets, but you will need to put some effort into matching irregularly formatted company names.

## Project Plan

The final goal of this milestone is to develop a team plan that will keep you on track for the remainder of the quarter.

1. Identify the key components of your project based on the criteria and your intended end result. (e.g. "Web scrape data source #1", "Merge code for Data Sources #2 and #3", "Map-based visualization")
- API-based Data Extraction and Consolidation (Data Source #1.1,#1.2,#1.3)
- Temporal Resampling & Data Normalization(data scales match)
- Data Integration & Alignment
- Map-based Visualization
- Encampment Volatility Mapping
- Cross-Variable Correlation Modeling
- Predictive Simulation Analysis

2. For each component identify who will be responsible, and when it should be ready. Consider if any components rely on others and how to mitigate the effect on the dependent team members (e.g. mock data for the visualization until the real data is ready)
3. Put this together into a (rough) weekly plan. What will be built by Week 7's prototype? 

## Questions

1. Help with statistical analysis
2. Help with Zillow or other place to get rental data
