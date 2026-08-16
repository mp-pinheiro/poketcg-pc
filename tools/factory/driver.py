#!/usr/bin/env python3
"""Wave runner: fan packets across lanes, repair-loop against the oracle.

``run_wave(packet_ids, translate_many, lanes_count, verify_width, max_rounds)``
is the seam: ``translate_many(prompts) -> replies`` is injected by the caller
(the orchestrator session wires it to its ``completion(...)``; any API client
fits). ``translate_many`` runs ONLY on the scheduler thread — a worker-thread
probe (2026-08-15) confirmed the harness completion bridge raises
``RuntimeError: Missing session/run/name`` outside the calling thread — while
lane provisioning, surgery+verification, and salvage run on a worker pool.
Translation and verification are not phase-barriered: a packet whose
translation parsed is submitted for verification as soon as a lane and a
verify slot are free, while the next translate batch keeps forming from
whichever other packets are ready. Only the scheduler thread (inside
``run_wave``) reads or mutates ``_Run``/packet state; pool jobs are pure
functions of their arguments and return values only. A packet pins its lane
until it reaches a terminal state, because targeted repair rounds rely on the
lane keeping the already-verified routines' files. A wave's packet cohort may
exceed ``lanes_count``: extra packets stay queued and are admitted into a lane
on disk; recovery is owned by ``migrate-recovery-state``.
"""

import argparse
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import time
import traceback
import uuid
from collections import deque
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lanes  # noqa: E402
import prompt as prompt_mod  # noqa: E402
import surgery  # noqa: E402
import verify as verify_mod  # noqa: E402
from common import (  # noqa: E402
    ACTIVE_CLAIM_STATES,
    EVENTS,
    FACTORY,
    HISTORICAL_STATES,
    METRICS,
    ROOT,
    SCHEMA,
    WAVE_LOCK,
    WaveDeadlineExpired,
    block_routine,
    claim_index,
    cohort_id,
    estimate_tokens,
    legacy_attempt_id,
    list_packets,
    load_packet,
    new_attempt_id,
    packet_path,
    record_event,
    record_metric,
    run_bounded,
    save_packet,
    set_state,
    wave_lock,
    write_json,
)

IN_FLIGHT = ("translating", "translated", "verifying", "repair")
ACTIVE_CLAIM_STATES = ("pending", *IN_FLIGHT, "green")

# Seconds to keep a ready translate batch waiting while verify/salvage jobs are
# still outstanding. Measured on wave a4745708 (14 packets): translation was 60%
# of packet-time and verification 2%, so a batch issued the instant one packet
# is ready fragments into width-1 calls that still cost 24-48s each. Waiting for
# the cheap verdicts re-widens the batch, and width 10 measured 107-123s against
# ~170s as two batches of five. The cap bounds the wait when one verify is slow.
TRANSLATE_COALESCE_S = 45.0


def _foreign_claims(packet: dict) -> set[str]:
    """Work IDs this packet shares with another non-terminal packet.

    An escalated packet releases its claims, so build() may have re-offered its
    routines into a fresh packet. Resetting it back to pending would then break
    the one-claim invariant; the caller must skip and leave it escalated.
    """
    mine = {r["work_id"] for r in packet.get("routines", []) if r.get("work_id")}
    held: set[str] = set()
    for other in list_packets(ACTIVE_CLAIM_STATES):
        if other["id"] == packet["id"]:
            continue
        for routine in other.get("routines", []):
            if routine.get("work_id") in mine:
                held.add(routine["work_id"])
    return held


def _progress_report() -> dict:
    """Return the live authoritative progress report."""
    spec = importlib.util.spec_from_file_location(
        "port_progress_report", ROOT / "tools" / "progress" / "report.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load progress report")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compute(
        module.load_inventory(), module.load_routines()[0], module.load_gate())


def _todo_status() -> dict[tuple[str, str], bool]:
    """(source, name) -> still todo, from the live progress report.

    An escalated packet can outlive its work: while it sat escalated its
    routines may have landed on main. Resetting it to pending would re-port
    committed code, so callers drop routines the report no longer marks todo.
    """
    return {
        (f["file"], f["name"]): f["status"] == "todo"
        for f in _progress_report()["functions"]
    }


def _work_key(work_id: str) -> tuple[str, str]:
    _scheme, _version, source, name = work_id.split(":")
    return source, name



def detail_digest(result: dict) -> str:
    """Identify a repeated failure across rounds: same status, same output."""
    payload = f"{result.get('status')}\n{result.get('detail') or ''}"
    return hashlib.sha1(payload.encode(), usedforsecurity=False).hexdigest()[:10]


