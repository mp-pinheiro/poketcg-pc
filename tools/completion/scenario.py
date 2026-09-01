#!/usr/bin/env python3
"""Run a packaged scenario and emit revision-keyed evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "build" / "poketcg"
PACK = ROOT / "build" / "completion" / "data-pack.bin"
EVIDENCE_DIR = ROOT / "build" / "completion" / "evidence"
SCENARIO_REQUIREMENTS = {
    "boot-title": "completion:v2:p2:boot-title",
    "boot-title-negative": "completion:v2:p2:boot-title-negative",
    "save-interchange": "completion:v2:p2:save-interchange",
    "audio-catalog": "completion:v2:p3:audio-trace",
    "ui-corpus": "completion:v2:p4:ui-corpus",
    "seeded-duel": "completion:v2:p5:seeded-duel",
    "all-maps-scripts": "completion:v2:p6:maps-and-campaign",
    "new-game-to-credits": "completion:v2:faithful-4x3:release",
    "link-ir-printer": "completion:v2:p7:link-ir",
    "faithful-4x3-corpus": "completion:v2:faithful-4x3:package",
    "widescreen-corpus": "completion:v2:p8:release:enhanced-corpus",
}

SCENARIO_SCHEMAS = {
    "boot-title": "scenario-corpus-v2",
    "boot-title-negative": "negative-evidence-v1",
    "save-interchange": "save-interchange-v1",
    "audio-catalog": "audio-trace-v1",
    "ui-corpus": "scene-corpus-v2",
    "seeded-duel": "duel-corpus-v2",
    "all-maps-scripts": "campaign-corpus-v2",
    "new-game-to-credits": "release-corpus-v2",
    "link-ir-printer": "transport-corpus-v1",
    "faithful-4x3-corpus": "package-proof-v1",
    "widescreen-corpus": "widescreen-corpus-v1",
}


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def state_hash(state: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(state)).hexdigest()
def boot_input(frames: int) -> list[int]:
    values = [0] * frames
    for index, value in ((180, 16), (240, 8), (241, 16)):
        if index < frames:
            values[index] = value
    return values



def current_key() -> str:
    from completion import content_key, load_toml

    return content_key(load_toml(ROOT / "tools/completion/baseline.toml"), load_toml(ROOT / "tools/completion/requirements.toml"))


def evidence_path(requirement: str) -> Path:
    return EVIDENCE_DIR / f"{requirement}.json"


def run_native(
    frames: int, state_path: Path, trace_path: Path, input_path: Path | None = None
) -> tuple[int, str, str]:
    command = [
        str(BINARY), "--headless", "--data-pack", str(PACK), "--frames", str(frames),
        "--dump-state", str(state_path), "--trace-entries", str(trace_path),
    ]
    if input_path is not None:
        command.extend(["--input", str(input_path)])
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return -1, "", str(exc)
    return result.returncode, result.stdout, result.stderr


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", choices=sorted(SCENARIO_REQUIREMENTS))
    parser.add_argument("--frames", type=int, default=600)
    args = parser.parse_args(argv)
    requirement = SCENARIO_REQUIREMENTS[args.scenario]
    key = current_key()
    artifact: dict[str, Any] = {
        "schema": SCENARIO_SCHEMAS[args.scenario],
        "status": "FAIL",
        "content_key": key,
        "scenario": args.scenario,
        "frames": args.frames,
        "events": 0,
        "state_fields": [],
        "oracles": ["native"],
        "required_edges": 0,
        "covered_edges": 0,
    }
    try:
        if args.frames < 1:
            raise ValueError("frame bound must be positive")
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="poketcg-scenario-") as directory:
            state_path = Path(directory) / "state.json"
            trace_path = Path(directory) / "trace.json"
            input_path = None
            if args.scenario == "boot-title":
                input_path = Path(directory) / "input.txt"
                input_path.write_text(
                    ",".join(str(value) for value in boot_input(args.frames)) + "\n",
                    encoding="utf-8",
                )
            returncode, stdout, stderr = run_native(
                args.frames, state_path, trace_path, input_path
            )
            if returncode != 0:
                artifact["failure"] = "EARLY_EXIT"
                artifact["detail"] = stderr.strip() or stdout.strip()
            else:
                state = json.loads(state_path.read_text(encoding="utf-8"))
                trace = json.loads(trace_path.read_text(encoding="utf-8"))
                artifact["state_sha256"] = state_hash(state)
                artifact["pixel_sha256"] = hashlib.sha256(
                    canonical_bytes(state.get("framebuffer", []))
                ).hexdigest()
                artifact["save_sha256"] = hashlib.sha256(
                    canonical_bytes(state.get("save", []))
                ).hexdigest()
                artifact["audio_sha256"] = hashlib.sha256(
                    canonical_bytes(state.get("apu_trace", []))
                ).hexdigest()
                artifact["state_fields"] = sorted(state)
                artifact["events"] = trace.get("events", 0)
                artifact["covered_edges"] = len(trace.get("edges", []))
                artifact["terminal_event"] = trace.get("terminal_event")
                artifact["trace_symbols"] = trace.get("symbols", [])
                if args.scenario == "boot-title":
                    if artifact["terminal_event"] != "NEW_GAME_ENTERED":
                        artifact["failure"] = "TERMINAL_EVENT_MISSING"
                    elif artifact["events"] < 3:
                        artifact["failure"] = "EVENT_BOUND_NOT_MET"
                    else:
                        artifact["failure"] = "REFERENCE_COMPARISON_MISSING"
                elif args.scenario == "boot-title-negative":
                    artifact["failure"] = "REFERENCE_COMPARISON_MISSING"
                else:
                    artifact["failure"] = "REFERENCE_COMPARISON_MISSING"
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        artifact["failure"] = "SCENARIO_ERROR"
        artifact["detail"] = str(exc)
    path = evidence_path(requirement)
    path.write_text(json.dumps(artifact, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({"status": artifact["status"], "scenario": args.scenario, **{
        key: artifact[key] for key in ("failure", "content_key", "frames", "covered_edges")
        if key in artifact
    }}, sort_keys=True))
    return 2


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools" / "completion"))
    raise SystemExit(main())
