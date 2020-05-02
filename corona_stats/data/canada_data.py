"""
Canada data pulled from:
    https://www.canada.ca/en/public-health/services/diseases/2019-novel
    -coronavirus-infection.html
"""


import datetime as dt
import urllib.request

import pandas as pd

from corona_stats.caching_decorator import cache_manager
from corona_stats.config import Config

CANADA_DATA_KEY = 'canada-data'


# TODO: put this elsewhere (make a us and canada html template).
CANADA_DESCRIPTION = (
    'NOTE: It appears that some cases are confirmed '
    'positive '
    'the following '
    'day. This can lead to an apparent decrease in negative '
    'cases one day (a case was negative but is now confirmed '
    'positive).'
    ' This data was pulled from gov canada, please see '
    '<a href="https://www.canada.ca/en/public-health/services'
    '/diseases/2019-novel-coronavirus-infection.html">here</a> '
    'for more information.')


PROVINCES = [
    'Ontario', 'British Columbia', 'Quebec', 'Alberta',
    'Repatriated travellers', 'Saskatchewan', 'Manitoba',
    'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia',
    'Prince Edward Island', 'Yukon', 'Northwest Territories',
    'Nunavut'
]

OTHER_PRNAME_CODES = ['Canada']


def get_canada_data():
    # Confusing but Gov Canada data has a special province code called "Canada"
    return get_canada_data_by_province(province='Canada')


def get_canada_data_by_province(province: str):
    df = get_data_from_gov_canada()
    df = df.sort_values('date', ascending=True)
    df_by_province = df[df['prname'] == province].copy()

    time_intervals = df_by_province['date'].diff()
    time_intervals_days = time_intervals.apply(lambda x: x.days)

    df_by_province.loc[:, 'totalIncrease'] = (
        df_by_province['numtested'].diff() /
        time_intervals_days)
    df_by_province.loc[:, 'positiveIncrease'] = (
        df_by_province['numconf'].diff() /
        time_intervals_days)
    df_by_province.loc[:, 'negativeIncrease'] = (
        df_by_province['totalIncrease'] -
        df_by_province['positiveIncrease'])
    return df_by_province


def get_last_time_canada_data_updated() -> dt.datetime:
    return cache_manager.last_updated(CANADA_DATA_KEY)


@cache_manager.memorize(CANADA_DATA_KEY,
                        Config.CORONA_DATA_TIMEOUT_SEC)
def get_data_from_gov_canada() -> pd.DataFrame:
    _download_canada_data()
    return _get_canada_corona_data_from_file()


def _download_canada_data():
    if not Config.OFFLINE_MODE:
        urllib.request.urlretrieve(Config.CANADA_DATA_URL,
                                   Config.CANADA_CORONA_DATA_FILENAME)


def _get_canada_corona_data_from_file() -> pd.DataFrame:
    df = pd.read_csv(Config.CANADA_CORONA_DATA_FILENAME)
    df.loc[:, 'date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    return df
