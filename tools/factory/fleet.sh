#!/usr/bin/env bash
# Fleet controller for supervised port-factory sessions. `start` builds a
# dedicated detached tmux session; `stop` is STOP-file based so every loop
# session (managed or hand-launched) finishes its current pass and exits;
# `halt` additionally terminates in-flight sessions, which is safe because all
# factory state is flock + append-only ledgers. Never creates or kills
# anything in other tmux sessions; the fleet session closes itself when its
# panes exit.
set -u
cd "$(dirname "$0")/../.." || exit 1
root=$(pwd)
session="${POKETCG_FLEET_SESSION:-poketcg-fleet}"

loop_children() {
  for pid in $(pgrep -f "omp --print --model" 2>/dev/null); do
    if [ "$(readlink "/proc/$pid/cwd" 2>/dev/null)" = "$root" ]; then
      echo "$pid"
    fi
  done
}

case "${1:-}" in
  start)
    panes="${2:-${POKETCG_FLEET_PANES:-4}}"
    rm -f .factory/STOP
    if tmux has-session -t "$session" 2>/dev/null; then
      echo "fleet: session '$session' already up; attach: tmux attach -t $session"
      exit 3
    fi
    tmux new-session -d -s "$session" -c "$root" "just launch-port-supervised"
    i=1
    while [ "$i" -lt "$panes" ]; do
      tmux split-window -t "$session" -c "$root" "just launch-port-supervised"
      tmux select-layout -t "$session" tiled
      i=$((i + 1))
    done
    echo "fleet: $panes supervised panes up; attach: tmux attach -t $session"
    ;;
  stop)
    touch .factory/STOP
    echo "fleet: STOP dropped; every loop session exits after its current pass"
    echo "fleet: immediate: just fleet-halt; restart: just fleet-start"
    ;;
  halt)
    touch .factory/STOP
    pids=$(loop_children)
    if [ -n "$pids" ]; then
      echo "$pids" | xargs -r kill -TERM
      echo "fleet: STOP dropped; terminated in-flight sessions: $(echo "$pids" | tr '\n' ' ')"
    else
      echo "fleet: STOP dropped; no in-flight loop sessions"
    fi
    ;;
  status)
    count=$(loop_children | wc -l)
    stop="absent"
    [ -e .factory/STOP ] && stop="present"
    up="down"
    tmux has-session -t "$session" 2>/dev/null && up="up"
    echo "fleet: loop_sessions=$count stop_file=$stop tmux_session=$up"
    ;;
  *)
    echo "usage: fleet.sh start [panes] | stop | halt | status" >&2
    exit 2
    ;;
esac
