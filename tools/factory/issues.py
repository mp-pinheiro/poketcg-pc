#!/usr/bin/env python3
"""Read and audit canonical routine issues from Forgejo.

Forgejo is the operational source for packet dispatch. This module performs
read-only pagination and desired-state audits; it never mutates remote issues.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, write_json  # noqa: E402

REPORT_PATH = ROOT / "tools" / "progress" / "report.py"
PROGRESS_JSON = ROOT / "site" / "data" / "progress.json"
CACHE = ROOT / ".factory" / "issues-cache.json"
PLAN_PATH = ROOT / ".factory" / "issues-plan.json"
FORGEJO_URL = os.environ.get(
    "POKETCG_FORGEJO_URL", "https://forgejo.yfrit.com"
).rstrip("/")
FORGEJO_OWNER = os.environ.get("POKETCG_FORGEJO_OWNER", "mpp")
FORGEJO_REPO = os.environ.get("POKETCG_FORGEJO_REPO", "poketcg-pc")
FORGEJO_TOKEN_FILE = Path(os.environ.get(
    "POKETCG_FORGEJO_TOKEN_FILE",
    "~/.config/yfrit-forgejo/api/poketcg-issues.token",
)).expanduser()
CF_TOKEN_FILE = Path(os.environ.get(
    "POKETCG_CF_ACCESS_TOKEN_FILE",
    "~/.config/yfrit-forgejo/git/cloudflare-access-service-token.json",
)).expanduser()
USER_AGENT = "poketcg-factory/1.0 (+https://forgejo.yfrit.com/mpp/poketcg-pc)"
DOTENV = ROOT / ".env"
DOTENV_KEYS = {
    "POKETCG_FORGEJO_TOKEN",
    "CF_ACCESS_CLIENT_ID",
    "CF_ACCESS_CLIENT_SECRET",
}
PAGE_SIZE = 50
TRANSIENT_STATUS = {429, 502, 503, 504}
MARKER = re.compile(
    r"<!--\s*poketcg-port-work:v1\s*(\{.*?\})\s*-->",
    re.DOTALL,
)
MARKER_PREFIX = "<!-- poketcg-port-work:v1"
GEN_BEGIN = "<!-- poketcg-port-generated:begin -->"
GEN_END = "<!-- poketcg-port-generated:end -->"
LIFECYCLE = {
    "port-ready", "port-blocked", "port-active", "port-awaiting-gate",
    "port-failing", "port-complete", "port-excluded",
}
MANAGED_LABELS = {"port", "tier-1", "tier-2", "tier-3", "tier-4"} | LIFECYCLE


class ModelError(ValueError):
    pass


def fail(message: str) -> None:
    raise SystemExit(f"issues: {message}")


def sha(data: object) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def normalize_issue(raw: dict) -> dict:
    normalized = []
    for label in raw.get("labels") or []:
        name = label.get("name") if isinstance(label, dict) else label
        if not isinstance(name, str) or not name:
            raise ModelError(
                f"issue #{raw.get('number')} has a malformed label"
            )
        normalized.append(name)
    state = str(raw.get("state", "")).lower()
    if state not in {"open", "closed"}:
        raise ModelError(
            f"issue #{raw.get('number')} has invalid state {state!r}"
        )
    return {
        "id": raw.get("id"),
        "number": int(raw["number"]),
        "title": raw.get("title", ""),
        "body": raw.get("body") or "",
        "state": state,
        "labels": sorted(normalized),
        "url": raw.get("html_url") or raw.get("url") or "",
    }


def snapshot_fingerprint(snapshot: dict) -> str:
    return sha({
        "schema": snapshot.get("schema"),
        "backend": snapshot.get("backend"),
        "repository": snapshot.get("repository"),
        "issues": [
            normalize_issue(issue) for issue in snapshot.get("issues", [])
        ],
    })


def issue_fingerprint(issue: dict) -> str:
    return sha({
        key: issue.get(key)
        for key in ("number", "title", "body", "state", "labels")
    })


def dotenv_credentials(path: Path = DOTENV) -> dict[str, str]:
    if not path.is_file():
        return {}
    credentials: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        name, separator, value = line.partition("=")
        if not separator or name not in DOTENV_KEYS:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        credentials[name] = value
    return credentials


def forgejo_authorization(
    token_file: Path = FORGEJO_TOKEN_FILE,
    dotenv: dict[str, str] | None = None,
) -> str:
    dotenv = dotenv if dotenv is not None else dotenv_credentials()
    token = os.environ.get("POKETCG_FORGEJO_TOKEN") or dotenv.get(
        "POKETCG_FORGEJO_TOKEN"
    )
    if token is None:
        try:
            token = token_file.read_text().strip()
        except OSError as exc:
            raise ModelError(
                f"cannot read Forgejo token file {token_file}: {exc}"
            ) from exc
    if token.lower().startswith("authorization:"):
        token = token.split(":", 1)[1].strip()
    if not token:
        raise ModelError("Forgejo token is empty")
    if not token.lower().startswith(("token ", "bearer ")):
        token = f"token {token}"
    return token


def cloudflare_access_headers(
    dotenv: dict[str, str] | None = None,
    *,
    cf_token_file: Path = CF_TOKEN_FILE,
) -> dict[str, str]:
    dotenv = dotenv if dotenv is not None else dotenv_credentials()
    client_id = os.environ.get("CF_ACCESS_CLIENT_ID") or dotenv.get(
        "CF_ACCESS_CLIENT_ID"
    )
    client_secret = os.environ.get("CF_ACCESS_CLIENT_SECRET") or dotenv.get(
        "CF_ACCESS_CLIENT_SECRET"
    )
    if bool(client_id) != bool(client_secret):
        raise ModelError(
            "CF_ACCESS_CLIENT_ID and CF_ACCESS_CLIENT_SECRET must be set together"
        )
    if client_id:
        return {
            "CF-Access-Client-Id": client_id,
            "CF-Access-Client-Secret": client_secret,
        }
    try:
        payload = json.loads(cf_token_file.read_text())
        file_id = payload["client_id"]
        file_secret = payload["client_secret"]
        expires_at = payload["expires_at"]
    except (OSError, ValueError, KeyError, TypeError):
        file_id = file_secret = expires_at = None
    if file_id and file_secret:
        expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        if expiry < datetime.now(timezone.utc):
            raise ModelError(
                f"Cloudflare Access service token expired at {expires_at}: "
                f"refresh {cf_token_file}"
            )
        return {
            "CF-Access-Client-Id": file_id,
            "CF-Access-Client-Secret": file_secret,
        }
    if FORGEJO_URL == "https://forgejo.yfrit.com":
        raise ModelError(
            "Cloudflare Access service token unavailable: set CF_ACCESS_CLIENT_ID "
            "and CF_ACCESS_CLIENT_SECRET, or provide "
            f"{cf_token_file}"
        )
    return {}


def fetch_page(page: int) -> list[dict]:
    if page < 1:
        raise ModelError("Forgejo page number must be positive")
    owner = urllib.parse.quote(FORGEJO_OWNER, safe="")
    repo = urllib.parse.quote(FORGEJO_REPO, safe="")
    query = urllib.parse.urlencode({
        "state": "all",
        "type": "issues",
        "limit": PAGE_SIZE,
        "page": page,
    })
    url = f"{FORGEJO_URL}/api/v1/repos/{owner}/{repo}/issues?{query}"
    dotenv = dotenv_credentials()
    headers = {
        "Accept": "application/json",
        "Authorization": forgejo_authorization(dotenv=dotenv),
        "User-Agent": USER_AGENT,
        **cloudflare_access_headers(dotenv),
    }
    request = urllib.request.Request(url, headers=headers)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                content_type = response.headers.get("Content-Type", "")
                body = response.read()
            if content_type.startswith("text/html"):
                raise ModelError(
                    f"Cloudflare Access intercepted {url}: the service token is not "
                    "authorized for the Forgejo REST API (see docs/jj-workflow.md)"
                )
            payload = json.loads(body)
            if not isinstance(payload, list):
                raise ModelError(f"Forgejo issue page {page} is not a list")
            return payload
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            if exc.code in TRANSIENT_STATUS and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise ModelError(
                f"Forgejo issue page {page} returned HTTP {exc.code}: {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            if attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise ModelError(f"cannot fetch Forgejo issue page {page}: {exc}") from exc
    raise AssertionError("unreachable")


def fetch_all_issues() -> list[dict]:
    by_number: dict[int, dict] = {}
    page = 1
    while True:
        items = fetch_page(page)
        for raw in items:
            issue = normalize_issue(raw)
            prior = by_number.get(issue["number"])
            if prior is not None and issue_fingerprint(prior) != issue_fingerprint(issue):
                raise ModelError(
                    f"Forgejo issue #{issue['number']} changed across pagination"
                )
            by_number[issue["number"]] = issue
        if len(items) < PAGE_SIZE:
            return [by_number[number] for number in sorted(by_number)]
        page += 1


def fetch_snapshot(attempts: int = 4) -> dict:
    if attempts < 2:
        raise ModelError("snapshot attempts must be at least two")
    previous = None
    for attempt in range(attempts):
        snapshot = {
            "schema": 2,
            "backend": "forgejo",
            "repository": f"{FORGEJO_OWNER}/{FORGEJO_REPO}",
            "fetched_at": int(time.time()),
            "issues": fetch_all_issues(),
        }
        fingerprint = snapshot_fingerprint(snapshot)
        if fingerprint == previous:
            indexed_issues(snapshot)
            if not forgejo_coverage_complete(snapshot):
                raise ModelError(
                    "Forgejo snapshot does not cover every canonical routine"
                )
            write_json(CACHE, snapshot)
            return snapshot
        previous = fingerprint
        if attempt + 1 < attempts:
            time.sleep(1)
    raise ModelError("Forgejo issue listing did not stabilize")


def load_cache(*, required: bool = True, path: Path = CACHE) -> dict | None:
    if not path.exists():
        if required:
            raise ModelError(f"issue cache missing: {path}; run fetch first")
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ModelError(f"invalid issue cache: {path}: {exc}") from exc
    if (
        data.get("schema") != 2
        or data.get("backend") != "forgejo"
        or data.get("repository") != f"{FORGEJO_OWNER}/{FORGEJO_REPO}"
        or not isinstance(data.get("issues"), list)
    ):
        raise ModelError(f"invalid or incomplete Forgejo issue cache: {path}")
    return data


def marker_for(work_id: str) -> str:
    return f'{MARKER_PREFIX}\n{{"work_id":{json.dumps(work_id)}}}\n-->'


def parse_marker(body: str) -> str | None:
    if MARKER_PREFIX not in body:
        return None
    matches = list(MARKER.finditer(body))
    if len(matches) != 1:
        raise ModelError("managed body has duplicate or malformed work markers")
    try:
        payload = json.loads(matches[0].group(1))
    except json.JSONDecodeError as exc:
        raise ModelError(f"malformed work marker: {exc}") from exc
    work_id = payload.get("work_id") if isinstance(payload, dict) else None
    if not isinstance(work_id, str) or not work_id.startswith("port:v1:"):
        raise ModelError("work marker has no valid port:v1 work_id")
    if set(payload) != {"work_id"}:
        raise ModelError("work marker contains unsupported fields")
    return work_id


def replace_generated(body: str, generated: str) -> str:
    begin = body.count(GEN_BEGIN)
    end = body.count(GEN_END)
    if begin != end or begin > 1:
        raise ModelError("generated issue block is duplicated or unterminated")
    block = f"{GEN_BEGIN}\n{generated.rstrip()}\n{GEN_END}"
    if begin == 0:
        return body.rstrip() + "\n\n" + block + "\n"
    start = body.index(GEN_BEGIN)
    finish = body.index(GEN_END, start) + len(GEN_END)
    return body[:start] + block + body[finish:]


def state_label(state: str) -> str:
    if state not in {
        "ready", "blocked", "active", "awaiting-gate", "failing",
        "complete", "excluded",
    }:
        raise ModelError(f"unknown lifecycle state: {state}")
    return f"port-{state}"


def generated_body(record: dict, packet: dict | None = None) -> str:
    blockers = list(record.get("blockers") or [])
    op = record.get("operational_blocker")
    if op:
        blockers.append(f"{op['reason']} (unblock: {op['unblock']})")
    state = record["state"]
    current = state
    if blockers:
        qualifier = "by" if state == "blocked" else "with recorded blockers"
        current += f" {qualifier} " + "; ".join(f"`{item}`" for item in blockers)
    packet_name = (packet or {}).get("id") or "unclaimed"
    source = record["source"]
    name = record["name"]
    return "\n".join((
        f"**Routine:** `{name}`",
        f"**Pret source:** `{source}:{record['line']}`",
        f"**Size / refs:** {record['size']} bytes / {record['refs']} refs",
        f"**Current state:** {current}",
        f"**Factory packet:** `{packet_name}`",
        "",
        "### Required deliverables",
        "- C implementation and declaration",
        "- probe adapter",
        "- schema-2 oracle cases covering zero, poisoned registers, and boundaries",
        "- recorded mutation that turns the oracle red",
        "- routine oracle PASS and release-gate verification",
        "",
        "### Verification",
        f"`just oracle-diff {name}`",
    ))


def desired_body(record: dict, existing: str = "", packet: dict | None = None) -> str:
    generated = generated_body(record, packet)
    marker = marker_for(record["work_id"])
    if existing:
        existing_marker = parse_marker(existing)
        if existing_marker and existing_marker != record["work_id"]:
            raise ModelError(f"body marker mismatch for {record['work_id']}")
        if existing_marker:
            legacy_generated = marker + "\n\n" + generated + "\n"
            body = marker if existing.strip() == legacy_generated.strip() else existing
        else:
            body = marker + "\n\n" + existing.lstrip()
        body = replace_generated(body, generated)
    else:
        body = replace_generated(marker, generated)
    if parse_marker(body) != record["work_id"]:
        raise ModelError(f"body marker mismatch for {record['work_id']}")
    return body


def desired_title(record: dict) -> str:
    return f"[T{record['tier']}] Port {record['name']}"


def desired_labels(record: dict, existing: list[str] | None = None) -> list[str]:
    labels = set(existing or [])
    labels.difference_update({"tier-1", "tier-2", "tier-3", "tier-4"} | LIFECYCLE)
    labels.update({"port", f"tier-{record['tier']}", state_label(record["state"])})
    return sorted(labels)


def load_report() -> dict:
    spec = importlib.util.spec_from_file_location("port_progress_report", REPORT_PATH)
    if spec is None or spec.loader is None:
        raise ModelError("cannot load progress report")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    inventory = module.load_inventory()
    routines = module.load_routines()[0]
    gate = module.load_gate()
    report = module.compute(inventory, routines, gate)
    active = {}
    queue = ROOT / ".factory" / "queue"
    active_states = {"pending", "translating", "translated", "verifying", "repair", "green"}
    for path in (sorted(queue.glob("*.json")) if queue.is_dir() else ()):
        packet = json.loads(path.read_text())
        if packet.get("state") not in active_states:
            continue
        for routine in packet.get("routines", []):
            name = routine["name"]
            work_id = routine["work_id"]
            if not isinstance(work_id, str) or not work_id:
                raise ModelError(
                    f"active packet {packet['id']} routine {name!r} "
                    "missing work ID"
                )
            if work_id in active:
                raise ModelError(
                    f"work ID {work_id} claimed by multiple active packets: "
                    f"{active[work_id]['id']} and {packet['id']}"
                )
            active[work_id] = {
                "id": packet["id"],
                "state": packet["state"],
                "issue_number": routine.get("issue_number"),
            }
    report["work_records"] = module.project_work_records(
        report["functions"], gate, active_packets=active,
    )
    return report


def record_map(report: dict) -> dict[str, dict]:
    records = report.get("work_records")
    if records is None:
        raise ModelError("progress report has no work-record projection")
    result = {}
    for record in records:
        work_id = record.get("work_id")
        if not work_id:
            continue
        if work_id in result:
            raise ModelError(f"duplicate desired work ID: {work_id}")
        result[work_id] = record
    return result


def indexed_issues(snapshot: dict) -> tuple[dict[str, dict], list[dict]]:
    by_work: dict[str, dict] = {}
    unmarked: list[dict] = []
    for raw in sorted(snapshot["issues"], key=lambda item: int(item["number"])):
        issue = normalize_issue(raw)
        work_id = parse_marker(issue["body"])
        if work_id is None:
            unmarked.append(issue)
            continue
        if work_id in by_work:
            raise ModelError(
                f"work ID {work_id} appears on issues "
                f"#{by_work[work_id]['number']} and #{issue['number']}"
            )
        by_work[work_id] = issue
    return by_work, unmarked


def forgejo_coverage_complete(snapshot: dict, report: dict | None = None) -> bool:
    report = report or load_report()
    records = record_map(report)
    managed, _ = indexed_issues(snapshot)
    desired = {
        work_id for work_id, record in records.items()
        if record["state"] != "excluded"
    }
    return bool(managed) and desired <= set(managed) <= set(records)


def action_for(record: dict, issue: dict | None) -> dict | None:
    if record["state"] == "excluded" and issue is None:
        return None
    body = desired_body(
        record, issue["body"] if issue else "", record.get("packet")
    )
    labels = desired_labels(record, issue.get("labels") if issue else None)
    title = desired_title(record)
    target_state = "closed" if record["state"] == "complete" else "open"
    if issue is None:
        return {
            "action": "create", "work_id": record["work_id"], "issue_number": None,
            "old_state": None, "desired_state": target_state,
            "reason": f"missing managed issue for {record['name']}",
            "title": title, "body": body, "labels": labels,
            "body_hash": sha(body), "labels_hash": sha(labels),
            "source_hash": None,
        }
    current_state = "closed" if issue["state"] == "closed" else "open"
    if (
        issue["title"] == title and issue["body"] == body
        and issue["labels"] == labels and current_state == target_state
    ):
        return None
    return {
        "action": "update", "work_id": record["work_id"],
        "issue_number": issue["number"], "old_state": current_state,
        "desired_state": target_state,
        "reason": f"reconcile {record['state']} state for {record['name']}",
        "title": title, "body": body, "labels": labels,
        "body_hash": sha(body), "labels_hash": sha(labels),
        "source_hash": issue_fingerprint(issue),
    }


def desired_plan(snapshot: dict, report: dict | None = None) -> dict:
    report = report or load_report()
    records = record_map(report)
    migrations = report.get("id_migrations") or {}
    by_work, unmarked = indexed_issues(snapshot)
    actions = []
    migrated_new: set[str] = set()
    for work_id in sorted(by_work):
        if work_id in records:
            continue
        new_id = migrations.get(work_id)
        if not new_id:
            raise ModelError(
                f"managed issue #{by_work[work_id]['number']} references "
                f"disappeared work ID {work_id}"
            )
        if new_id not in records or new_id in by_work:
            raise ModelError(f"invalid explicit work-ID migration {work_id} -> {new_id}")
        old_issue = by_work[work_id]
        record = records[new_id]
        migrated_body = MARKER.sub(
            marker_for(new_id), old_issue["body"], count=1,
        )
        migrated_issue = dict(old_issue, body=migrated_body)
        action = action_for(record, migrated_issue)
        if action:
            action["action"] = "migrate-id"
            action["work_id"] = new_id
            action["reason"] = f"explicit work-ID migration {work_id} -> {new_id}"
            action["source_hash"] = issue_fingerprint(old_issue)
            actions.append(action)
        migrated_new.add(new_id)
    for work_id in sorted(records):
        if work_id in migrated_new:
            continue
        action = action_for(records[work_id], by_work.get(work_id))
        if action:
            actions.append(action)
    return {
        "schema": 1,
        "source_snapshot": snapshot_fingerprint(snapshot),
        "actions": actions,
        "ignored_unmarked": [issue["number"] for issue in unmarked],
        "desired": len([r for r in records.values() if r["state"] != "excluded"]),
    }


def save_plan(plan: dict, path: Path = PLAN_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, sort_keys=True, indent=2) + "\n")


def print_plan(plan: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(plan, sort_keys=True, separators=(",", ":")))
        return
    print(f"actions: {len(plan['actions'])}")
    for action in plan["actions"]:
        number = (
            f"#{action['issue_number']}" if action.get("issue_number") else "new"
        )
        work_id = action.get("work_id", "legacy aggregate")
        print(f"{action['action']:18} {number:8} {work_id} "
              f"{action.get('old_state')} -> {action.get('desired_state')}")
    if plan.get("ignored_unmarked"):
        print("ignored unmarked issues: " + ", ".join(
            f"#{number}" for number in plan["ignored_unmarked"]))


def load_committed_report(path: Path) -> dict:
    if not path.exists():
        raise ModelError(
            f"{path} missing; run `just progress` first, "
            f"or pass --live-report to recompute in memory"
        )
    return json.loads(path.read_text())


def assert_gate_fresh() -> None:
    """Refuse to reconcile when a gate input changed after the gate ran."""
    gate_path = ROOT / "site" / "data" / "gate.json"
    if not gate_path.exists():
        raise ModelError(f"{gate_path} missing; run `just oracle-release-gate`")
    recorded = json.loads(gate_path.read_text()).get("commit")
    if not recorded:
        raise ModelError(f"{gate_path} records no commit; re-run the gate")
    spec = importlib.util.spec_from_file_location("port_gate_trust", REPORT_PATH)
    if spec is None or spec.loader is None:
        raise ModelError("cannot load progress report")
    report = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(report)
    head = report.current_revision()
    if not head:
        raise ModelError("cannot resolve the current revision")
    if recorded != head and report.gate_inputs_changed(recorded, head):
        raise ModelError(
            f"gate at {recorded[:12]} predates a change to a measured path; "
            f"run `just oracle-release-gate && just progress` before reconciling"
        )


def api_request(path: str, payload: dict | None = None,
                *, method: str = "GET") -> object:
    dotenv = dotenv_credentials()
    headers = {
        "Accept": "application/json",
        "Authorization": forgejo_authorization(dotenv=dotenv),
        "User-Agent": USER_AGENT,
        **cloudflare_access_headers(dotenv),
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    owner = urllib.parse.quote(FORGEJO_OWNER, safe="")
    repo = urllib.parse.quote(FORGEJO_REPO, safe="")
    url = f"{FORGEJO_URL}/api/v1/repos/{owner}/{repo}{path}"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                content_type = response.headers.get("Content-Type", "")
                body = response.read()
            if content_type.startswith("text/html"):
                raise ModelError(
                    f"Cloudflare Access intercepted {url}: the service token is "
                    "not authorized for the Forgejo REST API "
                    "(see docs/jj-workflow.md)"
                )
            return json.loads(body) if body else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:200]
            if exc.code in TRANSIENT_STATUS and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise ModelError(
                f"{method} {path} returned HTTP {exc.code}: {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            if attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise ModelError(f"{method} {path} failed: {exc}") from exc
    raise AssertionError("unreachable")


def label_ids() -> dict[str, int]:
    return {entry["name"]: entry["id"] for entry in api_request("/labels")}


def apply_action(action: dict, ids: dict[str, int]) -> None:
    number = action["issue_number"]
    if number is None:
        raise ModelError(
            f"cannot apply a create action for {action['work_id']}: "
            f"managed issues are created in Forgejo, not by this tool"
        )
    expected = action.get("source_hash")
    if expected:
        current = normalize_issue(api_request(f"/issues/{number}"))
        actual = issue_fingerprint(current)
        if actual != expected:
            raise ModelError(
                f"source drift for issue #{number}: expected {expected}, "
                f"found {actual}"
            )
    api_request(f"/issues/{number}", {
        "title": action["title"],
        "body": action["body"],
        "state": action["desired_state"],
    }, method="PATCH")
    api_request(f"/issues/{number}/labels",
                {"labels": [ids[name] for name in action["labels"]]},
                method="PUT")


def apply_plan(plan: dict, *, workers: int = 8) -> tuple[int, list[tuple]]:
    actions = plan["actions"]
    ids = label_ids()
    missing = {name for a in actions for name in a["labels"]} - set(ids)
    if missing:
        raise ModelError(f"Forgejo repository lacks labels: {sorted(missing)}")

    def work(action: dict) -> tuple[dict, str | None]:
        try:
            apply_action(action, ids)
            return action, None
        except ModelError as exc:
            return action, str(exc)

    applied = 0
    failures: list[tuple] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for action, error in pool.map(work, actions):
            if error is None:
                applied += 1
            else:
                failures.append((action["issue_number"], error))
    return applied, failures



def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("fetch")
    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("--json", action="store_true")
    plan_parser.add_argument("--cache", type=Path, default=CACHE)
    plan_parser.add_argument("--report", type=Path, default=PROGRESS_JSON)
    plan_parser.add_argument("--live-report", action="store_true")
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--cache", type=Path, default=CACHE)
    verify_parser.add_argument("--live", action="store_true")
    sync_parser = sub.add_parser("sync")
    sync_parser.add_argument("--apply", action="store_true")
    sync_parser.add_argument("--cache", type=Path, default=CACHE)
    sync_parser.add_argument("--report", type=Path, default=PROGRESS_JSON)
    sync_parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    try:
        if args.command == "fetch":
            snapshot = fetch_snapshot()
            print(
                f"fetched {len(snapshot['issues'])} Forgejo issues into {CACHE}"
            )
            return 0
        if args.command == "plan":
            snapshot = load_cache(path=args.cache)
            report = None if args.live_report else load_committed_report(args.report)
            plan = desired_plan(snapshot, report)
            save_plan(plan)
            print_plan(plan, args.json)
            return 0
        if args.command == "verify":
            snapshot = fetch_snapshot() if args.live else load_cache(path=args.cache)
            managed, _ = indexed_issues(snapshot)
            if not forgejo_coverage_complete(snapshot):
                raise ModelError(
                    "Forgejo snapshot does not cover every canonical routine"
                )
            print(
                f"issues: {len(managed)} managed routines, full Forgejo coverage"
            )
            return 0
        if args.command == "sync":
            assert_gate_fresh()
            plan = desired_plan(load_cache(path=args.cache),
                                load_committed_report(args.report))
            save_plan(plan)
            if not plan["actions"]:
                print("issues: already reconciled, 0 actions")
                return 0
            if not args.apply:
                print_plan(plan, False)
                print(f"\ndry run: {len(plan['actions'])} action(s); "
                      f"pass --apply to write them to Forgejo")
                return 0
            applied, failures = apply_plan(plan, workers=args.workers)
            print(f"applied {applied}/{len(plan['actions'])} action(s)")
            for number, error in failures[:20]:
                print(f"  FAILED #{number}: {error}")
            if failures:
                raise ModelError(f"{len(failures)} action(s) failed")
            residual = desired_plan(fetch_snapshot(),
                                    load_committed_report(args.report))
            if residual["actions"]:
                raise ModelError(
                    f"reconciliation incomplete: "
                    f"{len(residual['actions'])} action(s) still pending"
                )
            print("issues: reconciled, plan is empty")
            return 0
    except (ModelError, OSError, json.JSONDecodeError) as exc:
        fail(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
