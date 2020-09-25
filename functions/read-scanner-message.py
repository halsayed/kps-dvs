import logging
import json
import uuid
from datetime import datetime, timedelta


def main(ctx, msg):

    scanner_msg = json.loads(msg)

    logging.info('================ MQTT Message ===============================')    
    logging.info(f'Data from sensor: {scanner_msg}')
    buffer_config = ctx.get_config()
    trigger_time = datetime.utcnow()
    location = scanner_msg.get('location', 'Undefined')
    buffer_before = int(buffer_config.get('buffer_before', 5))
    buffer_after = int(buffer_config.get('buffer_after', 15))
    video_start_time = trigger_time - timedelta(seconds=buffer_before)
    video_end_time = trigger_time + timedelta(seconds=buffer_after)

    message = {
        'id': str(uuid.uuid4()),
        'location': location,
        'trigger_time': f'{trigger_time.isoformat(timespec="seconds")}+00:00',
        'buffer_before': int(buffer_config.get('buffer_before', 5)),
        'buffer_after': int(buffer_config.get('buffer_after', 15)),
        'video_start_time': f'{video_start_time.isoformat(timespec="seconds")}+00:00',
        'video_end_time': f'{video_end_time.isoformat(timespec="seconds")}+00:00',
        'operation': scanner_msg.get('operation'),
        'value': scanner_msg.get('value'),
        'rtsp-buffer': scanner_msg.get('rtsp-buffer')
    }
    logging.info(f'message before sending: {message}')
        
    return ctx.send(json.dumps(message).encode())
