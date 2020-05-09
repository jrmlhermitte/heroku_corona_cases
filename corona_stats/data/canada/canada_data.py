"""
Canada data pulled from:
    https://www.canada.ca/en/public-health/services/diseases/2019-novel
    -coronavirus-infection.html
"""
from __future__ import annotations

import datetime as dt
import urllib.request
from dataclasses import dataclass

import pandas as pd

from corona_stats.caching_decorator import cache_manager
from corona_stats.config import Config
from corona_stats.data.corona_data_versus_time import CoronaDataVersusTime
from corona_stats.data.country import Country

CANADA_DATA_KEY = "canada-data"


@dataclass
class RawCanadaData:
    df: pd.DataFrame
    last_updated: dt.datetime

    def _dataframe_by_province(self, province: str) -> pd.DataFrame:
        df = self.df
        df = df.sort_values("date", ascending=True)
        df = df.set_index("date", drop=False)
        df_by_province = df[df["prname"] == province].copy()
        df_by_province.drop_duplicates("date", inplace=True)
        return df_by_province

    def by_province(self, province: str) -> CoronaDataVersusTime:
        df_by_province = self._dataframe_by_province(province=province)
        time_intervals_days = _time_intervals_from_dates(
            df_by_province["date"]
        )
        totals = df_by_province["numtested"]
        positives = df_by_province["numconf"]

        total_increase = totals.diff() / time_intervals_days
        positive_increase = positives.diff() / time_intervals_days
        negative_increase = total_increase - positive_increase

        return CoronaDataVersusTime(
            total_increase=total_increase,
            positive_increase=positive_increase,
            negative_increase=negative_increase,
            last_updated=self.last_updated,
            region=province,
            country=Country.Canada,
        )


def _time_intervals_from_dates(dates: pd.Seris) -> pd.Series:
    time_intervals = dates.diff()
    time_intervals_days = time_intervals.apply(lambda x: x.days)
    return time_intervals_days


def get_canada_data_by_province(province: str) -> CoronaDataVersusTime:
    raw_canada_data = get_data_from_gov_canada()
    return raw_canada_data.by_province(province=province)


def get_canada_data() -> CoronaDataVersusTime:
    # Confusing but Gov Canada data has a special province code called "Canada"
    return get_canada_data_by_province("Canada")


@cache_manager.memorize(CANADA_DATA_KEY, Config.CORONA_DATA_TIMEOUT_SEC)
def get_data_from_gov_canada() -> RawCanadaData:
    _download_canada_data()
    df = _get_canada_corona_data_from_file()
    return RawCanadaData(df=df, last_updated=dt.datetime.utcnow())


def _download_canada_data():
    if not Config.OFFLINE_MODE:
        urllib.request.urlretrieve(
            Config.CANADA_DATA_URL, Config.CANADA_CORONA_DATA_FILENAME
        )


def _get_canada_corona_data_from_file() -> pd.DataFrame:
    df = pd.read_csv(Config.CANADA_CORONA_DATA_FILENAME)
    df.loc[:, "date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    return df
