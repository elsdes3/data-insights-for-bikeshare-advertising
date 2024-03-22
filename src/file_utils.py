#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Define utilities to work with files."""

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals,unused-argument,unnecessary-lambda


import os
import shutil
from datetime import datetime

import pandas as pd
import pytz
import requests

import datetime_utils as dtu


def download_file(url: str, raw_data_dir: str) -> str:
    """."""
    local_filepath = os.path.join(raw_data_dir, url.split("/")[-1])
    fpath_full = os.path.abspath(local_filepath)
    if not os.path.exists(local_filepath):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded data from {url} to {fpath_full}")
    else:
        print(f"Found file at {fpath_full}. Did nothing.")
    return local_filepath


def download_zip_file(raw_data_dir: str, url: str) -> str:
    """."""
    url_fname = os.path.basename(url)
    zip_filepath = os.path.join(raw_data_dir, os.path.splitext(url_fname)[0])
    if not os.path.exists(zip_filepath):
        extracted_dir = os.path.join(
            raw_data_dir, os.path.splitext(url_fname)[0]
        )
        if not os.path.exists(extracted_dir):
            shp_file_fpath = os.path.join(raw_data_dir, url_fname)
            r = requests.get(url)
            with open(shp_file_fpath, "wb") as f:
                f.write(r.content)
        if not os.path.exists(extracted_dir):
            zip_file_fpath_destination = os.path.join(raw_data_dir, url_fname)
            shutil.unpack_archive(zip_file_fpath_destination, zip_filepath)
        print(f"Retrieved geodata & saved to {os.path.abspath(zip_filepath)}")
    else:
        print(
            f"Found existing geodata at {os.path.abspath(zip_filepath)}. Did "
            "not download."
        )
    return zip_filepath


def load(
    df: pd.DataFrame,
    data_dir: str,
    data_type: str,
    my_timezone: str = "America/Toronto",
    verbose: bool = False,
) -> None:
    """."""
    dtime_now = datetime.now(tz=pytz.timezone(my_timezone))
    fpath = os.path.join(
        data_dir,
        (
            f"{data_type}__"
            f"{dtu.dtime2str(dtime_now, '%Y%m%d_%H%M%S')}.parquet.gzip"
        ),
    )
    df.to_parquet(fpath, compression="gzip", index=False, engine="pyarrow")
    if verbose:
        print(
            f"Exported {len(df):,} rows of {data_type} data to "
            f"{os.path.abspath(fpath)}"
        )
