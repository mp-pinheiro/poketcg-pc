#!/usr/bin/env python3
"""Mechanical acceptance for one packet inside a lane.

Pipeline: ninja build -> static case-lint (no PyBoy, no registry import) ->
schema audit -> GBRT primary comparison over records marked primary evidence
(the central gate's own comparator, so a packet cannot land something
`oracle-fn-all` rejects) -> PyBoy diff, scoped to the packet's own routines
(refresh on case changes, cached fast path otherwise, live evidence required
for acceptance) -> per-routine mutation RED/PASS -> adapter lint. Case-lint
runs before the schema audit deliberately: ``tests/routines.py`` eagerly
imports every case module to derive the registry, so a malformed case module
(the exact class of bug case-lint exists to catch) would otherwise crash the
audit subprocess with an opaque traceback instead of a targeted verdict.
Emits a structured verdict; on green, copies the quad + mutation receipts
into .factory/bundles/<id>/.

The verdict "detail" is raw tool output, trimmed — it is the repair-round
feedback payload.

``progress``, when given, is called with a phase name immediately before
each phase starts: "build", "case-inspect", "audit", "primary",
"diff-cache", "diff-refresh", "live", "mutation", "lint". A caller uses it to
emit per-phase timing without changing the verdict.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lanes
from common import (
    CACHE,
    ORACLE_PYTHON,
    ROOT,
    RUNNER,
    PhaseTimeout,
    WaveDeadlineExpired,
    run_bounded,
)

TAIL = 4000
TIMEOUT_MARK = "did not return within"


def _tail(text: str) -> str:
    text = text.strip()
    return text[-TAIL:] if len(text) > TAIL else text


def fn_args(routine_names: list[str]) -> list[str]:
    return [arg for fn in routine_names for arg in ("--fn", fn)]


def compile_cause(output: str) -> str:
    """Errors only when there are any: a lane build emits hundreds of
    ``-Wunused-parameter`` warnings and multi-kB link commands, which used to
    push the actual cause out of the trimmed repair feedback."""
    lines = output.splitlines()
    faults = [
        index
        for index, line in enumerate(lines)
        if "error:" in line or "undefined reference" in line
    ]
    if faults:
        keep: list[str] = []
        for index in faults[:20]:
            if index and "In function" in lines[index - 1]:
                keep.append(lines[index - 1])
            keep.append(lines[index])
            keep.extend(
                line
                for line in lines[index + 1 : index + 3]
                if line[:1].isspace() and "|" in line
            )
        return "\n".join(keep)
    return (
        "\n".join(
            line
            for line in lines
            if ("warning:" in line or line.startswith("src/") or "In function" in line)
            and " -o " not in line
        )
        or output
    )


_FAILURE_CLASSES = {
    "compile": "code",
    "cases": "translation",
    "schema": "schema",
    "primary": "code",
    "diff": "code",
    "mutation": "code",
    "lint": "harness",
    "timeout": "infrastructure",
    "infra-timeout": "infrastructure",
    "infra-error": "infrastructure",
    "bundle": "bundle",
    "green": None,
}


def verdict(
    kind: str,
    detail: str,
    routine: str | None = None,
    *,
    phase: str | None = None,
    failure_class: str | None = None,
    failing: list[str] | None = None,
    retryable: bool | None = None,
) -> dict:
    """Return the stable wire format consumed by recovery and journaling."""
    text = _tail(detail)
    if failure_class is None:
        failure_class = _FAILURE_CLASSES.get(kind, "code" if kind != "green" else None)
    if retryable is None:
        retryable = kind not in {"green"} and failure_class not in {"provider"}
    names = list(failing or ([routine] if routine else []))
    fingerprint = hashlib.sha256(
        json.dumps(
            {
                "status": kind,
                "phase": phase or kind,
                "failure_class": failure_class,
                "detail": text,
                "routine": routine,
                "failing": names,
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()
    return {
        "status": kind,
        "phase": phase or kind,
        "failure_class": failure_class,
        "detail": text,
        "routine": routine,
        "failing": names,
        "fingerprint": fingerprint,
        "retryable": bool(retryable),
    }


_DIAGNOSTIC_LIMIT = 8
_DIAGNOSTIC_CHARS = 320


def _normalize_diagnostic(value: object) -> str:
    """Make tool diagnostics stable and safe for ledger fingerprints."""
    text = str(value or "").replace("\x00", "")
    text = re.sub(r"\b(?:lane|checkout|worktree|build)/[^\s:'\"]+", "<path>", text)
    text = re.sub(r"(?<!\w)(?:[A-Za-z]:)?/[^\s'\"]+", "<path>", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:_DIAGNOSTIC_CHARS]


def _bounded_diagnostics(detail: object) -> list[str]:
    lines = [_normalize_diagnostic(line) for line in str(detail or "").splitlines()]
    return [line for line in lines if line][:_DIAGNOSTIC_LIMIT]


def _comparator_witness(
    output: str, *, routine: str | None = None, index: int | None = None
) -> dict:
    """Extract the comparator's final JSON object without retaining its log."""
    payload = None
    for line in reversed(output.splitlines()):
        try:
            candidate = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            payload = candidate
            break
    case_id = None
    mismatches: object = {}
    if payload:
        case_id = payload.get("case_id") or payload.get("case")
        mismatches = payload.get("mismatches", payload.get("mismatch", {}))
    if not isinstance(case_id, str) and routine is not None and index is not None:
        case_id = f"{routine}-{index}"
    if not isinstance(mismatches, (dict, list, str)):
        mismatches = str(mismatches)
    if isinstance(mismatches, dict):
        mismatches = {
            str(key): _normalize_diagnostic(value)
            for key, value in list(mismatches.items())[:_DIAGNOSTIC_LIMIT]
        }
    elif isinstance(mismatches, list):
        mismatches = [
            _normalize_diagnostic(item) for item in mismatches[:_DIAGNOSTIC_LIMIT]
        ]
    else:
        mismatches = _normalize_diagnostic(mismatches)
    witness = {"mismatches": mismatches}
    if case_id:
        witness["case_id"] = case_id
    return witness


