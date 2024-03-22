#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Define utilities to retrieve datasets from Toronto Open Data."""

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals,unused-argument,unnecessary-lambda


from typing import Dict

import pandas as pd
import requests


def get_open_data_package_resources(
    base_url: str, params: Dict[str, str]
) -> pd.DataFrame:
    """."""
    url = base_url + "/api/3/action/package_show"
    package = requests.get(url, params=params).json()
    df = pd.DataFrame.from_records(package["result"]["resources"])
    return df


def download_geo_open_data(
    raw_data_dir: str, base_url: str, params: Dict[str, str]
) -> str:
    """Download geodata if not found locally."""
    ds_name = list(params.values())[0]
    df = get_open_data_package_resources(base_url, params)
    # filters = "(format == 'SHP') & (~name.str.contains('historical'))"
    filters = (
        "(name.str.endswith('4326.geojson') & "
        "(~name.str.contains('historical')))"
    )
    filepath = df.query(filters).iloc[0]["url"]
    print(f"Retrieved dataset {ds_name} from filepath {filepath}")
    return filepath
