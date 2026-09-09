#!/usr/bin/env python3
"""Project the loop's measured facts onto the Forgejo issue tracker.

Every issue this tool owns is a fact the tooling already produces, keyed so a
re-run is idempotent: a session's first divergence (`session.py verify`), a
routine the sweep found wrong from a live seed (`session.py sweep`), a body
the composition audits rank as hollow, an echo or a cut. An issue opens when
the fact appears, carries the exact commands that reproduce it, and closes
when the fact is gone -- no hand-written progress, no plan projected onto the
tracker. The two earlier trackers projected plans; nobody working the loop
had a reason to touch them, and they rotted within a week.

Humans own exactly one kind of issue: a `route` item naming the next content
to record ("Isaac's duel via pokes"), closed here once the session it names
is clean.

Milestones are the game's route, so a milestone's counts answer "how far".
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import socket
import subprocess
import sys
from datetime import datetime, timezone
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "completion"))
sys.path.insert(0, str(ROOT))

import composition_audit
import session

API = "https://forgejo.yfrit.com/api/v1"
REPO = "fairfruit/poketcg-pc"
TRACKER_DIR = ROOT / "build" / "completion" / "tracker"
SYNC_STAMP = TRACKER_DIR / ".synced"
SYNC_LOCK = TRACKER_DIR / ".lock"
CLAIM_LABEL = "claimed"
CLAIM_MARK = re.compile(r"^claimed (\S+) by (.+)$")
CLAIM_TTL = 6 * 3600  # seconds a claim keeps an issue out of other sessions' issues-next
KEY_MARK = re.compile(r"<!-- tracker-key: ([^ ]+) -->")
ORDINAL_MARK = re.compile(r"<!-- tracker-ordinal: (\d+) -->")
SESSION_MARK = re.compile(r"^session:\s*`?([a-z0-9_-]+)`?", re.MULTILINE | re.IGNORECASE)

LABELS = {
    "p0-divergence": ("e11d21", "a recorded session leaves the ROM's trajectory here"),
    "p1-memory": ("d93f0b", "a routine computes different game state from a live seed"),
    "p2-registers": ("fbca04", "a routine leaves different exit registers from a live seed"),
    "p3-audit": ("c5def5", "a body the composition audits rank as hollow, an echo or a cut"),
    "route": ("0e8a16", "the next content to record; closes when its session is clean"),
    "tooling": ("5319e7", "loop machinery"),
    "claimed": ("ededed", "a session is on it (comment names who and when; expires after 6 h)"),
    "wontfix": ("ffffff", "the fact stands and is accepted; the tracker leaves it closed"),
    "noise": ("ffffff", "a harness artefact, not a port defect; the tracker leaves it closed"),
}
HOLD_LABELS = {"wontfix", "noise"}

# The route, in play order: (milestone, session names, session-name prefixes).
# A session names the milestone its ordinals belong to; a sweep row inherits
# the milestone of the first route session that reaches its ordinal. A session
# off the route (`ai-duel-*`, deck-machine drives) is engine work.
ROUTE = [
    ("Boot and Mason's lab", ["boot-menu", "first-duel", "practice-win"], ("boot-", "mason-")),
    ("Fighting Club", ["fighting-club"], ("fighting-",)),
    ("Rock Club", ["rock-club", "andrew-duel", "ryan-duel", "gene-duel"], ("rock-",)),
    ("Lightning Club", ["jennifer-duel", "lightning-2", "lightning-3", "isaac-duel"], ("lightning-",)),
    ("Water Club", [], ("water-",)),
    ("Grass Club", [], ("grass-",)),
    ("Psychic Club", [], ("psychic-",)),
    ("Science Club", [], ("science-",)),
    ("Fire Club", [], ("fire-",)),
    ("Ronald and the Challenge Hall", [], ("ronald-", "challenge-")),
    ("Pokemon Dome and credits", [], ("dome-", "credits-")),
]
ENGINE = "Engine"
TOOLING = "Tooling"
MILESTONES = [row[0] for row in ROUTE] + [ENGINE, TOOLING]
COIN_TOSS_NOISE = ("PinMissile", "HandleSandAttackOrSmokescreen", "TossCoin", "Fury", "Rage")


class TrackerError(RuntimeError):
    pass


def configured_secret(name: str) -> str:
    value = os.environ.get(name)
    if value:
        return value
    try:
        for line in (Path.home() / ".zsh_secrets").read_text(encoding="utf-8").splitlines():
            normalized = line.removeprefix("export ").strip()
            if normalized.startswith(f"{name}="):
                return normalized.split("=", 1)[1].strip().strip("\"'")
    except OSError:
        return ""
    return ""


def api_token() -> str:
    value = configured_secret("FJ_FORGEJO_TOKEN") or configured_secret("POKETCG_FORGEJO_TOKEN")
    if not value:
        token_path = Path(os.environ.get(
            "POKETCG_FORGEJO_TOKEN_FILE",
            str(Path.home() / ".config/yfrit-forgejo/api/poketcg-issues.token"),
        ))
        try:
            value = token_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise TrackerError(f"Forgejo API token is unavailable: {exc}") from exc
    value = value.removeprefix("Authorization:").strip()
    if value.casefold().startswith(("token ", "bearer ")):
        value = value.split(" ", 1)[1]
    if not value:
        raise TrackerError("Forgejo API token is empty")
    return value


class Forgejo:
    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"token {api_token()}",
            # Cloudflare's bot filter (error 1010) rejects urllib's default agent.
            "User-Agent": "poketcg-tracker/1 (+https://forgejo.yfrit.com/fairfruit/poketcg-pc)",
            "CF-Access-Client-Id": configured_secret("FJ_CF_ACCESS_CLIENT_ID"),
            "CF-Access-Client-Secret": configured_secret("FJ_CF_ACCESS_CLIENT_SECRET"),
        }
        self.writes = 0

    def call(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        if method != "GET" and self.dry_run:
            self.writes += 1
            print(f"DRY {method} {path} {json.dumps(payload)[:160] if payload else ''}")
            return {}
        data = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(f"{API}{path}", data=data, method=method, headers=self.headers)
        # Reads and idempotent writes retry through the tunnel's stalls; a POST
        # creates, so a timed-out POST is reported rather than repeated.
        attempts = 1 if method == "POST" else 3
        for attempt in range(1, attempts + 1):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    body = response.read()
                    if method != "GET":
                        self.writes += 1
                    return json.loads(body) if body else {}
            except urllib.error.HTTPError as exc:
                raise TrackerError(f"{method} {path} -> HTTP {exc.code}: {exc.read()[:200].decode(errors='replace')}") from exc
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                if attempt == attempts:
                    raise TrackerError(f"{method} {path} failed: {exc}") from exc
        raise AssertionError("unreachable")

    def paged(self, path: str) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        page = 1
        while True:
            chunk = self.call("GET", f"{path}&limit=50&page={page}")
            out.extend(chunk)
            if len(chunk) < 50:
                return out
            page += 1

    def issues(self) -> list[dict[str, Any]]:
        return self.paged(f"/repos/{REPO}/issues?state=all&type=issues")

    def labels(self) -> dict[str, int]:
        return {row["name"]: row["id"] for row in self.paged(f"/repos/{REPO}/labels?")}

    def milestones(self) -> dict[str, dict[str, Any]]:
        return {row["title"]: row for row in self.paged(f"/repos/{REPO}/milestones?state=all")}

    def ensure_labels(self) -> dict[str, int]:
        have = self.labels()
        for name, (color, description) in LABELS.items():
            if name not in have:
                created = self.call("POST", f"/repos/{REPO}/labels",
                                    {"name": name, "color": color, "description": description})
                have[name] = created.get("id", -1)
        return have

    def ensure_milestones(self) -> dict[str, dict[str, Any]]:
        have = self.milestones()
        for title in MILESTONES:
            if title not in have:
                have[title] = self.call("POST", f"/repos/{REPO}/milestones", {"title": title})
            elif have[title].get("state") == "closed":
                self.call("PATCH", f"/repos/{REPO}/milestones/{have[title]['id']}", {"state": "open"})
        return have

    def create(self, issue: dict[str, Any], label_ids: list[int], milestone: int | None) -> dict[str, Any]:
        payload = {"title": issue["title"], "body": issue["body"], "labels": label_ids}
        if milestone is not None:
            payload["milestone"] = milestone
        return self.call("POST", f"/repos/{REPO}/issues", payload)

    def patch(self, number: int, payload: dict[str, Any]) -> None:
        self.call("PATCH", f"/repos/{REPO}/issues/{number}", payload)

    def set_labels(self, number: int, label_ids: list[int]) -> None:
        self.call("PUT", f"/repos/{REPO}/issues/{number}/labels", {"labels": label_ids})

    def comment(self, number: int, text: str) -> None:
        self.call("POST", f"/repos/{REPO}/issues/{number}/comments", {"body": text})


def route_of(name: str) -> str:
    for milestone, names, prefixes in ROUTE:
        if name in names or name.startswith(prefixes):
            return milestone
    return ENGINE


def session_total(name: str) -> int | None:
    path = session.session_dir(name) / "session.json"
    return json.loads(path.read_text()).get("ordinals") if path.is_file() else None


def route_sessions() -> list[tuple[str, int, str]]:
    """(session, ordinals, milestone) for the recorded route sessions, by
    ordinal, so an ordinal maps to the region of the game it belongs to."""
    rows: list[tuple[str, int, str]] = []
    for name in session.session_names():
        if name.startswith("_"):
            continue
        milestone = route_of(name)
        total = session_total(name)
        if milestone != ENGINE and total:
            rows.append((name, total, milestone))
    rows.sort(key=lambda row: row[1])
    return rows


def milestone_for_ordinal(ordinal: int, sessions: list[tuple[str, int, str]]) -> str:
    for _name, end, milestone in sessions:
        if ordinal <= end:
            return milestone
    return sessions[-1][2] if sessions else ENGINE


def asm_locations() -> dict[str, str]:
    """routine -> `file:line` of its label in the disassembly."""
    found: dict[str, str] = {}
    label = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?")
    for path in (ROOT / "poketcg" / "src").rglob("*.asm"):
        for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            match = label.match(line)
            if match and match.group(1) not in found:
                found[match.group(1)] = f"{path.relative_to(ROOT)}:{number}"
    return found


def c_locations() -> dict[str, str]:
    """routine -> `file:line` of its definition in the port."""
    found: dict[str, str] = {}
    for path in sorted((ROOT / "src" / "home").glob("*.c")):
        lines = path.read_text(errors="replace").splitlines()
        for number, line in enumerate(lines, 1):
            match = composition_audit.DEFINITION.match(line)
            if match and number < len(lines) and lines[number].startswith("{"):
                found.setdefault(match.group(1), f"src/home/{path.name}:{number}")
    return found


def area_of(location: str | None) -> str:
    if not location:
        return "port"
    return Path(location.split(":")[0]).stem


def body(key: str, ordinal: int | None, lines: list[str]) -> str:
    head = [f"<!-- tracker-key: {key} -->"]
    if ordinal is not None:
        head.append(f"<!-- tracker-ordinal: {ordinal} -->")
    return "\n".join(head + lines) + "\n"


def routine_lines(routine: str, asm: dict[str, str], c: dict[str, str]) -> list[str]:
    return [f"**Asm:** `{asm.get(routine, '?')}`  **C:** `{c.get(routine, 'not ported')}`"]


def divergence_issues(sessions: list[tuple[str, int, str]]) -> dict[str, dict[str, Any]]:
    """One issue per session whose latest verify is not clean."""
    out: dict[str, dict[str, Any]] = {}
    for path in TRACKER_DIR.glob("verify-*.json"):
        report = json.loads(path.read_text())
        name = report["name"]
        status = report.get("status")
        if status not in ("diverged", "native-short"):
            continue
        confirmed = report.get("confirmed", 0)
        ordinal = report.get("divergence", {}).get("ordinal", confirmed + 1)
        rows = report.get("divergence", {}).get("rows", [])
        writers = [row["writer"] for row in rows if row.get("writer")]
        lines = [
            f"**Fact:** `just session-verify {name}` -> `status={status}` at DoFrame {ordinal} "
            f"(confirmed {confirmed} of {report.get('ordinals', '?')}).",
            "",
            "**Evidence:**",
        ]
        for row in rows[:8]:
            lines.append(f"- `{row['field']} {row['address']} {row['symbol']}`: native `{row['native']}` "
                         f"reference `{row['reference']}` writer `{row['writer'] or '-'}`")
        if status == "native-short":
            for line in (report.get("native_failure") or "").strip().splitlines()[-3:]:
                lines.append(f"- native: `{line}`")
        lines += [
            "",
            "**Repro:**",
            "```sh",
            f"just session-verify {name}",
            f"python3 tools/completion/session.py routines {name} {confirmed}",
            f"python3 tools/completion/session.py capture {name} --routine <R> --after {confirmed} --out tests/fixtures/{name}-<r>-entry.json",
            "```",
            "",
            ("**Done when:** the session verifies clean past this ordinal (the ratchet rises); "
             "the fix carries a fixture case and a red mutation (`docs/grind.md`, session decision table)."),
        ]
        title_writer = writers[0] if writers else status
        out[f"session:{name}"] = {
            "title": f"fix(session): {name} diverges at {ordinal} ({title_writer})",
            "body": body(f"session:{name}", ordinal, lines),
            "labels": ["p0-divergence"],
            "milestone": route_of(name),
        }
    return out


def sweep_issues(sessions: list[tuple[str, int, str]], asm: dict[str, str], c: dict[str, str],
                 resolved: set[str]) -> dict[str, dict[str, Any]]:
    """One issue per routine the newest sweep row reports failing. A routine
    seen passing in a newer sweep is resolved even if an older sweep failed it,
    and so is one a newer sweep of the same session covered without emitting a
    row at all: that sweep either passed it or stopped comparing it, and either
    way the older row is no longer evidence."""
    reports: list[tuple[float, dict[str, Any]]] = []
    for path in TRACKER_DIR.glob("sweep-*.json"):
        reports.append((path.stat().st_mtime, json.loads(path.read_text())))

    def superseded(stamp: float, name: str, row: dict[str, Any]) -> bool:
        for other_stamp, other in reports:
            if other_stamp <= stamp or other.get("name") != name:
                continue
            until = other.get("until")
            if until is None or not other.get("after", 0) <= row["ordinal"] <= until:
                continue
            if all(seen["routine"] != row["routine"] for seen in other.get("rows", [])):
                return True
        return False

    latest: dict[str, tuple[float, str, dict[str, Any]]] = {}
    for stamp, report in reports:
        for row in report.get("rows", []):
            routine = row["routine"]
            if superseded(stamp, report["name"], row):
                resolved.add(f"sweep:{routine}")
                continue
            if routine not in latest or latest[routine][0] < stamp:
                latest[routine] = (stamp, report["name"], row)
    out: dict[str, dict[str, Any]] = {}
    for routine, (_stamp, name, row) in latest.items():
        key = f"sweep:{routine}"
        if row["status"] != "fail":
            resolved.add(key)
            continue
        memory = bool(row.get("memory"))
        noise = memory and routine.startswith(COIN_TOSS_NOISE)
        ordinal = row["ordinal"]
        milestone = ENGINE if name.startswith("ai-duel") else milestone_for_ordinal(ordinal, sessions)
        lines = [
            f"**Fact:** `just session-sweep {name}` -> `{routine}` fails from its live entry at DoFrame {ordinal}: "
            + ("game state differs" if memory else "exit registers differ, memory agrees") + ".",
        ]
        if noise:
            lines.append("Coin-toss routine: the PyBoy lane advances the RNG per frame inside the routine, so"
                         " the tosses may land differently. Confirm on a session before treating as a defect.")
        lines += ["", "**Evidence:**"] + [f"- `{m[:200]}`" for m in row["mismatches"][:12]]
        lines += [""] + routine_lines(routine, asm, c) + [
            "",
            "**Repro:**",
            "```sh",
            f"python3 tools/completion/session.py capture {name} --routine {routine} --after {ordinal} --out tests/fixtures/{name}-{routine.lower()}-entry.json",
            f"just oracle-diff {routine}",
            "```",
            "",
            ("**Done when:** a fixture case from that capture is green with a red mutation, and the next "
             f"`just session-sweep {name}` lists the routine as ok."),
        ]
        registers = ", ".join(sorted({m.split(":")[0].strip() for m in row["mismatches"] if not m.lstrip().startswith(("$", "vram", "sram"))}))
        out[key] = {
            "title": (f"fix({area_of(c.get(routine))}): {routine} differs from a live seed"
                      if memory else f"fix({area_of(c.get(routine))}): {routine} exit registers ({registers})"),
            "body": body(key, ordinal, lines),
            "labels": ["p1-memory" if memory else "p2-registers"],
            "milestone": milestone,
        }
    return out


def audit_issues(asm: dict[str, str], c: dict[str, str]) -> dict[str, dict[str, Any]]:
    bodies = composition_audit.c_bodies()
    _looping, sizes, asm_calls = composition_audit.asm_shapes()
    out: dict[str, dict[str, Any]] = {}

    def add(kind: str, routine: str, fact: str, done: str) -> None:
        key = f"audit:{kind}:{routine}"
        lines = [f"**Fact:** `python3 tools/completion/composition_audit.py {kind}` -> {fact}", ""]
        lines += routine_lines(routine, asm, c)
        lines += ["", "**Repro:**", "```sh",
                  f"python3 tools/completion/composition_audit.py {kind}",
                  f"just oracle-diff {routine}",
                  "```", "", f"**Done when:** {done}"]
        out[key] = {
            "title": f"port({area_of(c.get(routine))}): {routine} is {'an echo' if kind == 'echoes' else 'a stub' if kind == 'stubs' else 'cut short'}",
            "body": body(key, None, lines),
            "labels": ["p3-audit"],
            "milestone": ENGINE,
        }

    for row in composition_audit.audit_echoes(bodies, sizes, asm_calls):
        add("echoes", row["routine"],
            f"{row['c_statements']} C statements and no callee for {row['asm_instructions']} asm instructions "
            f"making {row['asm_calls']} calls: the body writes the observed bytes instead of running the routine.",
            "the body calls what the asm calls, its cases seed a live state (a session capture), and the row is gone.")
    for row in composition_audit.audit_stubs(bodies, sizes, asm_calls):
        if row["asm_instructions"] < 25:
            continue
        add("stubs", row["routine"],
            f"one C statement for {row['asm_instructions']} asm instructions ({row['dropped_calls']} calls dropped).",
            "the routine is ported from the asm with a fixture case at a real entry and a red mutation.")
    for row in composition_audit.audit_cuts():
        add("cuts", row["routine"],
            f"its completion override stops both lanes at `{row['cuts_at']}` ({row['depth']} call(s) down), "
            "so the contract covers only the prefix before it.",
            "the completion block is deleted and the routine's cases run to its real `ret`.")
    return out


def load_desired() -> tuple[dict[str, dict[str, Any]], set[str]]:
    sessions = route_sessions()
    asm = asm_locations()
    c = c_locations()
    resolved: set[str] = set()
    desired: dict[str, dict[str, Any]] = {}
    desired.update(divergence_issues(sessions))
    desired.update(sweep_issues(sessions, asm, c, resolved))
    desired.update(audit_issues(asm, c))
    return desired, resolved


def last_landing(routine: str, c: dict[str, str]) -> str:
    location = c.get(routine)
    if not location:
        return ""
    path = location.split(":")[0]
    try:
        result = subprocess.run(
            ["jj", "log", "--no-graph", "-r", f"files({path!r}) & ::@-", "--limit", "1",
             "-T", 'commit_id.short() ++ " " ++ description.first_line()'],
            cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip()


def sync(dry_run: bool, retire_plan: bool) -> int:
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    with SYNC_LOCK.open("w") as lock:
        # Two sessions syncing at once would both create the same new fact.
        fcntl.flock(lock, fcntl.LOCK_EX)
        return locked_sync(dry_run, retire_plan)


def locked_sync(dry_run: bool, retire_plan: bool) -> int:
    api = Forgejo(dry_run=dry_run)
    desired, resolved = load_desired()
    c = c_locations()
    label_ids = api.ensure_labels() if not dry_run else {name: -1 for name in LABELS}
    milestones = api.ensure_milestones() if not dry_run else {name: {"id": -1, "title": name} for name in MILESTONES}
    existing = api.issues()
    by_key: dict[str, dict[str, Any]] = {}
    for issue in existing:
        match = KEY_MARK.search(issue.get("body") or "")
        if match:
            by_key[match.group(1)] = issue
    ratchet = session.read_ratchet()
    created = updated = closed = reopened = 0

    def label_list(names: list[str]) -> list[int]:
        return [label_ids[name] for name in names if name in label_ids]

    for key, want in sorted(desired.items()):
        have = by_key.get(key)
        milestone_id = milestones.get(want["milestone"], {}).get("id")
        if have is None:
            api.create(want, label_list(want["labels"]), milestone_id)
            created += 1
            continue
        have_labels = {label["name"] for label in have.get("labels", [])}
        if have_labels & HOLD_LABELS:
            continue
        if have["state"] == "closed":
            api.patch(have["number"], {"state": "open", "title": want["title"], "body": want["body"]})
            api.comment(have["number"], "Reopened: the fact is back in the latest run.")
            reopened += 1
            continue
        patch: dict[str, Any] = {}
        if have["title"] != want["title"]:
            patch["title"] = want["title"]
        if (have.get("body") or "").strip() != want["body"].strip():
            patch["body"] = want["body"]
        have_milestone = (have.get("milestone") or {}).get("title")
        if milestone_id is not None and have_milestone != want["milestone"]:
            patch["milestone"] = milestone_id
        if patch:
            api.patch(have["number"], patch)
            updated += 1
        wanted_labels = set(want["labels"])
        if wanted_labels - have_labels:
            api.set_labels(have["number"], label_list(sorted(wanted_labels | (have_labels & HOLD_LABELS))))

    for key, have in by_key.items():
        if key in desired or have["state"] == "closed":
            continue
        have_labels = {label["name"] for label in have.get("labels", [])}
        if key.startswith("sweep:") and key not in resolved:
            # The routine was not entered by any newer sweep: no evidence either way.
            continue
        routine = key.split(":")[-1]
        landing = last_landing(routine, c) if key.split(":")[0] in ("sweep", "audit") else ""
        reason = {
            "session": "the session verifies clean past this ordinal",
            "sweep": "the latest sweep lists the routine as ok",
            "audit": "the audit no longer reports the routine",
        }[key.split(":")[0]]
        api.comment(have["number"], f"Resolved: {reason}." + (f" Last landing on its file: `{landing}`." if landing else ""))
        api.patch(have["number"], {"state": "closed"})
        closed += 1

    for issue in existing:
        labels = {label["name"] for label in issue.get("labels", [])}
        if issue["state"] == "open" and CLAIM_LABEL in labels and not dry_run:
            age = claim_age(api, issue)
            if age is not None and age >= CLAIM_TTL:
                release_claim(api, issue, label_ids)
        if issue["state"] == "open" and "route" in labels:
            match = SESSION_MARK.search(issue.get("body") or "")
            if match:
                name = match.group(1)
                confirmed = ratchet.get(name, {}).get("confirmed_ordinal")
                total = session_total(name)
                if confirmed is not None and total and confirmed >= total:
                    api.comment(issue["number"], f"Resolved: session `{name}` is clean through {total} DoFrames.")
                    api.patch(issue["number"], {"state": "closed"})
                    closed += 1
        elif retire_plan and issue["state"] == "open" and not KEY_MARK.search(issue.get("body") or "") \
                and "route" not in labels:
            api.comment(issue["number"],
                        "Superseded: the tracker now projects measured facts (session divergences, sweep rows, "
                        "composition audits; `docs/grind.md`, Issues), and this plan-shaped item is not a unit of "
                        "work the loop produces. Route items are re-created as `route` issues.")
            if "lifecycle/superseded" in label_ids:
                api.set_labels(issue["number"], [label_ids["lifecycle/superseded"]])
            api.patch(issue["number"], {"state": "closed"})
            closed += 1
    if retire_plan:
        for title, row in api.milestones().items():
            if title not in MILESTONES and row.get("state") == "open":
                api.call("PATCH", f"/repos/{REPO}/milestones/{row['id']}", {"state": "closed"})
    print(f"TRACKER desired={len(desired)} created={created} updated={updated} reopened={reopened} "
          f"closed={closed} writes={api.writes}{' (dry run)' if dry_run else ''}")
    if not dry_run:
        TRACKER_DIR.mkdir(parents=True, exist_ok=True)
        SYNC_STAMP.touch()
    return 0


def warn_if_stale() -> None:
    """A report written after the last sync is a fact the tracker does not
    show yet; say so before listing, so nobody works from a stale list."""
    since = SYNC_STAMP.stat().st_mtime if SYNC_STAMP.is_file() else 0.0
    stale = sum(1 for path in TRACKER_DIR.glob("*.json") if path.stat().st_mtime > since)
    if stale:
        print(f"STALE reports={stale} newer than the last sync; run: just issues-sync")


def claimant() -> str:
    return os.environ.get("POKETCG_SESSION") or f"{socket.gethostname()}:{os.getppid()}"


def claim_age(api: Forgejo, issue: dict[str, Any]) -> float | None:
    """Seconds since the newest `claimed <ISO time> by <who>` comment, or None
    when the issue carries no live claim."""
    if CLAIM_LABEL not in {label["name"] for label in issue.get("labels", [])}:
        return None
    newest = None
    for comment in api.paged(f"/repos/{REPO}/issues/{issue['number']}/comments?"):
        match = CLAIM_MARK.match(comment.get("body") or "")
        if match:
            newest = datetime.fromisoformat(match.group(1))
    return (datetime.now(timezone.utc) - newest).total_seconds() if newest else float("inf")


def claim_issue(api: Forgejo, issue: dict[str, Any], label_ids: dict[str, int]) -> None:
    labels = {label["name"] for label in issue.get("labels", [])} | {CLAIM_LABEL}
    api.comment(issue["number"], f"claimed {datetime.now(timezone.utc).isoformat(timespec='seconds')} by {claimant()}")
    api.set_labels(issue["number"], [label_ids[name] for name in sorted(labels) if name in label_ids])


def release_claim(api: Forgejo, issue: dict[str, Any], label_ids: dict[str, int]) -> None:
    labels = {label["name"] for label in issue.get("labels", [])} - {CLAIM_LABEL}
    api.set_labels(issue["number"], [label_ids[name] for name in sorted(labels) if name in label_ids])


def next_issues(count: int, claim: bool) -> int:
    """The open facts in priority order. An issue another session claimed less
    than CLAIM_TTL ago is skipped; `claim` takes the first one listed."""
    warn_if_stale()
    api = Forgejo()
    rows = api.paged(f"/repos/{REPO}/issues?state=open&type=issues")
    ranked = []
    for issue in rows:
        labels = {label["name"] for label in issue.get("labels", [])}
        if labels & HOLD_LABELS:
            continue
        age = claim_age(api, issue)
        if age is not None and age < CLAIM_TTL:
            continue
        # Divergences block a session; recording the next content is how new
        # divergences are found; sweep and audit rows come after.
        rank = {"p0-divergence": 0, "route": 1, "p1-memory": 2, "p2-registers": 3, "p3-audit": 4}
        priority = min((rank[name] for name in labels if name in rank), default=5)
        match = ORDINAL_MARK.search(issue.get("body") or "")
        milestone = (issue.get("milestone") or {}).get("title")
        position = MILESTONES.index(milestone) if milestone in MILESTONES else len(MILESTONES)
        # Within a priority: play order, then the DoFrame the fact was seen at.
        ranked.append((priority, position, int(match.group(1)) if match else 1 << 30, issue))
    ranked.sort(key=lambda row: row[:3])
    if claim and ranked:
        claim_issue(api, ranked[0][3], api.ensure_labels())
    for index, (_priority, _position, _ordinal, issue) in enumerate(ranked[:count]):
        labels = sorted(label["name"] for label in issue.get("labels", []) if label["name"] != CLAIM_LABEL)
        milestone = (issue.get("milestone") or {}).get("title", "-")
        claimed = " claimed" if claim and index == 0 else ""
        print(f"#{issue['number']} [{', '.join(labels)}] {milestone}{claimed}\n  {issue['title']}")
        text = issue.get("body") or ""
        repro = re.search(r"\*\*Repro:\*\*\n```sh\n(.*?)```", text, re.DOTALL)
        if repro:
            for line in repro.group(1).strip().splitlines():
                print(f"    $ {line}")
        print(f"  https://forgejo.yfrit.com/{REPO}/issues/{issue['number']}")
    return 0


def claim(number: int) -> int:
    """(Re)claim one issue by number: renews the clock for work past CLAIM_TTL."""
    api = Forgejo()
    issue = api.call("GET", f"/repos/{REPO}/issues/{number}")
    if issue.get("state") != "open":
        raise TrackerError(f"#{number} is not open")
    claim_issue(api, issue, api.ensure_labels())
    print(f"#{number} claimed by {claimant()}")
    return 0


def release(number: int) -> int:
    """Give an issue back: the next issues-next anywhere may take it."""
    api = Forgejo()
    issue = api.call("GET", f"/repos/{REPO}/issues/{number}")
    release_claim(api, issue, api.labels())
    api.comment(issue["number"], f"released by {claimant()}")
    print(f"#{number} released")
    return 0


def route(name: str, title: str, how: str) -> int:
    """Open the one kind of issue a human writes: the next content to record.
    `session:` names the recording; the tracker closes the issue once that
    session verifies clean end to end."""
    if route_of(name) == ENGINE:
        raise TrackerError(f"{name} is not a route session name (see ROUTE prefixes)")
    api = Forgejo()
    for issue in api.paged(f"/repos/{REPO}/issues?state=open&type=issues&labels=route"):
        if SESSION_MARK.search(issue.get("body") or "") and SESSION_MARK.search(issue["body"]).group(1) == name:
            print(f"#{issue['number']} already names session {name}")
            return 0
    label_ids = api.ensure_labels()
    milestones = api.ensure_milestones()
    lines = [
        f"session: `{name}`",
        "",
        f"**Record:** {how}",
        "",
        "**Done when:** `just session-verify " + name + "` is clean end to end and the ratchet holds it; "
        "every divergence it surfaces is its own `p0-divergence` issue meanwhile.",
    ]
    created = api.create({"title": f"route: {title}", "body": "\n".join(lines) + "\n"},
                         [label_ids["route"]], milestones[route_of(name)]["id"])
    print(f"#{created.get('number', '?')} route: {title}")
    return 0


def status() -> int:
    warn_if_stale()
    api = Forgejo()
    milestones = api.milestones()
    ratchet = session.read_ratchet()
    sessions = route_sessions()
    print(f"{'milestone':32s} {'open':>5s} {'closed':>6s}  sessions")
    for title in MILESTONES:
        row = milestones.get(title, {})
        names = [name for name, _end, milestone in sessions if milestone == title]
        if title == ENGINE:
            names = sorted(name for name in session.session_names()
                           if route_of(name) == ENGINE and not name.startswith("_"))
        marks = []
        for name in names:
            total = session_total(name) or 0
            confirmed = ratchet.get(name, {}).get("confirmed_ordinal", 0)
            marks.append(f"{name}{' ok' if confirmed >= total and total else f' {confirmed}/{total}'}")
        print(f"{title:32s} {row.get('open_issues', 0):5d} {row.get('closed_issues', 0):6d}  {', '.join(marks)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sync_parser = sub.add_parser("sync", help="reconcile the tracker with the loop's latest facts")
    sync_parser.add_argument("--dry-run", action="store_true")
    sync_parser.add_argument("--retire-plan", action="store_true",
                             help="close the plan-shaped issues and milestones of the earlier trackers")
    next_parser = sub.add_parser("next", help="the highest-priority open issues with their repro commands")
    next_parser.add_argument("count", type=int, nargs="?", default=5)
    next_parser.add_argument("--claim", action="store_true", help="mark the first one as this session's")
    claim_parser = sub.add_parser("claim", help="(re)claim one issue by number")
    claim_parser.add_argument("number", type=int)
    release_parser = sub.add_parser("release", help="give a claimed issue back")
    release_parser.add_argument("number", type=int)
    sub.add_parser("status", help="milestones with their counts and sessions")
    route_parser = sub.add_parser("route", help="open a route item: the next content to record")
    route_parser.add_argument("session", help="the session name the recording will use")
    route_parser.add_argument("title")
    route_parser.add_argument("how", help="how to record it: the verbs, the branch, the pokes")
    args = parser.parse_args(argv)
    try:
        if args.command == "sync":
            return sync(args.dry_run, args.retire_plan)
        if args.command == "next":
            return next_issues(args.count, args.claim)
        if args.command == "claim":
            return claim(args.number)
        if args.command == "release":
            return release(args.number)
        if args.command == "route":
            return route(args.session, args.title, args.how)
        return status()
    except TrackerError as exc:
        print(f"tracker: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
