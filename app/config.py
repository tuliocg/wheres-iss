import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'some hard ass string'

class StagingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
        'sqlite:///{}'.format(os.path.join(base_dir, 'database/dev_db.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRD_DATABASE_URL") or \
        'sqlite:///{}'.format(os.path.join(base_dir, 'database/prd_db.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': StagingConfig
}
