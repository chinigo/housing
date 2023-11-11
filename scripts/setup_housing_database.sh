#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit

createdb "${HOUSING_DB_DATABASE}" 2>/dev/null || true

psql -h "${HOUSING_DB_HOST}" -p "${HOUSING_DB_PORT}" -c "CREATE SCHEMA IF NOT EXISTS data" "${HOUSING_DB_DATABASE}" || true
psql -h "${HOUSING_DB_HOST}" -p "${HOUSING_DB_PORT}" -c "CREATE USER ${HOUSING_DB_USERNAME} WITH ENCRYPTED PASSWORD '${HOUSING_DB_PASSWORD}';" || true
psql -h "${HOUSING_DB_HOST}" -p "${HOUSING_DB_PORT}" -c "GRANT ALL PRIVILEGES ON DATABASE ${HOUSING_DB_DATABASE} TO ${HOUSING_DB_USERNAME};" || true
psql -h "${HOUSING_DB_HOST}" -p "${HOUSING_DB_PORT}" -c "CREATE EXTENSION IF NOT EXISTS postgis" "${HOUSING_DB_DATABASE}" || true
