import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')


class Development(Config):
    """Configurations for development."""
    DEBUG = True
    APP_SETTINGS = "development"


class Testing(Config):
    """Configurations for testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    DB_NAME = os.getenv('TEST_DB')
    APP_SETTINGS = "testing"


class Production(Config):
    """Configurations for production."""
    DEBUG = False
    TESTING = False
    APP_SETTINGS = "production"


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}
