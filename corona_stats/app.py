import os

from flask import Flask, render_template

from .data.canada_data import PROVINCES
from .data.us_data import STATES
from .data.us_data import get_current_corona_data
from .plots.bubble_map import get_us_bubble_map_plot
from .routes import (
    cases_by_state,
    cases_for_united_states,
    cases_canada_by_province,
    cases_for_canada)


def create_app(test_config=None):
    # pylint: disable=unused-variable
    # create and configure the app
    config = {
        'DEBUG': True,  # some Flask specific configs
    }

    app = Flask(__name__,
                instance_relative_config=True)
    app.config.from_mapping(config)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # US routes
    app.route('/corona/us')(cases_for_united_states)
    app.route('/corona/us/<string:state_code>')(cases_by_state)

    # Canada routes
    app.route('/corona/canada')(cases_for_canada)
    app.route('/corona/canada/<string:province>')(cases_canada_by_province)

    # Home route
    @app.route('/')
    def home():
        df = get_current_corona_data()
        fig = get_us_bubble_map_plot(df, size_key='death', size_name='Deaths')
        return render_template('home.html',
                               us_states=STATES,
                               ca_provinces=PROVINCES,
                               us_map=fig.to_javascript())

    return app