def run(
    command: list[str], cwd: Path, timeout: float = 600, deadline: float | None = None
) -> subprocess.CompletedProcess[str]:
    return run_bounded(command, cwd=cwd, cap=timeout, deadline=deadline, check=False)


def witness_index(mutation_block: dict) -> int:
    ids = mutation_block.get("case_ids") or []
    for case_id in ids:
        match = re.search(r"-(\d+)$", str(case_id))
        if match:
            return int(match.group(1))
    return 0


def load_cases_module(lane: Path, basename: str):
    import importlib.util

    path = lane / "tests" / "cases" / f"{basename}.py"
    spec = importlib.util.spec_from_file_location(f"verify_cases_{basename}", path)
    module = importlib.util.module_from_spec(spec)
    saved = list(sys.path)
    sys.path.insert(0, str(lane))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = saved
    return module


POISON = {
    "a": 0xAA,
    "f": 0xF0,
    "b": 0xBB,
    "c": 0xCC,
    "d": 0xDD,
    "e": 0xEE,
    "hl": 0x1234,
}
# Mirrors tools/oracle/pyboy_oracle.py RESERVED; keep the two in step.
RESERVED = (range(0xCFF0, 0xCFF6), range(0xDC30, 0xDD00))


def reserved_overlap(address: int, size: int) -> range | None:
    return next(
        (
            region
            for region in RESERVED
            if address < region.stop and address + size > region.start
        ),
        None,
    )


def format_reserved() -> str:
    return ", ".join(
        f"${region.start:04X}-${region.stop - 1:04X}" for region in RESERVED
    )


