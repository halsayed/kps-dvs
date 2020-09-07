FROM python:3-alpine

# application folder
RUN mkdir /app
WORKDIR /app

ADD . /app

ENV FLASK_APP "/app/app.py"

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]