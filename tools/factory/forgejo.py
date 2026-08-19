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
from datetime import UTC, datetime, timedelta
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
MAX_PAGES = 400
TRANSIENT_CODES = frozenset({429, 502, 503, 504})
REQUEST_TIMEOUT_SECONDS = 30.0
REQUEST_DEADLINE_SECONDS = 120.0
LISTING_PATH = ROOT / ".factory" / "v2" / "listing.json"
LISTING_OVERLAP = timedelta(minutes=5)


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


def _total_count(response: Response) -> int | None:
    raw = response.headers.get("x-total-count")
    if raw is None or not raw.isdigit():
        return None
    return int(raw)


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


_CREDENTIALS: dict[str, dict[str, str]] = {}


def _credentials(url: str) -> dict[str, str]:
    cached = _CREDENTIALS.get(url)
    if cached is not None:
        return dict(cached)
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
    _CREDENTIALS[url] = dict(headers)
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
        listing_path: Path | None = LISTING_PATH,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.owner = owner
        self.repo = repo
        self._open = request or urllib.request.urlopen
        self._sleep = sleep
        self.listing_path = listing_path
        self._labels: dict[str, int] | None = None

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
        deadline = time.monotonic() + REQUEST_DEADLINE_SECONDS
        for attempt in range(retries):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ForgejoUnavailable(f"{method} {path} exceeded its {REQUEST_DEADLINE_SECONDS:.0f}s deadline")
            try:
                with self._open(request, timeout=min(REQUEST_TIMEOUT_SECONDS, remaining)) as response:
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
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt + 1 < retries and time.monotonic() < deadline:
                    self._sleep(min(2 ** attempt, max(0.0, deadline - time.monotonic())))
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

    def _pages(
        self,
        path: str,
        *,
        query: dict[str, object] | None = None,
    ) -> tuple[list[dict[str, Any]], int | None]:
        """Page until the server stops yielding new rows.

        Some Forgejo collections (issue comments) ignore `page` entirely and
        replay the same rows, so a length-only stop condition never fires.
        """
        page = 1
        rows: list[dict[str, Any]] = []
        seen: set[int] = set()
        total: int | None = None
        while page <= MAX_PAGES:
            values = dict(query or {})
            values.update({"page": page, "limit": PAGE_SIZE})
            response = self._request("GET", path, query=values)
            payload = response.payload
            if not isinstance(payload, list):
                raise ForgejoError(f"{path} page {page} is not a list")
            if total is None:
                total = _total_count(response)
            fresh = 0
            for row in payload:
                if not isinstance(row, dict):
                    continue
                identifier = row.get("id")
                if isinstance(identifier, int):
                    if identifier in seen:
                        continue
                    seen.add(identifier)
                rows.append(row)
                fresh += 1
            if fresh == 0 or len(payload) < PAGE_SIZE:
                return rows, total
            if total is not None and len(rows) >= total:
                return rows, total
            page += 1
        raise ForgejoError(f"{path} exceeded {MAX_PAGES} pages without completing")

    def _total_issues(self) -> int | None:
        response = self._request("GET", "/issues", query={
            "state": "all", "type": "issues", "limit": 1, "page": 1,
        })
        return _total_count(response)

    def _full_issue_listing(self) -> tuple[list[dict[str, Any]], int | None]:
        raw, total = self._pages("/issues", query={"state": "all", "type": "issues"})
        return [normalize_issue(row) for row in raw], total

    def _incremental_issue_listing(
        self,
        cached: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], int | None] | None:
        watermark = max(
            (parse_time(issue.get("updated_at")) for issue in cached),
            default=None,
        )
        total = self._total_issues()
        if watermark is None or total is None:
            return None
        raw, _filtered = self._pages("/issues", query={
            "state": "all",
            "type": "issues",
            "since": (watermark - LISTING_OVERLAP).isoformat(),
        })
        merged = {issue["number"]: issue for issue in cached}
        for row in raw:
            issue = normalize_issue(row)
            merged[issue["number"]] = issue
        if len(merged) != total:
            return None
        return list(merged.values()), total

    def issues(self) -> list[dict[str, Any]]:
        cached = self._load_listing()
        result = self._incremental_issue_listing(cached) if cached else None
        if result is None:
            result = self._full_issue_listing()
        issues, total = result
        numbers = [issue["number"] for issue in issues]
        if len(numbers) != len(set(numbers)):
            raise ForgejoError("Forgejo issue listing has duplicate numbers")
        if total is not None and len(numbers) != total:
            raise ForgejoError(f"Forgejo listed {len(numbers)} issues but reports {total}")
        listing = sorted(issues, key=lambda issue: issue["number"])
        self._store_listing(listing)
        return listing

    def _load_listing(self) -> list[dict[str, Any]] | None:
        if self.listing_path is None:
            return None
        try:
            value = json.loads(self.listing_path.read_text())
        except (OSError, json.JSONDecodeError):
            return None
        issues = value.get("issues")
        if value.get("repository") != self.repository or not isinstance(issues, list) or not issues:
            return None
        return [normalize_issue(issue) for issue in issues]

    def _store_listing(self, issues: list[dict[str, Any]]) -> None:
        if self.listing_path is None:
            return
        self.listing_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.listing_path.with_suffix(f".{os.getpid()}.tmp")
        temporary.write_text(canonical_json({
            "schema": 1,
            "repository": self.repository,
            "issues": issues,
        }))
        os.replace(temporary, self.listing_path)

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
        """Walk a comment thread forward by timestamp.

        The comments endpoint ignores `page` and caps each response, so `since`
        is the only cursor that reaches events beyond the first page.
        """
        collected: dict[int, dict[str, Any]] = {}
        cursor = since
        for _ in range(MAX_PAGES):
            query: dict[str, object] = {"limit": PAGE_SIZE}
            if cursor:
                query["since"] = cursor
            payload = self.request_json("GET", f"/issues/{number}/comments", query=query)
            if not isinstance(payload, list):
                raise ForgejoError(f"issue #{number} comments response is not a list")
            page = [normalize_comment(raw) for raw in payload if isinstance(raw, dict)]
            fresh = [comment for comment in page if comment["id"] not in collected]
            for comment in fresh:
                collected[comment["id"]] = comment
            if not fresh or len(page) < PAGE_SIZE:
                break
            newest = max((str(comment.get("created_at") or "") for comment in page), default="")
            if not newest or newest == cursor:
                break
            cursor = newest
        return sorted(collected.values(), key=lambda comment: comment["id"])

    def comments_since(self, number: int, since: str | None = None) -> list[dict[str, Any]]:
        return self.comments(number, since=since)

    def dependencies(self, number: int) -> list[dict[str, Any]]:
        rows, _total = self._pages(f"/issues/{number}/dependencies")
        return [normalize_issue(raw) for raw in rows]

    def labels(self) -> dict[str, int]:
        if self._labels is not None:
            return dict(self._labels)
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
        self._labels = dict(labels)
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
        self._labels = None
        current = self.labels()
        for name, (color, description, exclusive) in labels.items():
            if name not in current:
                current[name] = self.create_label(
                    name=name,
                    color=color,
                    description=description,
                    exclusive=exclusive,
                )
        self._labels = dict(current)
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
        created = self.append_comment(number, body)
        if event_id in created["body"]:
            return created
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
        patch: dict[str, Any] = {}
        if state != current["state"]:
            patch["state"] = state
        if title is not None and title != current["title"]:
            patch["title"] = title
        if body is not None and body != current["body"]:
            patch["body"] = body
        if patch:
            current = normalize_issue(self.request_json("PATCH", f"/issues/{number}", payload=patch))
        desired = sorted(set(labels))
        if desired == current["labels"]:
            return current
        ids = self.labels()
        missing = sorted(set(desired) - set(ids))
        if missing:
            raise ForgejoError(f"Forgejo labels are missing: {missing}")
        payload = self.request_json(
            "PUT", f"/issues/{number}/labels", payload={"labels": [ids[label] for label in desired]},
        )
        names = sorted({
            row["name"] for row in payload
            if isinstance(row, dict) and isinstance(row.get("name"), str)
        }) if isinstance(payload, list) else desired
        return {**current, "labels": names}

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
