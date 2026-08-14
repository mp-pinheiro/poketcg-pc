#!/usr/bin/env python3
"""Mechanical acceptance for one packet inside a lane.

Pipeline: ninja build -> static case-lint (no PyBoy, no registry import) ->
schema audit -> PyBoy diff, scoped to the packet's own routines (refresh on
case changes, cached fast path otherwise, live evidence required for
acceptance) -> per-routine mutation RED/PASS -> adapter lint.  Case-lint runs
before the schema audit deliberately: ``tests/routines.py`` eagerly imports
every case module to derive the registry, so a malformed case module (the
exact class of bug case-lint exists to catch) would otherwise crash the
audit subprocess with an opaque traceback instead of a targeted verdict.
Emits a structured verdict; on green, copies the quad + mutation receipts
into .factory/bundles/<id>/.

The verdict "detail" is raw tool output, trimmed — it is the repair-round
feedback payload.
"""

from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (BUNDLES, CACHE, ORACLE_PYTHON, ROOT, RUNNER, PhaseTimeout,
                    WaveDeadlineExpired, load_packet, packet_identity,
                    run_bounded)  # noqa: E402
import lanes  # noqa: E402
import surgery  # noqa: E402

TAIL = 4000
TIMEOUT_MARK = "did not return within"


def _tail(text: str) -> str:
    text = text.strip()
    return text[-TAIL:] if len(text) > TAIL else text


def fn_args(routine_names: list[str]) -> list[str]:
    return [arg for fn in routine_names for arg in ("--fn", fn)]




def compile_cause(output: str) -> str:
    """Diagnostics only: ninja echoes multi-kB link command lines that would
    otherwise crowd the real cause out of the trimmed feedback."""
    keep = [
        line for line in output.splitlines()
        if ("error:" in line or "undefined reference" in line
            or "warning:" in line or line.startswith("src/")
            or "In function" in line)
        and " -o " not in line
    ]
    return "\n".join(keep) if keep else output


def verdict(kind: str, detail: str, routine: str | None = None) -> dict:
    return {"status": kind, "detail": _tail(detail), "routine": routine}


def run(command: list[str], cwd: Path, timeout: float = 600,
        deadline: float | None = None) -> subprocess.CompletedProcess[str]:
    return run_bounded(command, cwd=cwd, cap=timeout, deadline=deadline, check=False)

def witness_index(mutation_block: dict) -> int:
    ids = mutation_block.get("case_ids") or []
    for case_id in ids:
        match = re.search(r"-(\d+)$", str(case_id))
        if match:
            return int(match.group(1))
    return 0


def load_cases_module(lane: Path, basename: str):
    import importlib.util
    path = lane / "tests" / "cases" / f"{basename}.py"
    spec = importlib.util.spec_from_file_location(f"verify_cases_{basename}", path)
    module = importlib.util.module_from_spec(spec)
    saved = list(sys.path)
    sys.path.insert(0, str(lane))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = saved
    return module


POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
RESERVED = range(0xCF00, 0xD000)


def case_lint(lane: Path, basename: str, routine_names: list[str]) -> dict[str, list[str]]:
    """Mechanical, PyBoy-free checks. Deliberately does not trust the case
    module to import cleanly: an undefined name in it (e.g. a stray C
    `_ADDR` macro referenced as a bare Python identifier — those macros do
    not exist in Python, only inside quoted MUTATIONS text) would otherwise
    crash the schema audit's subprocess too, since ``tests/routines.py``
    eagerly imports every case module to derive the registry. Run this
    before that subprocess."""
    violations: dict[str, list[str]] = {}

    def fail(fn: str, msg: str) -> None:
        violations.setdefault(fn, []).append(msg)

    try:
        module = load_cases_module(lane, basename)
    except Exception as exc:
        for fn in routine_names:
            fail(fn, f"case module fails to import: {exc}")
        return violations
    contract = getattr(module, "CONTRACT", {})
    cases = getattr(module, "CASES", {})
    mutations = getattr(module, "MUTATIONS", {})

    for fn in routine_names:
        fn_cases = cases.get(fn, [])
        if fn not in contract:
            fail(fn, f"CONTRACT[{fn!r}] is missing")
            continue
        if not any(sum(1 for reg, value in POISON.items()
                       if c.get(reg) == value) >= 4 for c in fn_cases):
            fail(fn, f"CASES[{fn!r}] has no poisoned-register case "
                     f"(need >=4 of a=0xAA f=0xF0 b=0xBB c=0xCC d=0xDD e=0xEE hl=0x1234)")
        for i, c in enumerate(fn_cases):
            for key in ("wram", "read", "expect"):
                for addr in c.get(key, {}) or {}:
                    if int(addr) in RESERVED:
                        fail(fn, f"CASES[{fn!r}][{i}].{key} writes reserved "
                                 f"${int(addr):04X} (oracle call frame $CF00-$CFFF)")
            if c.get("oracle") is False:
                why = c.get("why")
                expects = ("expect", "expect_regs", "expect_sram", "expect_vram")
                if not (isinstance(why, str) and why.strip()):
                    fail(fn, f"CASES[{fn!r}][{i}] has oracle=False without a non-empty why")
                if not any(c.get(k) for k in expects):
                    fail(fn, f"CASES[{fn!r}][{i}] has oracle=False without any of {expects}")
        block = mutations.get(fn)
        if block:
            for case_id in block.get("case_ids") or []:
                match = re.fullmatch(rf"{re.escape(fn)}-(\d+)", str(case_id))
                if not match or not (0 <= int(match.group(1)) < len(fn_cases)):
                    fail(fn, f"MUTATIONS[{fn!r}][case_ids] has invalid id {case_id!r} "
                             f"for {len(fn_cases)} cases")
    return violations


