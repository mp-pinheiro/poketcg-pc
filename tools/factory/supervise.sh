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
  # Re-check before the backoff, otherwise a STOP dropped while the session
  # ran would still be followed by one useless minute of sleep (or a respawn
  # if the operator removes STOP inside that window).
  if [ -e .factory/STOP ]; then
    break
  fi
  sleep 60
done
