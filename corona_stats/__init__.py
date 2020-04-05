import os

from flask import Flask
from .routes import cases_by_state, cases_for_united_states
from flask_caching import Cache

CACHE_TIMEOUT = 600


def create_app(test_config=None):
    # create and configure the app
    config = {
        'DEBUG': True,  # some Flask specific configs
        'CACHE_TYPE': 'simple',  # Flask-Caching related configs
        'CACHE_DEFAULT_TIMEOUT': CACHE_TIMEOUT
    }

    app = Flask(__name__,
                instance_relative_config=True)
    app.config.from_mapping(config)
    cache = Cache(app)

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
    app.route('/corona/byState/<string:state_code>')(
        cache.cached(timeout=CACHE_TIMEOUT)(
            (cases_by_state)))

    # a simple page that says hello
    app.route('/corona/allStates')(
        cache.cached(timeout=CACHE_TIMEOUT)(
            (cases_for_united_states)))


    return app
