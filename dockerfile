# syntax=docker/dockerfile:1

FROM python:3.13.1-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

