#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_URL = os.environ.get("POKETCG_FORGEJO_URL", "https://forgejo.yfrit.com").rstrip("/")
DEFAULT_OWNER = os.environ.get("POKETCG_FORGEJO_OWNER", "mpp")
DEFAULT_REPO = os.environ.get("POKETCG_FORGEJO_REPO", "poketcg-pc")
TOKEN_PATH = Path(os.environ.get(
    "POKETCG_FORGEJO_TOKEN_FILE",
    "~/.config/yfrit-forgejo/api/poketcg-issues.token",
)).expanduser()
USER_AGENT = "poketcg-factory-v2/1.0"
PAGE_SIZE = 50
TRANSIENT_CODES = frozenset({429, 502, 503, 504})


class ForgejoError(RuntimeError):
    pass


class ForgejoConflict(ForgejoError):
    pass


class ForgejoUnavailable(ForgejoError):
    pass

def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).astimezone(UTC)
    except ValueError:
        return None


def _header_values(url: str) -> list[str]:
    parsed = urllib.parse.urlparse(url)
    key = f"http.{parsed.scheme}://{parsed.netloc}/.extraHeader"
    values: list[str] = []
    for command in (
        ["git", "config", "--get-urlmatch", "http.extraHeader", url],
        ["git", "config", "--get-all", key],
    ):
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            values.extend(line for line in result.stdout.splitlines() if line)
    return list(dict.fromkeys(values))


def _authorization() -> str:
    token = os.environ.get("POKETCG_FORGEJO_TOKEN")
    if not token:
        try:
            token = TOKEN_PATH.read_text().strip()
        except OSError as exc:
            raise ForgejoError("Forgejo token file is unavailable") from exc
    if token.lower().startswith("authorization:"):
        token = token.split(":", 1)[1].strip()
    if not token:
        raise ForgejoError("Forgejo token is empty")
    if not token.lower().startswith(("token ", "bearer ")):
        token = f"token {token}"
    return token


def _credentials(url: str) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Authorization": _authorization(),
        "User-Agent": USER_AGENT,
    }
    for raw in _header_values(url):
        name, separator, value = raw.partition(":")
        if not separator or not name.strip() or not value.strip():
            continue
        if name.strip().lower() in {
            "cf-access-client-id",
            "cf-access-client-secret",
        }:
            headers[name.strip()] = value.strip()
    for env_name, header_name in (
        ("CF_ACCESS_CLIENT_ID", "CF-Access-Client-Id"),
        ("CF_ACCESS_CLIENT_SECRET", "CF-Access-Client-Secret"),
    ):
        if env_value := os.environ.get(env_name):
            headers[header_name] = env_value
    missing = {
        "CF-Access-Client-Id",
        "CF-Access-Client-Secret",
    } - set(headers)
    if missing:
        raise ForgejoError("Forgejo Cloudflare headers are unavailable")
    return headers


def normalize_issue(raw: dict[str, Any]) -> dict[str, Any]:
    labels: list[str] = []
    for label in raw.get("labels") or []:
        name = label.get("name") if isinstance(label, dict) else label
        if not isinstance(name, str) or not name:
            raise ForgejoError(f"issue #{raw.get('number')} has an invalid label")
        labels.append(name)
    number = raw.get("number")
    if not isinstance(number, int) or number <= 0:
        raise ForgejoError("Forgejo issue has no positive number")
    state = str(raw.get("state", "")).lower()
    if state not in {"open", "closed"}:
        raise ForgejoError(f"issue #{number} has invalid state {state!r}")
    user = raw.get("user") if isinstance(raw.get("user"), dict) else {}
    return {
        "id": raw.get("id"),
        "number": number,
        "title": str(raw.get("title") or ""),
        "body": str(raw.get("body") or ""),
        "state": state,
        "labels": sorted(set(labels)),
        "url": str(raw.get("html_url") or raw.get("url") or ""),
        "created_at": raw.get("created_at"),
        "updated_at": raw.get("updated_at"),
        "author": str(user.get("login") or ""),
    }


def issue_fingerprint(issue: dict[str, Any]) -> str:
    return sha256({
        key: issue.get(key)
        for key in ("number", "title", "body", "state", "labels", "updated_at")
    })


def normalize_comment(raw: dict[str, Any]) -> dict[str, Any]:
    identifier = raw.get("id")
    if not isinstance(identifier, int) or identifier <= 0:
        raise ForgejoError("Forgejo comment has no positive id")
    user = raw.get("user") if isinstance(raw.get("user"), dict) else {}
    return {
        "id": identifier,
        "body": str(raw.get("body") or ""),
        "created_at": raw.get("created_at"),
        "updated_at": raw.get("updated_at"),
        "author": str(user.get("login") or ""),
        "html_url": str(raw.get("html_url") or ""),
    }


