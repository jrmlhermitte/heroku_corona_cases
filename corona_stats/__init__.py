import os
import sys

from flask import Flask
from .routes import cases_by_state, cases_for_united_states


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

    # a simple page that says hello
    app.route('/corona/allStates')(cases_for_united_states)

    @app.route('/')
    def home():
        print('at home', file=sys.stderr)
        return ('Welcome to Corona Stats. Routes: \n'
                '- /allStates: stats for all states \n'
                '- /byState/NY: stats for state. Replace NY with state code')

    return app
