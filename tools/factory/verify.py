#!/usr/bin/env python3
"""Mechanical acceptance for one packet inside a lane.

Pipeline: ninja build -> schema audit -> PyBoy group diff (refresh on case
changes, cached fast path otherwise, live evidence required for acceptance)
-> per-routine mutation RED/PASS -> adapter lint.  Emits a structured verdict;
on green, copies the quad + mutation receipts into .factory/bundles/<id>/.

The verdict "detail" is raw tool output, trimmed — it is the repair-round
feedback payload.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import BUNDLES, CACHE, PBENV, ROOT, RUNNER, load_packet  # noqa: E402
import lanes  # noqa: E402
import surgery  # noqa: E402

TAIL = 4000
TIMEOUT_MARK = "did not return within"


def _tail(text: str) -> str:
    text = text.strip()
    return text[-TAIL:] if len(text) > TAIL else text


def verdict(kind: str, detail: str, routine: str | None = None) -> dict:
    return {"status": kind, "detail": _tail(detail), "routine": routine}


def run(command: list[str], cwd: Path, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True,
                          timeout=timeout, check=False)


def witness_index(mutation_block: dict) -> int:
    ids = mutation_block.get("case_ids") or []
    for case_id in ids:
        match = re.search(r"-(\d+)$", str(case_id))
        if match:
            return int(match.group(1))
    return 0


def load_mutations(lane: Path, basename: str) -> dict:
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
    return getattr(module, "MUTATIONS", {})


def verify_packet(packet: dict, lane: Path, cases_changed: bool) -> dict:
    basename = packet["basename"]
    routine_names = [r["name"] for r in packet["routines"]]

    built = lanes.build(lane)
    if built.returncode != 0:
        return verdict("compile", built.stdout + built.stderr)

    audit = run([sys.executable, "tools/audit_oracle_cases.py", "--stage", "routine"],
                lane)
    if audit.returncode != 0:
        # only failures naming this packet's module/routines are ours
        return verdict("schema", audit.stdout + audit.stderr)

    CACHE.mkdir(parents=True, exist_ok=True)
    mode = "refresh" if cases_changed else "cache"
    diff = run([str(PBENV), "tests/test_leaves.py", "--group", basename,
                "--oracle-mode", mode, "--cache-dir", str(CACHE),
                "--probe", str(lane / "build" / "poketcg_probe")],
               lane, timeout=1800)
    output = diff.stdout + diff.stderr
    if "cache miss" in output:
        mode = "refresh"
        diff = run([str(PBENV), "tests/test_leaves.py", "--group", basename,
                    "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
                    "--probe", str(lane / "build" / "poketcg_probe")],
                   lane, timeout=1800)
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
            if l.startswith("FAIL") or "fail " in l or "!=" in l
            or "Error" in l)
        names = re.findall(r"^FAIL (\S+):", output, flags=re.MULTILINE)
        result = verdict("diff", failing or output)
        result["failing"] = names
        return result
    if mode == "cache":
        live = run([str(PBENV), "tests/test_leaves.py", "--group", basename,
                    "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
                    "--probe", str(lane / "build" / "poketcg_probe")],
                   lane, timeout=1800)
        if live.returncode != 0:
            return verdict("diff", live.stdout + live.stderr)

    mutations = load_mutations(lane, basename)
    for fn in routine_names:
        if fn not in mutations:
            return verdict("mutation", f"MUTATIONS[{fn!r}] is missing", fn)
        index = witness_index(mutations[fn])
        red = run([sys.executable, "tools/run_mutation.py", fn,
                   f"tests/cases/{basename}.py", "--index", str(index),
                   "--build", "build", "--runner", str(RUNNER)],
                  lane, timeout=300)
        if red.returncode != 0:
            return verdict("mutation", red.stdout + red.stderr, fn)

    lint = run([sys.executable, "tools/lint_adapters.py"], lane)
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
