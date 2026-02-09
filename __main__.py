import json
import sys
import pathlib
from .crawler import scrape_park_page, get_park_urls, get_next_page_url
from .cleanup import normalize_address, clean_name, tokenize


def crawl(max_pages):
    """
    This function starts at a base URL for the parks site and
    crawls through each page of parks, scraping each park page
    and saving output to a file named "parks.json".

    Hint: Once you discover the first page of API results, you may hard-code
    that URL in this function.

    Parameters:
        * max_pages:  the maximum number of pages to crawl
    """
    start_url = "https://scrapple.fly.dev/parks-list"

    parks = []
    pages_crawled = 0

    # Loop to crawl through and scrape park pages until all pages are scraped
    # or the maximum page limit is reached
    while start_url:
        for park_url in get_park_urls(start_url):
            parks.append(scrape_park_page(park_url))
            pages_crawled += 1

            # Break out of for loop if it reaches the maximum page limit
            if pages_crawled == max_pages:
                break

        # Break out of while loop if it reaches the maximum page limit;
        # otherwise, start_url is reset to scrape more park pages
        if pages_crawled == max_pages:
            break
        start_url = get_next_page_url(start_url)

    with open("parks.json", "w") as f:
        json.dump(parks, f, indent=1)


def clean():
    """
    This function loads the parks.json file and writes a new file
    named normalized_parks.json that contains a normalized version
    of the parks data.
    """
    with open("parks.json") as f:
        parks_data = json.load(f)

    # Normalize park addresses, add park tokens before normalizing park names
    for park in parks_data:
        park["address"] = normalize_address(park["address"])
        park["tokens"] = tokenize(park)
        park["name"] = clean_name(park["name"])

    with open("normalized_parks.json", "w") as f:
        json.dump(parks_data, f, indent=1)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        max_pages = int(sys.argv[1])
    else:
        max_pages = 1000

    # check if parks.json exists and prompt to delete
    parks_json = pathlib.Path("parks.json")
    if parks_json.exists():
        print("parks.json already exists. Rescrape? [y/n]")
        if input().lower() == "y":
            crawl(max_pages)
    else:
        crawl(max_pages)

    print("Cleaning parks.json and writing to normalized_parks.json")
    clean()
