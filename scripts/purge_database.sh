#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

. ${SCRIPT_DIR}/_run_psql_cmd.sh

_run_psql_cmd "DROP DATABASE IF EXISTS ${_db_database};" "postgres"
_run_psql_cmd "DROP USER IF EXISTS ${_db_username};" "postgres"
