#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Define utilities to work with DataFrames."""

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals,unused-argument

from typing import List

import numpy as np
from IPython.display import display
from pandas import DataFrame, MultiIndex, Series


def show_df(df: DataFrame) -> None:
    """
    Show DataFrame with a summary in multi-row header.

    Parameters
    ----------
    df: DataFrame
        DataFrame to be shown
    """
    df_disp = df.copy()
    df_disp.columns = MultiIndex.from_tuples(
        list(
            zip(
                df_disp.columns,
                df_disp.dtypes,
                df_disp.nunique(),
                df_disp.isna().sum(),
            )
        ),
        names=["column", "dtype", "nunique", "missing"],
    )
    display(df_disp)


def show_nans_dtypes_nunique(
    df: DataFrame, show_transpose: bool = False
) -> None:
    """
    Summarize missing values, datatypes and number of unique values in header.

    Parameters
    ----------
    df: DataFrame
        DataFrame to be summarized
    show_transpose: bool=False
        whether to show a transpose of the summarized DataFrame
    """
    df_nans_dtypes = (
        df.isna()
        .sum()
        .rename("missing")
        .to_frame()
        .merge(
            df.nunique().rename("nunique").to_frame(),
            left_index=True,
            right_index=True,
            how="left",
        )
        .merge(
            df.dtypes.rename("dtype").to_frame(),
            left_index=True,
            right_index=True,
            how="left",
        )
    )
    if show_transpose:
        df_nans_dtypes = df_nans_dtypes.transpose()
    display(df_nans_dtypes)


def highlight_conditionally(
    df: DataFrame, col: str = "check", value: bool = False
) -> None:
    """
    Highlight rows based on conditional match(es) in column.

    Parameters
    ----------
    df: DataFrame
        DataFrame to be summarized
    col: str
        name of column to be checked
    value: bool
        value to be checked
    """
    display(
        df.style.apply(
            lambda _: (
                np.where(df[col] == value, "background-color: yellow", "")
            )
        )
    )


def highlight_unequal_columns(
    row: Series, left_col: str, right_col: str
) -> Series:
    """
    Highlight rows based on multi-column equality.

    Parameters
    ----------
    row: Series
        row to be checked
    left_col: str
        name of first row index to be checked for equality
    right_col: str
        name of second row index to be checked for equality
    """
    con = row.copy()
    con[:] = None
    if row[left_col] != row[right_col]:
        con[:] = "background-color: yellow"
    else:
        con[:] = "background-color: none"
    return con


def highlight_multiple_columns(col: Series) -> str:
    """
    Highlight all rows of single column.

    Parameters
    ----------
    col: str
        name of column to be highlighted
    """
    d = {"rmse": "yellow", "model_name": "cyan"}
    color = (
        f"background-color: {d[col.name]}"
        if col.name in list(d)
        else "background-color: #ffffff"
    )
    colors = [color for _ in col]
    return colors


def highlight_multiple_columns_ver2(df: DataFrame, columns: List[str]) -> None:
    """
    Highlight all rows of multiple columns.

    Parameters
    ----------
    df: DataFrame
        DataFrame whose columns are to be highlighted
    columns: List[str]
        list of columns to be highlighted
    """
    display(
        df.style.set_properties(
            subset=columns, **{"background-color": "yellow"}
        )
    )


def highlight_multiple_columns_row_greater_than(
    df: DataFrame, cols_to_check: List[str], threshold: int = 0
) -> DataFrame:
    """
    Highlight rows of multiple columns.

    Parameters
    ----------
    df: DataFrame
        DataFrame whose columns are to be checked and highlighted
    cols_to_check: List[str]
        list of columns to be checked and highlighted
    threshold: int
        value against which column values are to be checked
    """
    color = "background-color: yellow"

    # create empty DF
    df_colors = DataFrame("", index=df.index, columns=df.columns)

    # set new column background colors based on conditional
    for c in cols_to_check:
        df_colors.loc[df[c] > threshold, c] = color
    return df_colors
