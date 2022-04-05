
init::
	pip install --upgrade pip setuptools
	pip install -r requirements.txt
	npm install

databases::
	curl -qsfL -o digital-land.sqlite3 https://digital-land-production-collection-dataset.s3.eu-west-2.amazonaws.com/digital-land-builder/dataset/digital-land.sqlite3
	curl -qsfL -o entity.sqlite3 https://digital-land-production-collection-dataset.s3.eu-west-2.amazonaws.com/entity-builder/dataset/entity.sqlite3


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
