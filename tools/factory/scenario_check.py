#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import threading
from datetime import UTC, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import parse_qs, urlparse

import cache
import common
import control
import forecast
import forgejo
import integrate
import ledger
import migration
import scheduler
import workers


def comment(identifier: int, event: ledger.FactoryEvent, second: int) -> dict:
    return {
        "id": identifier,
        "body": event.comment_body(),
        "created_at": (datetime(2026, 8, 18, tzinfo=UTC) + timedelta(seconds=second)).isoformat(),
        "updated_at": (datetime(2026, 8, 18, tzinfo=UTC) + timedelta(seconds=second)).isoformat(),
        "author": "mpp",
    }


def make_event(
    kind: str,
    work_id: str | None,
    parent: tuple[int | None, str | None],
    intent: str,
    payload: dict,
) -> ledger.FactoryEvent:
    return ledger.FactoryEvent.create(
        kind=kind,
        run_id="run-1",
        work_id=work_id,
        attempt_id="attempt-1" if work_id else None,
        parent_comment_id=parent[0],
        parent_event_sha256=parent[1],
        base_revision="a" * 40,
        intent_sha256=intent,
        emitted_at="2026-08-18T00:00:00+00:00",
        payload=payload,
    )


def work_issue() -> dict:
    return {
        "number": 101,
        "body": "<!-- poketcg-port-work:v2 {\"work_id\":\"port:v1:src/home/demo.asm:Demo\"} -->\n\n<!-- poketcg-port-generated:begin -->\nDemo\n<!-- poketcg-port-generated:end -->\n",
        "state": "open",
        "labels": ["port/ready"],
    }


def check_ledger() -> None:
    issue = work_issue()
    intent = ledger.intent_sha256(issue, [], [])
    root = make_event(
        "migrated",
        "port:v1:src/home/demo.asm:Demo",
        (None, None),
        intent,
        {
            "state": "ready",
            "source_revision": "a" * 40,
            "publication_revision": "",
            "gate_sha256": "",
            "legacy_history_sha256": "b" * 64,
            "landed_at": None,
            "exclusion_reason": None,
        },
    )
    claim_a = make_event(
        "claim",
        root.work_id,
        (10, root.event_sha256),
        intent,
        {
            "lease_seconds": 600,
            "packet_sha256": "c" * 64,
            "model_route": "smol",
            "owned_paths_sha256": "d" * 64,
        },
    )
    claim_b = make_event(
        "claim",
        root.work_id,
        (10, root.event_sha256),
        intent,
        {
            "lease_seconds": 600,
            "packet_sha256": "e" * 64,
            "model_route": "smol",
            "owned_paths_sha256": "f" * 64,
        },
    )
    view = ledger.reduce_work(
        issue,
        [comment(10, root, 0), comment(11, claim_a, 1), comment(12, claim_b, 1)],
        [],
        now=datetime(2026, 8, 18, 0, 2, tzinfo=UTC),
        authorized_authors={"mpp"},
    )
    assert view.state == "running"
    assert view.claim_comment_id == 11
    assert any("losing concurrent branch" in item for item in view.ignored)
    result = make_event(
        "attempt-result",
        root.work_id,
        (11, claim_a.event_sha256),
        intent,
        {
            "claim_comment_id": 11,
            "outcome": "productive",
            "verdict": {"status": "green"},
            "artifact_sha256": "1" * 64,
            "next_wake_at": None,
        },
    )
    view = ledger.reduce_work(
        issue,
        [comment(10, root, 0), comment(11, claim_a, 1), comment(13, result, 2)],
        [],
        now=datetime(2026, 8, 18, 0, 2, tzinfo=UTC),
        authorized_authors={"mpp"},
        artifact_exists=lambda value: value == "1" * 64,
    )
    assert view.state == "integrating"
    assert view.productive_result_comment_id == 13
    landed = make_event(
        "landed",
        root.work_id,
        (13, result.event_sha256),
        intent,
        {
            "batch_id": "batch-1",
            "attempt_result_comment_id": 13,
            "source_revision": "a" * 40,
            "publication_revision": "b" * 40,
            "gate_sha256": "2" * 64,
            "progress_sha256": "3" * 64,
        },
    )
    view = ledger.reduce_work(
        issue,
        [comment(10, root, 0), comment(11, claim_a, 1), comment(13, result, 2), comment(14, landed, 3)],
        [],
        now=datetime(2026, 8, 18, 0, 4, tzinfo=UTC),
        authorized_authors={"mpp"},
        artifact_exists=lambda value: value == "1" * 64,
    )
    assert view.state == "done"


