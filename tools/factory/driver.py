#!/usr/bin/env python3
"""Wave runner: fan packets across lanes, repair-loop against the oracle.

``run_wave(packet_ids, translate_fn, lanes_count, max_rounds)`` is the seam:
``translate_fn(prompt_text) -> reply_text`` is injected by the caller (the
orchestrator session wires it to its ``completion(...)``; any API client
fits).  ``translate_fn`` runs ONLY on the calling thread — harness completion
bridges are not thread-safe — while surgery+verification run on a worker
pool.  A packet pins its lane until it reaches a terminal state, because
targeted repair rounds rely on the lane keeping the already-verified
routines' files.  Crash-safe: every transition is on disk; ``reset-stale``
returns in-flight packets to ``pending``.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    METRICS, block_routine, estimate_tokens, list_packets, load_packet,
    record_metric, save_packet, set_state,
)
import lanes  # noqa: E402
import prompt as prompt_mod  # noqa: E402
import surgery  # noqa: E402
import verify as verify_mod  # noqa: E402

IN_FLIGHT = ("translated", "verifying", "repair")


class _Run:
    def __init__(self, packet_id: str):
        self.packet = load_packet(packet_id)
        self.id = packet_id
        self.lane_index: int | None = None
        self.lane = None
        self.rounds = 0
        self.format_retry_used = False
        self.feedback: str | None = None
        self.targets: list[str] | None = None
        self.last_failing: list[str] | None = None
        self.prompt_tokens = 0
        self.reply_tokens = 0
        self.started = time.time()
        self.final: str | None = None
        self.reason: str | None = None

    def metric(self, model: str) -> dict:
        return {
            "id": self.id, "verdict": self.final, "reason": self.reason,
            "rounds": self.rounds, "wall_s": round(time.time() - self.started, 1),
            "prompt_tokens": self.prompt_tokens, "reply_tokens": self.reply_tokens,
            "routines": len(self.packet["routines"]), "model": model,
        }



def _apply_and_verify(run: _Run, translation: dict) -> dict:
    """Worker-thread step: surgery + verification inside the pinned lane."""
    try:
        changed = surgery.apply(run.lane, run.packet, translation)
    except surgery.SurgeryError as exc:
        return {"status": "surgery", "detail": str(exc)}
    cases_changed = any(str(p).endswith(".py") for p in changed) or run.rounds == 0
    set_state(run.packet, "verifying")
    return verify_mod.verify_packet(run.packet, run.lane, cases_changed)


def _salvage(run: _Run, failing: list[str] | None) -> bool:
    """Land the routines that pass; spill the failures into a new packet.

    A packet is a file group, and its routines are independent. Discarding
    six verified routines because two failed is pure waste, so at escalation
    the failing fragments are cut out of the lane, the reduced packet is
    re-verified, and the failures spill into ``<id>-rest`` for a later wave
    or the escalation lane.
    """
    names = [r["name"] for r in run.packet["routines"]]
    if not failing:
        return False
    failing = [fn for fn in failing if fn in names]
    keep = [fn for fn in names if fn not in failing]
    if not failing or not keep:
        return False
    try:
        surgery.remove(run.lane, run.packet, failing)
    except Exception:
        return False
    reduced = dict(run.packet)
    reduced["routines"] = [r for r in run.packet["routines"] if r["name"] in keep]
    result = verify_mod.verify_packet(reduced, run.lane, True)
    if result["status"] != "green":
        return False
    spill = dict(run.packet)
    spill["id"] = f"{run.packet['id']}-rest"
    spill["routines"] = [r for r in run.packet["routines"] if r["name"] in failing]
    spill["state"] = "pending"
    spill["rounds"] = 0
    spill["reason"] = f"spilled from {run.packet['id']} after {run.rounds} rounds"
    save_packet(spill)
    run.packet["routines"] = reduced["routines"]
    save_packet(run.packet)
    verify_mod.collect_bundle(run.packet, run.lane)
    run.final = "green"
    run.reason = f"partial: {len(keep)}/{len(names)} landed, {len(failing)} spilled"
    return True


def _decide(run: _Run, result: dict, max_rounds: int) -> bool:
    """Main-thread step. True = schedule another round."""
    if result["status"] == "green":
        verify_mod.collect_bundle(run.packet, run.lane)
        run.final, run.reason = "green", None
        return False
    if result["status"] == "timeout":
        spinner = result.get("routine") or run.packet["routines"][0]["name"]
        block_routine(spinner, "oracle timeout: callee never returns",
                      "port the blocking callee (see verdict)")
        run.final, run.reason = "parked", f"timeout: {spinner}"
        return False
    run.rounds += 1
    failing_now = result.get("failing") or (
        [result["routine"]] if result.get("routine") else None)
    if failing_now and run.last_failing == failing_now:
        if _salvage(run, failing_now):
            return False
    run.last_failing = failing_now
    if run.rounds >= max_rounds:
        if not _salvage(run, failing_now):
            run.final = "escalated"
            run.reason = f"{result['status']} after {max_rounds} rounds"
        return False
    run.targets = failing_now if failing_now else None
    run.feedback = f"{result['status']}:\n{result['detail']}"
    set_state(run.packet, "repair", run.feedback[:400])
    return True


def _render(run: _Run) -> str:
    text = prompt_mod.render(run.packet, run.feedback, run.targets)
    run.prompt_tokens += estimate_tokens(text)
    return text


def _accept(run: _Run, reply: str) -> dict | None:
    run.reply_tokens += estimate_tokens(reply)
    set_state(run.packet, "translated")
    try:
        return prompt_mod.parse(reply, run.packet, run.targets)
    except prompt_mod.FormatError as exc:
        if not run.format_retry_used:
            run.format_retry_used = True
            run.feedback = f"format: {exc}"
            return {}  # {} = retranslate this round
        run.final, run.reason = "rejected-format", str(exc)
        return None


def run_wave(packet_ids: list[str], translate_many, lanes_count: int = 10,
             max_rounds: int = 4, model: str = "unknown") -> dict:
    """Round-synchronous wave -> ``{"results": [...], "deferred": [ids]}``.

    ``translate_many(prompts: list[str]) -> list[str]`` translates a whole
    round at once so the caller can fan out concurrently (harness
    ``parallel(...)``); serial mapping still works but is the slow path.
    Packets are processed in chunks of ``lanes_count`` so each active packet
    keeps a pinned lane for its repair rounds.

    Deferred packets are returned, never dropped: a second packet of the same
    basename can only run once the first has LANDED, because the lane it
    needs is an rsync of a tip containing the first packet's routines. The
    caller must integrate, then call again with the returned ids.
    """
    scheduled, deferred, seen = [], [], set()
    for pid in packet_ids:
        basename = load_packet(pid)["basename"]
        (deferred if basename in seen else scheduled).append(pid)
        seen.add(basename)
    for pid in deferred:
        packet = load_packet(pid)
        set_state(packet, "pending", "deferred: same basename, needs a landed tip")
    if deferred:
        print(f"deferred until integrated (same basename): {deferred}")
    packet_ids = scheduled
    results: list[dict] = []

    def finalize(run: _Run) -> None:
        set_state(run.packet, run.final, run.reason)
        metric = run.metric(model)
        record_metric(metric)
        results.append(metric)

    for start in range(0, len(packet_ids), lanes_count):
        chunk = packet_ids[start:start + lanes_count]
        active = []
        for index, pid in enumerate(chunk):
            run = _Run(pid)
            run.lane_index = index
            run.lane = lanes.ensure(index)
            active.append(run)

        with ThreadPoolExecutor(max_workers=max(1, len(active))) as pool:
            while active:
                translations: dict[str, dict] = {}
                pending = list(active)
                for _attempt in (0, 1):  # second pass covers format retries
                    if not pending:
                        break
                    prompts = [_render(run) for run in pending]
                    try:
                        replies = translate_many(prompts)
                    except Exception:
                        for run in pending:
                            run.final = "escalated"
                            run.reason = f"translate: {traceback.format_exc(limit=2)}"
                        pending = []
                        break
                    retry = []
                    for run, reply in zip(pending, replies):
                        parsed = _accept(run, reply)
                        if parsed is None:
                            continue          # terminal (rejected-format)
                        if parsed == {}:
                            retry.append(run)  # one free reformat
                            continue
                        translations[run.id] = parsed
                    pending = retry

                futures = {pool.submit(_apply_and_verify, run, translations[run.id]): run
                           for run in active if run.id in translations}
                verdicts: dict[str, dict] = {}
                for future in futures:
                    run = futures[future]
                    try:
                        verdicts[run.id] = future.result()
                    except Exception:
                        verdicts[run.id] = {
                            "status": "surgery",
                            "detail": f"verify crash: {traceback.format_exc(limit=2)}"}

                still: list[_Run] = []
                for run in active:
                    if run.final:                      # terminal in translate
                        finalize(run)
                        continue
                    result = verdicts.get(run.id)
                    if result is None:                 # never translated
                        run.final = run.final or "escalated"
                        run.reason = run.reason or "no translation produced"
                        finalize(run)
                        continue
                    if _decide(run, result, max_rounds):
                        still.append(run)
                    else:
                        finalize(run)
                active = still
    return {"results": results, "deferred": deferred}


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
