#!/usr/bin/env bash
# Supervised port-factory session: restart the exact-`start` loop until the
# operator drops `.factory/STOP` or the restart budget runs out. A session
# that reaches `complete`/`stalled` exits cheaply and re-verifies each minute.
set -u
cd "$(dirname "$0")/../.." || exit 1
n=0
while [ ! -e .factory/STOP ] && [ "$n" -lt 500 ]; do
  omp --print start
  n=$((n+1))
  sleep 60
done
