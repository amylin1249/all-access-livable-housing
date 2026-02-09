import sys
import lxml.html
import httpx
import time
import json
import datetime

REQUEST_DELAY = 0.5


def get_data(
    starting_url="https://data.sfgov.org/api/archival.csv?id=w4sk-nq57&version=4867&method=export",
):
    """
    This function takes a URL to a page of parks and returns a
    list of URLs to each park on that page.

    Parameters:
        * url:  a URL to a page of parks

    Returns:
        A list of URLs to each park on the page.
    """
    url = starting_url
    # current version number Feb 8 2026
    version = 4867

    # total counts of people on waitlist in any given month
    counts_per_month = {}

    # number of days that had data for any given month
    days_per_month = {}

    # oldest version number July 5 2024
    while version >= 4286:
        time.sleep(REQUEST_DELAY)
        resp = httpx.get(url)
        # split data into rows
        data = resp.text.split("\n")[1:-1]
        # grab yyyy-mm for current file
        date = data[1][-24:-17]
        # issue with timeout error
        if date != "":
            counts_per_month[date] = counts_per_month.get(date, 0) + len(data)
            days_per_month[date] = days_per_month.get(date, 0) + 1
        url = url.replace(f"version={version}", f"version={version - 1}")
        version -= 1


# def scrape_page(url):
#     """
#     This function takes a URL to a park page and returns a
#     dictionary with the title, address, description,
#     and history of the park.

#     Parameters:
#         * url:  a URL to the page

#     Returns:
#         A dictionary with the following keys:
#             * url:          the URL of the park page
#             * name:         the name of the park
#             * address:      the address of the park
#             * description:  the description of the park
#             * history:      the history of the park
#     """
#     ### TBD - if we want to create a cache directory (similar to PA1)
#     ### TBD - if we want to check if URL starts with an allowed domain name

#     # Make HTTP request to server
#     time.sleep(REQUEST_DELAY)
#     resp = httpx.get(url)

#     response = make_request(url)
#     root = lxml.html.fromstring(response.text)

#     # Extract park name, address, and description from the park page
#     park_name = root.cssselect("div.page-title h2")[0]
#     park_address = root.cssselect("p.address")[0]
#     park_description = root.xpath(
#         "//h3[contains(text(), 'Description')]/following-sibling::div"
#     )[0]

#     # Extract park history only if it has a history section
#     if len(root.xpath("//h3[contains(text(), 'History')]")) == 0:
#         park_history = ""
#     else:
#         history = root.xpath(
#             "//h3[contains(text(), 'History')]/following-sibling::div"
#         )[0]
#         park_history = history.text_content()

#     park_data = {
#         "url": url,
#         "name": park_name.text_content(),
#         "address": park_address.text_content(),
#         "description": park_description.text_content(),
#         "history": park_history,
#     }

#     return park_data


# parks_json = make_request(url).json()

# for park in parks_json["parks"]:
#     park_rel_url = "/parks/" + str(park["id"])
#     park_urls.append(make_link_absolute(park_rel_url, url))

# return park_urls

# def get_next_page_url(url):
#     """
#     This function takes a URL to a page of parks and returns a
#     URL to the next page of parks if one exists.

#     If no next page exists, this function returns None.
#     """
#     parks_json = make_request(url).json()
#     parks_next_page = parks_json["next_page"]

#     if parks_next_page:
#         next_page_rel_url = "?page=" + parks_next_page
#         next_page_url = make_link_absolute(next_page_rel_url, url)
#         return next_page_url
#     return None


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
