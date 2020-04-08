import datetime as dt
import urllib.request

import pandas as pd

from corona_stats.caching_decorator import cache_manager
from corona_stats.config import Config


CORONA_VIRUS_BY_STATE_KEY = 'corona_virus_by_state'


def download_corona_data_file() -> None:
    urllib.request.urlretrieve(Config.CORONA_DATA_URL,
                               Config.CORONA_DATA_FILENAME)


def get_corona_data_from_file() -> pd.DataFrame:
    df = pd.read_csv(Config.CORONA_DATA_FILENAME)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['totalIncrease'] = df['positiveIncrease'] + df['negativeIncrease']
    return df


@cache_manager.memorize(CORONA_VIRUS_BY_STATE_KEY,
                        Config.CORONA_DATA_TIMEOUT_SEC)
def get_corona_data() -> pd.DataFrame:
    download_corona_data_file()
    return get_corona_data_from_file()


def get_latest_corona_data():
    df = get_corona_data()
    # NOTE: There should not be more than one value per state. If this is not
    # true, raise an error.
    today = df['date'].max()
    df_today = df[df['date'] == today]
    return df_today


def get_corona_data_by_state(state: str) -> pd.DataFrame:
    df = get_corona_data()
    return df[df['state'] == state]


def get_corona_data_for_united_states() -> pd.DataFrame:
    df = get_corona_data()
    df = df.groupby('date').sum()
    # We should just plot the index, and assume the date is the index.
    df['date'] = df.index
    df.reset_index(drop=True, inplace=True)
    return df


def get_last_time_updated() -> dt.datetime:
    return cache_manager.last_updated(CORONA_VIRUS_BY_STATE_KEY)


def get_help_message():
    return f'Available states: ' + ', '.join(STATES)


STATES = [
 'AK',
 'AL',
 'AR',
 'AS',
 'AZ',
 'CA',
 'CO',
 'CT',
 'DC',
 'DE',
 'FL',
 'GA',
 'GU',
 'HI',
 'IA',
 'ID',
 'IL',
 'IN',
 'KS',
 'KY',
 'LA',
 'MA',
 'MD',
 'ME',
 'MI',
 'MN',
 'MO',
 'MP',
 'MS',
 'MT',
 'NC',
 'ND',
 'NE',
 'NH',
 'NJ',
 'NM',
 'NV',
 'NY',
 'OH',
 'OK',
 'OR',
 'PA',
 'PR',
 'RI',
 'SC',
 'SD',
 'TN',
 'TX',
 'UT',
 'VA',
 'VI',
 'VT',
 'WA',
 'WI',
 'WV',
 'WY'
]