#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$(realpath ${SCRIPT_DIR}/..)

if [ ! -f ${ROOT_DIR}/.envrc ];
then
  echo 'No .envrc file exists. Copying from .envrc.example'
  cp -v -n "${ROOT_DIR}/.envrc.example" "${ROOT_DIR}/.envrc"
  exit 1
fi;
