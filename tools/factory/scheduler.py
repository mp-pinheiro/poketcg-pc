#!/usr/bin/env python3
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any


@dataclass(frozen=True)
class FactoryWork:
    issue_number: int
    work_id: str
    source: str
    basenames: tuple[str, ...]
    owned_paths: tuple[str, ...]
    size: int
    tier: int
    priority: str
    state: str
    dependencies: tuple[int, ...] = ()
    ready_at: datetime | None = None
    retry_at: datetime | None = None
    p50_seconds: float = 420.0
    cohort: bool = False
    recovery_tier: int = 0
    infra_failures: int = 0
    escalated: bool = False
    feature_class: str = "direct"


@dataclass(frozen=True)
class FactorySnapshot:
    sha256: str
    works: tuple[FactoryWork, ...]
    active_work_ids: frozenset[str] = frozenset()
    control_active: bool = True
    integration_ready: tuple[int, ...] = ()
    blockers: tuple[int, ...] = ()
    complete: bool = False


@dataclass(frozen=True)
class Capacity:
    job_slots: int = 16
    verifier_slots: int = 8
    active_jobs: int = 0
    provider_throttled: bool = False
    verifier_queue_p95: float = 0.0
    verifier_soft_deadline: float = 300.0
    healthy_completions: int = 0


@dataclass(frozen=True)
class PlannedAssignment:
    issue_number: int
    work_id: str
    model_route: str
    kind: str
    score: tuple[int, float, float, str]


@dataclass(frozen=True)
class FactoryPlan:
    snapshot_sha256: str
    assignments: tuple[PlannedAssignment, ...] = ()
    waiting_until: datetime | None = None
    waiting_reason: str | None = None
    dependency_analysis: tuple[int, ...] = ()
    blocker_review: tuple[int, ...] = ()
    infrastructure_incident: bool = False
    integration: tuple[int, ...] = ()
    complete: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "snapshot_sha256": self.snapshot_sha256,
            "assignments": [
                {
                    "issue_number": assignment.issue_number,
                    "work_id": assignment.work_id,
                    "model_route": assignment.model_route,
                    "kind": assignment.kind,
                }
                for assignment in self.assignments
            ],
            "waiting_until": self.waiting_until.isoformat() if self.waiting_until else None,
            "waiting_reason": self.waiting_reason,
            "dependency_analysis": list(self.dependency_analysis),
            "blocker_review": list(self.blocker_review),
            "infrastructure_incident": self.infrastructure_incident,
            "integration": list(self.integration),
            "complete": self.complete,
        }


_PRIORITY = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
ESCALATION_DIAGNOSTICS = 4
INFRASTRUCTURE_INCIDENT_WORKS = 3


def recovery_tier(diagnostic_count: int, repeat_fingerprints: int) -> int:
    tier = min(diagnostic_count, ESCALATION_DIAGNOSTICS)
    if repeat_fingerprints >= 1:
        tier = max(tier, 2)
    if repeat_fingerprints >= 2:
        tier = max(tier, 3)
    return min(tier, ESCALATION_DIAGNOSTICS)


