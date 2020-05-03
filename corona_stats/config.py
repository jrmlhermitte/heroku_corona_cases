import os

THIS_MODULE_DIR = os.path.dirname(__file__)


def get_int_from_env(name: str, default: int):
    return int(os.environ.get(name) or default)


class Config:
    # refresh rate for corona virus data
    CORONA_DATA_TIMEOUT_SEC = get_int_from_env("CORONA_DATA_TIMEOUT_SEC", 600)

    # Canada data
    CANADA_DATA_URL = (
        "https://health-infobase.canada.ca/src/data/covidLive" + "/covid19.csv"
    )
    CANADA_CORONA_DATA_FILENAME = "canada_corona_by_province.csv"

    # US data
    CORONA_DATA_URL = "https://covidtracking.com/api/v1/states/daily.csv"
    CORONA_DATA_FILENAME = "corona_by_state.csv"
    CURRENT_CORONA_DATA_FILENAME = "corona_by_state.csv"
    CURRENT_CORONA_DATA_URL = (
        "https://covidtracking.com/api/v1/states" + "/current.csv"
    )

    # Location of local static data
    US_LAT_LONG_FILENAME = THIS_MODULE_DIR + "/data/csv/us_state_capitals.csv"

    # disables downloading, make sure you have data downloaded first
    OFFLINE_MODE = False
