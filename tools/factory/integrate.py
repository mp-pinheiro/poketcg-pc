#!/usr/bin/env python3
"""Serial integrator: the only process that writes the repo, jj, or GitHub.

Lands green bundles FIFO: copy files -> barrier build -> live PyBoy group
diff -> progress -> ``jj commit`` (one commit per basename).  After each
batch: adapter lint, full GBRT inventory gate, schema audits, then
``jj git push``.  Any red stops the line before anything is pushed.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import BUNDLES, CACHE, PBENV, ROOT, list_packets, set_state  # noqa: E402


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
    basename = packet["basename"]
    cases_rel = Path("tests") / "cases" / f"{basename}.py"
    lost = (contract_keys(ROOT / cases_rel, f"repo_{basename}")
            - contract_keys(bundle / cases_rel, f"bundle_{basename}"))
    if lost:
        raise SystemExit(
            f"STOP-THE-LINE {packet['id']} would unregister {sorted(lost)}; "
            f"its lane predates those routines — rebuild the packet from the "
            f"current tip")
    for source in sorted(bundle.rglob("*")):
        if source.is_file():
            dest = ROOT / source.relative_to(bundle)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)

    if not (ROOT / "build-barrier" / "build.ninja").exists():
        run(["cmake", "-G", "Ninja", "-B", "build-barrier",
             "-DCMAKE_BUILD_TYPE=Debug", "-DPORT_FILES="],
            check_message="barrier configure failed")
    run(["ninja", "-C", "build-barrier"], check_message="barrier build failed")
    run([str(PBENV), "tests/test_leaves.py", "--group", packet["basename"],
         "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
         "--probe", str(ROOT / "build-barrier" / "poketcg_probe")],
        check_message=f"live diff failed for {packet['basename']}")
    run([sys.executable, "tools/progress/report.py", "build"],
        check_message="progress rebuild failed")
    run(["jj", "commit", "-m", f"feat(port): {packet['basename']}"],
        check_message="jj commit failed")
    head = run(["jj", "log", "--no-graph", "-r", "@-", "-T", "commit_id"]).stdout.strip()
    main_at = run(["jj", "log", "--no-graph", "-r", "main", "-T", "commit_id"]).stdout.strip()
    if head != main_at:
        run(["jj", "bookmark", "set", "main", "-r", "@-"],
            check_message="main bookmark set failed")
    set_state(packet, "landed")
    print(f"landed {packet['id']} at {head[:12]}")


def gate_and_push(push: bool) -> None:
    run([sys.executable, "tools/lint_adapters.py"], check_message="adapter lint failed")
    run(["just", "oracle-fn-all"], check_message="GBRT inventory gate failed")
    run([sys.executable, "tools/audit_oracle_cases.py", "--stage", "routine"],
        check_message="schema audit failed")
    run([sys.executable, "tools/progress/report.py", "build"],
        check_message="progress rebuild failed")
    status = run(["jj", "st"]).stdout
    if "gate.json" in status or "progress.json" in status or "history.jsonl" in status:
        run(["jj", "commit", "-m", "chore(progress): refresh gate report"],
            check_message="gate refresh commit failed")
        run(["jj", "bookmark", "set", "main", "-r", "@-"])
    if push:
        run(["jj", "git", "push"], check_message="push failed")
        print("pushed main")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=10,
                        help="gate+push after this many landings")
    parser.add_argument("--no-push", action="store_true")
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
            gate_and_push(not args.no_push)
    gate_and_push(not args.no_push)
    print(f"integrated {landed} packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
