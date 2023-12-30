.PHONY: backend frontend start stop tests test

SHELL := /bin/bash

backend:
	set "COMPOSE_DOCKER_CLI_BUILD=1" & set "DOCKER_BUILDKIT=1" & docker compose up --build --detach server

frontend:
	set "COMPOSE_DOCKER_CLI_BUILD=1" & set "DOCKER_BUILDKIT=1" & docker compose up --build --detach frontend

start:
	set "COMPOSE_DOCKER_CLI_BUILD=1" & set "DOCKER_BUILDKIT=1" & docker compose up --build --detach

stop:
	docker compose down

logs:
	docker compose logs --tail="all" --follow server frontend

tests:
	cd ./test && pytest .

test:
	cd ./test && pytest $(FILE)

install:
	poetry lock && poetry install --sync
	poetry export --without-hashes --format=requirements.txt --output=requirements.txt
	poetry export --without-hashes --format=requirements.txt --with="style" --output=requirements_style.txt
	poetry export --without-hashes --format=requirements.txt --with="test" --output=requirements_test.txt
	poetry export --without-hashes --format=requirements.txt --with="webserver" --output=requirements_webserver.txt
	poetry export --without-hashes --format=requirements.txt --with="notebooks" --output=requirements_notebooks.txt
