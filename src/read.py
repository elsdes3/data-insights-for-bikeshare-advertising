#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Define utilities to load station demand data."""

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals,unused-argument

import os
from typing import Dict, List, Union

import pandas as pd


def get_2020_data(
    period: str, fpath: str, dtypes: Dict, datetime_cols: List[str]
) -> pd.DataFrame:
    """Read bikeshare trips data from single month in 2020."""
    if int(period) in [10]:
        usecols = None
        parse_dates = None
        date_format = None
    else:
        usecols = None
        parse_dates = datetime_cols
        date_format = "%m/%d/%Y %H:%M"

    df = pd.read_csv(
        fpath,
        compression=None,
        encoding=None,
        engine="python",
        dtype=dtypes,
        usecols=usecols,
        parse_dates=parse_dates,
        date_format=date_format,
    )
    # for October 2020, columns were mis-aligned and to the datatypes & column
    # names need to be fixed (See above for details)
    if int(period) == 10:
        # filter data to only capture trips (rows) without mis-aligned columns
        df = df[df["Start Station Id"].str.len() <= 4]
        # set correct datatypes
        df = df.astype(
            {
                "Trip Id": pd.Int64Dtype(),
                "Start Station Id": pd.Int64Dtype(),
                "End Station Id": pd.Int64Dtype(),
                "Bike Id": pd.Int64Dtype(),
            }
        )
        # convert start and end time columns to datetime datatype
        end_col = "End Time"
        df[end_col] = pd.to_datetime(df[end_col], format="%m/%d/%Y %H:%M")
        df["Start Time"] = pd.to_datetime(
            df["Start Time"], format="%m/%d/%Y %H:%M"
        )
    return df


def get_read_csv_inputs(fpath: str) -> List[Union[str, int]]:
    """."""
    ym_file = os.path.splitext(os.path.basename(fpath))[0]
    if "2021" in ym_file or "2022" in ym_file or "2023" in ym_file:
        ym = ym_file.split(" ridership ")[-1]
        year, period = ym.split("-")
    elif "2018" in ym_file:
        yq = ym_file.split("Ridership_Q")[-1]
        period, year = yq.split(" ")
    elif "2020" in ym_file:
        year, period = ym_file.split("-")
    else:  # elif "2019" in ym_file:
        year, period = ym_file.split("-")
        period = period[1:]
    return [fpath, year, period]


def read_csv_file(
    fpath: str, year: str, period: str, datetime_fmt: str = "%m/%d/%Y %H:%M"
) -> pd.DataFrame:
    """Read single month of bikeshare trips data."""
    # Specify datatypes for columns in monthly bikeshare trips data, by year
    dtypes_trips = {
        "Trip Id": pd.Int64Dtype(),
        "Trip  Duration": pd.Int32Dtype(),
        "Start Station Id": pd.Int32Dtype(),
        "Start Station Name": pd.StringDtype(),
        "End Station Id": pd.Int64Dtype(),
        "End Station Name": pd.StringDtype(),
        "User Type": pd.StringDtype(),
        "Bike Id": pd.Int64Dtype(),
    }
    dtypes_2018_trips = {
        "trip_id": pd.StringDtype(),
        "trip_duration_seconds": pd.Int32Dtype(),
        "from_station_id": pd.Int32Dtype(),
        "from_station_name": pd.StringDtype(),
        "to_station_id": pd.StringDtype(),
        "to_station_name": pd.StringDtype(),
        "user_type": pd.StringDtype(),
    }
    dtypes_2020_trips = {
        m: (
            dtypes_trips
            if m not in [10]
            else {
                "Trip Id": pd.Int64Dtype(),
                "Trip  Duration": pd.Int64Dtype(),
                "Start Station Id": pd.StringDtype(),
                "Start Station Name": pd.StringDtype(),
                "End Station Id": pd.StringDtype(),
                "End Station Name": pd.StringDtype(),
                "User Type": pd.StringDtype(),
                "Bike Id": pd.StringDtype(),
            }
        )
        for m in range(1, 12 + 1)
    }
    dtypes_2021_trips = {
        m: (
            dtypes_trips
            if m in [1, 5]
            else {
                "ï»¿Trip Id": pd.Int64Dtype(),
                "Trip  Duration": pd.Int64Dtype(),
                "Start Station Id": pd.Int64Dtype(),
                "Start Station Name": pd.StringDtype(),
                "End Station Id": pd.Int64Dtype(),
                "End Station Name": pd.StringDtype(),
                "User Type": pd.StringDtype(),
                "Bike Id": pd.Int64Dtype(),
            }
        )
        for m in range(1, 12 + 1)
    }
    dtypes_2023_trips = {
        m: (
            {
                "ï»¿Trip Id": pd.Int64Dtype(),
                "Trip  Duration": pd.Int64Dtype(),
                "Start Station Id": pd.Int64Dtype(),
                "Start Station Name": pd.StringDtype(),
                "End Station Id": pd.Int64Dtype(),
                "End Station Name": pd.StringDtype(),
                "User Type": pd.StringDtype(),
                "Bike Id": pd.Int64Dtype(),
            }
            if m in [1]
            else dtypes_trips
        )
        for m in range(1, 12 + 1)
    }

    if year == "2020":
        datetime_cols = ["Start Time", "End Time"]
        df = get_2020_data(
            period, fpath, dtypes_2020_trips[int(period)], datetime_cols
        )
    else:
        # print(year)
        # select dtypes dictionary and python encoding based on year
        if year == "2021":
            dtypes = dtypes_2021_trips[int(period)]
            encoding = "unicode_escape"
            datetime_cols = ["Start Time", "End Time"]
        elif year in ["2019", "2022"]:
            dtypes = dtypes_trips
            encoding = None
            datetime_cols = ["Start Time", "End Time"]
        elif year == "2018":
            dtypes = dtypes_2018_trips
            encoding = None
            datetime_cols = ["trip_start_time", "trip_stop_time"]
        elif year == "2023":
            dtypes = dtypes_2023_trips[int(period)]
            encoding = "unicode_escape"
            datetime_cols = ["Start Time", "End Time"]
        # print(1)

        # read single month's bikeshare data
        df = pd.read_csv(
            fpath,
            # nrows=500,
            compression=None,
            encoding=encoding,
            engine="python",
            dtype=dtypes,
            usecols=None,
            parse_dates=datetime_cols,
            date_format=datetime_fmt,
        )
        # remove special characters from trip_id column in 2021
        if year in ["2021", "2023"]:
            df = df.rename(columns={"ï»¿Trip Id": "Trip Id"})
        # print(2)
    return df