class _Run:
    def __init__(self, packet_id: str, wave_id: str, started: float):
        self.packet = load_packet(packet_id)
        self.id = packet_id
        self.wave_id = wave_id
        self.lane_index: int | None = None
        self.lane = None
        self.deadline: float = 0.0
        self.rounds = int(self.packet.get("rounds", 0))
        self.format_retry_used = bool(self.packet.get("format_retry_used", False))
        self.feedback: str | None = None
        self.targets: list[str] | None = None
        self.last_failing: list[str] | None = None
        self.statics_baseline: list[str] | None = None
        self.prompt_tokens = 0
        self.last_digest: str | None = None
        self.reply_tokens = 0
        self.started = started
        self.final: str | None = None
        self.reason: str | None = None
        self.pending_reason: str | None = None
        self.job: str | None = None
        self.needs_translate = False
        self.translation: dict | None = None
        self.lane_s = 0.0
        self.translate_s = 0.0
        self.verify_s = 0.0
        self.salvage_s = 0.0
        self.busy: list[tuple[float, float]] = []

    def busy_s(self) -> float:
        """Wall time this packet had *some* work in flight.

        Phases overlap by design — a lane rsync runs while the scheduler is
        blocked in translate_many — so summing the per-phase totals
        double-counts and can exceed the packet's own wall time. Idle time has
        to come from the union of the busy intervals instead.
        """
        merged_end = 0.0
        total = 0.0
        for start, end in sorted(self.busy):
            if end <= merged_end:
                continue
            total += end - max(start, merged_end)
            merged_end = end
        return total

    def metric(self, model: str) -> dict:
        work_ids = sorted(r["work_id"] for r in self.packet["routines"])
        wall_s = round(time.monotonic() - self.started, 1)
        idle_s = round(max(0.0, (time.monotonic() - self.started) - self.busy_s()), 1)
        return {
            "id": self.id, "verdict": self.final, "reason": self.reason,
            "rounds": self.rounds, "wall_s": wall_s,
            "translate_s": round(self.translate_s, 1),
            "verify_s": round(self.verify_s, 1),
            "salvage_s": round(self.salvage_s, 1),
            "lane_s": round(self.lane_s, 1),
            "idle_s": idle_s,
            "prompt_tokens": self.prompt_tokens, "reply_tokens": self.reply_tokens,
            "routines": len(self.packet["routines"]), "wave_id": self.wave_id,
            "work_ids": work_ids,
            "issue_numbers": sorted(r["issue_number"] for r in self.packet["routines"]),
            "model": model,
        }


def _attempt(run: _Run, phase: str, deadline: float, round_number: int) -> None:
    run.packet["attempt"] = {
        "wave_id": run.wave_id, "phase": phase, "round": round_number,
        "started_at": int(time.time()), "deadline_at": int(time.time() + max(0, deadline - time.monotonic())),
    }
    set_state(run.packet, phase)
    save_packet(run.packet)


def _clear_attempt(run: _Run) -> None:
    run.packet.pop("attempt", None)
    save_packet(run.packet)


class _Timed:
    """Wrap a pool job so it records its own start and end.

    The scheduler blocks on ``translate_many`` (the harness completion bridge
    is bound to its calling thread), so a job can finish long before its
    future is harvested. Timing at harvest would bill that waiting to the
    job's phase instead of to the packet's idle time.
    """

    __slots__ = ("fn", "args", "start", "end")

    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args
        self.start = 0.0
        self.end = 0.0

    def __call__(self):
        self.start = time.monotonic()
        try:
            return self.fn(*self.args)
        finally:
            self.end = time.monotonic()

    @property
    def wall(self) -> float:
        return max(0.0, self.end - self.start)


def _apply_and_verify(packet: dict, lane: Path, translation: dict,
                      statics_baseline: list[str] | None, rounds: int,
                      deadline: float, wave_id: str, packet_id: str) -> dict:
    """Run surgery and verification behind a killable process boundary."""
    payload = json.dumps({
        "packet": packet,
        "lane": str(lane),
        "translation": translation,
        "statics_baseline": statics_baseline,
        "rounds": rounds,
        "deadline": deadline,
        "wave_id": wave_id,
        "packet_id": packet_id,
    })
    completed = run_bounded(
        [sys.executable, str(Path(__file__).with_name("verify_worker.py"))],
        cwd=ROOT,
        cap=max(0.001, deadline - time.monotonic()),
        deadline=deadline,
        check=True,
        input_text=payload,
    )
    response = json.loads(completed.stdout)
    if not isinstance(response, dict):
        raise TypeError("verification worker returned a non-object")
    if response.get("deadline"):
        raise WaveDeadlineExpired(str(response["deadline"]))
    result = response.get("result")
    baseline = response.get("statics_baseline")
    if not isinstance(result, dict) or not isinstance(result.get("status"), str):
        raise TypeError("verification worker returned an invalid verdict")
    if not isinstance(baseline, list):
        raise TypeError("verification worker returned an invalid statics baseline")
    result["_statics_baseline"] = baseline
    return result


def _salvage_verify(lane: Path, packet: dict, failing: list[str] | None,
                    deadline: float) -> dict | None:
    """Pool job: land the routines that pass, reduced to just the survivors.

    Pure with respect to shared state: writes only inside the lane. Returns
    the reduced packet's verdict, or None when salvage is not possible
    (nothing to keep, nothing to drop, or the reduced verify itself failed to
    run). WaveDeadlineExpired propagates so the scheduler can defer.
    """
    names = [r["name"] for r in packet["routines"]]
    failing = [fn for fn in (failing or []) if fn in names]
    keep = [fn for fn in names if fn not in failing]
    if not failing or not keep:
        return None
    try:
        surgery.remove(lane, packet, failing)
    except Exception:
        return None
    reduced = dict(packet)
    reduced["routines"] = [r for r in packet["routines"] if r["name"] in keep]
    try:
        return verify_mod.verify_packet(reduced, lane, True, deadline=deadline)
    except WaveDeadlineExpired:
        raise
    except Exception:
        return None


