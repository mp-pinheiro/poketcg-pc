#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import forgejo

ROOT = Path(__file__).resolve().parents[2]
CF_TOKEN_FILE = Path(os.environ.get(
    "POKETCG_CF_ACCESS_TOKEN_FILE",
    "~/.config/yfrit-forgejo/git/cloudflare-access-service-token.json",
)).expanduser()


def check_helpers() -> tuple[str, str]:
    helper = ROOT / "tools" / "git-credential-forgejo"
    return ("ok", f"helpers: {helper}") if helper.is_file() else ("fail", "helpers: credential helper missing")


def check_credentials() -> tuple[str, str]:
    try:
        token = forgejo._authorization()
        headers = forgejo._credentials(forgejo.DEFAULT_URL)
    except forgejo.ForgejoError as exc:
        return "fail", f"credentials: {exc}"
    required = {"CF-Access-Client-Id", "CF-Access-Client-Secret"}
    if not required <= set(headers):
        return "fail", "credentials: Cloudflare headers missing"
    return "ok", f"credentials: token length={len(token)} edge headers present"


def check_git() -> tuple[str, str]:
    result = subprocess.run(
        ["git", "ls-remote", "https://forgejo.yfrit.com/mpp/poketcg-pc"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    return ("ok", "git: origin read succeeded") if result.returncode == 0 else ("fail", "git: origin read failed")


def check_rest() -> tuple[str, str]:
    try:
        client = forgejo.ForgejoClient()
        payload = client.request_json("GET", "/issues", query={"state": "all", "type": "issues", "limit": 1, "page": 1})
    except forgejo.ForgejoError as exc:
        return "fail", f"rest: {exc}"
    if not isinstance(payload, list):
        return "fail", "rest: issue endpoint returned a non-list"
    return "ok", "rest: issue endpoint read succeeded"


def check_expiry() -> tuple[str, str] | None:
    try:
        expires_at = json.loads(CF_TOKEN_FILE.read_text())["expires_at"]
        expiry = datetime.fromisoformat(expires_at)
    except (OSError, ValueError, KeyError, TypeError):
        return None
    remaining = expiry - datetime.now(UTC)
    status = "warn" if remaining < timedelta(days=30) else "ok"
    return status, f"cf-expiry: {remaining.days}d remaining"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-rest", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = [check_helpers(), check_credentials(), check_git(), check_rest()]
    if expiry := check_expiry():
        results.append(expiry)
    if args.require_rest:
        results = [("fail" if status == "warn" and detail.startswith("rest:") else status, detail) for status, detail in results]
    if args.json:
        print(json.dumps([{"status": status, "detail": detail} for status, detail in results], sort_keys=True))
    else:
        for status, detail in results:
            print(f"[{status}] {detail}")
    return 1 if any(status == "fail" for status, _detail in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