def case_lint(
    lane: Path, basename: str, routine_names: list[str], module=None
) -> dict[str, list[str]]:
    """Mechanical, PyBoy-free checks. Deliberately does not trust the case
    module to import cleanly: an undefined name in it (e.g. a stray C
    `_ADDR` macro referenced as a bare Python identifier — those macros do
    not exist in Python, only inside quoted MUTATIONS text) would otherwise
    crash the schema audit's subprocess too, since ``tests/routines.py``
    eagerly imports every case module to derive the registry. Run this
    before that subprocess."""
    violations: dict[str, list[str]] = {}

    def fail(fn: str, msg: str) -> None:
        violations.setdefault(fn, []).append(msg)

    if module is None:
        try:
            module = load_cases_module(lane, basename)
        except (
            AttributeError,
            ImportError,
            NameError,
            OSError,
            RuntimeError,
            SyntaxError,
            TypeError,
            ValueError,
        ) as exc:
            for fn in routine_names:
                fail(fn, f"case module fails to import: {exc}")
            return violations
    contract = getattr(module, "CONTRACT", {})
    cases = getattr(module, "CASES", {})
    mutations = getattr(module, "MUTATIONS", {})

    for fn in routine_names:
        fn_cases = cases.get(fn, [])
        if fn not in contract:
            fail(fn, f"CONTRACT[{fn!r}] is missing")
            continue
        if not any(
            sum(1 for reg, value in POISON.items() if c.get(reg) == value) >= 4
            for c in fn_cases
        ):
            fail(
                fn,
                f"CASES[{fn!r}] has no poisoned-register case "
                f"(need >=4 of a=0xAA f=0xF0 b=0xBB c=0xCC d=0xDD e=0xEE hl=0x1234)",
            )
        for i, c in enumerate(fn_cases):
            for key in ("wram", "read", "expect"):
                for addr, value in (c.get(key, {}) or {}).items():
                    size = int(value) if key == "read" else len(value)
                    overlap = reserved_overlap(int(addr), size)
                    if overlap is not None:
                        fail(
                            fn,
                            f"CASES[{fn!r}][{i}].{key} overlaps reserved "
                            f"${overlap.start:04X}-${overlap.stop - 1:04X}",
                        )
            if c.get("oracle") is False:
                why = c.get("why")
                expects = ("expect", "expect_regs", "expect_sram", "expect_vram")
                if not (isinstance(why, str) and why.strip()):
                    fail(
                        fn,
                        f"CASES[{fn!r}][{i}] has oracle=False without a non-empty why",
                    )
                if not any(c.get(k) for k in expects):
                    fail(
                        fn,
                        f"CASES[{fn!r}][{i}] has oracle=False without any of {expects}",
                    )
        block = mutations.get(fn)
        if block:
            for case_id in block.get("case_ids") or []:
                match = re.fullmatch(rf"{re.escape(fn)}-(\d+)", str(case_id))
                if not match or not (0 <= int(match.group(1)) < len(fn_cases)):
                    fail(
                        fn,
                        f"MUTATIONS[{fn!r}][case_ids] has invalid id {case_id!r} "
                        f"for {len(fn_cases)} cases",
                    )
    return violations


def comparison_status(output: str) -> str | None:
    for line in reversed(output.splitlines()):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and isinstance(payload.get("status"), str):
            return payload["status"]
    return None


