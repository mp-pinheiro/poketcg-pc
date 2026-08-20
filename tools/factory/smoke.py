#!/usr/bin/env python3
"""Red/green rehearsal of the real port pipeline on a landed routine.

Every stage calls the production module it is named after, so a contract drift
between prompt, reply validation, surgery, verification, artifact staging, and
the integration saga fails here instead of consuming a live attempt. The
contract tier is offline and compiler-free; the full tier adds the lane build,
the oracle, and a throwaway git remote.

The fixture routine is `_PauseSong`: two cases, one call, already landed and
gate-passing, so any red is a harness defect rather than a port defect.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from collections.abc import Callable
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common
import integrate
import lanes
import packet as packet_mod
import prompt as prompt_mod
import surgery
import verify
import workers

WORK_ID = "port:v1:src/audio/music1.asm:_PauseSong"
FN = "_PauseSong"
BASENAME = "music1"
FIXTURE = Path(__file__).with_name("fixtures") / f"{FN}.reply.json"
QUARTET = (
    f"src/home/{BASENAME}.c",
    f"src/home/{BASENAME}.h",
    f"src/probe/{BASENAME}.c",
    f"tests/cases/{BASENAME}.py",
)
RECEIPT = f"tools/oracle/mutation_receipts/{FN}.json"
LANE_INDEX = 999
FRAGMENT_KEYS = {"C": "c", "H": "header", "PROBE": "probe", "CASES": "cases",
                 "MUTATION": "mutation"}


class StageFailure(RuntimeError):
    def __init__(self, message: str, payload: Any = None) -> None:
        super().__init__(message)
        self.payload = payload


def _require(condition: bool, message: str, payload: Any = None) -> None:
    if not condition:
        raise StageFailure(message, payload)


def _recorded_reply(attempt_id: str) -> dict[str, Any]:
    reply = json.loads(FIXTURE.read_text())
    reply["attempt_id"] = attempt_id
    return reply


def stage_packet(state: dict[str, Any]) -> str:
    functions, _inventory = packet_mod.compute_functions()
    matched = [f for f in functions if f["work_id"] == WORK_ID]
    _require(len(matched) == 1, f"inventory has no unique {WORK_ID}",
             [f["name"] for f in matched])
    packets = packet_mod.build_packets_for_work_ids(
        {WORK_ID}, issue_numbers={WORK_ID: 0})
    _require(len(packets) == 1, "expected exactly one packet", len(packets))
    built = packets[0]
    _require(len(built["routines"]) == 1, "expected exactly one routine",
             [r["name"] for r in built["routines"]])
    routine = built["routines"][0]
    _require(routine["name"] == FN, "packet routine is not the fixture", routine["name"])
    _require(bool(routine["asm"].strip()), "packet asm slice is empty")
    common.validate_packet(built)

    recorded = _recorded_reply(built["attempt_id"])["routines"][0]
    live = surgery.extract(common.ROOT, built)["routines"][FN]
    drift = [key for key, field in FRAGMENT_KEYS.items() if live[key] != recorded[field]]
    _require(not drift, f"{FN} quartet no longer matches the recorded fixture: {drift}. "
                        f"Re-record tools/factory/fixtures/{FN}.reply.json or pick "
                        f"another landed routine.",
             {key: {"repo": live[key], "fixture": recorded[FRAGMENT_KEYS[key]]}
              for key in drift})
    state["packet"] = built
    state["reply"] = _recorded_reply(built["attempt_id"])
    return f"{FN} {routine['size']}B feature={routine['feature_class']}"


def stage_prompt(state: dict[str, Any]) -> str:
    built = state["packet"]
    rendered = prompt_mod.render(built)
    example = prompt_mod.example_quad(built["example"])
    _require(example in rendered, "prompt does not carry its fragment example")
    for pattern in ("#include", "#ifndef", "#define", "#endif", "ProbeEntry",
                    "SCHEMA2_CASES", "probe_entries_"):
        _require(pattern not in example,
                 f"fragment example leaks whole-file syntax: {pattern}", example)
    for rule in ("C:", "header:", "probe:", "cases:", "mutation:"):
        _require(any(line.startswith(rule) for line in rendered.splitlines()),
                 f"prompt lost its {rule!r} fragment rule")
    _require("# OUTPUT FORMAT — MANDATORY" in rendered, "prompt lost its output contract")
    _require(built["attempt_id"] in rendered,
             "prompt demands an attempt_id it never states, so no credential-free "
             "generator can satisfy it")
    for routine in built["routines"]:
        _require(routine["name"] in rendered,
                 f"prompt never names routine {routine['name']}")
    poison = max(verify.POISON.values())
    _require(f"0x{poison:04X}" in rendered and "0xAA" in rendered,
             "prompt does not state the poisoned-register values case_lint enforces")
    _require(f"${verify.RESERVED.start:04X}" in rendered,
             "prompt does not state the reserved oracle call frame case_lint enforces")
    _require("case_ids" in rendered,
             "prompt does not state the mutation case-id rule case_lint enforces")
    state["prompt"] = rendered
    return f"{len(rendered)} chars, example {len(example)} chars"


def stage_validate(state: dict[str, Any]) -> str:
    built, reply = state["packet"], state["reply"]
    try:
        translation = workers.validate_translation_v2(built, reply)
    except (TypeError, ValueError) as exc:
        raise StageFailure(f"the reply under test was rejected: {exc}",
                           reply["routines"][0]) from exc
    _require(set(translation["routines"]) == {FN}, "validated translation lost the routine")

    def mutate(field: str, value: str) -> dict[str, Any]:
        broken = json.loads(json.dumps(reply))
        broken["routines"][0][field] = value
        return broken

    rejects = {
        "whole-file c": mutate("c", '#include "home/music1.h"\n'
                                    "void _PauseSong(void) { Music1_PauseSong(); }"),
        "guarded header": mutate("header", "#ifndef X\n#define X\nvoid _PauseSong(void);\n#endif"),
        "probe table": mutate(
            "probe",
            "static void adapt__PauseSong(ProbeState *s) { (void)s; _PauseSong(); }\n"
            "const ProbeEntry probe_entries_music1[] = { { NULL, NULL }, };"),
        "cases module table": mutate(
            "cases", 'CASES = {}\nCONTRACT["_PauseSong"] = {}\nCASES["_PauseSong"] = []'),
        "foreign mutation": mutate(
            "mutation", 'MUTATIONS["_ResumeSong"] = {"source_symbol": "_ResumeSong"}'),
    }
    accepted = []
    for label, broken in rejects.items():
        try:
            workers.validate_translation_v2(built, broken)
        except (TypeError, ValueError):
            continue
        accepted.append(label)
    _require(not accepted, f"reply validation accepted malformed fragments: {accepted}",
             {label: rejects[label]["routines"][0] for label in accepted})
    state["translation"] = translation
    return f"1 accepted, {len(rejects)} rejected"


def _minimal_tree(root: Path) -> None:
    for relative in (*QUARTET, RECEIPT, "tests/cases/_schema_migration.py"):
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(common.ROOT / relative, destination)
    headers: set[str] = set()
    for relative in QUARTET[:3]:
        headers |= set(surgery.INCLUDE_LINE.findall((common.ROOT / relative).read_text()))
    for header in sorted(headers):
        for base in ("src", "include"):
            source = common.ROOT / base / header
            if source.is_file():
                destination = root / base / header
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                break


def stage_surgery_roundtrip(state: dict[str, Any]) -> str:
    built, translation = state["packet"], state["translation"]
    with tempfile.TemporaryDirectory(prefix="factory-smoke-") as directory:
        tree = Path(directory)
        _minimal_tree(tree)
        surgery.remove(tree, built, [FN])
        removed = (tree / QUARTET[0]).read_text()
        _require(f"factory {FN} */" not in removed, "remove left the C marker behind")
        surgery.apply(tree, built, translation)
        first = {relative: (tree / relative).read_bytes() for relative in QUARTET}
        extracted = surgery.extract(tree, built)["routines"][FN]
        recorded = state["reply"]["routines"][0]
        drift = [key for key, field in FRAGMENT_KEYS.items()
                 if extracted[key] != recorded[field]]
        _require(not drift, f"apply/extract is not an inverse pair: {drift}",
                 {key: extracted[key] for key in drift})

        surgery.remove(tree, built, [FN])
        surgery.apply(tree, built, translation)
        second = {relative: (tree / relative).read_bytes() for relative in QUARTET}
        unstable = [relative for relative in QUARTET if first[relative] != second[relative]]
        _require(not unstable, f"remove/apply is not a fixed point: {unstable}",
                 {relative: second[relative].decode(errors="replace")[-400:]
                  for relative in unstable})

        probe = (tree / QUARTET[2]).read_text()
        rows = probe.count(f'{{ "{FN}", adapt_{FN} }},')
        _require(rows == 1, f"probe table has {rows} rows for {FN}", probe[-800:])

        module = verify.load_cases_module(tree, BASENAME)
        repo_module = verify.load_cases_module(common.ROOT, BASENAME)
        for table in ("CONTRACT", "CASES", "MUTATIONS"):
            _require(getattr(module, table)[FN] == getattr(repo_module, table)[FN],
                     f"{table}[{FN!r}] changed through the roundtrip",
                     {"roundtrip": getattr(module, table)[FN],
                      "repo": getattr(repo_module, table)[FN]})
        _require(module.SCHEMA2_CASES.get(FN) == repo_module.SCHEMA2_CASES.get(FN),
                 "schema-2 projection of the fixture routine changed",
                 {"roundtrip": module.SCHEMA2_CASES.get(FN),
                  "repo": repo_module.SCHEMA2_CASES.get(FN)})
    return "fragments identical, cycle is a fixed point"


def stage_build(state: dict[str, Any]) -> str:
    built = state["packet"]
    lane = lanes.ensure(LANE_INDEX, packet=built)
    started = time.monotonic()
    result = lanes.build(lane)
    _require(result.returncode == 0, "lane build failed",
             (result.stdout + result.stderr)[-3000:])
    probe = lane / "build" / "poketcg_probe"
    _require(probe.is_file(), f"lane build produced no probe at {probe}")
    state["lane"] = lane
    return f"{lane} in {round(time.monotonic() - started, 1)}s"


def stage_verify(state: dict[str, Any]) -> str:
    built, lane = state["packet"], state["lane"]
    baseline = surgery.read_statics(lane, BASENAME)
    surgery.apply(lane, built, state["translation"], statics_baseline=baseline)
    started = time.monotonic()
    result = verify.verify_packet(built, lane, True)
    _require(result.get("status") == "green", f"verify returned {result.get('status')}",
             result)
    return f"green in {round(time.monotonic() - started, 1)}s"


def _line_delta(repo: str, bundled: str) -> dict[str, list[str]]:
    before, after = repo.splitlines(), bundled.splitlines()
    return {
        "lost": sorted(set(before) - set(after))[:20],
        "gained": sorted(set(after) - set(before))[:20],
    }


def stage_artifact(state: dict[str, Any]) -> str:
    built, lane = state["packet"], state["lane"]
    staged = workers.stage_bundle(built, lane)
    stored = workers.store_artifact(staged)
    root = Path(stored["artifact_dir"])
    identical = []
    for relative in QUARTET:
        bundled = (root / relative).read_text()
        repo = (common.ROOT / relative).read_text()
        if bundled == repo:
            identical.append(relative)
            continue
        _require(sorted(bundled.splitlines()) == sorted(repo.splitlines()),
                 f"bundled {relative} gained or lost lines against the repo original",
                 _line_delta(repo, bundled))
    extracted = surgery.extract(root, built)["routines"][FN]
    recorded = state["reply"]["routines"][0]
    drift = [key for key, field in FRAGMENT_KEYS.items()
             if extracted[key] != recorded[field]]
    _require(not drift, f"bundled fragments differ from the accepted reply: {drift}",
             {key: extracted[key] for key in drift})
    rows = (root / QUARTET[2]).read_text().count(f'{{ "{FN}", adapt_{FN} }},')
    _require(rows == 1, f"bundled probe table has {rows} rows for {FN}")
    _require((root / RECEIPT).is_file(), f"bundle lacks {RECEIPT}")
    _require(workers.artifact_exists(stored["artifact_sha256"]),
             "stored artifact does not validate")
    state["artifact_sha256"] = stored["artifact_sha256"]
    return (f"{stored['artifact_sha256'][:16]}, {len(identical)}/{len(QUARTET)} files "
            f"byte-identical to the repo")


def _stub_scripts(root: Path) -> tuple[Path, Path]:
    gate = root / "stub-gate.py"
    gate.write_text(
        "import json, pathlib, subprocess\n"
        "revision = subprocess.run(['jj', 'log', '--no-graph', '-r', '@-', '-T', 'commit_id'],\n"
        "                          capture_output=True, text=True, check=True).stdout.strip()\n"
        "path = pathlib.Path('site/data/gate.json')\n"
        "path.parent.mkdir(parents=True, exist_ok=True)\n"
        "path.write_text(json.dumps({'commit': revision, 'complete': True,\n"
        "                            'stub': 'factory-smoke'}, sort_keys=True) + '\\n')\n"
    )
    progress = root / "stub-progress.py"
    progress.write_text(
        "import json, pathlib, subprocess\n"
        "revision = subprocess.run(['jj', 'log', '--no-graph', '-r', '@-', '-T', 'commit_id'],\n"
        "                          capture_output=True, text=True, check=True).stdout.strip()\n"
        "path = pathlib.Path('site/data/progress.json')\n"
        "path.parent.mkdir(parents=True, exist_ok=True)\n"
        "path.write_text(json.dumps({'source': revision, 'stub': 'factory-smoke'},\n"
        "                           sort_keys=True) + '\\n')\n"
    )
    return gate, progress


def _git(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    _require(result.returncode == 0, f"{' '.join(command)} failed",
             (result.stdout + result.stderr)[-2000:])
    return result.stdout.strip()


def stage_integrate(state: dict[str, Any]) -> str:
    saved_factory = integrate.FACTORY
    saved_clone = integrate.ensure_v2_clone
    with tempfile.TemporaryDirectory(prefix="factory-smoke-remote-",
                                     ignore_cleanup_errors=True) as directory:
        root = Path(directory)
        remote = root / "remote.git"
        clone = root / "clone"
        _git(["git", "clone", "--bare", str(common.ROOT), str(remote)], root)
        before = int(_git(["git", "rev-list", "--count", "main"], remote))
        _git(["jj", "git", "clone", "--colocate", str(remote), str(clone)], root)
        _git(["jj", "config", "set", "--repo",
              "experimental-advance-branches.enabled-branches", "[]"], clone)
        gate, progress = _stub_scripts(root)
        phases: list[str] = []
        integrate.FACTORY = root / "factory"
        integrate.ensure_v2_clone = lambda: clone
        try:
            expected = integrate._revision(clone, "main@origin")
            result = integrate.integrate_v2(
                [state["artifact_sha256"]],
                expected_remote_revision=expected,
                phase=lambda name, _proof: phases.append(name),
                gate_command=(sys.executable, str(gate)),
                progress_command=(sys.executable, str(progress)),
                candidate_proof=lambda _clone, _routines: None,
            )
        finally:
            integrate.FACTORY = saved_factory
            integrate.ensure_v2_clone = saved_clone
        _require(phases[-1] == "pushed", "saga did not reach pushed", phases)
        after = int(_git(["git", "rev-list", "--count", "main"], remote))
        _require(after == before + 2, f"remote gained {after - before} commits, expected 2",
                 _git(["git", "log", "--oneline", "-4", "main"], remote))
        remote_head = _git(["git", "rev-parse", "main"], remote)
        _require(remote_head == result.publication_revision,
                 "remote bookmark is not the publication revision",
                 {"remote": remote_head, "publication": result.publication_revision})
        _require(result.routine_names == (FN,), "saga landed the wrong routines",
                 result.routine_names)
        gate_json = json.loads((clone / "site" / "data" / "gate.json").read_text())
        _require(gate_json["commit"] == result.source_revision,
                 "gate record does not name the source revision", gate_json)
        return (f"{len(phases)} phases, source {result.source_revision[:12]}, "
                f"publication {result.publication_revision[:12]}")


CONTRACT_STAGES: tuple[tuple[str, Callable[[dict], str]], ...] = (
    ("packet", stage_packet),
    ("prompt", stage_prompt),
    ("validate", stage_validate),
    ("surgery-roundtrip", stage_surgery_roundtrip),
)

FULL_STAGES: tuple[tuple[str, Callable[[dict], str]], ...] = (
    ("build", stage_build),
    ("verify", stage_verify),
    ("artifact", stage_artifact),
    ("integrate (stub gate, progress, candidate-proof)", stage_integrate),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="also run build, verify, artifact and integrate")
    parser.add_argument("--reply", type=Path,
                        help="replace the recorded reply, to prove the harness fails")
    arguments = parser.parse_args(argv)

    stages = CONTRACT_STAGES + (FULL_STAGES if arguments.full else ())
    state: dict[str, Any] = {}
    artifacts = tempfile.TemporaryDirectory(prefix="factory-smoke-artifacts-")
    workers.V2_ARTIFACTS = Path(artifacts.name)
    override = json.loads(arguments.reply.read_text()) if arguments.reply else None
    try:
        for index, (name, run) in enumerate(stages):
            started = time.monotonic()
            try:
                detail = run(state)
                if name == "packet" and override is not None:
                    override["attempt_id"] = state["packet"]["attempt_id"]
                    state["reply"] = override
            except StageFailure as failure:
                print(f"FACTORY-SMOKE {name} FAIL {failure}")
                if failure.payload is not None:
                    print(json.dumps(failure.payload, indent=2, sort_keys=True, default=str))
                return 10 + index
            except Exception:
                print(f"FACTORY-SMOKE {name} FAIL unhandled exception")
                traceback.print_exc()
                return 10 + index
            print(f"FACTORY-SMOKE {name} ok  {round(time.monotonic() - started, 2)}s  {detail}")
    finally:
        artifacts.cleanup()
    print(f"FACTORY-SMOKE complete {len(stages)} stages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
