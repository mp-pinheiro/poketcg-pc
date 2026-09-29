#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINUXDEPLOY_URL = "https://github.com/linuxdeploy/linuxdeploy/releases/download/1-alpha-20251107-1/linuxdeploy-x86_64.AppImage"
LINUXDEPLOY_SHA256 = "c20cd71e3a4e3b80c3483cef793cda3f4e990aca14014d23c544ca3ce1270b4d"


def build_root() -> Path:
    return ROOT / os.environ.get("POKETCG_BUILD", "build-profiles")


def copy_product(stage: Path) -> None:
    binary_root = build_root()
    files = {
        "poketcg": binary_root / "poketcg",
        "poketcg-extended": binary_root / "poketcg-extended",
        "poketcg-launcher": binary_root / "poketcg-launcher",
        "data-pack.bin": binary_root / "completion" / "data-pack.bin",
        "data-pack-extended.bin": ROOT / "build-extended" / "completion" / "data-pack.bin",
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
        if path.is_file() and path.suffix.lower() in FORBIDDEN:
            raise SystemExit(f"profile package contains forbidden file: {path}")


def appimage(output: Path) -> Path:
    appdir = output / "AppDir"
    stage = appdir / "usr" / "bin"
    shutil.rmtree(appdir, ignore_errors=True)
    output.mkdir(parents=True, exist_ok=True)
    copy_product(stage)
    verify_stage(appdir)
    tool = output / "tools" / "linuxdeploy-x86_64.AppImage"
    tool.parent.mkdir(parents=True, exist_ok=True)
    if not tool.is_file():
        subprocess.run(["curl", "-fsSL", "-o", str(tool), LINUXDEPLOY_URL], check=True)
        subprocess.run(["sha256sum", "-c"], input=f"{LINUXDEPLOY_SHA256}  {tool}\n", text=True, check=True)
        tool.chmod(0o755)
    version = (ROOT / "VERSION").read_text().strip()
    result = output / f"poketcg-profiles-{version}-x86_64.AppImage"
    if result.exists():
        result.unlink()
    subprocess.run([
        str(tool), "--appdir", str(appdir), "--executable", str(stage / "poketcg-launcher"),
        "--desktop-file", str(ROOT / "tools/appimage/poketcg.desktop"),
        "--icon-file", str(ROOT / "tools/appimage/poketcg.png"),
        "--custom-apprun", str(ROOT / "tools/appimage/AppRun"), "--output", "appimage",
    ], cwd=output, env={**os.environ, "APPIMAGE_EXTRACT_AND_RUN": "1", "LDAI_OUTPUT": str(result), "LDAI_NO_APPSTREAM": "1"}, check=True)
    verify_stage(appdir)
    return result


def windows(output: Path) -> Path:
    stage = output / "poketcg-profiles"
    shutil.rmtree(stage, ignore_errors=True)
    output.mkdir(parents=True, exist_ok=True)
    copy_product(stage)
    verify_stage(stage)
    version = (ROOT / "VERSION").read_text().strip()
    archive = output / f"poketcg-profiles-{version}-windows.zip"
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
    args = parser.parse_args()
    output = (args.output or ROOT / "build" / f"{args.format}-profiles").resolve()
    result = appimage(output) if args.format == "appimage" else windows(output)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
