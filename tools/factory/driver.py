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
as soon as one frees up. Crash-safe: every transition is on disk;
``reset-stale`` returns in-flight packets to ``pending``.
"""

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import sys
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
    EVENTS,
    FACTORY,
    METRICS,
    ROOT,
    WAVE_LOCK,
    WaveDeadlineExpired,
    block_routine,
    estimate_tokens,
    list_packets,
    load_packet,
    packet_path,
    record_event,
    record_metric,
    run_bounded,
    save_packet,
    set_state,
    wave_lock,
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


def _todo_status() -> dict[tuple[str, str], bool]:
    """(source, name) -> still todo, from the live progress report.

    An escalated packet can outlive its work: while it sat escalated its
    routines may have landed on main. Resetting it to pending would re-port
    committed code, so callers drop routines the report no longer marks todo.
    """
    spec = importlib.util.spec_from_file_location(
        "port_progress_report", ROOT / "tools" / "progress" / "report.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load progress report")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.compute(
        module.load_inventory(), module.load_routines()[0], module.load_gate())
    return {
        (f["file"], f["name"]): f["status"] == "todo"
        for f in report["functions"]
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
        run.final = "escalated"
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
        run.final = "escalated"
        run.reason = f"infra-error: bundle collection failed: {str(exc)[-300:]}"
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
        run.final, run.reason = "parked", f"timeout: {spinner}"
        return "final"
    if result["status"] in {"infra-timeout", "infra-error"}:
        run.final = "escalated"
        prefix = result["status"]
        run.reason = f"{prefix}: {result['detail'][-400:]}"
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
        run.final = "escalated"
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
        run.final, run.reason = "rejected-format", str(exc)
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
                run.final = "escalated"
                run.reason = f"resumed at {run.rounds} rounds; max is {max_rounds}"
                finalize_and_refill(run)
                return
            run.needs_translate = True
            run.job = "lane"
            job = _Timed(lanes.ensure, run.lane_index, deadline)
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


def escalate(limit: int | None) -> int:
    escalated = list_packets(("escalated",))
    if limit:
        escalated = escalated[:limit]
    out_dir = FACTORY / "escalations"
    out_dir.mkdir(parents=True, exist_ok=True)
    briefs = []
    for packet in escalated:
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
            f"python3 tools/factory/verify.py {packet['id']} --lane <lane-dir> "
            f"normally.\n"
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
            print(f"stale in-flight: {stale}  (run reset-stale)")
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
    sub.add_parser("reset-stale")
    infra_parser = sub.add_parser(
        "reset-infra", help="return harness-failed escalations to pending")
    infra_parser.add_argument(
        "--reason-prefix", action="append", default=None,
        help="escalation reason prefix to requeue; repeatable")
    sub.add_parser("metrics")
    sub.add_parser("progress", help="inspect a live wave without taking its lock")
    escalate_parser = sub.add_parser(
        "escalate", help="write agentic-task briefs for escalated packets")
    escalate_parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.command == "status":
        counts: dict[str, int] = {}
        for packet in list_packets():
            counts[packet["state"]] = counts.get(packet["state"], 0) + 1
        for state, count in sorted(counts.items()):
            print(f"{state:16} {count}")
    elif args.command == "reset-stale":
        metadata = {
            "wave_id": f"reset-stale-{os.getpid()}",
            "pid": os.getpid(),
            "started_at": int(time.time()),
            "deadline_at": None,
            "packet_ids": [],
        }
        with wave_lock(metadata):
            for packet in list_packets(IN_FLIGHT):
                held = _foreign_claims(packet)
                if held:
                    print(f"skip {packet['id']}: held elsewhere {sorted(held)}")
                    continue
                packet.pop("attempt", None)
                set_state(packet, "pending", "reset-stale")
                print(f"reset {packet['id']}")
    elif args.command == "reset-infra":
        metadata = {
            "wave_id": f"reset-infra-{os.getpid()}",
            "pid": os.getpid(),
            "started_at": int(time.time()),
            "deadline_at": None,
            "packet_ids": [],
        }
        with wave_lock(metadata):
            prefixes = tuple(args.reason_prefix
                             or ("infra-error:", "infra-timeout:"))
            todo = _todo_status()
            for packet in list_packets(("escalated", "pending")):
                reason = packet.get("reason") or ""
                if packet["state"] == "pending":
                    if reason != "reset-infra" or not packet.get("rounds"):
                        continue
                elif not reason.startswith(prefixes):
                    continue
                stale = [r for r in packet["routines"]
                         if not todo.get(_work_key(r["work_id"]))]
                if stale:
                    packet["routines"] = [r for r in packet["routines"]
                                          if not todo.get(_work_key(r["work_id"]))]
                    if not packet["routines"]:
                        packet_path(packet["id"]).unlink()
                        print(f"dropped {packet['id']}: "
                              f"{len(stale)} routine(s) no longer todo")
                        continue
                    packet["bytes"] = sum(r.get("size", 0)
                                          for r in packet["routines"])
                    print(f"trimmed {packet['id']}: "
                          f"{len(stale)} routine(s) no longer todo")
                held = _foreign_claims(packet)
                if held:
                    print(f"skip {packet['id']}: held elsewhere {sorted(held)}")
                    continue
                packet.pop("attempt", None)
                packet["rounds"] = 0
                packet["format_retry_used"] = False
                set_state(packet, "pending", "reset-infra")
                print(f"reset {packet['id']}")
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
