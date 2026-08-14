#!/usr/bin/env python3
"""Offline invariants for the managed issue model.

This is deliberately fixture-driven and network-free so pull-request CI can
prove the Forgejo cache and planner contracts without credentials.
"""

from __future__ import annotations
import importlib.util
import json
import os
import tempfile
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
    original_url = issues.FORGEJO_URL
    original_env = {
        key: os.environ.get(key)
        for key in issues.DOTENV_KEYS
    }
    try:
        with tempfile.TemporaryDirectory() as directory:
            dotenv_path = Path(directory) / ".env"
            dotenv_path.write_text(
                "# ignored\n"
                "POKETCG_FORGEJO_TOKEN='file-pat'\n"
                "export CF_ACCESS_CLIENT_ID=\"file-id\"\n"
                "CF_ACCESS_CLIENT_SECRET=file-secret=with-equals\n"
                "UNRELATED=ignored\n"
            )
            for key in issues.DOTENV_KEYS:
                os.environ.pop(key, None)
            values = issues.dotenv_credentials(dotenv_path)
            assert values == {
                "POKETCG_FORGEJO_TOKEN": "file-pat",
                "CF_ACCESS_CLIENT_ID": "file-id",
                "CF_ACCESS_CLIENT_SECRET": "file-secret=with-equals",
            }
            assert issues.forgejo_authorization(dotenv=values) == "token file-pat"
            assert issues.cloudflare_access_headers(values) == {
                "CF-Access-Client-Id": "file-id",
                "CF-Access-Client-Secret": "file-secret=with-equals",
            }
            os.environ["POKETCG_FORGEJO_TOKEN"] = "process-pat"
            os.environ["CF_ACCESS_CLIENT_ID"] = "process-id"
            os.environ["CF_ACCESS_CLIENT_SECRET"] = "process-secret"
            assert issues.forgejo_authorization(dotenv=values) == "token process-pat"
            assert issues.cloudflare_access_headers(values) == {
                "CF-Access-Client-Id": "process-id",
                "CF-Access-Client-Secret": "process-secret",
            }
            os.environ.pop("CF_ACCESS_CLIENT_SECRET")
            try:
                issues.cloudflare_access_headers({
                    "CF_ACCESS_CLIENT_ID": "file-id",
                })
            except issues.ModelError as exc:
                assert str(exc) == (
                    "CF_ACCESS_CLIENT_ID and CF_ACCESS_CLIENT_SECRET "
                    "must be set together"
                )
            else:
                raise AssertionError("partial Cloudflare credentials accepted")
            os.environ.pop("CF_ACCESS_CLIENT_ID")
            try:
                issues.cloudflare_access_headers({
                    "CF_ACCESS_CLIENT_SECRET": "file-secret",
                })
            except issues.ModelError as exc:
                assert str(exc) == (
                    "CF_ACCESS_CLIENT_ID and CF_ACCESS_CLIENT_SECRET "
                    "must be set together"
                )
            else:
                raise AssertionError("partial Cloudflare credentials accepted")
            for key in issues.DOTENV_KEYS:
                os.environ.pop(key, None)
            issues.FORGEJO_URL = "https://forgejo.yfrit.com"
            try:
                issues.cloudflare_access_headers({})
            except issues.ModelError as exc:
                assert str(exc) == (
                    "CF_ACCESS_CLIENT_ID and CF_ACCESS_CLIENT_SECRET are "
                    "required for forgejo.yfrit.com"
                )
            else:
                raise AssertionError("production endpoint allowed missing Access credentials")
    finally:
        issues.FORGEJO_URL = original_url
        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

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

    packet = load("factory_packet", ROOT / "tools/factory/packet.py")

    def migration_packet(packet_id, state, names, identities=None):
        identities = identities or {}
        return {
            "id": packet_id,
            "basename": "demo",
            "file": "src/home/demo.asm",
            "state": state,
            "routines": [
                dict({"name": name, "size": 1}, **identities.get(name, {}))
                for name in names
            ],
        }

    def must_fail(call, label):
        try:
            call()
        except (RuntimeError, ValueError):
            return
        raise AssertionError(f"{label} was accepted")

    foo_id = "port:v1:src/home/demo.asm:Foo"
    bar_id = "port:v1:src/home/demo.asm:Bar"
    managed = {
        foo_id: {"issue_number": 101},
        bar_id: {"issue_number": 102},
    }
    pending = migration_packet("pending", "pending", ["Foo"])
    terminal = migration_packet("terminal", "landed", ["Foo"])
    matching = migration_packet(
        "matching", "green", ["Bar"],
        {"Bar": {"work_id": bar_id, "issue_number": 102}},
    )
    original_pending = json.loads(json.dumps(pending))
    migrated, migration_counts = packet.plan_work_id_migration(
        [pending, terminal, matching], managed,
    )
    assert pending == original_pending
    assert migration_counts == {
        "packets": 3,
        "routines": 3,
        "changed_packets": 2,
        "changed_routines": 2,
    }
    assert migrated[0]["routines"][0]["work_id"] == foo_id
    assert migrated[0]["routines"][0]["issue_number"] == 101
    assert migrated[1]["routines"][0]["work_id"] == foo_id
    assert migrated[2] == matching
    second, second_counts = packet.plan_work_id_migration(migrated, managed)
    assert second == migrated
    assert second_counts["changed_packets"] == 0
    assert second_counts["changed_routines"] == 0
    must_fail(
        lambda: packet.plan_work_id_migration(
            [migration_packet(
                "mismatch", "pending", ["Foo"],
                {"Foo": {"work_id": "port:v1:wrong", "issue_number": 101}},
            )],
            managed,
        ),
        "mismatched work ID",
    )
    must_fail(
        lambda: packet.plan_work_id_migration(
            [migration_packet(
                "mismatch-number", "pending", ["Foo"],
                {"Foo": {"work_id": foo_id, "issue_number": 999}},
            )],
            managed,
        ),
        "mismatched issue number",
    )
    must_fail(
        lambda: packet.plan_work_id_migration(
            [migration_packet("unresolved", "pending", ["Missing"])],
            managed,
        ),
        "unresolved work ID",
    )
    must_fail(
        lambda: packet.plan_work_id_migration(
            [
                migration_packet("active-a", "pending", ["Foo"]),
                migration_packet("active-b", "green", ["Foo"]),
            ],
            managed,
        ),
        "duplicate active claim",
    )

    def run_application_case(failure=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            queue = root / "queue"
            bundles = root / "bundles"
            backups = root / "backups"
            cache = root / "issues-cache.json"
            queue.mkdir()
            bundles.mkdir()
            p1 = migration_packet("p1", "pending", ["Foo"])
            p2 = migration_packet(
                "p2", "landed", ["Bar"],
                {"Bar": {"work_id": bar_id, "issue_number": 102}},
            )
            p1_raw = json.dumps(p1, indent=4).encode() + b"\n"
            p2_raw = json.dumps(p2, indent=1, sort_keys=True).encode() + b"\n"
            (queue / "p1.json").write_bytes(p1_raw)
            (queue / "p2.json").write_bytes(p2_raw)
            existing_identity = packet.common.packet_identity(p2)
            existing_raw = (
                json.dumps(existing_identity, indent=3).encode() + b"\n"
            )
            (bundles / "p1").mkdir()
            (bundles / "p2").mkdir()
            existing_metadata = bundles / "p2" / "packet.json"
            existing_metadata.write_bytes(existing_raw)
            (bundles / "p2" / "kept.bin").write_bytes(b"keep")
            cache_issues = []
            for number, work_id in ((101, foo_id), (102, bar_id)):
                marker = (
                    "<!-- poketcg-port-work:v1\n"
                    + json.dumps({"work_id": work_id})
                    + "\n-->"
                )
                cache_issues.append({
                    "number": number,
                    "body": marker,
                    "state": "open",
                    "labels": [],
                })
            packet.common.write_json(cache, {
                "schema": 2,
                "backend": "forgejo",
                "repository": "mpp/poketcg-pc",
                "issues": cache_issues,
            })
            old = (
                packet.QUEUE, packet.BUNDLES, packet.BACKUPS,
                packet.common.ISSUES_CACHE, packet.write_json,
                packet.read_json,
            )
            missing_metadata = bundles / "p1" / "packet.json"
            try:
                packet.QUEUE = queue
                packet.BUNDLES = bundles
                packet.BACKUPS = backups
                packet.common.ISSUES_CACHE = cache
                original_writer = packet.write_json
                original_reader = packet.read_json
                if failure in {"queue", "metadata"}:
                    def failing_writer(path, data):
                        if failure == "queue" and path == queue / "p1.json":
                            raise OSError("injected queue write failure")
                        if failure == "metadata" and path == missing_metadata:
                            raise OSError("injected metadata write failure")
                        return original_writer(path, data)
                    packet.write_json = failing_writer
                if failure == "readback":
                    def failing_reader(path):
                        if path == queue / "p1.json":
                            raise OSError("injected readback failure")
                        return original_reader(path)
                    packet.read_json = failing_reader
                before_metadata = existing_metadata.read_bytes()
                if failure is None:
                    result = packet.run_work_id_migration(apply=True)
                    assert result["changed_packets"] == 1
                    assert result["changed_routines"] == 1
                    assert result["changed_bundle_metadata"] == 1
                    assert json.loads((queue / "p1.json").read_bytes())[
                        "routines"
                    ][0]["issue_number"] == 101
                    assert json.loads(missing_metadata.read_bytes()) == (
                        packet.common.packet_identity(
                            json.loads((queue / "p1.json").read_bytes())
                        )
                    )
                    assert existing_metadata.read_bytes() == before_metadata
                    assert (bundles / "p2" / "kept.bin").read_bytes() == b"keep"
                    manifest = json.loads(
                        (Path(result["backup"]) / "manifest.json").read_bytes()
                    )
                    assert manifest["queue"] == ["queue/p1.json"]
                    assert manifest["bundle_metadata"] == [
                        "bundles/p2/packet.json"
                    ]
                    assert manifest["absent_bundle_metadata"] == ["p1/packet.json"]
                else:
                    before_queue = (queue / "p1.json").read_bytes()
                    try:
                        packet.run_work_id_migration(apply=True)
                    except RuntimeError as exc:
                        assert "backup at" in str(exc)
                    else:
                        raise AssertionError(f"{failure} failure was accepted")
                    assert (queue / "p1.json").read_bytes() == before_queue
                    assert not missing_metadata.exists()
                    assert existing_metadata.read_bytes() == before_metadata
            finally:
                (
                    packet.QUEUE, packet.BUNDLES, packet.BACKUPS,
                    packet.common.ISSUES_CACHE, packet.write_json,
                    packet.read_json,
                ) = old

    run_application_case()
    for injected_failure in ("queue", "metadata", "readback"):
        run_application_case(injected_failure)

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
