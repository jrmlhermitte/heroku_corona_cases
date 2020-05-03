import plotly.graph_objects as go
from corona_stats.plots.plotly_plot import PlotlyPlot


def get_plotly_cases_plot(df) -> PlotlyPlot:
    """Returns javascript code."""

    updatemenus = list(
        [
            dict(
                buttons=list(
                    [
                        dict(
                            label="Linear Scale",
                            method="relayout",
                            args=[{"yaxis.type": "linear"}],
                        ),
                        dict(
                            label="Log Scale",
                            method="relayout",
                            args=[{"yaxis.type": "log"}],
                        ),
                    ]
                )
            )
        ]
    )

    fig = go.Figure(
        data=[
            go.Bar(
                name="Positive Cases",
                x=df["date"],
                y=df["positiveIncrease"],
                marker_color="#9B2208",
            ),
            go.Bar(
                name="Negative Cases",
                x=df["date"],
                y=df["negativeIncrease"],
                marker_color="#C7ECDF",
            ),
        ]
    )

    # Change the bar mode
    fig.update_layout(barmode="stack")
    fig.update_layout(updatemenus=updatemenus)
    # fig.update_layout(yaxis_type="log")
    return PlotlyPlot(fig=fig)
