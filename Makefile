
abbrev_hash := $(shell git rev-parse --short HEAD)

run::
	flask run

init::
	python -m pip install pip-tools
	npm install
	python -m piptools sync requirements/requirements.txt

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

docker-push-candidate: docker-login-public
	docker push $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)
	docker push $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)-testing
	docker push $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)-development
	docker push $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)-live

docker-login-public:
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

.PHONY: test-build
test-build:
	@echo "Building test image"
	@docker compose \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		build application

.PHONY: test
test:
	@echo "Running tests"
	env GIT_ABBREV_COMMIT_HASH=$(abbrev_hash) docker compose \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm application bash -c "wait-for-it database:5432 && flask db upgrade && pytest tests/"

.PHONY: test-debug
test-debug:
	env GIT_ABBREV_COMMIT_HASH=$(abbrev_hash) docker compose \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm application bash
