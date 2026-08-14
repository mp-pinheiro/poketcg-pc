#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import surgery
import verify as verify_mod
from common import PhaseTimeout, WaveDeadlineExpired


def main() -> int:
    payload = json.load(sys.stdin)
    packet = payload["packet"]
    lane = Path(payload["lane"])
    translation = payload["translation"]
    statics_baseline = payload.get("statics_baseline")
    rounds = int(payload["rounds"])
    deadline = float(payload["deadline"])

    if statics_baseline is None:
        statics_baseline = surgery.read_statics(lane, packet["basename"])
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
                packet, lane, cases_changed, deadline=deadline,
            )
        except PhaseTimeout as exc:
            result = {"status": "infra-timeout", "detail": str(exc)}
        except WaveDeadlineExpired as exc:
            print(json.dumps({"deadline": str(exc)}))
            return 0

    print(json.dumps({
        "result": result,
        "statics_baseline": statics_baseline,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