def _salvage_finish(run: "_Run", verdict: dict | None, failing: list[str]) -> None:
    """Scheduler-thread step: write the spill packet and finalize run from a
    completed _salvage_verify result."""
    if not verdict or verdict.get("status") != "green":
        run.final = "retry-ready"
        run.reason = run.pending_reason
        return
    names = [r["name"] for r in run.packet["routines"]]
    failing = [fn for fn in failing if fn in names]
    keep = [fn for fn in names if fn not in failing]
    spill = dict(run.packet)
    spill["id"] = f"{run.packet['id']}-rest"
    spill["routines"] = [r for r in run.packet["routines"] if r["name"] in failing]
    spill["state"] = "pending"
    spill["rounds"] = 0
    spill["format_retry_used"] = False
    spill.pop("attempt", None)
    spill["updated_at"] = int(time.time())
    spill["reason"] = f"spilled from {run.packet['id']} after {run.rounds} rounds"
    save_packet(spill)
    run.packet["routines"] = [r for r in run.packet["routines"] if r["name"] in keep]
    save_packet(run.packet)
    try:
        verify_mod.collect_bundle(run.packet, run.lane)
    except Exception as exc:
        run.final = "retry-ready"
        run.reason = f"bundle failure: {str(exc)[-300:]}"
        return
    run.final = "green"
    run.reason = f"partial: {len(keep)}/{len(names)} landed, {len(failing)} spilled"


def _decide(run: "_Run", result: dict, max_rounds: int) -> str:
    """Scheduler-thread step. Returns 'repair', 'salvage', or 'final'."""
    if result["status"] == "green":
        verify_mod.collect_bundle(run.packet, run.lane)
        run.final, run.reason = "green", None
        return "final"
    if result["status"] == "timeout":
        spinner = result.get("routine") or run.packet["routines"][0]["name"]
        block_routine(spinner, "oracle timeout: callee never returns",
                      "port the blocking callee (see verdict)")
        run.final, run.reason = "blocked", f"timeout: {spinner}"
        return "final"
    if result["status"] in {"infra-timeout", "infra-error"}:
        detail = result["detail"][-400:]
        if "bundle input missing:" in detail:
            run.final = "repair"
            run.reason = f"missing bundle fixture: {detail}"
        else:
            run.final = "retry-ready"
            prefix = result["status"]
            run.reason = f"{prefix}: {detail}"
        return "final"
    run.rounds += 1
    run.packet["rounds"] = run.rounds
    save_packet(run.packet)
    failing_now = result.get("failing") or (
        [result["routine"]] if result.get("routine") else None)
    run.last_failing = failing_now
    digest = detail_digest(result)
    repeated = digest == run.last_digest
    run.last_digest = digest
    if run.rounds >= max_rounds or repeated:
        reason = (
            f"{result['status']} repeated verbatim at round {run.rounds}"
            if repeated else
            f"{result['status']} after {max_rounds} rounds"
        )
        names = [r["name"] for r in run.packet["routines"]]
        failing = [fn for fn in (failing_now or []) if fn in names]
        keep = [fn for fn in names if fn not in failing]
        if failing and keep:
            run.pending_reason = reason
            return "salvage"
        run.final = "retry-ready"
        run.reason = reason
        return "final"
    run.targets = failing_now if failing_now else None
    run.feedback = f"{result['status']}:\n{result['detail']}"
    _attempt(run, "repair", run.deadline, run.rounds)
    set_state(run.packet, "repair", run.feedback[:400])
    return "repair"


def _render(run: "_Run") -> str:
    text = prompt_mod.render(run.packet, run.feedback, run.targets)
    run.prompt_tokens += estimate_tokens(text)
    return text


def _accept(run: "_Run", reply: str) -> dict | None:
    run.reply_tokens += estimate_tokens(reply)
    set_state(run.packet, "translated")
    try:
        return prompt_mod.parse(reply, run.packet, run.targets)
    except prompt_mod.FormatError as exc:
        if not run.format_retry_used:
            run.format_retry_used = True
            run.packet["format_retry_used"] = True
            save_packet(run.packet)
            run.feedback = f"format: {exc}"
            return {}
        run.final, run.reason = "retry-ready", f"format: {exc}"
        return None


