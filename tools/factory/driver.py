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

import argparse
import json
import os
import sys
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lanes  # noqa: E402
import prompt as prompt_mod  # noqa: E402
import surgery  # noqa: E402
import verify as verify_mod  # noqa: E402
from common import (  # noqa: E402
    FACTORY,
    METRICS,
    ROOT,
    WaveDeadlineExpired,
    block_routine,
    estimate_tokens,
    list_packets,
    load_packet,
    record_metric,
    run_bounded,
    save_packet,
    set_state,
    wave_lock,
)

IN_FLIGHT = ("translating", "translated", "verifying", "repair")
ACTIVE_CLAIM_STATES = ("pending", *IN_FLIGHT, "green")


class _Run:
    def __init__(self, packet_id: str, wave_id: str, started: float):
        self.packet = load_packet(packet_id)
        self.id = packet_id
        self.wave_id = wave_id
        self.lane_index: int | None = None
        self.lane = None
        self.rounds = int(self.packet.get("rounds", 0))
        self.format_retry_used = bool(self.packet.get("format_retry_used", False))
        self.feedback: str | None = None
        self.targets: list[str] | None = None
        self.last_failing: list[str] | None = None
        self.statics_baseline: list[str] | None = None
        self.prompt_tokens = 0
        self.reply_tokens = 0
        self.started = started
        self.final: str | None = None
        self.reason: str | None = None

    def metric(self, model: str) -> dict:
        work_ids = sorted(r["work_id"] for r in self.packet["routines"])
        return {
            "id": self.id, "verdict": self.final, "reason": self.reason,
            "rounds": self.rounds, "wall_s": round(time.monotonic() - self.started, 1),
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





def _apply_and_verify(packet: dict, lane: Path, translation: dict,
                      statics_baseline: list[str] | None, rounds: int,
                      deadline: float) -> dict:
    """Run surgery and verification behind a killable process boundary."""
    payload = json.dumps({
        "packet": packet,
        "lane": str(lane),
        "translation": translation,
        "statics_baseline": statics_baseline,
        "rounds": rounds,
        "deadline": deadline,
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
    try:
        result = verify_mod.verify_packet(reduced, run.lane, True, deadline=run.deadline)
    except WaveDeadlineExpired:
        raise
    except Exception:
        return False
    if result.get("status") != "green":
        return False
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
    run.packet["routines"] = reduced["routines"]
    save_packet(run.packet)
    try:
        verify_mod.collect_bundle(run.packet, run.lane)
    except Exception as exc:
        run.final = "escalated"
        run.reason = f"infra-error: bundle collection failed: {str(exc)[-300:]}"
        return False
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
    if result["status"] in {"infra-timeout", "infra-error"}:
        run.final = "escalated"
        prefix = result["status"]
        run.reason = f"{prefix}: {result['detail'][-400:]}"
        return False
    run.rounds += 1
    run.packet["rounds"] = run.rounds
    save_packet(run.packet)
    failing_now = result.get("failing") or (
        [result["routine"]] if result.get("routine") else None)
    run.last_failing = failing_now
    if run.rounds >= max_rounds:
        if not _salvage(run, failing_now):
            run.final = "escalated"
            run.reason = f"{result['status']} after {max_rounds} rounds"
        return False
    run.targets = failing_now if failing_now else None
    run.feedback = f"{result['status']}:\n{result['detail']}"
    _attempt(run, "repair", run.deadline, run.rounds)
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
            run.packet["format_retry_used"] = True
            save_packet(run.packet)
            run.feedback = f"format: {exc}"
            return {}
        run.final, run.reason = "rejected-format", str(exc)
        return None


def run_wave(packet_ids: list[str], translate_many, lanes_count: int = 10,
             max_rounds: int = 4, model: str = "unknown", max_wall_s: float = 1800,
             on_event=None) -> dict:
    if lanes_count <= 0 or max_rounds <= 0 or max_wall_s <= 0:
        raise ValueError("lanes_count, max_rounds, and max_wall_s must be positive")
    if any(not isinstance(pid, str) or not pid for pid in packet_ids):
        raise ValueError("wave packet IDs must be non-empty strings")
    if len(set(packet_ids)) != len(packet_ids):
        raise ValueError("wave packet IDs must be unique")
    if len(packet_ids) > lanes_count:
        raise ValueError(
            f"wave has {len(packet_ids)} packets but only {lanes_count} lanes; "
            "select a bounded cohort"
        )
    wave_id = uuid.uuid4().hex
    started = time.monotonic()
    deadline = started + max_wall_s
    events: list[str] = []
    event_errors: list[str] = []
    callbacks_enabled = True

    def emit(event: str, **payload) -> None:
        nonlocal callbacks_enabled
        if not callbacks_enabled:
            return
        data = {"event": event, "elapsed_s": round(time.monotonic() - started, 3), **payload}
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
        runs = [_Run(pid, wave_id, started) for pid in packet_ids]
        for run in runs:
            run.deadline = deadline
        emit("wave-start", wave_id=wave_id, packet_ids=packet_ids, max_wall_s=max_wall_s)
        results: list[dict] = []
        deferred: list[str] = []
        stop_reason = None

        def finalize(run: _Run) -> None:
            _clear_attempt(run)
            set_state(run.packet, run.final, run.reason)
            metric = run.metric(model)
            record_metric(metric)
            results.append(metric)
            emit("packet-final", wave_id=wave_id, packet_id=run.id,
                 verdict=run.final, reason=run.reason, rounds=run.rounds,
                 wall_s=metric["wall_s"])

        for index, run in enumerate(runs):
            run.lane_index = index
            try:
                run.lane = lanes.ensure(index, deadline=deadline)
            except Exception as exc:
                stop_reason = f"lane: {str(exc).strip()[-400:]}"
                break
        for run in runs:
            if run.rounds >= max_rounds:
                run.final = "escalated"
                run.reason = f"resumed at {run.rounds} rounds; max is {max_rounds}"
        for run in runs:
            if run.final:
                finalize(run)
        if stop_reason is None:
            active = [run for run in runs if not run.final]
        if stop_reason is None and active:
            with ThreadPoolExecutor(max_workers=max(1, len(active))) as pool:
                while active:
                    if time.monotonic() >= deadline:
                        stop_reason = "wave deadline expired"
                        break
                    emit("round-start", wave_id=wave_id,
                         rounds={run.id: run.rounds + 1 for run in active})
                    translations: dict[str, dict] = {}
                    pending = list(active)
                    try:
                        for run in pending:
                            _attempt(run, "translating", deadline, run.rounds + 1)
                        prompts = [_render(run) for run in pending]
                        replies = translate_many(prompts)
                        if time.monotonic() >= deadline:
                            raise WaveDeadlineExpired("wave deadline expired after translation")
                        if not isinstance(replies, (list, tuple)) or len(replies) != len(prompts):
                            raise RuntimeError("translator returned wrong reply collection")
                        retry: list[_Run] = []
                        for run, reply in zip(pending, replies):
                            if not isinstance(reply, str):
                                raise RuntimeError("translator returned a non-string reply")
                            parsed = _accept(run, reply)
                            if parsed is None:
                                continue
                            if parsed == {}:
                                retry.append(run)
                            else:
                                translations[run.id] = parsed
                        if retry:
                            prompts = [_render(run) for run in retry]
                            replies = translate_many(prompts)
                            if time.monotonic() >= deadline:
                                raise WaveDeadlineExpired("wave deadline expired after translation")
                            if not isinstance(replies, (list, tuple)) or len(replies) != len(prompts):
                                raise RuntimeError("translator returned wrong reply collection")
                            for run, reply in zip(retry, replies):
                                if not isinstance(reply, str):
                                    raise RuntimeError("translator returned a non-string reply")
                                parsed = _accept(run, reply)
                                if parsed is not None and parsed != {}:
                                    translations[run.id] = parsed
                    except WaveDeadlineExpired as exc:
                        stop_reason = str(exc)
                        deferred = [run.id for run in active if not run.final]
                        for run in active:
                            if not run.final:
                                _clear_attempt(run)
                                set_state(run.packet, "pending", stop_reason)
                        break
                    except Exception as exc:
                        stop_reason = f"translate: {str(exc).strip()[-400:]}"
                        deferred = [run.id for run in active if not run.final]
                        for run in active:
                            if not run.final:
                                _clear_attempt(run)
                                set_state(run.packet, "pending", stop_reason)
                        break
                    futures = {}
                    try:
                        for run in active:
                            if run.id not in translations or run.final:
                                continue
                            _attempt(run, "verifying", deadline, run.rounds)
                            future = pool.submit(
                                _apply_and_verify,
                                run.packet,
                                run.lane,
                                translations[run.id],
                                run.statics_baseline,
                                run.rounds,
                                deadline,
                            )
                            futures[future] = run
                    except Exception as exc:
                        stop_reason = f"verify setup: {str(exc).strip()[-400:]}"
                        deferred = [run.id for run in active if not run.final]
                        break
                    verdicts: dict[str, dict] = {}
                    try:
                        for future in as_completed(futures):
                            run = futures[future]
                            try:
                                verdict = future.result()
                                run.statics_baseline = verdict.pop("_statics_baseline")
                                verdicts[run.id] = verdict
                            except WaveDeadlineExpired:
                                raise
                            except Exception:
                                verdicts[run.id] = {
                                    "status": "infra-error",
                                    "detail": traceback.format_exc(limit=4),
                                }
                            emit("verify-finished", wave_id=wave_id, packet_id=run.id,
                                 round=run.rounds, status=verdicts[run.id]["status"])
                    except WaveDeadlineExpired as exc:
                        stop_reason = str(exc)
                        deferred = [run.id for run in active if not run.final]
                        break
                    if stop_reason is not None:
                        break
                    still: list[_Run] = []
                    for run in active:
                        if run.final:
                            finalize(run)
                            continue
                        result = verdicts.get(run.id)
                        if result is None:
                            deferred.append(run.id)
                            _clear_attempt(run)
                            set_state(run.packet, "pending", "translator stopped")
                            continue
                        if _decide(run, result, max_rounds):
                            still.append(run)
                        else:
                            finalize(run)
                    active = still
        if stop_reason is not None:
            for run in runs:
                if not run.final and run.id not in deferred:
                    deferred.append(run.id)
                if not run.final:
                    _clear_attempt(run)
                    set_state(run.packet, "pending", stop_reason)
            emit("wave-deferred", wave_id=wave_id, packet_ids=deferred, reason=stop_reason)
        status = "complete" if stop_reason is None else (
            "deadline" if "deadline" in stop_reason else "stopped"
        )
        emit("wave-finish", wave_id=wave_id, status=status,
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


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("reset-stale")
    sub.add_parser("metrics")
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
                packet.pop("attempt", None)
                set_state(packet, "pending", "reset-stale")
                print(f"reset {packet['id']}")
    elif args.command == "escalate":
        return escalate(args.limit)
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
