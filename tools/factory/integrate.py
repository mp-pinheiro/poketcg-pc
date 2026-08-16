#!/usr/bin/env python3
"""Journaled two-phase integration of verified factory bundles."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import BUNDLES, CACHE, FACTORY, ORACLE_PYTHON, ROOT, list_packets, packet_identity, set_state
from verify import fn_args
import surgery

GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
JOURNAL = FACTORY / "integration.json"
PHASES = ("prepared", "applied", "source-committed", "gate-failed", "gate-passed", "progress-committed", "pushed", "finalized")


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


def _read_journal() -> dict | None:
    if not JOURNAL.exists():
        return None
    try:
        journal = json.loads(JOURNAL.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"STOP-THE-LINE corrupt integration journal: {exc}")
    if journal.get("schema") != 1 or journal.get("phase") not in PHASES:
        raise SystemExit("STOP-THE-LINE invalid integration journal")
    return journal


def _write_journal(journal: dict) -> None:
    FACTORY.mkdir(parents=True, exist_ok=True)
    temporary = JOURNAL.with_suffix(".tmp")
    temporary.write_text(json.dumps(journal, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, JOURNAL)


def _commit(revision: str) -> str:
    return run(["jj", "log", "--no-graph", "-r", revision, "-T", "commit_id"], check_message=f"cannot read {revision}").stdout.strip()


def _clean_tree() -> None:
    status = run(["jj", "st"])
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
        if packet.get("base_commit") and packet["base_commit"] != main:
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


def integrate(packets: list[dict], *, push: bool = True,
              group: bool = False) -> dict:
    """Run or replay one explicit packet or dependency-group transaction."""
    ids = [p.get("attempt_id", p.get("id")) for p in packets]
    existing = _read_journal()
    if existing:
        if existing.get("packet_ids") != ids:
            raise SystemExit("STOP-THE-LINE unresolved integration journal identity mismatch")
        journal = existing
        if journal["phase"] == "finalized":
            return journal
        baseline = journal["base_commit"]
    else:
        _clean_tree()
        _origin_is_ancestor()
        baseline, digest = _validate_batch(
            packets, allow_duplicate_basename=group)
        journal = {
            "schema": 1,
            "transaction_id": _digest(ids + [time.time_ns()]),
            "phase": "prepared",
            "packet_ids": ids,
            "base_commit": baseline,
            "candidate_commit": None,
            "batch_digest": digest,
            "started_at": int(time.time()),
            "push": push,
            "group": group,
            "error": None,
        }
        _write_journal(journal)
    if journal["phase"] == "gate-failed":
        raise SystemExit("STOP-THE-LINE candidate gate previously failed; repair candidate")
    if journal.get("batch_digest") != _digest(ids):
        raise SystemExit("STOP-THE-LINE integration journal batch hash mismatch")
    if journal["phase"] in {"source-committed", "gate-passed",
                            "progress-committed", "pushed"}:
        if _commit("@") != journal.get("candidate_commit"):
            raise SystemExit("STOP-THE-LINE candidate commit hash mismatch")
    try:
        if journal["phase"] == "prepared":
            if _commit("main") != baseline:
                raise SystemExit("STOP-THE-LINE baseline changed during replay")
            for packet in packets:
                _apply_packet(packet)
            _candidate_checks(packets)
            journal["phase"] = "applied"
            _write_journal(journal)
        if journal["phase"] == "applied":
            run(["jj", "commit", "-m", "feat(port): integrate factory batch"], check_message="candidate source commit failed")
            journal["candidate_commit"] = _commit("@")
            journal["phase"] = "source-committed"
            _write_journal(journal)
        if journal["phase"] == "source-committed":
            try:
                _gate()
            except SystemExit as exc:
                journal["phase"] = "gate-failed"
                journal["error"] = str(exc)
                _write_journal(journal)
                for packet in packets:
                    set_state(packet, "repair", str(exc))
                raise
            journal["phase"] = "gate-passed"
            _write_journal(journal)
        if journal["phase"] == "gate-passed":
            status = run(["jj", "st"]).stdout
            if any(name in status for name in ("gate.json", "progress.json", "history.jsonl")):
                run(["jj", "commit", "site/data/gate.json", "site/data/progress.json", "site/data/history.jsonl", ".factory/blocked.toml", "-m", "chore(progress): refresh gate report"], check_message="progress commit failed")
            journal["candidate_commit"] = _commit("@")
            journal["phase"] = "progress-committed"
            _write_journal(journal)
        if journal["phase"] == "progress-committed":
            if push:
                _origin_is_ancestor()
                run(["jj", "bookmark", "set", "main", "-r", "@"], check_message="main bookmark advance failed")
                run(["jj", "git", "push", "--bookmark", "main"], check_message="push failed")
            else:
                run(["jj", "bookmark", "set", "main", "-r", "@"], check_message="main bookmark advance failed")
            journal["phase"] = "pushed"
            _write_journal(journal)
        if journal["phase"] == "pushed":
            for packet in packets:
                set_state(packet, "landed")
            journal["phase"] = "finalized"
            _write_journal(journal)
        return journal
    except Exception:
        raise


def land(packet: dict) -> None:
    integrate([packet], push=False)


def gate_and_push(push: bool) -> None:
    _gate()
    if push:
        _origin_is_ancestor()
        run(["jj", "git", "push", "--bookmark", "main"], check_message="push failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=10)
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--packet", action="append", dest="packet_ids")
    parser.add_argument("--group", action="append", dest="group_ids")
    args = parser.parse_args()
    selected = set(args.packet_ids or []) | set(args.group_ids or [])
    greens = sorted(list_packets(("green",)), key=lambda p: p.get("updated_at", 0))
    if selected:
        greens = [p for p in greens if p.get("id") in selected or p.get("attempt_id") in selected]
    if not greens:
        print("nothing green to land")
        return 0
    result = integrate(greens[:args.batch], push=not args.no_push,
                       group=bool(args.group_ids))
    print(f"integration {result['phase']} {len(result['packet_ids'])} packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
