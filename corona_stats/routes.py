from bokeh.embed import file_html
from bokeh.models.annotations import Title
from bokeh.resources import CDN

from .data.us_data import (
    get_corona_data_by_state,
    get_last_time_updated,
    get_corona_data_for_united_states,
    get_latest_corona_data)
from .data.canada_data import (
    get_canada_data_by_province,
    get_last_time_canada_data_updated)

from .plots.vbar_stacked import get_cases_plot
from .plots.pie_chart import make_pie_chart


def positive_pie_chart():
    # Get the latest corona virus data.
    df = get_latest_corona_data()
    p = make_pie_chart(df, 'state', 'positive')

    bokeh_title = Title()
    bokeh_title.text = f'Positive Cases by state'
    p.title = bokeh_title

    return file_html(p, CDN, 'corona virus positive cases by state')


def cases_by_state(state_code):
    # Get the latest corona virus data.

    df = get_corona_data_by_state(state_code)
    last_updated = get_last_time_updated()
    title_text = (f'Cases for state {state_code}. Last downloaded: '
                  f' {last_updated}.')

    p = get_cases_plot(df)
    bokeh_title = Title()
    bokeh_title.text = title_text
    p.title = bokeh_title

    return file_html(p, CDN, 'corona virus')


def cases_canada_by_province(province):
    # Get the latest corona virus data.

    df = get_canada_data_by_province(province)
    last_updated = get_last_time_canada_data_updated()
    title_text = (f'Canada cases for province {province}. Last downloaded: '
                  f' {last_updated}.')

    p = get_cases_plot(df)
    bokeh_title = Title()
    bokeh_title.text = title_text
    p.title = bokeh_title

    return file_html(p, CDN, 'corona virus')


def cases_for_united_states():
    # Get the latest corona virus data.
    df = get_corona_data_for_united_states()
    last_updated = get_last_time_updated()
    title_text = (f'Cases for United States. Last downloaded: '
                  f' {last_updated}.')

    p = get_cases_plot(df)
    bokeh_title = Title()
    bokeh_title.text = title_text
    p.title = bokeh_title

    return file_html(p, CDN, 'corona virus')
