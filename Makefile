
abbrev_hash := $(shell git rev-parse --short HEAD)

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
	[ -f digital-land.sqlite3 ] || curl -qsfL -o digital-land.sqlite3 https://digital-land-production-collection-dataset.s3.eu-west-2.amazonaws.com/digital-land-builder/dataset/digital-land.sqlite3
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

test:
	python -m pytest

reqs:
	python -m piptools compile requirements/requirements.in

sync:
	 python -m piptools sync requirements/requirements.txt

docker-push-candidate: docker-login-public
	docker push $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)
	docker push $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)-development
	docker push $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)-live

docker-promote-candidate: docker-login-public
ifeq (, $(ENVIRONMENT))
	$(error "No environment specified via $$ENVIRONMENT, please pass as make argument")
endif
	docker pull $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)-live
	docker tag $(DOCKER_REPO)/$(APPLICATION):$(abbrev_hash)-live $(DOCKER_REPO)/$(APPLICATION):$(ENVIRONMENT)
	docker push $(DOCKER_REPO)/$(APPLICATION):$(ENVIRONMENT)

docker-login-public:
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

cf-login:
	cf api https://api.london.cloud.service.gov.uk
	cf auth

cf-deploy: cf-login
ifeq (, $(ENVIRONMENT))
	$(error "No environment specified via $$ENVIRONMENT, please pass as make argument")
endif
	cf target -o dluhc-digital-land -s $(ENVIRONMENT)
	cf push $(ENVIRONMENT)-$(APPLICATION) --docker-image $(DOCKER_REPO)/$(APPLICATION):$(ENVIRONMENT)

docker-dev-build:
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.development.yml \
		build application

docker-dev-up:
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.development.yml \
		up

.PHONY: docker-test
docker-test:
	env GIT_ABBREV_COMMIT_HASH=$(abbrev_hash) docker-compose \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm application bash -c "wait-for-it database:5432 && flask db upgrade && pytest tests/"

.PHONY: docker-test-debug
docker-test-debug:
	env GIT_ABBREV_COMMIT_HASH=$(abbrev_hash) docker-compose \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm application bash
