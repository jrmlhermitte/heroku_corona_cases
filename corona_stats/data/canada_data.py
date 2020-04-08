import urllib.request
import datetime as dt

import pandas as pd

from corona_stats.caching_decorator import cache_manager
from corona_stats.config import Config

CANADA_DATA_KEY = 'canada-data'


def _download_canada_data():
    urllib.request.urlretrieve(Config.CANADA_DATA_URL,
                               Config.CANADA_CORONA_DATA_FILENAME)


def _get_canada_corona_data_from_file() -> pd.DataFrame:
    df = pd.read_csv(Config.CANADA_CORONA_DATA_FILENAME)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    return df


@cache_manager.memorize(CANADA_DATA_KEY,
                        Config.CORONA_DATA_TIMEOUT_SEC)
def get_canada_corona_data() -> pd.DataFrame:
    _download_canada_data()
    return _get_canada_corona_data_from_file()


def get_canada_data_by_province(province: str):
    df = get_canada_corona_data()
    df = df.sort_values('date', ascending=True)
    df_by_province = df[df['prname'] == province]

    time_intervals = df_by_province['date'].diff()
    time_intervals_days = time_intervals.apply(lambda x: x.days)

    df_by_province['totalIncrease'] = (df_by_province['numtested'].diff() /
                           time_intervals_days)
    df_by_province['positiveIncrease'] = (df_by_province['numconf'].diff() /
                              time_intervals_days)
    df_by_province['negativeIncrease'] = (
            df_by_province['totalIncrease'] -
            df_by_province['positiveIncrease'])
    return df_by_province


def get_last_time_canada_data_updated() -> dt.datetime:
    return cache_manager.last_updated(CANADA_DATA_KEY)


def get_help_message():
    return f'Available provinces: ' + ', '.join(PROVINCES)


PROVINCES = [
    'Ontario', 'British Columbia', 'Canada', 'Quebec', 'Alberta',
    'Repatriated travellers', 'Saskatchewan', 'Manitoba',
    'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia',
    'Prince Edward Island', 'Yukon', 'Northwest Territories',
    'Nunavut'
]
