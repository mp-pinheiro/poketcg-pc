#!/usr/bin/env python3
"""Offline invariants for the managed issue model.

This is deliberately fixture-driven and network-free so pull-request CI can
prove the planner contract without GitHub credentials.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def routine(name: str, *, state: str = "ready") -> dict:
    return {
        "work_id": f"port:v1:src/home/demo.asm:{name}",
        "name": name,
        "source": "src/home/demo.asm",
        "line": 12,
        "size": 9,
        "refs": 1,
        "tier": 1,
        "excluded": False,
        "blockers": [],
        "operational_blocker": None,
        "state": state,
    }


def main() -> int:
    issues = load("issue_model", ROOT / "tools/factory/issues.py")
    report = {"work_records": [routine("Foo"), routine("Bar")]}
    work = report["work_records"][0]
    human = "# Human history\n\nKeep this paragraph.\n"
    rendered = issues.desired_body(work, human)
    assert issues.parse_marker(rendered) == work["work_id"]
    assert rendered.count(issues.GEN_BEGIN) == 1
    assert "Keep this paragraph." in rendered

    created_body = issues.desired_body(work)
    assert created_body.count(issues.GEN_BEGIN) == 1
    assert issues.desired_body(work, created_body) == created_body
    legacy_generated = (
        issues.marker_for(work["work_id"]) + "\n\n"
        + issues.generated_body(work) + "\n"
    )
    assert issues.desired_body(work, legacy_generated) == created_body
    unmarked = {
        "schema": 1,
        "fetched_at": 1,
        "issues": [{
            "number": 7, "title": "legacy", "body": "human",
            "state": "open", "labels": ["port", "epic"],
        }],
    }
    plan = issues.desired_plan(unmarked, report)
    assert len(plan["actions"]) == 2
    assert plan["ignored_unmarked"] == [7]
    assert all(action["action"] == "create" for action in plan["actions"])
    managed_foo = dict(
        unmarked["issues"][0],
        body=issues.marker_for(report["work_records"][0]["work_id"]),
    )
    managed_bar = dict(
        unmarked["issues"][0],
        number=8,
        body=issues.marker_for(report["work_records"][1]["work_id"]),
    )
    assert not issues.migration_coverage_complete(
        {"schema": 1, "issues": [managed_foo]}, report,
    )
    assert issues.migration_coverage_complete(
        {"schema": 1, "issues": [managed_foo, managed_bar]}, report,
    )


    stale = {
        "schema": 1,
        "complete": True,
        "commit": "tested",
        "inventory": {"routines": 2, "failures": 0, "primary_missing": 0},
        "routines": {"Foo": {"status": "pass"}},
    }
    report_module = load("progress_report", ROOT / "tools/progress/report.py")
    assert not report_module.gate_is_trusted(stale, revision="tested")
    complete_gate = dict(stale, routines={
        "Foo": {"status": "pass"},
        "Bar": {"status": "pass"},
    })
    assert report_module.gate_is_trusted(complete_gate, revision="tested")
    incomplete = dict(complete_gate, routines={"Foo": {"status": "pass"}})
    assert not report_module.gate_is_trusted(incomplete, revision="tested")
    same_name = [
        {
            "name": "Shared",
            "file": "src/home/one.asm",
            "line": 1,
            "size": 1,
            "refs": 0,
            "status": "todo",
            "blockers": [],
        },
        {
            "name": "Shared",
            "file": "src/home/two.asm",
            "line": 1,
            "size": 1,
            "refs": 0,
            "status": "todo",
            "blockers": [],
        },
    ]
    canonical = load("progress_for_projection", ROOT / "tools/progress/report.py")
    target = canonical.canonical_work_id("src/home/two.asm", "Shared")
    projected = canonical.project_work_records(
        same_name, None, active_packets={target: {"id": "packet-2", "state": "pending"}},
    )
    assert projected[0]["state"] == "ready"
    assert projected[1]["state"] == "active"

    duplicate = issues.marker_for(work["work_id"]) + issues.marker_for(work["work_id"])
    try:
        issues.parse_marker(duplicate)
    except issues.ModelError:
        pass
    else:
        raise AssertionError("duplicate marker was accepted")

    legacy = {
        "number": 8,
        "title": "old single routine",
        "body": (
            "**Pret source:** `poketcg/src/home/demo.asm`\n\n"
            "| routine | size | line | refs |\n"
            "|---------|------|------|------|\n"
            "| Foo | 9b | 12 | 1 |\n\nHuman text.\n"
        ),
        "state": "open",
        "labels": ["port", "tier-1"],
    }
    report["work_records"][0]["packet"] = {
        "id": "packet-foo", "state": "pending",
    }
    adopted = issues.migration_plan({"schema": 1, "issues": [legacy]}, report)
    assert adopted["actions"][0]["action"] == "adopt"
    assert "Human text." in adopted["actions"][0]["body"]
    assert "**Factory packet:** `packet-foo`" in adopted["actions"][0]["body"]
    report["work_records"][0]["state"] = "complete"

    aggregate = dict(legacy)
    aggregate["number"] = 9
    aggregate["body"] = aggregate["body"].replace(
        "| Foo | 9b | 12 | 1 |\n",
        "| Foo | 9b | 12 | 1 |\n| Bar | 9b | 12 | 1 |\n",
    )
    split = issues.migration_plan({"schema": 1, "issues": [aggregate]}, report)
    kinds = [action["action"] for action in split["actions"]]
    assert kinds.count("create-replacement") == 2
    assert kinds.count("supersede") == 1
    foo_create = next(
        action for action in split["actions"]
        if action.get("work_id") == report["work_records"][0]["work_id"]
    )
    partial = {
        "number": 10, "title": foo_create["title"],
        "body": foo_create["body"], "state": "open",
        "labels": foo_create["labels"],
    }
    resumed = issues.migration_plan(
        {"schema": 1, "issues": [aggregate, partial]}, report,
    )
    foo_actions = [
        action for action in resumed["actions"]
        if action.get("work_id") == report["work_records"][0]["work_id"]
    ]
    assert len(foo_actions) == 1
    assert foo_actions[0]["action"] == "update"
    assert foo_actions[0]["issue_number"] == 10
    excluded_foo = routine("Foo", state="excluded")
    excluded_bar = routine("Bar", state="excluded")
    excluded_foo["excluded"] = True
    excluded_bar["excluded"] = True
    excluded = issues.migration_plan(
        {"schema": 1, "issues": [aggregate]},
        {"work_records": [excluded_foo, excluded_bar]},
    )
    assert excluded["actions"] == []
    assert excluded["classified"][0]["classification"] == "legacy-all-excluded"
    resume_plan = {
        "source_snapshot": "snapshot-0",
        "actions": [
            {"action": "create", "work_id": "one"},
            {"action": "create", "work_id": "two"},
            {"action": "supersede", "issue_number": 9},
        ],
    }
    batch, checkpoint = issues.select_apply_batch(
        resume_plan, None, "snapshot-0", 1,
    )
    assert [action["work_id"] for action in batch] == ["one"]
    checkpoint["completed"].append(issues.action_key(batch[0]))
    checkpoint["expected_snapshot"] = "snapshot-1"
    resumed, checkpoint = issues.select_apply_batch(
        resume_plan, checkpoint, "snapshot-1", 1,
    )
    assert [action["work_id"] for action in resumed] == ["two"]
    checkpoint["completed"].append(issues.action_key(resumed[0]))
    checkpoint["expected_snapshot"] = "snapshot-2"
    final, _ = issues.select_apply_batch(
        resume_plan, checkpoint, "snapshot-2", 1,
    )
    assert final[0]["action"] == "supersede"
    try:
        issues.select_apply_batch(
            resume_plan, checkpoint, "unexpected-snapshot", 1,
        )
    except issues.ModelError:
        pass
    else:
        raise AssertionError("stale apply checkpoint was accepted")
    reflected_action = issues.action_for(routine("Reflected"), None)
    reflected_issue = {
        "id": "reflected-node", "number": 11,
        "title": reflected_action["title"], "body": reflected_action["body"],
        "state": "open", "labels": reflected_action["labels"], "url": "",
    }
    stale_snapshot = {"schema": 1, "issues": []}
    reflected_snapshot = {"schema": 1, "issues": [reflected_issue]}
    assert not issues.action_is_reflected(reflected_action, stale_snapshot)
    assert issues.action_is_reflected(reflected_action, reflected_snapshot)
    snapshots = iter((stale_snapshot, reflected_snapshot))
    original_fetch = issues.fetch_snapshot
    original_sleep = issues.time.sleep
    issues.fetch_snapshot = lambda: next(snapshots)
    issues.time.sleep = lambda _: None
    try:
        assert issues.fetch_reflected_snapshot(
            [reflected_action], attempts=2,
        ) == reflected_snapshot
        try:
            issues.fetch_reflected_snapshot([reflected_action], attempts=0)
        except issues.ModelError:
            pass
        else:
            raise AssertionError("zero reflection attempts were accepted")
    finally:
        issues.fetch_snapshot = original_fetch
        issues.time.sleep = original_sleep
    graphql_calls = []
    original_metadata = issues.github_node_metadata
    original_graphql = issues.run_graphql
    original_fetch = issues.fetch_snapshot
    issues.github_node_metadata = lambda labels: ("repo-node", {"port": "label-node"})
    issues.run_graphql = lambda query, variables: (
        graphql_calls.append((query, variables))
        or (
            {"a0": {"issue": {"id": "issue-node", "number": 10}}}
            if "createIssue" in query
            else {"c0": {"issue": {"id": "issue-node", "number": 10}}}
        )
    )
    issues.fetch_snapshot = lambda: {"schema": 1, "issues": []}
    try:
        issues.apply_graphql_batch(
            [{
                "action": "create",
                "work_id": "port:v1:src/home/demo.asm:Created",
                "title": "Created",
                "body": "body",
                "labels": ["port"],
                "desired_state": "closed",
            }],
            {"schema": 1, "issues": []},
        )
    finally:
        issues.github_node_metadata = original_metadata
        issues.run_graphql = original_graphql
        issues.fetch_snapshot = original_fetch
    assert len(graphql_calls) == 2
    assert "createIssue" in graphql_calls[0][0]
    assert graphql_calls[0][1]["v0"]["repositoryId"] == "repo-node"
    assert graphql_calls[0][1]["v0"]["labelIds"] == ["label-node"]
    assert graphql_calls[1][1]["c0"]["state"] == "CLOSED"
    graphql_calls.clear()
    created_work_id = "port:v1:src/home/demo.asm:Created"
    created_body = issues.marker_for(created_work_id) + "\n\nbody"
    reflected_create = {
        "id": "issue-node", "number": 10, "title": "Created",
        "body": created_body, "state": "open", "labels": ["port"], "url": "",
    }
    issues.github_node_metadata = lambda labels: ("repo-node", {"port": "label-node"})
    issues.run_graphql = lambda query, variables: (
        graphql_calls.append((query, variables))
        or (
            {"a0": {"issue": None}}
            if "createIssue" in query
            else {"c0": {"issue": {"id": "issue-node", "number": 10}}}
        )
    )
    issues.fetch_snapshot = lambda: {
        "schema": 1, "issues": [reflected_create],
    }
    try:
        issues.apply_graphql_batch(
            [{
                "action": "create",
                "work_id": created_work_id,
                "title": "Created", "body": created_body, "labels": ["port"],
                "desired_state": "closed",
            }],
            {"schema": 1, "issues": []},
        )
    finally:
        issues.github_node_metadata = original_metadata
        issues.run_graphql = original_graphql
        issues.fetch_snapshot = original_fetch
    assert graphql_calls[1][1]["c0"]["id"] == "issue-node"
    original_graphql = issues.run_graphql
    original_sleep = issues.time.sleep
    retry_calls = []
    retry_waits = []

    def flaky_graphql(query, variables):
        retry_calls.append((query, variables))
        if len(retry_calls) < 3:
            raise issues.ModelError("gh: HTTP 502")
        return {"ok": True}

    issues.run_graphql = flaky_graphql
    issues.time.sleep = retry_waits.append
    try:
        assert issues.run_graphql_retryable("mutation{}", {}) == {"ok": True}
    finally:
        issues.run_graphql = original_graphql
        issues.time.sleep = original_sleep
    assert len(retry_calls) == 3
    assert retry_waits == [1, 2]
    mutation_mix = [
        {"action": "supersede", "desired_state": "closed"},
        {"action": "create", "desired_state": "closed"},
        {"action": "create-replacement", "desired_state": "closed"},
        {"action": "create", "desired_state": "open"},
        {"action": "update", "desired_state": "open"},
    ]
    assert issues.content_mutation_count(mutation_mix) == 8
    original_time = issues.time.time
    original_sleep = issues.time.sleep
    waits = []
    issues.time.time = lambda: 10
    issues.time.sleep = waits.append
    try:
        issues.wait_for_content_budget({"next_apply_at": 12.5})
    finally:
        issues.time.time = original_time
        issues.time.sleep = original_sleep
    assert waits == [2.5]




    first = {"schema": 1, "fetched_at": 1, "issues": []}
    second = {"schema": 1, "fetched_at": 2, "issues": []}
    fetch_issue = {
        "id": "stable-node", "number": 12, "title": "Stable",
        "body": created_body, "state": "OPEN",
        "labels": [{"name": "port"}], "url": "",
    }
    duplicate_listing = json.dumps([fetch_issue, fetch_issue])
    original_run_gh = issues.run_gh
    original_cache = issues.CACHE
    original_sleep = issues.time.sleep
    issues.run_gh = lambda *args: duplicate_listing
    issues.CACHE = Path("/tmp/poketcg-issue-model-cache.json")
    issues.time.sleep = lambda _: None
    try:
        stable = issues.fetch_snapshot(attempts=2)
        assert len(stable["issues"]) == 1
        assert stable["issues"][0]["number"] == 12
    finally:
        issues.run_gh = original_run_gh
        issues.CACHE = original_cache
        issues.time.sleep = original_sleep
        Path("/tmp/poketcg-issue-model-cache.json").unlink(missing_ok=True)
    assert issues.snapshot_fingerprint(first) == issues.snapshot_fingerprint(second)
    print("issue model: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