def primary_compare(
    lane: Path,
    basename: str,
    routine_names: list[str],
    case_counts: dict,
    primary_indices: dict[str, list[int]],
    witness_indices: dict[str, list[int]],
    deadline: float | None,
) -> dict | None:
    """Compare only schema-2 records marked as primary evidence."""
    for fn in routine_names:
        count = case_counts.get(fn)
        if not isinstance(count, int) or count <= 0:
            return verdict("cases", f"SCHEMA2_CASES[{fn!r}] has no cases", fn)
        indices = primary_indices.get(fn) or []
        if not indices:
            return verdict(
                "cases",
                "no primary oracle case",
                fn,
                failure_class="unsupported-evidence",
                retryable=False,
            )
        primary_set = set(indices)
        for witness in witness_indices.get(fn) or []:
            if witness not in primary_set:
                return verdict(
                    "cases",
                    f"mutation witness {fn}-{witness} is not primary",
                    fn,
                    failure_class="unsupported-evidence",
                    retryable=False,
                )
        for index in indices:
            compared = run(
                [
                    sys.executable,
                    "tools/oracle/gbref/compare_one.py",
                    "--fn",
                    fn,
                    "--index",
                    str(index),
                    "--case",
                    f"tests/cases/{basename}.py",
                    "--rom",
                    str(ROOT / "poketcg/poketcg.gbc"),
                    "--symbols",
                    str(ROOT / "poketcg/poketcg.sym"),
                    "--probe",
                    str(lane / "build" / "poketcg_probe"),
                    "--runner",
                    str(RUNNER),
                ],
                lane,
                timeout=300,
                deadline=deadline,
            )
            if compared.returncode == 0:
                continue
            output = compared.stdout + compared.stderr
            # Two comparator failures carry no JSON status yet are the
            # candidate's to fix, and reporting them as infrastructure told the
            # next generation nothing. A setup entry naming a routine the probe
            # has no adapter for is a case-authoring error; a probe that never
            # returns is a port that does not terminate.
            unknown_setup = re.search(r"unknown setup routine: (\S+?)\"", output)
            if unknown_setup:
                return verdict(
                    "cases",
                    f"setup routine {unknown_setup.group(1)} has no probe adapter; "
                    "a setup entry may only name an already-ported routine",
                    fn,
                    failure_class="code",
                )
            if "TimeoutExpired" in output:
                return verdict(
                    "primary",
                    f"case {fn}-{index} native probe did not terminate; the C body "
                    "loops forever on state the reference resolves",
                    fn,
                    failure_class="code",
                )
            if comparison_status(output) is None and not output.startswith("SCHEMA"):
                return verdict("infra-error", _normalize_diagnostic(output), fn)
            result = verdict("primary", f"case {fn}-{index}\n{output}", fn)
            result["case_id"] = f"{fn}-{index}"
            result["witness"] = _comparator_witness(output, routine=fn, index=index)
            result["failing"] = [fn]
            return result
    return None


