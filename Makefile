.ONESHELL:
.DEFAULT_GOAL := help

SHELL := /bin/bash

DEV_COMPOSE := @docker-compose --project-name muoh -f .docker/docker-compose.yml
TEST_COMPOSE := @docker-compose --project-name muoh-test -f .docker/docker-compose.test.yml


.PHONY: help rebuild build up run stop down down-tests down-all build-test stop-test run-tests test migrate apply-migrations

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

rebuild: down build ## rebuild base Docker images

build: ## Build base Docker images
	$(DEV_COMPOSE) build --no-cache

stop: ## stop Docker containers without removing them. Useful if up command is run in detached mode
	$(DEV_COMPOSE) stop

run up: ## run the project
	$(DEV_COMPOSE) run --service-ports --rm api || true
	$(MAKE) stop

down: ## stop and remove Docker containers
	$(DEV_COMPOSE) down --remove-orphans

down-tests:
	$(TEST_COMPOSE) down --remove-orphans

down-all: down down-tests

build-test: ## Build base Docker images
	$(TEST_COMPOSE) build --no-cache

stop-test:
	$(TEST_COMPOSE) stop

run-tests: ## Execute pytest unit tests
	$(TEST_COMPOSE) run --rm collection-test sh -c 'alembic upgrade head && pytest tests/${route}'

test:
	$(MAKE) run-tests || true
	$(MAKE) stop-test

migrate: ## Generate migrations e.g. make migrate msg='migration'
	$(DEV_COMPOSE) run --rm api sh -c 'alembic revision --autogenerate -m "${msg}"'

apply-migrations: ## Generate migrations
	$(DEV_COMPOSE) run --rm api sh -c 'alembic upgrade head'
