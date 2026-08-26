#!/usr/bin/env bash
# Supervised port-factory session: restart the exact-`start` loop until the
# operator drops `.factory/STOP` or the restart budget runs out. A session
# that reaches `complete`/`stalled` exits cheaply and re-verifies each minute.
#
# `omp --print` buffers the whole transcript until the pass ends, so the pane
# would otherwise sit silent for minutes; the live feed below tails the shared
# landings ledger instead, printing one line per fleet-wide landing.
set -u
cd "$(dirname "$0")/../.." || exit 1
touch .factory/landings.jsonl
tail -Fn0 .factory/landings.jsonl 2>/dev/null \
  | jq --unbuffered -r '"landed  " + ((.routines // []) | join(",")) + "  gate=" + ((.seconds_gate // 0) | tostring) + "s"' &
feed=$!
trap 'kill "$feed" 2>/dev/null' EXIT
# The orchestrator drives deterministic tooling; translation quality lives in
# the repo-pinned candidate agents, so the session model stays on the
# sustainable tier and opus is reserved for capability work and the gen-12+
# retry ladder.
model="${POKETCG_LOOP_MODEL:-anthropic/claude-sonnet-5:high}"
n=0
while [ ! -e .factory/STOP ] && [ "$n" -lt 500 ]; do
  n=$((n+1))
  printf 'supervise: pass %d begin %s (transcript prints when the pass ends)\n' "$n" "$(date +%H:%M:%S)"
  omp --print --model "$model" start
  rc=$?
  printf 'supervise: pass %d end rc=%d %s\n' "$n" "$rc" "$(date +%H:%M:%S)"
  if [ -e .factory/STOP ]; then
    break
  fi
  sleep 60
done
printf 'supervise: exit (STOP or restart budget spent)\n'
