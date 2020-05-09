from __future__ import annotations
from dataclasses import dataclass
import plotly


import plotly.graph_objects as go
from corona_stats.data.corona_data_by_region import CoronaDataByRegion
from corona_stats.data.country import Country

from corona_stats.plots.models.quantile_to_plot import QuantileToPlot

SHADE_OF_GREY = "rgb(217, 217, 217)"
_COUNTRY_TO_GEO_SCOPE = {Country.USA: "usa", Country.Canada: "canada"}
# TODO (jrmlhermitte): Look up mode for Canada
_COUNTRY_TO_LOCATION_MODE = {Country.USA: "USA-states"}


# Default quantile ranges to set for the categorical coloring of data.
DEFAULT_QUANTILES_TO_PLOT = [
    QuantileToPlot(
        start=0, end=0.1, color="royalblue", include_endpoint=False
    ),
    QuantileToPlot(
        start=0.1, end=0.5, color="crimson", include_endpoint=False
    ),
    QuantileToPlot(
        start=0.5, end=0.75, color="lightseagreen", include_endpoint=False
    ),
    QuantileToPlot(
        start=0.75, end=0.9, color="orange", include_endpoint=False
    ),
    QuantileToPlot(start=0.9, end=1.0, color="red", include_endpoint=True),
]


# Followed: https://plotly.com/python/bubble-maps/
@dataclass
class PlotlyBubbleMap:
    fig: go.Figure
    scale: float

    def to_javascript(self) -> str:
        return plotly.offline.plot(
            self.fig,
            config={"displayModeBar": False},
            show_link=False,
            include_plotlyjs=False,
            output_type="div",
        )

    @staticmethod
    def empty(scale: int = 1) -> PlotlyBubbleMap:
        fig = go.Figure()
        plot = PlotlyBubbleMap(fig=fig, scale=scale)
        return plot

    @classmethod
    def from_corona_data(
        cls, corona_data: CoronaDataByRegion
    ) -> PlotlyBubbleMap:
        plot = cls.empty()
        for quantile in DEFAULT_QUANTILES_TO_PLOT:
            plot.add_regions_for_quantile(corona_data, quantile)
        plot.update_layout_for_country(corona_data)
        return plot

    def add_regions_for_quantile(
        self, corona_data: CoronaDataByRegion, quantile: QuantileToPlot
    ):
        quantile_range = quantile.to_numerical_range()
        values_range = corona_data.numerical_range_for_quantile_range(
            quantile_range
        )
        regions = corona_data.regions_in_range(values_range)

        size_color = quantile.color
        size_category_text = values_range.to_text(round_to_decimal=0)
        latitudes = [region.latitude for region in regions]
        longitudes = [region.longitude for region in regions]
        descriptions = [region.description_html() for region in regions]
        counts = [region.count / self.scale for region in regions]

        location_mode = _COUNTRY_TO_LOCATION_MODE[corona_data.country]
        scatter_geo = go.Scattergeo(
            locationmode=location_mode,
            lon=longitudes,
            lat=latitudes,
            text=descriptions,
            marker=dict(
                size=counts,
                color=size_color,
                line_color="rgb(40,40,40)",
                line_width=0.5,
                sizemode="area",
            ),
            name=size_category_text,
        )

        self.fig.add_trace(scatter_geo)

    def update_layout_for_country(self, corona_data: CoronaDataByRegion):
        self.fig.update_layout(
            title_text=corona_data.description(), showlegend=True
        )
        self._update_geo_scope(corona_data)

    def _update_geo_scope(self, corona_data: CoronaDataByRegion):
        plot_scope = _COUNTRY_TO_GEO_SCOPE.get(corona_data.country)
        geo = dict(scope=plot_scope, landcolor=SHADE_OF_GREY)
        self.fig.update_layout(geo=geo)
