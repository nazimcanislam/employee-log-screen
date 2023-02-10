FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONNUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . .

RUN pip install -r requirements.txt
