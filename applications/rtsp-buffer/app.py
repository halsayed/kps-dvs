import os
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
from config import config, log
from helpers import get_video_cache_list, video_join_list, combine_videos

app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV') or 'default'])
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    current_time = datetime.utcnow()
    default_buffer_seconds = int(app.config['BUFFER_BEFORE']) + int(app.config['BUFFER_INTERVAL'])
    default_start_time = current_time - timedelta(seconds=default_buffer_seconds)
    default_end_time = current_time - timedelta(seconds=int(app.config['BUFFER_INTERVAL']))
    output_video_filename = f'{str(uuid.uuid4())}.mp4'
    output_video_dir = app.config['VIDEO_DIR']

    # Set defualt values just in case no data on payload
    start_time = default_start_time
    end_time = default_end_time

    if request.method == 'POST':
        if request.values:
            start_time = request.values.get('start_time')
            end_time = request.values.get('end_time')

        if request.json:
            start_time = request.json.get('start_time')
            end_time = request.json.get('end_time')

        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
            end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
        except (ValueError, TypeError):
            log.info('Error in parsing datetime from string, taking default timers')
            start_time = default_start_time
            end_time = default_end_time

        log.info(f'Start Time: {start_time}, End Time: {end_time}')
        video_cache_list = get_video_cache_list(app.config['CACHE_DIR'], app.config['BUFFER_INTERVAL'])
        log.info(video_cache_list)

        # generate list of the required video files and timeframes
        required_video = video_join_list(video_cache_list, start_time, end_time)
        log.info(required_video)
        combine_videos(required_video, os.path.join(output_video_dir, output_video_filename))

        return send_from_directory(output_video_dir, output_video_filename,
                                   mimetype='video/mp4', as_attachment=True)

    return render_template('index.html',
                           title='RTSP-BUFFER',
                           start_time=default_start_time.isoformat(timespec='seconds'),
                           end_time=default_end_time.isoformat(timespec='seconds'))


if __name__ == '__main__':
    app.run()