def verify_packet(
    packet: dict,
    lane: Path,
    cases_changed: bool,
    deadline: float | None = None,
    *,
    progress=None,
) -> dict:
    basename = packet["basename"]
    routine_names = [r["name"] for r in packet["routines"]]

    if progress:
        progress("build")
    try:
        built = lanes.build(lane, deadline)
    except (PhaseTimeout, WaveDeadlineExpired) as exc:
        if isinstance(exc, WaveDeadlineExpired):
            raise
        return verdict("infra-timeout", str(exc))
    if built.returncode != 0:
        return verdict("compile", compile_cause(built.stdout + built.stderr))
    probe = lane / "build" / "poketcg_probe"
    if not probe.exists():
        return verdict("compile", f"{probe} was not produced by a successful build")
    if progress:
        progress("case-inspect")
    try:
        inspected = run_bounded(
            [
                sys.executable,
                str(ROOT / "tools/factory" / "case_inspect.py"),
                "--lane",
                str(lane),
                "--basename",
                basename,
                *[arg for fn in routine_names for arg in ("--fn", fn)],
            ],
            cwd=lane,
            cap=60,
            deadline=deadline,
            check=True,
        )
        inspection = json.loads(inspected.stdout)
    except WaveDeadlineExpired:
        raise
    except PhaseTimeout as exc:
        return verdict("infra-timeout", str(exc))
    except (
        json.JSONDecodeError,
        OSError,
        RuntimeError,
        subprocess.SubprocessError,
        TypeError,
        ValueError,
    ):
        return verdict("infra-error", traceback.format_exc(limit=2))
    if inspection.get("violations"):
        result = verdict("cases", json.dumps(inspection["violations"], sort_keys=True))
        result["failing"] = sorted(inspection["violations"])
        return result

    if progress:
        progress("audit")
    audit = run(
        [
            sys.executable,
            "tools/audit_oracle_cases.py",
            "--stage",
            "routine",
            "--only",
            basename,
        ],
        lane,
        deadline=deadline,
    )
    if audit.returncode != 0:
        return verdict("schema", audit.stdout + audit.stderr)

    if progress:
        progress("primary")
    primary = primary_compare(
        lane,
        basename,
        routine_names,
        inspection.get("case_counts") or {},
        inspection.get("primary_indices") or {},
        inspection.get("witness_indices") or {},
        deadline,
    )
    if primary is not None:
        return primary

    CACHE.mkdir(parents=True, exist_ok=True)
    mode = "refresh" if cases_changed else "cache"
    if progress:
        progress("diff-cache" if mode == "cache" else "diff-refresh")
    diff = run(
        [
            *ORACLE_PYTHON,
            "tests/test_leaves.py",
            *fn_args(routine_names),
            "--oracle-mode",
            mode,
            "--cache-dir",
            str(CACHE),
            "--probe",
            str(lane / "build" / "poketcg_probe"),
        ],
        lane,
        timeout=1800,
        deadline=deadline,
    )
    output = diff.stdout + diff.stderr
    if "cache miss" in output:
        mode = "refresh"
        if progress:
            progress("diff-refresh")
        diff = run(
            [
                *ORACLE_PYTHON,
                "tests/test_leaves.py",
                *fn_args(routine_names),
                "--oracle-mode",
                "refresh",
                "--cache-dir",
                str(CACHE),
                "--probe",
                str(lane / "build" / "poketcg_probe"),
            ],
            lane,
            timeout=1800,
            deadline=deadline,
        )
        output = diff.stdout + diff.stderr
    if TIMEOUT_MARK in output:
        spinner = None
        for line in output.splitlines():
            if TIMEOUT_MARK in line:
                match = re.search(r"OracleError: (\S+) did not return", line)
                spinner = match.group(1) if match else None
                break
        return verdict("timeout", output, spinner)
    if diff.returncode != 0:
        failing = "\n".join(
            l
            for l in output.splitlines()
            if l.startswith("FAIL") or "fail " in l or "!=" in l or "Error" in l
        )
        names = re.findall(r"^FAIL (\S+):", output, flags=re.MULTILINE)
        result = verdict("diff", failing or output)
        result["witness"] = _comparator_witness(output)
        result["failing"] = names
        return result
    if mode == "cache":
        if progress:
            progress("live")
        live = run(
            [
                *ORACLE_PYTHON,
                "tests/test_leaves.py",
                *fn_args(routine_names),
                "--oracle-mode",
                "refresh",
                "--cache-dir",
                str(CACHE),
                "--probe",
                str(lane / "build" / "poketcg_probe"),
            ],
            lane,
            timeout=1800,
            deadline=deadline,
        )
        if live.returncode != 0:
            live_witness = _comparator_witness(live.stdout + live.stderr)
            result = verdict("diff", live.stdout + live.stderr)
            result["witness"] = live_witness
            return result
    if progress:
        progress("mutation")
    try:
        module = load_cases_module(lane, basename)
        mutations = getattr(module, "MUTATIONS", {})
        for fn in routine_names:
            mutation = mutations.get(fn)
            if not mutation:
                return verdict("mutation", f"mutation missing for {fn}")
            index = witness_index(mutation)
            mutation_run = run(
                [
                    sys.executable,
                    "tools/run_mutation.py",
                    fn,
                    f"tests/cases/{basename}.py",
                    "--index",
                    str(index),
                    "--build",
                    str(lane / "build"),
                    "--runner",
                    str(RUNNER),
                ],
                lane,
                timeout=1800,
                deadline=deadline,
            )
            if mutation_run.returncode != 0:
                return verdict(
                    "mutation", mutation_run.stdout + mutation_run.stderr, routine=fn
                )
    except WaveDeadlineExpired:
        raise
    except PhaseTimeout as exc:
        return verdict("infra-timeout", str(exc))
    except (
        AttributeError,
        ImportError,
        NameError,
        OSError,
        RuntimeError,
        subprocess.SubprocessError,
        SyntaxError,
        TypeError,
        ValueError,
    ):
        return verdict("infra-error", traceback.format_exc(limit=2))

    if progress:
        progress("lint")
    lint = run(
        ["python3", "tools/lint_adapters.py"],
        lane,
        timeout=300,
        deadline=deadline,
    )
    if lint.returncode != 0:
        return verdict("lint", lint.stdout + lint.stderr, phase="lint")

    if progress:
        progress("complete")
    return verdict("green", output)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_bundle_inputs(packet: dict, lane: Path) -> tuple[dict, dict[str, str]]:
    """Require surgery markers and a complete, importable cases contract."""
    import surgery

    basename = packet["basename"]
    try:
        extracted = surgery.extract(lane, packet)
        module = load_cases_module(lane, basename)
    except Exception as exc:
        raise RuntimeError(f"bundle structural extraction failed: {exc}") from exc
    contract = getattr(module, "CONTRACT", {})
    cases = getattr(module, "CASES", {})
    mutations = getattr(module, "MUTATIONS", {})
    expected = {r["name"] for r in packet["routines"]}
    missing = expected - set(contract) - set(cases) - set(mutations)
    if missing:
        raise RuntimeError(f"bundle contract missing routines: {sorted(missing)}")
    for fn in expected:
        blocks = extracted["routines"].get(fn, {})
        absent = {"C", "H", "PROBE", "CASES", "MUTATION"} - set(blocks)
        if absent:
            raise RuntimeError(f"bundle {fn} missing marker blocks: {sorted(absent)}")
    rels = [
        f"src/home/{basename}.c",
        f"src/home/{basename}.h",
        f"src/probe/{basename}.c",
        f"tests/cases/{basename}.py",
    ]
    rels += [
        f"tools/oracle/mutation_receipts/{r['name']}.json" for r in packet["routines"]
    ]
    hashes = {}
    for rel in rels:
        path = lane / rel
        if not path.is_file():
            raise RuntimeError(f"bundle input missing: {path}")
        hashes[rel] = _sha256(path)
    return extracted, hashes


