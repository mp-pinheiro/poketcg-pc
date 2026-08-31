#!/usr/bin/env python3
"""Enumerate original-ROM control-flow edges and compare production traces."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ASM_ROOT = ROOT / "poketcg" / "src"
DEFAULT_OUTPUT = ROOT / "build" / "completion" / "cfg.json"
LABEL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.#@]*):{1,2}\s*$")
INSTRUCTION_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_.]*)\s*(.*)$")
BRANCHES = {
    "call": "direct-call", "jp": "direct-jump", "jr": "direct-jump",
    "farcall": "direct-call", "bank1call": "direct-call", "homecall": "direct-call",
    "callab": "direct-call", "callba": "direct-call",
}
CONDITIONS = {"z", "nz", "c", "nc"}
TERMINATORS = {"ret", "reti", "jp", "jr", "halt", "stop"}


def fail(message: str) -> None:
    raise ValueError(message)


def labels_in_sources(files: list[Path]) -> set[str]:
    labels: set[str] = set()
    for path in files:
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = LABEL_RE.match(raw.split(";", 1)[0].strip())
            if match:
                labels.add(match.group(1))
    return labels


def branch_target(operands: str) -> str | None:
    tokens = [token.strip() for token in operands.replace(",", " ").split() if token.strip()]
    while tokens and tokens[0].casefold() in CONDITIONS:
        tokens.pop(0)
    if not tokens:
        return None
    target = tokens[0]
    if target.startswith("$") or target.isdigit() or target.casefold() in {"hl", "bc"}:
        return None
    return target


def enumerate_edges() -> list[dict[str, Any]]:
    if not ASM_ROOT.is_dir():
        fail("run just bootstrap first")
    files = sorted(ASM_ROOT.rglob("*.asm"))
    labels = labels_in_sources(files)
    edges: set[tuple[str, str, str, str, int]] = set()
    for path in files:
        current: str | None = None
        previous: tuple[str, str, int] | None = None
        for lineno, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            stripped = raw.split(";", 1)[0].strip()
            if not stripped:
                continue
            label = LABEL_RE.match(stripped)
            if label:
                name = label.group(1)
                if (
                    current
                    and previous
                    and previous[1].casefold().split()[0] not in TERMINATORS
                    and name in labels
                ):
                    edges.add((current, name, "fallthrough", str(path.relative_to(ROOT)), lineno))
                current = name
                previous = None
                continue
            instruction = INSTRUCTION_RE.match(stripped)
            if not instruction or current is None:
                continue
            mnemonic = instruction.group(1).casefold()
            operands = instruction.group(2)
            if mnemonic in BRANCHES:
                target = branch_target(operands)
                if target in labels:
                    edges.add((current, target, BRANCHES[mnemonic], str(path.relative_to(ROOT)), lineno))
                elif target is None and mnemonic in {"jp", "call"}:
                    edges.add((current, "<indirect>", "indirect", str(path.relative_to(ROOT)), lineno))
            elif mnemonic in {"jp_hl", "callhl", "callindirect", "callbc"}:
                edges.add((current, "<indirect>", "indirect", str(path.relative_to(ROOT)), lineno))
            previous = (current, stripped, lineno)
    return [
        {"source": source, "target": target, "type": edge_type, "file": file, "line": line}
        for source, target, edge_type, file, line in sorted(edges)
    ]


def load_trace(path: Path | None) -> set[tuple[str, str, str]]:
    if path is None:
        return set()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid production trace: {exc}") from exc
    edges = value.get("edges") if isinstance(value, dict) else value
    if not isinstance(edges, list):
        raise ValueError("production trace has no edges")
    result = set()
    for edge in edges:
        if isinstance(edge, dict) and all(isinstance(edge.get(key), str) for key in ("source", "target", "type")):
            result.add((edge["source"], edge["target"], edge["type"]))
    return result


def audit(trace_path: Path | None = None) -> dict[str, Any]:
    edges = enumerate_edges()
    trace = load_trace(trace_path)
    required = {(edge["source"], edge["target"], edge["type"]) for edge in edges}
    covered = required & trace
    uncovered = sorted(required - covered)
    return {
        "schema": 1,
        "required_edges": len(required),
        "covered_edges": len(covered),
        "uncovered_required_edges": len(uncovered),
        "trace_present": trace_path is not None,
        "edges": edges,
        "uncovered": [
            {"source": source, "target": target, "type": edge_type}
            for source, target, edge_type in uncovered
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        report = audit(args.trace)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n")
    summary = {key: report[key] for key in (
        "schema", "required_edges", "covered_edges", "uncovered_required_edges", "trace_present"
    )}
    print(json.dumps(summary, sort_keys=True))
    return 0 if report["uncovered_required_edges"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
