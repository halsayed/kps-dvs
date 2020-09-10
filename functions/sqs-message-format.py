import logging
import json


def main(ctx, msg):
    message = json.loads(msg)

    logging.info('================ Local datastream Message ============================')
    logging.info(f'Data from stream: {message}')

    message['source_type'] = 'barcode_scanner'
    message['display_fields'] = ['trigger_time', 'location', 'data']

    return ctx.send(json.dumps(message).encode())
