#!/usr/bin/env python3
"""Reconcile the factory ledgers against the tree.

Three failure classes strand the loop without failing anything, so nothing
retries them and `factory-next` reports work in flight forever:

- a landing recorded in `.factory/landings.jsonl` whose marker blocks are not in
  the tree (an orphaned publication commit, a hand-rebase that dropped a commit,
  or a whole-file copy that erased a sibling). `select_artifacts` excludes the
  artifact because the ledger names it, and the fresh pool excludes the routine
  because its attempt is `green`;
- an `issued` attempt whose routine can never be dispatched again, because it
  picked up an operational blocker or left the ready frontier. It counts as
  `active`, so the loop reports `active` instead of `stalled`;
- a `red` attempt that both selection pools have abandoned - retry budget spent
  or the same diagnostic twice - with no blocker recorded, so it keeps inflating
  `ready` and its dependents stay stranded.

Every repair is derived from on-disk evidence, never from a heuristic about what
a routine "should" be. Only `.factory/blocked.toml` is git-tracked under
`.factory/`, so reaping and revoking never dirty the checkout and can run inline
in selection; retiring a red writes that file and therefore runs only from this
command.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common
import packet as packet_mod

REVOCATIONS_NAME = "revocations.jsonl"
BLOCKED_NAME = "blocked.toml"
DEFAULT_TTL_SECONDS = 21600.0  # 6h; a live wave settles in minutes
DEFAULT_RETRY_LIMIT = 8  # must match try_one.main's --retry-limit default
RETIRED_PREFIX = "AUTO-RETIRED: "

# Both markers require a space after `factory`, so `factory-mutation`,
# `factory-completion` and `factory-cases-statics` never match. The statics
# block does share the C shape, so it is discarded by name.
C_MARKER = re.compile(r"^/\* >>> factory ([A-Za-z_][\w.]*) \*/$", re.MULTILINE)
PY_MARKER = re.compile(r"^# >>> factory ([A-Za-z_][\w.]*)$", re.MULTILINE)


def _now_iso() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat()


def marker_census(root: Path = common.ROOT) -> tuple[set[str], set[str]]:
    """(routines with a C block under src/home, routines with a cases block)."""
    c_names: set[str] = set()
    py_names: set[str] = set()
    home = root / "src" / "home"
    if home.is_dir():
        for path in sorted(home.glob("*.c")):
            c_names.update(C_MARKER.findall(path.read_text(errors="replace")))
    cases = root / "tests" / "cases"
    if cases.is_dir():
        for path in sorted(cases.glob("*.py")):
            if path.name.startswith("_"):
                continue
            py_names.update(PY_MARKER.findall(path.read_text(errors="replace")))
    c_names.discard("statics")
    py_names.discard("statics")
    return c_names, py_names


def _jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict):
            records.append(entry)
    return records


def revoked_artifacts(root: Path = common.ROOT) -> set[str]:
    """artifact_sha256 values recorded in .factory/revocations.jsonl."""
    return {
        entry["artifact_sha256"]
        for entry in _jsonl(root / ".factory" / REVOCATIONS_NAME)
        if isinstance(entry.get("artifact_sha256"), str)
    }


def lost_landings(root: Path = common.ROOT) -> tuple[list[dict[str, Any]], list[str]]:
    """(artifacts whose landed routines vanished, routines present in one half).

    A routine missing from both censuses was published and then lost; its
    artifact payload is immutable, so re-landing it is cheaper and safer than
    re-porting. A routine missing from exactly one census is a broken quartet,
    not a lost landing: the gate diagnoses that, and grafting half a routine back
    would hide it.
    """
    import workers

    c_names, py_names = marker_census(root)
    already = revoked_artifacts(root)
    lost: list[dict[str, Any]] = []
    half: list[str] = []
    for entry in _jsonl(root / ".factory" / "landings.jsonl"):
        sha = entry.get("artifact_sha256")
        claimed = entry.get("routines")
        if not isinstance(sha, str) or not isinstance(claimed, list):
            continue
        names = [name for name in claimed if isinstance(name, str)]
        absent = [n for n in names if n not in c_names and n not in py_names]
        half.extend(n for n in names if (n in c_names) != (n in py_names))
        if not absent or sha in already:
            continue
        if not workers.artifact_exists(sha):
            continue
        lost.append({
            "artifact_sha256": sha,
            "basename": str(entry.get("basename") or ""),
            "routines": sorted(absent),
        })
    return lost, sorted(set(half))


def revoke_lost_landings(root: Path = common.ROOT, *,
                         apply: bool = True) -> list[dict[str, Any]]:
    """Un-exclude every intact artifact whose landing never reached the tree.

    A revocation is the only thing that lets `select_artifacts` offer a recorded
    landing again, and `_artifact_attempted_names` stop treating its routines as
    already attempted.
    """
    lost, half = lost_landings(root)
    prefix = "HEAL " if apply else "HEAL would-"
    for name in half:
        print(f"{prefix}half-landed {name}")
    records: list[dict[str, Any]] = []
    for item in lost:
        record = {
            "revoked_at": _now_iso(),
            "artifact_sha256": item["artifact_sha256"],
            "basename": item["basename"],
            "routines": item["routines"],
            "reason": "landed content is absent from the tree",
        }
        if apply:
            common.append_jsonl(root / ".factory" / REVOCATIONS_NAME, record)
        records.append(record)
        print(f"{prefix}revoke {item['artifact_sha256'][:16]} "
              f"{','.join(item['routines'])}")
    return records


def _attempt_dir(fn: str, attempt_id: str) -> Path:
    # try_one.TRY_ROOT is the single source of truth for attempt storage, and the
    # rehearsal harness repoints it at a temp tree; rebuilding the path from a
    # root argument would make every relocated attempt look abandoned.
    import try_one

    return try_one.TRY_ROOT / fn / "attempts" / attempt_id


def _reap_reason(fn: str, state: dict[str, Any], rows: dict[str, dict[str, Any]],
                 *, ttl_seconds: float) -> str | None:
    row = rows.get(fn)
    if row is None:
        return "not-ready"
    if row.get("operational_blocker"):
        return "blocked"
    if row.get("state") != "ready":
        return "not-ready"
    import try_one

    attempt = _attempt_dir(fn, str(state["attempt_id"]))
    if attempt.is_dir():
        if (attempt / "result.json").is_file() or any(attempt.glob("candidate-*.json")):
            return None
        newest = max((path.stat().st_mtime for path in attempt.rglob("*")),
                     default=attempt.stat().st_mtime)
    else:
        # A claim with no attempt directory ages from its own current.json rather
        # than being reaped on sight: issuance writes both, so only a claim that
        # is also old proves the issuing session died. Reaping a fresh one would
        # hand another session the basename this one already owns.
        marker = try_one._current_path(fn)
        if not marker.is_file():
            return None
        newest = marker.stat().st_mtime
    age = datetime.datetime.now(datetime.UTC).timestamp() - newest
    return "abandoned" if age > ttl_seconds else None


def reap_stale_issued(states: dict[str, dict[str, Any]],
                      rows: dict[str, dict[str, Any]], *,
                      ttl_seconds: float = DEFAULT_TTL_SECONDS,
                      apply: bool = True) -> list[str]:
    """Flip `issued` attempts that can never be verified back to `stale`.

    `stale` rather than deleted: the non-retry pool accepts `None` and `stale`,
    and issue_attempt carries the generation forward from a stale parent, so a
    reaped routine re-enters selection with its history intact the moment its
    blocker clears.
    """
    import try_one

    prefix = "HEAL " if apply else "HEAL would-"
    reaped: list[str] = []
    for fn in sorted(states):
        state = states[fn]
        if state.get("state") != "issued":
            continue
        reason = _reap_reason(fn, state, rows, ttl_seconds=ttl_seconds)
        if reason is None:
            continue
        if apply:
            current = dict(state)
            current["state"] = "stale"
            try_one._store_current(current)
        reaped.append(fn)
        print(f"{prefix}reap {fn} reason={reason}")
    return reaped


def _last_diagnostic(fn: str, state: dict[str, Any]) -> tuple[str, str, str]:
    path = _attempt_dir(fn, str(state["attempt_id"])) / "result.json"
    try:
        results = json.loads(path.read_text()).get("results") or []
    except (OSError, json.JSONDecodeError, ValueError, AttributeError):
        return "unknown", "unknown", "unknown"
    for entry in reversed(results):
        if isinstance(entry, dict):
            return (str(entry.get("phase", "unknown")),
                    str(entry.get("failure_class", "unknown")),
                    str(entry.get("detail", "unknown")))
    return "unknown", "unknown", "unknown"


def _context_is_stale(fn: str) -> bool:
    """True when this red's recorded translation context no longer matches the
    tree, so its spent budget is evidence about a tree that no longer exists.

    An exhausted red is normally retired to a blocker, but a routine whose
    blocker was just cleared, or whose callees have since landed, is being judged
    on attempts it never had a fair chance at. Rebuilding the packet is the same
    comparison `factory-try` makes before it verifies a candidate.
    """
    import try_one

    try:
        issued = try_one.load_current_attempt(fn)
        if issued is None:
            return False
        return try_one.verification_packet(issued) is None
    except (LookupError, OSError, RuntimeError, ValueError):
        return False


def retire_exhausted_reds(states: dict[str, dict[str, Any]],
                          rows: dict[str, dict[str, Any]], *,
                          retry_limit: int = DEFAULT_RETRY_LIMIT,
                          root: Path = common.ROOT,
                          apply: bool = True) -> list[dict[str, Any]]:
    """Record a blocker for every red both selection pools have abandoned.

    Without this the routine stays `ready` forever: the fresh pool rejects it
    because an artifact attempt exists, the retry pool rejects it as exhausted or
    trapped, and every routine that depends on it is stranded behind a frontier
    entry that will never be selected.
    """
    import try_one

    prefix = "HEAL " if apply else "HEAL would-"
    entries: list[dict[str, Any]] = []
    for fn in sorted(states):
        state = states[fn]
        if state.get("state") != "red":
            continue
        row = rows.get(fn)
        if row is None or row.get("state") != "ready" or row.get("operational_blocker"):
            continue
        generation = int(state.get("generation", 0))
        trapped = try_one.is_trapped(fn, state)
        if generation < retry_limit and not trapped:
            continue
        if _context_is_stale(fn):
            if apply:
                refreshed = dict(state)
                refreshed["state"] = "stale"
                try_one._store_current(refreshed)
            print(f"{prefix}refresh {fn} generation={generation} "
                  f"detail=translation context changed since its last attempt")
            continue
        phase, failure_class, detail = _last_diagnostic(fn, state)
        source = str(row.get("source") or "")
        entries.append({
            "name": fn,
            "reason": (
                f"{RETIRED_PREFIX}{source}:{row.get('line')} "
                f"(basename `{Path(source).stem}`). {generation + 1} generations "
                f"exhausted (trapped={trapped}); last diagnostic "
                f"phase={phase} failure_class={failure_class} detail={detail}"
            ),
            "unblock": (
                f"read the recorded diagnostics under .factory/try/{fn}/attempts/ "
                f"and replace this machine-generated note with a diagnosed "
                f"capability blocker, or delete the entry to retry once that gap "
                f"closes"
            ),
        })
        print(f"{prefix}retire {fn} generation={generation} trapped={trapped}")
    if entries and apply:
        append_blockers(entries, root)
    return entries


def _toml_string(text: str) -> str:
    """A single-line TOML basic string.

    TOML basic-string escapes are a superset of JSON's for ASCII, and every
    stanza already in blocked.toml is a single-line basic string, so json.dumps
    of a newline-free, length-bounded value round-trips through tomllib.
    """
    flat = " ".join(str(text).split())
    return json.dumps(flat[:1500], ensure_ascii=True)


def append_blockers(entries: list[dict[str, Any]],
                    root: Path = common.ROOT) -> None:
    """Append `[[blocked]]` stanzas, atomically, never rewriting existing prose.

    blocked.toml is 230 KB of hand-written diagnosis and report.py hard-fails on
    a duplicate name, so the appended file is re-parsed and duplicate-checked
    before it replaces the original.
    """
    path = root / ".factory" / BLOCKED_NAME
    original = path.read_text() if path.is_file() else ""
    chunks = [original.rstrip("\n")] if original.strip() else []
    for entry in entries:
        chunks.append(
            "[[blocked]]\n"
            f"name = {_toml_string(entry['name'])}\n"
            f"reason = {_toml_string(entry['reason'])}\n"
            f"unblock = {_toml_string(entry['unblock'])}"
        )
    text = "\n\n".join(chunks) + "\n"
    parsed = tomllib.loads(text)
    names = [row.get("name") for row in parsed.get("blocked", [])]
    if len(names) != len(set(names)):
        duplicates = sorted({n for n in names if names.count(n) > 1})
        raise ValueError(f"appending would duplicate blocked names: {duplicates}")
    temp = path.with_name(path.name + ".heal-tmp")
    temp.write_text(text)
    os.replace(temp, path)


def _work_records() -> list[dict[str, Any]]:
    report = packet_mod.report_module()
    return report.compute(report.load_inventory(), report.load_routines()[0],
                          report.load_gate())["work_records"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="perform the repairs instead of listing them")
    parser.add_argument("--retry-limit", type=int, default=DEFAULT_RETRY_LIMIT,
                        help="generation at which a red is retired to a blocker")
    parser.add_argument("--ttl-hours", type=float, default=DEFAULT_TTL_SECONDS / 3600,
                        help="age at which a candidate-less issued attempt is reaped")
    arguments = parser.parse_args(argv)
    if arguments.retry_limit < 1:
        parser.error("--retry-limit must be at least 1")
    if arguments.ttl_hours <= 0:
        parser.error("--ttl-hours must be positive")

    import try_one

    root = common.ROOT
    rows = {str(row["name"]): row for row in _work_records()}
    # The same lock issuance takes: a reap must not interleave with a selection
    # that is about to claim the routine it is reaping.
    with common.file_lock(common.locks_dir(root) / "select.lock", timeout=900):
        reaped = reap_stale_issued(
            try_one._current_states(), rows,
            ttl_seconds=arguments.ttl_hours * 3600,
            apply=arguments.apply,
        )
        revoked = revoke_lost_landings(root, apply=arguments.apply)
        retired = retire_exhausted_reds(
            try_one._current_states(), rows,
            retry_limit=arguments.retry_limit, root=root, apply=arguments.apply,
        )
    _lost, half = lost_landings(root)
    print(
        f"HEAL status reaped={len(reaped)} revoked={len(revoked)} "
        f"retired={len(retired)} half_landed={len(half)} "
        f"blocked_toml_dirty={1 if (retired and arguments.apply) else 0}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