def run_wave(packet_ids: list[str], translate_many, lanes_count: int = 10,
             max_rounds: int = 4, model: str = "unknown", max_wall_s: float = 1800,
             on_event=None, verify_width: int | None = None) -> dict:
    if lanes_count <= 0 or max_rounds <= 0 or max_wall_s <= 0:
        raise ValueError("lanes_count, max_rounds, and max_wall_s must be positive")
    if verify_width is None:
        verify_width = max(2, min(lanes_count, (os.cpu_count() or 4) - 2))
    if verify_width <= 0:
        raise ValueError("verify_width must be positive")
    if any(not isinstance(pid, str) or not pid for pid in packet_ids):
        raise ValueError("wave packet IDs must be non-empty strings")
    if len(set(packet_ids)) != len(packet_ids):
        raise ValueError("wave packet IDs must be unique")
    wave_id = uuid.uuid4().hex
    started = time.monotonic()
    deadline = started + max_wall_s
    event_errors: list[str] = []
    callbacks_enabled = True

    def emit(event: str, **payload) -> None:
        nonlocal callbacks_enabled
        data = {"event": event, "wave_id": wave_id,
                "elapsed_s": round(time.monotonic() - started, 3), **payload}
        record_event(data)
        if not callbacks_enabled:
            return
        try:
            if on_event is not None:
                on_event(data)
        except Exception:
            callbacks_enabled = False
            event_errors.append(traceback.format_exc(limit=2).strip()[-4000:])

    metadata = {
        "wave_id": wave_id, "pid": os.getpid(), "started_at": int(time.time()),
        "deadline_at": int(time.time() + max_wall_s), "packet_ids": packet_ids,
    }
    with wave_lock(metadata):
        packets = [load_packet(pid) for pid in packet_ids]
        if any(packet.get("state") != "pending" for packet in packets):
            bad = [packet["id"] for packet in packets if packet.get("state") != "pending"]
            raise ValueError(f"wave packets must be pending: {', '.join(bad)}")
        emit("wave-start", packet_ids=packet_ids, max_wall_s=max_wall_s)

        results: list[dict] = []
        deferred: list[str] = []
        stop_reason: str | None = None
        active: list[_Run] = []
        waiting: "deque[str]" = deque(packet_ids[lanes_count:])
        jobs: dict = {}
        harvested: list = []
        slots_used = 0
        translate_coalesce_since: float | None = None

        def finalize(run: _Run) -> None:
            _clear_attempt(run)
            set_state(run.packet, run.final, run.reason)
            metric = run.metric(model)
            record_metric(metric)
            results.append(metric)
            emit("packet-final", packet_id=run.id,
                 verdict=run.final, reason=run.reason, rounds=run.rounds,
                 wall_s=metric["wall_s"])

        def refill() -> None:
            if stop_reason is not None or not waiting:
                return
            used = {r.lane_index for r in active}
            freed = next((i for i in range(lanes_count) if i not in used), None)
            if freed is None:
                return
            packet_id = waiting.popleft()
            emit("refill", packet_id=packet_id, lane=freed)
            admit(packet_id, freed)

        def finalize_and_refill(run: _Run) -> None:
            finalize(run)
            if run in active:
                active.remove(run)
            refill()

        def admit(packet_id: str, lane_index: int) -> None:
            run = _Run(packet_id, wave_id, time.monotonic())
            run.deadline = deadline
            run.lane_index = lane_index
            active.append(run)
            if run.rounds >= max_rounds:
                run.final = "retry-ready"
                run.reason = f"resumed at {run.rounds} rounds; max is {max_rounds}"
                finalize_and_refill(run)
                return
            run.needs_translate = True
            run.job = "lane"
            job = _Timed(lanes.ensure, run.lane_index, deadline, run.packet)
            jobs[pool.submit(job)] = ("lane", (run, job))

        with ThreadPoolExecutor(max_workers=lanes_count + verify_width + 2) as pool:
            for index, packet_id in enumerate(packet_ids[:lanes_count]):
                admit(packet_id, index)

            def submit_verifies() -> None:
                nonlocal slots_used
                for run in active:
                    if (run.job is None and run.lane is not None
                            and run.translation is not None and not run.final
                            and slots_used < verify_width):
                        run.job = "verify"
                        _attempt(run, "verifying", deadline, run.rounds)
                        job = _Timed(
                            _apply_and_verify, run.packet, run.lane, run.translation,
                            run.statics_baseline, run.rounds, deadline, wave_id, run.id,
                        )
                        jobs[pool.submit(job)] = ("verify", (run, job))
                        slots_used += 1
                        emit("verify-start", packet_id=run.id, round=run.rounds)

            def translate_inline(batch: list) -> None:
                """Blocking, on the scheduler thread: the harness completion
                bridge is bound to its calling thread. Verify and salvage jobs
                keep running in the pool for the whole call."""
                nonlocal stop_reason
                for run in batch:
                    run.needs_translate = False
                    _attempt(run, "translating", deadline, run.rounds + 1)
                prompts = [_render(run) for run in batch]
                emit("translate-start", packet_ids=[run.id for run in batch])
                started_at = time.monotonic()

                def requeue() -> None:
                    for run in batch:
                        if not run.final:
                            run.needs_translate = True

                try:
                    replies = translate_many(prompts)
                except WaveDeadlineExpired as exc:
                    stop_reason = str(exc)
                    requeue()
                    return
                except Exception as exc:
                    stop_reason = f"translate: {str(exc).strip()[-400:]}"
                    requeue()
                    return
                finished_at = time.monotonic()
                wall = round(finished_at - started_at, 2)
                for run in batch:
                    run.translate_s += wall
                    run.busy.append((started_at, finished_at))
                if not isinstance(replies, (list, tuple)) or len(replies) != len(batch):
                    stop_reason = "translate: translator returned wrong reply collection"
                    requeue()
                    return
                emit("translate-finished", count=len(batch), wall_s=wall)
                for run, reply in zip(batch, replies):
                    if not isinstance(reply, str):
                        stop_reason = "translate: translator returned a non-string reply"
                        run.needs_translate = True
                        continue
                    parsed = _accept(run, reply)
                    if parsed is None:
                        finalize_and_refill(run)
                    elif parsed == {}:
                        run.needs_translate = True
                    else:
                        run.translation = parsed

            def harvest(timeout: float) -> None:
                harvested.clear()
                if not jobs:
                    return
                done, _ = wait(list(jobs), timeout=timeout, return_when=FIRST_COMPLETED)
                harvested.extend(done)

            def outstanding_fast() -> int:
                return sum(1 for kind, _ in jobs.values()
                           if kind in ("verify", "salvage"))

            while active or jobs:
                if time.monotonic() >= deadline:
                    stop_reason = "wave deadline expired"
                    break

                harvest(0)
                if not harvested:
                    if stop_reason is None:
                        submit_verifies()
                        batch = [run for run in active
                                 if run.needs_translate and run.translation is None
                                 and not run.final]
                        if batch:
                            if outstanding_fast() == 0:
                                translate_coalesce_since = None
                                translate_inline(batch)
                                continue
                            if translate_coalesce_since is None:
                                translate_coalesce_since = time.monotonic()
                            elif (time.monotonic() - translate_coalesce_since
                                  >= TRANSLATE_COALESCE_S):
                                translate_coalesce_since = None
                                translate_inline(batch)
                                continue
                    if not jobs:
                        break
                    harvest(5)

                for future in list(harvested):
                    kind, payload_ = jobs.pop(future)

                    if kind == "lane":
                        run, job = payload_
                        run.job = None
                        run.lane_s += job.wall
                        run.busy.append((job.start, job.end))
                        try:
                            lane = future.result()
                        except Exception as exc:
                            stop_reason = f"lane: {str(exc).strip()[-400:]}"
                            continue
                        run.lane = lane
                        emit("lane-ready", packet_id=run.id, lane=run.lane_index,
                             wall_s=round(job.wall, 2))

                    elif kind == "verify":
                        run, job = payload_
                        run.job = None
                        slots_used -= 1
                        run.verify_s += job.wall
                        run.busy.append((job.start, job.end))
                        try:
                            verdict = future.result()
                        except WaveDeadlineExpired as exc:
                            stop_reason = str(exc)
                            continue
                        except Exception as exc:
                            verdict = {"status": "infra-error",
                                       "detail": "".join(traceback.format_exception(exc))}
                        else:
                            run.statics_baseline = verdict.pop("_statics_baseline")
                        emit("verify-finished", packet_id=run.id, round=run.rounds,
                             status=verdict["status"], digest=detail_digest(verdict),
                             wall_s=round(job.wall, 2))
                        action = _decide(run, verdict, max_rounds)
                        if action == "repair":
                            run.translation = None
                            run.needs_translate = True
                        elif action == "salvage":
                            run.job = "salvage"
                            salvage_job = _Timed(_salvage_verify, run.lane, run.packet,
                                                 run.last_failing, deadline)
                            jobs[pool.submit(salvage_job)] = ("salvage", (run, salvage_job))
                            slots_used += 1
                            emit("salvage-start", packet_id=run.id)
                        else:
                            finalize_and_refill(run)

                    elif kind == "salvage":
                        run, job = payload_
                        run.job = None
                        slots_used -= 1
                        run.salvage_s += job.wall
                        run.busy.append((job.start, job.end))
                        try:
                            salvage_verdict = future.result()
                        except WaveDeadlineExpired as exc:
                            stop_reason = str(exc)
                            continue
                        except Exception:
                            salvage_verdict = None
                        emit("salvage-finished", packet_id=run.id,
                             status=(salvage_verdict or {}).get("status"),
                             wall_s=round(job.wall, 2))
                        _salvage_finish(run, salvage_verdict, run.last_failing or [])
                        finalize_and_refill(run)

        if stop_reason is not None:
            for run in active:
                if not run.final and run.id not in deferred:
                    deferred.append(run.id)
                if not run.final:
                    _clear_attempt(run)
                    set_state(run.packet, "pending", stop_reason)
            for packet_id in waiting:
                if packet_id not in deferred:
                    deferred.append(packet_id)
            emit("wave-deferred", packet_ids=deferred, reason=stop_reason)
        status = "complete" if stop_reason is None else (
            "deadline" if "deadline" in stop_reason else "stopped"
        )

        emit("wave-finish", status=status,
             result_count=len(results), deferred_count=len(deferred),
             stop_reason=stop_reason, wall_s=round(time.monotonic() - started, 3))
        return {
            "status": status, "results": results, "deferred": deferred,
            "stop_reason": stop_reason,
            "wall_s": round(time.monotonic() - started, 3),
            "event_errors": event_errors,
        }
