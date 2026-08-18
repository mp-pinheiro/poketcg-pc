#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import random
import statistics
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
    values = sorted(max(0, value) for value in all_sizes)
    if not values:
        return 0
    below = sum(value <= size for value in values)
    return min(9, max(0, (below * 10 - 1) // len(values)))


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


def _sample_for(node: Node, samples: list[Sample], rng: random.Random, all_sizes: list[int]) -> Sample:
    node_decile = size_decile(node.size, all_sizes)
    matching = [
        sample for sample in samples
        if sample.tier == node.tier and size_decile(sample.size, all_sizes) == node_decile
    ]
    if len(matching) < 20:
        matching = [sample for sample in samples if abs(sample.tier - node.tier) <= 1]
    if len(matching) < 20:
        matching = list(samples)
    if matching:
        return rng.choice(matching)
    conservative = max(300.0, node.size * 3.0)
    return Sample(node.tier, node.size, conservative, 1, 600.0)


def _priority(node: Node) -> tuple[int, str]:
    ranks = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
    return ranks.get(node.priority, 2), node.work_id


def _trial(
    nodes: list[Node],
    samples: list[Sample],
    *,
    lanes: int,
    rng: random.Random,
    gate_batch: int,
    calibration_multiplier: float,
) -> tuple[float, int, int]:
    remaining = {
        node.work_id: node
        for node in nodes
        if node.state not in {"done", "excluded"}
    }
    completed = {node.work_id for node in nodes if node.state in {"done", "excluded"}}
    active: list[tuple[float, Node]] = []
    occupied: set[str] = set()
    all_sizes = [node.size for node in nodes]
    now = 0.0
    gates = 0
    retries = 0
    green_since_gate = 0
    while remaining or active:
        ready = sorted(
            (
                node for node in remaining.values()
                if set(node.dependencies) <= completed and not (set(node.basenames) & occupied)
            ),
            key=_priority,
        )
        while ready and len(active) < lanes:
            node = ready.pop(0)
            sample = _sample_for(node, samples, rng, all_sizes)
            attempts = max(1, sample.attempts)
            retries += attempts - 1
            duration = sample.seconds * attempts * calibration_multiplier
            active.append((now + duration, node))
            active.sort(key=lambda item: item[0])
            occupied.update(node.basenames)
            del remaining[node.work_id]
            ready = sorted(
                (
                    candidate for candidate in remaining.values()
                    if set(candidate.dependencies) <= completed and not (set(candidate.basenames) & occupied)
                ),
                key=_priority,
            )
        if not active:
            raise ValueError("forecast graph has unresolved dependency cycle or blocker")
        now, node = active.pop(0)
        occupied.difference_update(node.basenames)
        completed.add(node.work_id)
        green_since_gate += 1
        if green_since_gate >= gate_batch or (not remaining and not active):
            gate_samples = [sample.gate_seconds for sample in samples if sample.gate_seconds > 0]
            now += rng.choice(gate_samples) if gate_samples else 600.0
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
    for _ in range(trials):
        duration, gate_count, retry_count = _trial(
            nodes,
            samples,
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
