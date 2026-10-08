#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
from pathlib import Path

from profiles import load_catalog

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("profiles", "default", "source", "rom", "map", "sym", "binary", "probe", "pack",
                                         "inventory", "removed-basenames", "overlay-root"))
    parser.add_argument("--profile")
    args = parser.parse_args()
    default, profiles = load_catalog(ROOT / "profiles" / "profiles.json")
    if args.kind == "profiles":
        print(";".join(profiles))
        return 0
    if args.kind == "default":
        print(default)
        return 0
    profile = profiles[args.profile or os.environ.get("POKETCG_PROFILE") or default]
    if args.kind == "removed-basenames":
        print(";".join(sorted(profile.removed_basenames)))
        return 0
    if args.kind == "overlay-root":
        print(profile.overlay_root or "")
        return 0
    paths = {
        "source": profile.source_path(ROOT),
        "rom": profile.rom_path(ROOT),
        "map": profile.map_path(ROOT),
        "sym": profile.sym_path(ROOT),
        "binary": profile.binary_path(ROOT),
        "probe": profile.probe_path(ROOT),
        "pack": profile.data_pack_path(ROOT),
        "inventory": profile.artifact_path("inventory", ROOT),
    }
    print(paths[args.kind])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
