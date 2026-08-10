#!/usr/bin/env python3
"""Generate tiered GitHub issues for ready-to-port routines.

Reads the frontier from report.py, groups routines by pret source file,
tiers by total bytes, and creates GitHub issues via `gh issue create`.
Idempotent: skips issues that already exist (matched by title).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
REPORT = ROOT / "tools" / "progress" / "report.py"
INVENTORY = ROOT / "site" / "data" / "inventory.json"

TIER_BOUNDS = [
    (1, 0, 100),       # tier-1: <100 bytes — quick wins
    (2, 100, 300),     # tier-2: 100–300 bytes — medium effort
    (3, 300, 800),     # tier-3: 300–800 bytes — large tasks
    (4, 800, None),    # tier-4: >800 bytes — major undertakings
]

LABELS = {
    "port": ("1d76db", "Routine porting work"),
    "tier-1": ("0e8a16", "Quick wins (<100 bytes)"),
    "tier-2": ("fbca04", "Medium effort (100–300 bytes)"),
    "tier-3": ("d93f0b", "Large porting tasks (300–800 bytes)"),
    "tier-4": ("b60205", "Major undertakings (>800 bytes)"),
}


def fail(msg: str) -> None:
    print(f"gen_port_issues: {msg}", file=sys.stderr)
    raise SystemExit(2)


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def fetch_frontier(dir_filter: str | None) -> list[dict]:
    argv = [sys.executable, str(REPORT), "frontier", "--limit", "0", "--json"]
    if dir_filter:
        argv.extend(["--dir", dir_filter])
    raw = subprocess.check_output(argv, text=True)
    return json.loads(raw)


def load_pret_commit() -> str:
    with open(INVENTORY) as f:
        inv = json.load(f)
    return inv["pret_commit"]


def tier_for(total_bytes: int) -> int:
    for tier, lo, hi in TIER_BOUNDS:
        if hi is None:
            return tier
        if total_bytes < hi:
            return tier
    return 4


def group_by_file(routines: list[dict]) -> dict[str, dict]:
    groups: dict[str, dict] = {}
    for r in routines:
        file = r["file"]
        if file not in groups:
            groups[file] = {
                "file": file,
                "basename": Path(file).stem,
                "routines": [],
                "total_bytes": 0,
            }
        groups[file]["routines"].append(r)
        groups[file]["total_bytes"] += r["size"]
    return groups


def build_issue_body(
    group: dict, tier: int, pret_commit: str, pret_blob_base: str
) -> str:
    basename = group["basename"]
    file = group["file"]
    routines = group["routines"]
    total = group["total_bytes"]

    table_lines = [
        "| routine | size | line | refs |",
        "|---------|------|------|------|",
    ]
    for r in sorted(routines, key=lambda r: r["name"]):
        table_lines.append(
            f"| {r['name']} | {r['size']}b | {r['line']} | {r['refs']} |"
        )

    routine_names = [r["name"] for r in routines]
    first_routine = routine_names[0]

    body = f"""## Port: {basename} (tier {tier})

**Pret source:** `poketcg/{file}` (pin {pret_commit[:7]})
**Pret link:** {pret_blob_base}/{file}

### Routines to port ({len(routines)} routines, {total}b total)

{chr(10).join(table_lines)}

### Files to create

- `src/home/{basename}.h` — prototypes
- `src/home/{basename}.c` — the C port
- `src/probe/{basename}.c` — adapters + `probe_entries_{basename}[]`
- `tests/cases/{basename}.py` — CONTRACT + CASES + SCHEMA2_CASES

### Edit

- `tests/routines.py` — add `"{basename}": ({", ".join(repr(n) for n in routine_names)},)` to ROUTINES (create the key if it doesn't exist)

### Validate

```sh
just oracle-diff {first_routine}   # must print PASS, for EACH routine
just progress                      # regenerate progress.json
```

### Acceptance

- [ ] `just oracle-diff <RoutineName>` prints PASS for every routine
- [ ] Mutation test: corrupt -> RED -> restore -> PASS
- [ ] `just progress` runs and updates site/data/progress.json
- [ ] `git commit -m "feat(port): <subject>"` (Conventional Commits, <=50 char subject)
"""
    return body


def issue_exists(title: str) -> bool:
    result = subprocess.run(
        ["gh", "issue", "list", "--search", title, "--state", "open",
         "--json", "title", "--jq", ".[].title"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return False
    return title in result.stdout.splitlines()


def ensure_labels() -> None:
    for name, (color, desc) in LABELS.items():
        subprocess.run(
            ["gh", "label", "create", name,
             "--color", color, "--description", desc],
            capture_output=True,
        )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate tiered GitHub issues for ready-to-port routines."
    )
    ap.add_argument("--tier", type=int, choices=[1, 2, 3, 4],
                    help="Only create issues for this tier")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what would be created, don't create")
    ap.add_argument("--dir",
                    help="Filter frontier to a directory prefix "
                         "(e.g. src/home)")
    opts = ap.parse_args()

    try:
        routines = fetch_frontier(opts.dir)
    except subprocess.CalledProcessError:
        fail("could not fetch frontier; run `just progress` first")

    if not routines:
        print("no ready routines found")
        return

    pret_commit = load_pret_commit()
    pret_blob_base = f"https://github.com/pret/poketcg/blob/{pret_commit}"

    groups = group_by_file(routines)

    tiers: dict[int, list[dict]] = {}
    for file, group in groups.items():
        t = tier_for(group["total_bytes"])
        tiers.setdefault(t, []).append(group)

    ensure_labels()

    total_created = 0
    total_skipped = 0

    for tier in sorted(tiers):
        if opts.tier is not None and tier != opts.tier:
            continue

        file_groups = sorted(tiers[tier], key=lambda g: g["total_bytes"],
                             reverse=True)

        for group in file_groups:
            title = (
                f"[T{tier}] Port {group['basename']}: "
                f"{len(group['routines'])} routines, "
                f"{group['total_bytes']}b"
            )
            body = build_issue_body(group, tier, pret_commit, pret_blob_base)
            labels = ["port", f"tier-{tier}"]

            if opts.dry_run:
                print(f"WOULD CREATE: {title}")
                print(f"  labels: {labels}")
                print(f"  body:   {len(body)} bytes")
                print()
                total_created += 1
                continue

            if issue_exists(title):
                print(f"SKIP (exists): {title}")
                total_skipped += 1
                continue

            label_args: list[str] = []
            for lbl in labels:
                label_args.extend(["--label", lbl])

            subprocess.run(
                ["gh", "issue", "create",
                 "--title", title,
                 "--body", body,
                 *label_args],
                check=True,
            )
            print(f"CREATED: {title}")
            total_created += 1

    print()
    print(f"created: {total_created}  skipped: {total_skipped}  "
          f"total: {total_created + total_skipped}")


if __name__ == "__main__":
    main()
