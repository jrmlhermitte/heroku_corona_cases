import os
import sys

from flask import Flask
from .routes import (
    cases_by_state,
    cases_for_united_states,
    positive_pie_chart,
    cases_canada_by_province,
    cases_for_canada)

# TODO: rename this and move to routes
from .data.us_data import get_help_message as us_message
from .data.canada_data import get_help_message as canada_message


def create_app(test_config=None):
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

    # a simple page that says hello
    app.route('/corona/byState/<string:state_code>')(cases_by_state)

    app.route('/corona/canada/<string:province>')(cases_canada_by_province)

    # a simple page that says hello
    app.route('/corona/allStates')(cases_for_united_states)
    app.route('/corona')(positive_pie_chart)

    app.route('/corona/canada')(cases_for_canada)

    @app.route('/')
    def home():
        message = (
            'Welcome to Corona Stats. Routes: <br />'
            '- <a href="/corona/allStates">/corona/allStates</a>: stats '
            'for all states <br />'
            '- <a href="/corona/byState/NY">/corona/byState/NY</a>: stats '
            'for state. Replace NY with state <br />'
            '- <a href="/corona">/corona</a>: Positive cases by state'
            'code <br />'
            '- <a href="/corona/canada/Quebec">/corona/canada/Quebec</a>: '
            'Positive cases by province. <br />')
        message = message + '<br />' * 2 + us_message()
        message = message + '<br />' * 2 + canada_message()
        return message

    return app
