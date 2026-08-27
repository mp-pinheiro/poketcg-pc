#!/usr/bin/env python3
"""Reconcile the factory ledgers against the tree.

These failure classes strand the loop without failing anything, so nothing
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
- a staged artifact whose routines have all landed through other artifacts. It
  is skipped by `select_artifacts` forever, yet it kept inflating
  `artifacts_pending` and pinned its basename in the pending-artifact deferral
  set, ordering that basename last in every later selection.

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

LANDINGS_NAME = "landings.jsonl"
REVOCATIONS_NAME = "revocations.jsonl"
QUARANTINE_NAME = "quarantine.jsonl"
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
CLUSTER_RETIRED_PREFIX = "AUTO-RETIRED (cluster): "
# Both machine-written reasons share this stem; a hand-diagnosed blocker never
# starts with it, which is what makes an auto-retirement safe to undo in bulk.
RETIRED_STEM = "AUTO-RETIRED"

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


def _latest_timestamps(path: Path, key: str) -> dict[str, datetime.datetime]:
    """Newest `key` timestamp per artifact_sha256 in a JSONL ledger."""
    latest: dict[str, datetime.datetime] = {}
    for entry in _jsonl(path):
        sha, stamp = entry.get("artifact_sha256"), entry.get(key)
        if not isinstance(sha, str) or not isinstance(stamp, str):
            continue
        try:
            moment = datetime.datetime.fromisoformat(stamp)
        except ValueError:
            continue
        if sha not in latest or moment > latest[sha]:
            latest[sha] = moment
    return latest


def revocations_pending_relanding(root: Path = common.ROOT) -> set[str]:
    """Revoked artifacts that must be selectable again, so they can be re-landed.

    A revocation says a recorded landing never reached the tree, so the payload
    has to be re-grafted. It expires the moment a *terminal disposition* newer
    than it is recorded: a later landing put the payload back, and a later
    quarantine says this artifact will never land - its routines arrived through
    a sibling, or the gate rejected it. Without the quarantine arm a revoked
    artifact whose routines later land elsewhere is un-excluded forever: every
    retirement is undone on the next read, so it can never be retired, it counts
    against `artifacts_pending`, and it pins its basename in the pending-artifact
    deferral set that orders a basename last in selection. A revocation with no
    comparable timestamp keeps the artifact selectable, because losing a landing
    is worse than regrafting one.
    """
    revoked = revoked_artifacts(root)
    if not revoked:
        return revoked
    revocations = _latest_timestamps(root / ".factory" / REVOCATIONS_NAME, "revoked_at")
    settled = _latest_timestamps(root / ".factory" / LANDINGS_NAME, "landed_at")
    for sha, moment in _latest_timestamps(
            root / ".factory" / QUARANTINE_NAME, "quarantined_at").items():
        if sha not in settled or moment > settled[sha]:
            settled[sha] = moment
    return {
        sha for sha in revoked
        if sha not in settled or sha not in revocations
        or revocations[sha] > settled[sha]
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
    for entry in _jsonl(root / ".factory" / LANDINGS_NAME):
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
        # Age decides, candidates included. Exempting an attempt because it holds
        # candidates made every claim a killed session left behind immortal: the
        # candidates are written in minutes, the verification that consumes them
        # takes minutes more, and nothing else ever clears the claim, so four
        # routines sat `issued` with three candidates each and no session alive to
        # verify them. A directory untouched for the whole TTL is a dead session
        # whatever it contains; a live one is writing.
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
# shell or editor that merely mentions a marker is not a candidate. The drivers
# are here too, not just the compute: an orphaned `land.py` keeps running gates
# and writing commits into a repository nobody is watching.
ORPHAN_MARKERS = ("tests/test_leaves.py", "tools/oracle/fn_all.py",
                  "gbref/compare_one.py", "poketcg_probe", "gbref_runner",
                  "factory/land.py", "factory/try_one.py")
# WSL reparents orphans to its own `/init`, not to pid 1, so a reaper is
# recognised by identity rather than by number.
REAPER_NAMES = frozenset({"init", "systemd"})


def _process_command(pid: int) -> str:
    try:
        raw = Path(f"/proc/{pid}/cmdline").read_bytes()
    except OSError:
        return ""
    return raw.replace(b"\0", b" ").decode(errors="replace").strip()


def _process_stat(pid: int) -> tuple[int, int] | None:
    """This process's `(ppid, session id)`, or None if it is already gone."""
    try:
        raw = Path(f"/proc/{pid}/stat").read_text()
    except OSError:
        return None
    try:
        # `comm` is parenthesised and may itself contain spaces and parens, so
        # the fixed fields only start after its final `)`.
        fields = raw[raw.rindex(")") + 2:].split()
        return int(fields[1]), int(fields[3])
    except (ValueError, IndexError):
        return None


def _is_reaper(pid: int) -> bool:
    if pid <= 1:
        return True
    command = _process_command(pid)
    return bool(command) and Path(command.split(" ")[0]).name in REAPER_NAMES


