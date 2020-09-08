import os
import logging
import json
import uuid
import requests
from datetime import datetime, timedelta

LOCATION = 'Undefined'


def init():
    """
    Global functions of shared data between all pipelines. Used to extract the following info:
    - Service Domain location label
    """
    global LOCATION

    logging.info("============ Setting globals to init ============ ")
    host = os.environ.get('UI_SVC_SERVICE_HOST', 'localhost')
    url = f'http://{host}:30003/env'
    r = requests.get(url)
    if r.status_code == 200:
        environ_list = json.loads(r.content)
        LOCATION = environ_list.get('LOCATION', 'Undefined')
    else:
        LOCATION = 'Undefined'
    return


init()


def main(ctx, msg):

    global LOCATION
    scanner_msg = msg.decode().strip()

    logging.info('================ MQTT Message ===============================')    
    logging.info(f'Data from sensor: {scanner_msg}')
    buffer_config = ctx.get_config()
    trigger_time = datetime.utcnow()
    buffer_before = int(buffer_config.get('buffer_before', 5))
    buffer_after = int(buffer_config.get('buffer_after', 15))
    video_start_time = trigger_time - timedelta(seconds=buffer_before)
    video_end_time = trigger_time + timedelta(seconds=buffer_after)

    message = {'data': {
        'operation': '',
        'value': ''
    }}

    # checkin operation
    if scanner_msg[:10] == '[checkin]-':
        message['data']['operation'] = 'checkin'
        message['data']['value'] = scanner_msg[10:]
    # checkout operation
    elif scanner_msg[:11] == '[checkout]-':
        message['data']['operation'] = 'checkout'
        message['data']['value'] = scanner_msg[11:]
    # message not defined, don't log the message from MQTT
    else:
        return 0

    message = {
        'id': str(uuid.uuid4()),
        'location': LOCATION,
        'trigger_time': f'{trigger_time.isoformat(timespec="seconds")}+00:00',
        'buffer_before': int(buffer_config.get('buffer_before', 5)),
        'buffer_after': int(buffer_config.get('buffer_after', 15)),
        'video_start_time': f'{video_start_time.isoformat(timespec="seconds")}+00:00',
        'video_end_time': f'{video_end_time.isoformat(timespec="seconds")}+00:00'
    }
        
    return ctx.send(json.dumps(message).encode())
