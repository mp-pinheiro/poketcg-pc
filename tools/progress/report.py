#!/usr/bin/env python3
"""Compute the port progress report from the pret inventory, scope rules,
registry, and gate record. Writes site/data/progress.json.

Reads only site/data/inventory.json, tools/progress/scope.toml,
tests/routines.py, and (if present) site/data/gate.json — never poketcg/,
so it runs in CI without a disassembly checkout.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
import time
import tomllib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
INVENTORY = ROOT / "site" / "data" / "inventory.json"
SCOPE = ROOT / "tools" / "progress" / "scope.toml"
REGISTRY = ROOT / "tests" / "routines.py"
GATE = ROOT / "site" / "data" / "gate.json"
PROGRESS = ROOT / "site" / "data" / "progress.json"
HISTORY = ROOT / "site" / "data" / "history.jsonl"
BLOCKED = ROOT / ".factory" / "blocked.toml"
COMPLETION_TOOL = ROOT / "tools" / "completion" / "completion.py"

TIER_BOUNDS = ((1, 0, 100), (2, 100, 300), (3, 300, 800), (4, 800, None))
LIFECYCLE_STATES = (
    "ready", "blocked", "active", "awaiting-gate", "failing", "complete",
    "excluded",
)


def _write_json_atomic(path: Path, payload: dict) -> None:
    """Publish progress.json by rename: the factory reads it while we write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def tier_for(size: int) -> int:
    for tier, lower, upper in TIER_BOUNDS:
        if upper is None or size < upper:
            return tier
    return 4


def canonical_work_id(source: str, name: str) -> str:
    if not source or not name:
        raise ValueError("a routine needs a source path and symbol")
    return f"port:v1:{source}:{name}"


# Mirrors tools/oracle/fn_all.py's GATE_INPUT_PATHS; both sides must name the
# same tracked paths in the same order or the gate reads as untrusted.
GATE_INPUT_PATHS = ("src", "tests", "tools/oracle", "CMakeLists.txt")


