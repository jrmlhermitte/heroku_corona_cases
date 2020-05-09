import urllib.request

import pandas as pd

from corona_stats.caching_decorator import cache_manager
from corona_stats.config import Config
from corona_stats.data.us.us_data import CURRENT_CORONA_VIRUS_BY_STATE_KEY
from corona_stats.data.country import Country
import datetime as dt
from corona_stats.data.corona_data_by_region import (
    CoronaDataByRegion,
    RegionCoronaData,
)
from dataclasses import dataclass


@dataclass
class RawCurrentUSCoronaData:
    df: pd.DataFrame
    last_updated: dt.datetime

    def by_statistic(self, statistic_name: str) -> CoronaDataByRegion:
        regions = []
        total = 0
        for _, row in self.df.iterrows():
            name = row["state"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            # we ignore non-existant lat or long
            if pd.isna(latitude) or pd.isna(longitude):
                continue

            count = row[statistic_name]
            total += count
            region = RegionCoronaData(
                name=name,
                latitude=latitude,
                longitude=longitude,
                statistic_name=statistic_name,
                count=count,
            )
            regions.append(region)
        return CoronaDataByRegion(
            country=Country.USA,
            statistic_name=statistic_name,
            total=total,
            regions=tuple(regions),
            last_updated=self.last_updated,
        )


@cache_manager.memorize(
    CURRENT_CORONA_VIRUS_BY_STATE_KEY, Config.CORONA_DATA_TIMEOUT_SEC
)
def get_current_corona_data() -> RawCurrentUSCoronaData:
    _download_current_corona_data_file()
    return _get_current_corona_data_from_file()


# Wrap into a CoronaDataByRegion class
def _download_current_corona_data_file() -> None:
    if not Config.OFFLINE_MODE:
        urllib.request.urlretrieve(
            Config.CURRENT_CORONA_DATA_URL, Config.CURRENT_CORONA_DATA_FILENAME
        )


def _get_current_corona_data_from_file() -> RawCurrentUSCoronaData:
    df = pd.read_csv(Config.CURRENT_CORONA_DATA_FILENAME)
    df_latlong = _get_us_lat_long_coord()
    df = pd.merge(df, df_latlong, on="state", how="left")
    return RawCurrentUSCoronaData(df=df, last_updated=dt.datetime.utcnow())


def _get_us_lat_long_coord() -> pd.DataFrame:
    # Found from https://raw.githubusercontent.com/jasperdebie/VisInfo/master
    # /us-state-capitals.csv
    # and I had to manually add state codes on top of it.
    df = pd.read_csv(Config.US_LAT_LONG_FILENAME)
    df["state"] = df["state_code"]
    # We ignore the city, we just need it for a good latitude and longitude.
    return df[["state", "latitude", "longitude"]]
