import base64
import zipfile
import io
import os
import paho.mqtt.client as mqtt
from config import Config, log
from os import path


def on_connect(mqtt_client, userdata, flags, rc):
    log.info(f'MQTT connected with result code {str(rc)}')
    mqtt_client.subscribe('$SYS/#')


def on_message(mqtt_client, userdata, msg):
    log.info(f'MQTT msg - topic: {msg.topic}, payload: {msg.payload}')


def unpack_certs(b64str, tmpdir='./'):
    data = base64.decodebytes(b64str)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        contents = []
        for entry in archive.filelist:
            suffix = entry.filename.split('_', 1)[1]
            contents.append(suffix)
            archive.extract(entry.filename, tmpdir)
            os.rename(os.path.join(tmpdir, entry.filename),
                      os.path.join(tmpdir, suffix))

        expected = ['CACertificate.crt', 'certificate.crt', 'privateKey.key']
        contents.sort()
        if contents != expected:
            raise Exception("unexpected archive contents: {} != {}".format(contents, expected))

        ca_certs, certfile, keyfile = [os.path.join(tmpdir, fn) for fn in expected]
        return ca_certs, certfile, keyfile


def send_message(topic, message):
    log.info(f'MQTT - connecting to host {Config.MQTT_HOST}:{Config.MQTT_PORT}')
    client.connect(Config.MQTT_HOST, Config.MQTT_PORT, 60)
    client.publish(topic, message)
    log.info(f'MQTT - sent topic: {topic}, payload: {message}')
    client.disconnect()
    log.info('MQTT - disconnected from host')


ca_certificate, client_certificate, client_key = unpack_certs(bytes(Config.CLIENT_CERTIFICATE, encoding='ascii'))

if path.isfile(ca_certificate) and path.isfile(client_certificate) \
        and path.isfile(client_key):
    log.info('MQTT TLS files loaded')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(ca_certs=ca_certificate, certfile=client_certificate, keyfile=client_key)
    client.tls_insecure_set(True)
    log.info('MQTT - client configured ...')




