"""Deterministic factory metrics snapshot.

Prints one `key=value` line per metric so successive runs diff cleanly.
Reads recorded state only: `.factory/landings.jsonl`, `.factory/blocked.toml`,
`.factory/try/*/current.json` (+ newest attempt artifacts), and
`site/data/progress.json`. Writes nothing.

Window metrics use the wall clock, so an idle fleet shows falling rates and a
growing trailing stall. `stall_minutes_24h` sums inter-landing gaps over 30
minutes inside the last 24 h, including the trailing gap from the newest
landing to now.
"""

from __future__ import annotations

import contextlib
import datetime
import io
import itertools
import json
import re
import statistics
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANDINGS = ROOT / ".factory" / "landings.jsonl"
BLOCKED = ROOT / ".factory" / "blocked.toml"
TRY_DIR = ROOT / ".factory" / "try"
PROGRESS = ROOT / "site" / "data" / "progress.json"

STALL_GAP = datetime.timedelta(minutes=30)

# Diagnostic signatures that name a harness/capability gap rather than a
# translation bug; keep in sync with the recurring `.factory/blocked.toml`
# stanza classes. REFERENCE_DIVERGENCE is excluded on purpose: it means the
# case declared `preserve` for a register the real ROM does not preserve, which
# the candidate can repair from the diagnostic alone.
STRUCTURAL = re.compile(
    r"BUDGET_EXHAUSTED|hBankROM|DoFrameIfLCDEnabled"
    r"|\$CF[0-9A-Fa-f]{2}|0xCF[0-9A-Fa-f]{2}|reserved window",
)


def _parse(value: str | int | float) -> datetime.datetime:
    if isinstance(value, (int, float)):
        return datetime.datetime.fromtimestamp(value, tz=datetime.UTC)
    stamp = datetime.datetime.fromisoformat(value)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=datetime.UTC)
    return stamp


