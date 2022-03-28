FROM python:3.10
COPY . /src
WORKDIR /src

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install curl

EXPOSE 5000
CMD gunicorn -b 0.0.0.0:5000 application.wsgi:app
