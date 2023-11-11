#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit

createdb "${AIRFLOW_DB_DATABASE}" 2>/dev/null || true

psql -h "${AIRFLOW_DB_HOST}" -p "${AIRFLOW_DB_PORT}" -c "CREATE USER ${AIRFLOW_DB_USERNAME} WITH ENCRYPTED PASSWORD '${AIRFLOW_DB_PASSWORD}';" || true
psql -h "${AIRFLOW_DB_HOST}" -p "${AIRFLOW_DB_PORT}" -c "GRANT ALL PRIVILEGES ON DATABASE ${AIRFLOW_DB_DATABASE} TO ${AIRFLOW_DB_USERNAME};" || true
psql -h "${AIRFLOW_DB_HOST}" -p "${AIRFLOW_DB_PORT}" -c "GRANT ALL ON SCHEMA public TO ${AIRFLOW_DB_USERNAME};" || true
