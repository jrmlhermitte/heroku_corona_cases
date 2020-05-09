from flask import render_template

from .data.us import us_data
from .data.canada import canada_data
from corona_stats.plots.plotly_vbar_plot import PlotlyVBarPlot
from .data.canada.provinces import PROVINCES
from corona_stats.plots.plotly_bubble_map import PlotlyBubbleMap
from .data.us.current_us_data import get_current_corona_data
from .data.us.states import STATES


def cases_by_state(state_code):
    # Get the latest corona virus data.
    raw_corona_data = us_data.get_corona_data()
    corona_data = raw_corona_data.by_state(state_code)
    plot = PlotlyVBarPlot.from_corona_data(corona_data)

    return render_template(
        "us_plot.html",
        plot_data=plot.to_javascript(),
        title=corona_data.description(),
    )


def cases_canada_by_province(province):
    # Get the latest corona virus data.
    province_data = canada_data.get_canada_data_by_province(province=province)
    fig = PlotlyVBarPlot.from_corona_data(province_data)

    return render_template(
        "canada_plot.html",
        plot_data=fig.to_javascript(),
        title=province_data.description(),
    )


def cases_for_canada():
    corona_data = canada_data.get_canada_data()
    fig = PlotlyVBarPlot.from_corona_data(corona_data)

    return render_template(
        "canada_plot.html",
        plot_data=fig.to_javascript(),
        title=corona_data.description(),
    )


def cases_for_united_states():
    # Get the latest corona virus data.
    raw_corona_data = us_data.get_corona_data()
    corona_data = raw_corona_data.all_states()

    plot = PlotlyVBarPlot.from_corona_data(corona_data)

    return render_template(
        "us_plot.html",
        plot_data=plot.to_javascript(),
        title=corona_data.description(),
    )


def home():
    """Right now this is a plot of US deaths."""
    raw_corona_data = get_current_corona_data()
    corona_data = raw_corona_data.by_statistic("death")
    plot = PlotlyBubbleMap.from_corona_data(corona_data)
    return render_template(
        "home.html",
        us_states=STATES,
        ca_provinces=PROVINCES,
        us_map=plot.to_javascript(),
    )
