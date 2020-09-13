import logging
import json


def main(ctx, msg):
    message = json.loads(msg)

    logging.info('================ Local datastream Message ============================')
    logging.info(f'Data from stream: {message}')
    message['source_type'] = 'barcode_scanner'

    return ctx.send(json.dumps(message).encode())
