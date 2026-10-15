#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.completion.package_smoke import FORBIDDEN_SUFFIXES
from tools.profiles import get_profile


def build_root() -> Path:
    return get_profile(root=ROOT).build_path(ROOT)


def copy_product(stage: Path) -> None:
    binary_root = build_root()
    files = {
        "poketcg": binary_root / "poketcg",
        "poketcg-extended": binary_root / "poketcg-extended",
        "poketcg-launcher": binary_root / "poketcg-launcher",
        "data-pack.bin": binary_root / "completion" / "data-pack.bin",
        "data-pack-extended.bin": binary_root / "completion" / "data-pack-extended.bin",
    }
    stage.mkdir(parents=True, exist_ok=True)
    for name, source in files.items():
        if not source.is_file():
            raise SystemExit(f"missing profile package input: {source}")
        shutil.copy2(source, stage / name)
    (stage / "NOTICE-EXTENDED.txt").write_text(
        (ROOT / "profiles" / "extended" / "provenance.toml").read_text()
    )
    for source in sorted((ROOT / "third_party" / "fonts").glob("*LICENSE*.txt")):
        shutil.copy2(source, stage / source.name)


def verify_stage(stage: Path) -> None:
    for path in stage.rglob("*"):
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            raise SystemExit(f"profile package contains forbidden file: {path}")


def appimage(output: Path, name: str) -> Path:
    appdir = output / "AppDir"
    stage = appdir / "usr" / "bin"
    shutil.rmtree(appdir, ignore_errors=True)
    output.mkdir(parents=True, exist_ok=True)
    copy_product(stage)
    verify_stage(appdir)
    result = output / f"{name}.AppImage"
    if result.exists():
        result.unlink()
    subprocess.run(
        [str(ROOT / "tools/appimage/build.sh"), "--profiles", str(appdir), str(output), name],
        cwd=ROOT, check=True,
    )
    verify_stage(appdir)
    return result


def windows(output: Path, name: str) -> Path:
    stage = output / name
    shutil.rmtree(stage, ignore_errors=True)
    output.mkdir(parents=True, exist_ok=True)
    vanilla = get_profile("vanilla", ROOT).data_pack_path(ROOT)
    extended = get_profile("extended", ROOT).data_pack_path(ROOT)
    subprocess.run(
        [str(ROOT / "tools/windows/build.sh"), "--profiles", str(vanilla), str(extended), str(stage)],
        cwd=ROOT, check=True,
    )
    shutil.copy2(ROOT / "profiles/extended/provenance.toml", stage / "NOTICE-EXTENDED.txt")
    verify_stage(stage)
    archive = output / f"{name}.zip"
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in stage.rglob("*"):
            bundle.write(path, path.relative_to(output))
    return archive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("appimage", "windows"), required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--private", action="store_true", help="mark artifact filenames as private")
    args = parser.parse_args()
    output = (args.output or build_root() / f"{args.format}-profiles").resolve()
    version = (ROOT / "VERSION").read_text().strip()
    purpose = "-private" if args.private else ""
    platform = "x86_64" if args.format == "appimage" else "windows"
    name = f"poketcg-profiles-{version}{purpose}-{platform}"
    result = appimage(output, name) if args.format == "appimage" else windows(output, name)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
