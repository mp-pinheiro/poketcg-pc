#!/usr/bin/env python3
"""Revision-pinned completion audit, status, and obligation checks."""

from __future__ import annotations

import argparse
import copy
import fnmatch
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = ROOT / "tools" / "completion" / "baseline.toml"
MANIFEST_PATH = ROOT / "tools" / "completion" / "requirements.toml"
INVENTORY_PATH = ROOT / "site" / "data" / "inventory.json"
INVENTORY_TOOL = ROOT / "tools" / "progress" / "inventory.py"
ROM_PATH = ROOT / "poketcg" / "poketcg.gbc"
MAP_PATH = ROOT / "poketcg" / "poketcg.map"
SYMBOL_PATH = ROOT / "poketcg" / "poketcg.sym"
ROM_SHA1_PATH = ROOT / "poketcg" / "rom.sha1"
SCOPE_PATH = ROOT / "tools" / "progress" / "scope.toml"
REGISTRY_PATH = ROOT / "tests" / "routines.py"
MAIN_PATH = ROOT / "src" / "main.c"
COMPLETION_DIR = ROOT / "build" / "completion"
CFG_TOOL = ROOT / "tools" / "completion" / "cfg.py"
CFG_OUTPUT = COMPLETION_DIR / "cfg.json"
MAPPING_PATH = COMPLETION_DIR / "routine-mapping.json"
EVIDENCE_DIR = COMPLETION_DIR / "evidence"
ROM_SIZE = 0x100000
EXPECTED_PROVISIONAL = 160
EXPECTED_EXTRA_REGISTRATIONS = 10
ALLOWED_SPAN_KINDS = {"code", "data", "header/metadata", "padding", "unclassified"}
REQUIRED_RELATION_FIELDS = {
    "wram", "hram", "sram_bank_0", "sram_bank_1", "sram_bank_2",
    "sram_bank_3", "vram_bank_0", "vram_bank_1", "oam", "io", "palette_ram",
    "mapper_state", "input_latch", "timer_frame_counters", "rng", "apu_state",
    "apu_trace", "framebuffer", "save", "transport", "printer",
    "sm83_registers_function_boundary", "hardware_exclusions",
}
P8_IDS = {
    "completion:v2:p8:ppu:span-widening",
    "completion:v2:p8:runtime:viewport-rect",
    "completion:v2:p8:ui:wide-layouts",
    "completion:v2:p8:features:render-only",
    "completion:v2:p8:release:enhanced-corpus",
}
C_FUNCTION_RE = re.compile(
    r"(?m)^\s*(?:static\s+)?(?:const\s+)?"
    r"[A-Za-z_][A-Za-z0-9_\s*]*?\b"
    r"([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*\{"
)


class AuditError(RuntimeError):
    """A repository fact violates the completion contract."""


def load_toml(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as stream:
            value = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise AuditError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"{path} is not a TOML table")
    return value


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuditError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"{path} is not a JSON object")
    return value


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
    except OSError as exc:
        raise AuditError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def current_revision() -> str:
    commands = (
        ["jj", "log", "-r", "@-", "--no-graph", "-T", "commit_id"],
        ["git", "rev-parse", "HEAD"],
    )
    for command in commands:
        try:
            result = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return "unknown"


