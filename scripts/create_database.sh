#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

. ${SCRIPT_DIR}/_run_psql_cmd.sh

createdb "${_db_database}" 2>/dev/null || true

_run_psql_cmd "CREATE USER ${_db_username} WITH ENCRYPTED PASSWORD '${_db_password}';" "${_db_database}"
_run_psql_cmd "GRANT ALL PRIVILEGES ON DATABASE ${_db_database} TO ${_db_username};" "${_db_database}"