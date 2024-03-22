#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Define utilities to work with geodata."""

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals,unused-argument,unnecessary-lambda


from typing import List

import geopandas as gpd
import pandas as pd


def get_neighbourhood_containing_point(
    gdf: gpd.GeoDataFrame,
    df: pd.DataFrame,
    lat: str = "Latitude",
    lon: str = "Longitude",
    crs: int = 4326,
) -> gpd.GeoDataFrame:
    """Get name of Toronto neighbourhood containing a point co-ordinate."""
    cols_order = list(df) + list(gdf)
    polygons_contains = (
        gpd.sjoin(
            gdf,
            gpd.GeoDataFrame(
                df, geometry=gpd.points_from_xy(df[lon], df[lat]), crs=crs
            ),
            predicate="contains",
        )
        .reset_index(drop=True)
        .drop(columns=["index_right"])[cols_order]
    )
    print("Extracted neighbourhood name.")
    return polygons_contains


def get_data_with_neighbourhood(
    gdf: gpd.GeoDataFrame,
    df: pd.DataFrame,
    lat: int,
    lon: int,
    col_to_join: str,
    cols_to_keep: List[str],
    id_col: str,
    crs: int = 4326,
) -> gpd.GeoDataFrame:
    """Add city neighourhood name to bikeshare data."""
    df_check = get_neighbourhood_containing_point(gdf, df, lat, lon, crs)[
        cols_to_keep
    ]
    df = df.merge(
        df_check.drop(columns=["geometry"]), on=col_to_join, how="left"
    )
    df = df.dropna(subset=[id_col])
    num_dropped_rows = df[id_col].isna().sum()
    print(
        f"Dropped {num_dropped_rows} rows with a missing {id_col} "
        "(geodata) column"
    )
    print("Added geodata to data.")
    return df
