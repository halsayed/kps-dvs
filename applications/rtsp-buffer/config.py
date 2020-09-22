import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    BUFFER_INTERVAL = int(os.environ.get('BUFFER_INTERVAL', 10))
    BUFFER_BEFORE = int(os.environ.get('BUFFER_BEFORE', 10))
    CACHE_DIR = os.environ.get('CACHE_DIR', '/cache')
    VIDEO_DIR = os.environ.get('VIDEO_DIR', '/video')

    NATS_SERVICE_HOST = os.environ.get('NATS_SERVICE_HOST', 'nats')
    NATS_SERVICE_PORT = os.environ.get('NATS_SERVICE_PORT', '4222')
    NATS_URL = f'{NATS_SERVICE_HOST}:{NATS_SERVICE_PORT}'
    NATS_TOPIC = os.environ.get('NATS_TOPIC', None)

    LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_HOST = 'localhost'


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    REDIS_HOST = 'localhost'


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig(),
    'testing': TestConfig(),
    'production': ProductionConfig(),

    'default': DevelopmentConfig()
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
