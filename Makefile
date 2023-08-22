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
	poetry export --without-hashes --format=requirements.txt --with="style,test,webserver" --output=requirements.txt
	poetry lock && poetry install --sync