all: backend frontend

backend:
	docker build . -f docker/Dockerfile_server
	docker-compose up -d server

frontend:
	docker build . -f docker/Dockerfile_frontend
	docker-compose up -d frontend

start:
	docker-compose up -d

stop:
	docker-compose down

tests:
	cd ./test && pytest .

test:
	cd ./test && pytest $(FILE)

.PHONY: all backend frontend start stop tests test