def verify_packet(packet: dict, lane: Path, cases_changed: bool,
                  deadline: float | None = None) -> dict:
    basename = packet["basename"]
    routine_names = [r["name"] for r in packet["routines"]]

    try:
        built = lanes.build(lane, deadline)
    except (PhaseTimeout, WaveDeadlineExpired) as exc:
        if isinstance(exc, WaveDeadlineExpired):
            raise
        return verdict("infra-timeout", str(exc))
    try:
        inspected = run_bounded(
            [sys.executable, str(ROOT / "tools/factory" / "case_inspect.py"),
             "--lane", str(lane), "--basename", basename,
             *[arg for fn in routine_names for arg in ("--fn", fn)]],
            cwd=lane, cap=60, deadline=deadline, check=True,
        )
        inspection = json.loads(inspected.stdout)
    except WaveDeadlineExpired:
        raise
    except PhaseTimeout as exc:
        return verdict("infra-timeout", str(exc))
    except Exception as exc:
        return verdict("infra-error", traceback.format_exc(limit=2))
    if inspection.get("violations"):
        result = verdict("cases", json.dumps(inspection["violations"], sort_keys=True))
        result["failing"] = sorted(inspection["violations"])
        return result

    audit = run([sys.executable, "tools/audit_oracle_cases.py", "--stage", "routine",
                "--only", basename], lane, deadline=deadline)
    if audit.returncode != 0:
        return verdict("schema", audit.stdout + audit.stderr)

    CACHE.mkdir(parents=True, exist_ok=True)
    mode = "refresh" if cases_changed else "cache"
    diff = run([*ORACLE_PYTHON, "tests/test_leaves.py", *fn_args(routine_names),
                "--oracle-mode", mode, "--cache-dir", str(CACHE),
                "--probe", str(lane / "build" / "poketcg_probe")],
               lane, timeout=1800, deadline=deadline)
    output = diff.stdout + diff.stderr
    if "cache miss" in output:
        mode = "refresh"
        diff = run([*ORACLE_PYTHON, "tests/test_leaves.py", *fn_args(routine_names),
                    "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
                    "--probe", str(lane / "build" / "poketcg_probe")],
                   lane, timeout=1800, deadline=deadline)
        output = diff.stdout + diff.stderr
    if TIMEOUT_MARK in output:
        spinner = None
        for line in output.splitlines():
            if TIMEOUT_MARK in line:
                match = re.search(r"OracleError: (\S+) did not return", line)
                spinner = match.group(1) if match else None
                break
        return verdict("timeout", output, spinner)
    if diff.returncode != 0:
        failing = "\n".join(
            l for l in output.splitlines()
            if l.startswith("FAIL") or "fail " in l or "!=" in l or "Error" in l
        )
        names = re.findall(r"^FAIL (\S+):", output, flags=re.MULTILINE)
        result = verdict("diff", failing or output)
        result["failing"] = names
        return result
    if mode == "cache":
        live = run([*ORACLE_PYTHON, "tests/test_leaves.py", *fn_args(routine_names),
                    "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
                    "--probe", str(lane / "build" / "poketcg_probe")],
                   lane, timeout=1800, deadline=deadline)
        if live.returncode != 0:
            return verdict("diff", live.stdout + live.stderr)

    witnesses = inspection.get("witnesses", {})
    for fn in routine_names:
        index = witnesses.get(fn)
        if index is None:
            return verdict("mutation", f"MUTATIONS[{fn!r}] is missing", fn)
        red = run([sys.executable, "tools/run_mutation.py", fn,
                   f"tests/cases/{basename}.py", "--index", str(index),
                   "--build", "build", "--runner", str(RUNNER)],
                  lane, timeout=300, deadline=deadline)
        if red.returncode != 0:
            return verdict("mutation", red.stdout + red.stderr, fn)

    lint = run([sys.executable, "tools/lint_adapters.py"], lane,
               timeout=600, deadline=deadline)
    if lint.returncode != 0:
        return verdict("lint", lint.stdout + lint.stderr)

    return verdict("green", "all checks passed")


def collect_bundle(packet: dict, lane: Path) -> Path:
    bundle = BUNDLES / packet["id"]
    if bundle.exists():
        shutil.rmtree(bundle)
    basename = packet["basename"]
    rels = [f"src/home/{basename}.c", f"src/home/{basename}.h",
            f"src/probe/{basename}.c", f"tests/cases/{basename}.py"]
    rels += [f"tools/oracle/mutation_receipts/{r['name']}.json"
             for r in packet["routines"]]
    for rel in rels:
        source = lane / rel
        if not source.exists():
            raise RuntimeError(f"bundle input missing: {source}")
        dest = bundle / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    metadata = packet_identity(packet)
    (bundle / "packet.json").write_text(
        json.dumps(metadata, sort_keys=True, indent=2) + "\n"
    )
    return bundle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet")
    parser.add_argument("--lane", type=Path, required=True)
    parser.add_argument("--cases-changed", action="store_true")
    args = parser.parse_args()
    packet = load_packet(args.packet)
    result = verify_packet(packet, args.lane, args.cases_changed)
    if result["status"] == "green":
        bundle = collect_bundle(packet, args.lane)
        result["bundle"] = str(bundle)
    print(json.dumps(result, indent=1))
    return 0 if result["status"] == "green" else 1


if __name__ == "__main__":
    raise SystemExit(main())
