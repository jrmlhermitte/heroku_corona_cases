from flask import render_template

from .data import canada_data
from .data import us_data
from .plots.vbar_stacked import get_plotly_cases_plot


def cases_by_state(state_code):
    # Get the latest corona virus data.

    df = us_data.get_corona_data_by_state(state_code)
    last_updated = us_data.get_last_time_updated()
    title_text = (f'Cases for state {state_code}. Last downloaded: '
                  f' {last_updated}.')
    fig = get_plotly_cases_plot(df)

    return render_template('plotly_plot.html',
                           plot_data=fig.to_javascript(),
                           title=title_text)


def cases_canada_by_province(province):
    # Get the latest corona virus data.
    df = canada_data.get_canada_data_by_province(province)

    last_updated = canada_data.get_last_time_canada_data_updated()
    title_text = (f'Canada cases for province {province}. '
                  'Last downloaded: '
                  f' {last_updated}.')

    fig = get_plotly_cases_plot(df)

    return render_template('plotly_plot.html',
                           plot_data=fig.to_javascript(),
                           title=title_text,
                           description=canada_data.CANADA_DESCRIPTION)


def cases_for_canada():
    df = canada_data.get_canada_data()
    fig = get_plotly_cases_plot(df)
    title_text = 'Canada Data'

    return render_template('plotly_plot.html',
                           plot_data=fig.to_javascript(),
                           title=title_text,
                           description=canada_data.CANADA_DESCRIPTION)


def cases_for_united_states():
    # Get the latest corona virus data.
    df = us_data.get_corona_data_for_united_states()
    last_updated = us_data.get_last_time_updated()
    title_text = (f'Cases for United States. Last downloaded: '
                  f' {last_updated}.')

    fig = get_plotly_cases_plot(df)

    return render_template('plotly_plot.html',
                           plot_data=fig.to_javascript(),
                           title=title_text)
