#!/usr/bin/env python3
"""Red/green rehearsal of the real port pipeline on a landed routine.

Every stage calls the production module it is named after, so a contract drift
between prompt, reply validation, surgery, verification, artifact staging, and
the landing driver fails here instead of consuming a live attempt. The
contract tier is offline and compiler-free; the full tier adds the lane build,
the oracle, and a throwaway git remote.

The fixture routine is `_PauseSong`: two cases, one call, already landed and
gate-passing, so any red is a harness defect rather than a port defect.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
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
import lanes
import packet as packet_mod
import prompt as prompt_mod
import surgery
import try_one
import land
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


def _fixture_rows(limit: int) -> list[dict[str, Any]]:
    report = packet_mod.report_module()
    records = report.compute(
        report.load_inventory(),
        report.load_routines()[0],
        report.load_gate(),
    )["work_records"]
    rows = [
        row for row in records
        if row["state"] == "ready"
        and not row.get("operational_blocker")
        and try_one._case_classification(row["name"], row.get("source"))
        == "legacy-appendable"
    ]
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        stem = Path(row["source"]).stem
        if stem in seen:
            continue
        seen.add(stem)
        selected.append(row)
        if len(selected) == limit:
            break
    _require(len(selected) >= limit, f"need {limit} appendable ready fixture rows",
             [row["name"] for row in rows])
    return selected


def _patch_report(rows: list[dict[str, Any]]) -> tuple[Any, Any]:
    report = packet_mod.report_module()
    previous = report.compute
    report.compute = lambda *_args, **_kwargs: {"work_records": rows}
    return report, previous


def _restore_report(report: Any, previous: Any) -> None:
    report.compute = previous


def _capture(run: Callable[[], Any]) -> tuple[Any, str]:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        result = run()
    return result, output.getvalue()


def stage_immutable_pending(state: dict[str, Any]) -> str:
    row = _fixture_rows(1)[0]
    with tempfile.TemporaryDirectory(prefix="factory-smoke-attempts-") as directory:
        previous_root = try_one.TRY_ROOT
        try_one.TRY_ROOT = Path(directory)
        issued = try_one.issue_attempt(row["name"], 0)
        attempt_id = issued["current"]["attempt_id"]
        report, previous = _patch_report([row])
        previous_scores = try_one._score_rows
        try_one._score_rows = lambda _rows, retry: [(1, row)]
        try:
            result, output = _capture(lambda: try_one.subcommand_next(1, False, 1))
            current_id = try_one._read_current(row["name"])[ "attempt_id"]
            _require(
                not list(issued["run_dir"].glob("candidate-*.json"))
                and not (issued["run_dir"] / "result.json").exists(),
                "pending selection wrote candidate or result artifacts",
            )
        finally:
            _restore_report(report, previous)
            try_one._score_rows = previous_scores
            try_one.TRY_ROOT = previous_root
        _require(result == 3 and "status=active" in output,
                 "pending factory-next did not stop as active", output)
        _require(current_id == attempt_id,
                 "pending factory-next rotated the issued attempt")
    return f"attempt {attempt_id} remained issued"


def stage_unrelated_rebase(state: dict[str, Any]) -> str:
    row = _fixture_rows(1)[0]
    with tempfile.TemporaryDirectory(prefix="factory-smoke-rebase-") as directory:
        previous_root = try_one.TRY_ROOT
        previous_resolve = try_one.resolve
        try_one.TRY_ROOT = Path(directory)
        issued = try_one.issue_attempt(row["name"], 0)
        candidate = issued["run_dir"] / "candidate-0.json"
        try_one._write_json(
            candidate, {"attempt_id": issued["current"]["attempt_id"]}
        )

        def unrelated(fn: str) -> tuple[dict[str, Any], dict[str, Any]]:
            routine, packet = previous_resolve(fn)
            packet["base_commit"] = "unrelated-landing"
            return routine, packet

        try_one.resolve = unrelated
        rebased = try_one.verification_packet(issued)
        try_one.resolve = previous_resolve
        try_one.TRY_ROOT = previous_root
        _require(rebased is not None, "unrelated landing invalidated the attempt")
        _require(rebased["attempt_id"] == issued["current"]["attempt_id"],
                 "unrelated landing changed attempt identity")
        _require(rebased["base_commit"] == "unrelated-landing",
                 "artifact verification packet did not rebase", rebased)
        _require(
            json.loads(candidate.read_text())["attempt_id"]
            == issued["current"]["attempt_id"],
            "unrelated landing invalidated the pending candidate",
        )
    return f"attempt {issued['current']['attempt_id']} rebased"


def stage_same_owner_stale(state: dict[str, Any]) -> str:
    row = _fixture_rows(1)[0]
    with tempfile.TemporaryDirectory(prefix="factory-smoke-stale-") as directory:
        previous_root = try_one.TRY_ROOT
        previous_resolve = try_one.resolve
        current_id = replacement_id = ""
        try:
            try_one.TRY_ROOT = Path(directory)
            issued = try_one.issue_attempt(row["name"], 0)

            def owned_change(fn: str) -> tuple[dict[str, Any], dict[str, Any]]:
                routine, packet = previous_resolve(fn)
                packet["routines"][0]["asm"] += "\nowned change"
                return routine, packet

            try_one.resolve = owned_change
            stale = try_one.verification_packet(issued)
            _require(stale is None, "same-owner translation change stayed valid")
            current = try_one._read_current(row["name"])
            current_id = current["attempt_id"]
            _require(current["state"] == "stale", "stale attempt state was not recorded")
            replacement = try_one.issue_attempt(
                row["name"],
                current["generation"] + 1,
                parent_attempt_id=current["attempt_id"],
            )
            replacement_id = replacement["current"]["attempt_id"]
            _require(replacement["current"]["attempt_id"] != current["attempt_id"],
                     "stale attempt was not reissued")
        finally:
            try_one.resolve = previous_resolve
            try_one.TRY_ROOT = previous_root
    return f"{current_id} stale, {replacement_id} reissued"
def stage_owned_path_quarantine(state: dict[str, Any]) -> str:
    with tempfile.TemporaryDirectory(prefix="factory-smoke-owned-path-") as directory:
        root = Path(directory)
        artifact_sha = "a" * 64
        bundle = root / "bundle"
        bundle.mkdir()
        previous_members = land._artifact_members
        previous_bundle_paths = land._bundle_paths
        previous_revision = land._revision
        previous_run = land._run
        try:
            land._artifact_members = lambda _sha: [bundle]
            land._bundle_paths = lambda _bundle: (
                {
                    "basename": "fixture",
                    "base_commit": "base",
                    "routines": [{"name": "Fixture"}],
                },
                ["src/home/fixture.c"],
            )
            land._revision = lambda _root, revision: revision
            land._run = lambda command, cwd, timeout: subprocess.CompletedProcess(
                command, 0, "src/home/fixture.c\n", ""
            )
            compatible, quarantined = land._stale_owned_artifacts(
                root, [artifact_sha], "main"
            )
        finally:
            land._artifact_members = previous_members
            land._bundle_paths = previous_bundle_paths
            land._revision = previous_revision
            land._run = previous_run
        _require(not compatible, "same-owner artifact remained compatible")
        _require(
            len(quarantined) == 1
            and quarantined[0]["failure_class"] == "stale-owned-path"
            and quarantined[0]["changed_paths"] == ["src/home/fixture.c"],
            "same-owner artifact was not quarantined with changed paths",
            quarantined,
        )
    return "same-owner artifact quarantined"




def stage_stale_candidates(state: dict[str, Any]) -> str:
    row = _fixture_rows(1)[0]
    with tempfile.TemporaryDirectory(prefix="factory-smoke-candidates-") as directory:
        previous_root = try_one.TRY_ROOT
        try:
            try_one.TRY_ROOT = Path(directory)
            issued = try_one.issue_attempt(row["name"], 0)
            flat = try_one.TRY_ROOT / row["name"] / "candidate-99.json"
            try_one._write_json(flat, {"attempt_id": "flat-prior-attempt"})
            active = (
                try_one.TRY_ROOT / row["name"] / "attempts"
                / issued["current"]["attempt_id"]
            )
            try_one._write_json(
                active / "candidate-0.json",
                {"attempt_id": "prior-attempt"},
            )
            result, output = _capture(
                lambda: try_one.main(["--fn", row["name"], "--candidates", "1"])
            )
            _require(result == 3 and "stale candidate ignored" in output,
                     "stale candidate was not ignored", output)
            _require(not (active / "result.json").exists(),
                     "stale candidate created a result")
            _require(
                json.loads(flat.read_text()) == {"attempt_id": "flat-prior-attempt"},
                "flat legacy candidate was consumed or rewritten",
            )
        finally:
            try_one.TRY_ROOT = previous_root
    return "active-attempt stale candidate ignored"


def stage_appendability_classifier(state: dict[str, Any]) -> str:
    with tempfile.TemporaryDirectory(prefix="factory-smoke-cases-") as directory:
        root = Path(directory)
        compact = root / "compact.py"
        compact.write_text(
            "CASES={}; CONTRACT={}" + chr(10)
            + "SCHEMA2_CASES=legacy_to_schema(CASES,CONTRACT)" + chr(10)
        )
        native = root / "native.py"
        native.write_text("SCHEMA2_CASES = {'Fn': []}" + chr(10))
        _require(common.classify_case_module(root / "missing.py") == "new",
                 "missing case module was not classified new")
        _require(common.classify_case_module(compact) == "legacy-appendable",
                 "compact legacy case module was rejected")
        _require(
            surgery._legacy_tail_at(compact.read_text(), compact) >= 0,
            "surgery rejected compact legacy appendability",
        )
        _require(common.classify_case_module(native) == "native-migration-required",
                 "native case module was accepted")
    return "new, compact legacy, and native classifications correct"


def stage_native_preflight(state: dict[str, Any]) -> str:
    append_row = _fixture_rows(1)[0]
    report = packet_mod.report_module()
    records = report.compute(
        report.load_inventory(),
        report.load_routines()[0],
        report.load_gate(),
    )["work_records"]
    native_candidates = [
        row for row in records
        if try_one._case_classification(row["name"], row.get("source"))
        == "native-migration-required"
    ]
    _require(native_candidates, "no native schema fixture exists")
    native_row = dict(native_candidates[0])
    native_row["state"] = "ready"
    native_row["operational_blocker"] = None
    rows = [native_row, append_row]
    with tempfile.TemporaryDirectory(prefix="factory-smoke-preflight-") as directory:
        previous_root = try_one.TRY_ROOT
        previous_scores = try_one._score_rows
        previous_issue = try_one.issue_attempt
        try_one.TRY_ROOT = Path(directory)
        report, previous_report = _patch_report(rows)
        try_one._score_rows = lambda _rows, retry: [
            (100, native_row), (1, append_row)
        ]

        def fake_issue(fn: str, generation: int, *,
                       parent_attempt_id: str | None = None) -> dict[str, Any]:
            return {
                "current": {"attempt_id": f"smoke-{fn}"},
                "packet": {},
                "routine": {},
                "run_dir": Path(directory),
            }

        try_one.issue_attempt = fake_issue
        try:
            result, output = _capture(lambda: try_one.subcommand_next(1, False, 1))
        finally:
            _restore_report(report, previous_report)
            try_one._score_rows = previous_scores
            try_one.issue_attempt = previous_issue
            try_one.TRY_ROOT = previous_root
        _require(result == 0 and "phase=preflight detail=native-migration-required" in output,
                 "native preflight did not block", output)
        _require(f"NEXT {append_row['name']} " in output,
                 "selection did not backfill after native preflight", output)
    return f"{native_row['name']} blocked, {append_row['name']} backfilled"


def stage_evidence_filter(state: dict[str, Any]) -> str:
    calls: list[list[str]] = []
    previous_run = verify.run

    def fake_run(command: list[str], _cwd: Path, timeout: float = 600,
                 deadline: float | None = None) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, "", "")

    verify.run = fake_run
    try:
        result = verify.primary_compare(
            Path("/tmp/factory-smoke-lane"),
            "mixed",
            ["Mixed"],
            {"Mixed": 3},
            {"Mixed": [0, 2]},
            {"Mixed": [0]},
            None,
        )
        _require(result is None, "mixed evidence comparison failed", result)
        indices = [int(command[command.index("--index") + 1]) for command in calls]
        _require(indices == [0, 2], "non-primary evidence reached GBRT", indices)
        unsupported = verify.primary_compare(
            Path("/tmp/factory-smoke-lane"),
            "none",
            ["None"],
            {"None": 1},
            {"None": []},
            {"None": []},
            None,
        )
    finally:
        verify.run = previous_run
    _require(
        unsupported and unsupported["failure_class"] == "unsupported-evidence"
        and unsupported["detail"] == "no primary oracle case",
        "no-primary evidence was not operationally blocked",
        unsupported,
    )
    try:
        try_one.resolve("_TossCoin")
    except try_one.OperationalBlocker:
        pass
    else:
        raise StageFailure("_TossCoin was not excluded by blocked.toml")
    return "GBRT saw primary indices 0,2; no-primary was blocked"


def stage_retry_fairness(state: dict[str, Any]) -> str:
    rows = _fixture_rows(3)
    with tempfile.TemporaryDirectory(prefix="factory-smoke-retry-") as directory:
        previous_root = try_one.TRY_ROOT
        previous_issue = try_one.issue_attempt
        previous_scores = try_one._score_rows
        try_one.TRY_ROOT = Path(directory)
        for index, row in enumerate(rows):
            try_one._store_current({
                "schema": common.SCHEMA,
                "fn": row["name"],
                "attempt_id": f"red-{index}",
                "generation": 0,
                "context_sha256": "fixture",
                "base_commit": "fixture",
                "state": "red",
            })
        report, previous_report = _patch_report(rows)
        try_one._score_rows = lambda selected_rows, retry: [
            (index, row) for index, row in enumerate(selected_rows)
        ]
        selected: list[tuple[str, int]] = []

        def fake_issue(fn: str, generation: int, *, parent_attempt_id: str | None = None) -> dict[str, Any]:
            selected.append((fn, generation))
            current = try_one._read_current(fn)
            current["attempt_id"] = f"retry-{fn}"
            current["generation"] = generation
            try_one._store_current(current)
            return {"current": current, "packet": {}, "routine": {}, "run_dir": Path(directory)}

        try_one.issue_attempt = fake_issue
        try:
            first, first_output = _capture(lambda: try_one.subcommand_next(3, True, 1))
            second, second_output = _capture(lambda: try_one.subcommand_next(3, True, 1))
        finally:
            _restore_report(report, previous_report)
            try_one._score_rows = previous_scores
            try_one.issue_attempt = previous_issue
            try_one.TRY_ROOT = previous_root
        _require(first == 0 and len(selected) == 3
                 and all(generation == 1 for _fn, generation in selected),
                 "retry generation did not rotate every red once",
                 {"selected": selected, "output": first_output})
        _require(second == 4 and "status=stalled" in second_output
                 and "exhausted=3" in second_output,
                 "retry exhaustion did not stop at stalled", second_output)
    return f"rotated {len(selected)} reds before stalled"


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


def stage_land(state: dict[str, Any]) -> str:
    with tempfile.TemporaryDirectory(prefix="factory-smoke-remote-",
                                     ignore_cleanup_errors=True) as directory:
        root = Path(directory)
        remote = root / "remote.git"
        clone = root / "clone"
        _git(["git", "clone", "--bare", str(common.ROOT), str(remote)], root)
        before = int(_git(["git", "rev-list", "--count", "main"], remote))
        _git(["jj", "git", "clone", "--colocate", str(remote), str(clone)], root)
        _git(["jj", "config", "set", "--repo",
              "experimental-advance-branches.enabled-branches", '["main"]'], clone)
        gate, progress = _stub_scripts(root)
        completed = subprocess.run(
            [sys.executable, str(common.ROOT / "tools" / "factory" / "land.py"),
             "--root", str(clone),
             "--artifact", state["artifact_sha256"],
             "--gate-command", sys.executable, "--gate-command", str(gate),
             "--progress-command", sys.executable, "--progress-command", str(progress)],
            cwd=clone, capture_output=True, text=True, check=False,
            env={**os.environ, "FACTORY_ARTIFACTS": str(workers.V2_ARTIFACTS)},
        )
        output = completed.stdout + completed.stderr
        _require(completed.returncode == 0, "land.py failed", output[-3000:])
        _require("LAND done landed=1 quarantined=0" in completed.stdout,
                 "land.py did not report one landing", output[-3000:])
        landing_log = clone / ".factory" / "landings.jsonl"
        _require(landing_log.is_file(), "landing log was not written under the clone root")
        landings = landing_log.read_text().splitlines()
        _require(len(landings) == 1, "expected exactly one landing record", landings)
        record = json.loads(landings[-1])
        after = int(_git(["git", "rev-list", "--count", "main"], remote))
        _require(after == before + 2, f"remote gained {after - before} commits, expected 2",
                 _git(["git", "log", "--oneline", "-4", "main"], remote))
        remote_head = _git(["git", "rev-parse", "main"], remote)
        _require(remote_head == record["publication_revision"],
                 "remote bookmark is not the publication revision",
                 {"remote": remote_head, "publication": record["publication_revision"]})
        _require(record["routines"] == [FN], "landing recorded the wrong routines",
                 record["routines"])
        gate_json = json.loads((clone / "site" / "data" / "gate.json").read_text())
        _require(gate_json["commit"] == record["source_revision"],
                 "gate record does not name the source revision", gate_json)
        return (f"source {record['source_revision'][:12]}, "
                f"publication {record['publication_revision'][:12]}")


CONTRACT_STAGES: tuple[tuple[str, Callable[[dict], str]], ...] = (
    ("immutable-pending", stage_immutable_pending),
    ("unrelated-rebase", stage_unrelated_rebase),
    ("same-owner-stale", stage_same_owner_stale),
    ("owned-path-quarantine", stage_owned_path_quarantine),
    ("stale-candidates", stage_stale_candidates),
    ("appendability-classifier", stage_appendability_classifier),
    ("native-preflight", stage_native_preflight),
    ("evidence-filter", stage_evidence_filter),
    ("retry-fairness", stage_retry_fairness),
    ("packet", stage_packet),
    ("prompt", stage_prompt),
    ("validate", stage_validate),
    ("surgery-roundtrip", stage_surgery_roundtrip),
)

FULL_STAGES: tuple[tuple[str, Callable[[dict], str]], ...] = (
    ("build", stage_build),
    ("verify", stage_verify),
    ("artifact", stage_artifact),
    ("land (stub gate, progress)", stage_land),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="also run build, verify, artifact and land")
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
