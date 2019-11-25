from flask import Flask
from pichobby.config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize databases
    from pichobby.api import picapi as picapi_blueprint
    app.register_blueprint(picapi_blueprint)

    return app
