import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import mqtt
from config import Config


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html', message=Config.LOCATION, vue_file='index.js')


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
        mqtt.send_message('checkin-barcode', f'[checkin]-{barcode}')
        return redirect(url_for('main'))

    return render_template('barcode.html', title='Checkin Item', vue_file='barcode.js')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        req = request.form
        barcode = req.get('barcode', 'None')
        mqtt.send_message('checkout-barcode', f'[checkout]-{barcode}')
        return redirect(url_for('main'))

    return render_template('barcode.html', title='Checkout Item', vue_file='barcode.js')


if __name__ == '__main__':
    app.run()