def check_first_claim_election() -> None:
    issue = work_issue()
    intent = ledger.intent_sha256(issue, [], [])
    root = make_event(
        "migrated",
        "port:v1:src/home/demo.asm:Demo",
        (None, None),
        intent,
        {
            "state": "ready",
            "source_revision": "a" * 40,
            "publication_revision": "",
            "gate_sha256": "b" * 64,
            "legacy_history_sha256": None,
            "landed_at": None,
            "exclusion_reason": None,
        },
    )
    claim = make_event(
        "claim",
        root.work_id,
        (10, root.event_sha256),
        intent,
        {
            "lease_seconds": 900,
            "packet_sha256": "c" * 64,
            "model_route": "smol",
            "owned_paths_sha256": "d" * 64,
        },
    )
    comments = [comment(10, root, 0), comment(11, claim, 1)]
    winner = ledger.elect_lease(
        comments,
        work_id=root.work_id,
        now=datetime(2026, 8, 18, 0, 2, tzinfo=UTC),
    )
    assert winner is not None
    assert winner.comment_id == 11
    result = make_event(
        "attempt-result",
        root.work_id,
        (11, claim.event_sha256),
        intent,
        {
            "claim_comment_id": 11,
            "outcome": "diagnostic",
            "verdict": {"status": "red", "fingerprint": "x"},
            "artifact_sha256": None,
            "next_wake_at": None,
        },
    )
    released = ledger.elect_lease(
        [*comments, comment(12, result, 2)],
        work_id=root.work_id,
        now=datetime(2026, 8, 18, 0, 3, tzinfo=UTC),
    )
    assert released is None


def check_lease_covers_deadline() -> None:
    for route in ("smol", "task"):
        lease = control._lease_seconds({"model_route": route})
        assert lease > control._hard_deadline(route)
        assert lease > control._soft_deadline(route)
        clipped = control._lease_seconds({"model_route": route, "lease_seconds": 60})
        assert clipped == lease
        extended = control._lease_seconds({"model_route": route, "lease_seconds": 7000})
        assert extended == 7000
    assert control._lease_seconds({"model_route": "task", "lease_seconds": 99999}) == 7200


def check_dirty_guard() -> None:
    summary = (
        "M src/home/sgb.c\n"
        "M tools/factory/control.py\n"
        "A src/probe/sgb.c\n"
        "D tests/cases/sgb.py\n"
        "M site/data/progress.json\n"
        "A tools/oracle/mutation_receipts/SendSGB.json\n"
        "?? untracked-noise\n"
    )
    assert control.owned_dirty_paths(summary) == [
        "src/home/sgb.c",
        "src/probe/sgb.c",
        "tests/cases/sgb.py",
        "tools/oracle/mutation_receipts/SendSGB.json",
    ]
    assert control.owned_dirty_paths("") == []
    assert control.owned_dirty_paths("M tools/factory/ledger.py") == []


