#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Define utilities to clean start and end station names."""

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals,unused-argument


from typing import List

import pandas as pd


def clean_status_station_names(
    df: pd.DataFrame, columns: List[str]
) -> pd.DataFrame:
    """Clean station names using Pandas."""
    for c in columns:
        df[c] = (
            df[c]
            .str.replace(" - SMART", "", regex=True)
            .str.replace(" SMART", "", regex=True)
            .str.replace("  SMART", "", regex=True)
            .str.replace(" -SMART", "", regex=True)
            .str.replace("WEST", "West", regex=True)
            .str.replace(r"\.", "", regex=True)
            .str.replace(r" \(Green P\)", "", regex=True)
            .str.replace(" Green P", "", regex=True)
            .str.replace(r"\.", "", regex=True)
            .str.replace(r"\?", "-", regex=True)
            .str.replace(r"–", "-", regex=True)
            .str.replace(r"GÃÃ´", "", regex=True)
            .str.replace(r"GÇô", "", regex=True)
            .str.replace(r"â", "", regex=True)
            .str.replace(r"GÃÃ", "", regex=True)
            .str.replace(r"GÇÖ", "", regex=True)
            .str.replace(r"\(West Side\)", "(West)", regex=True)
            .str.replace(
                r"York St / Lakeshore St W - South",
                r"York St / Lake Shore Blvd W",
                regex=True,
            )
            .str.replace("[^A-z0-9 / ]", "", regex=True)
            .str.replace("  ", " ")
            .str.rstrip("-")
            .str.strip()
            .str.replace("/", " / ")
            .str.replace("  ", " ")
            .str.replace("Lakeshore", "Lake Shore")
            .str.replace("King s", "Kings")
            .str.replace(" East Side", "")
            .str.replace(" West Side", "")
            .str.replace(" North Side", "")
            .str.replace(" South Side", "")
            .str.replace(" East", "")
            .str.replace("/ern Ave", "Eastern Ave")
            .str.replace("W West", "W")
            # added
            .str.replace("(East ", "East")
            .str.replace("(West ", "West")
            .str.replace("(South ", "South")
            .str.replace("(North ", "North")
            .str.replace("(East", "East")
            .str.replace("(West", "West")
            .str.replace("(South", "South")
            .str.replace("(North", "North")
            .str.replace("(Allan ", "Allan")
            .str.replace("(Ferry ", "Ferry")
            .str.replace("(Bus ", "Bus")
            .str.replace("(City ", "City")
            .str.replace("(Hockey ", "Hockey")
            .str.replace("(Broadview ", "Broadview")
            .str.replace("(Queen ", "Queen")
            .str.replace("(Queens", "Queens")
            .str.replace("(Riverdale ", "Riverdale")
            .str.replace("(Wychwood ", "Wychwood")
            .str.replace("(Dufferin ", "Dufferin")
            .str.replace("(Marilyn ", "Marilyn")
            .str.replace("(Green ", "Green")
            .str.replace("(High ", "High")
            .str.replace("(Sheridan ", "Sheridan")
            .str.replace("(Yonge ", "Yonge")
            .str.replace("(1010 ", "1010")
            .str.replace("(Greenwood ", "Greenwood")
            .str.replace("(Sandown ", "Sandown")
            .str.replace("(Leslie ", "Leslie")
            .str.replace("(Jane ", "Jane")
            .str.replace("(Highland ", "Highland")
            .str.replace("(Rouge ", "Rouge")
            .str.replace("(Glendon ", "Glendon")
            .str.replace("(Eglinton ", "Eglinton")
            .str.replace("(Harbord ", "Harbord")
            .str.replace("(Atlantic ", "Atlantic")
            .str.replace("(Arena ", "Arena")
            .str.replace("(Monarch ", "Monarch")
            .str.replace("(Love ", "Love")
            .str.replace("(Aberfoyle ", "Aberfoyle")
            .str.replace("(Martin ", "Martin")
            .str.replace("(TMU", "TMU")
            .str.replace("Quay(Billy ", "Quay Billy ")
            .str.replace("QuayBilly ", "Quay Billy ")
            .str.replace("(1", "1")
            .str.replace("(2", "2")
            .str.replace("(5", "5")
            .str.replace("PBSCOPS", "")
            .str.replace(" - SMART", "")
            .str.replace("  ", " ")
            .str.replace(". ", " ")
            .str.replace(")", "")
            .str.replace(" 1", "")
            .str.replace(" 2", "")
        )
    return df
