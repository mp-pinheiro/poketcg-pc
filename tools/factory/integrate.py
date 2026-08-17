#!/usr/bin/env python3
"""Journaled publication of verified factory actions."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state
import surgery
from common import (
    BUNDLES,
    CACHE,
    FACTORY,
    ORACLE_PYTHON,
    ROOT,
    packet_identity,
    port_owned_paths,
)
from verify import fn_args

GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}


def run(command: list[str], timeout: int = 1800, cwd: Path = ROOT, check_message: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False, env=GIT_ENV)
    if check_message and result.returncode != 0:
        raise SystemExit(f"STOP-THE-LINE {check_message}: {' '.join(command)}\n{result.stdout[-3000:]}\n{result.stderr[-2000:]}")
    return result


def contract_keys(path: Path, tag: str) -> set[str]:
    if not path.exists():
        return set()
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"contract_{tag}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return set(getattr(module, "CONTRACT", {}))


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()




def _commit(revision: str) -> str:
    return run(["jj", "log", "--no-graph", "-r", revision, "-T", "commit_id"], check_message=f"cannot read {revision}").stdout.strip()

def _base_compatible(packet: dict, main: str) -> bool:
    base = packet.get("base_commit")
    if not base or base == main:
        return True
    ancestor = run(["git", "merge-base", "--is-ancestor", base, main])
    if ancestor.returncode != 0:
        return False
    owned_paths = port_owned_paths(packet["basename"])
    unchanged = run(["git", "diff", "--quiet", base, main, "--", *owned_paths])
    return unchanged.returncode == 0


def _clean_tree() -> None:
    status = run(["jj", "diff", "--summary"])
    if status.returncode != 0 or status.stdout.strip():
        raise SystemExit("STOP-THE-LINE orchestrator working copy is not clean")


def _origin_is_ancestor() -> None:
    run(["jj", "git", "fetch"], check_message="fetch before integration failed")
    ahead = run(["jj", "log", "--no-graph", "-r", "main@origin ~ ::main", "-T", 'commit_id.short() ++ "\\n"']).stdout.split()
    if ahead:
        raise SystemExit("STOP-THE-LINE main is not based on main@origin")


def _validate_batch(packets: list[dict], *, allow_duplicate_basename: bool = False) -> tuple[str, str]:
    if not packets:
        raise SystemExit("no packets supplied")
    ids = [p.get("attempt_id", p.get("id")) for p in packets]
    if len(ids) != len(set(ids)):
        raise SystemExit("STOP-THE-LINE duplicate packet identity")
    work_ids = [r["work_id"] for p in packets for r in p.get("routines", [])]
    if len(work_ids) != len(set(work_ids)):
        raise SystemExit("STOP-THE-LINE duplicate work ID in integration batch")
    basenames = [p["basename"] for p in packets]
    if not allow_duplicate_basename and len(basenames) != len(set(basenames)):
        raise SystemExit("STOP-THE-LINE duplicate basename requires explicit group")
    main = _commit("main")
    if main != _commit("main@origin"):
        raise SystemExit("STOP-THE-LINE local main diverges from main@origin")
    for packet in packets:
        if packet.get("state") != "green":
            raise SystemExit(f"packet {packet.get('id')} is not green")
        if not _base_compatible(packet, main):
            raise SystemExit(f"STOP-THE-LINE {packet['id']} base commit mismatch")
        bundle = BUNDLES / packet.get("attempt_id", packet["id"])
        metadata = bundle / "packet.json"
        if not bundle.is_dir() or not metadata.exists():
            raise SystemExit(f"bundle missing for {packet.get('id')}")
        if json.loads(metadata.read_text()) != packet_identity(packet):
            raise SystemExit(f"STOP-THE-LINE {packet['id']} identity mismatch")
        surgery.extract(bundle, packet)
    return main, _digest(ids)


def _apply_packet(packet: dict) -> None:
    bundle = BUNDLES / packet.get("attempt_id", packet["id"])
    basename = packet["basename"]
    cases_rel = Path("tests") / "cases" / f"{basename}.py"
    before = contract_keys(ROOT / cases_rel, f"candidate_before_{basename}")
    surgery.apply(ROOT, packet, surgery.extract(bundle, packet))
    after = contract_keys(ROOT / cases_rel, f"candidate_after_{basename}")
    expected = before | {r["name"] for r in packet["routines"]}
    if not expected <= after:
        raise SystemExit(f"STOP-THE-LINE {packet['id']} lost contract keys")
    for routine in packet["routines"]:
        source = bundle / "tools/oracle/mutation_receipts" / f"{routine['name']}.json"
        if not source.exists():
            raise SystemExit(f"bundle missing mutation receipt: {source}")
        destination = ROOT / source.relative_to(bundle)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

def _candidate_checks(packets: list[dict]) -> None:
    """Run the batch-local build and live proofs before committing the candidate."""
    if not (ROOT / "build-barrier" / "build.ninja").exists():
        run(["cmake", "-G", "Ninja", "-B", "build-barrier",
             "-DCMAKE_BUILD_TYPE=Debug", "-DPORT_FILES="],
            check_message="barrier configure failed")
    run(["ninja", "-C", "build-barrier"], check_message="barrier build failed")
    names = [routine["name"] for packet in packets
             for routine in packet["routines"]]
    run([*ORACLE_PYTHON, "tests/test_leaves.py", *fn_args(names),
         "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
         "--probe", str(ROOT / "build-barrier" / "poketcg_probe")],
        check_message="candidate live proof failed")


def _gate() -> None:
    run([sys.executable, "tools/lint_adapters.py"], check_message="adapter lint failed")
    run([sys.executable, "tools/audit_constants.py"], check_message="constant audit failed")
    run(["just", "oracle-release-gate"], check_message="release gate failed")
    run([sys.executable, "tools/progress/report.py", "build"], check_message="progress rebuild failed")


def _action_packets(
    connection, action_id: str, *, allow_empty: bool = False,
) -> list[dict]:
    packets = []
    for attempt_id, attempt_state in connection.execute(
        """SELECT a.attempt_id, a.state
           FROM action_attempt aa
           JOIN attempt a ON a.attempt_id = aa.attempt_id
           WHERE aa.action_id = ? ORDER BY a.attempt_id""",
        (action_id,),
    ):
        if attempt_state not in {"green", "integrating"}:
            raise SystemExit(
                f"STOP-THE-LINE integration attempt {attempt_id} is {attempt_state}"
            )
        manifest = BUNDLES / attempt_id / "packet.json"
        if not manifest.is_file():
            raise SystemExit(f"STOP-THE-LINE bundle missing for {attempt_id}")
        packet = json.loads(manifest.read_text())
        packet["state"] = "green"
        packets.append(packet)
    if not packets and not allow_empty:
        raise SystemExit("STOP-THE-LINE integration action has no attempts")
    return packets


def _bundle_paths(packets: list[dict]) -> list[str]:
    paths = set()
    for packet in packets:
        bundle = BUNDLES / packet["attempt_id"]
        paths.update(
            path.relative_to(bundle).as_posix()
            for path in bundle.rglob("*")
            if path.is_file() and path.name != "packet.json"
        )
    return sorted(paths)


def _dirty_paths() -> set[str]:
    result = run(["jj", "diff", "--summary"], check_message="cannot inspect candidate")
    paths = set()
    for line in result.stdout.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            paths.add(parts[1])
    return paths


def _recover_prepared_candidate(action_id: str, baseline: str, allowed: list[str]) -> None:
    dirty = _dirty_paths()
    if not dirty:
        return
    unexpected = dirty - set(allowed)
    if unexpected:
        raise SystemExit(
            "STOP-THE-LINE prepared candidate contains unknown dirty paths: "
            + ", ".join(sorted(unexpected))
        )
    backup = FACTORY / "recovery" / action_id
    backup.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for relative in sorted(dirty):
        source = ROOT / relative
        if source.is_file():
            destination = backup / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            manifest[relative] = hashlib.sha256(source.read_bytes()).hexdigest()
    (backup / "manifest.json").write_text(
        json.dumps({"baseline": baseline, "files": manifest}, sort_keys=True, indent=2)
        + "\n"
    )
    run(
        ["jj", "restore", "--from", "main", *sorted(dirty)],
        check_message="cannot restore interrupted prepared candidate",
    )
    if _dirty_paths():
        raise SystemExit("STOP-THE-LINE prepared candidate restore did not clean tree")


def _hash_file(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"STOP-THE-LINE expected generated file missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integrate_leased_action(
    connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    push: bool = True,
) -> dict:
    """Replay one leased integration action through its durable publication phases."""
    kind_row = connection.execute(
        "SELECT kind FROM action WHERE action_id = ?", (action_id,),
    ).fetchone()
    if kind_row is None:
        raise KeyError(action_id)
    gate_refresh = kind_row[0] == "gate-refresh"
    packets = _action_packets(connection, action_id, allow_empty=gate_refresh)
    try:
        journal = state.integration_status(connection, action_id)
    except KeyError:
        _clean_tree()
        _origin_is_ancestor()
        baseline = _commit("main")
        if packets:
            baseline, _digest_value = _validate_batch(packets)
        journal = state.prepare_integration(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, baseline_revision=baseline,
            now=int(time.time()),
        )
    baseline = journal["baseline_revision"]
    if journal["phase"] == "finalized":
        return journal
    if _commit("main") != baseline:
        raise SystemExit("STOP-THE-LINE integration baseline moved during replay")
    allowed_paths = _bundle_paths(packets)
    while journal["phase"] != "finalized":
        state.heartbeat_action(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, lease_seconds=7200, now=int(time.time()),
        )
        phase = journal["phase"]
        if phase == "prepared":
            _recover_prepared_candidate(action_id, baseline, allowed_paths)
            for packet in packets:
                _apply_packet(packet)
            if packets:
                _candidate_checks(packets)
            candidate_tree = run(
                ["jj", "log", "--no-graph", "-r", "@", "-T", "tree_id"],
                check_message="cannot read candidate tree",
            ).stdout.strip()
            journal = state.advance_integration(
                connection, action_id, lease_owner=lease_owner,
                lease_token=lease_token, expected_phase="prepared",
                values={"candidate_tree": candidate_tree}, now=int(time.time()),
            )
            continue
        if phase == "applied":
            if _dirty_paths():
                run(
                    ["jj", "commit", "-m", "feat(port): integrate factory batch"],
                    check_message="candidate source commit failed",
                )
            candidate_commit = _commit("@")
            journal = state.advance_integration(
                connection, action_id, lease_owner=lease_owner,
                lease_token=lease_token, expected_phase="applied",
                values={"candidate_commit": candidate_commit}, now=int(time.time()),
            )
            continue
        if phase == "source-committed":
            _gate()
            journal = state.advance_integration(
                connection, action_id, lease_owner=lease_owner,
                lease_token=lease_token, expected_phase="source-committed",
                values={"gate_hash": _hash_file(ROOT / "site/data/gate.json")},
                now=int(time.time()),
            )
            continue
        if phase == "gate-passed":
            status = run(["jj", "st"], check_message="cannot inspect progress output").stdout
            generated = [
                "site/data/gate.json", "site/data/progress.json",
                "site/data/history.jsonl", ".factory/blocked.toml",
            ]
            if any(path in status for path in generated):
                run(
                    ["jj", "commit", *generated,
                     "-m", "chore(progress): refresh gate report"],
                    check_message="progress commit failed",
                )
            candidate_commit = _commit("@")
            journal = state.advance_integration(
                connection, action_id, lease_owner=lease_owner,
                lease_token=lease_token, expected_phase="gate-passed",
                values={
                    "candidate_commit": candidate_commit,
                    "progress_hash": _hash_file(ROOT / "site/data/progress.json"),
                },
                now=int(time.time()),
            )
            continue
        if phase == "progress-committed":
            if push:
                _origin_is_ancestor()
            run(
                ["jj", "bookmark", "set", "main", "-r", "@"],
                check_message="main bookmark advance failed",
            )
            if push:
                run(
                    ["jj", "git", "push", "--bookmark", "main"],
                    check_message="push failed",
                )
            remote = _commit("main@origin") if push else _commit("main")
            journal = state.advance_integration(
                connection, action_id, lease_owner=lease_owner,
                lease_token=lease_token, expected_phase="progress-committed",
                values={"remote_revision": remote}, now=int(time.time()),
            )
            continue
        if phase == "pushed":
            result = state.finalize_integration(
                connection, action_id, lease_owner=lease_owner,
                lease_token=lease_token,
                remote_revision=journal["remote_revision"], now=int(time.time()),
            )
            return {**journal, "phase": "finalized", "result": result}
        raise SystemExit(f"STOP-THE-LINE unknown integration phase {phase!r}")
    return journal




