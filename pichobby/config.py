import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '`Secret&`Key!`'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    protocol = 'postgresql://postgres:'
    password = 'Kinsman.'
    host = '@localhost'
    dbase = '/pichobby'
    localPostgress = protocol+password+host+dbase
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB_URI') or localPostgress


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URL') or 'sqlite://'


class ProdConfig(Config):
    DEBUG = False
    sqldb = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or sqldb


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}
