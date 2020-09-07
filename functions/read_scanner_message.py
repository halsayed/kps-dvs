import logging
import os
import json
import uuid
from time import time
from datetime import datetime


def main(ctx, msg):

    scanner_msg = msg.decode().strip()

    logging.info('================ MQTT Message ===============================')    
    logging.info(f'Data from sensor: {scanner_msg}')
    current_time = datetime.utcfromtimestamp(int(time()))

    message = {
        'id': str(uuid.uuid4()),
        'trigger_time': current_time.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'buffer_before': 5,
        'buffer_after': 15,
        'data' : {
            'operation': None,
            'value': '' 
        }
    }


    # checkin operation
    if scanner_msg[:10] == '[checkin]-':
        message['data']['operation'] = 'checkin'
        message['data']['value'] = scanner_msg[10:]
    # checkout operation
    elif scanner_msg[:11] == '[checkout]-':
        message['data']['operation'] = 'checkout'
        message['data']['value'] = scanner_msg[11:]
    # messagge not defined
    else:
        return 0
        
    return ctx.send(json.dumps(message).encode())