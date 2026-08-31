#!/usr/bin/env python3
"""Run the pinned BizHawk/Gambatte reference capture lane."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PINS_PATH = ROOT / "tools" / "completion" / "bizhawk_pins.toml"
REQUIRED_DOMAINS = ("WRAM", "ROM", "VRAM", "OAM", "HRAM", "CartRAM", "System Bus")
REQUIRED_REGISTERS = ("A", "F", "B", "C", "D", "E", "H", "L", "SP", "PC")


class BizHawkError(RuntimeError):
    pass


def load_pins() -> dict[str, Any]:
    try:
        with PINS_PATH.open("rb") as stream:
            pins = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise BizHawkError(f"cannot load pins: {exc}") from exc
    if pins.get("schema") != 1:
        raise BizHawkError("BizHawk pin schema is not 1")
    return pins


def resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def digest(path: Path) -> str:
    result = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                result.update(chunk)
    except OSError as exc:
        raise BizHawkError(f"cannot hash {path}: {exc}") from exc
    return result.hexdigest()


def pin_status(name: str, pin: dict[str, Any]) -> dict[str, Any]:
    path_text = pin.get("path", "")
    expected = pin.get("sha256", "")
    row: dict[str, Any] = {"status": "UNAVAILABLE", "path": path_text, "sha256": expected}
    if not isinstance(path_text, str) or not path_text:
        row["reason"] = "pin path is not configured"
        return row
    if not isinstance(expected, str) or len(expected) != 64:
        row["reason"] = "pin SHA-256 is not configured"
        return row
    path = resolve(path_text)
    if not path.is_file():
        row["reason"] = "pinned file is missing"
        return row
    actual = digest(path)
    row["actual_sha256"] = actual
    if actual != expected:
        row["status"] = "DRIFT"
        row["reason"] = "pinned file hash differs"
        return row
    row["status"] = "PASS"
    return row


def health_report(pins: dict[str, Any]) -> dict[str, Any]:
    files = {
        name: pin_status(name, pins.get(name, {}))
        for name in ("build", "core", "firmware", "config", "sync", "display", "script", "rom")
    }
    requirements = pins.get("requirements", {})
    domains = requirements.get("domains")
    registers = requirements.get("registers")
    capabilities = {
        "domains": {
            "required": list(REQUIRED_DOMAINS),
            "pinned": domains,
            "status": "PASS" if domains == list(REQUIRED_DOMAINS) else "DRIFT",
        },
        "registers": {
            "required": list(REQUIRED_REGISTERS),
            "pinned": registers,
            "status": "PASS" if registers == list(REQUIRED_REGISTERS) else "DRIFT",
        },
        "bus_scope": {
            "required_contains": requirements.get("scope_contains"),
            "status": "PASS" if requirements.get("scope_contains") == "bus" else "DRIFT",
        },
    }
    status = "PASS" if all(
        row["status"] == "PASS" for row in files.values()
    ) and all(row["status"] == "PASS" for row in capabilities.values()) else "FAIL"
    return {
        "schema": 1,
        "status": status,
        "pins": files,
        "capabilities": capabilities,
        "api": pins.get("api"),
    }


def load_capture(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BizHawkError(f"invalid raw capture: {exc}") from exc
    if not isinstance(value, dict) or value.get("format") != "bizhawk-raw-v1":
        raise BizHawkError("raw capture format is not bizhawk-raw-v1")
    if value.get("schema") != 1:
        raise BizHawkError("raw capture schema is not 1")
    domains = value.get("domains")
    if not isinstance(domains, dict) or any(domain not in domains for domain in REQUIRED_DOMAINS):
        raise BizHawkError("raw capture is missing a required memory domain")
    registers = value.get("registers")
    if not isinstance(registers, dict) or any(
        register not in registers and register.lower() not in registers
        for register in REQUIRED_REGISTERS
    ):
        raise BizHawkError("raw capture is missing a required register")
    if not isinstance(value.get("input_rle"), list) or not value["input_rle"]:
        raise BizHawkError("raw capture has no neutral input log")
    if not isinstance(value.get("trace"), list):
        raise BizHawkError("raw capture has no bus trace")
    screenshot = value.get("screenshot")
    if not isinstance(screenshot, str) or not resolve(screenshot).is_file() and not Path(screenshot).is_file():
        raise BizHawkError("raw capture screenshot is missing")
    return value


def import_capture(path: Path, output: Path, pins: dict[str, Any]) -> dict[str, Any]:
    record = load_capture(path)
    expected_rom = pins["rom"]["sha256"]
    if record.get("rom_sha256", expected_rom) != expected_rom:
        raise BizHawkError("capture ROM identity differs from pins")
    domains = {
        name: hashlib.sha256(bytes.fromhex(record["domains"][name])).hexdigest()
        for name in REQUIRED_DOMAINS
    }
    imported = {
        "schema": 1,
        "format": "bizhawk-import-v1",
        "scenario": record.get("scenario"),
        "input_rle": record["input_rle"],
        "input_sha256": hashlib.sha256(
            json.dumps(record["input_rle"], sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "domain_sha256": domains,
        "registers": record["registers"],
        "trace": record["trace"],
        "bus_scope": record.get("bus_scope"),
        "screenshot_sha256": digest(resolve(record["screenshot"])),
        "raw_capture_sha256": digest(path),
        "oracle": "bizhawk-gambatte",
        "savestate_canonical": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(imported, sort_keys=True, separators=(",", ":")) + "\n")
    return imported


def capture(args: argparse.Namespace, pins: dict[str, Any]) -> int:
    report = health_report(pins)
    if report["status"] != "PASS":
        print(json.dumps(report, sort_keys=True))
        return 2
    executable = resolve(pins["build"]["path"])
    config = resolve(pins["config"]["path"])
    script = resolve(pins["script"]["path"])
    output = args.output or ROOT / "build" / "completion" / "bizhawk" / f"{args.scenario}.json"
    screenshot = output.with_suffix(".png")
    output.parent.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment.update({
        "POKETCG_BIZHAWK_OUTPUT": str(output),
        "POKETCG_BIZHAWK_SCREENSHOT": str(screenshot),
        "POKETCG_BIZHAWK_SCENARIO": args.scenario,
        "POKETCG_BIZHAWK_FRAMES": str(args.frames),
        "POKETCG_BIZHAWK_ANCHOR_ADDR": args.anchor,
        "POKETCG_BIZHAWK_ROM_SHA256": pins["rom"]["sha256"],
    })
    command = [str(executable), "--chromeless", "--config", str(config), "--lua", str(script)]
    try:
        completed = subprocess.run(
            command, cwd=ROOT, env=environment, capture_output=True, text=True,
            timeout=args.timeout, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2
    if completed.returncode:
        print(json.dumps({
            "status": "FAIL", "reason": "BizHawk exited nonzero",
            "returncode": completed.returncode, "stderr": completed.stderr,
        }, sort_keys=True))
        return 2
    try:
        imported = import_capture(output, args.import_output or output.with_suffix(".imported.json"), pins)
    except BizHawkError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({"status": "PASS", "scenario": args.scenario, "import": imported}, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("health", "capture", "import"))
    parser.add_argument("scenario", nargs="?")
    parser.add_argument("--oracle", choices=("bizhawk",), default="bizhawk")
    parser.add_argument("--bizhawk", type=Path)
    parser.add_argument("--frames", type=int, default=1)
    parser.add_argument("--anchor", default="0x0150")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--import-output", type=Path)
    parser.add_argument("--input", type=Path)
    args = parser.parse_args(argv)
    try:
        pins = load_pins()
        if args.bizhawk:
            pins["build"]["path"] = str(args.bizhawk)
        if args.command == "health":
            report = health_report(pins)
            print(json.dumps(report, sort_keys=True))
            return 0 if report["status"] == "PASS" else 2
        if args.command == "import":
            if not args.input or not args.output:
                parser.error("import requires --input and --output")
            imported = import_capture(args.input, args.output, pins)
            print(json.dumps({"status": "PASS", "import": imported}, sort_keys=True))
            return 0
        if not args.scenario:
            parser.error("capture requires a scenario")
        if args.frames < 1:
            parser.error("--frames must be positive")
        return capture(args, pins)
    except (BizHawkError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
