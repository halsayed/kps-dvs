import os
import logging


class Config:
    APP_NAME = os.environ.get('APP_NAME', 'Barcode Reader Emulator')
    SHORT_NAME = os.environ.get('SHORT_NAME', 'BRE')
    MQTT_DIR = os.environ.get('MQTT_DIR', 'mqtt')
    MQTT_HOST = os.environ.get('MQTT_HOST', 'localhost')
    MQTT_PORT = os.environ.get('MQTT_PORT', 1883)
    MQTT_READY = False
    LOCATION = os.environ.get('LOCATION', 'Undefined')
    CLIENT_CERTIFICATE = os.environ.get('CLIENT_CERTIFICATE')

    LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)


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

