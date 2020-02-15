FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV CONF_DIR config

RUN mkdir -p /opt/scheduler-backend
WORKDIR /opt/scheduler-backend

COPY requirements.txt /opt/scheduler-backend

RUN pip install -r requirements.txt

COPY . /opt/scheduler-backend
