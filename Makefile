.ONESHELL:
SHELL = bash

backend_container := backend
docker_run := docker compose run --rm
docker_backend := $(docker_run) $(backend_container)

-include ./Makefile.properties

hello:
	echo "Hello, world!"

runserver:
	docker exec -it $(backend_container) uvicorn app.main:app --port 9000 --host 0.0.0.0 --reload

runbackend:
	docker compose -f docker-compose.yml up -d --build

coverage:
	$(docker_backend) coverage run --source=app -m pytest
	$(docker_backend) coverage xml


migrate:
	$(docker_backend) alembic upgrade head

migrations:
	$(docker_backend) alembic revision --autogenerate -m $(name)

migrateversion:
	$(docker_backend) alembic upgrade $(version)

stamp:
	$(docker_backend) alembic stamp $(version)

pylint:
	$(docker_backend) pylint ./app --disable=C0114,C0115,C0116,R0903,R0913,C0411 --extension-pkg-whitelist=pydantic --load-plugins pylint_flask_sqlalchemy

mypy:
	$(docker_backend) mypy ./app --install-types --strict

check: pylint \
	mypy \
	tests \

tests:
	docker compose run --rm -e TESTING=true $(backend_container) pytest ./app/tests -x -vv