def gate_input_trees() -> dict[str, str] | None:
    """Map every measured gate input to its git tree id at the revision under test.

    Identity travels inside the commit, so a landing keeps its trust when CI
    re-parents it onto a release commit: the trees are byte-identical while the
    commit id the gate ran at no longer exists in the published history. In CI
    HEAD is the commit under test; in the colocated jj checkout HEAD is @-,
    which is the revision tools/oracle/fn_all.py recorded.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", *(f"HEAD:{path}" for path in GATE_INPUT_PATHS)],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    ids = result.stdout.split()
    if result.returncode != 0 or len(ids) != len(GATE_INPUT_PATHS):
        return None
    return dict(zip(GATE_INPUT_PATHS, ids))


def gate_is_trusted(gate_data: dict | None) -> bool:
    """Return true only for a complete, structurally valid gate."""
    if not gate_data or gate_data.get("schema") != 1:
        return False
    if not gate_data.get("complete"):
        return False
    inventory = gate_data.get("inventory") or {}
    count = inventory.get("routines")
    if (
        not isinstance(count, int)
        or count <= 0
        or inventory.get("failures", 0)
        or inventory.get("primary_missing", 0)
    ):
        return False
    routines = gate_data.get("routines")
    if (
        not isinstance(routines, dict)
        or not routines
        or len(routines) != count
        or any(
            not isinstance(entry, dict)
            or entry.get("status") not in {"pass", "fail"}
            for entry in routines.values()
        )
    ):
        return False
    if not gate_data.get("commit"):
        return False
    recorded_trees = gate_data.get("input_trees")
    if not isinstance(recorded_trees, dict) or not recorded_trees:
        return False
    computed_trees = gate_input_trees()
    if computed_trees is None:
        return False
    return recorded_trees == computed_trees


def load_operational_blockers() -> dict[str, dict]:
    if not BLOCKED.exists():
        return {}
    with BLOCKED.open("rb") as stream:
        data = tomllib.load(stream)
    blockers: dict[str, dict] = {}
    for entry in data.get("blocked", []):
        name = entry.get("name")
        if not name:
            fail("blocked.toml entry has no name")
        if name in blockers:
            fail(f"duplicate operational blocker: {name}")
        blockers[name] = {
            "reason": str(entry.get("reason", "operational blocker")),
            "unblock": str(entry.get("unblock", "clear the blocker")),
        }
    return blockers


def project_work_records(
    functions: list[dict],
    gate_data: dict | None,
    *,
    active_packets: dict[str, dict] | None = None,
) -> list[dict]:
    """Project report rows into stable, issue-sized desired work records."""
    trusted = gate_is_trusted(gate_data)
    gate_routines = (gate_data or {}).get("routines") or {}
    operational = load_operational_blockers()
    active_packets = active_packets or {}
    records = []
    for function in functions:
        source = function.get("file")
        name = function["name"]
        work_id = canonical_work_id(source, name) if source else None
        work = {
            "work_id": work_id,
            "name": name,
            "source": source,
            "line": function.get("line"),
            "size": function.get("size", 0),
            "refs": function.get("refs", 0),
            "tier": tier_for(function.get("size", 0)),
            "excluded": function["status"] == "excluded",
            "blockers": list(function.get("blockers") or []),
            "operational_blocker": operational.get(name),
            "packet": active_packets.get(work_id),
            "gate_trusted": trusted,
        }
        if work["excluded"]:
            work["state"] = "excluded"
        elif trusted and gate_routines.get(name, {}).get("status") == "pass":
            work["state"] = "complete"
        elif trusted and gate_routines.get(name, {}).get("status") == "fail":
            work["state"] = "failing"
        elif function["status"] in ("ported", "verified", "failing"):
            work["state"] = "awaiting-gate"
        elif work["packet"] and work["packet"].get("state") in {
            "pending", "translated", "verifying", "repair", "green",
        }:
            work["state"] = "active"
        elif work["operational_blocker"] or work["blockers"]:
            work["state"] = "blocked"
        else:
            work["state"] = "ready"
        records.append(work)
    return records


def fail(msg: str) -> None:
    print(f"report: {msg}", file=sys.stderr)
    raise SystemExit(2)


def parent(name: str) -> str:
    return name.split(".", 1)[0]


def _resolve_ast_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _resolve_ast_name(node.value)
        return f"{base}.{node.attr}" if base else None
    return None


def _load_registry() -> dict[str, tuple[str, ...]] | None:
    spec = importlib.util.spec_from_file_location("routines_registry", REGISTRY)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None
    return module.ROUTINES


def load_routines() -> tuple[set[str], dict[str, str]]:
    raw = _load_registry()
    if raw is None:
        fail(f"cannot load {REGISTRY}")
    ported_parents: set[str] = set()
    name_to_parent: dict[str, str] = {}
    for entries in raw.values():
        for name in entries:
            p = parent(name)
            ported_parents.add(p)
            name_to_parent[name] = p
    return ported_parents, name_to_parent


def load_scope() -> list[dict]:
    if not SCOPE.exists():
        fail("scope.toml not found")
    with open(SCOPE, "rb") as f:
        data = tomllib.load(f)
    return data.get("exclude", [])

def load_id_migrations() -> dict[str, str]:
    if not SCOPE.exists():
        return {}
    with SCOPE.open("rb") as stream:
        data = tomllib.load(stream)
    migrations: dict[str, str] = {}
    for entry in data.get("id_migration", []):
        old = entry.get("old_work_id")
        new = entry.get("new_work_id")
        if (
            not isinstance(old, str) or not old.startswith("port:v1:")
            or not isinstance(new, str) or not new.startswith("port:v1:")
            or old in migrations
        ):
            fail("invalid or duplicate explicit work-ID migration")
        migrations[old] = new
    return migrations


def resolve_scope(
    rules: list[dict], functions: dict[str, dict], inventory: dict,
) -> tuple[dict[str, dict], set[str], int, int]:
    excluded: dict[str, dict] = {}
    for rule in rules:
        kind = rule["kind"]
        reason = rule["reason"]
        files = rule.get("files", [])
        symbols = rule.get("symbols", [])
        matched_any = False
        for name, info in functions.items():
            if name in excluded:
                continue
            if name in symbols or info.get("file") in files:
                excluded[name] = {"kind": kind, "reason": reason}
                matched_any = True
        if not matched_any:
            fail(f"scope: rule matches nothing: {reason}")
    excl_bytes = sum(inventory["functions"][n]["size"] for n in excluded)
    return excluded, set(excluded), len(excluded), excl_bytes


def category_for(file: str) -> str:
    if file is None:
        return "unknown"
    parts = file.split("/")
    if len(parts) >= 3 and parts[0] == "src" and parts[1] == "engine":
        return f"{parts[0]}/{parts[1]}/{parts[2]}"
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return "unknown"


def load_inventory() -> dict:
    if not INVENTORY.exists():
        fail("site/data/inventory.json missing; run just progress-inventory")
    with open(INVENTORY) as f:
        inv = json.load(f)
    artifacts = ROOT / "tools" / "oracle" / "artifacts.json"
    if artifacts.exists():
        with open(artifacts) as f:
            pret_expected = json.load(f).get("pret", {}).get("commit", "")
        if pret_expected and inv.get("pret_commit", "")[:7] != pret_expected[:7]:
            fail(f"inventory is stale for pret {pret_expected}; run just progress-inventory")
    return inv


def load_gate() -> dict | None:
    if not GATE.exists():
        return None
    with open(GATE) as f:
        return json.load(f)

def load_completion_status() -> dict | None:
    if not COMPLETION_TOOL.exists():
        return None
    try:
        result = subprocess.run(
            [sys.executable, str(COMPLETION_TOOL), "status", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"schema": 2, "complete": False, "errors": [str(exc)]}
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {
            "schema": 2,
            "complete": False,
            "errors": [f"completion status is not JSON: {exc}"],
        }
    if not isinstance(value, dict):
        return {"schema": 2, "complete": False, "errors": ["completion status is not an object"]}
    if result.returncode:
        value.setdefault("errors", []).append(
            f"completion status exited {result.returncode}"
        )
        value["complete"] = False
    return value


def jj_commit_short() -> str | None:
    commands = (
        ["jj", "log", "-r", "@-", "--no-graph", "-T", "commit_id"],
        ["git", "rev-parse", "HEAD"],
    )
    for command in commands:
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception:
            pass
    return None


def jj_commits() -> list[tuple[str, int]]:
    try:
        result = subprocess.run(
            ["jj", "log", "-r", "::main", "--no-graph",
             "-T", 'commit_id.short() ++ "|" ++ committer.timestamp().utc() ++ "\\n"'],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return []
        from datetime import datetime, timezone
        commits = []
        for line in result.stdout.strip().splitlines():
            if "|" not in line:
                continue
            cid, ts_str = line.split("|", 1)
            try:
                dt = datetime.strptime(ts_str.rsplit(" ", 1)[0], "%Y-%m-%d %H:%M:%S.%f")
                ts = int(dt.replace(tzinfo=timezone.utc).timestamp())
                commits.append((cid, ts))
            except ValueError:
                pass
        return commits
    except Exception:
        return []


def get_routines_at(rev: str) -> set[str] | None:
    try:
        result = subprocess.run(
            ["jj", "file", "show", "-r", rev, "tests/routines.py"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return None
        tree = ast.parse(result.stdout)
        routines_node = None
        for stmt in ast.iter_child_nodes(tree):
            if isinstance(stmt, (ast.AnnAssign, ast.Assign)):
                targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
                for target in targets:
                    if _resolve_ast_name(target) == "ROUTINES":
                        routines_node = stmt.value
                        break
            if routines_node is not None:
                break
        if routines_node is None:
            return None
        raw: dict[str, tuple[str, ...]] = ast.literal_eval(routines_node)
        return {parent(name) for entries in raw.values() for name in entries}
    except Exception:
        return None


def recent_ports(inventory: dict, limit: int = 8) -> list[dict]:
    """Newest port files by creation date.

    Returns [{"name": str, "file": str | None, "timestamp": int}, ...]
    sorted by timestamp desc. ``file`` is the pret asm path when the stem
    maps 1:1 to a pret file, else None (ambiguous stems like core/debug/save).
    Degrades to [] when git is unavailable.
    """
    routines = _load_registry()
    if routines is None:
        return []

    funcs = inventory["functions"]
    stem_file: dict[str, str | None] = {}
    for stem, names in routines.items():
        files = {funcs[n]["file"] for n in names if n in funcs}
        stem_file[stem] = next(iter(files)) if len(files) == 1 else None

    try:
        result = subprocess.run(
            ["git", "log", "--name-only", "--diff-filter=A",
             "--format=COMMIT|%ct", "--", "src/home"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return []
        created: dict[str, int] = {}
        cur = None
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("COMMIT|"):
                cur = int(line.split("|", 1)[1])
            elif cur is not None and line.startswith("src/home/") and line.endswith(".c"):
                created.setdefault(line, cur)
    except Exception:
        return []

    entries = []
    for stem in routines:
        cfile = f"src/home/{stem}.c"
        if cfile in created:
            entries.append({
                "name": stem_file[stem] or stem,
                "file": stem_file[stem],
                "timestamp": created[cfile],
            })
    entries.sort(key=lambda e: e["timestamp"], reverse=True)
    return entries[:limit]


def compute(inventory: dict, routines: set[str], gate_data: dict | None) -> dict:
    funcs = inventory["functions"]
    excluded_map, excluded_set, excl_funcs, excl_bytes = resolve_scope(
        load_scope(), funcs, inventory,
    )
    print(f"scope: {excl_funcs} functions / {excl_bytes} bytes excluded", file=sys.stderr)

    for name in excluded_set:
        if name in routines:
            fail(f"scope: {name} is both excluded and ported")

    for name in sorted(routines):
        if name not in funcs:
            fail(f"ROUTINES names {name}, not a code label in the inventory")

    gate_routines: dict[str, dict] = {}
    if gate_data and gate_data.get("routines"):
        gate_routines = gate_data["routines"]

    functions_out: list[dict] = []
    categories: dict[str, dict] = {}
    units: dict[str, dict] = {}

    for name in sorted(funcs.keys()):
        info = funcs[name]
        file = info.get("file")
        size = info["size"]
        deps = info.get("deps", [])
        fallthrough = info.get("fallthrough")
        refs = info.get("refs", 0)

        if name in excluded_set:
            exc = excluded_map[name]
            functions_out.append({
                "name": name, "file": file, "line": info["line"], "size": size,
                "status": "excluded", "ready": False, "refs": refs,
                "blockers": [], "excluded_kind": exc["kind"],
                "excluded_reason": exc["reason"],
            })
            continue

        cat = category_for(file)
        if cat not in categories:
            categories[cat] = {"name": cat, "code": 0, "code_total": 0,
                               "functions": 0, "functions_total": 0}
        categories[cat]["code_total"] += size
        categories[cat]["functions_total"] += 1

        if file and file not in units:
            units[file] = {"file": file, "category": cat,
                           "code": 0, "code_total": 0,
                           "functions": 0, "functions_total": 0}
        if file:
            units[file]["code_total"] += size
            units[file]["functions_total"] += 1

        ported = name in routines
        is_failing = False
        is_verified = False
        if ported:
            gate_r = gate_routines.get(name)
            if gate_r is not None:
                is_verified = gate_r["status"] == "pass"
                is_failing = gate_r["status"] == "fail"

        if is_verified:
            status = "verified"
        elif is_failing:
            status = "failing"
        elif ported:
            status = "ported"
        else:
            status = "todo"

        all_blockers = list(deps)
        if fallthrough:
            all_blockers.append(fallthrough)
        unported_blockers = [b for b in all_blockers
                            if b not in routines and b not in excluded_set
                            and b in funcs]
        ready = status == "todo" and not unported_blockers

        functions_out.append({
            "name": name, "file": file, "line": info["line"], "size": size,
            "status": status, "ready": ready, "refs": refs,
            "blockers": unported_blockers if status == "todo" else [],
            "excluded_kind": None, "excluded_reason": None,
        })

        if status in ("verified", "ported", "failing"):
            categories[cat]["code"] += size
            categories[cat]["functions"] += 1
            if file:
                units[file]["code"] += size
                units[file]["functions"] += 1

    categories_list = sorted(categories.values(), key=lambda c: c["name"])
    units_list = sorted(units.values(), key=lambda u: u["file"])

    total_code = sum(c["code"] for c in categories_list)
    total_code_all = sum(c["code_total"] for c in categories_list)
    total_funcs = sum(c["functions"] for c in categories_list)
    total_funcs_all = sum(c["functions_total"] for c in categories_list)

    verified_code = sum(
        f["size"] for f in functions_out if f["status"] == "verified"
    )
    verified_funcs = sum(1 for f in functions_out if f["status"] == "verified")

    unit_done = sum(1 for u in units_list if u["code"] == u["code_total"])
    unit_total = len(units_list)

    gate_summary = {"present": False, "complete": False, "commit": None}
    if gate_data:
        gate_summary = {
            "present": True,
            "complete": gate_data.get("complete", False),
            "commit": gate_data.get("commit"),
            "trusted": gate_is_trusted(gate_data),
        }
    work_records = project_work_records(functions_out, gate_data)
    work_ids = [record["work_id"] for record in work_records
                if not record["excluded"]]
    if None in work_ids or len(work_ids) != len(set(work_ids)):
        fail("work-record projection produced a missing or duplicate work ID")

    return {
        "schema": 1,
        "generated_at": int(time.time()),
        "commit": None,
        "commit_url": None,
        "pret_commit": inventory["pret_commit"],
        "pret_blob": f"https://github.com/pret/poketcg/blob/{inventory['pret_commit'][:7]}/",
        "id_migrations": load_id_migrations(),
        "gate": gate_summary,
        "measures": {
            "code": total_code,
            "code/total": total_code_all,
            "verified_code": verified_code,
            "verified_code/total": total_code_all,
            "functions": total_funcs,
            "functions/total": total_funcs_all,
            "verified_functions": verified_funcs,
            "verified_functions/total": total_funcs_all,
            "excluded_code": excl_bytes,
            "excluded_functions": excl_funcs,
            "data_bytes": inventory["totals"]["data_bytes"],
            "rom_bytes": inventory["rom_bytes"],
            "units": unit_done,
            "units/total": unit_total,
        },
        "categories": categories_list,
        "units": units_list,
        "functions": functions_out,
        "work_records": work_records,
    }


def subcommand_build():
    inv = load_inventory()
    routines_set, _ = load_routines()
    gate_data = load_gate()
    commit = jj_commit_short()
    report = compute(inv, routines_set, gate_data)
    completion = load_completion_status()
    if completion is not None:
        report["completion"] = completion
    report["recent"] = recent_ports(inv)
    previous_report = None
    if PROGRESS.exists():
        try:
            previous_report = json.loads(PROGRESS.read_text())
        except json.JSONDecodeError:
            pass
    unchanged = previous_report is not None and all(
        previous_report.get(key) == report.get(key)
        for key in (
            "measures", "categories", "units", "functions", "work_records",
            "id_migrations", "completion", "recent",
        )
    )
    if unchanged and previous_report.get("commit"):
        report["commit"] = previous_report["commit"]
        report["commit_url"] = previous_report.get("commit_url")
        report["generated_at"] = previous_report.get("generated_at", report["generated_at"])
    elif commit:
        report["commit"] = commit[:12]
        report["commit_url"] = f"https://github.com/mp-pinheiro/poketcg-pc/commit/{commit}"

    _write_json_atomic(PROGRESS, report)

    line = {
        "commit": commit[:12] if commit else None,
        "timestamp": int(time.time()),
        "code": report["measures"]["code"],
        "code_total": report["measures"]["code/total"],
        "functions": report["measures"]["functions"],
        "functions_total": report["measures"]["functions/total"],
    }
    points_by_day = {}
    if HISTORY.exists():
        with open(HISTORY) as f:
            for entry_line in f:
                try:
                    point = json.loads(entry_line)
                    points_by_day[point["timestamp"] // 86400] = point
                except (json.JSONDecodeError, KeyError, TypeError):
                    pass
    day = line["timestamp"] // 86400
    existing = points_by_day.get(day)
    measure_keys = ("code", "code_total", "functions", "functions_total")
    if existing is None or any(existing.get(key) != line[key] for key in measure_keys):
        points_by_day[day] = line
    points = sorted(points_by_day.values(), key=lambda p: p.get("timestamp", 0))
    with open(HISTORY, "w") as f:
        for p in points:
            f.write(json.dumps(p, sort_keys=True, separators=(",", ":")) + "\n")
    m = report["measures"]
    pct = m["code"] * 100 / m["code/total"]
    print(f"progress: {m['code']}/{m['code/total']} code bytes ({pct:.2f}%)")


def subcommand_check():
    inv = load_inventory()
    routines_set, _ = load_routines()
    gate_data = load_gate()
    current = compute(inv, routines_set, gate_data)
    committed = None
    if PROGRESS.exists():
        with open(PROGRESS) as f:
            committed = json.load(f)
    if committed is None:
        fail("site/data/progress.json missing; run just progress first")
    diffs = []
    for key in (
        "measures", "categories", "units", "functions", "work_records",
        "id_migrations",
    ):
        a = json.dumps(current.get(key), sort_keys=True)
        b = json.dumps(committed.get(key), sort_keys=True)
        if a != b:
            diffs.append(key)
    if diffs:
        for key in diffs:
            print(f"progress.json mismatch: {key}")
        raise SystemExit(1)
    print("progress.json is current")


def subcommand_frontier(args: list[str]):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--dir")
    ap.add_argument("--json", action="store_true")
    opts = ap.parse_args(args)
    inv = load_inventory()
    routines_set, _ = load_routines()
    gate_data = load_gate()
    report = compute(inv, routines_set, gate_data)
    ready = [f for f in report["functions"]
             if f["status"] == "todo" and f["ready"]]
    ready.sort(key=lambda f: f["size"], reverse=True)
    if opts.dir:
        ready = [f for f in ready if (f["file"] or "").startswith(opts.dir)]
    if opts.json:
        out = ready if opts.limit == 0 else ready[:opts.limit]
        print(json.dumps(out, sort_keys=True, separators=(",", ":")))
    else:
        limit = opts.limit if opts.limit > 0 else len(ready)
        for f in ready[:limit]:
            suffix = " [unreferenced]" if f["refs"] == 0 else ""
            print(f"{f['size']}b  {f['name']}  {f['file']}:{f['line']}  deps={len(f['blockers'])}{suffix}")


def subcommand_backfill():
    inv = load_inventory()
    commits = jj_commits()
    points = []
    skipped = 0
    for commit_id, timestamp in commits:
        routines = get_routines_at(commit_id)
        if routines is None:
            skipped += 1
            continue
        report = compute(inv, routines, None)
        points.append({
            "commit": commit_id,
            "timestamp": timestamp,
            "code": report["measures"]["code"],
            "code_total": report["measures"]["code/total"],
            "functions": report["measures"]["functions"],
            "functions_total": report["measures"]["functions/total"],
        })
    points.sort(key=lambda p: p["timestamp"])
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY, "w") as f:
        for p in points:
            f.write(json.dumps(p, sort_keys=True, separators=(",", ":")) + "\n")
    print(f"backfill: {len(points)} points, {skipped} revisions skipped")


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] == "build":
        subcommand_build()
    elif sys.argv[1] == "check":
        subcommand_check()
    elif sys.argv[1] == "frontier":
        subcommand_frontier(sys.argv[2:])
    elif sys.argv[1] == "backfill":
        subcommand_backfill()
    else:
        print(f"usage: {sys.argv[0]} [build|check|frontier|backfill]", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
