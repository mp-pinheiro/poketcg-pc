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

Compute outlives its driver too: `run_bounded` detaches every child into its own
session, so a driver that dies abruptly leaves PyBoy and probe processes pinned
to a core with nothing left to read them. Those are killed on sight, and
`--sweep-only` does that and nothing else.

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
import signal
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
# Must match try_one.main's --retry-limit default. The generation ceiling is not
# the waste guard - is_trapped is, and it retires any red that repeats one
# diagnostic whatever its generation. The ceiling only reaches routines that
# keep producing NEW diagnostics, which is to say the ones still converging:
# PracticeDuel_RepeatInstructions greened at generation 8, and OpenCardPage
# passed its oracle comparison at generation 11. A ceiling of 8 retired both of
# those a wave or two before they were done.
DEFAULT_RETRY_LIMIT = 16
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


def reconcile_landed(states: dict[str, dict[str, Any]],
                     rows: dict[str, dict[str, Any]], *,
                     apply: bool = True) -> list[str]:
    """Retire attempt state for routines the tree has already landed.

    Two sessions land into one tree, so a routine can be published while another
    session still holds a `red` or `issued` current.json for it. Nothing else
    clears that: `reap_stale_issued` only ages `issued` claims and never looks at
    a `red`, and `retire_exhausted_reds` waits for the retry ceiling. Until it is
    cleared the routine is offered by every retry pass, `resolve` rejects it as
    `already-implemented`, and the discarded attempt still consumes its
    basename's per-call selection slot -- a claim that can never be satisfied and
    never expires.

    The work record decides, not a marker census: `state == "complete"` is the
    same verdict the release gate and the dashboard read, and it holds for a
    routine whose cases module predates the `# >>> factory` convention. Age and
    generation are irrelevant here -- completeness is a property of the tree.
    """
    import try_one

    prefix = "HEAL " if apply else "HEAL would-"
    reconciled: list[str] = []
    for fn in sorted(states):
        state = states[fn]
        if state.get("state") not in ("red", "issued"):
            continue
        row = rows.get(fn)
        if row is None or row.get("state") != "complete":
            continue
        if apply:
            current = dict(state)
            current["state"] = "stale"
            try_one._store_current(current)
        reconciled.append(fn)
        print(f"{prefix}landed {fn} was={state.get('state')}")
    return reconciled


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


# Factory compute is worth killing on sight once its driver is gone. `common.
# run_bounded` starts every child in its own session (`start_new_session=True`)
# so a killed session leader never drags the tree down with it, and its
# `_stop_process_tree` only runs while the driver itself is alive. A driver that
# dies abruptly -- SIGKILL, a cancelled tool call, a compacted session -- leaves
# PyBoy and probe processes spinning against unlinked temp files that nothing
# will ever read. One sweep of this class recovered 12 CPU-hours and two of six
# cores.
#
# Matched against the first two argv tokens, never the whole command line, so a
# shell or editor that merely mentions a marker is not a candidate.
ORPHAN_MARKERS = ("tests/test_leaves.py", "tools/oracle/fn_all.py",
                  "gbref/compare_one.py", "poketcg_probe", "gbref_runner")
# WSL reparents orphans to its own `/init`, not to pid 1, so orphanhood is the
# parent's identity rather than its number.
REAPER_NAMES = frozenset({"init", "systemd"})


def _process_command(pid: int) -> str:
    try:
        raw = Path(f"/proc/{pid}/cmdline").read_bytes()
    except OSError:
        return ""
    return raw.replace(b"\0", b" ").decode(errors="replace").strip()


def _process_parent(pid: int) -> int | None:
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("PPid:"):
                return int(line.split()[1])
    except (OSError, ValueError):
        return None
    return None


def _parent_is_reaper(pid: int) -> bool:
    if pid <= 1:
        return True
    command = _process_command(pid)
    return bool(command) and Path(command.split(" ")[0]).name in REAPER_NAMES


def reap_orphan_processes(apply: bool = True) -> list[int]:
    """SIGKILL factory compute whose driver is no longer there to read it."""
    prefix = "HEAL " if apply else "HEAL would-"
    killed: list[int] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        if pid == os.getpid():
            continue
        command = _process_command(pid)
        head = " ".join(command.split(" ")[:2])
        if not any(marker in head for marker in ORPHAN_MARKERS):
            continue
        parent = _process_parent(pid)
        if parent is None or not _parent_is_reaper(parent):
            continue
        if apply:
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                continue
        killed.append(pid)
        print(f"{prefix}kill {pid} orphan={head}")
    return killed


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

