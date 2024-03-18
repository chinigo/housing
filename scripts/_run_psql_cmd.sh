#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit

_run_psql_cmd () {
  psql -e -h "${_db_host}" -p "${_db_port}" -c "${1}" "${2}" || true
}