def check_policy_veto_routing() -> None:
    def work(number: int, *, state: str, dependencies: tuple[int, ...] = ()) -> scheduler.FactoryWork:
        return scheduler.FactoryWork(
            issue_number=number,
            work_id=f"port:v1:src/home/demo{number}.asm:Demo{number}",
            source=f"src/home/demo{number}.asm",
            basenames=(f"demo{number}",),
            owned_paths=(f"src/home/demo{number}.c",),
            size=20,
            tier=1,
            priority="normal",
            state=state,
            dependencies=dependencies,
            ready_at=datetime(2026, 8, 18, tzinfo=UTC),
        )

    vetoed = work(201, state="blocked")
    waiting_on_callee = work(202, state="blocked", dependencies=(203,))
    callee = work(203, state="ready")
    planned = scheduler.plan(
        scheduler.FactorySnapshot(sha256="f" * 64, works=(vetoed, waiting_on_callee)),
        scheduler.Capacity(job_slots=4),
        datetime(2026, 8, 18, 1, tzinfo=UTC),
    )
    assert planned.assignments == ()
    assert planned.blocker_review == (201,)
    assert planned.dependency_analysis == ()
    dependency_only = scheduler.plan(
        scheduler.FactorySnapshot(sha256="e" * 64, works=(waiting_on_callee, callee)),
        scheduler.Capacity(job_slots=4),
        datetime(2026, 8, 18, 1, tzinfo=UTC),
    )
    assert [item.issue_number for item in dependency_only.assignments] == [203]
    assert migration.state_for({"status": "todo", "tier": 1, "operational_blocker": {"reason": "veto"}}) == "blocked"
    assert migration.state_for({"status": "todo", "tier": 1}) == "ready"
    assert "attention/human" in migration.labels_for(
        {"tier": 1, "operational_blocker": {"reason": "veto"}}, "blocked",
    )
    assert "attention/human" not in migration.labels_for({"tier": 1}, "ready")


def check_cohort_state() -> None:
    def function(name: str, *, blockers: tuple[str, ...] = (), veto: bool = False) -> dict:
        value = {
            "name": name,
            "file": "src/home/cycle.asm",
            "status": "todo",
            "ready": False,
            "size": 20,
            "line": 1,
            "refs": 1,
            "tier": 1,
            "work_id": f"port:v1:src/home/cycle.asm:{name}",
            "blockers": list(blockers),
        }
        if veto:
            value["operational_blocker"] = {"reason": "veto", "unblock": "clear it"}
        return value

    cycle = [function("A", blockers=("B",)), function("B", blockers=("A",))]
    actions = migration._cohort_actions(cycle)
    assert len(actions) == 1
    assert actions[0]["state"] == "ready"
    assert "attention/human" not in actions[0]["labels"]
    with_external = [function("A", blockers=("B", "Outside")), function("B", blockers=("A",)), function("Outside")]
    external_actions = migration._cohort_actions(with_external)
    assert [action["state"] for action in external_actions] == ["blocked"]
    vetoed = [function("A", blockers=("B",), veto=True), function("B", blockers=("A",))]
    vetoed_actions = migration._cohort_actions(vetoed)
    assert vetoed_actions[0]["state"] == "blocked"
    assert "attention/human" in vetoed_actions[0]["labels"]



