#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

. ${SCRIPT_DIR}/_run_psql_cmd.sh

_run_psql_cmd "CREATE EXTENSION IF NOT EXISTS postgis" "${_db_database};"