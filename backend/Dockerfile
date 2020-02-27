FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /backend
WORKDIR /backend

COPY requirements.txt /backend

RUN pip install -r requirements.txt

COPY . /backend