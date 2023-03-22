# Pull official image
FROM --platform=linux/amd64 python:3.11-slim

# Set the app work directory
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./ ./