def check_recovery_ladder() -> None:
    issue = work_issue()
    intent = ledger.intent_sha256(issue, [], [])
    root = make_event(
        "migrated",
        "port:v1:src/home/demo.asm:Demo",
        (None, None),
        intent,
        {
            "state": "ready",
            "source_revision": "a" * 40,
            "publication_revision": "",
            "gate_sha256": "b" * 64,
            "legacy_history_sha256": None,
            "landed_at": None,
            "exclusion_reason": None,
        },
    )
    comments = [comment(10, root, 0)]
    parent = (10, root.event_sha256)
    for index in range(3):
        diagnostic = make_event(
            "attempt-result",
            root.work_id,
            parent,
            intent,
            {
                "claim_comment_id": 10,
                "outcome": "diagnostic",
                "verdict": {"status": "red", "fingerprint": "stuck"},
                "artifact_sha256": None,
                "next_wake_at": None,
            },
        )
        comments.append(comment(20 + index, diagnostic, 2 + index))
        parent = (20 + index, diagnostic.event_sha256)
    view = ledger.reduce_work(
        issue,
        comments,
        [],
        now=datetime(2026, 8, 18, 1, tzinfo=UTC),
        authorized_authors={"mpp"},
    )
    assert view.state == "recovery"
    assert view.diagnostic_count == 3
    assert view.repeat_fingerprints == 2
    assert scheduler.recovery_tier(1, 0) == 1
    assert scheduler.recovery_tier(2, 0) == 2
    assert scheduler.recovery_tier(1, 2) == 3
    assert scheduler.recovery_tier(view.diagnostic_count, view.repeat_fingerprints) == 3

    def stuck_work(tier: int, *, escalated: bool = False) -> scheduler.FactoryWork:
        return scheduler.FactoryWork(
            issue_number=101,
            work_id=root.work_id or "",
            source="src/home/demo.asm",
            basenames=("demo",),
            owned_paths=("src/home/demo.c",),
            size=20,
            tier=1,
            priority="normal",
            state="recovery",
            ready_at=datetime(2026, 8, 18, tzinfo=UTC),
            recovery_tier=tier,
            escalated=escalated,
        )

    routes = {}
    for tier in (1, 2, 3):
        planned = scheduler.plan(
            scheduler.FactorySnapshot(sha256="c" * 64, works=(stuck_work(tier),)),
            scheduler.Capacity(job_slots=4),
            datetime(2026, 8, 18, 1, tzinfo=UTC),
        )
        assignment = planned.assignments[0]
        routes[tier] = (assignment.model_route, assignment.kind)
    assert routes[1] == ("smol", "completion")
    assert routes[2] == ("task", "task")
    assert routes[3] == ("task", "repair")
    exhausted = scheduler.plan(
        scheduler.FactorySnapshot(
            sha256="d" * 64,
            works=(stuck_work(scheduler.ESCALATION_DIAGNOSTICS, escalated=True),),
        ),
        scheduler.Capacity(job_slots=4),
        datetime(2026, 8, 18, 1, tzinfo=UTC),
    )
    assert exhausted.assignments == ()
    assert exhausted.blocker_review == (101,)
    block = make_event(
        "block",
        root.work_id,
        parent,
        intent,
        {
            "reason": "recovery-exhausted",
            "unblock": "4 diagnostics, verdict fingerprint stuck; fix the cause, then post /factory unblock",
            "dependency_issue_numbers": [],
        },
    )
    blocked_view = ledger.reduce_work(
        issue,
        [*comments, comment(30, block, 6)],
        [],
        now=datetime(2026, 8, 18, 1, tzinfo=UTC),
        authorized_authors={"mpp"},
    )
    assert blocked_view.state == "blocked"
    assert blocked_view.escalated
    unblock = make_event(
        "unblock",
        root.work_id,
        (30, block.event_sha256),
        intent,
        {"block_comment_id": 30, "reason": "human cleared the blocker"},
    )
    resumed = ledger.reduce_work(
        issue,
        [*comments, comment(30, block, 6), comment(31, unblock, 7)],
        [],
        now=datetime(2026, 8, 18, 1, tzinfo=UTC),
        authorized_authors={"mpp"},
    )
    assert resumed.state == "recovery"
    assert not resumed.escalated
    assert resumed.diagnostic_count == 0


def check_control() -> None:
    issue = {
        "number": 1,
        "body": "<!-- poketcg-factory-control:v1 {\"repository\":\"mpp/poketcg-pc\"} -->",
    }
    event = make_event(
        "run-claim",
        None,
        (None, None),
        "0" * 64,
        {"runner_instance": "scenario", "lease_seconds": 600},
    )
    view = ledger.reduce_control(
        issue,
        [comment(1, event, 0)],
        now=datetime(2026, 8, 18, 0, 1, tzinfo=UTC),
    )
    assert view.active
    assert view.claim_comment_id == 1


def check_planner() -> None:
    ready = scheduler.FactoryWork(
        issue_number=101,
        work_id="port:v1:src/home/demo.asm:Demo",
        source="src/home/demo.asm",
        basenames=("demo",),
        owned_paths=("src/home/demo.c",),
        size=20,
        tier=1,
        priority="normal",
        state="ready",
        ready_at=datetime(2026, 8, 18, tzinfo=UTC),
    )
    blocked = scheduler.FactoryWork(
        issue_number=102,
        work_id="port:v1:src/home/next.asm:Next",
        source="src/home/next.asm",
        basenames=("next",),
        owned_paths=("src/home/next.c",),
        size=20,
        tier=1,
        priority="high",
        state="blocked",
        dependencies=(101,),
    )
    snapshot = scheduler.FactorySnapshot(
        sha256=hashlib.sha256(b"scenario").hexdigest(),
        works=(ready, blocked),
    )
    planned = scheduler.plan(
        snapshot,
        scheduler.Capacity(job_slots=4),
        datetime(2026, 8, 18, tzinfo=UTC),
    )
    assert [assignment.issue_number for assignment in planned.assignments] == [101]
    assert planned.assignments[0].model_route == "smol"


