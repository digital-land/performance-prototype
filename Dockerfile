FROM python:3.10
COPY . /src
WORKDIR /src

RUN curl -qsfL -o digital-land.sqlite3 https://digital-land-production-collection-dataset.s3.eu-west-2.amazonaws.com/digital-land-builder/dataset/digital-land.sqlite3
RUN curl -qsfL -o entity.sqlite3 https://digital-land-production-collection-dataset.s3.eu-west-2.amazonaws.com/entity-builder/dataset/entity.sqlite3

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install curl

EXPOSE 5000
#CMD gunicorn -b 0.0.0.0:5000 application.wsgi:app