def _migration_progress() -> tuple[dict[str, bool], dict]:
    report = _progress_report()
    todo = {
        f"{row.get('file')}:{row.get('name')}": row.get("status") == "todo"
        for row in report.get("functions", [])
        if row.get("file") and row.get("name")
    }
    return todo, report


def _migration_backup(raw_packets: list[tuple[Path, bytes]]) -> Path:
    backups = FACTORY / "backups"
    backups.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
    backup = backups / f"recovery-state-{stamp}-{time.time_ns() % 1000000:06d}"
    backup.mkdir()
    manifest = []
    for path, raw in raw_packets:
        destination = backup / "queue" / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        manifest.append(str(destination.relative_to(backup)))
    write_json(backup / "manifest.json", {
        "kind": "migrate-recovery-state",
        "created_at": int(time.time()),
        "queue": manifest,
    })
    return backup


def _migration_plan() -> dict:
    """Build a deterministic schema-2 recovery migration without side effects."""
    todo, report = _migration_progress()
    entries = []
    queue = FACTORY / "queue"
    if queue.is_dir():
        for path in sorted(queue.glob("*.json")):
            raw = path.read_bytes()
            entries.append((path, raw, json.loads(raw)))

    planned = []
    legacy_count = 0
    already_schema2 = 0
    for path, raw, original in entries:
        if original.get("schema") == SCHEMA and original.get("attempt_id"):
            already_schema2 += 1
            planned.append({
                "path": path, "raw": raw, "original": original,
                "packet": copy.deepcopy(original), "legacy": False,
                "sort_key": (0, path.stat().st_mtime_ns, path.name),
            })
            continue
        legacy_count += 1
        packet_id = original.get("id") or path.stem
        if not isinstance(packet_id, str) or not packet_id:
            raise ValueError(f"legacy packet {path} has no id")
        routines = original.get("routines")
        if not isinstance(routines, list):
            raise ValueError(f"legacy packet {packet_id} has no routines")
        attempt_id = legacy_attempt_id(packet_id, raw)
        converted = copy.deepcopy(original)
        converted.update({
            "schema": SCHEMA,
            "id": attempt_id,
            "attempt_id": attempt_id,
            "kind": converted.get("kind") or "translation",
            "base_commit": converted.get("base_commit") or "unknown",
            "failure_history": list(converted.get("failure_history") or []),
            "retired_routines": list(converted.get("retired_routines") or []),
        })
        converted_routines = []
        for routine in routines:
            source = converted.get("file") or routine.get("file")
            name = routine.get("name")
            if not source or not name:
                raise ValueError(f"legacy packet {packet_id} has malformed routine")
            work_id = routine.get("work_id") or f"port:v1:{source}:{name}"
            item = copy.deepcopy(routine)
            item["work_id"] = work_id
            if todo.get(f"{source}:{name}", False):
                converted_routines.append(item)
            else:
                converted["retired_routines"].append(item)
        converted["routines"] = converted_routines
        converted["cohort_id"] = cohort_id(
            [r["work_id"] for r in converted_routines]
            or [r["work_id"] for r in routines]
        )
        state = original.get("state")
        if state in {"escalated", "rejected-format"}:
            converted["state"] = "retry-ready"
        elif state == "parked":
            converted["state"] = "blocked"
        elif state not in {
            "pending", "translating", "translated", "verifying", "repair",
            "retry-ready", "recovering", "green", "integrating", "blocked",
            "landed", "superseded",
        }:
            converted["state"] = "pending"
        planned.append({
            "path": path, "raw": raw, "original": original,
            "packet": converted, "legacy": True,
            "sort_key": (1, path.stat().st_mtime_ns, packet_id),
        })

    owners = {}
    duplicate_work = set()
    duplicate_pairs = 0
    for entry in planned:
        packet = entry["packet"]
        for routine in list(packet.get("routines", [])):
            work_id = routine["work_id"]
            previous = owners.get(work_id)
            if previous is None:
                owners[work_id] = entry
                continue
            duplicate_work.add(work_id)
            duplicate_pairs += 1
            winner = min((previous, entry), key=lambda item: item["sort_key"])
            loser = entry if winner is previous else previous
            owners[work_id] = winner
            loser["packet"].setdefault("superseded_work_ids", []).append(work_id)
            loser["packet"].setdefault("retired_routines", []).append(
                copy.deepcopy(routine)
            )
            loser["packet"]["routines"] = [
                item for item in loser["packet"].get("routines", [])
                if item.get("work_id") != work_id
            ]

    superseded = []
    for entry in planned:
        packet = entry["packet"]
        if not packet.get("routines"):
            packet["state"] = "superseded"
            superseded.append(packet["attempt_id"])
        packet["cohort_id"] = cohort_id(
            [r["work_id"] for r in packet.get("routines", [])]
            or [r["work_id"] for r in packet.get("retired_routines", [])]
            or [f"port:v1:retired:{packet['attempt_id']}"]
        )

    partition = {
        "managed_routines": len(todo),
        "todo_residual": sum(
            1 for work_id, owner in owners.items()
            if any(r.get("work_id") == work_id
                   for r in owner["packet"].get("routines", []))
        ),
        "retired_routines": sum(
            len(entry["packet"].get("retired_routines", [])) for entry in planned
        ),
        "superseded_packets": len(superseded),
    }
    counts = {
        "packets": len(planned),
        "legacy_packets": legacy_count,
        "schema2_packets": already_schema2,
        "converted_packets": legacy_count,
        "retry_ready": sum(
            entry["packet"].get("state") == "retry-ready" for entry in planned
        ),
        "blocked": sum(
            entry["packet"].get("state") == "blocked" for entry in planned
        ),
        "duplicate_work_ids": len(duplicate_work),
        "duplicate_owner_pairs": duplicate_pairs,
        "partition": partition,
    }
    return {
        "entries": planned, "counts": counts, "report": report,
        "duplicate_work_ids": sorted(duplicate_work),
    }