def adjusted_capacity(capacity: Capacity) -> tuple[Capacity, str | None]:
    if capacity.job_slots < 4 or capacity.job_slots > 16:
        raise ValueError("job_slots must be 4..16")
    if capacity.verifier_slots < 1:
        raise ValueError("verifier_slots must be positive")
    if capacity.provider_throttled or capacity.verifier_queue_p95 > capacity.verifier_soft_deadline:
        return Capacity(
            job_slots=max(4, capacity.job_slots // 2),
            verifier_slots=capacity.verifier_slots,
            active_jobs=capacity.active_jobs,
            verifier_queue_p95=capacity.verifier_queue_p95,
            verifier_soft_deadline=capacity.verifier_soft_deadline,
        ), "decrease"
    if (
        capacity.healthy_completions >= 20
        and capacity.verifier_queue_p95 < capacity.verifier_soft_deadline * 0.8
        and capacity.job_slots < 16
    ):
        return Capacity(
            job_slots=capacity.job_slots + 1,
            verifier_slots=capacity.verifier_slots,
            active_jobs=capacity.active_jobs,
            verifier_queue_p95=capacity.verifier_queue_p95,
            verifier_soft_deadline=capacity.verifier_soft_deadline,
        ), "increase"
    return capacity, None


def _dependency_ready(work: FactoryWork, by_issue: dict[int, FactoryWork]) -> bool:
    return all(
        dependency in by_issue and by_issue[dependency].state in {"done", "excluded"}
        for dependency in work.dependencies
    )


def _model_route(work: FactoryWork) -> str:
    return "task" if work.cohort or work.tier >= 2 or work.recovery_tier >= 2 else "smol"


def _assignment_kind(work: FactoryWork) -> str:
    if work.recovery_tier >= 3:
        return "repair"
    return "task" if _model_route(work) == "task" else "completion"


def _dependent_bytes(works: tuple[FactoryWork, ...]) -> dict[int, int]:
    reverse: dict[int, set[int]] = defaultdict(set)
    sizes = {work.issue_number: work.size for work in works}
    for work in works:
        for dependency in work.dependencies:
            reverse[dependency].add(work.issue_number)
    result: dict[int, int] = {}
    for root in sizes:
        seen: set[int] = set()
        pending = list(reverse.get(root, ()))
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            pending.extend(reverse.get(current, ()))
        result[root] = sum(sizes[current] for current in seen)
    return result


def _score(
    work: FactoryWork,
    dependent_bytes: dict[int, int],
    now: datetime,
) -> tuple[int, float, float, str]:
    age = (now - work.ready_at).total_seconds() if work.ready_at else 0.0
    leverage = dependent_bytes.get(work.issue_number, 0) / max(work.p50_seconds, 1.0)
    return _PRIORITY.get(work.priority, _PRIORITY["normal"]), -leverage, -age, work.work_id


def plan(
    snapshot: FactorySnapshot,
    capacity: Capacity,
    now: datetime | None = None,
) -> FactoryPlan:
    now = now or datetime.now(UTC)
    capacity, _change = adjusted_capacity(capacity)
    if snapshot.complete:
        return FactoryPlan(snapshot_sha256=snapshot.sha256, complete=True)
    stalled = [
        work for work in snapshot.works
        if work.infra_failures >= 2 and work.state == "recovery"
    ]
    if len(stalled) >= INFRASTRUCTURE_INCIDENT_WORKS:
        return FactoryPlan(
            snapshot_sha256=snapshot.sha256,
            infrastructure_incident=True,
            waiting_until=now + timedelta(seconds=300),
            waiting_reason="infrastructure-incident",
            blocker_review=tuple(sorted(work.issue_number for work in stalled)),
        )
    by_issue = {work.issue_number: work for work in snapshot.works}
    active_basenames = {
        basename
        for work in snapshot.works
        if work.work_id in snapshot.active_work_ids
        for basename in work.basenames
    }
    available = max(0, capacity.job_slots - capacity.active_jobs)
    dependent_bytes = _dependent_bytes(snapshot.works)
    fresh = [
        work for work in snapshot.works
        if work.state == "ready"
        and not work.escalated
        and _dependency_ready(work, by_issue)
        and work.work_id not in snapshot.active_work_ids
    ]
    recovery = [
        work for work in snapshot.works
        if work.state == "recovery"
        and not work.escalated
        and (work.retry_at is None or work.retry_at <= now)
        and _dependency_ready(work, by_issue)
        and work.work_id not in snapshot.active_work_ids
    ]
    fresh.sort(key=lambda work: _score(work, dependent_bytes, now))
    recovery.sort(key=lambda work: _score(work, dependent_bytes, now))
    if snapshot.integration_ready and (not fresh and not recovery or len(snapshot.integration_ready) >= 8):
        return FactoryPlan(snapshot_sha256=snapshot.sha256, integration=tuple(snapshot.integration_ready[:16]))
    selected: list[FactoryWork] = []
    recovery_slots = max(1, math.floor(capacity.job_slots / 5)) if recovery else 0
    queues = [(recovery, recovery_slots), (fresh, available - recovery_slots)] if recovery_slots else [(fresh, available)]
    for queue, slots in queues:
        for work in queue:
            if len(selected) >= available or slots <= 0:
                break
            if active_basenames & set(work.basenames):
                continue
            selected.append(work)
            active_basenames.update(work.basenames)
            slots -= 1
    for work in fresh + recovery:
        if len(selected) >= available:
            break
        if work in selected or active_basenames & set(work.basenames):
            continue
        selected.append(work)
        active_basenames.update(work.basenames)
    if selected:
        return FactoryPlan(
            snapshot_sha256=snapshot.sha256,
            assignments=tuple(
                PlannedAssignment(
                    issue_number=work.issue_number,
                    work_id=work.work_id,
                    model_route=_model_route(work),
                    kind=_assignment_kind(work),
                    score=_score(work, dependent_bytes, now),
                )
                for work in selected
            ),
        )
    waits = [work.retry_at for work in snapshot.works if work.retry_at is not None and work.retry_at > now]
    if waits:
        return FactoryPlan(snapshot_sha256=snapshot.sha256, waiting_until=min(waits), waiting_reason="backoff")
    review = [
        work.issue_number for work in snapshot.works
        if work.state == "paused"
        or work.escalated
        or (work.state == "blocked" and not work.dependencies)
    ]
    blocked = [
        work.issue_number for work in snapshot.works
        if work.state not in {"done", "excluded"}
        and not work.escalated
        and work.dependencies
        and (work.state == "blocked" or not _dependency_ready(work, by_issue))
    ]
    if review:
        return FactoryPlan(snapshot_sha256=snapshot.sha256, blocker_review=tuple(sorted(set(review))))
    if blocked:
        return FactoryPlan(snapshot_sha256=snapshot.sha256, dependency_analysis=tuple(sorted(set(blocked))))
    if snapshot.integration_ready:
        return FactoryPlan(snapshot_sha256=snapshot.sha256, integration=tuple(snapshot.integration_ready[:16]))
    return FactoryPlan(
        snapshot_sha256=snapshot.sha256,
        waiting_until=now + timedelta(seconds=60),
        waiting_reason="no-actionable-work",
    )
