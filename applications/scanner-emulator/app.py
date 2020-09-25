import os
import json
import mqtt
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from config import Config
from helpers import allowed_file, certificate_bundle_loaded, unpack_certificate_bundle


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER


@app.route('/')
def main():
    if certificate_bundle_loaded():
        return render_template('index.html', message=Config.LOCATION, vue_file='index.js')
    else:
        return redirect(url_for('upload'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'cert_bundle' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['cert_bundle']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_full_path)
            Config.CA_CERT, Config.CLIENT_CERT, Config.CLIENT_KEY \
                = unpack_certificate_bundle(file_full_path, Config.UPLOAD_FOLDER)
            return redirect(url_for('main'))

    return render_template('upload.html', message=f'No certificate for {Config.LOCATION}')


@app.route('/env')
def env():
    env_list = {}
    for item, value in os.environ.items():
        env_list[item] = value
    return jsonify(env_list)


@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        req = request.form
        barcode = req.get('barcode', 'None')
        payload = {
            'operation': 'checkin',
            'value': barcode,
            'location': Config.LOCATION,
            'rtsp-buffer': Config.RTSP_BUFFER_URL
        }
        mqtt.send_message('checkin-barcode', json.dumps(payload))
        return redirect(url_for('main'))

    return render_template('barcode.html', title='Checkin Item', vue_file='barcode.js')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        req = request.form
        barcode = req.get('barcode', 'None')
        payload = {
            'operation': 'checkout',
            'value': barcode,
            'location': Config.LOCATION,
            'rtsp-buffer': Config.RTSP_BUFFER_URL
        }
        mqtt.send_message('checkout-barcode', json.dumps(payload))
        return redirect(url_for('main'))

    return render_template('barcode.html', title='Checkout Item', vue_file='barcode.js')


if __name__ == '__main__':
    app.run()