@dataclass(frozen=True)
class Response:
    status: int
    headers: dict[str, str]
    payload: object


class ForgejoClient:
    def __init__(
        self,
        *,
        base_url: str = DEFAULT_URL,
        owner: str = DEFAULT_OWNER,
        repo: str = DEFAULT_REPO,
        request: Callable[[urllib.request.Request, float], Any] | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.owner = owner
        self.repo = repo
        self._open = request or urllib.request.urlopen
        self._sleep = sleep

    @property
    def repository(self) -> str:
        return f"{self.owner}/{self.repo}"

    def _url(self, path: str, query: dict[str, object] | None = None) -> str:
        owner = urllib.parse.quote(self.owner, safe="")
        repo = urllib.parse.quote(self.repo, safe="")
        suffix = urllib.parse.urlencode(query or {}, doseq=True)
        base = f"{self.base_url}/api/v1/repos/{owner}/{repo}{path}"
        return f"{base}?{suffix}" if suffix else base

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | list[Any] | None = None,
        query: dict[str, object] | None = None,
        retries: int = 4,
    ) -> Response:
        url = self._url(path, query)
        headers = _credentials(self.base_url)
        data: bytes | None = None
        if payload is not None:
            data = canonical_json(payload).encode()
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        for attempt in range(retries):
            try:
                with self._open(request, timeout=60) as response:
                    raw = response.read()
                    content_type = response.headers.get("Content-Type", "")
                    if content_type.startswith("text/html"):
                        raise ForgejoError("Cloudflare Access returned HTML for Forgejo REST")
                    try:
                        parsed = json.loads(raw) if raw else None
                    except json.JSONDecodeError as exc:
                        raise ForgejoError("Forgejo returned invalid JSON") from exc
                    return Response(
                        status=getattr(response, "status", response.getcode()),
                        headers={key.lower(): value for key, value in response.headers.items()},
                        payload=parsed,
                    )
            except urllib.error.HTTPError as exc:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                if exc.code in TRANSIENT_CODES and attempt + 1 < retries:
                    delay = float(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
                    self._sleep(min(delay, 30.0))
                    continue
                if exc.code in {409, 412, 422}:
                    raise ForgejoConflict(f"{method} {path} conflicted with remote state") from exc
                if exc.code in TRANSIENT_CODES:
                    raise ForgejoUnavailable(f"{method} {path} remains unavailable") from exc
                raise ForgejoError(f"{method} {path} returned HTTP {exc.code}") from exc
            except urllib.error.URLError as exc:
                if attempt + 1 < retries:
                    self._sleep(2 ** attempt)
                    continue
                raise ForgejoUnavailable(f"{method} {path} is unreachable") from exc
        raise AssertionError("unreachable")

    def request_json(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | list[Any] | None = None,
        query: dict[str, object] | None = None,
    ) -> object:
        return self._request(method, path, payload=payload, query=query).payload

    def _pages(self, path: str, *, query: dict[str, object] | None = None) -> list[dict[str, Any]]:
        page = 1
        rows: list[dict[str, Any]] = []
        while True:
            values = dict(query or {})
            values.update({"page": page, "limit": PAGE_SIZE})
            payload = self.request_json("GET", path, query=values)
            if not isinstance(payload, list):
                raise ForgejoError(f"{path} page {page} is not a list")
            rows.extend(row for row in payload if isinstance(row, dict))
            if len(payload) < PAGE_SIZE:
                return rows
            page += 1

    def issues(self) -> list[dict[str, Any]]:
        issues = [normalize_issue(raw) for raw in self._pages("/issues", query={"state": "all", "type": "issues"})]
        numbers = [issue["number"] for issue in issues]
        if len(numbers) != len(set(numbers)):
            raise ForgejoError("Forgejo issue listing has duplicate numbers")
        return sorted(issues, key=lambda issue: issue["number"])

    def stable_snapshot(self, *, attempts: int = 4) -> dict[str, Any]:
        if attempts < 2:
            raise ValueError("stable snapshot needs at least two reads")
        prior: str | None = None
        for _ in range(attempts):
            issues = self.issues()
            snapshot = {
                "schema": 1,
                "repository": self.repository,
                "fetched_at": datetime.now(UTC).isoformat(),
                "issues": issues,
            }
            fingerprint = sha256({"repository": self.repository, "issues": issues})
            if fingerprint == prior:
                snapshot["sha256"] = fingerprint
                return snapshot
            prior = fingerprint
            self._sleep(1)
        raise ForgejoConflict("Forgejo issue listing did not stabilize")

    def issue(self, number: int) -> dict[str, Any]:
        return normalize_issue(self.request_json("GET", f"/issues/{number}"))

    def comments(self, number: int, *, since: str | None = None) -> list[dict[str, Any]]:
        query: dict[str, object] = {}
        if since:
            query["since"] = since
        comments = [normalize_comment(raw) for raw in self._pages(f"/issues/{number}/comments", query=query)]
        by_id = {comment["id"]: comment for comment in comments}
        if len(by_id) != len(comments):
            raise ForgejoError(f"issue #{number} has duplicate comment IDs")
        return sorted(comments, key=lambda comment: comment["id"])

    def comments_since(self, number: int, since: str | None = None) -> list[dict[str, Any]]:
        return self.comments(number, since=since)

    def dependencies(self, number: int) -> list[dict[str, Any]]:
        return [normalize_issue(raw) for raw in self._pages(f"/issues/{number}/dependencies")]

    def labels(self) -> dict[str, int]:
        payload = self.request_json("GET", "/labels")
        if not isinstance(payload, list):
            raise ForgejoError("Forgejo labels response is not a list")
        labels: dict[str, int] = {}
        for row in payload:
            if not isinstance(row, dict):
                continue
            name, identifier = row.get("name"), row.get("id")
            if isinstance(name, str) and isinstance(identifier, int):
                labels[name] = identifier
        return labels

    def create_label(
        self,
        *,
        name: str,
        color: str,
        description: str,
        exclusive: bool,
    ) -> int:
        existing = self.labels()
        if name in existing:
            return existing[name]
        payload = {
            "name": name,
            "color": color,
            "description": description,
            "exclusive": exclusive,
        }
        result = self.request_json("POST", "/labels", payload=payload)
        if not isinstance(result, dict) or not isinstance(result.get("id"), int):
            raise ForgejoError(f"Forgejo did not return a label ID for {name}")
        return int(result["id"])

    def ensure_labels(self, labels: dict[str, tuple[str, str, bool]]) -> dict[str, int]:
        current = self.labels()
        for name, (color, description, exclusive) in labels.items():
            if name not in current:
                current[name] = self.create_label(
                    name=name,
                    color=color,
                    description=description,
                    exclusive=exclusive,
                )
        return current

    def create_issue(self, *, title: str, body: str, labels: list[str]) -> dict[str, Any]:
        issue = normalize_issue(self.request_json("POST", "/issues", payload={"title": title, "body": body}))
        self.set_projection(issue["number"], labels=labels, state="open")
        return self.issue(issue["number"])

    def append_comment(self, number: int, body: str) -> dict[str, Any]:
        return normalize_comment(self.request_json("POST", f"/issues/{number}/comments", payload={"body": body}))

    def append_event(self, number: int, body: str, event_id: str) -> dict[str, Any]:
        for comment in self.comments(number):
            if event_id in comment["body"]:
                return comment
        self.append_comment(number, body)
        for comment in self.comments(number):
            if event_id in comment["body"]:
                return comment
        raise ForgejoConflict(f"event {event_id} was not readable after append to #{number}")

    def set_projection(
        self,
        number: int,
        *,
        labels: list[str],
        state: str,
        title: str | None = None,
        body: str | None = None,
        expected_fingerprint: str | None = None,
    ) -> dict[str, Any]:
        current = self.issue(number)
        if expected_fingerprint and issue_fingerprint(current) != expected_fingerprint:
            raise ForgejoConflict(f"issue #{number} changed before projection")
        patch: dict[str, Any] = {"state": state}
        if title is not None:
            patch["title"] = title
        if body is not None:
            patch["body"] = body
        self.request_json("PATCH", f"/issues/{number}", payload=patch)
        ids = self.labels()
        missing = sorted(set(labels) - set(ids))
        if missing:
            raise ForgejoError(f"Forgejo labels are missing: {missing}")
        self.request_json("PUT", f"/issues/{number}/labels", payload={"labels": [ids[label] for label in sorted(set(labels))]})
        return self.issue(number)

    def add_dependency(self, number: int, dependency: int) -> None:
        if dependency in {row["number"] for row in self.dependencies(number)}:
            return
        payload = {"owner": self.owner, "repo": self.repo, "index": dependency}
        try:
            self.request_json("POST", f"/issues/{number}/dependencies", payload=payload)
        except ForgejoConflict:
            if dependency not in {row["number"] for row in self.dependencies(number)}:
                raise

    def remove_dependency(self, number: int, dependency: int) -> None:
        if dependency not in {row["number"] for row in self.dependencies(number)}:
            return
        payload = {"owner": self.owner, "repo": self.repo, "index": dependency}
        try:
            self.request_json("DELETE", f"/issues/{number}/dependencies", payload=payload)
        except ForgejoConflict:
            if dependency in {row["number"] for row in self.dependencies(number)}:
                raise
