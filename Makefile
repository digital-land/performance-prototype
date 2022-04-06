
init::
	python -m pip install --upgrade pip
	python -m pip install pip-tools
	npm install
	pip install -r requirements.txt

reqs::
	python -m piptools compile requirements/requirements.in

sync:
	python -m piptools sync requirements/requirements.txt

deploy: databases push release

databases::
	curl -qsfL -o digital-land.sqlite3 https://digital-land-production-collection-dataset.s3.eu-west-2.amazonaws.com/digital-land-builder/dataset/digital-land.sqlite3
	bin/load.sh

black:
	black .

black-check:
	black --check .

flake8:
	flake8 --exclude .venv,node_modules

lint: black-check flake8

run::
	flask run

frontend-assets: javascripts stylesheets 

javascripts:
	npm run copyjs
	npm run nps copy.javascripts

stylesheets:
	npm run nps build.stylesheets

watch:
	npm run watch
