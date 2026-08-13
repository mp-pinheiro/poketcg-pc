#!/usr/bin/env python3
"""Plan and reconcile one managed GitHub issue per port routine.

Normal mode is marker-scoped: unmarked historical issues are read and reported
but never adopted or rewritten.  Legacy adoption is available only through the
explicit ``migrate`` command.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, write_json  # noqa: E402

REPORT_PATH = ROOT / "tools" / "progress" / "report.py"
CACHE = ROOT / ".factory" / "issues-cache.json"
PLAN_PATH = ROOT / ".factory" / "issues-plan.json"
APPLY_STATE = ROOT / ".factory" / "issues-apply-state.json"
MARKER = re.compile(
    r"<!--\s*poketcg-port-work:v1\s*(\{.*?\})\s*-->",
    re.DOTALL,
)
MARKER_PREFIX = "<!-- poketcg-port-work:v1"
GEN_BEGIN = "<!-- poketcg-port-generated:begin -->"
GEN_END = "<!-- poketcg-port-generated:end -->"
LIFECYCLE = {
    "port-ready", "port-blocked", "port-active", "port-awaiting-gate",
    "port-failing", "port-complete", "port-excluded",
}
MANAGED_LABELS = {"port", "tier-1", "tier-2", "tier-3", "tier-4"} | LIFECYCLE
LABEL_META = {
    "port-ready": ("1d76db", "Routine is semantically ready"),
    "port-blocked": ("b60205", "Routine has a recorded blocker"),
    "port-active": ("fbca04", "Routine is claimed by a factory packet"),
    "port-awaiting-gate": ("d93f0b", "Routine landed without a trusted gate"),
    "port-failing": ("b60205", "Trusted gate reports a routine failure"),
    "port-complete": ("0e8a16", "Routine passed the trusted release gate"),
    "port-excluded": ("6f42c1", "Previously managed routine is excluded"),
}
ROW = re.compile(
    r"^\|\s*([A-Za-z_][A-Za-z0-9_.]*)\s*\|\s*(\d+)b\s*\|\s*(\d+)\s*\|"
)
SOURCE = re.compile(r"\*\*Pret source:\*\*\s*`(?:poketcg/)?([^`]+)`")


class ModelError(ValueError):
    pass


def fail(message: str) -> None:
    raise SystemExit(f"issues: {message}")


def sha(data: object) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def run_gh(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["gh", *args], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if check and result.returncode:
        raise ModelError(result.stderr.strip() or "gh command failed")
    return result.stdout.strip()

def ensure_labels(labels: set[str]) -> None:
    for label in sorted(labels & (MANAGED_LABELS | {"superseded"})):
        if label in LABEL_META:
            color, description = LABEL_META[label]
        elif label == "port":
            color, description = "1d76db", "Routine porting work"
        elif label.startswith("tier-"):
            color, description = "fbca04", "Routine effort tier"
        else:
            color, description = "6f42c1", "Managed factory label"
        run_gh(
            "label", "create", label, "--color", color,
            "--description", description, check=False,
        )


def normalize_issue(raw: dict) -> dict:
    labels = raw.get("labels") or []
    normalized = []
    for label in labels:
        normalized.append(label.get("name") if isinstance(label, dict) else label)
    return {
        "id": raw.get("id"),
        "number": int(raw["number"]),
        "title": raw.get("title", ""),
        "body": raw.get("body") or "",
        "state": str(raw.get("state", "OPEN")).lower(),
        "labels": sorted(x for x in normalized if x),
        "url": raw.get("url"),
    }


def snapshot_fingerprint(snapshot: dict) -> str:
    return sha({
        "schema": snapshot.get("schema"),
        "issues": [
            normalize_issue(issue) for issue in snapshot.get("issues", [])
        ],
    })


def issue_fingerprint(issue: dict) -> str:
    return sha({
        key: issue.get(key)
        for key in ("number", "title", "body", "state", "labels")
    })


def fetch_snapshot(attempts: int = 4) -> dict:
    if attempts < 2:
        raise ModelError("snapshot attempts must be at least two")
    previous = None
    for attempt in range(attempts):
        raw = run_gh(
            "issue", "list", "--label", "port", "--state", "all",
            "--limit", "10000",
            "--json", "id,number,title,body,state,labels,url",
        )
        by_number = {}
        conflicted = False
        for item in json.loads(raw or "[]"):
            issue = normalize_issue(item)
            prior = by_number.get(issue["number"])
            if prior is not None and issue_fingerprint(prior) != issue_fingerprint(issue):
                conflicted = True
                break
            by_number[issue["number"]] = issue
        snapshot = {
            "schema": 1,
            "fetched_at": int(time.time()),
            "issues": [by_number[number] for number in sorted(by_number)],
        }
        fingerprint = None if conflicted else snapshot_fingerprint(snapshot)
        if fingerprint is not None and fingerprint == previous:
            cached = load_cache(required=False)
            if (
                (cached and cached.get("migration_complete"))
                or migration_coverage_complete(snapshot)
            ):
                snapshot["migration_complete"] = True
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(json.dumps(snapshot, sort_keys=True, separators=(",", ":")))
            return snapshot
        previous = fingerprint
        if attempt + 1 < attempts:
            time.sleep(1)
    raise ModelError("GitHub issue listing did not stabilize")


def load_cache(*, required: bool = True, path: Path = CACHE) -> dict | None:
    if not path.exists():
        if required:
            raise ModelError(f"issue cache missing: {path}; run fetch first")
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ModelError(f"invalid issue cache: {path}: {exc}") from exc
    if data.get("schema") != 1 or not isinstance(data.get("issues"), list):
        raise ModelError(f"invalid issue cache schema: {path}")
    return data


def marker_for(work_id: str) -> str:
    return f'{MARKER_PREFIX}\n{{"work_id":{json.dumps(work_id)}}}\n-->'


def parse_marker(body: str) -> str | None:
    if MARKER_PREFIX not in body:
        return None
    matches = list(MARKER.finditer(body))
    if len(matches) != 1:
        raise ModelError("managed body has duplicate or malformed work markers")
    try:
        payload = json.loads(matches[0].group(1))
    except json.JSONDecodeError as exc:
        raise ModelError(f"malformed work marker: {exc}") from exc
    work_id = payload.get("work_id") if isinstance(payload, dict) else None
    if not isinstance(work_id, str) or not work_id.startswith("port:v1:"):
        raise ModelError("work marker has no valid port:v1 work_id")
    if set(payload) != {"work_id"}:
        raise ModelError("work marker contains unsupported fields")
    return work_id


def replace_generated(body: str, generated: str) -> str:
    begin = body.count(GEN_BEGIN)
    end = body.count(GEN_END)
    if begin != end or begin > 1:
        raise ModelError("generated issue block is duplicated or unterminated")
    block = f"{GEN_BEGIN}\n{generated.rstrip()}\n{GEN_END}"
    if begin == 0:
        return body.rstrip() + "\n\n" + block + "\n"
    start = body.index(GEN_BEGIN)
    finish = body.index(GEN_END, start) + len(GEN_END)
    return body[:start] + block + body[finish:]


def state_label(state: str) -> str:
    if state not in {
        "ready", "blocked", "active", "awaiting-gate", "failing",
        "complete", "excluded",
    }:
        raise ModelError(f"unknown lifecycle state: {state}")
    return f"port-{state}"


def generated_body(record: dict, packet: dict | None = None) -> str:
    blockers = list(record.get("blockers") or [])
    op = record.get("operational_blocker")
    if op:
        blockers.append(f"{op['reason']} (unblock: {op['unblock']})")
    state = record["state"]
    current = state
    if blockers:
        qualifier = "by" if state == "blocked" else "with recorded blockers"
        current += f" {qualifier} " + "; ".join(f"`{item}`" for item in blockers)
    packet_name = (packet or {}).get("id") or "unclaimed"
    source = record["source"]
    name = record["name"]
    return "\n".join((
        f"**Routine:** `{name}`",
        f"**Pret source:** `{source}:{record['line']}`",
        f"**Size / refs:** {record['size']} bytes / {record['refs']} refs",
        f"**Current state:** {current}",
        f"**Factory packet:** `{packet_name}`",
        "",
        "### Required deliverables",
        "- C implementation and declaration",
        "- probe adapter",
        "- schema-2 oracle cases covering zero, poisoned registers, and boundaries",
        "- recorded mutation that turns the oracle red",
        "- routine oracle PASS and release-gate verification",
        "",
        "### Verification",
        f"`just oracle-diff {name}`",
    ))


def desired_body(record: dict, existing: str = "", packet: dict | None = None) -> str:
    generated = generated_body(record, packet)
    marker = marker_for(record["work_id"])
    if existing:
        existing_marker = parse_marker(existing)
        if existing_marker and existing_marker != record["work_id"]:
            raise ModelError(f"body marker mismatch for {record['work_id']}")
        if existing_marker:
            legacy_generated = marker + "\n\n" + generated + "\n"
            body = marker if existing.strip() == legacy_generated.strip() else existing
        else:
            body = marker + "\n\n" + existing.lstrip()
        body = replace_generated(body, generated)
    else:
        body = replace_generated(marker, generated)
    if parse_marker(body) != record["work_id"]:
        raise ModelError(f"body marker mismatch for {record['work_id']}")
    return body


def desired_title(record: dict) -> str:
    return f"[T{record['tier']}] Port {record['name']}"


def desired_labels(record: dict, existing: list[str] | None = None) -> list[str]:
    labels = set(existing or [])
    labels.difference_update({"tier-1", "tier-2", "tier-3", "tier-4"} | LIFECYCLE)
    labels.update({"port", f"tier-{record['tier']}", state_label(record["state"])})
    return sorted(labels)


def load_report() -> dict:
    spec = importlib.util.spec_from_file_location("port_progress_report", REPORT_PATH)
    if spec is None or spec.loader is None:
        raise ModelError("cannot load progress report")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    inventory = module.load_inventory()
    routines = module.load_routines()[0]
    gate = module.load_gate()
    report = module.compute(inventory, routines, gate)
    active = {}
    queue = ROOT / ".factory" / "queue"
    active_states = {"pending", "translated", "verifying", "repair", "green"}
    for path in (sorted(queue.glob("*.json")) if queue.is_dir() else ()):
        packet = json.loads(path.read_text())
        if packet.get("state") not in active_states:
            continue
        for routine in packet.get("routines", []):
            name = routine["name"]
            work_id = routine.get("work_id")
            if not work_id:
                work_id = f"port:v1:{packet['file']}:{name}"
            if work_id in active:
                raise ModelError(
                    f"work ID {work_id} claimed by multiple active packets: "
                    f"{active[work_id]['id']} and {packet['id']}"
                )
            active[work_id] = {
                "id": packet["id"],
                "state": packet["state"],
                "issue_number": routine.get("issue_number"),
            }
    report["work_records"] = module.project_work_records(
        report["functions"], gate, active_packets=active,
    )
    return report


def record_map(report: dict) -> dict[str, dict]:
    records = report.get("work_records")
    if records is None:
        raise ModelError("progress report has no work-record projection")
    result = {}
    for record in records:
        work_id = record.get("work_id")
        if not work_id:
            continue
        if work_id in result:
            raise ModelError(f"duplicate desired work ID: {work_id}")
        result[work_id] = record
    return result


def indexed_issues(snapshot: dict) -> tuple[dict[str, dict], list[dict]]:
    by_work: dict[str, dict] = {}
    unmarked: list[dict] = []
    for raw in sorted(snapshot["issues"], key=lambda item: int(item["number"])):
        issue = normalize_issue(raw)
        work_id = parse_marker(issue["body"])
        if work_id is None:
            unmarked.append(issue)
            continue
        if work_id in by_work:
            raise ModelError(
                f"work ID {work_id} appears on issues "
                f"#{by_work[work_id]['number']} and #{issue['number']}"
            )
        by_work[work_id] = issue
    return by_work, unmarked


def migration_coverage_complete(snapshot: dict, report: dict | None = None) -> bool:
    report = report or load_report()
    records = record_map(report)
    managed, _ = indexed_issues(snapshot)
    desired = {
        work_id for work_id, record in records.items()
        if record["state"] != "excluded"
    }
    return bool(managed) and desired <= set(managed) <= set(records)



def action_for(record: dict, issue: dict | None) -> dict | None:
    if record["state"] == "excluded" and issue is None:
        return None
    body = desired_body(
        record, issue["body"] if issue else "", record.get("packet")
    )
    labels = desired_labels(record, issue.get("labels") if issue else None)
    title = desired_title(record)
    target_state = "closed" if record["state"] == "complete" else "open"
    if issue is None:
        return {
            "action": "create", "work_id": record["work_id"], "issue_number": None,
            "old_state": None, "desired_state": target_state,
            "reason": f"missing managed issue for {record['name']}",
            "title": title, "body": body, "labels": labels,
            "body_hash": sha(body), "labels_hash": sha(labels),
            "source_hash": None,
        }
    current_state = "closed" if issue["state"] == "closed" else "open"
    if (
        issue["title"] == title and issue["body"] == body
        and issue["labels"] == labels and current_state == target_state
    ):
        return None
    return {
        "action": "update", "work_id": record["work_id"],
        "issue_number": issue["number"], "old_state": current_state,
        "desired_state": target_state,
        "reason": f"reconcile {record['state']} state for {record['name']}",
        "title": title, "body": body, "labels": labels,
        "body_hash": sha(body), "labels_hash": sha(labels),
        "source_hash": issue_fingerprint(issue),
    }


def desired_plan(snapshot: dict, report: dict | None = None) -> dict:
    report = report or load_report()
    records = record_map(report)
    migrations = report.get("id_migrations") or {}
    by_work, unmarked = indexed_issues(snapshot)
    actions = []
    migrated_new: set[str] = set()
    for work_id in sorted(by_work):
        if work_id in records:
            continue
        new_id = migrations.get(work_id)
        if not new_id:
            raise ModelError(
                f"managed issue #{by_work[work_id]['number']} references "
                f"disappeared work ID {work_id}"
            )
        if new_id not in records or new_id in by_work:
            raise ModelError(f"invalid explicit work-ID migration {work_id} -> {new_id}")
        old_issue = by_work[work_id]
        record = records[new_id]
        migrated_body = MARKER.sub(
            marker_for(new_id), old_issue["body"], count=1,
        )
        migrated_issue = dict(old_issue, body=migrated_body)
        action = action_for(record, migrated_issue)
        if action:
            action["action"] = "migrate-id"
            action["work_id"] = new_id
            action["reason"] = f"explicit work-ID migration {work_id} -> {new_id}"
            action["source_hash"] = issue_fingerprint(old_issue)
            actions.append(action)
        migrated_new.add(new_id)
    for work_id in sorted(records):
        if work_id in migrated_new:
            continue
        action = action_for(records[work_id], by_work.get(work_id))
        if action:
            actions.append(action)
    return {
        "schema": 1,
        "source_snapshot": snapshot_fingerprint(snapshot),
        "actions": actions,
        "ignored_unmarked": [issue["number"] for issue in unmarked],
        "desired": len([r for r in records.values() if r["state"] != "excluded"]),
    }


def legacy_rows(issue: dict) -> tuple[str | None, list[str]]:
    source_match = SOURCE.search(issue["body"])
    source = source_match.group(1) if source_match else None
    names = []
    for line in issue["body"].splitlines():
        match = ROW.match(line.strip())
        if match and match.group(1) != "routine":
            names.append(match.group(1))
    return source, names


def migration_plan(snapshot: dict, report: dict | None = None) -> dict:
    report = report or load_report()
    records = record_map(report)
    marked, unmarked = indexed_issues(snapshot)
    actions = []
    adopted_ids: set[str] = set()
    replacement_ids: set[str] = set()
    classified = []
    for issue in unmarked:
        source, names = legacy_rows(issue)
        exact = [
            records[work_id] for work_id in sorted(records)
            if records[work_id]["source"] == source
            and records[work_id]["name"] in names
        ]
        exact_by_name = {record["name"]: record for record in exact}
        if (
            len(names) == 1 and len(exact) == 1
            and exact[0]["name"] == names[0]
        ):
            record = exact[0]
            body = desired_body(record, issue["body"], record.get("packet"))
            actions.append({
                "action": "adopt", "work_id": record["work_id"],
                "issue_number": issue["number"], "old_state": issue["state"],
                "desired_state": "closed" if record["state"] == "complete" else "open",
                "reason": "exact source and symbol match in explicit migration",
                "title": desired_title(record), "body": body,
                "labels": desired_labels(record, issue["labels"]),
                "body_hash": sha(body), "labels_hash": sha(
                    desired_labels(record, issue["labels"])),
                "source_hash": issue_fingerprint(issue),
            })
            adopted_ids.add(record["work_id"])
            classified.append({"issue": issue["number"], "classification": "adopt"})
        elif len(names) > 1 and len(exact_by_name) == len(names):
            created = []
            replacements = []
            for name in names:
                record = exact_by_name[name]
                existing = marked.get(record["work_id"])
                replacement = action_for(record, existing)
                if replacement is None and existing is None:
                    continue
                replacements.append(record["work_id"])
                replacement_ids.add(record["work_id"])
                if replacement is None:
                    continue
                if existing is None:
                    replacement["action"] = "create-replacement"
                    replacement["legacy_issue_number"] = issue["number"]
                    created.append(record["work_id"])
                actions.append(replacement)
            if replacements:
                actions.append({
                    "action": "supersede", "issue_number": issue["number"],
                    "replacement_work_ids": sorted(replacements),
                    "desired_state": "closed",
                    "labels": sorted(set(issue["labels"]) | {"superseded"}),
                    "reason": "aggregate replaced by one exact routine issue per row",
                    "source_hash": issue_fingerprint(issue),
                })
                classification = "split-aggregate"
            else:
                classification = "legacy-all-excluded"
            classified.append({
                "issue": issue["number"], "classification": classification,
                "source": source, "routines": names, "created": created,
            })
        else:
            classified.append({
                "issue": issue["number"],
                "classification": "legacy-unmatched-or-aggregate",
                "source": source, "routines": names,
            })
    normal = desired_plan(snapshot, report)
    actions.extend(
        action for action in normal["actions"]
        if action["work_id"] not in adopted_ids | replacement_ids
    )
    return {
        "schema": 1, "mode": "migrate",
        "source_snapshot": snapshot_fingerprint(snapshot), "actions": actions,
        "classified": classified, "ignored_unmarked": normal["ignored_unmarked"],
    }


def save_plan(plan: dict, path: Path = PLAN_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, sort_keys=True, indent=2) + "\n")


def run_graphql(query: str, variables: dict) -> dict:
    result = subprocess.run(
        ["gh", "api", "graphql", "--input", "-"],
        cwd=ROOT,
        text=True,
        input=json.dumps({"query": query, "variables": variables}),
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ModelError(result.stderr.strip() or "GitHub GraphQL request failed")
    payload = json.loads(result.stdout)
    if payload.get("errors"):
        messages = "; ".join(
            str(error.get("message", error)) for error in payload["errors"]
        )
        raise ModelError(f"GitHub GraphQL mutation failed: {messages}")
    return payload.get("data") or {}
def run_graphql_retryable(query: str, variables: dict, attempts: int = 4) -> dict:
    if attempts < 1:
        raise ModelError("GraphQL attempts must be positive")
    for attempt in range(attempts):
        try:
            return run_graphql(query, variables)
        except ModelError as exc:
            transient = re.search(r"\bHTTP (?:502|503|504)\b", str(exc))
            if not transient or attempt + 1 == attempts:
                raise
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable")




def action_key(action: dict) -> str:
    return sha(action)


def select_apply_batch(
    plan: dict,
    state: dict | None,
    current_snapshot: str,
    limit: int,
) -> tuple[list[dict], dict]:
    if not 1 <= limit <= 50:
        raise ModelError("apply limit must be between 1 and 50")
    plan_hash = sha(plan)
    if state is None:
        if current_snapshot != plan.get("source_snapshot"):
            raise ModelError("live issues changed since plan; re-run fetch and plan")
        state = {
            "schema": 1,
            "plan_hash": plan_hash,
            "expected_snapshot": current_snapshot,
            "completed": [],
        }
    elif (
        state.get("schema") != 1
        or state.get("plan_hash") != plan_hash
        or not isinstance(state.get("completed"), list)
    ):
        raise ModelError(
            "apply checkpoint belongs to another plan; remove it after review"
        )
    elif current_snapshot != state.get("expected_snapshot"):
        raise ModelError("live issues changed since the last apply checkpoint")
    keys = [action_key(action) for action in plan["actions"]]
    if len(keys) != len(set(keys)):
        raise ModelError("plan contains duplicate actions")
    completed = set(state["completed"])
    ordinary = [
        action for action, key in zip(plan["actions"], keys)
        if key not in completed and action["action"] != "supersede"
    ]
    pending = ordinary or [
        action for action, key in zip(plan["actions"], keys)
        if key not in completed
    ]
    return pending[:limit], state


def github_node_metadata(labels: set[str]) -> tuple[str, dict[str, str]]:
    ensure_labels(labels)
    repository = json.loads(run_gh("repo", "view", "--json", "id"))
    raw_labels = json.loads(
        run_gh("label", "list", "--limit", "1000", "--json", "id,name") or "[]"
    )
    label_ids = {label["name"]: label["id"] for label in raw_labels}
    missing = labels - set(label_ids)
    if missing:
        raise ModelError(f"GitHub labels missing after creation: {sorted(missing)}")
    return repository["id"], label_ids


def apply_graphql_batch(actions: list[dict], snapshot: dict) -> None:
    by_number = {
        int(issue["number"]): normalize_issue(issue)
        for issue in snapshot["issues"]
    }
    by_work, _ = indexed_issues(snapshot)
    labels = {
        label for action in actions for label in action.get("labels", [])
    }
    repository_id, label_ids = github_node_metadata(labels)
    declarations = []
    mutations = []
    variables = {}
    close_aliases = []
    for index, action in enumerate(actions):
        kind = action["action"]
        if kind in {"create", "create-replacement"}:
            if action["work_id"] in by_work:
                raise ModelError(
                    f"work ID {action['work_id']} already has a managed issue"
                )
            variable = f"v{index}"
            alias = f"a{index}"
            declarations.append(f"${variable}:CreateIssueInput!")
            variables[variable] = {
                "repositoryId": repository_id,
                "title": action["title"],
                "body": action["body"],
                "labelIds": [label_ids[label] for label in action["labels"]],
                "clientMutationId": action_key(action),
            }
            mutations.append(
                f"{alias}:createIssue(input:${variable})"
                "{issue{id number}}"
            )
            if action["desired_state"] == "closed":
                close_aliases.append(alias)
            continue
        number = action.get("issue_number")
        current = by_number.get(int(number)) if number else None
        if current is None or not current.get("id"):
            raise ModelError(f"issue #{number} missing a GraphQL node ID")
        if action.get("source_hash") and issue_fingerprint(current) != action["source_hash"]:
            raise ModelError(f"issue #{number} changed since plan; re-plan")
        if kind in {"update", "adopt", "migrate-id"}:
            variable = f"v{index}"
            declarations.append(f"${variable}:UpdateIssueInput!")
            variables[variable] = {
                "id": current["id"],
                "title": action["title"],
                "body": action["body"],
                "labelIds": [label_ids[label] for label in action["labels"]],
                "state": action["desired_state"].upper(),
                "clientMutationId": action_key(action),
            }
            mutations.append(
                f"a{index}:updateIssue(input:${variable})"
                "{issue{id number}}"
            )
            continue
        if kind != "supersede":
            raise ModelError(f"unsupported issue action: {kind}")
        replacement_numbers = []
        for work_id in action["replacement_work_ids"]:
            replacement = by_work.get(work_id)
            replacement_numbers.append(
                replacement["number"] if replacement else None
            )
        if any(value is None for value in replacement_numbers):
            raise ModelError(
                f"legacy issue #{number} has incomplete replacements; remains open"
            )
        update_variable = f"v{index}u"
        comment_variable = f"v{index}c"
        declarations.extend((
            f"${update_variable}:UpdateIssueInput!",
            f"${comment_variable}:AddCommentInput!",
        ))
        variables[update_variable] = {
            "id": current["id"],
            "labelIds": [label_ids[label] for label in action["labels"]],
            "state": "CLOSED",
            "clientMutationId": action_key(action),
        }
        links = " ".join(f"#{value}" for value in replacement_numbers)
        variables[comment_variable] = {
            "subjectId": current["id"],
            "body": f"Superseded by atomic routine issues: {links}.",
            "clientMutationId": action_key(action) + "-comment",
        }
        mutations.extend((
            f"a{index}u:updateIssue(input:${update_variable})"
            "{issue{id number}}",
            f"a{index}c:addComment(input:${comment_variable})"
            "{commentEdge{node{id}}}",
        ))
    query = (
        "mutation(" + ",".join(declarations) + "){"
        + " ".join(mutations) + "}"
    )
    retryable = all(
        action["action"] in {"update", "adopt", "migrate-id"}
        for action in actions
    )
    request = run_graphql_retryable if retryable else run_graphql
    data = request(query, variables)
    if close_aliases:
        snapshot = fetch_snapshot()
        by_work, _ = indexed_issues(snapshot)
        close_declarations = []
        close_mutations = []
        close_variables = {}
        for index, alias in enumerate(close_aliases):
            action = actions[int(alias[1:])]
            issue = (data.get(alias) or {}).get("issue") or {}
            if not issue.get("id"):
                issue = by_work.get(action["work_id"]) or {}
            if not issue.get("id"):
                raise ModelError(f"create mutation {alias} returned no issue ID")
            variable = f"c{index}"
            close_declarations.append(f"${variable}:UpdateIssueInput!")
            close_variables[variable] = {"id": issue["id"], "state": "CLOSED"}
            close_mutations.append(
                f"c{index}:updateIssue(input:${variable})"
                "{issue{id number}}"
            )
        close_query = (
            "mutation(" + ",".join(close_declarations) + "){"
            + " ".join(close_mutations) + "}"
        )
        run_graphql_retryable(close_query, close_variables)


def action_is_reflected(action: dict, snapshot: dict) -> bool:
    by_number = {
        int(issue["number"]): normalize_issue(issue)
        for issue in snapshot["issues"]
    }
    by_work, _ = indexed_issues(snapshot)
    issue = (
        by_work.get(action.get("work_id"))
        if action.get("work_id")
        else by_number.get(int(action["issue_number"]))
    )
    if issue is None:
        return False
    target_state = "closed" if action["desired_state"] == "closed" else "open"
    current_state = "closed" if issue["state"] == "closed" else "open"
    if action["action"] == "supersede":
        return current_state == target_state and issue["labels"] == action["labels"]
    return (
        issue["title"] == action["title"]
        and issue["body"] == action["body"]
        and issue["labels"] == action["labels"]
        and current_state == target_state
    )


def fetch_reflected_snapshot(actions: list[dict], attempts: int = 6) -> dict:
    if attempts < 1:
        raise ModelError("reflection attempts must be positive")
    for attempt in range(attempts):
        snapshot = fetch_snapshot()
        if all(action_is_reflected(action, snapshot) for action in actions):
            return snapshot
        if attempt + 1 < attempts:
            time.sleep(2)
    missing = [
        action.get("work_id") or f"issue #{action['issue_number']}"
        for action in actions if not action_is_reflected(action, snapshot)
    ]
    raise ModelError(
        "GitHub did not reflect applied actions before checkpoint: "
        + ", ".join(missing)
    )


def content_mutation_count(actions: list[dict]) -> int:
    count = 0
    for action in actions:
        if action["action"] == "supersede":
            count += 2
        elif (action["action"].startswith("create")
              and action["desired_state"] == "closed"):
            count += 2
        else:
            count += 1
    return count


def wait_for_content_budget(state: dict | None) -> None:
    next_apply_at = (state or {}).get("next_apply_at", 0)
    delay = next_apply_at - time.time()
    if delay > 0:
        print(f"issues: waiting {delay:.0f}s for GitHub content budget",
              file=sys.stderr)
        time.sleep(delay)


def apply_plan(
    plan: dict,
    *,
    limit: int = 25,
    batches: int = 1,
    state_path: Path = APPLY_STATE,
    content_interval: float = 8.0,
) -> dict:
    if batches < 1:
        raise ModelError("apply batches must be positive")
    if content_interval < 0:
        raise ModelError("content interval cannot be negative")
    if plan.get("mode") != "migrate":
        snapshot = load_cache(required=False)
        if not snapshot or not snapshot.get("migration_complete"):
            raise ModelError(
                "normal issue apply is disabled until explicit migration completes"
            )
    result = {"applied": 0, "remaining": len(plan["actions"]), "complete": False}
    for _ in range(batches):
        current = fetch_snapshot()
        state = json.loads(state_path.read_text()) if state_path.exists() else None
        batch, state = select_apply_batch(
            plan, state, snapshot_fingerprint(current), limit,
        )
        if not batch:
            result.update(remaining=0, complete=True)
            return result
        wait_for_content_budget(state)
        apply_graphql_batch(batch, current)
        refreshed = fetch_reflected_snapshot(batch)
        state["completed"].extend(action_key(action) for action in batch)
        state["expected_snapshot"] = snapshot_fingerprint(refreshed)
        state["updated_at"] = int(time.time())
        state["next_apply_at"] = (
            time.time() + content_mutation_count(batch) * content_interval
        )
        write_json(state_path, state)
        result["applied"] += len(batch)
        result["remaining"] = len(plan["actions"]) - len(state["completed"])
        if result["remaining"] == 0:
            result["complete"] = True
            return result
    return result

def mark_migration_complete(state_path: Path = APPLY_STATE) -> None:
    snapshot = fetch_snapshot()
    drift = desired_plan(snapshot)
    if drift["actions"]:
        raise ModelError(
            f"migration left {len(drift['actions'])} desired issue actions"
        )
    snapshot["migration_complete"] = True
    CACHE.write_text(json.dumps(snapshot, sort_keys=True, separators=(",", ":")))
    state_path.unlink(missing_ok=True)


def print_plan(plan: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(plan, sort_keys=True, separators=(",", ":")))
        return
    print(f"actions: {len(plan['actions'])}")
    for action in plan["actions"]:
        number = (
            f"#{action['issue_number']}" if action.get("issue_number") else "new"
        )
        work_id = action.get("work_id", "legacy aggregate")
        print(f"{action['action']:18} {number:8} {work_id} "
              f"{action.get('old_state')} -> {action.get('desired_state')}")
    if plan.get("ignored_unmarked"):
        print("ignored unmarked issues: " + ", ".join(
            f"#{number}" for number in plan["ignored_unmarked"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("fetch")
    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("--json", action="store_true")
    plan_parser.add_argument("--migrate", action="store_true")
    plan_parser.add_argument("--cache", type=Path, default=CACHE)
    plan_parser.add_argument("--report", type=Path)
    apply_parser = sub.add_parser("apply")
    apply_parser.add_argument("--plan", type=Path, default=PLAN_PATH)
    apply_parser.add_argument("--limit", type=int, default=25)
    apply_parser.add_argument("--batches", type=int, default=1)
    apply_parser.add_argument("--state", type=Path, default=APPLY_STATE)
    apply_parser.add_argument("--content-interval", type=float, default=8.0)
    apply_parser.add_argument("--require-complete", action="store_true")
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--cache", type=Path, default=CACHE)
    verify_parser.add_argument("--state", type=Path, default=APPLY_STATE)
    verify_parser.add_argument("--plan", type=Path, default=PLAN_PATH)
    verify_parser.add_argument("--live", action="store_true")
    verify_parser.add_argument("--complete-migration", action="store_true")
    migrate_parser = sub.add_parser("migrate")
    migrate_parser.add_argument("--json", action="store_true")
    migrate_parser.add_argument("--cache", type=Path, default=CACHE)
    migrate_parser.add_argument("--apply", action="store_true")
    migrate_parser.add_argument("--limit", type=int, default=25)
    migrate_parser.add_argument("--batches", type=int, default=1)
    migrate_parser.add_argument("--state", type=Path, default=APPLY_STATE)
    migrate_parser.add_argument("--content-interval", type=float, default=8.0)
    args = parser.parse_args()

    try:
        if args.command == "fetch":
            snapshot = fetch_snapshot()
            print(f"fetched {len(snapshot['issues'])} port-labeled issues into {CACHE}")
            return 0
        if args.command == "plan":
            snapshot = load_cache(path=args.cache)
            report = json.loads(args.report.read_text()) if args.report else None
            plan = (migration_plan if args.migrate else desired_plan)(snapshot, report)
            save_plan(plan)
            print_plan(plan, args.json)
            return 0
        if args.command == "apply":
            result = apply_plan(
                json.loads(args.plan.read_text()),
                limit=args.limit,
                batches=args.batches,
                state_path=args.state,
                content_interval=args.content_interval,
            )
            print(json.dumps(result, sort_keys=True))
            return 0 if result["complete"] or not args.require_complete else 3
        if args.command == "verify":
            snapshot = fetch_snapshot() if args.live else load_cache(path=args.cache)
            plan = desired_plan(snapshot)
            if plan["actions"]:
                print_plan(plan, False)
                return 1
            recorded = (
                json.loads(args.plan.read_text()) if args.plan.exists() else {}
            )
            if args.complete_migration and recorded.get("mode") != "migrate":
                raise ModelError(
                    "migration completion requires a recorded migration plan"
                )
            if recorded.get("mode") == "migrate":
                mark_migration_complete(args.state)
            else:
                args.state.unlink(missing_ok=True)
            print("issues: zero drift")
            return 0
        if args.command == "migrate":
            snapshot = load_cache(path=args.cache)
            plan = migration_plan(snapshot)
            save_plan(plan)
            if args.apply:
                result = apply_plan(
                    plan, limit=args.limit, batches=args.batches,
                    state_path=args.state,
                    content_interval=args.content_interval,
                )
                if result["complete"]:
                    mark_migration_complete(args.state)
                    print("migration: applied and verified")
                else:
                    print(json.dumps(result, sort_keys=True))
            else:
                print_plan(plan, args.json)
            return 0
    except (ModelError, OSError, json.JSONDecodeError) as exc:
        fail(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
