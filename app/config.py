import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'some hard ass string'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class StagingConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': StagingConfig
}