# Cross-routine trap short-circuit: a red whose diagnostic names a harness
# failure identity (status, pc) already documented by several blocked.toml
# stanzas is rediscovering a known root cause; retire it immediately instead of
# burning its remaining generations (12 attempts were spent re-deriving the
# AIPlay_* root cause on AITryToRetreat alone). Guards: only hang statuses
# cluster (ordinary PORT mismatches also print a pc), the pc must
# match exactly and be nonzero (pc drifts across siblings of one root cause,
# so an exact repeat at one nonzero pc across two routines is already strong;
# pc=0 is a missing-value artifact), at least _CLUSTER_MIN_STANZAS stanzas
# must already name the identity, and generations 0-1 always get their honest
# retry.
#
# REFERENCE_DIVERGENCE is deliberately NOT clustered. compare_one.py only
# reaches that branch after the reference ran to completion, so its pc is the
# sentinel rather than a hang site, and the mismatch is always the candidate's
# own CONTRACT declaring `preserve` for a register the ROM clobbers. Clustering
# it retired three fixable routines (CreditsSequenceCmd_LoadScene,
# _PauseMenu_Diary, Func_5a81) at generation 2 instead of letting the corrected
# feedback land.
_CLUSTER_STATUS = re.compile(r"BUDGET_EXHAUSTED")
_CLUSTER_PC = re.compile(r"[\"']?pc[\"']?\s*[:=]\s*(\d+)")
_CLUSTER_MIN_STANZAS = 2
_CLUSTER_MIN_GENERATION = 2


def _cluster_keys(text: str) -> set[tuple[str, int]]:
    """(status, pc) harness-failure identities named in `text`."""
    statuses = set(_CLUSTER_STATUS.findall(text))
    pcs = {int(pc) for pc in _CLUSTER_PC.findall(text) if int(pc) != 0}
    return {(status, pc) for status in statuses for pc in pcs}


def _blocked_cluster_index(root: Path) -> dict[tuple[str, int], dict[str, Any]]:
    """Map documented (status, pc) identities to their first stanza and count."""
    path = root / ".factory" / BLOCKED_NAME
    if not path.is_file():
        return {}
    index: dict[tuple[str, int], dict[str, Any]] = {}
    for stanza in tomllib.loads(path.read_text()).get("blocked", []):
        reason = str(stanza.get("reason") or "")
        phase = re.search(r"phase=([\w-]+)", reason)
        for key in _cluster_keys(reason):
            row = index.setdefault(key, {
                "name": str(stanza.get("name") or ""),
                "unblock": str(stanza.get("unblock") or ""),
                "phase": phase.group(1) if phase else "",
                "count": 0,
            })
            row["count"] += 1
    return index


def _cluster_match(index: dict[tuple[str, int], dict[str, Any]], fn: str,
                   phase: str, detail: str) -> tuple[tuple[str, int], dict[str, Any]] | None:
    """First documented identity this diagnostic rediscovers, if any."""
    for key in sorted(_cluster_keys(str(detail or ""))):
        row = index.get(key)
        if row is None or row["count"] < _CLUSTER_MIN_STANZAS:
            continue
        if row["name"] == fn:
            continue
        if row["phase"] and phase and row["phase"] != phase:
            continue
        return key, row
    return None


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
    cluster_index = _blocked_cluster_index(root)
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
        phase, failure_class, detail = _last_diagnostic(fn, state)
        cluster = None
        if generation >= _CLUSTER_MIN_GENERATION:
            cluster = _cluster_match(cluster_index, fn, phase, detail)
        if generation < retry_limit and not trapped and cluster is None:
            continue
        if _context_is_stale(fn):
            if apply:
                refreshed = dict(state)
                refreshed["state"] = "stale"
                try_one._store_current(refreshed)
            print(f"{prefix}refresh {fn} generation={generation} "
                  f"detail=translation context changed since its last attempt")
            continue
        source = str(row.get("source") or "")
        if cluster is not None:
            (status, pc), matched = cluster
            entries.append({
                "name": fn,
                "reason": (
                    f"AUTO-RETIRED (cluster): matches {matched['name']} on "
                    f"{status} pc={pc} ({matched['count']} stanzas). "
                    f"{source}:{row.get('line')} (basename `{Path(source).stem}`). "
                    f"generation={generation}; last diagnostic phase={phase} "
                    f"failure_class={failure_class} detail={detail}"
                ),
                "unblock": matched["unblock"],
            })
            print(f"{prefix}cluster-retired {fn} matches={matched['name']}")
            continue
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
    parser.add_argument("--sweep-only", action="store_true",
                        help="only kill orphaned factory compute, touch no ledger")
    arguments = parser.parse_args(argv)
    if arguments.retry_limit < 1:
        parser.error("--retry-limit must be at least 1")
    if arguments.ttl_hours <= 0:
        parser.error("--ttl-hours must be positive")

    # Outside the lock: killing compute nobody is waiting on touches no ledger,
    # and it must still happen when the ledger repairs below cannot run.
    orphans = reap_orphan_processes(apply=arguments.apply or arguments.sweep_only)
    if arguments.sweep_only:
        print(f"HEAL status orphans={len(orphans)}")
        return 0

    import try_one

    root = common.ROOT
    rows = {str(row["name"]): row for row in _work_records()}
    # The same lock issuance takes: a reap must not interleave with a selection
    # that is about to claim the routine it is reaping.
    with common.file_lock(common.locks_dir(root) / "select.lock", timeout=900):
        # Before ageing or retiring anything: a claim on an already-landed
        # routine is settled by the tree, not by its own age or generation.
        landed = reconcile_landed(try_one._current_states(), rows,
                                  apply=arguments.apply)
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
        f"HEAL status landed={len(landed)} reaped={len(reaped)} "
        f"revoked={len(revoked)} retired={len(retired)} half_landed={len(half)} "
        f"orphans={len(orphans)} "
        f"blocked_toml_dirty={1 if (retired and arguments.apply) else 0}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
