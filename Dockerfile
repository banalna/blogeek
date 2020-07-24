FROM python:3.6-alpine

RUN adduser -D blogeek

WORKDIR /home/blogeek

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

# copy files
COPY app app
COPY migrations migrations
COPY blogeek.py config.py boot.sh ./
RUN chmod +x boot.sh

# env vars
ENV FLASK_APP blogeek.py

RUN chown -R blogeek:blogeek ./
USER blogeek

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]