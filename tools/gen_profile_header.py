#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.profiles import get_profile, load_catalog

PROFILE_FEATURES = ("card_pop", "gift_center", "link_duel", "multi_bank_scripts", "nine_bit_card_ids", "printer", "three_palette_cards")

def render(name: str) -> str:
    _, profiles = load_catalog(ROOT / "profiles" / "profiles.json")
    profile = get_profile(name, ROOT)
    index = list(profiles).index(profile.name)
    lines = [
        "#ifndef POKETCG_GENERATED_PROFILE_FEATURES_H",
        "#define POKETCG_GENERATED_PROFILE_FEATURES_H",
        "",
        f"#define PROFILE_INDEX {index}u",
        f'#define PROFILE_SAVE_TAG "{profile.save_tag}"',
        f"#define PROFILE_SAVE_SCHEMA {profile.save_schema}u",
        f"#define PROFILE_CARD_ID_TYPE {'uint16_t' if profile.features.get('nine_bit_card_ids', False) else 'uint8_t'}",
    ]
    for feature in sorted(set(PROFILE_FEATURES) | set(profile.features)):
        enabled = profile.features.get(feature, False)
        macro = "PROFILE_FEATURE_" + re.sub(r"[^A-Za-z0-9]", "_", feature).upper()
        lines.append(f"#define {macro} {1 if enabled else 0}")
    lines += ["", "#endif", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit generated/profile_features.h from profiles/profiles.json.")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    target = args.out / "profile_features.h"
    text = render(args.profile)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_file() or target.read_text() != text:
        target.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
