FROM python:3.10
COPY . /src
WORKDIR /src

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install curl

ENV FLASK_ENV=production
ENV FLASK_CONFIG=config.Config
ENV FLASK_APP=application.wsgi:app

EXPOSE $PORT
CMD gunicorn -b 0.0.0.0:$PORT application.wsgi:app --timeout 120 --workers=2 --threads=4 --worker-class=gthread
