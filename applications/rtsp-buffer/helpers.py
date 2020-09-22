from os import path
from datetime import datetime, timedelta
from glob import glob
import ffmpeg


def convert_str_to_datetime(time_string):
    datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')


def get_video_cache_list(cache_dir, interval):
    video_files = glob(path.join(cache_dir, '*.mp4'))
    video_files.sort()
    video_list = []
    for video in video_files:
        video_time = time_from_filename(video)
        video_list.append({
            'video': video,
            'start': video_time,
            'end': video_time + timedelta(seconds=interval)
        })

    return video_list


def time_from_filename(filename):
    return datetime.strptime(path.basename(filename)[:-4], '%Y-%m-%dT%H-%M-%SZ')


def video_join_list(video_list, start_time, end_time):
    join_list = []
    entry = {
        'video': 'video_name',
        'partial': True,
        'start': 0,
        'end': 10
    }
    for video in video_list:
        # if the buffer video within the required time range
        if video['start'] >= start_time and video['end'] <= end_time:
            entry = {'video': video['video'], 'partial': False, 'start': 0, 'end': _get_video_seconds(video)}
            join_list.append(entry)

        # if the buffer video starts before the required time, include partially
        elif video['start'] <= start_time < video['end']:
            start = _difference_in_seconds(video['start'], start_time)
            interval = _get_video_seconds(video)
            if interval - start <= _difference_in_seconds(start_time, end_time):
                end = interval
            else:
                end = start + _difference_in_seconds(start_time, end_time)
            entry = {'video': video['video'], 'partial': True, 'start': start, 'end': end}
            join_list.append(entry)

        # if the buffer video ends after the required time frame, include partially
        elif video['start'] < end_time <= video['end']:
            start = 0
            interval = _get_video_seconds(video)
            if interval > _difference_in_seconds(video['start'], end_time):
                end = _difference_in_seconds(video['start'], end_time)
            else:
                end = interval
            entry = {'video': video['video'], 'partial': True, 'start': start, 'end': end}
            join_list.append(entry)

    return join_list


def _get_video_seconds(video):
    return _difference_in_seconds(video['start'], video['end'])


def _difference_in_seconds(start, end):
    return int((end - start).total_seconds())


def combine_videos(video_list, output_file):
    videos = []
    for video in video_list:
        if video['partial']:
            videos.append(ffmpeg.input(video['video'], ss=video['start'], to=video['end']))
        else:
            videos.append(ffmpeg.input(video['video']))

    joined = ffmpeg.concat(*videos)
    out = ffmpeg.output(joined, output_file)
    out.run()

