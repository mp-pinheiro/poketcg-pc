#!/usr/bin/env python3
"""Emit reproducibility identities for the installed oracle backend."""

from __future__ import annotations

import hashlib
import importlib
import importlib.metadata
import json
import platform
import sys
import sysconfig
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    modules = {}
    for name in ("pyboy", "pyboy.core.cpu", "pyboy.core.opcodes", "pyboy.core.mb"):
        module = importlib.import_module(name)
        path = getattr(module, "__file__", None)
        if path:
            resolved = Path(path).resolve()
            modules[name] = {"path": str(resolved), "sha256": sha256(resolved)}
    lock = ROOT / "tools/oracle/uv.lock"
    distribution = importlib.metadata.distribution("pyboy")
    record = next(
        (distribution.locate_file(path) for path in (distribution.files or []) if path.name == "RECORD"),
        None,
    )
    result = {
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "soabi": sysconfig.get_config_var("SOABI"),
            "platform": platform.platform(),
        },
        "pyboy": {
            "version": distribution.version,
            "distribution_record": str(record) if record else None,
            "modules": modules,
        },
        "uv_lock_sha256": sha256(lock),
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
