from __future__ import annotations

from dataclasses import dataclass
from corona_stats.data.corona_data_versus_time import CoronaDataVersusTime
import pandas as pd

import plotly
import plotly.graph_objects as go


linear_scale_button = {
    "label": "Linear Scale",
    "method": "relayout",
    "args": [{"yaxis.type": "linear"}],
}


log_scale_button = {
    "label": "Log Scale",
    "method": "relayout",
    "args": [{"yaxis.type": "log"}],
}


@dataclass
class PlotlyVBarPlot:
    fig: go.Figure

    def to_javascript(self) -> str:
        return plotly.offline.plot(
            self.fig,
            config={"displayModeBar": False},
            show_link=False,
            include_plotlyjs=False,
            output_type="div",
        )

    def add_series_to_plot(self, series: pd.Series, title: str, color: str):
        bar_plot = go.Bar(
            name=title, x=series.index, y=series.values, marker_color=color
        )
        self.fig.add_trace(bar_plot)

    @classmethod
    def empty(cls) -> PlotlyVBarPlot:
        fig = go.Figure()
        fig = cls._setup_plot(fig)
        return PlotlyVBarPlot(fig=fig)

    @classmethod
    def from_corona_data(cls, corona_data: CoronaDataVersusTime):
        plot = cls.empty()
        # fig.update_layout(yaxis_type="log")
        plot.add_series_to_plot(
            corona_data.positive_increase,
            title="Positive Cases",
            color="#9B2208",
        )
        plot.add_series_to_plot(
            corona_data.negative_increase,
            title="Negative Cases",
            color="#C7ECDF",
        )
        return plot

    @staticmethod
    def _setup_plot(fig: go.Figure) -> go.Figure:
        updatemenus = [{"buttons": [linear_scale_button, log_scale_button]}]
        # Change the bar mode
        fig.update_layout(barmode="stack")
        fig.update_layout(updatemenus=updatemenus)
        return fig
