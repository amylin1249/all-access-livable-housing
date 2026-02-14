import sys
import lxml.html
import httpx
import time
import json
import datetime

REQUEST_DELAY = 1
EXPORT_URL_TEMPLATE = "https://data.sfgov.org/api/archival.csv?id=w4sk-nq57&version=VERSION&method=export"
API_URL = "https://data.sfgov.org/api/publishing/v1/revision/w4sk-nq57/changes?cursor="


def get_data():
    """
    ADD DOCSTRING
    """
    export_url = EXPORT_URL_TEMPLATE
    next_page_url = API_URL

    # Total counts of people on waitlist in any given month
    counts_per_month = {}

    # Number of days that had data for any given month
    days_per_month = {}

    # Dummy value to ensure shelters_next_page is not 0 and will run in while loop
    shelters_next_page = 1

    while shelters_next_page:
        # Access first page of hidden API (i.e., most recent records)
        time.sleep(REQUEST_DELAY)
        shelters_json = httpx.get(API_URL).json() ### SHOULD WE CREATE CACHE SINCE THIS IS REPEATED ACROSS BOTH FUNCTIONS?

        # Get key fields of each record (i.e., counts per day)
        for record in shelters_json["resource"]:
            version = record["value"]["version"]
            year_month = record["value"]["created_at"][:7]
            export_url = EXPORT_URL_TEMPLATE.replace("VERSION", version)

            time.sleep(REQUEST_DELAY)
            export_resp = httpx.get(export_url)

            # Split data into rows, excluding header and last blank row
            data = export_resp.text.split("\n")[1:-1]

            # HAVEN'T ACCOUNTED FOR TIMEOUT ERRORS YET
            counts_per_month[year_month] = counts_per_month.get(year_month, 0) + len(data)
            days_per_month[year_month] = days_per_month.get(year_month, 0) + 1
    
        # Check if next page exists -- not using helper function yet
        shelters_next_page = shelters_json["meta"]["next"]

        if shelters_next_page:
            next_page_url = next_page_url + shelters_next_page

    return counts_per_month, days_per_month


def get_next_page_url(url):
    """
    This function takes a URL to a page of shelter information (incl. version
    number and date) and returns a URL to the next page if one exists.

    If no next page exists, this function returns None.
    """
    pass


### OLD FUNCTION WE WROTE
# def get_data(
#     starting_url="https://data.sfgov.org/api/archival.csv?id=w4sk-nq57&version=4867&method=export",
# ):
#     """
#     """
#     url = starting_url
#     # current version number Feb 8 2026
#     version = 4867

#     # total counts of people on waitlist in any given month
#     counts_per_month = {}

#     # number of days that had data for any given month
#     days_per_month = {}

#     # oldest version number July 5 2024
#     while version >= 4286:
#         time.sleep(REQUEST_DELAY)
#         resp = httpx.get(url)
#         # split data into rows
#         data = resp.text.split("\n")[1:-1]
#         # grab yyyy-mm for current file
#         date = data[1][-24:-17]
#         # issue with timeout error
#         if date != "":
#             counts_per_month[date] = counts_per_month.get(date, 0) + len(data)
#             days_per_month[date] = days_per_month.get(date, 0) + 1
#         url = url.replace(f"version={version}", f"version={version - 1}")
#         version -= 1


# NEED TO MODIFY THIS
if __name__ == "__main__":
    """
    Tip: It can be convenient to add small entrypoints to submodules
         for ease of testing.

    In this file, we call scrape_park_page with a given URL and pretty-print
    the output.

    This allows testing that function from the command line with:

    $ python -m parks.crawler https://scrapple.fly.dev/parks/4

    Feel free to modify/change this if you wish, you won't be graded on this code.
    """
    from pprint import pprint

    if len(sys.argv) != 2:
        print("Usage: python -m parks.crawler <url>")
        sys.exit(1)
    result = scrape_park_page(sys.argv[1])
    pprint(result)
