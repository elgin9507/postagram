IMAGE_NAME=postagram
DOCS_SOURCE=docs/source

build:
	docker build -t $(IMAGE_NAME) .

up:
	docker-compose up -d

buildup: build up

down:
	docker-compose down

logs:
	docker-compose logs -f

shell: up
	docker-compose exec postagram /bin/bash

makemigrations: up
	docker-compose exec postagram alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

migrate: up
	docker-compose exec postagram alembic upgrade head

wait_for_mysql:
	@echo "Waiting for MySQL to start..."
	@while ! docker-compose exec mysql mysqladmin ping -h"localhost" --silent; do sleep 1; done
	@sleep 3

dev: build up wait_for_mysql migrate
	@echo "Development environment is ready"