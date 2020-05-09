import pandas as pd
import datetime as dt
from dataclasses import dataclass
from corona_stats.data.country import Country


@dataclass
class CoronaDataVersusTime:
    country: Country
    region: str
    positive_increase: pd.Series
    negative_increase: pd.Series
    total_increase: pd.Series
    last_updated: dt.datetime

    def description(self) -> str:
        return (
            f"Coronavirus cases for country {self.country.value}"
            f" and region {self.region}."
            f" Last updated: {self.last_updated}."
        )
