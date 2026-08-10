#!/usr/bin/env python3
"""Verify immutable inputs used by the function oracles."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tools" / "oracle" / "artifacts.json"
CP312_EXTENSION = re.compile(r"\.cpython-312(?:[-.]|$)")



def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_pyboy_identity(root: Path, manifest: dict) -> int:
    try:
        identity = manifest["identity"]
        if not isinstance(identity, dict):
            raise TypeError("identity must be an object")
        required_identity = (
            "python_implementation",
            "python_version",
            "soabi_family",
            "pyboy_sdist_version",
            "pyboy_sdist_sha256",
            "uv_lock_sha256",
            "wheel_tag",
            "compiled_modules",
        )
        for key in required_identity:
            if key not in identity:
                raise KeyError(f"identity.{key}")
        pyboy_artifact = manifest["pyboy"]
        if not isinstance(pyboy_artifact, dict):
            raise TypeError("pyboy must be an object")
        for key in ("version", "sdist_sha256"):
            if key not in pyboy_artifact:
                raise KeyError(f"pyboy.{key}")
        required_strings = (
            "python_implementation",
            "python_version",
            "soabi_family",
            "pyboy_sdist_version",
            "pyboy_sdist_sha256",
            "uv_lock_sha256",
            "wheel_tag",
        )
        if any(not isinstance(identity[key], str) for key in required_strings):
            raise TypeError("identity scalar values must be strings")
        if any(not isinstance(pyboy_artifact[key], str) for key in ("version", "sdist_sha256")):
            raise TypeError("pyboy artifact values must be strings")
        expected_version = identity["pyboy_sdist_version"]
        expected_sdist_hash = identity["pyboy_sdist_sha256"]
        expected_modules = identity["compiled_modules"]
        if not isinstance(expected_modules, list) or not all(
            isinstance(name, str) for name in expected_modules
        ):
            raise TypeError("identity.compiled_modules must be a list of strings")
    except (KeyError, TypeError) as error:
        return fail(f"pyboy identity manifest invalid: {error}")

    try:
        completed = subprocess.run(
            [sys.executable, str(root / "tools/oracle/fingerprint.py")],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        observed = json.loads(completed.stdout)
        if not isinstance(observed, dict):
            raise TypeError("fingerprint result must be an object")
        python = observed.get("python", {})
        pyboy = observed.get("pyboy", {})
        if not isinstance(python, dict) or not isinstance(pyboy, dict):
            raise TypeError("fingerprint python/pyboy values must be objects")
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError, TypeError) as error:
        return fail(f"pyboy identity probe failed: {error}")

    checks = (
        ("python implementation", python.get("implementation"), identity["python_implementation"]),
        ("python version", python.get("version"), identity["python_version"]),
        ("SOABI family", python.get("soabi_family"), identity["soabi_family"]),
        ("PyBoy version", pyboy.get("version"), expected_version),
        ("uv.lock sha256", observed.get("uv_lock_sha256"), identity["uv_lock_sha256"]),
    )
    for label, actual, wanted in checks:
        if actual != wanted:
            return fail(f"pyboy identity {label} expected={wanted} actual={actual}")

    if pyboy_artifact["version"] != expected_version:
        return fail(
            f"pyboy identity artifact version expected={expected_version} "
            f"actual={pyboy_artifact['version']}"
        )
    if pyboy_artifact["sdist_sha256"] != expected_sdist_hash:
        return fail("pyboy identity sdist hash disagrees with artifact manifest")

    try:
        lock_text = (root / "tools/oracle/uv.lock").read_text()
    except (OSError, UnicodeError) as error:
        return fail(f"pyboy identity lock read failed: {error}")
    if (
        'name = "pyboy"' not in lock_text
        or f'version = "{expected_version}"' not in lock_text
    ):
        return fail(f"pyboy identity lock has no version {expected_version} package")
    if expected_sdist_hash not in lock_text:
        return fail("pyboy identity sdist hash is absent from uv.lock")
    wheel_tags = pyboy.get("wheel_tags", [])
    if not isinstance(wheel_tags, list) or identity["wheel_tag"] not in wheel_tags:
        return fail(
            f"pyboy identity WHEEL tag expected={identity['wheel_tag']} actual={wheel_tags}"
        )
    modules = pyboy.get("modules", {})
    if not isinstance(modules, dict):
        return fail(f"pyboy identity modules are malformed actual={modules!r}")
    for name in expected_modules:
        module = modules.get(name)
        if not isinstance(module, dict):
            return fail(f"pyboy identity module={name} is missing")
        path = module.get("path", "")
        if not module.get("compiled") or not isinstance(path, str) or not CP312_EXTENSION.search(path):
            return fail(f"pyboy identity module={name} is not a cp312 extension actual={path}")
    print(
        f"ARTIFACT pyboy identity python={python['version']} "
        f"version={pyboy['version']} wheel={identity['wheel_tag']}"
    )
    return 0


def fail(message: str) -> int:
    print(f"ARTIFACT {message}", file=sys.stderr)
    return 2


def verify_pret(root: Path, manifest: dict, commit_only: bool = False) -> int:
    checkout = root / "poketcg"
    if not checkout.is_dir():
        return fail(f"missing checkout {checkout}")
    try:
        expected_commit = manifest["pret"]["commit"]
    except (KeyError, TypeError) as error:
        return fail(f"pret manifest invalid: {error}")
    actual_commit = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    if not actual_commit.startswith(expected_commit):
        return fail(f"pret commit expected={expected_commit} actual={actual_commit}")
    if commit_only:
        print(f"ARTIFACT pret commit={actual_commit}")
        return 0
    rom = checkout / "poketcg.gbc"
    if not rom.is_file():
        return fail(f"missing ROM {rom}")
    try:
        expected_rom = manifest["pret"]["rom_sha1"]
    except (KeyError, TypeError) as error:
        return fail(f"pret manifest invalid: {error}")
    actual_rom = digest(rom, "sha1")
    if actual_rom != expected_rom:
        return fail(f"ROM sha1 expected={expected_rom} actual={actual_rom}")
    print(f"ARTIFACT pret commit={actual_commit} rom_sha1={actual_rom}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--commit-only", action="store_true")
    parser.add_argument("--pyboy-identity", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads((args.root / "tools/oracle/artifacts.json").read_text())
        if not isinstance(manifest, dict):
            raise TypeError("manifest must be an object")
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as error:
        return fail(f"manifest invalid: {error}")
    if args.pyboy_identity:
        return verify_pyboy_identity(args.root, manifest)
    return verify_pret(args.root, manifest, args.commit_only)

if __name__ == "__main__":
    raise SystemExit(main())
