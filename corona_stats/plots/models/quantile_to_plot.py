from dataclasses import dataclass

from corona_stats.data.numerical_range import NumericalRange


@dataclass
class QuantileToPlot:
    start: float
    end: float
    color: str
    include_endpoint: bool = False

    def to_numerical_range(self) -> NumericalRange:
        return NumericalRange(
            start=self.start,
            end=self.end,
            include_endpoint=self.include_endpoint,
        )
