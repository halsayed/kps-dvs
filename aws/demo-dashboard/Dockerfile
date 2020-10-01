FROM python:3-alpine

RUN apk add --update --no-cache tzdata
RUN rm -rf /car/cache/apk/*

# set timezonet to UTC
RUN cp /usr/share/zoneinfo/UTC /etc/localtime
RUN echo "UTC" >> /etc/timezone
RUN apk del tzdata

# install gevent
RUN apk add --no-cache --virtual .build-deps \
    python3-dev \
    libffi-dev \
    gcc  \
    musl-dev \
    make \
    && pip install --upgrade pip \
    && pip install --no-cache-dir gevent-websocket \
    && apk del .build-deps

# application folder
RUN mkdir /app
WORKDIR /app

# python requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# application scripts
COPY *.py /app/
COPY templates /app/templates
COPY static /app/static

EXPOSE 5000
ENTRYPOINT ["python", "-u"]
CMD ["/app/app.py"]
