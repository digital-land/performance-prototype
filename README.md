# Maturity model prototype

Based on the govuk-flask-prototype-kit

### Getting started

We recommend using a virtual env.

Install dependencies

  make init

Get local copy of all the data (can take a while but then you'll have local sqlite dbs for this app)

  make databases

Run flask application

  flask run

### Before pushing changes

The first time you run the tests you will need to install the chromium browser for play-wright

```
python -m playwright install chromium
```

Run the following to eyeball the pages are all still working

```
pytest tests/acceptance -p no:warnings --headed --slowmo 1000
```
