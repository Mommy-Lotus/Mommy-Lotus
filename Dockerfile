FROM python:3.10-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add gcc g++ git

WORKDIR /mommy-lotus
RUN mkdir -p /mommy-lotus/servers/logs

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN git config --global --add safe.directory /mommy-lotus

ENTRYPOINT [ "python3", "lotus.py" ]
