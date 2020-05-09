import datetime as dt
import functools
from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd

from corona_stats.data.country import Country
from corona_stats.data.numerical_range import NumericalRange

# Arbitrary
_LRU_CACHE_SIZE = 400


@dataclass(frozen=True)
class RegionCoronaData:
    name: str
    latitude: float
    longitude: float
    statistic_name: str
    count: int

    def description_html(self) -> str:
        return f"{self.name} <br /> {self.statistic_name}: {self.count}."


@dataclass(frozen=True)
class CoronaDataByRegion:
    country: Country
    statistic_name: str
    total: int
    regions: Tuple[RegionCoronaData, ...]
    last_updated: dt.datetime

    def description(self) -> str:
        return (
            f"Corona Virus {self.statistic_name}s"
            f"for {self.country}. Total: {self.total}."
        )

    @functools.lru_cache(maxsize=_LRU_CACHE_SIZE)
    def statistics(self) -> pd.Series:
        return pd.Series([region.count for region in self.regions])

    def quantile(self, quantile_value: float) -> float:
        return self.statistics().quantile(quantile_value)

    def numerical_range_for_quantile_range(
        self, quantile_range: NumericalRange
    ) -> NumericalRange:
        start_limit = self.quantile(quantile_range.start)
        end_limit = self.quantile(quantile_range.end)
        return NumericalRange(
            start=start_limit,
            end=end_limit,
            include_endpoint=quantile_range.include_endpoint,
        )

    def regions_in_range(
        self, numerical_range: NumericalRange
    ) -> List[RegionCoronaData]:
        regions = []
        for region in self.regions:
            if numerical_range.within_bounds(region.count):
                regions.append(region)
        return regions
