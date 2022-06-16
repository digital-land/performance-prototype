FROM ubuntu:22.04 AS base

RUN apt-get update \
    && apt-get upgrade --assume-yes \
    && apt-get install --assume-yes  \
      build-essential \
      git curl rsync netcat wait-for-it sqlite3 \
      python3.10 python3-pip \
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
#RUN curl -s https://deb.nodesource.com/setup_16.x | bash \
#    && apt-get install --assume-yes nodejs \
#    && npm install \
#    && apt-get remove --assume-yes nodejs \
#    && apt-get clean \
#    && apt-get autoclean --assume-yes

ENV FLASK_ENV=production
ENV FLASK_CONFIG=config.Config
ENV FLASK_APP=application.wsgi:app
EXPOSE $PORT

RUN make databases

FROM base AS testing
RUN pip install --no-cache-dir \
    pytest==7.1.2 \
    playwright==1.22.0 \
    pytest-playwright==0.3.0 \
    pytest-mock==3.7.0

RUN apt-get install --assume-yes \
      libglib2.0-0 \
      libnss3 \
      libnspr4 \
      libatk1.0-0 \
      libatk-bridge2.0-0 \
      libcups2 \
      libdrm2 \
      libdbus-1-3 \
      libxkbcommon0 \
      libxcomposite1 \
      libxdamage1 \
      libxfixes3 \
      libxrandr2 \
      libgbm1 \
      libpango-1.0-0 \
      libcairo2 \
      libasound2 \
      libatspi2.0-0 \
    && python3 -m playwright install chromium

FROM testing AS development
CMD flask db upgrade && flask run

FROM base AS live
RUN rm -rf tests
RUN apt-get remove --assume-yes build-essential \
    && apt-get clean \
    && apt-get autoclean --assume-yes
CMD gunicorn -b 0.0.0.0:$PORT application.wsgi:app --timeout 120 --workers=2 --threads=4 --worker-class=gthread
