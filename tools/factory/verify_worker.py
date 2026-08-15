#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import surgery
import verify as verify_mod
from common import PhaseTimeout, WaveDeadlineExpired, record_event


def main() -> int:
    payload = json.load(sys.stdin)
    packet = payload["packet"]
    lane = Path(payload["lane"])
    translation = payload["translation"]
    statics_baseline = payload.get("statics_baseline")
    rounds = int(payload["rounds"])
    deadline = float(payload["deadline"])
    wave_id = payload.get("wave_id")
    packet_id = payload.get("packet_id", packet.get("id"))

    last: dict = {"phase": None, "at": time.monotonic()}

    def progress(phase: str) -> None:
        now = time.monotonic()
        if last["phase"] is not None:
            record_event({
                "event": "verify-phase", "wave_id": wave_id, "packet_id": packet_id,
                "round": rounds, "phase": last["phase"],
                "wall_s": round(now - last["at"], 2),
            })
        last["phase"], last["at"] = phase, now

    if statics_baseline is None:
        statics_baseline = surgery.read_statics(lane, packet["basename"])
    progress("surgery")
    try:
        changed = surgery.apply(
            lane, packet, translation, statics_baseline=statics_baseline,
        )
    except surgery.SurgeryError as exc:
        result = {"status": "surgery", "detail": str(exc)}
    else:
        cases_changed = any(str(path).endswith(".py") for path in changed) or rounds == 0
        try:
            result = verify_mod.verify_packet(
                packet, lane, cases_changed, deadline=deadline, progress=progress,
            )
        except PhaseTimeout as exc:
            result = {"status": "infra-timeout", "detail": str(exc)}
        except WaveDeadlineExpired as exc:
            progress("done")
            print(json.dumps({"deadline": str(exc)}))
            return 0
    progress("done")

    print(json.dumps({
        "result": result,
        "statics_baseline": statics_baseline,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
