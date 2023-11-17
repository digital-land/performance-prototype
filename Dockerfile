FROM ubuntu:22.04 AS base

RUN apt-get update \
    && apt-get upgrade --assume-yes \
    && apt-get install --assume-yes  \
      build-essential \
      git curl rsync netcat wait-for-it sqlite3 \
      python3.10 python3-pip  nodejs npm \
    && apt-get clean \
    && apt-get autoclean --assume-yes

WORKDIR /app

# We copy only the requirements files across here,
# meaning we can avoid rebuilding packages if only
# the application has changed.
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements /app/requirements
RUN pip install --upgrade pip pip-tools
RUN python3 -m piptools sync \
    --pip-args="--no-cache-dir"  \
    requirements/requirements.txt

COPY . /app
# RUN set -ex; \
#   curl -s https://deb.nodesource.com/setup_19.x | bash;\
#   apt-get install --assume-yes nodejs; \

RUN npm install;

ENV FLASK_ENV=production
ENV FLASK_CONFIG=config.Config
ENV FLASK_APP=application.wsgi:app
EXPOSE $PORT

RUN make databases

FROM base AS development
ENV FLASK_ENV=development
ENV FLASK_CONFIG=config.DevelopmentConfig
RUN pip install --no-cache-dir pytest==7.1.2
CMD flask db upgrade && flask run -p $PORT -h 0.0.0.0

FROM base AS live
RUN rm -rf tests
RUN set -ex; \
  apt-get remove --assume-yes \
    nodejs \
    build-essential; \
  apt-get clean; \
  apt-get autoclean --assume-yes
CMD gunicorn -b 0.0.0.0:$PORT application.wsgi:app --timeout 120 --workers=2 --threads=4 --worker-class=gthread
