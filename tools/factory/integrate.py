#!/usr/bin/env python3
"""Serial integrator: the only process that writes the repo, jj, or GitHub.

Lands green bundles FIFO: transplant each bundle's marked fragments onto the
repo tree (``surgery.extract`` + ``surgery.apply`` — additive, so concurrent
lanes' packets for the same basename compose instead of one overwriting the
other) -> barrier build -> live PyBoy diff, scoped to the packet's own
routines -> ``jj commit`` (one commit per basename).  After each batch:
adapter lint, full GBRT inventory gate, schema audit, progress rebuild, then
``jj git push``.  Any red stops the line before anything is pushed.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import BUNDLES, CACHE, PBENV, ROOT, list_packets, set_state  # noqa: E402
from verify import fn_args  # noqa: E402
import surgery  # noqa: E402


def run(command: list[str], timeout: int = 1800, cwd: Path = ROOT,
        check_message: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True,
                            timeout=timeout, check=False)
    if check_message and result.returncode != 0:
        raise SystemExit(
            f"STOP-THE-LINE {check_message}: {' '.join(command)}\n"
            f"{result.stdout[-3000:]}\n{result.stderr[-2000:]}")
    return result


def contract_keys(path: Path, tag: str) -> set[str]:
    if not path.exists():
        return set()
    import importlib.util
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location(f"contract_{tag}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(getattr(module, "CONTRACT", {}))


def land(packet: dict) -> None:
    bundle = BUNDLES / packet["id"]
    if not bundle.is_dir():
        raise SystemExit(f"bundle missing for {packet['id']}")
    metadata = bundle / "packet.json"
    if not metadata.exists():
        raise SystemExit(f"bundle missing packet identity: {metadata}")
    identity = json.loads(metadata.read_text())
    expected_identity = [
        {
            "name": routine["name"],
            "work_id": routine.get("work_id")
            or f"port:v1:{packet['file']}:{routine['name']}",
            "issue_number": routine.get("issue_number"),
        }
        for routine in packet["routines"]
    ]
    if identity.get("routines") != expected_identity:
        raise SystemExit(f"STOP-THE-LINE {packet['id']} identity mismatch")
    basename = packet["basename"]
    cases_rel = Path("tests") / "cases" / f"{basename}.py"

    before = contract_keys(ROOT / cases_rel, f"repo_{basename}")
    surgery.apply(ROOT, packet, surgery.extract(bundle, packet))
    expected = before | {r["name"] for r in packet["routines"]}
    after = contract_keys(ROOT / cases_rel, f"landed_{basename}")
    if not expected <= after:
        raise SystemExit(
            f"STOP-THE-LINE {packet['id']} lost {sorted(expected - after)} on "
            f"transplant; a concurrent packet's landing must have raced this one")

    for r in packet["routines"]:
        receipt = f"tools/oracle/mutation_receipts/{r['name']}.json"
        source = bundle / receipt
        if not source.exists():
            raise SystemExit(f"bundle missing mutation receipt: {source}")
        dest = ROOT / receipt
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)

    if not (ROOT / "build-barrier" / "build.ninja").exists():
        run(["cmake", "-G", "Ninja", "-B", "build-barrier",
             "-DCMAKE_BUILD_TYPE=Debug", "-DPORT_FILES="],
            check_message="barrier configure failed")
    run(["ninja", "-C", "build-barrier"], check_message="barrier build failed")
    run([str(PBENV), "tests/test_leaves.py",
         *fn_args([r["name"] for r in packet["routines"]]),
         "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
         "--probe", str(ROOT / "build-barrier" / "poketcg_probe")],
        check_message=f"live diff failed for {packet['basename']}")
    run(["jj", "commit", "-m", f"feat(port): {packet['basename']}"],
        check_message="jj commit failed")
    head = run(["jj", "log", "--no-graph", "-r", "@-", "-T", "commit_id"]).stdout.strip()
    main_at = run(["jj", "log", "--no-graph", "-r", "main", "-T", "commit_id"]).stdout.strip()
    if head != main_at:
        run(["jj", "bookmark", "set", "main", "-r", "@-"],
            check_message="main bookmark set failed")
    set_state(packet, "landed")
    print(f"landed {packet['id']} at {head[:12]}")


def assert_fast_forward() -> None:
    """Abort unless local ``main`` is a descendant of ``main@origin``.

    The release bot appends ``chore(release)`` commits to main. A gate run
    takes ~50 s — long enough for one to land after the last fetch — and
    pushing a head that is not a descendant moves the bookmark sideways,
    dropping that release out of main's history (observed: v0.48.0). Re-fetch
    and check here, immediately before the push, where the window is smallest.

    Aborting rather than auto-rebasing is deliberate: reordering commits
    around a published, tagged release is a judgment call, not something a
    batch tool should do unattended.
    """
    run(["jj", "git", "fetch"], check_message="fetch before push failed")
    ahead = run(["jj", "log", "--no-graph", "-r", "main@origin ~ ::main",
                 "-T", 'commit_id.short() ++ "\\n"']).stdout.split()
    if ahead:
        raise SystemExit(
            f"STOP-THE-LINE push aborted: main@origin has {len(ahead)} commit(s) "
            f"absent from local main ({', '.join(ahead[:3])}). Origin advanced — "
            f"almost certainly a release. Rebase local commits onto main@origin, "
            f"re-run the gate, then integrate again. Landed packets stay "
            f"committed locally; nothing is lost.")


def reconcile_issues(enabled: bool = False) -> None:
    """Refresh issue state only with an explicit write opt-in."""
    if not enabled and os.environ.get("POKETCG_ISSUE_SYNC") != "1":
        return
    run([sys.executable, "tools/factory/issues.py", "fetch"],
        check_message="issue fetch failed")
    snapshot = json.loads((ROOT / ".factory" / "issues-cache.json").read_text())
    if not snapshot.get("migration_complete"):
        raise SystemExit(
            "issue migration is incomplete; run the explicit bounded "
            "issues.py migrate --apply workflow first"
        )
    run([sys.executable, "tools/factory/issues.py", "plan", "--json"],
        check_message="issue plan failed")
    plan_path = ROOT / ".factory" / "issues-plan.json"
    plan = json.loads(plan_path.read_text())
    if plan.get("actions"):
        run([
            sys.executable, "tools/factory/issues.py", "apply",
            "--limit", "25", "--batches", "4", "--require-complete",
        ], check_message="issue apply failed")
    run([sys.executable, "tools/factory/issues.py", "verify", "--live"],
        check_message="issue zero-drift verification failed")


def gate_and_push(push: bool, sync_issues: bool = False) -> None:
    run([sys.executable, "tools/lint_adapters.py"],
        check_message="adapter lint failed")
    run([sys.executable, "tools/audit_constants.py"],
        check_message="constant audit failed: a locally #define'd value "
                      "disagrees with pret and is live-used")
    run(["just", "oracle-release-gate"], check_message="release gate failed")
    run([sys.executable, "tools/progress/report.py", "build"],
        check_message="progress rebuild failed")
    reconcile_issues(sync_issues)
    status = run(["jj", "st"]).stdout
    if "gate.json" in status or "progress.json" in status or "history.jsonl" in status:
        run(["jj", "commit", "-m", "chore(progress): refresh gate report"],
            check_message="gate refresh commit failed")
        run(["jj", "bookmark", "set", "main", "-r", "@-"])
    if push:
        assert_fast_forward()
        run(["jj", "git", "push", "--bookmark", "main"], check_message="push failed")
        print("pushed main")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=10,
                        help="gate+push after this many landings")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--sync-issues", action="store_true",
                        help="apply the reviewed managed-issue plan")
    args = parser.parse_args()
    greens = sorted(list_packets(("green",)), key=lambda p: p.get("updated_at", 0))
    if not greens:
        print("nothing green to land")
        return 0
    landed = 0
    for packet in greens:
        land(packet)
        landed += 1
        if landed % args.batch == 0:
            gate_and_push(not args.no_push, args.sync_issues)
    gate_and_push(not args.no_push, args.sync_issues)
    print(f"integrated {landed} packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
