from dataclasses import dataclass

import plotly
from plotly.graph_objects import Figure


@dataclass
class PlotlyPlot:
    fig: Figure

    def to_javascript(self) -> str:
        return plotly.offline.plot(
            self.fig,
            config={"displayModeBar": False},
            show_link=False,
            include_plotlyjs=False,
            output_type='div')