def _is_orphaned(pid: int, ppid: int, sid: int) -> bool:
    """True when no driver is left above this process.

    The direct parent is the wrong thing to ask. `run_bounded` launches
    `uv run ... python tests/test_leaves.py`, so the process that actually burns
    the core is a grandchild: its parent is the `uv` wrapper, which is very much
    alive, and only the wrapper is reparented to init when the driver dies. The
    session is the unit that gets detached (`start_new_session=True` makes the
    wrapper a session leader), so the session leader's parent is the driver, and
    a leader that is gone or reparented means the driver is gone.
    """
    if sid == pid:
        return _is_reaper(ppid)
    leader = _process_stat(sid)
    if leader is None:
        return True
    return _is_reaper(leader[0])


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
        stat = _process_stat(pid)
        if stat is None or not _is_orphaned(pid, *stat):
            continue
        # The detached session leader is the `uv`/shell wrapper around this
        # process. Killing the worker alone usually collapses it, but a wrapper
        # that outlives its child would keep the session alive and hide the next
        # sweep's evidence, so take the whole session down.
        for victim in (pid, stat[1]) if stat[1] != pid else (pid,):
            if apply:
                try:
                    os.kill(victim, signal.SIGKILL)
                except OSError:
                    continue
            killed.append(victim)
        print(f"{prefix}kill {pid} session={stat[1]} orphan={head}")
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
                    f"{CLUSTER_RETIRED_PREFIX}matches {matched['name']} on "
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


def retire_superseded_artifacts(rows: dict[str, dict[str, Any]], *,
                                root: Path = common.ROOT,
                                apply: bool = True) -> list[dict[str, Any]]:
    """Quarantine staged artifacts whose routines have all landed elsewhere.

    A routine can land twice - a stale reissue greens again, or two sessions
    verify the same basename - and `select_artifacts` then skips the loser
    forever, because every routine it carries is already `complete`. Nothing
    retired it, so it inflated `artifacts_pending` and pinned its basename in
    the pending-artifact deferral set, ordering that basename last in every
    later selection. `superseded` is a landing disposition, not a failure.
    """
    import workers

    prefix = "HEAL " if apply else "HEAL would-"
    excluded: set[str] = set()
    for name in (LANDINGS_NAME, QUARANTINE_NAME):
        excluded |= {
            entry["artifact_sha256"]
            for entry in _jsonl(root / ".factory" / name)
            if isinstance(entry.get("artifact_sha256"), str)
        }
    excluded -= revocations_pending_relanding(root)
    retired: list[dict[str, Any]] = []
    for record in workers.artifact_records():
        sha = record["artifact_sha256"]
        if sha in excluded:
            continue
        identity = record.get("identity") or {}
        routines = sorted(
            str(routine["name"])
            for routine in identity.get("routines") or []
            if isinstance(routine, dict) and routine.get("name")
        )
        if not routines:
            continue
        if not all(rows.get(name, {}).get("state") == "complete" for name in routines):
            continue
        entry = {
            "quarantined_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "artifact_sha256": sha,
            "basename": str(identity.get("basename") or ""),
            "failure_class": "superseded",
            "detail": "all routines already landed via other artifacts",
        }
        if apply:
            common.append_jsonl(root / ".factory" / QUARANTINE_NAME, entry)
        retired.append(entry)
        print(f"{prefix}supersede {sha[:16]} {','.join(routines)}")
    return retired


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


_BLOCKED_NAME_LINE = re.compile(r'^\s*name\s*=\s*"(.*?)"\s*$')
# Every diagnostic this un-retirement class can undo, keyed by the subcommand
# value. The value is matched against the machine-written `reason`, which
# quotes the failing payload verbatim.
UNRETIRE_DIAGNOSTICS = {"budget": "BUDGET_EXHAUSTED"}


def _stanza_groups(text: str) -> list[list[str]]:
    """Split blocked.toml into line groups, one per `[[blocked]]` stanza.

    Grouped by lines rather than parsed and re-serialised: the file is 230 KB of
    hand-written diagnosis, and a rewrite would normalise prose only a human
    should touch. Every stanza uses single-line values (name/reason/unblock plus
    a handful of note/workaround), so a group boundary is exactly a line equal
    to `[[blocked]]`. Anything before the first one stays in the leading group.
    """
    groups: list[list[str]] = []
    for line in text.splitlines():
        if line.strip() == "[[blocked]]" or not groups:
            groups.append([])
        groups[-1].append(line)
    return groups


def _group_name(group: list[str]) -> str | None:
    for line in group:
        match = _BLOCKED_NAME_LINE.match(line)
        if match:
            return match.group(1)
    return None


def _drop_stanzas(text: str, names: set[str]) -> tuple[str, list[str]]:
    keep: list[list[str]] = []
    removed: list[str] = []
    for group in _stanza_groups(text):
        name = _group_name(group)
        if name is not None and name in names:
            removed.append(name)
            continue
        keep.append(group)
    body = "\n\n".join("\n".join(group).strip("\n") for group in keep if any(group))
    return (body + "\n" if body else ""), removed


