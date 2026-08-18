#!/usr/bin/env bash
set -eu
omp_bin=$(command -v omp)
omp_entry=$(readlink -f "$omp_bin")
export NODE_PATH="$(dirname "$(dirname "$(dirname "$(dirname "$omp_entry")")")")${NODE_PATH:+:$NODE_PATH}"
exec bun "$(dirname "$0")/run.ts" "$@"
