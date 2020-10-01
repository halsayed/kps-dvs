from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from config import config
from dynamo import list_all_records, read_stream_records
from card_generator import CardGenerator
from flask_socketio import SocketIO
from threading import Lock
import os

app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_CONFIG', 'default')])
bootstrap = Bootstrap(app)
cards = CardGenerator(app.config['CARD_TEMPLATE_DIR'])
socketio = SocketIO(app, async_mode=app.config['ASYNC_MODE'])
thread = None
thread_lock = Lock()


@app.route('/')
def index():

    search = request.args.get('search')
    records = list_all_records(1000, search=search)
    locations = {}

    for location in records:
        locations[location] = cards.render_list(records[location])

    return render_template('index.html', locations=locations,
                           async_mode=socketio.async_mode,
                           search=search)


def background_thread():
    while True:
        socketio.sleep(1.5)
        inserts_by_location, updated_records = read_stream_records()

        if inserts_by_location:
            inserts = {}
            for location in inserts_by_location:
                inserts[location] = cards.render_list(inserts_by_location[location])
            socketio.emit('dashboard_insert', inserts, namespace='/stream')

        if updated_records:
            updates = {}
            for card in updated_records:
                updates[card['id']] = cards.render_card(card)
                print(card)
            socketio.emit('dashboard_update', updates, namespace='/stream')


@socketio.on('connect', namespace='/stream')
def update_dashboard():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
