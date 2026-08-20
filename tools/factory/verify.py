#!/usr/bin/env python3
"""Mechanical acceptance for one packet inside a lane.

Pipeline: ninja build -> static case-lint (no PyBoy, no registry import) ->
schema audit -> GBRT primary comparison over every case (the central gate's
own comparator, so a packet cannot land something `oracle-fn-all` rejects) ->
PyBoy diff, scoped to the packet's own routines (refresh on case changes,
cached fast path otherwise, live evidence required for acceptance) ->
per-routine mutation RED/PASS -> adapter lint.  Case-lint runs
before the schema audit deliberately: ``tests/routines.py`` eagerly imports
every case module to derive the registry, so a malformed case module (the
exact class of bug case-lint exists to catch) would otherwise crash the
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
        index for index, line in enumerate(lines)
        if "error:" in line or "undefined reference" in line
    ]
    if faults:
        keep: list[str] = []
        for index in faults[:20]:
            if index and "In function" in lines[index - 1]:
                keep.append(lines[index - 1])
            keep.append(lines[index])
            keep.extend(
                line for line in lines[index + 1:index + 3]
                if line[:1].isspace() and "|" in line
            )
        return "\n".join(keep)
    return "\n".join(
        line for line in lines
        if ("warning:" in line or line.startswith("src/") or "In function" in line)
        and " -o " not in line
    ) or output


_FAILURE_CLASSES = {
    "compile": "code", "cases": "translation", "schema": "schema",
    "primary": "code", "diff": "code", "mutation": "code", "lint": "harness",
    "timeout": "infrastructure", "infra-timeout": "infrastructure",
    "infra-error": "infrastructure", "bundle": "bundle", "green": None,
}


def verdict(kind: str, detail: str, routine: str | None = None,
            *, phase: str | None = None, failure_class: str | None = None,
            failing: list[str] | None = None, retryable: bool | None = None) -> dict:
    """Return the stable wire format consumed by recovery and journaling."""
    text = _tail(detail)
    if failure_class is None:
        failure_class = _FAILURE_CLASSES.get(kind, "code" if kind != "green" else None)
    if retryable is None:
        retryable = kind not in {"green"} and failure_class not in {"provider"}
    names = list(failing or ([routine] if routine else []))
    fingerprint = hashlib.sha256(
        json.dumps({"status": kind, "phase": phase or kind,
                    "failure_class": failure_class, "detail": text,
                    "routine": routine, "failing": names},
                   sort_keys=True).encode()).hexdigest()
    return {"status": kind, "phase": phase or kind, "failure_class": failure_class,
            "detail": text, "routine": routine, "failing": names,
            "fingerprint": fingerprint, "retryable": bool(retryable)}

def verdict_v1(result: dict, work_ids: list[str]) -> dict:
    status = str(result.get("status") or "infra-error")
    phase = str(result.get("phase") or status)
    failure_class = result.get("failure_class")
    if not isinstance(failure_class, str):
        failure_class = _FAILURE_CLASSES.get(status, "infrastructure")
    scope = "routine"
    if failure_class in {"harness", "bundle", "infrastructure"}:
        scope = "infrastructure" if failure_class == "infrastructure" else "shared-harness"
    if status == "green":
        retry_action = "accept"
    elif failure_class == "provider":
        retry_action = "backoff"
    elif failure_class in {"schema", "translation"}:
        retry_action = "repair"
    elif failure_class == "infrastructure":
        retry_action = "retry"
    else:
        retry_action = "diagnose"
    detail = str(result.get("detail") or result.get("output") or "")
    summary = detail.splitlines()[0][:400] if detail else status
    evidence = {
        "status": status,
        "phase": phase,
        "detail_sha256": hashlib.sha256(detail.encode()).hexdigest(),
        "tail_sha256": hashlib.sha256(_tail(detail).encode()).hexdigest(),
    }
    stable_signature = {
        "status": status,
        "phase": phase,
        "failure_class": failure_class,
        "scope": scope,
        "work_ids": sorted(work_ids),
        "failing": sorted(str(value) for value in result.get("failing") or []),
    }
    return {
        "status": status,
        "phase": phase,
        "failure_class": failure_class,
        "scope": scope,
        "retry_action": retry_action,
        "work_ids": sorted(work_ids),
        "summary": summary,
        "evidence": evidence,
        "fingerprint": hashlib.sha256(
            json.dumps(stable_signature, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
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
    return [line for line in lines if line][: _DIAGNOSTIC_LIMIT]


def _comparator_witness(output: str, *, routine: str | None = None,
                        index: int | None = None) -> dict:
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
        mismatches = [_normalize_diagnostic(item) for item in mismatches[:_DIAGNOSTIC_LIMIT]]
    else:
        mismatches = _normalize_diagnostic(mismatches)
    witness = {"mismatches": mismatches}
    if case_id:
        witness["case_id"] = case_id
    return witness


def verdict_v2(result: dict, work_ids: list[str], *, phase_seconds: dict[str, float] | None = None) -> dict:
    base = verdict_v1(result, work_ids)
    raw_witness = result.get("witness")
    witness = dict(raw_witness) if isinstance(raw_witness, dict) else {}
    case_id = result.get("case_id")
    if isinstance(case_id, str):
        witness["case_id"] = case_id
    for key in ("expected", "native", "registers", "bus", "mismatches"):
        if key in result and key not in witness:
            witness[key] = result[key]
    witness = _bounded_witness(witness)
    diagnostics = _bounded_diagnostics(result.get("detail") or result.get("output"))
    fingerprint_witness = {
        key: witness[key] for key in ("case_id", "mismatches") if key in witness
    }
    fingerprint = hashlib.sha256(json.dumps({
        "phase": base["phase"],
        "failure_class": base["failure_class"],
        "case_id": fingerprint_witness.get("case_id"),
        "mismatches": fingerprint_witness.get("mismatches", {}),
        "diagnostics": diagnostics,
    }, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "schema": 2,
        "status": "green" if base["status"] == "green" else "red",
        "phase": base["phase"],
        "failure_class": base["failure_class"],
        "scope": base["scope"],
        "retry_action": base["retry_action"],
        "work_ids": base["work_ids"],
        "summary": _normalize_diagnostic(base["summary"]),
        "diagnostics": diagnostics,
        "witness": witness,
        "phase_seconds": phase_seconds or {},
        "fingerprint": fingerprint,
    }


def _bounded_witness(witness: dict) -> dict:
    bounded: dict = {}
    if isinstance(witness.get("case_id"), str):
        bounded["case_id"] = witness["case_id"][:160]
    mismatches = witness.get("mismatches")
    if isinstance(mismatches, dict):
        bounded["mismatches"] = {
            str(k)[:120]: _normalize_diagnostic(v)
            for k, v in list(mismatches.items())[:_DIAGNOSTIC_LIMIT]
        }
    elif isinstance(mismatches, list):
        bounded["mismatches"] = [
            _normalize_diagnostic(item) for item in mismatches[:_DIAGNOSTIC_LIMIT]
        ]
    elif mismatches is not None:
        bounded["mismatches"] = _normalize_diagnostic(mismatches)
    for key in ("expected", "native", "registers", "bus"):
        if key in witness:
            bounded[key] = _normalize_diagnostic(witness[key])
    return bounded


def run(command: list[str], cwd: Path, timeout: float = 600,
        deadline: float | None = None) -> subprocess.CompletedProcess[str]:
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


POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
RESERVED = range(0xCF00, 0xD000)


def case_lint(lane: Path, basename: str, routine_names: list[str],
              module=None) -> dict[str, list[str]]:
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
            AttributeError, ImportError, NameError, OSError, RuntimeError,
            SyntaxError, TypeError, ValueError,
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
        if not any(sum(1 for reg, value in POISON.items()
                       if c.get(reg) == value) >= 4 for c in fn_cases):
            fail(fn, f"CASES[{fn!r}] has no poisoned-register case "
                     f"(need >=4 of a=0xAA f=0xF0 b=0xBB c=0xCC d=0xDD e=0xEE hl=0x1234)")
        for i, c in enumerate(fn_cases):
            for key in ("wram", "read", "expect"):
                for addr in c.get(key, {}) or {}:
                    if int(addr) in RESERVED:
                        fail(fn, f"CASES[{fn!r}][{i}].{key} writes reserved "
                                 f"${int(addr):04X} (oracle call frame $CF00-$CFFF)")
            if c.get("oracle") is False:
                why = c.get("why")
                expects = ("expect", "expect_regs", "expect_sram", "expect_vram")
                if not (isinstance(why, str) and why.strip()):
                    fail(fn, f"CASES[{fn!r}][{i}] has oracle=False without a non-empty why")
                if not any(c.get(k) for k in expects):
                    fail(fn, f"CASES[{fn!r}][{i}] has oracle=False without any of {expects}")
        block = mutations.get(fn)
        if block:
            for case_id in block.get("case_ids") or []:
                match = re.fullmatch(rf"{re.escape(fn)}-(\d+)", str(case_id))
                if not match or not (0 <= int(match.group(1)) < len(fn_cases)):
                    fail(fn, f"MUTATIONS[{fn!r}][case_ids] has invalid id {case_id!r} "
                             f"for {len(fn_cases)} cases")
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


def primary_compare(lane: Path, basename: str, routine_names: list[str],
                    case_counts: dict, deadline: float | None) -> dict | None:
    """Every case, not just the mutation witness: ``oracle-fn-all`` runs them
    all centrally, and a packet that skips one lands a red gate."""
    for fn in routine_names:
        count = case_counts.get(fn)
        if not isinstance(count, int) or count <= 0:
            return verdict("cases", f"SCHEMA2_CASES[{fn!r}] has no cases", fn)
        for index in range(count):
            compared = run(
                [sys.executable, "tools/oracle/gbref/compare_one.py",
                 "--fn", fn, "--index", str(index),
                 "--case", f"tests/cases/{basename}.py",
                 "--rom", str(ROOT / "poketcg/poketcg.gbc"),
                 "--symbols", str(ROOT / "poketcg/poketcg.sym"),
                 "--probe", str(lane / "build" / "poketcg_probe"),
                 "--runner", str(RUNNER)],
                lane, timeout=300, deadline=deadline)
            if compared.returncode == 0:
                continue
            output = compared.stdout + compared.stderr
            if comparison_status(output) is None and not output.startswith("SCHEMA"):
                return verdict("infra-error", _normalize_diagnostic(output), fn)
            result = verdict("primary", f"case {fn}-{index}\n{output}", fn)
            result["case_id"] = f"{fn}-{index}"
            result["witness"] = _comparator_witness(output, routine=fn, index=index)
            result["failing"] = [fn]
            return result
    return None


def verify_packet(packet: dict, lane: Path, cases_changed: bool,
                  deadline: float | None = None, *, progress=None) -> dict:
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
            [sys.executable, str(ROOT / "tools/factory" / "case_inspect.py"),
             "--lane", str(lane), "--basename", basename,
             *[arg for fn in routine_names for arg in ("--fn", fn)]],
            cwd=lane, cap=60, deadline=deadline, check=True,
        )
        inspection = json.loads(inspected.stdout)
    except WaveDeadlineExpired:
        raise
    except PhaseTimeout as exc:
        return verdict("infra-timeout", str(exc))
    except (
        json.JSONDecodeError, OSError, RuntimeError,
        subprocess.SubprocessError, TypeError, ValueError,
    ):
        return verdict("infra-error", traceback.format_exc(limit=2))
    if inspection.get("violations"):
        result = verdict("cases", json.dumps(inspection["violations"], sort_keys=True))
        result["failing"] = sorted(inspection["violations"])
        return result

    if progress:
        progress("audit")
    audit = run([sys.executable, "tools/audit_oracle_cases.py", "--stage", "routine",
                "--only", basename], lane, deadline=deadline)
    if audit.returncode != 0:
        return verdict("schema", audit.stdout + audit.stderr)

    if progress:
        progress("primary")
    primary = primary_compare(lane, basename, routine_names,
                              inspection.get("case_counts") or {}, deadline)
    if primary is not None:
        return primary

    CACHE.mkdir(parents=True, exist_ok=True)
    mode = "refresh" if cases_changed else "cache"
    if progress:
        progress("diff-cache" if mode == "cache" else "diff-refresh")
    diff = run([*ORACLE_PYTHON, "tests/test_leaves.py", *fn_args(routine_names),
                "--oracle-mode", mode, "--cache-dir", str(CACHE),
                "--probe", str(lane / "build" / "poketcg_probe")],
               lane, timeout=1800, deadline=deadline)
    output = diff.stdout + diff.stderr
    if "cache miss" in output:
        mode = "refresh"
        if progress:
            progress("diff-refresh")
        diff = run([*ORACLE_PYTHON, "tests/test_leaves.py", *fn_args(routine_names),
                    "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
                    "--probe", str(lane / "build" / "poketcg_probe")],
                   lane, timeout=1800, deadline=deadline)
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
            l for l in output.splitlines()
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
        live = run([*ORACLE_PYTHON, "tests/test_leaves.py", *fn_args(routine_names),
                    "--oracle-mode", "refresh", "--cache-dir", str(CACHE),
                    "--probe", str(lane / "build" / "poketcg_probe")],
                   lane, timeout=1800, deadline=deadline)
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
                [sys.executable, "tools/run_mutation.py", fn,
                 f"tests/cases/{basename}.py", "--index", str(index),
                 "--build", str(lane / "build"), "--runner", str(RUNNER)],
                lane, timeout=1800, deadline=deadline)
            if mutation_run.returncode != 0:
                return verdict("mutation", mutation_run.stdout + mutation_run.stderr,
                               routine=fn)
    except WaveDeadlineExpired:
        raise
    except PhaseTimeout as exc:
        return verdict("infra-timeout", str(exc))
    except (
        AttributeError, ImportError, NameError, OSError, RuntimeError,
        subprocess.SubprocessError, SyntaxError, TypeError, ValueError,
    ):
        return verdict("infra-error", traceback.format_exc(limit=2))

    if progress:
        progress("lint")
    lint = run(
        ["python3", "tools/lint_adapters.py"],
        lane, timeout=300, deadline=deadline,
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
    rels = [f"src/home/{basename}.c", f"src/home/{basename}.h",
            f"src/probe/{basename}.c", f"tests/cases/{basename}.py"]
    rels += [f"tools/oracle/mutation_receipts/{r['name']}.json"
             for r in packet["routines"]]
    hashes = {}
    for rel in rels:
        path = lane / rel
        if not path.is_file():
            raise RuntimeError(f"bundle input missing: {path}")
        hashes[rel] = _sha256(path)
    return extracted, hashes
