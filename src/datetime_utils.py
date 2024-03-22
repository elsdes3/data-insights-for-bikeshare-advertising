#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Define utilities to manipulate datetimes."""

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals,unused-argument

from datetime import datetime


def conv2dtime(date_time: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """."""
    return datetime.strptime(date_time, fmt)


def dtime2str(date_time: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """."""
    return date_time.strftime(fmt)
