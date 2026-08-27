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
while :; do
  sleep "${POKETCG_FEED_INTERVAL:-300}"
  pct=$(jq -r '.measures.code * 10000 / .measures["code/total"] | floor / 100' site/data/progress.json 2>/dev/null)
  stats=$(python3 tools/factory/measure.py 2>/dev/null \
    | grep -E "^(landings_per_hour_6h|bytes_per_hour_6h|ready_count|pool_issued|pool_green|pool_red)=" \
    | tr '\n' ' ')
  # A pass can run for many minutes, and compute detached from a dead driver
  # burns a core for all of it. The sweep is one /proc scan and kills only
  # sessions whose driver is gone, so it is safe to run beside live lanes.
  swept=$(python3 tools/factory/heal.py --sweep-only 2>/dev/null \
    | grep -c '^HEAL kill ') || true
  [ "${swept:-0}" -gt 0 ] && printf 'sweep      %s orphaned process(es) killed\n' "$swept"
  printf 'heartbeat  %s%%  %s%s\n' "${pct:-?}" "$stats" "$(date +%H:%M:%S)"
done &
beat=$!
trap 'kill "$feed" "$beat" 2>/dev/null' EXIT
# The orchestrator drives deterministic tooling; translation quality lives in
# the repo-pinned candidate agents, so the session model stays on the
# sustainable tier and opus is reserved for capability work and the gen-12+
# retry ladder.
model="${POKETCG_LOOP_MODEL:-openai-codex/gpt-5.6-luna:medium}"
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
if [ -e .factory/STOP ]; then
  printf 'supervise: exit: .factory/STOP present (fleet-stop/halt); resume: just fleet-start\n'
else
  printf 'supervise: exit: restart budget spent (%d passes)\n' "$n"
fi
