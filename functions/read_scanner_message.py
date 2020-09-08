import logging
import json
import uuid
from datetime import datetime


def main(ctx, msg):

    scanner_msg = msg.decode().strip()

    logging.info('================ MQTT Message ===============================')    
    logging.info(f'Data from sensor: {scanner_msg}')
    current_time = f'{datetime.utcnow().isoformat(timespec="seconds")}+00:00'
    buffer_config = ctx.get_config()

    message = {}

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
        'trigger_time': current_time,
        'buffer_before': int(buffer_config.get('buffer_before', 5)),
        'buffer_after': int(buffer_config.get('buffer_after', 15))
    }
        
    return ctx.send(json.dumps(message).encode())