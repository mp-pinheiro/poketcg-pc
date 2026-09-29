#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from profiles import ProfileError, get_profile

REQUIRED_RGBDS = "1.0.0"
RGBDS_TOOLS = ("rgbasm", "rgbfix", "rgbgfx", "rgblink")


def run(root: Path, *command: str) -> str:
    result = subprocess.run(command, cwd=root, check=True, text=True, stdout=subprocess.PIPE)
    return result.stdout.strip()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tool_version(tool: str) -> str:
    path = shutil.which(tool)
    if path is None:
        raise SystemExit(f"missing RGBDS tool {tool}; install RGBDS {REQUIRED_RGBDS}")
    result = subprocess.run([path, "--version"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    first = result.stdout.splitlines()[0] if result.stdout.splitlines() else ""
    expected = f"{tool} v{REQUIRED_RGBDS}"
    if not first.startswith(expected):
        raise SystemExit(f"{tool} version mismatch: expected {expected}, got {first}")
    return path


def apply_patch(root: Path, checkout: Path) -> None:
    patch = root / "profiles" / "extended" / "source-fixes.patch"
    check = subprocess.run(
        ["git", "-C", str(checkout), "apply", "--check", str(patch)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check.returncode == 0:
        run(root, "git", "-C", str(checkout), "apply", str(patch))
        return
    reverse = subprocess.run(
        ["git", "-C", str(checkout), "apply", "--reverse", "--check", str(patch)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if reverse.returncode != 0:
        raise SystemExit(f"cannot apply Extended source fix: {check.stderr.strip()}")


def ensure_checkout(root: Path, profile) -> Path:
    checkout = profile.source_path(root)
    if not checkout.exists():
        run(root, "git", "clone", profile.source_repository, str(checkout))
    if not (checkout / ".git").exists():
        raise SystemExit(f"Extended checkout is not a git repository: {checkout}")
    run(root, "git", "-C", str(checkout), "fetch", "--all", "--tags")
    run(root, "git", "-C", str(checkout), "checkout", "--detach", profile.source_commit)
    run(root, "git", "-C", str(checkout), "checkout", "--", "src")
    actual = run(root, "git", "-C", str(checkout), "rev-parse", "HEAD")
    if actual != profile.source_commit:
        raise SystemExit(f"Extended checkout mismatch: expected {profile.source_commit}, got {actual}")
    return checkout


def build_once(root: Path, checkout: Path, debug: bool) -> Path:
    run(root, "make", "-C", str(checkout), "clean")
    rgbds_dir = str(Path(tool_version("rgbasm")).parent) + "/"
    for tool in RGBDS_TOOLS[1:]:
        tool_version(tool)
    command = ["make", "-C", str(checkout), f"RGBDS={rgbds_dir}"]
    if debug:
        command.insert(3, "DEBUG=1")
    subprocess.run(command, cwd=root, check=True)
    profile = get_profile("extended", root)
    rom = profile.rom_path(root)
    if not rom.is_file():
        raise SystemExit(f"Extended build did not produce {rom}")
    if debug:
        for path in (profile.map_path(root), profile.sym_path(root)):
            if not path.is_file():
                raise SystemExit(f"Extended build did not produce {path}")
    return rom


def record_hash(root: Path, value: str) -> None:
    catalog_path = root / "profiles" / "profiles.json"
    document = json.loads(catalog_path.read_text())
    current = document["profiles"]["extended"]["artifacts"].get("rom_sha256")
    if current not in (None, value):
        raise SystemExit(f"catalog ROM hash mismatch: recorded {current}, built {value}")
    document["profiles"]["extended"]["artifacts"]["rom_sha256"] = value
    catalog_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        profile = get_profile("extended", root)
    except ProfileError as error:
        raise SystemExit(str(error)) from error
    checkout = ensure_checkout(root, profile)
    pristine = digest(build_once(root, checkout, debug=False))
    apply_patch(root, checkout)
    first = digest(build_once(root, checkout, debug=True))
    if first != pristine:
        raise SystemExit(f"Extended source fix changed the ROM: pristine {pristine} != patched {first}")
    second = digest(build_once(root, checkout, debug=True))
    if first != second:
        raise SystemExit(f"Extended build is not reproducible: {first} != {second}")
    record_hash(root, first)
    actual = digest(profile.rom_path(root))
    if actual != first:
        raise SystemExit(f"Extended ROM changed after recording: {first} != {actual}")
    print(f"bootstrap-extended: commit={profile.source_commit} rom_sha256={actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