def migrate_recovery_state(*, apply: bool, as_json: bool) -> int:
    plan = _migration_plan()
    counts = plan["counts"]
    changed = any(
        entry["legacy"]
        or entry["path"].stem != entry["packet"].get("attempt_id")
        or entry["original"] != entry["packet"]
        for entry in plan["entries"]
    )
    backup = None
    if apply and changed:
        backup = _migration_backup(
            [(entry["path"], entry["raw"]) for entry in plan["entries"]]
        )
        queue = FACTORY / "queue"
        try:
            for entry in plan["entries"]:
                destination = queue / f"{entry['packet']['attempt_id']}.json"
                write_json(destination, entry["packet"])
            for entry in plan["entries"]:
                destination = queue / f"{entry['packet']['attempt_id']}.json"
                if entry["path"] != destination:
                    entry["path"].unlink()
            claims = claim_index()
            expected = {
                routine["work_id"]
                for entry in plan["entries"]
                if entry["packet"].get("state") not in {"landed", "superseded"}
                for routine in entry["packet"].get("routines", [])
            }
            if set(claims) != expected:
                missing = sorted(expected - set(claims))
                extra = sorted(set(claims) - expected)
                raise RuntimeError(
                    "migration claim partition mismatch: "
                    f"missing={missing[:5]} extra={extra[:5]}"
                )
        except Exception as exc:
            raise RuntimeError(f"migration failed; backup at {backup}: {exc}") from exc
    result = dict(counts)
    result["backup"] = str(backup) if backup else None
    result["dry_run"] = not apply
    result["duplicate_work_ids"] = plan["duplicate_work_ids"]
    if as_json:
        print(json.dumps(result, sort_keys=True))
    else:
        print("migrate-recovery-state " + ("applied" if apply else "dry-run"))
        for key, value in sorted(result.items()):
            print(f"{key}: {value}")
    return 0