def check_forgejo_client() -> None:
    state = {
        "issues": [{
            "id": 101,
            "number": 101,
            "title": "Demo",
            "body": work_issue()["body"],
            "state": "open",
            "labels": [{"id": 1, "name": "port/ready"}],
            "created_at": "2026-08-18T00:00:00Z",
            "updated_at": "2026-08-18T00:00:00Z",
            "user": {"login": "mpp"},
        }],
        "comments": [],
    }

    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, payload: object) -> None:
            raw = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path.endswith("/issues"):
                self._send(200, state["issues"])
                return
            if path.endswith("/issues/101/comments"):
                self._send(200, state["comments"])
                return
            if path.endswith("/issues/101/dependencies"):
                self._send(200, [])
                return
            if path.endswith("/labels"):
                self._send(200, [{"id": 1, "name": "port/ready"}])
                return
            if path.endswith("/issues/101"):
                self._send(200, state["issues"][0])
                return
            self._send(404, {})

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            raw = self.rfile.read(int(self.headers.get("Content-Length", "0")))
            payload = json.loads(raw or b"{}")
            if path.endswith("/issues/101/comments"):
                identifier = len(state["comments"]) + 1
                value = {
                    "id": identifier,
                    "body": payload["body"],
                    "created_at": f"2026-08-18T00:00:0{identifier}Z",
                    "updated_at": f"2026-08-18T00:00:0{identifier}Z",
                    "user": {"login": "mpp"},
                }
                state["comments"].append(value)
                self._send(201, value)
                return
            self._send(404, {})

        def log_message(self, _format: str, *_args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    original_credentials = forgejo._credentials
    forgejo._credentials = lambda _url: {"Accept": "application/json"}
    try:
        client = forgejo.ForgejoClient(
            base_url=f"http://127.0.0.1:{server.server_port}",
            sleep=lambda _seconds: None,
            listing_path=None,
        )
        snapshot = client.stable_snapshot()
        assert snapshot["sha256"]
        event = make_event(
            "migrated",
            "port:v1:src/home/demo.asm:Demo",
            (None, None),
            "0" * 64,
            {
                "state": "ready",
                "source_revision": "a" * 40,
                "publication_revision": "",
                "gate_sha256": "",
                "legacy_history_sha256": "b" * 64,
                "landed_at": None,
                "exclusion_reason": None,
            },
        )
        first = client.append_event(101, event.comment_body(), event.event_id)
        second = client.append_event(101, event.comment_body(), event.event_id)
        assert first["id"] == second["id"] == 1
    finally:
        forgejo._credentials = original_credentials
        server.shutdown()
        server.server_close()
        thread.join()


def check_incremental_listing() -> None:
    issues = {
        number: {
            "id": number,
            "number": number,
            "title": f"Issue {number}",
            "body": "original",
            "state": "open",
            "labels": [],
            "created_at": "2026-08-18T00:00:00Z",
            "updated_at": f"2026-08-18T00:0{number - 100}:00Z",
            "user": {"login": "mpp"},
        }
        for number in (101, 102, 103)
    }
    requests: list[dict[str, list[str]]] = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            requests.append(query)
            rows = sorted(issues.values(), key=lambda issue: issue["number"])
            since = query.get("since", [None])[0]
            if since:
                rows = [row for row in rows if row["updated_at"] >= since]
            limit = int(query.get("limit", ["50"])[0])
            page = int(query.get("page", ["1"])[0])
            window = rows[(page - 1) * limit:page * limit]
            raw = json.dumps(window).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("X-Total-Count", str(len(rows)))
            self.end_headers()
            self.wfile.write(raw)

        def log_message(self, _format: str, *_args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    original_credentials = forgejo._credentials
    forgejo._credentials = lambda _url: {"Accept": "application/json"}
    try:
        with TemporaryDirectory() as directory:
            client = forgejo.ForgejoClient(
                base_url=f"http://127.0.0.1:{server.server_port}",
                sleep=lambda _seconds: None,
                listing_path=Path(directory) / "listing.json",
            )
            cold = client.issues()
            assert [issue["number"] for issue in cold] == [101, 102, 103]
            assert all("since" not in query for query in requests)
            issues[102]["body"] = "changed"
            issues[102]["updated_at"] = "2026-08-18T01:00:00Z"
            requests.clear()
            warm = client.issues()
            assert {issue["number"]: issue["body"] for issue in warm} == {
                101: "original", 102: "changed", 103: "original",
            }
            assert len(requests) == 2
            assert requests[1]["since"]
            del issues[103]
            requests.clear()
            shrunk = client.issues()
            assert [issue["number"] for issue in shrunk] == [101, 102]
            assert any("since" not in query for query in requests)
    finally:
        forgejo._credentials = original_credentials
        server.shutdown()
        server.server_close()
        thread.join()


def check_ledger_samples() -> None:
    chain = [
        {"kind": "migrated", "emitted_at": "2026-08-18T00:00:00+00:00"},
        {"kind": "claim", "emitted_at": "2026-08-18T00:00:00+00:00"},
        {"kind": "attempt-result", "emitted_at": "2026-08-18T00:05:00+00:00"},
        {"kind": "claim", "emitted_at": "2026-08-18T01:00:00+00:00"},
        {"kind": "heartbeat", "emitted_at": "2026-08-18T01:01:00+00:00"},
        {"kind": "attempt-result", "emitted_at": "2026-08-18T01:03:00+00:00"},
        {"kind": "claim", "emitted_at": "2026-08-18T02:00:00+00:00"},
        {"kind": "attempt-result", "emitted_at": "2026-08-19T02:00:00+00:00"},
        {"kind": "landed", "emitted_at": "2026-08-19T03:00:00+00:00"},
    ]
    samples = forecast.samples_from_chain(chain, tier=2, size=140)
    assert [sample.seconds for sample in samples] == [300.0, 180.0]
    assert {sample.tier for sample in samples} == {2}
    assert forecast.samples_from_chain([], tier=1, size=10) == []


def check_pagination_terminates() -> None:
    """Forgejo comment listings ignore `page`: the pager must still finish."""
    comments = [
        {
            "id": index,
            "body": f"comment {index}",
            "created_at": "2026-08-18T00:00:00Z",
            "updated_at": "2026-08-18T00:00:00Z",
            "user": {"login": "mpp"},
        }
        for index in range(1, 121)
    ]
    served = {"pages": 0}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            served["pages"] += 1
            raw = json.dumps(comments[:50]).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def log_message(self, _format: str, *_args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    original_credentials = forgejo._credentials
    forgejo._credentials = lambda _url: {"Accept": "application/json"}
    try:
        client = forgejo.ForgejoClient(
            base_url=f"http://127.0.0.1:{server.server_port}",
            sleep=lambda _seconds: None,
            listing_path=None,
        )
        rows = client.comments(3103)
        assert [row["id"] for row in rows] == list(range(1, 51))
        assert served["pages"] == 2
    finally:
        forgejo._credentials = original_credentials
        server.shutdown()
        server.server_close()
        thread.join()


def check_derived_cache() -> None:
    issue = {
        **work_issue(),
        "id": 101,
        "title": "Demo",
        "created_at": "2026-08-18T00:00:00Z",
        "updated_at": "2026-08-18T00:00:00Z",
        "author": "mpp",
        "url": "",
    }

    class Client:
        def stable_snapshot(self) -> dict:
            return {"sha256": "a" * 64, "issues": [issue]}

        def comments_since(self, number: int, since: str | None) -> list[dict]:
            assert number == 101
            return []

        def dependencies(self, number: int) -> list[dict]:
            assert number == 101
            return []

    with TemporaryDirectory() as directory:
        path = Path(directory) / "cache.sqlite3"
        first = cache.refresh(Client(), path=path)
        second = cache.refresh(Client(), path=path)
        loaded = cache.load(path)
        assert first["changed"] == 1
        assert second["changed"] == 0
        assert loaded["snapshot_sha256"] == "a" * 64
def check_artifact_store() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "source"
        source.mkdir()
        (source / "src" / "home").mkdir(parents=True)
        (source / "src" / "probe").mkdir(parents=True)
        (source / "tests" / "cases").mkdir(parents=True)
        (source / "tools" / "oracle" / "mutation_receipts").mkdir(parents=True)
        (source / "src" / "home" / "demo.c").write_text("int demo(void) { return 0; }\n")
        (source / "src" / "home" / "demo.h").write_text("int demo(void);\n")
        (source / "src" / "probe" / "demo.c").write_text("int probe(void) { return 0; }\n")
        (source / "tests" / "cases" / "demo.py").write_text("CONTRACT = {}\n")
        (source / "tools" / "oracle" / "mutation_receipts" / "Demo.json").write_text("{}\n")
        (source / "packet.json").write_text(
            json.dumps({"basename": "demo", "routines": [{"name": "Demo"}]}) + "\n"
        )
        digest = common.payload_tree_digest(source)
        (source / ".factory-artifact.json").write_text(
            json.dumps({"bundle_sha256": digest}) + "\n"
        )
        previous = workers.V2_ARTIFACTS
        workers.V2_ARTIFACTS = root / "artifacts"
        try:
            stored = workers.store_artifact(
                {"artifact_dir": str(source), "bundle_sha256": digest}
            )
            assert workers.artifact_exists(stored["artifact_sha256"])
            clone = root / "clone"
            clone.mkdir()
            assert integrate.apply_v2_artifacts(clone, [stored["artifact_sha256"]]) == ("Demo",)
            assert (clone / "src" / "home" / "demo.c").is_file()
            grouped = workers.store_group_artifact([stored])
            assert workers.artifact_exists(grouped["artifact_sha256"])
        finally:
            workers.V2_ARTIFACTS = previous


def check_forecast() -> None:
    nodes = [
        forecast.Node("a", 1, 10, ("a",), (), "ready"),
        forecast.Node("b", 1, 10, ("b",), ("a",), "ready"),
    ]
    samples = [forecast.Sample(1, 10, 60.0, 1, 30.0) for _ in range(20)]
    result = forecast.monte_carlo(nodes, samples, lanes=2, trials=200, seed="scenario")
    assert result["p50_seconds"] == 150.0
    dated = forecast.forecast_dates(result, started_at=datetime(2026, 8, 18, tzinfo=UTC))
    assert dated["p85_at"].startswith("2026-08-18T00:02:30")


def check_migration_identity() -> None:
    issue = {
        **work_issue(),
        "created_at": "2026-08-18T00:00:00Z",
        "updated_at": "2026-08-18T00:00:00Z",
    }
    action = {
        "kind": "adopt-routine",
        "work_id": "port:v1:src/home/demo.asm:Demo",
        "issue_number": 101,
        "body": issue["body"],
        "state": "ready",
        "labels": ["port/ready", "tier/1"],
    }
    gate = {"commit": "c" * 40, "complete": True}
    plan = {
        "created_at": "2026-08-18T00:00:00+00:00",
        "gate_commit": gate["commit"],
    }

    class Stub:
        def dependencies(self, _number: int) -> list[dict]:
            return []

    first = migration._migration_event(issue, action, plan=plan, gate=gate, client=Stub())
    moved = migration._migration_event(
        issue, action, plan={**plan, "revision": "d" * 40}, gate=gate, client=Stub(),
    )
    assert first.event_id == moved.event_id
    assert first.payload["source_revision"] == gate["commit"]
    rebuilt = migration._migration_event(
        issue, action, plan={**plan, "gate_commit": "e" * 40}, gate=gate, client=Stub(),
    )
    assert rebuilt.event_id != first.event_id



def main() -> int:
    check_ledger()
    check_control()
    check_planner()
    check_first_claim_election()
    check_lease_covers_deadline()
    check_dirty_guard()
    check_policy_veto_routing()
    check_cohort_state()
    check_recovery_ladder()
    check_forgejo_client()
    check_incremental_listing()
    check_pagination_terminates()
    check_derived_cache()
    check_artifact_store()
    check_forecast()
    check_ledger_samples()
    check_migration_identity()
    print("factory scenario check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
