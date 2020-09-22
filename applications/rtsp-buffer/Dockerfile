FROM python:3-alpine

RUN apk add --update --no-cache python3-dev libffi-dev gcc musl-dev make ffmpeg tzdata supervisor
RUN rm -rf /car/cache/apk/*

# set timezonet to UTC
RUN cp /usr/share/zoneinfo/UTC /etc/localtime
RUN echo "UTC" >> /etc/timezone
RUN apk del tzdata

# temp cache and finished video folder
RUN mkdir /cache
RUN mkdir /video

# application folder
RUN mkdir /app
WORKDIR /app

# python requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# set default environmnet variables
ENV CACHE_DIR="/cache"
ENV BUFFER_INTERVAL=10

# Supervisor config
ADD /supervisor /src/supervisor
RUN mkdir /var/log/supervisord

# video capture script
COPY start_capture.sh /app/
RUN chmod +x /app/start_capture.sh
# buffer clean up cron
RUN echo "5 * * * *   find $CACHE_DIR -name '*.mp4' -type f -mmin +15 -exec rm -f {} \;" > /etc/crontabs/root

# application scripts
COPY *.py /app/
COPY templates /app/templates

EXPOSE 80
CMD ["supervisord","-c","/src/supervisor/service_script.conf"]