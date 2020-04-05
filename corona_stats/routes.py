from bokeh.embed import file_html
from bokeh.models.annotations import Title
from bokeh.resources import CDN
import sys

from .data import (
    get_corona_data_by_state,
    get_last_time_updated,
    get_corona_data_for_united_states)
from .plots import get_cases_plot


def cases_by_state(state_code):
    # Get the latest corona virus data.

    print('getting dataframe', file=sys.stderr)
    df = get_corona_data_by_state(state_code)
    print(f'Got dataframe', file=sys.stderr)
    last_updated = get_last_time_updated()
    title_text = (f'Cases for state {state_code}. Last downloaded: '
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
