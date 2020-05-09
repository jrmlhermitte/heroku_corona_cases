import datetime as dt
import urllib.request
from dataclasses import dataclass
from typing import Union

import pandas as pd

from corona_stats.caching_decorator import cache_manager
from corona_stats.config import Config
from corona_stats.data.corona_data_versus_time import CoronaDataVersusTime
from corona_stats.data.country import Country

CORONA_VIRUS_BY_STATE_KEY = "corona_virus_by_state"
CURRENT_CORONA_VIRUS_BY_STATE_KEY = "current_corona_virus_by_state"

DATA_ELEMENT = Union[int, float, dt.datetime]
ALL_STATES = "All States"


@dataclass
class RawUSData:
    df: pd.DataFrame
    last_updated: dt.datetime

    def _dataframe_by_state(self, state: str) -> pd.DataFrame:
        return self.df[self.df["state"] == state]

    def by_state(self, state: str) -> CoronaDataVersusTime:
        df_state = self._dataframe_by_state(state=state)
        # TODO(jrmlhermitte): Check if there are duplicates and warn.
        df_state.drop_duplicates("date", inplace=True)
        positive_increase = df_state["positiveIncrease"]
        negative_increase = df_state["negativeIncrease"]
        total_increase = df_state["totalIncrease"]
        return CoronaDataVersusTime(
            country=Country.USA,
            region=state,
            positive_increase=positive_increase,
            negative_increase=negative_increase,
            total_increase=total_increase,
            last_updated=self.last_updated,
        )

    def all_states(self) -> CoronaDataVersusTime:
        # Can't have an index and column with same name, so we rename
        # the index.
        # TODO (jrmlhermitte): "date" is used when dropping duplicates
        #  (which operates on a column) as well as the index for
        #  extracted series.
        df = self.df.rename_axis(None)
        df = df.groupby("date").sum()
        positive_increase = df["positiveIncrease"]
        negative_increase = df["negativeIncrease"]
        total_increase = df["totalIncrease"]
        return CoronaDataVersusTime(
            country=Country.USA,
            region=ALL_STATES,
            positive_increase=positive_increase,
            negative_increase=negative_increase,
            total_increase=total_increase,
            last_updated=self.last_updated,
        )


@cache_manager.memorize(
    CORONA_VIRUS_BY_STATE_KEY, Config.CORONA_DATA_TIMEOUT_SEC
)
def get_corona_data() -> RawUSData:
    _download_corona_data_file()
    df = _get_corona_data_from_file()
    return RawUSData(df=df, last_updated=dt.datetime.utcnow())


def _download_corona_data_file() -> None:
    if not Config.OFFLINE_MODE:
        urllib.request.urlretrieve(
            Config.CORONA_DATA_URL, Config.CORONA_DATA_FILENAME
        )


def _get_corona_data_from_file() -> pd.DataFrame:
    df = pd.read_csv(Config.CORONA_DATA_FILENAME)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df["totalIncrease"] = df["positiveIncrease"] + df["negativeIncrease"]
    df.set_index("date", inplace=True, drop=False)
    return df
