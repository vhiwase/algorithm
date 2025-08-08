import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_should_be_changed_in_production'
    DEBUG = os.environ.get('FLASK_DEBUG') == '1'
    # Add other configuration variables here
    # For example, logging configuration, database URIs, etc.
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # More restrictive settings for production
    LOG_LEVEL = 'WARNING'

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
