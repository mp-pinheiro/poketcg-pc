#!/usr/bin/env python3
"""Run a packaged scenario and emit revision-keyed evidence."""

from __future__ import annotations

import argparse
import hashlib
import re
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
BINARY = ROOT / "build" / "poketcg"
PACK = ROOT / "build" / "completion" / "data-pack.bin"
EVIDENCE_DIR = ROOT / "build" / "completion" / "evidence"
SCENARIO_REQUIREMENTS = {
    "boot-title": "completion:v2:p2:boot-title",
    "boot-title-negative": "completion:v2:p2:boot-title-negative",
    "save-interchange": "completion:v2:p2:save-interchange",
    "audio-catalog": "completion:v2:p3:audio-trace",
    "audio-pcm": "completion:v2:p3:audio-pcm",
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
    "audio-pcm": "audio-pcm-v1",
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
    for index, value in ((1000, 16), (1100, 8), (1101, 16), (1200, 128), (1201, 16)):
        if index < frames:
            values[index] = value
    return values

def reference_boot_input() -> str:
    return "f1000:A:1,f1100:D:1,f1101:A:1,f1200:S:1,f1201:A:1"

AUDIO_WRITE_RE = re.compile(
    r"\[WRITE\]\s+cyc=(\d+)\s+addr=([0-9A-Fa-f]{4}).*<=\s+([0-9A-Fa-f]{2})"
)


def parse_reference_audio(path: Path) -> list[dict[str, int]]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = AUDIO_WRITE_RE.search(line)
        if match:
            records.append({
                "tick": int(match.group(1)),
                "address": int(match.group(2), 16),
                "value": int(match.group(3), 16),
            })
    if not records:
        raise ValueError("reference audio trace has no register writes")
    return records



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
    if args.frames < 1:
        raise ValueError("frame bound must be positive")
    run_frames = max(args.frames, 2000) if args.scenario == "boot-title" else args.frames
    requirement = SCENARIO_REQUIREMENTS[args.scenario]
    key = current_key()
    artifact: dict[str, Any] = {
        "schema": SCENARIO_SCHEMAS[args.scenario],
        "status": "FAIL",
        "content_key": key,
        "scenario": args.scenario,
        "frames": run_frames,
        "state_fields": [],
        "oracles": ["native"],
        "required_edges": 0,
        "covered_edges": 0,
    }
    try:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="poketcg-scenario-") as directory:
            state_path = Path(directory) / "state.json"
            trace_path = Path(directory) / "trace.json"
            input_path = None
            if args.scenario == "boot-title":
                input_path = Path(directory) / "input.txt"
                input_path.write_text(
                    ",".join(str(value) for value in boot_input(run_frames)) + "\n",
                    encoding="utf-8",
                )
            returncode, stdout, stderr = run_native(
                run_frames, state_path, trace_path, input_path
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
                        try:
                            from tests.scene_diff import STATE_FIELDS, _first_difference, _state_field
                            from tools.oracle.gbrecomp_oracle import Oracle

                            reference_save = Path(directory) / "reference.gbs"
                            with Oracle(timeout=60.0) as oracle:
                                reference = oracle.run(
                                    input_file=reference_boot_input(),
                                    frame_limit=run_frames,
                                    save_state=reference_save,
                                )
                            mismatches = []
                            for field in STATE_FIELDS:
                                reference_value = _state_field(reference.state, field)
                                native_value = _state_field(state, field)
                                if reference_value is None or native_value is None:
                                    mismatches.append({"field": field, "reason": "missing"})
                                    continue
                                offset = _first_difference(reference_value, native_value)
                                if offset is not None:
                                    mismatches.append({"field": field, "offset": offset})
                            artifact["oracles"] = ["oracle-b", "native"]
                            artifact["comparison"] = {
                                "status": "PASS" if not mismatches else "FAIL",
                                "mismatches": mismatches,
                            }
                            if mismatches:
                                artifact["failure"] = "STATE_MISMATCH"
                            else:
                                artifact["status"] = "PASS"
                                artifact.pop("failure", None)
                        except (OSError, ValueError, RuntimeError) as exc:
                            artifact["failure"] = "ORACLE_ERROR"
                            artifact["detail"] = str(exc)
                elif args.scenario == "audio-catalog":
                    try:
                        from tools.oracle.gbrecomp_oracle import Oracle

                        reference_trace = Path(directory) / "reference-audio.log"
                        with Oracle(timeout=60.0) as oracle:
                            oracle.run(frame_limit=run_frames, audio_trace=reference_trace)
                        reference_audio = parse_reference_audio(reference_trace)
                        native_audio = state.get("apu_trace")
                        if not isinstance(native_audio, list):
                            raise ValueError("native audio trace is not a list")
                        native_pairs = [
                            (int(item["address"]), int(item["value"]))
                            for item in native_audio
                            if isinstance(item, dict)
                            and "address" in item
                            and "value" in item
                        ]
                        reference_pairs = [
                            (item["address"], item["value"]) for item in reference_audio
                        ]
                        common = min(len(native_pairs), len(reference_pairs))
                        first_mismatch = next(
                            (
                                index for index in range(common)
                                if native_pairs[index] != reference_pairs[index]
                            ),
                            common if len(native_pairs) != len(reference_pairs) else None,
                        )
                        artifact["oracles"] = ["oracle-b", "native"]
                        artifact["comparison"] = {
                            "native_writes": len(native_pairs),
                            "reference_writes": len(reference_pairs),
                            "first_mismatch": first_mismatch,
                            "status": "PASS" if first_mismatch is None else "FAIL",
                        }
                        if first_mismatch is None:
                            artifact["status"] = "PASS"
                            artifact["terminal_event"] = "AUDIO_TRACE_CLOSED"
                            artifact.pop("failure", None)
                        else:
                            artifact["failure"] = "AUDIO_TRACE_MISMATCH"
                    except (OSError, ValueError, RuntimeError) as exc:
                        artifact["failure"] = "ORACLE_ERROR"
                        artifact["detail"] = str(exc)
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
