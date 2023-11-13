all: run_airflow

initialize: install_python upgrade_pip install_airflow setup_housing_database setup_airflow_database

purge:
	rm -rf .direnv airflow

install_python:
	asdf install python

install_airflow:
	pip install --quiet --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_MINOR_VERSION}.txt" "apache-airflow[postgres]==${AIRFLOW_VERSION}"
	airflow users list -o json | jq --exit-status "select(.[].username == \"admin\")" &&\
		airflow users delete -u admin || true
	airflow users list -o json | jq --exit-status "select(.[].username == \"${AIRFLOW_WEB_USERNAME}\")" ||\
 		airflow users create --username "${AIRFLOW_WEB_USERNAME}" --password "${AIRFLOW_WEB_PASSWORD}" --role Admin --email admin --firstname admin --lastname admin

run_airflow:
	airflow standalone

setup_housing_database:
	./scripts/setup_housing_database.sh

setup_airflow_database:
	./scripts/setup_airflow_database.sh

upgrade_pip:
	pip install --upgrade pip
