import datetime as dt
import urllib.request
from dataclasses import dataclass
from typing import Union

import pandas as pd

from corona_stats.caching_decorator import cache_manager
from corona_stats.config import Config

CORONA_VIRUS_BY_STATE_KEY = "corona_virus_by_state"
CURRENT_CORONA_VIRUS_BY_STATE_KEY = "current_corona_virus_by_state"

DATA_ELEMENT = Union[int, float, dt.datetime]


@dataclass
class USData:
    def __init__(self, df: pd.DataFrame):
        self.df = df


def download_corona_data_file() -> None:
    if not Config.OFFLINE_MODE:
        urllib.request.urlretrieve(
            Config.CORONA_DATA_URL, Config.CORONA_DATA_FILENAME
        )


def get_corona_data_from_file() -> pd.DataFrame:
    df = pd.read_csv(Config.CORONA_DATA_FILENAME)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df["totalIncrease"] = df["positiveIncrease"] + df["negativeIncrease"]
    df_latlong = get_us_lat_long_coord()
    return pd.merge(df, df_latlong, on="state", how="left")


def download_current_corona_data_file() -> None:
    if not Config.OFFLINE_MODE:
        urllib.request.urlretrieve(
            Config.CURRENT_CORONA_DATA_URL, Config.CURRENT_CORONA_DATA_FILENAME
        )


def get_current_corona_data_from_file() -> pd.DataFrame:
    df = pd.read_csv(Config.CURRENT_CORONA_DATA_FILENAME)
    df_latlong = get_us_lat_long_coord()
    return pd.merge(df, df_latlong, on="state", how="left")


def get_us_lat_long_coord() -> pd.DataFrame:
    # Found from https://raw.githubusercontent.com/jasperdebie/VisInfo/master
    # /us-state-capitals.csv
    # and I had to manually add state codes on top of it.
    df = pd.read_csv(Config.US_LAT_LONG_FILENAME)
    df["state"] = df["state_code"]
    # We ignore the city, we just need it for a good latitude and longitude.
    return df[["state", "latitude", "longitude"]]


@cache_manager.memorize(
    CORONA_VIRUS_BY_STATE_KEY, Config.CORONA_DATA_TIMEOUT_SEC
)
def get_corona_data() -> pd.DataFrame:
    download_corona_data_file()
    return get_corona_data_from_file()


@cache_manager.memorize(
    CURRENT_CORONA_VIRUS_BY_STATE_KEY, Config.CORONA_DATA_TIMEOUT_SEC
)
def get_current_corona_data() -> pd.DataFrame:
    download_current_corona_data_file()
    return get_current_corona_data_from_file()


def get_latest_corona_data():
    df = get_corona_data()
    # NOTE: There should not be more than one value per state. If this is not
    # true, raise an error.
    today = df["date"].max()
    df_today = df[df["date"] == today]
    return df_today


def get_corona_data_by_state(state: str) -> pd.DataFrame:
    df = get_corona_data()
    return df[df["state"] == state]


def get_corona_data_for_united_states() -> pd.DataFrame:
    df = get_corona_data()
    df = df.groupby("date").sum()
    # We should just plot the index, and assume the date is the index.
    df["date"] = df.index
    df.reset_index(drop=True, inplace=True)
    return df


def get_last_time_updated() -> dt.datetime:
    return cache_manager.last_updated(CORONA_VIRUS_BY_STATE_KEY)


STATES = [
    "AK",
    "AL",
    "AR",
    "AS",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "GU",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MP",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "PR",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VI",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
]
