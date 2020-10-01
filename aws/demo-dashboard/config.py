import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-west-2')

    DYNAMO_TABLE = os.environ.get('DYNAMO_TABLE', 'xiiot-demo')
    DEFAULT_CARD_TEMPLATE = os.environ.get('DEFAULT_CARD_TEMPLATE', 'default')
    CARD_TEMPLATE_DIR = os.environ.get('CARD_TEMPLATE_DIR', 'templates/cards')

    ASYNC_MODE = os.environ.get('ASYNC_MODE', None)

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    VERIFY_SSL = True


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}


# create logger
log = logging.getLogger()
log.setLevel(Config.LOG_LEVEL)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(Config.LOG_LEVEL)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)