def escalate(limit: int | None) -> int:
    terminal = list_packets(("escalated", "parked", "rejected-format"))
    if limit:
        terminal = terminal[:limit]
    out_dir = FACTORY / "escalations"
    out_dir.mkdir(parents=True, exist_ok=True)
    briefs = []
    for packet in terminal:
        lane_dir = "/tmp/poketcg-factory/lane-<n>  (any free lane; run lanes.ensure(n) first)"
        paths = "\n".join((
            f"- `src/home/{packet['basename']}.c`",
            f"- `src/home/{packet['basename']}.h`",
            f"- `src/probe/{packet['basename']}.c`",
            f"- `tests/cases/{packet['basename']}.py`",
        ))
        routines_md = "\n\n".join(
            f"### `{r['name']}` ({r['size']} bytes)\n```asm\n{r['asm']}\n```"
            for r in packet["routines"])
        brief = (
            f"# Escalation: {packet['id']}\n\n"
            f"**basename**: `{packet['basename']}`  \n"
            f"**mode**: {packet['mode']}  \n"
            f"**terminal reason**: {packet.get('reason')}\n\n"
            f"## Owned paths\n{paths}\n\n"
            f"## Routines\n\n{routines_md}\n\n"
            f"## Lane\n\nWork in {lane_dir}. Provision with "
            f"`python3 -c \"import sys; sys.path.insert(0,'tools/factory'); "
            f"import lanes; print(lanes.ensure(<n>))\"`.\n\n"
            f"## Acceptance\n\nWrite the four files' fragments with the same "
            f"marker convention as `tools/factory/surgery.py` "
            f"(`/* >>> factory <Fn> */`...`/* <<< factory <Fn> */` for C/H/PROBE, "
            f"`# >>> factory <Fn>`...`# <<< factory <Fn>` for CASES, "
            f"`# >>> factory-mutation <Fn>`...`# <<< factory-mutation <Fn>` for "
            f"MUTATION), or call `surgery.apply(lane, packet, translation)` "
            f"directly. Then run exactly:\n\n"
            f"```sh\n"
            f"python3 tools/factory/verify.py {packet['id']} --lane <lane-dir>\n"
            f"```\n"
        )
        path = out_dir / f"{packet['id']}.md"
        path.write_text(brief)
        briefs.append(str(path))
    for path in briefs:
        print(path)
    return 0


