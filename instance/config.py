import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                os.urandom(16))
    CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True


APP_CONFIG = {'development': DevelopmentConfig,
              'testing': TestingConfig,
              'production': ProductionConfig
              }