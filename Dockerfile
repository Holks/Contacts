FROM python:3.6-alpine

RUN adduser -D smit

WORKDIR ~/smit

RUN apk add -U --no-cache gcc build-base linux-headers ca-certificates  python3-dev libffi-dev libressl-dev libxslt-dev git

RUN git clone https://github.com/Holks/XXXX

COPY requirements.txt requirements.txt

RUN python -m venv venv


RUN venv/bin/pip install --upgrade setuptools
RUN venv/bin/pip install  -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY mdl.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP coinsys.py

RUN chown -R smit:smit ./
USER smit

EXPOSE 5000
ENTRYPOINT ["sh","./boot.sh"]
