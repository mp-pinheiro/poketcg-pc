#!/usr/bin/env python3
"""Emit reproducibility identities for the installed oracle backend."""

from __future__ import annotations

import hashlib
import importlib
import importlib.metadata
import json
import platform
import re
import sysconfig
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ESSENTIAL_MODULES = ("pyboy", "pyboy.core.cpu", "pyboy.core.opcodes", "pyboy.core.mb")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect() -> dict:
    modules = {}
    for name in ESSENTIAL_MODULES:
        module = importlib.import_module(name)
        path = getattr(module, "__file__", None)
        if path:
            resolved = Path(path).resolve()
            modules[name] = {
                "path": str(resolved),
                "sha256": sha256(resolved),
                "compiled": resolved.suffix in {".so", ".pyd", ".dylib"},
                "extension_suffix": resolved.suffix,
            }
    lock = ROOT / "tools/oracle/uv.lock"
    distribution = importlib.metadata.distribution("pyboy")
    distribution_files = {}
    record = None
    wheel = None
    wheel_tags = []
    for relative in distribution.files or ():
        candidate = distribution.locate_file(relative)
        if not candidate.is_file():
            continue
        if relative.name in {"RECORD", "WHEEL"}:
            digest = sha256(candidate)
            if relative.name == "RECORD":
                record = {"path": str(candidate.resolve()), "sha256": digest}
            else:
                wheel = {"path": str(candidate.resolve()), "sha256": digest}
                wheel_tags = [
                    line.split(":", 1)[1].strip()
                    for line in candidate.read_text().splitlines()
                    if line.startswith("Tag:")
                ]
        if relative.parts and relative.parts[0] == "pyboy" and candidate.suffix in {".py", ".so", ".pyd", ".dylib", ".pyc"}:
            distribution_files[str(relative)] = {
                "path": str(candidate.resolve()),
                "sha256": sha256(candidate),
            }
    soabi = sysconfig.get_config_var("SOABI") or ""
    soabi_match = re.match(r"(?P<family>cpython-\d+)", soabi)
    result = {
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "soabi": soabi,
            "soabi_family": soabi_match.group("family") if soabi_match else soabi,
            "platform": platform.platform(),
        },
        "pyboy": {
            "version": distribution.version,
            "distribution_record": record,
            "wheel": wheel,
            "wheel_tags": wheel_tags,
            "modules": modules,
            "distribution_files": distribution_files,
        },
        "uv_lock_sha256": sha256(lock),
    }
    return result


def main() -> None:
    print(json.dumps(collect(), sort_keys=True, indent=2))

if __name__ == "__main__":
    main()

