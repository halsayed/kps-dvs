import paho.mqtt.client as mqtt
from config import Config, log
from helpers import certificate_bundle_loaded


def on_connect(mqtt_client, userdata, flags, rc):
    log.info(f'MQTT connected with result code {str(rc)}')
    mqtt_client.subscribe('$SYS/#')


def on_message(mqtt_client, userdata, msg):
    log.info(f'MQTT msg - topic: {msg.topic}, payload: {msg.payload}')


def send_message(topic, message):
    if not Config.MQTT_READY:
        log.info('MQTT certificate not loaded, unpacking from zip')
        load_client_certificate()
    log.info(f'MQTT - connecting to host {Config.MQTT_HOST}:{Config.MQTT_PORT}')
    client.connect(Config.MQTT_HOST, Config.MQTT_PORT, 60)
    client.publish(topic, message)
    log.info(f'MQTT - sent topic: {topic}, payload: {message}')
    client.disconnect()
    log.info('MQTT - disconnected from host')


def load_client_certificate():
    if certificate_bundle_loaded():
        client.tls_set(ca_certs=Config.CA_CERT, certfile=Config.CLIENT_CERT, keyfile=Config.CLIENT_KEY)
    else:
        raise Exception('Certificate bundle not loaded on the client.')
    client.tls_insecure_set(True)
    Config.MQTT_READY = True
    log.info('MQTT - certificate loaded')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message





