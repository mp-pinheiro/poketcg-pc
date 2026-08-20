#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import heapq
import json
import random
import statistics
from bisect import bisect_right
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from itertools import pairwise
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Sample:
    tier: int
    size: int
    seconds: float
    attempts: int
    gate_seconds: float = 0.0


@dataclass(frozen=True)
class Node:
    work_id: str
    tier: int
    size: int
    basenames: tuple[str, ...]
    dependencies: tuple[str, ...]
    state: str
    priority: str = "normal"


def quantile(values: list[float], fraction: float) -> float:
    if not values:
        raise ValueError("quantile requires values")
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def size_decile(size: int, all_sizes: Iterable[int]) -> int:
    return _decile(size, sorted(max(0, value) for value in all_sizes))


def _decile(size: int, ordered: list[int]) -> int:
    if not ordered:
        return 0
    below = bisect_right(ordered, size)
    return min(9, max(0, (below * 10 - 1) // len(ordered)))


def _sample_buckets(
    samples: list[Sample],
    ordered_sizes: list[int],
) -> dict[tuple[int, int], list[Sample]]:
    exact: dict[tuple[int, int], list[Sample]] = {}
    by_tier: dict[int, list[Sample]] = {}
    for sample in samples:
        exact.setdefault((sample.tier, _decile(sample.size, ordered_sizes)), []).append(sample)
        by_tier.setdefault(sample.tier, []).append(sample)
    window: dict[int, list[Sample]] = {}
    for tier in by_tier:
        window[tier] = [
            sample
            for near in (tier - 1, tier, tier + 1)
            for sample in by_tier.get(near, ())
        ]
    resolved: dict[tuple[int, int], list[Sample]] = {}
    for tier in {sample.tier for sample in samples} | {1, 2, 3, 4}:
        for decile in range(10):
            choices = exact.get((tier, decile), [])
            if len(choices) < 20:
                choices = window.get(tier, [])
            if len(choices) < 20:
                choices = samples
            resolved[(tier, decile)] = choices
    return resolved


def samples_from_telemetry(events: Iterable[dict[str, Any]]) -> list[Sample]:
    samples: list[Sample] = []
    for event in events:
        payload = event.get("payload") if isinstance(event, dict) else None
        if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
            continue
        for record in payload["records"]:
            if not isinstance(record, dict):
                continue
            seconds = record.get("service_seconds")
            tier = record.get("tier")
            size = record.get("size")
            if not isinstance(seconds, (int, float)) or seconds <= 0:
                continue
            if not isinstance(tier, int) or not isinstance(size, int):
                continue
            attempts = record.get("attempts", 1)
            gate_seconds = record.get("gate_seconds", 0.0)
            if not isinstance(attempts, int) or attempts < 1:
                attempts = 1
            if not isinstance(gate_seconds, (int, float)) or gate_seconds < 0:
                gate_seconds = 0.0
            samples.append(Sample(tier, size, float(seconds), attempts, float(gate_seconds)))
    return samples


def samples_from_chain(
    chain: Iterable[dict[str, Any]],
    *,
    tier: int,
    size: int,
    gate_seconds: float = 600.0,
    limit_seconds: float = 7200.0,
) -> list[Sample]:
    """One sample per claim/attempt-result pair: the measured service time."""
    samples: list[Sample] = []
    claimed: datetime | None = None
    for item in chain:
        kind = item.get("kind")
        try:
            emitted = datetime.fromisoformat(str(item.get("emitted_at")))
        except ValueError:
            continue
        if kind == "claim":
            claimed = emitted
            continue
        if kind != "attempt-result" or claimed is None:
            continue
        seconds = (emitted - claimed).total_seconds()
        claimed = None
        if 1.0 <= seconds <= limit_seconds:
            samples.append(Sample(tier, size, seconds, 1, gate_seconds))
    return samples


_PRIORITY_RANKS = {"urgent": 0, "high": 1, "normal": 2, "low": 3}


def _priority(node: Node) -> tuple[int, str]:
    return _PRIORITY_RANKS.get(node.priority, 2), node.work_id


@dataclass(frozen=True)
class _Graph:
    nodes: dict[str, Node]
    order: dict[str, tuple[int, str]]
    dependents: dict[str, tuple[str, ...]]
    indegree: dict[str, int]
    roots: tuple[str, ...]
    buckets: dict[tuple[int, int], list[Sample]]
    node_decile: dict[str, int]
    gate_seconds: tuple[float, ...]


def build_graph(nodes: list[Node], samples: list[Sample]) -> _Graph:
    pending = {
        node.work_id: node
        for node in nodes
        if node.state not in {"done", "excluded"}
    }
    dependents: dict[str, list[str]] = {work_id: [] for work_id in pending}
    indegree: dict[str, int] = {}
    for work_id, node in pending.items():
        unmet = [dep for dep in node.dependencies if dep in pending and dep != work_id]
        indegree[work_id] = len(unmet)
        for dep in unmet:
            dependents[dep].append(work_id)
    ordered_sizes = sorted(max(0, node.size) for node in nodes)
    return _Graph(
        nodes=pending,
        order={work_id: _priority(node) for work_id, node in pending.items()},
        dependents={work_id: tuple(values) for work_id, values in dependents.items()},
        indegree=indegree,
        roots=tuple(sorted(
            (work_id for work_id, degree in indegree.items() if degree == 0),
            key=lambda work_id: _priority(pending[work_id]),
        )),
        buckets=_sample_buckets(samples, ordered_sizes),
        node_decile={work_id: _decile(node.size, ordered_sizes) for work_id, node in pending.items()},
        gate_seconds=tuple(sample.gate_seconds for sample in samples if sample.gate_seconds > 0),
    )


def _sample_for(graph: _Graph, node: Node, work_id: str, rng: random.Random) -> Sample:
    choices = graph.buckets.get((node.tier, graph.node_decile[work_id])) or []
    if choices:
        return rng.choice(choices)
    return Sample(node.tier, node.size, max(300.0, node.size * 3.0), 1, 600.0)


def _trial(
    graph: _Graph,
    *,
    lanes: int,
    rng: random.Random,
    gate_batch: int,
    calibration_multiplier: float,
) -> tuple[float, int, int]:
    indegree = dict(graph.indegree)
    ready: list[tuple[int, str]] = [(*graph.order[work_id][:1], work_id) for work_id in graph.roots]
    heapq.heapify(ready)
    deferred: list[tuple[int, str]] = []
    active: list[tuple[float, str]] = []
    occupied: set[str] = set()
    started = 0
    total = len(graph.nodes)
    now = 0.0
    gates = 0
    retries = 0
    green_since_gate = 0
    while started < total or active:
        while ready and len(active) < lanes:
            entry = heapq.heappop(ready)
            node = graph.nodes[entry[1]]
            if occupied.intersection(node.basenames):
                deferred.append(entry)
                continue
            sample = _sample_for(graph, node, entry[1], rng)
            attempts = max(1, sample.attempts)
            retries += attempts - 1
            heapq.heappush(active, (now + sample.seconds * attempts * calibration_multiplier, entry[1]))
            occupied.update(node.basenames)
            started += 1
        if not active:
            raise ValueError("forecast graph has unresolved dependency cycle or blocker")
        now, finished_id = heapq.heappop(active)
        finished = graph.nodes[finished_id]
        occupied.difference_update(finished.basenames)
        for entry in deferred:
            heapq.heappush(ready, entry)
        deferred.clear()
        for dependent in graph.dependents[finished_id]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, (graph.order[dependent][0], dependent))
        green_since_gate += 1
        if green_since_gate >= gate_batch or (started >= total and not active):
            now += rng.choice(graph.gate_seconds) if graph.gate_seconds else 600.0
            gates += 1
            green_since_gate = 0
    return now, gates, retries


def monte_carlo(
    nodes: list[Node],
    samples: list[Sample],
    *,
    lanes: int,
    trials: int,
    seed: str,
    gate_batch: int = 8,
    calibration_multiplier: float = 1.0,
) -> dict[str, Any]:
    if lanes < 1 or trials < 1 or gate_batch < 1:
        raise ValueError("lanes, trials, and gate_batch must be positive")
    digest = hashlib.sha256(seed.encode()).digest()
    rng = random.Random(int.from_bytes(digest[:16], "big"))
    durations: list[float] = []
    gates: list[int] = []
    retries: list[int] = []
    graph = build_graph(nodes, samples)
    for _ in range(trials):
        duration, gate_count, retry_count = _trial(
            graph,
            lanes=lanes,
            rng=rng,
            gate_batch=gate_batch,
            calibration_multiplier=calibration_multiplier,
        )
        durations.append(duration)
        gates.append(gate_count)
        retries.append(retry_count)
    return {
        "trials": trials,
        "p50_seconds": quantile(durations, 0.50),
        "p85_seconds": quantile(durations, 0.85),
        "p95_seconds": quantile(durations, 0.95),
        "mean_seconds": statistics.fmean(durations),
        "mean_gates": statistics.fmean(gates),
        "mean_retries": statistics.fmean(retries),
        "samples": len(samples),
        "remaining_nodes": sum(node.state not in {"done", "excluded"} for node in nodes),
        "remaining_bytes": sum(node.size for node in nodes if node.state not in {"done", "excluded"}),
    }


def forecast_dates(result: dict[str, Any], *, started_at: datetime) -> dict[str, Any]:
    value = dict(result)
    for label in ("p50", "p85", "p95"):
        seconds = float(value[f"{label}_seconds"])
        value[f"{label}_at"] = (started_at + timedelta(seconds=seconds)).isoformat()
    return value


def provisional_history(path: Path, *, now: datetime, days: int = 28) -> list[Sample]:
    entries = [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]
    points = sorted(entries, key=lambda entry: int(entry["timestamp"]))
    samples: list[Sample] = []
    for prior, current in pairwise(points):
        elapsed = int(current["timestamp"]) - int(prior["timestamp"])
        code = int(current.get("code", 0)) - int(prior.get("code", 0))
        if elapsed <= 0 or code < 0:
            continue
        date = datetime.fromtimestamp(int(current["timestamp"]), UTC)
        if date < now - timedelta(days=days):
            continue
        samples.append(Sample(1, max(1, code), float(elapsed), 1, 600.0))
    return samples


def calibration(
    observed: list[tuple[float, float]]) -> dict[str, Any]:
    if len(observed) < 8:
        return {"windows": len(observed), "p85_coverage": None, "multiplier": 1.0, "confidence": "low"}
    coverage = sum(actual <= predicted for actual, predicted in observed) / len(observed)
    multiplier = min(2.0, max(1.0, 0.85 / max(0.1, coverage)))
    return {
        "windows": len(observed),
        "p85_coverage": coverage,
        "multiplier": multiplier,
        "confidence": "high" if coverage >= 0.75 else "low",
    }
def forecast_status(
    *,
    valid_attempts: int,
    landed: int,
    route_observations: dict[str, int] | None = None,
    remaining_feature_classes: Iterable[str] = (),
) -> str:
    """Return the publishable schema-2 status without fabricating an ETA."""
    observations = route_observations or {}
    if valid_attempts < 30 or landed < 5 or any(count < 5 for count in observations.values()):
        return "unavailable"
    if any(remaining_feature_classes):
        return "provisional"
    if landed < 30:
        return "provisional"
    return "calibrated"
