import logging
import json
import requests
import io
import pickle
from time import sleep
from datetime import datetime


def main(ctx, msg):
    scanner_msg = msg.decode().strip()

    logging.info('================ MQTT Message ===============================')
    logging.info(f'Data from sensor: {scanner_msg}')

    msg_dict = json.loads(scanner_msg)
    wait_time = int(msg_dict['buffer_after']) + 20
    logging.info(f'Sleeping for {wait_time} seconds')
    sleep(wait_time)

    try:
        start_time = datetime.strptime(msg_dict['video_start_time'], '%Y-%m-%dT%H:%M:%S+00:00')
        end_time = datetime.strptime(msg_dict['video_end_time'], '%Y-%m-%dT%H:%M:%S+00:00')
        payload = {
            'start_time': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end_time': end_time.strftime('%Y-%m-%dT%H:%M:%S')}
    except (ValueError, TypeError):
        logging.info('start and end time error or not provided, going with default')
        payload = {}

    if msg_dict.get('rtsp-buffer'):
        headers = {'Content-Type': 'application/json'}
        url = msg_dict.get('rtsp-buffer')
        logging.info(f'Payload: {payload}')
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        logging.info(f'Request code: {r.status_code}, header: {r.headers}')
    else:
        logging.info('No RTSP buffer provided, exiting...')
        return None

    if r.status_code == 200:
        msg_dict.update({
            'video_filename': f'{msg_dict["id"]}.mp4',
            'video_content': r.content
        })

        temp_file = io.BytesIO()
        pickle.dump(msg_dict, temp_file)

        ctx.send(temp_file.getvalue())