def _manifest_digest(manifest: dict) -> str:
    value = manifest.get("tree_sha256")
    if isinstance(value, str) and value:
        return value
    return hashlib.sha256(
        json.dumps(
            manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


_SOURCE_PREFIXES = ("src/", "tests/", "tools/", "include/", "docs/", "site/")


def _artifact_reference_valid(root: Path, reference: dict) -> tuple[bool, bool]:
    path_text = reference.get("path")
    digest = reference.get("sha256")
    if not isinstance(path_text, str) or not isinstance(digest, str) or not path_text:
        return False, False
    if path_text.startswith(_SOURCE_PREFIXES):
        return False, False
    path = (root / path_text).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return False, False
    if not path.is_file() or _sha256(path) != digest:
        return False, False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, False
    if not isinstance(payload, dict):
        return False, False
    schema = payload.get("schema")
    if schema == "workflow-command-v1":
        argv = payload.get("argv")
        return (
            isinstance(argv, list) and bool(argv) and payload.get("returncode") == 0,
            True,
        )
    if schema != "workflow-observation-v1":
        return False, False
    files = payload.get("files")
    if not isinstance(files, list) or not files:
        return False, False
    for entry in files:
        if not isinstance(entry, dict):
            return False, False
        nested_path = entry.get("path")
        nested_digest = entry.get("sha256")
        if (
            not isinstance(nested_path, str)
            or not isinstance(nested_digest, str)
            or nested_path.startswith(_SOURCE_PREFIXES)
        ):
            return False, False
        candidate = (root / nested_path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            return False, False
        if not candidate.is_file() or _sha256(candidate) != nested_digest:
            return False, False
    return True, False


def _manifest_has_tree(manifest: dict) -> bool:
    value = manifest.get("tree_sha256")
    return isinstance(value, str) and bool(value)


def integration_check(
    base_manifest: dict,
    candidate_manifest: dict,
    work_results: list[dict],
    *,
    run_dir: Path,
    root: Path = ROOT,
) -> dict:
    root = root.resolve()
    if not isinstance(base_manifest, dict) or not isinstance(candidate_manifest, dict):
        raise ValueError("integration manifests must be objects")
    if not _manifest_has_tree(base_manifest) or not _manifest_has_tree(
        candidate_manifest
    ):
        raise ValueError("integration manifests need source tree identities")
    if not isinstance(work_results, list) or not work_results:
        raise ValueError("integration check requires work results")
    target_witnesses: list[dict] = []
    checks: list[dict] = []
    errors: list[dict] = []
    source_changed = _manifest_digest(base_manifest) != _manifest_digest(
        candidate_manifest
    )
    for result in work_results:
        if not isinstance(result, dict):
            errors.append({"reason": "malformed-work-result"})
            continue
        work_id = result.get("work_id")
        attempt_id = result.get("attempt_id")
        input_digest = result.get("input_digest")
        outcome = result.get("outcome")
        references = result.get("artifact_refs")
        result_errors: list[str] = []
        if not all(
            isinstance(value, str) and value
            for value in (work_id, attempt_id, input_digest)
        ):
            result_errors.append("work identity is malformed")
        if outcome != "progress":
            result_errors.append("work did not report progress")
        if not isinstance(references, list) or not references:
            result_errors.append("work has no measured artifact references")
            valid_refs = False
            has_command = False
        else:
            reference_checks = [
                _artifact_reference_valid(root, reference)
                for reference in references
                if isinstance(reference, dict)
            ]
            valid_refs = len(reference_checks) == len(references) and all(
                valid for valid, _command in reference_checks
            )
            has_command = any(command for _valid, command in reference_checks)
            if not valid_refs:
                result_errors.append(
                    "artifact references are not measured observations"
                )
        argv = result.get("argv")
        returncode = result.get("returncode")
        if not isinstance(argv, list) or not argv or returncode != 0 or not has_command:
            result_errors.append("work has no successful measured command")
        oracles = result.get("oracles")
        requires_bilateral = result.get("bilateral", True)
        if requires_bilateral is not False and (
            not isinstance(oracles, list)
            or not {"native", "reference"}
            <= {str(value).casefold() for value in oracles}
        ):
            result_errors.append("work lacks bilateral native/reference evidence")
        if source_changed:
            paths = result.get("write_paths")
            before = result.get("base_hashes")
            after = result.get("target_hashes")
            if (
                not isinstance(paths, list)
                or not paths
                or not isinstance(before, dict)
                or not isinstance(after, dict)
                or not any(before.get(path) != after.get(path) for path in paths)
            ):
                result_errors.append("source-changing work lacks changed source bytes")
        target_witnesses.append(
            {
                "work_id": work_id,
                "attempt_id": attempt_id,
                "input_digest": input_digest,
                "outcome": outcome,
                "artifact_refs": references,
                "valid": not result_errors,
                "errors": result_errors,
            }
        )
        checks.append(
            {
                "name": "measured-work-contract",
                "argv": argv if isinstance(argv, list) else [],
                "input_digest": input_digest,
                "output_digest": hashlib.sha256(
                    json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest(),
                "outcome": "PASS" if not result_errors else "FAIL",
            }
        )
        errors.extend(
            {"work_id": work_id, "reason": reason} for reason in result_errors
        )
    accepted = bool(target_witnesses) and not errors
    record = {
        "schema": "integration-check-v1",
        "base_tree_sha256": _manifest_digest(base_manifest),
        "candidate_tree_sha256": _manifest_digest(candidate_manifest),
        "native_manifest_sha256": _manifest_digest(
            candidate_manifest.get("native", candidate_manifest)
            if isinstance(candidate_manifest.get("native", candidate_manifest), dict)
            else candidate_manifest
        ),
        "work_ids": [
            result.get("work_id")
            for result in work_results
            if isinstance(result, dict) and isinstance(result.get("work_id"), str)
        ],
        "target_witnesses": target_witnesses,
        "checks": checks,
        "baseline_failures": [],
        "new_failures": errors,
        "regressions": [],
        "accepted": accepted,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "integration-check.json"
    encoded = (
        json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    )
    if path.exists() and path.read_text(encoding="utf-8") != encoded:
        raise ValueError("integration check already exists with different content")
    path.write_text(encoded, encoding="utf-8")
    return record
