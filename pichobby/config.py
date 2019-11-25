import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
    SQLACHEMY_DATABASE_URI = os.environ.get('DEV_DB_URI') or localPostgress


class TestConfig(Config):
    TESTING = True
    SQLACHEMY_DATABASE_URI = os.environ.get('TEST_DB_URL') or 'sqlite://'


class ProdConfig(Config):
    DEBUG = False
    sqldb = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLACHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or sqldb


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}
