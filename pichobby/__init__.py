from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from pichobby.config import config


db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize databases
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    # Routes
    from pichobby.api import picapi as picapi_blueprint
    app.register_blueprint(picapi_blueprint)

    return app
