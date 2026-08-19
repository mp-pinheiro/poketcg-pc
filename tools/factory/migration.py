#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import threading
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import common
import forgejo
import ledger
import packet

ROOT = Path(__file__).resolve().parents[2]
V2_ROOT = ROOT / ".factory" / "v2"
PLAN_PATH = V2_ROOT / "migration-plan.json"
CHECKPOINT_PATH = V2_ROOT / "migration-checkpoint.json"
LEGACY_ROUTINE_ROW = re.compile(r"^\|\s*([A-Za-z_][A-Za-z0-9_]*)\s*\|", re.MULTILINE)
OLD_MARKER = re.compile(r"<!--\s*poketcg-port-work:v1\s*(\{.*?\})\s*-->", re.DOTALL)

LABELS: dict[str, tuple[str, str, bool]] = {
    "port/ready": ("0e8a16", "Factory work ready for claim", True),
    "port/running": ("1d76db", "Factory implementation is leased", True),
    "port/blocked": ("b60205", "Factory work has unresolved dependencies", True),
    "port/recovery": ("d93f0b", "Factory work needs bounded recovery", True),
    "port/integrating": ("5319e7", "Factory artifact awaits gated integration", True),
    "port/paused": ("6a737d", "Factory work is paused by an authorized command", True),
    "port/done": ("1a7f37", "Factory work has pushed gate evidence", True),
    "port/excluded": ("8250df", "Factory work is explicitly excluded", True),
    "tier/1": ("bfd4f2", "Factory complexity tier 1", True),
    "tier/2": ("91ca55", "Factory complexity tier 2", True),
    "tier/3": ("f9d0c4", "Factory complexity tier 3", True),
    "tier/4": ("fef2c0", "Factory complexity tier 4", True),
    "priority/urgent": ("b60205", "Factory scheduling priority urgent", True),
    "priority/high": ("d93f0b", "Factory scheduling priority high", True),
    "priority/normal": ("0e8a16", "Factory scheduling priority normal", True),
    "priority/low": ("6a737d", "Factory scheduling priority low", True),
    "attention/stalled": ("fbca04", "Factory liveness needs attention", False),
    "attention/human": ("5319e7", "Factory needs human decision", False),
    "attention/infrastructure": ("8250df", "Factory infrastructure needs attention", False),
}


class MigrationError(RuntimeError):
    pass


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
    temporary.replace(path)


def old_work_id(body: str) -> str | None:
    matches = OLD_MARKER.findall(body)
    if not matches:
        return None
    if len(matches) != 1:
        raise MigrationError("duplicate legacy work markers")
    try:
        value = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise MigrationError("invalid legacy work marker") from exc
    work_id = value.get("work_id") if isinstance(value, dict) else None
    if not isinstance(work_id, str) or not work_id.startswith("port:v1:"):
        raise MigrationError("legacy marker has invalid work ID")
    return work_id


def replace_old_marker(body: str, work_id: str) -> str:
    matches = list(OLD_MARKER.finditer(body))
    if len(matches) != 1:
        raise MigrationError("expected exactly one legacy work marker")
    marker = f'<!-- poketcg-port-work:v2 {{"work_id":{json.dumps(work_id)}}} -->'
    return body[:matches[0].start()] + marker + body[matches[0].end():]


def generated_body(work_id: str, function: dict[str, Any], state: str) -> str:
    return "\n".join((
        f'<!-- poketcg-port-work:v2 {{"work_id":{json.dumps(work_id)}}} -->',
        "",
        "<!-- poketcg-port-generated:begin -->",
        f"**Routine:** `{function['name']}`",
        f"**Pret source:** `{function['file']}:{function['line']}`",
        f"**Size:** {function['size']} bytes",
        f"**Factory state:** {state}",
        "<!-- poketcg-port-generated:end -->",
        "",
    ))


