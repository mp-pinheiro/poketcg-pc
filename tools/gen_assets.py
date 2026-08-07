#!/usr/bin/env python3
"""Extract built pret graphics assets into a reproducible C header."""

from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

EXTENSIONS = (".1bpp", ".2bpp", ".pal", ".dimensions")
HEX_RE = re.compile(r"0x([0-9a-fA-F]{2})")
MANIFEST_RE = re.compile(
    r"^/\* POKETCG_ASSET path=(\S+) name=(\w+) size=(\d+) sha256=([0-9a-f]{64}) \*/$"
)
ARRAY_RE = re.compile(
    r"static const uint8_t (\w+)\[\] = \{(.*?)\};", re.DOTALL
)


@dataclass(frozen=True)
class Asset:
    path: str
    name: str
    data: bytes
    kind: str
    digest: str


def discover(root: Path) -> list[Asset]:
    paths = sorted(
        p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONS
    )
    assets: list[Asset] = []
    for path in paths:
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        stem = re.sub(r"[^A-Za-z0-9_]", "_", rel)
        if stem[:1].isdigit():
            stem = "_" + stem
        name = f"poketcg_asset_{stem}_{hashlib.sha256(rel.encode()).hexdigest()[:8]}"
        assets.append(Asset(rel, name, data, path.suffix[1:], digest))
    return assets


def c_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render(assets: list[Asset], source: str) -> str:
    out = [
        f"/* Generated from {source} by tools/gen_assets.py. Do not edit. */",
        "#ifndef POKETCG_GENERATED_ASSETS_H",
        "#define POKETCG_GENERATED_ASSETS_H",
        "",
        "#include <stddef.h>",
        "#include <stdint.h>",
        "",
    ]
    for asset in assets:
        out.append(
            f"/* POKETCG_ASSET path={asset.path} name={asset.name} "
            f"size={len(asset.data)} sha256={asset.digest} */"
        )
        out.append(f"static const uint8_t {asset.name}[] = {{")
        for offset in range(0, len(asset.data), 16):
            chunk = asset.data[offset : offset + 16]
            out.append("    " + ", ".join(f"0x{byte:02x}" for byte in chunk) + ",")
        out.append("};")
        out.append("")
    out.extend(
        [
            "typedef struct {",
            "    const char *path;",
            "    const char *kind;",
            "    size_t size;",
            "    const char *sha256;",
            "    const uint8_t *data;",
            "} PoketcgAsset;",
            "",
            f"#define POKETCG_ASSET_COUNT {len(assets)}u",
            "static const PoketcgAsset poketcg_assets[] = {",
        ]
    )
    for asset in assets:
        out.append(
            f"    {{{c_string(asset.path)}, {c_string(asset.kind)}, {len(asset.data)}u, "
            f"{c_string(asset.digest)}, {asset.name}}},"
        )
    out.extend(["};", "", "#endif", ""])
    return "\n".join(out)


def parse_header(text: str) -> dict[str, bytes]:
    arrays: dict[str, bytes] = {}
    for match in ARRAY_RE.finditer(text):
        arrays[match.group(1)] = bytes(int(value, 16) for value in HEX_RE.findall(match.group(2)))
    return arrays


def verify_text(text: str, assets: list[Asset]) -> tuple[int, int]:
    arrays = parse_header(text)
    total = 0
    for asset in assets:
        if arrays.get(asset.name) != asset.data:
            got = arrays.get(asset.name)
            offset = next(
                (i for i, (want, actual) in enumerate(zip(asset.data, got or b"")) if want != actual),
                min(len(asset.data), len(got or b"")),
            )
            raise ValueError(f"asset {asset.path}: first differing offset 0x{offset:x}")
        total += len(asset.data)
    if len(arrays) != len(assets):
        raise ValueError(f"generated asset count {len(arrays)} != expected {len(assets)}")
    return len(assets), total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disasm", type=Path, default=Path("poketcg"))
    parser.add_argument("--out", type=Path, default=Path("include/generated/assets.h"))
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.verify and args.check:
        parser.error("--verify and --check are mutually exclusive")
    assets = discover(args.disasm)
    if not assets:
        raise SystemExit(f"no built assets found under {args.disasm}")
    if args.check:
        if not args.out.exists():
            raise SystemExit(f"missing generated output: {args.out}")
        count, total = verify_text(args.out.read_text(), assets)
        print(f"gen_assets: checked {args.out} -- {count} assets, {total} bytes")
        return 0
    rendered = render(assets, str(args.disasm))
    if args.verify:
        count, total = verify_text(rendered, assets)
        corrupted = bytearray(assets[0].data)
        corrupted[0] ^= 0xFF
        altered = list(assets)
        altered[0] = Asset(assets[0].path, assets[0].name, bytes(corrupted), assets[0].kind, assets[0].digest)
        try:
            verify_text(render( altered, str(args.disasm)), assets)
        except ValueError:
            pass
        else:
            raise SystemExit("gen_assets: negative-control perturbation was not detected")
        print(f"gen_assets: verified {count} assets, {total} bytes")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(rendered)
    print(f"gen_assets: wrote {args.out} ({len(assets)} assets)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        raise SystemExit(f"gen_assets: error: {exc}")