def remove_blockers(names: set[str], root: Path = common.ROOT) -> list[str]:
    """Delete whole `[[blocked]]` stanzas by name, atomically.

    Mirrors append_blockers: the result is re-parsed before it replaces the
    original, so a stanza whose shape line grouping cannot see is skipped by
    name rather than allowed to corrupt 118 others.
    """
    path = root / ".factory" / BLOCKED_NAME
    if not path.is_file() or not names:
        return []
    original = path.read_text()
    text, removed = _drop_stanzas(original, set(names))
    if not removed:
        return []
    try:
        tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        text, removed = original, []
        for name in sorted(names):
            candidate, dropped = _drop_stanzas(text, {name})
            if not dropped:
                continue
            try:
                tomllib.loads(candidate)
            except tomllib.TOMLDecodeError:
                print(f"HEAL unretire-skip {name} "
                      f"reason=stanza is not a single-line group")
                continue
            text = candidate
            removed.extend(dropped)
        if not removed:
            return []
    temp = path.with_name(path.name + ".heal-tmp")
    temp.write_text(text)
    os.replace(temp, path)
    return removed


def unretire_class(diagnostic: str, rows: dict[str, dict[str, Any]], *,
                   root: Path = common.ROOT,
                   apply: bool = True) -> list[str]:
    """Return every routine auto-retired on one diagnostic to the fresh pool.

    Deleting the stanza alone is not enough: a red at or above --retry-limit is
    in neither pool (the fresh one wants None/stale, the retry one wants
    generation < limit), so it would sit `ready` and unselectable until heal
    re-retired it. Those ladders were spent on prompts that never named the
    fix, so the attempt state moves with the stanza - exactly as
    reap_stale_issued does - and issue_attempt carries generation + 1 from a
    stale parent, which buys each routine one directive-informed draw and no
    more. Raising --retry-limit instead would hand every unrelated red eight
    more blind generations.
    """
    import try_one

    marker = UNRETIRE_DIAGNOSTICS[diagnostic]
    path = root / ".factory" / BLOCKED_NAME
    if not path.is_file():
        return []
    names = {
        str(stanza.get("name") or "")
        for stanza in tomllib.loads(path.read_text()).get("blocked", [])
        if str(stanza.get("reason") or "").startswith(RETIRED_STEM)
        and marker in str(stanza.get("reason") or "")
    } - {""}
    prefix = "HEAL " if apply else "HEAL would-"
    states = try_one._current_states()
    if not apply:
        for name in sorted(names):
            print(f"{prefix}unretire {name} "
                  f"generation={states.get(name, {}).get('generation', 0)}")
        return sorted(names)
    removed = remove_blockers(names, root)
    for name in sorted(removed):
        state = states.get(name)
        generation = int((state or {}).get("generation", 0))
        # `rows` was computed before the stanza was removed, so a routine
        # un-retired here still reads `blocked` there; only an already-landed
        # `complete` row must keep its red, since replaying it would claim work
        # the tree has settled.
        if (state is not None and state.get("state") == "red"
                and rows.get(name, {}).get("state") != "complete"):
            refreshed = dict(state)
            refreshed["state"] = "stale"
            try_one._store_current(refreshed)
        print(f"{prefix}unretire {name} generation={generation}")
    return removed


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
    parser.add_argument("--unretire-class", choices=sorted(UNRETIRE_DIAGNOSTICS),
                        help="return routines auto-retired on one diagnostic to "
                             "the fresh pool, once the prompt names its remedy")
    arguments = parser.parse_args(argv)
    if arguments.retry_limit < 1:
        parser.error("--retry-limit must be at least 1")
    if arguments.ttl_hours <= 0:
        parser.error("--ttl-hours must be positive")
    if arguments.sweep_only and arguments.unretire_class:
        parser.error("--sweep-only touches no ledger; it cannot un-retire")

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
        # Before retiring: an un-retired routine leaves `red`, so this run's
        # retire pass no longer sees it, and the cluster index it reads is the
        # one this removal produced.
        unretired = (
            unretire_class(arguments.unretire_class, rows, root=root,
                           apply=arguments.apply)
            if arguments.unretire_class else []
        )
        retired = retire_exhausted_reds(
            try_one._current_states(), rows,
            retry_limit=arguments.retry_limit, root=root, apply=arguments.apply,
        )
        superseded = retire_superseded_artifacts(
            rows, root=root, apply=arguments.apply,
        )
    _lost, half = lost_landings(root)
    dirty = 1 if ((retired or unretired) and arguments.apply) else 0
    print(
        f"HEAL status landed={len(landed)} reaped={len(reaped)} "
        f"revoked={len(revoked)} retired={len(retired)} "
        f"superseded={len(superseded)} unretired={len(unretired)} "
        f"half_landed={len(half)} orphans={len(orphans)} "
        f"blocked_toml_dirty={dirty}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
