from bokeh.embed import components
from bokeh.embed import file_html
from bokeh.models import DatetimeTickFormatter

from bokeh.resources import CDN
from flask import Flask
from flask_cors import CORS
from bokeh.models.annotations import Title
import numpy as np

from .data import (
    get_corona_data_by_state,
    get_last_time_updated,
    get_corona_data_for_united_states)
from .plots import get_cases_plot


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
