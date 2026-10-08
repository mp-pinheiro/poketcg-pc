#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from profiles import Profile, ProfileError, get_profile

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


def tool_version(tool: str, required: str) -> str:
    path = shutil.which(tool)
    if path is None:
        raise SystemExit(f"missing RGBDS tool {tool}; install RGBDS {required}")
    result = subprocess.run([path, "--version"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    first = result.stdout.splitlines()[0] if result.stdout.splitlines() else ""
    expected = f"{tool} v{required}"
    if not first.startswith(expected):
        raise SystemExit(f"{tool} version mismatch: expected {expected}, got {first}")
    return path


def apply_patch(root: Path, profile: Profile, checkout: Path) -> bool:
    patch = root / "profiles" / profile.name / "source-fixes.patch"
    if not patch.is_file():
        return False
    check = subprocess.run(["git", "-C", str(checkout), "apply", "--check", str(patch)],
                           text=True, capture_output=True, check=False)
    if check.returncode == 0:
        run(root, "git", "-C", str(checkout), "apply", str(patch))
        return True
    reverse = subprocess.run(["git", "-C", str(checkout), "apply", "--reverse", "--check", str(patch)],
                             text=True, capture_output=True, check=False)
    if reverse.returncode != 0:
        raise SystemExit(f"cannot apply the {profile.title} source fix: {check.stderr.strip()}")
    return True


def ensure_checkout(root: Path, profile: Profile) -> Path:
    checkout = profile.source_path(root)
    if not checkout.exists():
        run(root, "git", "clone", profile.source_repository, str(checkout))
    if not (checkout / ".git").exists():
        raise SystemExit(f"{profile.title} checkout is not a git repository: {checkout}")
    run(root, "git", "-C", str(checkout), "fetch", "--all", "--tags")
    run(root, "git", "-C", str(checkout), "checkout", "--detach", profile.source_commit)
    run(root, "git", "-C", str(checkout), "checkout", "--", "src")
    actual = run(root, "git", "-C", str(checkout), "rev-parse", "HEAD")
    if actual != profile.source_commit:
        raise SystemExit(f"{profile.title} checkout mismatch: expected {profile.source_commit}, got {actual}")
    return checkout


def build_once(root: Path, profile: Profile, checkout: Path, debug: bool) -> Path:
    required = profile.source.get("rgbds_version")
    if not isinstance(required, str) or not required:
        raise SystemExit(f"profile {profile.name} pins no source.rgbds_version")
    run(root, "make", "-C", str(checkout), "clean")
    rgbds_dir = str(Path(tool_version("rgbasm", required)).parent) + "/"
    for tool in RGBDS_TOOLS[1:]:
        tool_version(tool, required)
    command = ["make", "-C", str(checkout), f"RGBDS={rgbds_dir}"]
    if debug:
        command.insert(3, "DEBUG=1")
    subprocess.run(command, cwd=root, check=True)
    rom = profile.rom_path(root)
    if not rom.is_file():
        raise SystemExit(f"{profile.title} build did not produce {rom}")
    if debug:
        for path in (profile.map_path(root), profile.sym_path(root)):
            if not path.is_file():
                raise SystemExit(f"{profile.title} build did not produce {path}")
    return rom


def record_hash(root: Path, profile: Profile, value: str) -> None:
    catalog_path = root / "profiles" / "profiles.json"
    document = json.loads(catalog_path.read_text())
    artifacts = document["profiles"][profile.name]["artifacts"]
    current = artifacts.get("rom_sha256")
    if current not in (None, value):
        raise SystemExit(f"catalog ROM hash mismatch: recorded {current}, built {value}")
    artifacts["rom_sha256"] = value
    catalog_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and verify a profile's pinned ROM.")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        profile = get_profile(args.profile, root)
    except ProfileError as error:
        raise SystemExit(str(error)) from error
    checkout = ensure_checkout(root, profile)
    pristine = digest(build_once(root, profile, checkout, debug=False))
    patched = apply_patch(root, profile, checkout)
    first = digest(build_once(root, profile, checkout, debug=True))
    if patched and first != pristine:
        raise SystemExit(f"{profile.title} source fix changed the ROM: pristine {pristine} != patched {first}")
    second = digest(build_once(root, profile, checkout, debug=True))
    if first != second:
        raise SystemExit(f"{profile.title} build is not reproducible: {first} != {second}")
    record_hash(root, profile, first)
    actual = digest(profile.rom_path(root))
    if actual != first:
        raise SystemExit(f"{profile.title} ROM changed after recording: {first} != {actual}")
    print(f"bootstrap-profile: profile={profile.name} commit={profile.source_commit} rom_sha256={actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
