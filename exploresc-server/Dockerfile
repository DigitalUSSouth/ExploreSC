FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3-virtualenv python3-dev python3-pip

COPY api2/requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /app
EXPOSE 8000
ENTRYPOINT gunicorn api:app -w 2 --bind 0.0.0.0:8000