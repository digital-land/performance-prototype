
init::
	pip install --upgrade pip setuptools
	pip install -r requirements.txt
	npm install


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
