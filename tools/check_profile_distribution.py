#!/usr/bin/env python3

from __future__ import annotations

import argparse
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROVENANCE = ROOT / "profiles" / "extended" / "provenance.toml"
BLOCKED_MESSAGE = "Extended packaging blocked: no recorded distribution permission"


def check(path: Path) -> None:
    try:
        document = tomllib.loads(path.read_text())
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise SystemExit(f"cannot read Extended provenance: {error}") from error
    if document.get("distribution") != "allowed" or not document.get("permission_evidence"):
        raise SystemExit(BLOCKED_MESSAGE)
    evidence = document["permission_evidence"]
    if not isinstance(evidence, list) or any(not isinstance(item, str) or not item.strip() for item in evidence):
        raise SystemExit("Extended packaging blocked: permission evidence is malformed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provenance", type=Path, default=PROVENANCE)
    args = parser.parse_args()
    check(args.provenance.resolve())
    print("Extended packaging permission recorded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
