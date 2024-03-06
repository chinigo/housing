# Meta
.PHONY: all
all: .envrc

MAKEFLAGS=--jobs=3
.PHONY: dev
dev: $(MAKE) start_prefect serve_deployments open_prefect_ui

.PHONY: initialize
initialize: .envrc setup_python setup_databases

.PHONY: purge
purge: purge_python purge_databases

# Environment
.envrc:
	./scripts/confirm_envrc.sh


# Databases
.PHONY: setup_databases
setup_databases: create_housing_database create_prefect_database setup_prefect_database

.PHONY: purge_databases
purge_databases: purge_housing_database purge_prefect_database

.PHONY: create_housing_database
create_housing_database:
	_db_database=${HOUSING_DB_DATABASE} _db_host=${HOUSING_DB_HOST} _db_password=${HOUSING_DB_PASSWORD} _db_port=${HOUSING_DB_PORT} _db_username=${HOUSING_DB_USERNAME} ./scripts/create_database.sh
	_db_database=${PREFECT_DB_DATABASE} _db_host=${PREFECT_DB_HOST} _db_port=${PREFECT_DB_PORT} ./scripts/install_postgis.sh

.PHONY: create_prefect_database
create_prefect_database:
	_db_database=${PREFECT_DB_DATABASE} _db_host=${PREFECT_DB_HOST} _db_password=${PREFECT_DB_PASSWORD} _db_port=${PREFECT_DB_PORT} _db_username=${PREFECT_DB_USERNAME} ./scripts/create_database.sh

.PHONY: purge_housing_database
purge_housing_database:
	_db_database=${HOUSING_DB_DATABASE} _db_host=${HOUSING_DB_HOST} _db_password=${HOUSING_DB_PASSWORD} _db_port=${HOUSING_DB_PORT} _db_username=${HOUSING_DB_USERNAME} ./scripts/purge_database.sh

.PHONY: purge_prefect_database
purge_prefect_database:
	_db_database=${PREFECT_DB_DATABASE} _db_host=${PREFECT_DB_HOST} _db_password=${PREFECT_DB_PASSWORD} _db_port=${PREFECT_DB_PORT} _db_username=${PREFECT_DB_USERNAME} ./scripts/purge_database.sh

.PHONY: setup_prefect_database
setup_prefect_database:
	prefect server database reset --yes


# Prefect
.PHONY: open_prefect_ui
open_prefect_ui:
	sleep 2 && open "http://${PREFECT_SERVER_API_HOST}:${PREFECT_SERVER_API_PORT}"

.PHONY: serve_deployments
serve_deployments:
	python ./main.py

.PHONY: start_prefect
start_prefect:
	prefect server start


# Python
.PHONY: setup_python
setup_python: install_python upgrade_pip install_pipenv install_dependencies

.PHONY: install_dependencies
install_dependencies:
	pipenv install

.PHONY: install_pipenv
install_pipenv:
	pip install pipenv

.PHONY: install_python
install_python:
	asdf install python

.PHONY: purge_python
purge_python:
	rm -rf .venv

.PHONY: upgrade_pip
upgrade_pip:
	pip install --upgrade pip
