#!/usr/bin/env python3
"""Decompress pret .lz assets into a reproducible C header."""

from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

HEX_RE = re.compile(r"0x([0-9a-fA-F]{2})")
ARRAY_RE = re.compile(r"static const uint8_t (\w+)\[\] = \{(.*?)\};", re.DOTALL)


@dataclass(frozen=True)
class Blob:
    path: str
    compressed_name: str
    decompressed_name: str
    compressed: bytes
    decompressed: bytes
    compressed_sha256: str
    decompressed_sha256: str


def decompress(source: bytes) -> bytes:
    buffer = bytearray(0x100)
    source_pos = 0
    buffer_pos = 0xEF
    length_byte = 0
    repeat_toggle = False
    output = bytearray()
    while source_pos < len(source):
        command = source[source_pos]
        source_pos += 1
        for bit in range(8):
            if source_pos >= len(source):
                break
            if command & (1 << (7 - bit)):
                value = source[source_pos]
                source_pos += 1
                output.append(value)
                buffer[buffer_pos] = value
                buffer_pos = (buffer_pos + 1) & 0xFF
                continue
            repeat_toggle = not repeat_toggle
            if source_pos >= len(source):
                raise ValueError("repeat command missing offset")
            offset = source[source_pos]
            if repeat_toggle:
                if source_pos + 1 >= len(source):
                    raise ValueError("repeat command missing length")
                length_byte = source[source_pos + 1]
                source_pos += 2
            else:
                source_pos += 1
            count = ((length_byte >> 4) if repeat_toggle else (length_byte & 0x0F)) + 2
            for _ in range(count):
                value = buffer[offset]
                offset = (offset + 1) & 0xFF
                output.append(value)
                buffer[buffer_pos] = value
                buffer_pos = (buffer_pos + 1) & 0xFF
    return bytes(output)


def discover(root: Path) -> list[Blob]:
    blobs: list[Blob] = []
    for path in sorted(root.rglob("*.lz")):
        rel = path.relative_to(root).as_posix()
        compressed = path.read_bytes()
        decompressed = decompress(compressed)
        stem = re.sub(r"[^A-Za-z0-9_]", "_", rel)
        if stem[:1].isdigit():
            stem = "_" + stem
        suffix = hashlib.sha256(rel.encode()).hexdigest()[:8]
        c_name = f"poketcg_lz_compressed_{stem}_{suffix}"
        d_name = f"poketcg_lz_decompressed_{stem}_{suffix}"
        blobs.append(
            Blob(
                rel,
                c_name,
                d_name,
                compressed,
                decompressed,
                hashlib.sha256(compressed).hexdigest(),
                hashlib.sha256(decompressed).hexdigest(),
            )
        )
    return blobs


def c_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def emit_bytes(data: bytes) -> list[str]:
    return ["    " + ", ".join(f"0x{byte:02x}" for byte in data[i : i + 16]) + "," for i in range(0, len(data), 16)]


def render(blobs: list[Blob], source: str) -> str:
    out = [
        f"/* Generated from {source} by tools/gen_lz.py. Do not edit. */",
        "#ifndef POKETCG_GENERATED_LZ_H",
        "#define POKETCG_GENERATED_LZ_H",
        "",
        "#include <stddef.h>",
        "#include <stdint.h>",
        "",
    ]
    for blob in blobs:
        out.append(
            f"/* POKETCG_LZ path={blob.path} compressed={len(blob.compressed)} "
            f"decompressed={len(blob.decompressed)} "
            f"compressed_sha256={blob.compressed_sha256} "
            f"decompressed_sha256={blob.decompressed_sha256} */"
        )
        out.append(f"static const uint8_t {blob.compressed_name}[] = {{")
        out.extend(emit_bytes(blob.compressed))
        out.append("};")
        out.append(f"static const uint8_t {blob.decompressed_name}[] = {{")
        out.extend(emit_bytes(blob.decompressed))
        out.extend(["};", ""])
    out.extend(
        [
            "typedef struct {",
            "    const char *path;",
            "    size_t compressed_size;",
            "    size_t decompressed_size;",
            "    const char *compressed_sha256;",
            "    const char *decompressed_sha256;",
            "    const uint8_t *compressed;",
            "    const uint8_t *decompressed;",
            "} PoketcgLzBlob;",
            "",
            f"#define POKETCG_LZ_COUNT {len(blobs)}u",
            "static const PoketcgLzBlob poketcg_lz_blobs[] = {",
        ]
    )
    for blob in blobs:
        out.append(
            f"    {{{c_string(blob.path)}, {len(blob.compressed)}u, {len(blob.decompressed)}u, "
            f"{c_string(blob.compressed_sha256)}, {c_string(blob.decompressed_sha256)}, "
            f"{blob.compressed_name}, {blob.decompressed_name}}},"
        )
    out.extend(["};", "", "#endif", ""])
    return "\n".join(out)


def parse_header(text: str) -> dict[str, bytes]:
    return {name: bytes(int(value, 16) for value in HEX_RE.findall(body)) for name, body in ARRAY_RE.findall(text)}


def verify_text(text: str, blobs: list[Blob]) -> tuple[int, int, int]:
    arrays = parse_header(text)
    compressed_total = 0
    decompressed_total = 0
    for blob in blobs:
        if arrays.get(blob.compressed_name) != blob.compressed:
            raise ValueError(f"compressed {blob.path}: generated bytes differ")
        if arrays.get(blob.decompressed_name) != blob.decompressed:
            raise ValueError(f"decompressed {blob.path}: generated bytes differ")
        compressed_total += len(blob.compressed)
        decompressed_total += len(blob.decompressed)
    if len(arrays) != len(blobs) * 2:
        raise ValueError(f"generated array count {len(arrays)} != expected {len(blobs) * 2}")
    return len(blobs), compressed_total, decompressed_total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disasm", type=Path, default=Path("poketcg"))
    parser.add_argument("--out", type=Path, default=Path("include/generated/lz.h"))
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.verify and args.check:
        parser.error("--verify and --check are mutually exclusive")
    blobs = discover(args.disasm)
    if not blobs:
        raise SystemExit(f"no .lz inputs found under {args.disasm}")
    if args.check:
        if not args.out.exists():
            raise SystemExit(f"missing generated output: {args.out}")
        count, compressed_total, decompressed_total = verify_text(args.out.read_text(), blobs)
        print(f"gen_lz: checked {args.out} -- {count} blobs, {compressed_total} compressed bytes, {decompressed_total} decompressed bytes")
        return 0
    rendered = render(blobs, str(args.disasm))
    if args.verify:
        count, compressed_total, decompressed_total = verify_text(rendered, blobs)
        altered = list(blobs)
        first = blobs[0]
        corrupt = bytearray(first.decompressed)
        corrupt[0] ^= 0xFF
        altered[0] = Blob(first.path, first.compressed_name, first.decompressed_name, first.compressed, bytes(corrupt), first.compressed_sha256, first.decompressed_sha256)
        try:
            verify_text(render(altered, str(args.disasm)), blobs)
        except ValueError:
            pass
        else:
            raise SystemExit("gen_lz: negative-control perturbation was not detected")
        print(f"gen_lz: verified {count} blobs, {compressed_total} compressed bytes, {decompressed_total} decompressed bytes")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(rendered)
    print(f"gen_lz: wrote {args.out} ({len(blobs)} blobs)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        raise SystemExit(f"gen_lz: error: {exc}")
