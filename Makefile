run::
	flask run

init::
	python -m pip install pip-tools
	npm install
	python -m piptools sync requirements/requirements.txt

deploy: databases push release

databases::
# Prefer local sqlite3 if available (e.g. in development environment to reduce rebuild time)
# When run in CI this should always pull a fresh version when building image
	[ -f digital-land.sqlite3 ] || curl -qsfL -o digital-land.sqlite3 https://datasette.planning.data.gov.uk/digital-land.db
	bin/load.sh

black:
	black .

black-check:
	black --check .

flake8:
	flake8 --exclude .venv,node_modules

lint: black-check flake8
frontend-assets: javascripts stylesheets

javascripts:
	npm run copyjs
	npm run nps copy.javascripts

stylesheets:
	npm run nps build.stylesheets

watch:
	npm run watch

upgrade-db:
	flask db upgrade

downgrade-db:
	flask db downgrade

reqs:
	python -m piptools compile requirements/requirements.in

sync:
	 python -m piptools sync requirements/requirements.txt

