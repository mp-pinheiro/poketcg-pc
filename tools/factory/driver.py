#!/usr/bin/env python3
"""Wave runner: fan packets across lanes, repair-loop against the oracle.

``run_wave(packet_ids, translate_fn, lanes_count, max_rounds)`` is the seam:
``translate_fn(prompt_text) -> reply_text`` is injected by the caller (the
orchestrator session wires it to its ``completion(...)``; any API client fits).
The driver owns everything else: lane refresh, surgery, verification, state,
metrics.  Crash-safe: every transition is on disk; ``reset-stale`` returns
in-flight packets to ``pending``.
"""

from __future__ import annotations

import argparse
import json
import queue as queue_mod
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    METRICS, block_routine, estimate_tokens, list_packets, load_packet,
    record_metric, set_state,
)
import lanes  # noqa: E402
import prompt as prompt_mod  # noqa: E402
import surgery  # noqa: E402
import verify as verify_mod  # noqa: E402

IN_FLIGHT = ("translated", "verifying", "repair")


def _process(packet_id: str, lane_index: int, translate_fn, max_rounds: int,
             model: str) -> dict:
    packet = load_packet(packet_id)
    started = time.time()
    prompt_tokens = 0
    reply_tokens = 0
    feedback: str | None = None
    format_retry_used = False
    rounds = 0
    final = "escalated"
    reason: str | None = None

    lane = lanes.ensure(lane_index)
    while True:
        text = prompt_mod.render(packet, feedback)
        prompt_tokens += estimate_tokens(text)
        reply = translate_fn(text)
        reply_tokens += estimate_tokens(reply)
        set_state(packet, "translated")
        try:
            translation = prompt_mod.parse(reply, packet)
        except prompt_mod.FormatError as exc:
            if not format_retry_used:
                format_retry_used = True
                feedback = f"format: {exc}"
                continue
            final, reason = "rejected-format", str(exc)
            break
        try:
            changed = surgery.apply(lane, packet, translation)
        except surgery.SurgeryError as exc:
            final, reason = "escalated", f"surgery: {exc}"
            break
        cases_changed = any(p.name.endswith(".py") for p in changed) or rounds == 0
        set_state(packet, "verifying")
        result = verify_mod.verify_packet(packet, lane, cases_changed)
        if result["status"] == "green":
            verify_mod.collect_bundle(packet, lane)
            final, reason = "green", None
            break
        if result["status"] == "timeout":
            spinner = result.get("routine") or packet["routines"][0]["name"]
            block_routine(spinner, "oracle timeout: callee never returns",
                          "port the blocking callee (see verdict)")
            final, reason = "parked", f"timeout: {spinner}"
            break
        rounds += 1
        if rounds >= max_rounds:
            final, reason = "escalated", f"{result['status']} after {max_rounds} rounds"
            break
        feedback = f"{result['status']}:\n{result['detail']}"
        set_state(packet, "repair", feedback[:400])

    set_state(packet, final, reason)
    metric = {
        "id": packet_id, "verdict": final, "reason": reason, "rounds": rounds,
        "wall_s": round(time.time() - started, 1),
        "prompt_tokens": prompt_tokens, "reply_tokens": reply_tokens,
        "routines": len(packet["routines"]), "model": model,
    }
    record_metric(metric)
    return metric


def run_wave(packet_ids: list[str], translate_fn, lanes_count: int = 8,
             max_rounds: int = 4, model: str = "unknown") -> list[dict]:
    lane_pool: queue_mod.Queue[int] = queue_mod.Queue()
    for index in range(lanes_count):
        lane_pool.put(index)

    def worker(packet_id: str) -> dict:
        lane_index = lane_pool.get()
        try:
            return _process(packet_id, lane_index, translate_fn, max_rounds, model)
        except Exception:
            packet = load_packet(packet_id)
            set_state(packet, "escalated", f"driver crash: {traceback.format_exc(limit=3)}")
            metric = {"id": packet_id, "verdict": "escalated", "reason": "driver crash",
                      "rounds": 0, "wall_s": 0, "prompt_tokens": 0, "reply_tokens": 0,
                      "routines": len(packet.get("routines", [])), "model": model}
            record_metric(metric)
            return metric
        finally:
            lane_pool.put(lane_index)

    with ThreadPoolExecutor(max_workers=lanes_count) as pool:
        results = list(pool.map(worker, packet_ids))
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("reset-stale")
    sub.add_parser("metrics")
    args = parser.parse_args()
    if args.command == "status":
        counts: dict[str, int] = {}
        for packet in list_packets():
            counts[packet["state"]] = counts.get(packet["state"], 0) + 1
        for state, count in sorted(counts.items()):
            print(f"{state:16} {count}")
    elif args.command == "reset-stale":
        for packet in list_packets(IN_FLIGHT):
            set_state(packet, "pending", "reset-stale")
            print(f"reset {packet['id']}")
    elif args.command == "metrics":
        if not METRICS.exists():
            print("no metrics yet")
            return 0
        rows = [json.loads(line) for line in METRICS.read_text().splitlines()]
        greens = [r for r in rows if r["verdict"] == "green"]
        total_routines = sum(r["routines"] for r in rows) or 1
        print(f"packets={len(rows)} green={len(greens)} "
              f"escalated={sum(1 for r in rows if r['verdict'] == 'escalated')} "
              f"parked={sum(1 for r in rows if r['verdict'] == 'parked')} "
              f"rejected={sum(1 for r in rows if r['verdict'] == 'rejected-format')}")
        if rows:
            tokens = sum(r["prompt_tokens"] + r["reply_tokens"] for r in rows)
            wall = sum(r["wall_s"] for r in rows)
            rounds = [r["rounds"] for r in greens]
            print(f"tokens/routine (est.): {tokens // total_routines}")
            print(f"wall/packet avg: {wall / len(rows):.0f}s")
            if rounds:
                print(f"repair rounds on greens: avg {sum(rounds) / len(rounds):.2f} "
                      f"max {max(rounds)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
