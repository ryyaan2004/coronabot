FROM python:3.6-alpine
RUN apk add gcc musl-dev && pip install pipenv

COPY Pipfile /opt
WORKDIR /opt
RUN pipenv lock --requirements > requirements.txt && \
    pip install -r /opt/requirements.txt && \
    pip install gunicorn

ADD src/ /opt/coronabot

ENV FLASK_APP=/opt/coronabot/coronabot.py
ENV PORT=5000
WORKDIR /opt/coronabot
CMD exec gunicorn -b :$PORT coronabot:app