def _frontier() -> tuple[int, int]:
    """Rows and distinct basenames the selector can actually issue from."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sink = io.StringIO()
    try:
        with contextlib.redirect_stdout(sink):
            import packet as packet_mod
            report = packet_mod.report_module()
            records = report.compute(report.load_inventory(),
                                     report.load_routines()[0],
                                     report.load_gate())["work_records"]
    except Exception:
        return -1, -1
    rows = [r for r in records if r.get("state") == "ready"]
    return len(rows), len({Path(r["source"]).stem for r in rows if r.get("source")})


def _pending_artifacts() -> int:
    """Staged artifacts not yet landed or quarantined; revoked ones re-pend."""
    art = ROOT / ".factory" / "artifacts"
    if not art.is_dir():
        return 0
    excluded: set[str] = set()
    revoked: set[str] = set()
    for name, sink in (("landings.jsonl", excluded),
                       ("quarantine.jsonl", excluded),
                       ("revocations.jsonl", revoked)):
        path = ROOT / ".factory" / name
        if not path.is_file():
            continue
        for line in path.read_text().splitlines():
            try:
                sha = json.loads(line).get("artifact_sha256")
            except json.JSONDecodeError:
                continue
            if isinstance(sha, str):
                sink.add(sha)
    excluded -= revoked
    return sum(1 for p in art.iterdir()
               if p.is_dir() and p.name not in excluded)


def _load_landings() -> list[dict]:
    if not LANDINGS.is_file():
        return []
    records = []
    for line in LANDINGS.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record.get("landed_at"), str):
            records.append(record)
    return records


def _batches(records: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for record in records:
        key = record.get("batch_id") or record["artifact_sha256"]
        grouped.setdefault(key, []).append(record)
    batches = []
    for recs in grouped.values():
        batches.append({
            "at": max(_parse(r["landed_at"]) for r in recs),
            "routines": [name for r in recs for name in r.get("routines", [])],
            "seconds_gate": float(recs[0].get("seconds_gate") or 0.0),
        })
    batches.sort(key=lambda b: b["at"])
    return batches


def _sizes() -> dict[str, dict]:
    if not PROGRESS.is_file():
        return {}
    functions = json.loads(PROGRESS.read_text()).get("functions", [])
    return {fn["name"]: fn for fn in functions if isinstance(fn, dict) and "name" in fn}


def _pool() -> dict[str, list[Path]]:
    pool: dict[str, list[Path]] = {}
    if not TRY_DIR.is_dir():
        return pool
    for current in sorted(TRY_DIR.glob("*/current.json")):
        try:
            state = json.loads(current.read_text()).get("state", "unknown")
        except (OSError, json.JSONDecodeError):
            state = "unreadable"
        pool.setdefault(state, []).append(current)
    return pool


def _newest_result(fn_dir: Path) -> dict | None:
    results = sorted(fn_dir.glob("attempts/*/result.json"),
                     key=lambda p: p.stat().st_mtime)
    for path in reversed(results):
        try:
            return json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
    return None


def _classify_reds(reds: list[Path]) -> tuple[int, int, int]:
    structural = translation = unknown = 0
    for current in reds:
        result = _newest_result(current.parent)
        if result is None:
            unknown += 1
            continue
        text = " ".join(
            f"{entry.get('phase', '')} {entry.get('failure_class', '')} "
            f"{entry.get('detail', '')}"
            for entry in result.get("results", [])
        )
        if STRUCTURAL.search(text):
            structural += 1
        else:
            translation += 1
    return structural, translation, unknown


def _stale_causes(stales: list[Path], batches: list[dict],
                  records: list[dict]) -> tuple[int, int, int]:
    landed_basenames = [
        (_parse(r["landed_at"]), r.get("basename")) for r in records
    ]
    same = cross = unknown = 0
    for current in stales:
        try:
            state = json.loads(current.read_text())
            attempt_dir = current.parent / "attempts" / state["attempt_id"]
            packet = json.loads((attempt_dir / "packet.json").read_text())
        except (OSError, json.JSONDecodeError, KeyError):
            unknown += 1
            continue
        basename = packet.get("basename")
        issued_raw = packet.get("updated_at")
        if not basename or not issued_raw:
            unknown += 1
            continue
        issued = _parse(issued_raw)
        staled = datetime.datetime.fromtimestamp(current.stat().st_mtime,
                                                 tz=datetime.UTC)
        window = [b for at, b in landed_basenames if issued <= at <= staled]
        if basename in window:
            same += 1
        elif window:
            cross += 1
        else:
            unknown += 1
    return same, cross, unknown


def main() -> int:
    now = datetime.datetime.now(datetime.UTC)
    records = _load_landings()
    batches = _batches(records)
    sizes = _sizes()
    lines: list[str] = []

    for hours in (6, 24):
        cutoff = now - datetime.timedelta(hours=hours)
        window = [b for b in batches if b["at"] > cutoff]
        routines = [name for b in window for name in b["routines"]]
        landed_bytes = sum(sizes.get(name, {}).get("size", 0) for name in routines)
        lines.append(f"landings_per_hour_{hours}h={len(routines) / hours:.2f}")
        lines.append(f"bytes_per_hour_{hours}h={landed_bytes / hours:.0f}")
        if hours == 6:
            gate = sum(b["seconds_gate"] for b in window)
            mean_batch = (len(routines) / len(window)) if window else 0.0
            lines.append(f"gate_share_6h={gate / (hours * 3600):.3f}")
            lines.append(f"mean_batch_6h={mean_batch:.2f}")

    recent = [b["seconds_gate"] for b in batches[-50:] if b["seconds_gate"]]
    median_gate = statistics.median(recent) if recent else 0.0
    lines.append(f"gate_seconds_median_50={median_gate:.1f}")

    cutoff = now - datetime.timedelta(hours=24)
    stamps = [b["at"] for b in batches if b["at"] > cutoff] + [now]
    stall = datetime.timedelta()
    for previous, current in itertools.pairwise(stamps):
        gap = current - previous
        if gap > STALL_GAP:
            stall += gap
    lines.append(f"stall_minutes_24h={stall.total_seconds() / 60:.0f}")

    todo = [fn for fn in sizes.values() if fn.get("status") == "todo"]
    ready = [fn for fn in todo if fn.get("ready")]
    lines.append(f"ready_count={len(ready)}")
    lines.append(f"ready_bytes={sum(fn.get('size', 0) for fn in ready)}")

    stanzas = []
    if BLOCKED.is_file():
        stanzas = tomllib.loads(BLOCKED.read_text()).get("blocked", [])
    blocked_names = [s.get("name") for s in stanzas if s.get("name")]
    blocked_bytes = sum(sizes.get(name, {}).get("size", 0) for name in blocked_names)
    lines.append(f"blocked_stanzas={len(stanzas)}")
    lines.append(f"blocked_bytes={blocked_bytes}")
    lines.append(f"artifacts_pending={_pending_artifacts()}")

    pool = _pool()
    for state in ("green", "red", "stale", "issued"):
        lines.append(f"pool_{state}={len(pool.get(state, []))}")

    # Selection is per-basename exclusive, so distinct basenames among the
    # selector's own `ready` work records is the hard ceiling on useful
    # concurrent sessions. progress.json's `ready` flag counts routines whose
    # artifacts are already staged and overstates that ceiling several-fold.
    rows, basenames = _frontier()
    lines.append(f"frontier_rows={rows}")
    lines.append(f"frontier_basenames={basenames}")

    structural, translation, unknown = _classify_reds(pool.get("red", []))
    lines.append(f"red_structural={structural}")
    lines.append(f"red_translation={translation}")
    lines.append(f"red_unknown={unknown}")

    same, cross, unknown = _stale_causes(pool.get("stale", []), batches, records)
    lines.append(f"stale_same_basename={same}")
    lines.append(f"stale_cross_basename={cross}")
    lines.append(f"stale_unknown={unknown}")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
