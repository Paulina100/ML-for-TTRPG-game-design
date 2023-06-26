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

test:
	cd ./test && pytest .

.PHONY: all backend frontend start stop test