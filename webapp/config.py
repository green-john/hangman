import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'this should be on an env variable'
    STATIC_FOLDER = "webapp/"
    STATIC_URL_PATH = "/webapp"


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


config = {
    'dev': DevConfig,
    'test': TestConfig
}