def _live_wave() -> dict | None:
    """The wave's metadata if a wave holds the lock, else None.

    Liveness comes from the flock, never from the file's contents: the lock
    file keeps the last wave's metadata after release, and its pid is usually
    a still-live orchestrator kernel, so trusting either would report a
    finished wave as running.
    """
    if not WAVE_LOCK.exists():
        return None
    try:
        descriptor = WAVE_LOCK.open("a+")
    except OSError:
        return None
    try:
        try:
            fcntl.flock(descriptor.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            descriptor.seek(0)
            try:
                metadata = json.loads(descriptor.read() or "{}")
            except json.JSONDecodeError:
                return None
            return metadata if isinstance(metadata, dict) and metadata else None
        fcntl.flock(descriptor.fileno(), fcntl.LOCK_UN)
        return None
    finally:
        descriptor.close()


def _progress_command() -> None:
    meta = _live_wave()
    if meta is None:
        print("no live wave")
        stale = sorted(p["id"] for p in list_packets(IN_FLIGHT))
        if stale:
            print(f"stale in-flight: {stale}  (run migrate-recovery-state)")
    else:
        now = int(time.time())
        elapsed = now - int(meta.get("started_at", now))
        remaining = int(meta.get("deadline_at", now)) - now
        print(f"wave {str(meta.get('wave_id', '?'))[:8]} pid {meta.get('pid')} "
              f"elapsed {elapsed}s deadline in {remaining}s")
        verify_phases: dict[str, str] = {}
        if EVENTS.exists():
            for line in EVENTS.read_text().splitlines()[-2000:]:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("event") == "verify-phase" and event.get("packet_id"):
                    verify_phases[event["packet_id"]] = event.get("phase", "?")
        for packet in sorted(list_packets(IN_FLIGHT), key=lambda p: p["id"]):
            attempt = packet.get("attempt") or {}
            secs = now - int(attempt.get("started_at", now))
            phase = attempt.get("phase", packet["state"])
            inner = verify_phases.get(packet["id"], "")
            suffix = f" [{inner}]" if packet["state"] == "verifying" and inner else ""
            print(f"  {packet['id']:32} {packet['state']:12} "
                  f"round {attempt.get('round', '?')} {phase}{suffix} {secs}s")
    histogram: dict[str, int] = {}
    for packet in list_packets():
        histogram[packet["state"]] = histogram.get(packet["state"], 0) + 1
    print(" ".join(f"{state}={count}" for state, count in sorted(histogram.items())))


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    migration_parser = sub.add_parser(
        "migrate-recovery-state",
        help="migrate legacy recovery packets into schema-2 state",
    )
    migration_parser.add_argument("--dry-run", action="store_true")
    migration_parser.add_argument("--json", action="store_true")
    sub.add_parser("reset-stale", help="disabled; use migrate-recovery-state")
    infra_parser = sub.add_parser(
        "reset-infra", help="disabled; use migrate-recovery-state")
    infra_parser.add_argument("--reason-prefix", action="append", default=None)
    sub.add_parser("metrics")
    sub.add_parser("progress", help="inspect a live wave without taking its lock")
    escalate_parser = sub.add_parser(
        "escalate", help="write agentic-task briefs for escalated packets")
    escalate_parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.command == "migrate-recovery-state":
        return migrate_recovery_state(
            apply=not args.dry_run, as_json=args.json)
    if args.command == "status":
        from supervisor import snapshot
        snap = snapshot()
        for category, count in snap["categories"].items():
            print(f"{category:20} {count}")
        measures = snap["completion"]["measures"]
        verified_code = measures["verified_code"]
        total_code = measures["verified_code/total"]
        verified_functions = measures["verified_functions"]
        total_functions = measures["verified_functions/total"]
        code_pct = verified_code * 100 / total_code if total_code else 100.0
        function_pct = (
            verified_functions * 100 / total_functions
            if total_functions else 100.0
        )
        print(f"verified code bytes: {verified_code}/{total_code} ({code_pct:.1f}%)")
        print(
            f"verified routines: {verified_functions}/{total_functions} "
            f"({function_pct:.1f}%)"
        )
        if snap["completion"]["complete"]:
            print("PORT COMPLETE")
        elif not any(snap["categories"].values()):
            print("STOP-THE-LINE invariant:no-frontier")
        else:
            print("PORT INCOMPLETE")
    elif args.command in {"reset-stale", "reset-infra"}:
        print(
            f"{args.command} is disabled; run migrate-recovery-state "
            "to perform deterministic recovery migration",
            file=sys.stderr,
        )
        return 2
    elif args.command == "escalate":
        return escalate(args.limit)
    elif args.command == "progress":
        _progress_command()
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
        phased = [r for r in rows if "translate_s" in r]
        if phased:
            total_wall = sum(r["wall_s"] for r in phased) or 1
            parts = {
                "translate": sum(r.get("translate_s", 0) for r in phased),
                "verify": sum(r.get("verify_s", 0) for r in phased),
                "salvage": sum(r.get("salvage_s", 0) for r in phased),
                "lane": sum(r.get("lane_s", 0) for r in phased),
                "idle": sum(r.get("idle_s", 0) for r in phased),
            }
            split = " ".join(
                f"{name} {value / total_wall * 100:.0f}%" for name, value in parts.items())
            print(f"phase split over {len(phased)} packets: {split}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