def load_rom_inventory_module() -> Any:
    path = ROOT / "tools" / "completion" / "rom_inventory.py"
    spec = importlib.util.spec_from_file_location("completion_rom_inventory", path)
    if spec is None or spec.loader is None:
        raise AuditError(f"cannot load independent inventory {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise AuditError(f"cannot load independent inventory {path}: {exc}") from exc
    return module


def run_source_inventory() -> dict[str, Any]:
    try:
        result = subprocess.run(
            [sys.executable, str(INVENTORY_TOOL)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AuditError(f"source inventory did not run: {exc}") from exc
    if result.returncode:
        detail = (result.stderr or result.stdout).strip().splitlines()
        raise AuditError(
            "source inventory failed: " + (detail[-1] if detail else "unknown error")
        )
    return load_json(INVENTORY_PATH)

def run_cfg_audit() -> dict[str, Any]:
    try:
        result = subprocess.run(
            [sys.executable, str(CFG_TOOL), "--output", str(CFG_OUTPUT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AuditError(f"CFG audit did not run: {exc}") from exc
    if not CFG_OUTPUT.is_file():
        detail = (result.stderr or result.stdout).strip().splitlines()
        raise AuditError(
            "CFG audit produced no report: " + (detail[-1] if detail else "unknown error")
        )
    report = load_json(CFG_OUTPUT)
    if not isinstance(report.get("uncovered_required_edges"), int):
        raise AuditError("CFG report has no uncovered edge count")
    return report


def read_rom_sha1() -> str:
    try:
        text = ROM_SHA1_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise AuditError(f"cannot read {ROM_SHA1_PATH}: {exc}") from exc
    match = re.search(r"\b([0-9a-fA-F]{40})\b", text)
    if not match:
        raise AuditError(f"no SHA-1 in {ROM_SHA1_PATH}")
    return match.group(1).lower()


def validate_baseline(baseline: dict[str, Any], inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    values = baseline.get("baseline")
    if not isinstance(values, dict):
        return ["baseline table is missing"]
    required = {
        "epoch", "pret_commit", "rom_sha1", "rom_sha256", "rom_size", "rom_banks",
        "map_sha256", "symbol_sha256", "inventory_sha256", "inventory_schema",
        "map_parser", "symbol_parser", "inventory_parser",
    }
    missing = sorted(required - values.keys())
    if missing:
        errors.append(f"baseline missing fields: {','.join(missing)}")
        return errors
    try:
        epoch = int(values["epoch"])
    except (TypeError, ValueError):
        errors.append("baseline epoch is not an integer")
        epoch = 0
    if epoch < 1:
        errors.append("baseline epoch must be positive")
    try:
        actual_size = ROM_PATH.stat().st_size
    except OSError as exc:
        errors.append(f"ROM is unavailable: {exc}")
        actual_size = -1
    if values["pret_commit"] != "0e7157e885c03d68b3b44410d3adc5aede385627":
        errors.append("pret commit is not the frozen epoch")
    try:
        pret = subprocess.run(
            ["git", "-C", str(ROOT / "poketcg"), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        actual_pret = pret.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        actual_pret = ""
    if actual_pret != values["pret_commit"]:
        errors.append("pret checkout revision differs from baseline")
    if actual_size != values["rom_size"] or actual_size != ROM_SIZE:
        errors.append(f"ROM size is {actual_size}, expected {ROM_SIZE}")
    if values["rom_banks"] != ROM_SIZE // 0x4000:
        errors.append("baseline ROM bank count is invalid")
    try:
        actual_sha256 = sha256_path(ROM_PATH)
        actual_map = sha256_path(MAP_PATH)
        actual_symbols = sha256_path(SYMBOL_PATH)
        actual_inventory = sha256_path(INVENTORY_PATH)
    except AuditError as exc:
        errors.append(str(exc))
        return errors
    if values["rom_sha1"] != read_rom_sha1():
        errors.append("ROM SHA-1 differs from rom.sha1")
    if values["rom_sha256"] != actual_sha256:
        errors.append("ROM SHA-256 differs from baseline")
    if values["map_sha256"] != actual_map:
        errors.append("map SHA-256 differs from baseline")
    if values["symbol_sha256"] != actual_symbols:
        errors.append("symbol SHA-256 differs from baseline")
    if values["inventory_sha256"] != actual_inventory:
        errors.append("source inventory SHA-256 differs from baseline")
    if values["inventory_schema"] != inventory.get("schema"):
        errors.append("source inventory schema differs from baseline")
    if inventory.get("pret_commit") != values["pret_commit"]:
        errors.append("source inventory pret revision differs from baseline")
    return errors


def validate_manifest_source(manifest: dict[str, Any], expected_sha: str) -> None:
    table = manifest.get("manifest")
    if not isinstance(table, dict):
        raise AuditError("manifest table is missing")
    source = table.get("source")
    if source != "docs/vision.md":
        raise AuditError("requirements source is not docs/vision.md")
    if table.get("source_sha256") != expected_sha:
        raise AuditError("requirements source hash is stale")


def validate_manifest(manifest: dict[str, Any], baseline: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    table = manifest.get("manifest")
    if not isinstance(table, dict):
        return ["requirements manifest table is missing"]
    if table.get("schema") != 2:
        errors.append("requirements manifest schema is not 2")
    epoch = baseline.get("baseline", {}).get("epoch")
    if table.get("version") != f"completion-v2-epoch-{epoch}":
        errors.append("requirements manifest version does not match baseline epoch")
    try:
        validate_manifest_source(manifest, sha256_path(ROOT / "docs" / "vision.md"))
    except AuditError as exc:
        errors.append(str(exc))
    milestones = table.get("milestones")
    if not isinstance(milestones, list) or not milestones:
        errors.append("requirements milestones are missing")
        milestones = []
    milestone_set = {item for item in milestones if isinstance(item, str)}
    representation = manifest.get("representation")
    if not isinstance(representation, list):
        errors.append("representation relation is missing")
        representation = []
    relation_fields: set[str] = set()
    for index, row in enumerate(representation):
        if not isinstance(row, dict):
            errors.append(f"representation row {index} is malformed")
            continue
        field = row.get("field")
        if not isinstance(field, str) or not field:
            errors.append(f"representation row {index} has no field")
        elif field in relation_fields:
            errors.append(f"duplicate representation field: {field}")
        else:
            relation_fields.add(field)
        if row.get("required") is not True:
            errors.append(f"representation field is not mandatory: {field}")
    missing_relation = sorted(REQUIRED_RELATION_FIELDS - relation_fields)
    if missing_relation:
        errors.append("missing representation fields: " + ",".join(missing_relation))
    exclusion = next(
        (row for row in representation if isinstance(row, dict)
         and row.get("field") == "hardware_exclusions"),
        None,
    )
    refinement = exclusion.get("refinement", "") if exclusion else ""
    if "LY" not in refinement or "DIV" not in refinement:
        errors.append("LY/DIV lack named directional transform rows")
    requirements = manifest.get("requirement")
    if not isinstance(requirements, list) or not requirements:
        return errors + ["requirements entries are missing"]
    ids: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, req in enumerate(requirements):
        if not isinstance(req, dict):
            errors.append(f"requirement {index} is malformed")
            continue
        req_id = req.get("id")
        if not isinstance(req_id, str) or not req_id:
            errors.append(f"requirement {index} has no stable ID")
            continue
        if req_id in by_id:
            errors.append(f"duplicate requirement ID: {req_id}")
        ids.append(req_id)
        by_id[req_id] = req
        for field in (
            "anchor", "milestone", "command", "terminal_event", "artifact_schema",
        ):
            if not isinstance(req.get(field), str) or not req[field]:
                errors.append(f"{req_id} missing {field}")
        if req.get("milestone") not in milestone_set:
            errors.append(f"{req_id} names unknown milestone")
        if req.get("command") != f"just completion-check {req_id}":
            errors.append(f"{req_id} command is not its exact completion-check")
        for field in ("min_frames", "min_events"):
            value = req.get(field)
            if not isinstance(value, int) or value < 0:
                errors.append(f"{req_id} has invalid {field}")
        state_fields = req.get("state_fields")
        if not isinstance(state_fields, list) or not all(
            isinstance(field, str) and field for field in state_fields
        ):
            errors.append(f"{req_id} has invalid state_fields")
        deps = req.get("deps")
        if not isinstance(deps, list) or not all(isinstance(dep, str) for dep in deps):
            errors.append(f"{req_id} has invalid dependencies")
        issue = req.get("tracker_issue")
        if not isinstance(issue, int) or issue < 0:
            errors.append(f"{req_id} has invalid tracker_issue")
    for req_id, req in by_id.items():
        for dep in req.get("deps", []):
            if dep not in by_id:
                errors.append(f"{req_id} depends on unknown {dep}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(req_id: str) -> None:
        if req_id in visiting:
            raise AuditError(f"requirement dependency cycle at {req_id}")
        if req_id in visited:
            return
        visiting.add(req_id)
        for dep in by_id.get(req_id, {}).get("deps", []):
            if dep in by_id:
                visit(dep)
        visiting.remove(req_id)
        visited.add(req_id)

    try:
        for req_id in ids:
            visit(req_id)
    except AuditError as exc:
        errors.append(str(exc))
    boot = by_id.get("completion:v2:p2:boot-title")
    if boot:
        if boot.get("min_frames") != 600 or boot.get("terminal_event") != "NEW_GAME_ENTERED":
            errors.append("boot-title requirement was weakened")
        fields = set(boot.get("state_fields", []))
        if not {"wram", "framebuffer"} <= fields:
            errors.append("boot-title omits required state fields")
    negative = by_id.get("completion:v2:p2:boot-title-negative")
    if negative and negative.get("terminal_event") != "FIRST_MISMATCH":
        errors.append("boot-title-negative has no first-mismatch terminal")
    if not P8_IDS <= set(by_id):
        errors.append("Phase 8 stable obligations are incomplete")
    scenarios = manifest.get("scenario")
    scenarios_by_id = {
        scenario.get("id"): scenario
        for scenario in scenarios if isinstance(scenario, dict)
    } if isinstance(scenarios, list) else {}
    for scenario_id in ("boot-title", "boot-title-negative"):
        scenario = scenarios_by_id.get(scenario_id)
        if scenario is None:
            errors.append(f"missing immutable scenario: {scenario_id}")
            continue
        if scenario.get("requirement") not in by_id:
            errors.append(f"{scenario_id} points at unknown requirement")
        for field in (
            "start_state", "input_schema", "terminal_event",
            "raw_checkpoint_schema", "comparison",
        ):
            if not isinstance(scenario.get(field), str) or not scenario[field]:
                errors.append(f"{scenario_id} missing {field}")
        if not isinstance(scenario.get("minimum_rendered_frames"), int):
            errors.append(f"{scenario_id} has no frame bound")
    boot_scenario = scenarios_by_id.get("boot-title")
    if boot_scenario and boot_scenario.get("minimum_rendered_frames") != 600:
        errors.append("boot-title scenario was weakened")
    negative_scenario = scenarios_by_id.get("boot-title-negative")
    if negative_scenario and not negative_scenario.get("perturbation"):
        errors.append("boot-title-negative has no perturbation")
    return errors


def span_interval(span: dict[str, Any]) -> tuple[int, int]:
    try:
        offset = int(span["offset"])
        length = int(span["length"])
    except (KeyError, TypeError, ValueError) as exc:
        raise AuditError(f"malformed span: {span!r}") from exc
    if offset < 0 or length <= 0:
        raise AuditError(f"invalid span extent: {span!r}")
    return offset, offset + length


def validate_mapped_spans(spans: list[dict[str, Any]]) -> int:
    cursor = 0
    total = 0
    for span in sorted(spans, key=lambda item: int(item.get("offset", -1))):
        if span.get("kind") not in ALLOWED_SPAN_KINDS - {"padding"}:
            raise AuditError(f"invalid mapped span kind: {span.get('kind')!r}")
        start, end = span_interval(span)
        if start < cursor:
            raise AuditError(f"overlapping mapped span at 0x{start:06x}")
        cursor = end
        total += end - start
    return total


def validate_physical_spans(spans: list[dict[str, Any]], expected_end: int) -> dict[str, int]:
    cursor = 0
    totals: dict[str, int] = {}
    for span in sorted(spans, key=lambda item: int(item.get("offset", -1))):
        kind = span.get("kind")
        if kind not in ALLOWED_SPAN_KINDS:
            raise AuditError(f"invalid physical span kind: {kind!r}")
        start, end = span_interval(span)
        if start != cursor:
            if start < cursor:
                raise AuditError(f"overlapping physical span at 0x{start:06x}")
            raise AuditError(f"missing physical span at 0x{cursor:06x}")
        cursor = end
        totals[kind] = totals.get(kind, 0) + end - start
    if cursor != expected_end:
        raise AuditError(f"physical span union ends at 0x{cursor:06x}, expected 0x{expected_end:06x}")
    return totals


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def canonical_name(name: str) -> str:
    return name.split(".", 1)[0]


def load_registry() -> tuple[list[str], dict[str, list[str]]]:
    spec = importlib.util.spec_from_file_location("completion_routines", REGISTRY_PATH)
    if spec is None or spec.loader is None:
        raise AuditError(f"cannot load {REGISTRY_PATH}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise AuditError(f"cannot load {REGISTRY_PATH}: {exc}") from exc
    groups = getattr(module, "ROUTINES", {})
    if not isinstance(groups, dict):
        raise AuditError("ROUTINES is not a mapping")
    registrations = [name for values in groups.values() for name in values]
    grouped: dict[str, list[str]] = {}
    for name in registrations:
        grouped.setdefault(canonical_name(name), []).append(name)
    return registrations, grouped


def load_scope_exclusions(inventory_functions: dict[str, Any] | None = None) -> set[str]:
    if not SCOPE_PATH.is_file():
        return set()
    scope = load_toml(SCOPE_PATH)
    exclusions: set[str] = set()
    for rule in scope.get("exclude", []):
        if not isinstance(rule, dict):
            continue
        symbols = rule.get("symbols", [])
        exclusions.update(symbol for symbol in symbols if isinstance(symbol, str))
        if inventory_functions is None:
            continue
        patterns = [pattern for pattern in rule.get("files", []) if isinstance(pattern, str)]
        for name, info in inventory_functions.items():
            file_name = info.get("file") if isinstance(info, dict) else None
            if isinstance(file_name, str) and any(
                fnmatch.fnmatch(file_name, pattern) for pattern in patterns
            ):
                exclusions.add(name)
    return exclusions


def native_definitions() -> set[str]:
    definitions: set[str] = set()
    for path in sorted((ROOT / "src" / "home").glob("*.c")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise AuditError(f"cannot read {path}: {exc}") from exc
        definitions.update(C_FUNCTION_RE.findall(text))
    return definitions
def build_mapping(inventory: dict[str, Any]) -> dict[str, Any]:
    registrations, grouped = load_registry()
    inventory_functions = inventory.get("functions")
    if not isinstance(inventory_functions, dict):
        raise AuditError("inventory functions are missing")
    excluded = load_scope_exclusions(inventory_functions)
    canonical_inventory = {
        name for name in inventory_functions
        if name not in excluded
    }
    canonical_registry = set(grouped)
    native = native_definitions()
    rows: list[dict[str, Any]] = []
    missing_native: list[str] = []
    provisional: list[str] = []
    for name in sorted(canonical_registry):
        info = inventory_functions.get(name)
        span = None if info is None else {
            "bank": info.get("bank"), "address": info.get("addr"), "length": info.get("size"),
        }
        candidates = [candidate for candidate in (name, name.replace(".", "_")) if candidate in native]
        primary = candidates[0] if candidates else None
        primary_case = primary_case_for(name)
        if primary_case is None:
            primary_case = next(
                (primary_case_for(registration) for registration in grouped[name]
                 if primary_case_for(registration) is not None),
                None,
            )
        mode = primary_case.get("completion", {}).get("mode") if primary_case else None
        if mode != "return" and name not in excluded:
            provisional.append(name)
        disposition = "source-unreachable" if name in excluded else (
            "native-implementation-provisional" if mode != "return" else "native-implementation-final"
        )
        rows.append({
            "canonical": name,
            "registrations": grouped[name],
            "native_symbols": candidates,
            "disposition": disposition if primary is not None or name in excluded else "missing-native",
            "completion_mode": mode,
            "span": span,
        })
    orphan = sorted(
        name for name in registrations
        if canonical_name(name) not in inventory_functions
    )
    unregistered = sorted(canonical_inventory - canonical_registry)
    registration_rows = []
    for name in registrations:
        canonical = canonical_name(name)
        registration_rows.append({
            "registration": name,
            "canonical": canonical,
            "subentry_of": canonical if "." in name else None,
            "span": next((row["span"] for row in rows if row["canonical"] == canonical), None),
        })
    return {
        "schema": 1,
        "registrations": len(registrations),
        "logical_routines": len(canonical_registry),
        "expected_logical_routines": len(canonical_inventory),
        "extra_registrations": len(registrations) - len(canonical_registry),
        "expected_extra_registrations": EXPECTED_EXTRA_REGISTRATIONS,
        "orphan_registrations": len(orphan),
        "orphan_names": orphan,
        "unregistered_inventory": len(unregistered),
        "unregistered_names": unregistered,
        "missing_native": len(missing_native),
        "missing_native_names": missing_native,
        "final_routines": len(canonical_registry) - len(provisional),
        "provisional_routines": len(provisional),
        "provisional_names": provisional,
        "rows": rows,
        "registration_rows": registration_rows,
    }


_PRIMARY_CASES: dict[str, dict[str, Any]] | None = None


def primary_case_for(name: str) -> dict[str, Any] | None:
    global _PRIMARY_CASES
    if _PRIMARY_CASES is None:
        _PRIMARY_CASES = {}
        case_dir = ROOT / "tests" / "cases"
        for path in sorted(case_dir.glob("*.py")):
            if path.name.startswith("_") or path.name == "__init__.py":
                continue
            spec = importlib.util.spec_from_file_location(f"completion_case_{path.stem}", path)
            if spec is None or spec.loader is None:
                raise AuditError(f"cannot load case module {path}")
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as exc:
                raise AuditError(f"cannot load case module {path}: {exc}") from exc
            for routine, records in getattr(module, "SCHEMA2_CASES", {}).items():
                primary = [record for record in records if record.get("evidence") == "primary"]
                if primary:
                    _PRIMARY_CASES[routine] = primary[0]
    return _PRIMARY_CASES.get(name)


def evidence_path(req_id: str) -> Path:
    return EVIDENCE_DIR / f"{req_id}.json"


def check_evidence(req: dict[str, Any], content_key: str) -> tuple[str, str | None]:
    path = evidence_path(req["id"])
    if not path.is_file():
        return "missing", f"missing artifact {path.relative_to(ROOT)}"
    try:
        artifact = load_json(path)
    except AuditError as exc:
        return "invalid", str(exc)
    if artifact.get("schema") != req["artifact_schema"]:
        return "stale", "artifact schema does not match requirement"
    if artifact.get("status") != "PASS":
        return "failing", "artifact status is not PASS"
    if artifact.get("content_key") != content_key:
        return "stale", "artifact content key differs from current revision"
    if artifact.get("terminal_event") != req["terminal_event"]:
        return "failing", "required terminal event is absent"
    if not isinstance(artifact.get("frames"), int) or artifact["frames"] < req["min_frames"]:
        return "failing", "minimum frame bound is not met"
    if not isinstance(artifact.get("events"), int) or artifact["events"] < req["min_events"]:
        return "failing", "minimum event bound is not met"
    fields = artifact.get("state_fields")
    if not isinstance(fields, list) or not set(req["state_fields"]) <= set(fields):
        return "failing", "representation fields are incomplete"
    oracles = artifact.get("oracles")
    if not isinstance(oracles, list) or not oracles:
        return "unsupported", "artifact has no oracle identities"
    if artifact.get("unsupported") or artifact.get("timeout") or artifact.get("partial"):
        return "failing", "artifact records unsupported, timeout, or partial evidence"
    return "pass", None


def content_key(baseline: dict[str, Any], manifest: dict[str, Any]) -> str:
    values = baseline["baseline"]
    digest = hashlib.sha256()
    for value in (
        values["epoch"], values["pret_commit"], values["rom_sha256"], values["map_sha256"],
        values["symbol_sha256"], values["inventory_sha256"], manifest["manifest"]["version"],
        manifest["manifest"]["source_sha256"], current_revision(),
    ):
        digest.update(str(value).encode("utf-8"))
        digest.update(b"\0")
    digest.update(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    digest.update(b"\0")
    return digest.hexdigest()[:24]


def run_negative_fixtures() -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    checks = {
        "overlap": lambda: validate_physical_spans(
            [{"kind": "code", "offset": 0, "length": 2},
             {"kind": "data", "offset": 1, "length": 3}], 4),
        "missing": lambda: validate_physical_spans(
            [{"kind": "code", "offset": 0, "length": 2},
             {"kind": "padding", "offset": 3, "length": 1}], 4),
    }
    for name, check in checks.items():
        try:
            check()
        except AuditError:
            results[name] = {"status": "PASS", "observed": "rejected"}
        else:
            results[name] = {"status": "FAIL", "observed": "accepted"}
    try:
        validate_registration_fixture(["Known", "Orphan"], {"Known"})
    except AuditError:
        results["orphan_registration"] = {"status": "PASS", "observed": "rejected"}
    else:
        results["orphan_registration"] = {"status": "FAIL", "observed": "accepted"}
    try:
        manifest = load_toml(MANIFEST_PATH)
        weakened = copy.deepcopy(manifest)
        for req in weakened["requirement"]:
            if req.get("id") == "completion:v2:p2:boot-title":
                req["min_frames"] = 1
        manifest_errors = validate_manifest(weakened, {"baseline": {"epoch": 2}})
    except AuditError as exc:
        results["weakened_requirement"] = {
            "status": "FAIL", "observed": f"fixture error: {exc}",
        }
    else:
        rejected = "boot-title requirement was weakened" in manifest_errors
        results["weakened_requirement"] = {
            "status": "PASS" if rejected else "FAIL",
            "observed": "rejected" if rejected else "accepted",
        }
    try:
        validate_manifest_source({"manifest": {
            "source": "docs/vision.md", "source_sha256": "0" * 64,
        }}, sha256_path(ROOT / "docs" / "vision.md"))
    except AuditError:
        results["stale_source_hash"] = {"status": "PASS", "observed": "rejected"}
    else:
        results["stale_source_hash"] = {"status": "FAIL", "observed": "accepted"}
    return results


def validate_registration_fixture(registrations: list[str], known: set[str]) -> None:
    orphan = [name for name in registrations if canonical_name(name) not in known]
    if orphan:
        raise AuditError("orphan registration: " + ",".join(orphan))


def collect_report() -> dict[str, Any]:
    errors: list[str] = []
    baseline = load_toml(BASELINE_PATH)
    manifest = load_toml(MANIFEST_PATH)
    try:
        inventory = run_source_inventory()
    except AuditError as exc:
        return {
            "schema": 2, "complete": False, "errors": [str(exc)],
            "counts": {"rom_bytes": ROM_SIZE, "unclassified_bytes": None},
        }
    baseline_errors = validate_baseline(baseline, inventory)
    errors.extend(baseline_errors)
    errors.extend(validate_manifest(manifest, baseline))
    try:
        independent_module = load_rom_inventory_module()
        independent = independent_module.build(ROM_PATH, MAP_PATH, SYMBOL_PATH)
    except (AuditError, OSError, ValueError) as exc:
        independent = {"spans": [], "totals": {}, "unclassified_bytes": None}
        errors.append(f"independent inventory failed: {exc}")
    source_spans = inventory.get("spans", [])
    if not isinstance(source_spans, list):
        errors.append("source inventory has no spans")
        source_spans = []
    try:
        source_mapped = validate_mapped_spans(source_spans)
    except AuditError as exc:
        source_mapped = 0
        errors.append(f"source span audit: {exc}")
    independent_spans = independent.get("spans", [])
    try:
        independent_totals = validate_physical_spans(independent_spans, ROM_SIZE)
    except AuditError as exc:
        independent_totals = independent.get("totals", {})
        errors.append(f"independent span audit: {exc}")
    source_mapped_intervals = [
        span_interval(span) for span in source_spans if isinstance(span, dict)
    ]
    independent_mapped_intervals = [
        span_interval(span) for span in independent_spans
        if isinstance(span, dict) and span.get("kind") != "padding"
    ]
    if merge_intervals(source_mapped_intervals) != merge_intervals(independent_mapped_intervals):
        errors.append("source and independent mapped ROM unions disagree")
    source_unclassified = sum(
        int(span.get("length", 0)) for span in source_spans
        if isinstance(span, dict) and span.get("kind") == "unclassified"
    )
    independent_unclassified = int(independent.get("unclassified_bytes", 0) or 0)
    if source_unclassified or independent_unclassified:
        errors.append(
            f"unclassified ROM spans remain: source={source_unclassified}, "
            f"independent={independent_unclassified}"
        )
    if independent_totals.get("padding", 0) != ROM_SIZE - source_mapped:
        errors.append("padding does not account for bytes outside mapped sections")
    try:
        cfg = run_cfg_audit()
    except AuditError as exc:
        cfg = {"required_edges": 0, "covered_edges": 0, "uncovered_required_edges": None}
        errors.append(str(exc))
    if cfg.get("uncovered_required_edges"):
        errors.append(
            f"uncovered required CFG edges: {cfg['uncovered_required_edges']}"
        )
    try:
        mapping = build_mapping(inventory)
    except AuditError as exc:
        mapping = {
            "registrations": 0, "logical_routines": 0, "final_routines": 0,
            "provisional_routines": 0, "orphan_registrations": 0,
        }
        errors.append(str(exc))
    COMPLETION_DIR.mkdir(parents=True, exist_ok=True)
    MAPPING_PATH.write_text(
        json.dumps(mapping, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    if mapping.get("orphan_registrations"):
        errors.append(f"orphan registrations: {mapping['orphan_registrations']}")
    if mapping.get("unregistered_inventory"):
        errors.append(f"unregistered canonical routines: {mapping['unregistered_inventory']}")
    if mapping.get("missing_native"):
        errors.append(f"missing native implementations: {mapping['missing_native']}")
    if mapping.get("logical_routines") != mapping.get("expected_logical_routines"):
        errors.append("registry and canonical inventory counts disagree")
    if mapping.get("extra_registrations") != EXPECTED_EXTRA_REGISTRATIONS:
        errors.append(
            f"registration mismatch: logical={mapping.get('logical_routines')}, "
            f"registrations={mapping.get('registrations')}, "
            f"extra={mapping.get('extra_registrations')}, expected_extra={EXPECTED_EXTRA_REGISTRATIONS}"
        )
    if mapping.get("provisional_routines") != EXPECTED_PROVISIONAL:
        errors.append(
            f"provisional routine count is {mapping.get('provisional_routines')}, "
            f"expected {EXPECTED_PROVISIONAL}"
        )
    baseline_values = baseline.get("baseline", {})
    manifest_values = manifest.get("manifest", {})
    key = content_key(baseline, manifest)
    requirement_rows: dict[str, dict[str, Any]] = {}
    requirements = manifest.get("requirement", [])
    for req in requirements if isinstance(requirements, list) else []:
        if not isinstance(req, dict) or not isinstance(req.get("id"), str):
            continue
        status, reason = check_evidence(req, key)
        row = {"status": status, "artifact": str(evidence_path(req["id"]).relative_to(ROOT))}
        if reason:
            row["reason"] = reason
        requirement_rows[req["id"]] = row
        if status != "pass":
            errors.append(f"requirement {req['id']}: {status}")
    passing_requirements = sum(row["status"] == "pass" for row in requirement_rows.values())
    milestone_pass = {
        milestone: all(
            requirement_rows.get(req.get("id"), {}).get("status") == "pass"
            for req in requirements
            if isinstance(req, dict) and req.get("milestone") == milestone
        )
        for milestone in manifest_values.get("milestones", [])
    }
    production_source = MAIN_PATH.read_text(encoding="utf-8") if MAIN_PATH.is_file() else ""
    roots = {
        symbol: bool(re.search(rf"\b{symbol}\s*\(", production_source))
        for symbol in ("Start", "GameLoop", "HandleTitleScreen")
    }
    if not all(roots.values()):
        errors.append("production game root is not integrated")
    native_scene_count = sum(
        row["status"] == "pass"
        for req_id, row in requirement_rows.items()
        if req_id.startswith("completion:v2:p") and ":p2:" not in req_id
    )
    if native_scene_count == 0:
        errors.append("native scene corpus is empty")
    gate_path = ROOT / "site" / "data" / "gate.json"
    try:
        gate = load_json(gate_path)
    except AuditError:
        gate = {}
    trusted_gate = (
        gate.get("schema") == 2
        and gate.get("complete") is True
        and gate.get("commit") == current_revision()
    )
    if not trusted_gate:
        errors.append("trusted oracle evidence is empty or stale")
    fixtures = run_negative_fixtures()
    for name, result in fixtures.items():
        if result.get("status") != "PASS":
            errors.append(f"negative fixture accepted invalid {name}")
    counts = {
        "rom_bytes": ROM_SIZE,
        "mapped_rom_bytes": source_mapped,
        "unclassified_bytes": source_unclassified + independent_unclassified,
        "padding_bytes": independent_totals.get("padding", 0),
        "landed_inventory": {
            "routines": mapping.get("expected_logical_routines", 0),
            "code_bytes": sum(
                int(info.get("size", 0))
                for name, info in inventory.get("functions", {}).items()
                if name not in load_scope_exclusions(inventory.get("functions", {}))
            ),
        },
        "final_routines": {
            "count": mapping.get("final_routines", 0),
            "total": mapping.get("logical_routines", 0),
        },
        "provisional_routines": mapping.get("provisional_routines", 0),
        "trusted_oracle_evidence": {
            "count": 1 if trusted_gate else 0,
            "total": 1,
        },
        "production_integration": {
            "roots": sum(roots.values()),
            "root_total": len(roots),
            "native_scenes": native_scene_count,
            "required_edges": cfg.get("required_edges", 0),
            "covered_edges": cfg.get("covered_edges", 0),
            "uncovered_required_edges": cfg.get("uncovered_required_edges"),
        },
        "requirements": {
            "passing": passing_requirements,
            "total": len(requirement_rows),
            "remaining": len(requirement_rows) - passing_requirements,
        },
        "milestone_gates": {
            "passing": sum(milestone_pass.values()),
            "total": len(milestone_pass),
        },
        "orphan_registrations": mapping.get("orphan_registrations", 0),
    }
    return {
        "complete": not errors,
        "revision": current_revision(),
        "content_key": key,
        "baseline": {
            "epoch": baseline_values.get("epoch"),
            "pret_commit": baseline_values.get("pret_commit"),
            "valid": not baseline_errors,
        },
        "counts": counts,
        "mapping": {
            key: mapping[key]
            for key in (
                "registrations", "logical_routines", "expected_logical_routines",
                "extra_registrations", "expected_extra_registrations", "orphan_registrations",
                "unregistered_inventory", "missing_native", "final_routines",
                "provisional_routines",
            )
            if key in mapping
        },
        "requirements": requirement_rows,
        "milestones": milestone_pass,
        "fixtures": fixtures,
        "errors": sorted(set(errors)),
    }


def command_audit() -> int:
    report = collect_report()
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report.get("complete") else 2


def command_status() -> int:
    report = collect_report()
    report["eta"] = {"p50": "insufficient-data", "p90": "insufficient-data"}
    report["remaining_obligations"] = report["counts"]["requirements"]["remaining"]
    report["critical_path"] = [
        req_id for req_id, row in report.get("requirements", {}).items()
        if row.get("status") != "pass"
    ]
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0


def command_check(req_id: str) -> int:
    manifest = load_toml(MANIFEST_PATH)
    requirements = manifest.get("requirement", [])
    req = next(
        (item for item in requirements if isinstance(item, dict) and item.get("id") == req_id),
        None,
    )
    if req is None:
        print(json.dumps({"status": "FAIL", "id": req_id, "reason": "unknown requirement"}))
        return 2
    baseline = load_toml(BASELINE_PATH)
    key = content_key(baseline, manifest)
    status, reason = check_evidence(req, key)
    payload = {"schema": 2, "id": req_id, "status": status, "content_key": key}
    if reason:
        payload["reason"] = reason
    print(json.dumps(payload, sort_keys=True))
    return 0 if status == "pass" else 2


def command_next() -> int:
    manifest = load_toml(MANIFEST_PATH)
    baseline = load_toml(BASELINE_PATH)
    key = content_key(baseline, manifest)
    done: dict[str, bool] = {}
    for req in manifest.get("requirement", []):
        if isinstance(req, dict) and isinstance(req.get("id"), str):
            done[req["id"]] = check_evidence(req, key)[0] == "pass"
    for req in manifest.get("requirement", []):
        if not isinstance(req, dict) or done.get(req.get("id")):
            continue
        if all(done.get(dep, False) for dep in req.get("deps", [])):
            print(req["id"])
            return 0
    print("none")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("audit")
    status = subparsers.add_parser("status")
    status.add_argument("--json", action="store_true")
    check = subparsers.add_parser("check")
    check.add_argument("id")
    subparsers.add_parser("next")
    args = parser.parse_args(argv)
    if args.command == "audit":
        return command_audit()
    if args.command == "status":
        return command_status()
    if args.command == "check":
        return command_check(args.id)
    return command_next()


if __name__ == "__main__":
    raise SystemExit(main())
