#!/usr/bin/env python3
"""Offline invariants for the managed issue model.

This is deliberately fixture-driven and network-free so pull-request CI can
prove the Forgejo cache and planner contracts without credentials.
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
    assert not issues.forgejo_coverage_complete(
        {"schema": 1, "issues": [managed_foo]}, report,
    )
    assert issues.forgejo_coverage_complete(
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

    normalized = issues.normalize_issue({
        "id": 12,
        "number": 12,
        "title": "Forgejo",
        "body": created_body,
        "state": "OPEN",
        "labels": [{"name": "port"}, {"name": "port-ready"}],
        "html_url": "https://forgejo.example/mpp/poketcg-pc/issues/12",
    })
    assert normalized == {
        "id": 12,
        "number": 12,
        "title": "Forgejo",
        "body": created_body,
        "state": "open",
        "labels": ["port", "port-ready"],
        "url": "https://forgejo.example/mpp/poketcg-pc/issues/12",
    }

    original_page_size = issues.PAGE_SIZE
    original_fetch_page = issues.fetch_page
    issues.PAGE_SIZE = 2
    page_calls = []
    pages = {
        1: [
            dict(normalized, number=1, id=1),
            dict(normalized, number=2, id=2),
        ],
        2: [dict(normalized, number=3, id=3)],
    }
    issues.fetch_page = lambda page: page_calls.append(page) or pages[page]
    try:
        fetched = issues.fetch_all_issues()
    finally:
        issues.PAGE_SIZE = original_page_size
        issues.fetch_page = original_fetch_page
    assert page_calls == [1, 2]
    assert [issue["number"] for issue in fetched] == [1, 2, 3]

    issues.PAGE_SIZE = 1
    conflict_pages = {
        1: [dict(normalized, number=1, title="first")],
        2: [dict(normalized, number=1, title="changed")],
        3: [],
    }
    issues.fetch_page = lambda page: conflict_pages[page]
    try:
        try:
            issues.fetch_all_issues()
        except issues.ModelError:
            pass
        else:
            raise AssertionError("conflicting Forgejo pages were accepted")
    finally:
        issues.PAGE_SIZE = original_page_size
        issues.fetch_page = original_fetch_page

    exact_foo = dict(
        normalized,
        number=7,
        body=issues.desired_body(report["work_records"][0]),
        title=issues.desired_title(report["work_records"][0]),
        labels=issues.desired_labels(report["work_records"][0]),
    )
    exact_bar = dict(
        normalized,
        number=8,
        body=issues.desired_body(report["work_records"][1]),
        title=issues.desired_title(report["work_records"][1]),
        labels=issues.desired_labels(report["work_records"][1]),
    )
    exact_snapshot = {
        "schema": 2,
        "backend": "forgejo",
        "repository": "mpp/poketcg-pc",
        "issues": [exact_foo, exact_bar],
    }
    assert issues.desired_plan(exact_snapshot, report)["actions"] == []

    cache_path = Path("/tmp/poketcg-forgejo-issue-cache.json")
    original_cache = issues.CACHE
    original_fetch_all = issues.fetch_all_issues
    original_coverage = issues.forgejo_coverage_complete
    original_sleep = issues.time.sleep
    fetches = []
    issues.CACHE = cache_path
    issues.fetch_all_issues = lambda: fetches.append(True) or [exact_foo, exact_bar]
    issues.forgejo_coverage_complete = lambda snapshot: True
    issues.time.sleep = lambda _: None
    try:
        stable = issues.fetch_snapshot(attempts=2)
        assert len(fetches) == 2
        assert stable["schema"] == 2
        assert stable["backend"] == "forgejo"
        assert "migration_complete" not in stable
        assert json.loads(cache_path.read_text())["issues"] == [exact_foo, exact_bar]

        cache_path.write_text('{"sentinel":true}')
        issues.forgejo_coverage_complete = lambda snapshot: False
        try:
            issues.fetch_snapshot(attempts=2)
        except issues.ModelError:
            pass
        else:
            raise AssertionError("incomplete Forgejo coverage was cached")
        assert json.loads(cache_path.read_text()) == {"sentinel": True}
    finally:
        issues.CACHE = original_cache
        issues.fetch_all_issues = original_fetch_all
        issues.forgejo_coverage_complete = original_coverage
        issues.time.sleep = original_sleep
        cache_path.unlink(missing_ok=True)

    for retired in (
        "run_gh",
        "run_graphql",
        "apply_graphql_batch",
        "apply_plan",
        "mark_migration_complete",
    ):
        assert not hasattr(issues, retired)
    common = load("factory_common_contract", ROOT / "tools/factory/common.py")
    common_cache = Path("/tmp/poketcg-common-issue-cache.json")
    original_common_cache = common.ISSUES_CACHE
    common.ISSUES_CACHE = common_cache
    try:
        common.write_json(common_cache, exact_snapshot)
        cached = common.issue_records(required=True)
        assert cached[work["work_id"]]["labels"] == ["port", "port-ready", "tier-1"]
        assert cached[work["work_id"]]["url"].endswith("/issues/12")
        stale = dict(exact_snapshot, schema=1)
        common.write_json(common_cache, stale)
        try:
            common.issue_records(required=True)
        except RuntimeError:
            pass
        else:
            raise AssertionError("retired issue cache schema was accepted")
    finally:
        common.ISSUES_CACHE = original_common_cache
        common_cache.unlink(missing_ok=True)
    print("issue model: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
