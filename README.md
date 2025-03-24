
# Performance application
# ⚠️ Inactive

This application is no longer deployed anywhere. The data collected during it's use has
been backed up and is available in [data/database_backup.dump](data/database_backup.dump)


[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/digital-land/performance-prototype/blob/main/LICENSE)
[![Run pipeline](https://github.com/digital-land/brownfield-land-collection/actions/workflows/run.yml/badge.svg)](https://github.com/digital-land/performance-prototype/actions/workflows/deploy.yml)

Pages intended to help the team show progress in collecting planning data, identify gaps and issues in collecting the data and helping the team prioritise its work.

### Getting started

The application is based on the govuk-flask-prototype-kit and uses a Postgres database.

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python [requirements](requirements.txt), [makerules](https://github.com/digital-land/makerules) and other dependencies. Requires GNU Make 4.0 or newer.

Install dependencies

    make init

Get local copy of all the data (can take a while but then you'll have local sqlite dbs for this app)

    make databases

Run flask application

    make run

### Before pushing changes

The first time you run the tests you will need to install the chromium browser for play-wright

    python -m playwright install chromium

Run the following to eyeball the pages are all still working

    pytest tests/acceptance -p no:warnings --headed --slowmo 1000
