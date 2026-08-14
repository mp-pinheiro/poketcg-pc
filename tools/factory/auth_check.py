#!/usr/bin/env python3
"""Prove Forgejo git + REST credentials authenticate with no browser prompt.

Reuses tools/factory/issues.py's credential resolution so this check and the
REST client never drift. Hard checks (helpers, edge-headers, token,
git-push-auth) fail the run; rest is soft until Cloudflare Access is opened
to /api/v1/* (see docs/jj-workflow.md), and cf-expiry only warns.
"""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_spec = importlib.util.spec_from_file_location(
    "issue_model", ROOT / "tools/factory/issues.py"
)
issues = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(issues)


def run_git_config(key: str) -> list[str]:
    result = subprocess.run(
        ["git", "config", "--get-all", key],
        capture_output=True, text=True, check=False,
    )
    return [line for line in result.stdout.splitlines() if line != ""]


def check_helpers() -> tuple[str, str]:
    entries = run_git_config("credential.https://forgejo.yfrit.com.helper")
    problems = []
    for entry in entries:
        if "oauth" in entry.lower():
            problems.append(f"interactive helper configured: {entry}")
            continue
        path = Path(entry)
        if not path.is_absolute() or not os.access(path, os.X_OK):
            problems.append(f"helper missing or not executable: {entry}")
    if problems:
        return "fail", "helpers: " + "; ".join(problems)
    configured = ", ".join(entries) if entries else "(none)"
    return "ok", f"helpers: {configured}"


def check_edge_headers() -> tuple[str, str]:
    entries = run_git_config("http.https://forgejo.yfrit.com/.extraheader")
    has_id = any(line.startswith("CF-Access-Client-Id:") for line in entries)
    has_secret = any(line.startswith("CF-Access-Client-Secret:") for line in entries)
    if has_id and has_secret:
        return "ok", "edge-headers: CF-Access-Client-Id and CF-Access-Client-Secret set"
    remediation = (
        'git config --global http.https://forgejo.yfrit.com/.extraHeader '
        '"CF-Access-Client-Id: <client-id>.access" && '
        'git config --global --add http.https://forgejo.yfrit.com/.extraHeader '
        '"CF-Access-Client-Secret: <client-secret>" (see docs/jj-workflow.md)'
    )
    return "fail", f"edge-headers: missing CF-Access headers ({remediation})"


def token_source(dotenv: dict[str, str]) -> str:
    if os.environ.get("POKETCG_FORGEJO_TOKEN"):
        return "env"
    if dotenv.get("POKETCG_FORGEJO_TOKEN"):
        return ".env"
    return str(issues.FORGEJO_TOKEN_FILE)


def check_token(dotenv: dict[str, str]) -> tuple[str, str, str | None]:
    try:
        token = issues.forgejo_authorization(dotenv=dotenv)
    except issues.ModelError as exc:
        return "fail", f"token: {exc}", None
    source = token_source(dotenv)
    return "ok", f"token: source={source} length={len(token)}", token


def strip_scheme(token: str) -> str:
    for prefix in ("token ", "Token ", "bearer ", "Bearer "):
        if token.startswith(prefix):
            return token[len(prefix):]
    return token


def check_git_push_auth(dotenv: dict[str, str], token: str | None) -> tuple[str, str]:
    if token is None:
        return "fail", "git-push-auth: no token available"
    user = os.environ.get("POKETCG_FORGEJO_USER", "mpp")
    basic = base64.b64encode(f"{user}:{strip_scheme(token)}".encode()).decode()
    try:
        cf_headers = issues.cloudflare_access_headers(dotenv)
    except issues.ModelError as exc:
        return "fail", f"git-push-auth: {exc}"
    owner = urllib.parse.quote(issues.FORGEJO_OWNER, safe="")
    repo = urllib.parse.quote(issues.FORGEJO_REPO, safe="")
    # Advertises refs only (service=git-receive-pack) — never updates one.
    url = (f"{issues.FORGEJO_URL}/{owner}/{repo}.git/info/refs"
           "?service=git-receive-pack")
    headers = {
        "Authorization": f"Basic {basic}",
        "User-Agent": issues.USER_AGENT,
        **cf_headers,
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        first_line = detail.splitlines()[0] if detail else ""
        return "fail", f"git-push-auth: HTTP {exc.code} {first_line}"
    except urllib.error.URLError as exc:
        return "fail", f"git-push-auth: {exc}"
    if content_type.startswith("text/html"):
        return "fail", ("git-push-auth: Cloudflare Access rejected the "
                        "service token on the git routes")
    if content_type.startswith("application/x-git-receive-pack-advertisement"):
        return "ok", f"git-push-auth (200 {content_type})"
    return "fail", f"git-push-auth: unexpected content-type {content_type}"


def check_rest(dotenv: dict[str, str], token: str | None) -> tuple[str, str]:
    if token is None:
        return "fail", "rest: no token available"
    try:
        cf_headers = issues.cloudflare_access_headers(dotenv)
    except issues.ModelError as exc:
        return "fail", f"rest: {exc}"
    owner = urllib.parse.quote(issues.FORGEJO_OWNER, safe="")
    repo = urllib.parse.quote(issues.FORGEJO_REPO, safe="")
    url = f"{issues.FORGEJO_URL}/api/v1/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/json",
        "Authorization": token,
        "User-Agent": issues.USER_AGENT,
        **cf_headers,
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            body = response.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            detail = exc.read().decode(errors="replace")
            if "1010" in detail:
                return "warn", "rest: blocked by the Cloudflare WAF (User-Agent)"
        return "fail", f"rest: HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return "fail", f"rest: {exc}"
    if content_type.startswith("text/html") and b"Cloudflare Access" in body:
        return "warn", (
            "rest: blocked by Cloudflare Access: the service token is not in "
            'a policy covering /api/v1/* (add a path-scoped app with a '
            'non_identity service-token policy, like "Metabase MCP service auth")'
        )
    if content_type.startswith("application/json"):
        payload = json.loads(body)
        push = payload.get("permissions", {}).get("push")
        return "ok", f"rest: permissions.push={push}"
    return "fail", f"rest: unexpected response {content_type}"


def check_cf_expiry() -> tuple[str, str] | None:
    try:
        payload = json.loads(issues.CF_TOKEN_FILE.read_text())
        expires_at = payload["expires_at"]
    except (OSError, ValueError, KeyError):
        return None
    expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    remaining = expiry - datetime.now(timezone.utc)
    detail = (f"cf-expiry: service token expires {expires_at} "
              f"({remaining.days}d remaining)")
    if remaining < timedelta(days=30):
        return "warn", detail
    return "ok", detail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--require-rest", action="store_true")
    args = parser.parse_args()

    dotenv = issues.dotenv_credentials()

    results: list[tuple[str, str]] = [check_helpers(), check_edge_headers()]
    token_status, token_detail, token = check_token(dotenv)
    results.append((token_status, token_detail))
    results.append(check_git_push_auth(dotenv, token))

    rest_status, rest_detail = check_rest(dotenv, token)
    if args.require_rest and rest_status == "warn":
        rest_status = "fail"
    results.append((rest_status, rest_detail))

    expiry_result = check_cf_expiry()
    if expiry_result is not None:
        results.append(expiry_result)

    if args.json:
        print(json.dumps(
            [{"status": status, "detail": detail} for status, detail in results],
            sort_keys=True,
        ))
    else:
        for status, detail in results:
            print(f"[{status}] {detail}")

    return 1 if any(status == "fail" for status, _ in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