def labels_for(function: dict[str, Any], state: str) -> list[str]:
    labels = [f"port/{state}", f"tier/{int(function['tier'])}", "priority/normal"]
    if function.get("operational_blocker"):
        labels.append("attention/human")
    return labels


def state_for(function: dict[str, Any]) -> str:
    status = str(function.get("status") or "todo")
    if status == "verified":
        return "done"
    if status == "excluded":
        return "excluded"
    if status == "ported":
        return "integrating"
    if function.get("operational_blocker") or function.get("blockers"):
        return "blocked"
    return "ready"


def _control_actions(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    markers = [issue for issue in issues if ledger.control_marker(issue) is not None]
    if len(markers) > 1:
        raise MigrationError("multiple factory control issues exist")
    if markers:
        return []
    return [{
        "kind": "create-control",
        "title": "[Factory] Control plane",
        "body": '<!-- poketcg-factory-control:v1 {"repository":"mpp/poketcg-pc"} -->\n',
        "labels": ["port/paused"],
    }]


def _cohort_actions(functions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_name = {function["name"]: function for function in functions}
    actions: list[dict[str, Any]] = []
    for group in packet.scc_projection(functions):
        names = set(group["work_ids"])
        members = sorted(by_name[name]["work_id"] for name in names)
        digest = common.cohort_id(set(members))
        work_id = f"cohort:v1:{digest}"
        external = sorted({
            blocker
            for name in names
            for blocker in by_name[name].get("blockers") or []
            if blocker not in names
        })
        vetoed = any(by_name[name].get("operational_blocker") for name in names)
        state = "blocked" if external or vetoed else "ready"
        labels = [f"port/{state}", "tier/4", "priority/normal"]
        if vetoed:
            labels.append("attention/human")
        actions.append({
            "kind": "create-cohort",
            "work_id": work_id,
            "members": members,
            "title": f"[Factory] Cohort {len(members)} routines",
            "body": (
                f'<!-- poketcg-port-cohort:v1 {{"work_id":{json.dumps(work_id)},'
                f'"members":{json.dumps(members, separators=(",", ":"))}}} -->\n'
            ),
            "labels": labels,
            "state": state,
        })
    return sorted(actions, key=lambda action: action["work_id"])


def build_plan(snapshot: dict[str, Any], *, revision: str, gate: dict[str, Any]) -> dict[str, Any]:
    functions, _inventory = packet.compute_functions()
    function_by_name = {function["name"]: function for function in functions}
    existing_v1: dict[str, dict[str, Any]] = {}
    existing_v2: dict[str, dict[str, Any]] = {}
    ambiguous: list[int] = []
    ignored_superseded: list[int] = []
    for issue in snapshot["issues"]:
        marker = ledger.work_marker(issue)
        if marker is not None:
            work_id = str(marker["work_id"])
            if work_id in existing_v2:
                raise MigrationError(f"duplicate v2 work ID {work_id}")
            existing_v2[work_id] = issue
            continue
        legacy = old_work_id(str(issue.get("body") or ""))
        if legacy is not None:
            if legacy in existing_v1:
                raise MigrationError(f"duplicate legacy work ID {legacy}")
            existing_v1[legacy] = issue
            continue
        labels = set(issue.get("labels") or [])
        port_like = "port" in labels or str(issue.get("title") or "").startswith("[T")
        if not port_like:
            continue
        if issue.get("state") == "closed" and "superseded" in labels:
            ignored_superseded.append(int(issue["number"]))
            continue
        names = [
            name for name in LEGACY_ROUTINE_ROW.findall(str(issue.get("body") or ""))
            if name != "routine"
        ]
        if (
            issue.get("state") == "closed"
            and names
            and all(
                name in function_by_name
                and function_by_name[name].get("status") in {"verified", "excluded"}
                for name in names
            )
        ):
            ignored_superseded.append(int(issue["number"]))
            continue
        ambiguous.append(int(issue["number"]))
    actions: list[dict[str, Any]] = _control_actions(snapshot["issues"])
    expected = {function["work_id"] for function in functions}
    for function in sorted(functions, key=lambda item: item["work_id"]):
        work_id = function["work_id"]
        state = state_for(function)
        labels = labels_for(function, state)
        if work_id in existing_v2:
            issue = existing_v2[work_id]
            actions.append({
                "kind": "verify-routine",
                "work_id": work_id,
                "issue_number": issue["number"],
                "state": state,
                "labels": labels,
            })
        elif work_id in existing_v1:
            issue = existing_v1[work_id]
            actions.append({
                "kind": "adopt-routine",
                "work_id": work_id,
                "issue_number": issue["number"],
                "body": replace_old_marker(str(issue.get("body") or ""), work_id),
                "state": state,
                "labels": labels,
            })
        else:
            actions.append({
                "kind": "create-routine",
                "work_id": work_id,
                "title": f"[T{function['tier']}] Port {function['name']}",
                "body": generated_body(work_id, function, state),
                "state": state,
                "labels": labels,
            })
    surplus = sorted((set(existing_v1) | set(existing_v2)) - expected)
    if surplus:
        raise MigrationError(f"managed issues no longer map to inventory: {surplus}")
    actions.extend(_cohort_actions(functions))
    plan = {
        "schema": 1,
        "repository": snapshot["repository"],
        "snapshot_sha256": snapshot["sha256"],
        "revision": revision,
        "gate_commit": gate.get("commit"),
        "created_at": datetime.now(UTC).isoformat(),
        "unmarked_port_like": sorted(ambiguous),
        "ignored_superseded": sorted(ignored_superseded),
        "actions": actions,
        "counts": {
            "functions": len(functions),
            "legacy_markers": len(existing_v1),
            "v2_markers": len(existing_v2),
            "excluded_creates": sum(
                action["kind"] == "create-routine" and action["state"] == "excluded"
                for action in actions
            ),
            "cohorts": sum(action["kind"] == "create-cohort" for action in actions),
        },
    }
    plan["plan_sha256"] = forgejo.sha256({
        key: value for key, value in plan.items() if key != "created_at"
    })
    return plan


def _projection_labels(issue: dict[str, Any], action: dict[str, Any]) -> list[str]:
    labels = {
        label for label in issue.get("labels") or []
        if label != "port"
        and not label.startswith("tier-")
        and not label.startswith("port-")
        and not label.startswith("tier/")
        and not label.startswith("port/")
        and not label.startswith("priority/")
        and not label.startswith("attention/")
    }
    labels.update(action.get("labels") or [])
    return sorted(labels)


def _desired_projection(issue: dict[str, Any], action: dict[str, Any]) -> tuple[list[str], str, str | None]:
    return (
        _projection_labels(issue, action),
        "closed" if action["state"] in {"done", "excluded"} else "open",
        str(action["body"]) if action["kind"] in {"adopt-routine", "create-routine"} else None,
    )


def _already_projected(issue: dict[str, Any], action: dict[str, Any]) -> bool:
    labels, state, body = _desired_projection(issue, action)
    return (
        issue["labels"] == sorted(set(labels))
        and issue["state"] == state
        and (body is None or issue["body"] == body)
    )


def _issue_for_action(
    client: forgejo.ForgejoClient,
    action: dict[str, Any],
    *,
    existing: dict[str, dict[str, Any]],
    control_issue: dict[str, Any] | None,
) -> dict[str, Any]:
    kind = action["kind"]
    work_id = action.get("work_id")
    if isinstance(work_id, str) and work_id in existing:
        known = existing[work_id]
        if kind == "verify-routine" or _already_projected(known, action):
            return known
        labels, state, body = _desired_projection(known, action)
        return client.set_projection(int(known["number"]), labels=labels, state=state, body=body)
    if kind == "verify-routine":
        return client.issue(int(action["issue_number"]))
    if kind == "adopt-routine":
        issue = client.issue(int(action["issue_number"]))
        if _already_projected(issue, action):
            return issue
        labels, state, body = _desired_projection(issue, action)
        return client.set_projection(int(issue["number"]), labels=labels, state=state, body=body)
    if kind == "create-routine":
        issue = client.create_issue(
            title=str(action["title"]),
            body=str(action["body"]),
            labels=list(action["labels"]),
        )
        labels, state, _body = _desired_projection(issue, action)
        if issue["labels"] == sorted(set(labels)) and issue["state"] == state:
            return issue
        return client.set_projection(int(issue["number"]), labels=labels, state=state)
    if kind == "create-cohort":
        return client.create_issue(
            title=str(action["title"]),
            body=str(action["body"]),
            labels=list(action["labels"]),
        )
    if kind == "create-control":
        if control_issue is not None:
            return client.issue(int(control_issue["number"]))
        return client.create_issue(
            title=str(action["title"]),
            body=str(action["body"]),
            labels=list(action["labels"]),
        )
    raise MigrationError(f"unknown migration action {kind}")


def _edge(
    numbers: dict[str, int],
    dependent: str,
    dependency: str,
    *,
    require_complete: bool,
) -> tuple[int, int] | None:
    if dependent in numbers and dependency in numbers:
        return numbers[dependent], numbers[dependency]
    if require_complete:
        raise MigrationError(f"dependency edge {dependent} -> {dependency} has no issue number")
    return None


def _dependency_edges(
    plan: dict[str, Any],
    numbers: dict[str, int],
    *,
    require_complete: bool = True,
) -> list[tuple[int, int]]:
    functions, _inventory = packet.compute_functions()
    by_name = {function["name"]: function for function in functions}
    cohorts = {
        member: action["work_id"]
        for action in plan["actions"]
        if action["kind"] == "create-cohort"
        for member in action["members"]
    }
    actions = {
        action["work_id"]: action
        for action in plan["actions"]
        if isinstance(action.get("work_id"), str)
    }
    edges: set[tuple[int, int]] = set()
    for function in functions:
        work_id = function["work_id"]
        action = actions.get(work_id)
        if action is None or action.get("state") in {"done", "excluded"}:
            continue
        if work_id in cohorts:
            edge = _edge(numbers, work_id, cohorts[work_id], require_complete=require_complete)
            if edge is not None:
                edges.add(edge)
            continue
        for blocker in function.get("blockers") or []:
            dependency = by_name.get(blocker)
            if dependency is None:
                raise MigrationError(f"{work_id} has unknown blocker {blocker}")
            dependency_work_id = cohorts.get(dependency["work_id"], dependency["work_id"])
            if dependency_work_id != work_id:
                edge = _edge(numbers, work_id, dependency_work_id, require_complete=require_complete)
                if edge is not None:
                    edges.add(edge)
    for action in plan["actions"]:
        if action["kind"] != "create-cohort":
            continue
        members = set(action["members"])
        for member in members:
            function = next(function for function in functions if function["work_id"] == member)
            for blocker in function.get("blockers") or []:
                dependency = by_name.get(blocker)
                if dependency is None:
                    raise MigrationError(f"{member} has unknown blocker {blocker}")
                dependency_work_id = cohorts.get(dependency["work_id"], dependency["work_id"])
                if dependency_work_id not in members and dependency_work_id != action["work_id"]:
                    edge = _edge(
                        numbers, action["work_id"], dependency_work_id,
                        require_complete=require_complete,
                    )
                    if edge is not None:
                        edges.add(edge)
    return sorted(edges)


def _migration_event(
    issue: dict[str, Any],
    action: dict[str, Any],
    *,
    plan: dict[str, Any],
    gate: dict[str, Any],
    client: forgejo.ForgejoClient,
) -> ledger.FactoryEvent:
    work_id = str(action["work_id"])
    dependencies = client.dependencies(int(issue["number"]))
    intent = ledger.intent_sha256(issue, dependencies, [])
    state = str(action.get("state") or "ready")
    measured = str(plan["gate_commit"])
    return ledger.FactoryEvent.create(
        kind="migrated",
        run_id="migration",
        work_id=work_id,
        attempt_id=None,
        parent_comment_id=None,
        parent_event_sha256=None,
        base_revision=measured,
        intent_sha256=intent,
        emitted_at=str(plan["created_at"]),
        payload={
            "state": state,
            "source_revision": measured,
            "publication_revision": measured if state == "done" else "",
            "gate_sha256": forgejo.sha256(gate),
            "legacy_history_sha256": forgejo.sha256(action),
            "landed_at": plan["created_at"] if state == "done" else None,
            "exclusion_reason": "migration" if state == "excluded" else None,
        },
    )


def _fan_out(items: Iterable[Any], worker: Callable[[Any], Any], *, workers: int) -> list[Any]:
    values = list(items)
    if workers <= 1 or len(values) <= 1:
        return [worker(value) for value in values]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(worker, values))


def apply_plan(
    client: forgejo.ForgejoClient,
    plan: dict[str, Any],
    *,
    gate: dict[str, Any],
    limit: int | None = None,
    workers: int = 8,
) -> dict[str, Any]:
    if plan.get("gate_commit") != gate.get("commit"):
        raise MigrationError("migration plan no longer matches the current gate")
    if plan.get("unmarked_port_like"):
        raise MigrationError("migration has unmarked port-like issues")
    client.ensure_labels(LABELS)
    current = client.stable_snapshot()
    existing: dict[str, dict[str, Any]] = {}
    control_issue: dict[str, Any] | None = None
    for issue in current["issues"]:
        marker = ledger.work_marker(issue)
        if marker is not None:
            existing[str(marker["work_id"])] = issue
        if ledger.control_marker(issue) is not None:
            control_issue = issue
    numbers = {
        work_id: int(issue["number"])
        for work_id, issue in existing.items()
    }
    actions = plan["actions"] if limit is None else plan["actions"][:limit]
    scoped = plan if limit is None else {**plan, "actions": actions}
    lock = threading.Lock()
    applied: dict[str, dict[str, Any]] = {}
    progress = 0

    def project(action: dict[str, Any]) -> None:
        nonlocal control_issue, progress
        with lock:
            snapshot_existing = dict(existing)
            snapshot_control = control_issue
        issue = _issue_for_action(
            client,
            action,
            existing=snapshot_existing,
            control_issue=snapshot_control,
        )
        work_id = action.get("work_id")
        with lock:
            if isinstance(work_id, str):
                numbers[work_id] = int(issue["number"])
                existing[work_id] = issue
                applied[work_id] = issue
            elif action["kind"] == "create-control":
                control_issue = issue
            progress += 1
            if progress % 50 == 0:
                atomic_json(CHECKPOINT_PATH, {
                    "plan_sha256": plan["plan_sha256"],
                    "completed": progress,
                    "numbers": numbers,
                })

    _fan_out(actions, project, workers=workers)
    edges = _dependency_edges(scoped, numbers, require_complete=limit is None)
    _fan_out(edges, lambda edge: client.add_dependency(edge[0], edge[1]), workers=workers)

    def publish(action: dict[str, Any]) -> None:
        work_id = action.get("work_id")
        if not isinstance(work_id, str) or action["kind"] == "verify-routine":
            return
        issue = applied.get(work_id) or client.issue(numbers[work_id])
        event = _migration_event(
            issue,
            action,
            plan=plan,
            gate=gate,
            client=client,
        )
        client.append_event(int(issue["number"]), event.comment_body(), event.event_id)

    _fan_out(actions, publish, workers=workers)
    atomic_json(CHECKPOINT_PATH, {
        "plan_sha256": plan["plan_sha256"],
        "completed": progress,
        "numbers": numbers,
    })
    return {
        "applied": progress,
        "remaining": len(plan["actions"]) - progress,
        "dependencies": len(edges),
        "numbers": numbers,
        "plan_sha256": plan["plan_sha256"],
    }
