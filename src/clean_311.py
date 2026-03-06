import csv
import sys
import pandas as pd
import numpy as np
import geopandas as gpd
from typing import NamedTuple
from pathlib import Path
from openpyxl import load_workbook
from datetime import datetime
import jellyfish
import math


def clean_parenthesis(name):
    """
    This function takes a name and removes any parenthesized portion.

    Returns:
        A string with parenthesized portion removed.
    """

    name = name.replace("(", "*(")
    name = name.replace(")", ")*")

    split_name = name.split("*")
    output_list = []

    for word in split_name:
        if word == "":
            continue
        elif word[0] != "(" and word[-1] != ")":
            output_list.append(word.strip())
    return " ".join(output_list)


STOPWORDS = [
    "st",
    "street",
    "av",
    "avenue",
    "ave",
    "av",
    "blvd",
    "boulevard",
    "rd",
    "road",
    "ln",
    "lane",
    "dr",
    "drive",
    "ct",
    "court",
    "pkwy",
    "parkway",
    "dr",
    "drive",
    "ter",
    "terrace",
    "cir",
    "circle",
    "pl",
    "place",
    "stwy",
    "a",
    "an",
    "and",
    "&",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
    "park",
    "parks",
    "intersection",
]

PUNCTUATION = ".,?-#/()[]"


def clean_address(address):
    address = address.lower()
    address = address.replace("i poi", "")
    address = clean_parenthesis(address)
    text_data = address.split(" ")
    cleaned_list = [word.strip(PUNCTUATION) for word in text_data]
    cleaned_list = [word for word in cleaned_list if word != ""]
    cleaned_list = [word for word in cleaned_list if word not in STOPWORDS]
    return " ".join(cleaned_list)


class EncampmentReport(NamedTuple):
    year: int
    month: int
    address: str
    lat: float
    lon: float


REPORT_PATH = Path(__file__).parent.parent / "raw-data" / "311_cases.csv"


def clean_311():

    file_input = REPORT_PATH

    with open(file_input, newline="") as csvfile:
        """
        Given a CSV containing 311, return a list of Encampment report objects.
        """
        lat_lon_dict = {}
        output_report = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            ### Clean the date ####
            datetime_str = row.get("Opened").replace(" PM", "")
            datetime_str = datetime_str.replace(" AM", "")
            datetime_object = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")
            date_year = datetime_object.year
            date_month = datetime_object.month
            if row["Latitude"] == "":
                lat = 0
            else:
                lat = float(row["Latitude"])

            if row["Longitude"] == "":
                lon = 0
            else:
                lon = float(row["Longitude"])

            address = clean_address(row.get("Address"))
            tuple_out = EncampmentReport(date_year, date_month, address, None, None)
            key = tuple_out
            if key not in lat_lon_dict:
                lat_lon_dict[key] = []
                lat_lon_dict[key].append((lat, lon))

            output_report.append(tuple_out)

    return output_report, lat_lon_dict


def attach_lat_lon(output_report, lat_lon_dict):
    unique_list = set(output_report)
    output = []
    for tuple_report in list(unique_list):
        lat_lon = lat_lon_dict[tuple_report]

        lat = sum(loc[0] for loc in lat_lon if loc[0] != 0) / len(lat_lon)
        lon = sum(loc[1] for loc in lat_lon if loc[1] != 0) / len(lat_lon)

        tuple_out = EncampmentReport(
            tuple_report.year, tuple_report.month, tuple_report.address, lat, lon
        )
        output.append(tuple_out)
