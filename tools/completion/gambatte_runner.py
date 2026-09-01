#!/usr/bin/env python3
"""Build and run the pinned headless Gambatte reference lane."""

from __future__ import annotations

import argparse
import binascii
import ctypes
import hashlib
import json
import os
import shutil
import struct
import subprocess
import tarfile
import tempfile
import urllib.error
import urllib.request
import zlib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PINS_PATH = ROOT / "tools" / "completion" / "gambatte_pins.toml"
BUILD_ROOT = ROOT / "build" / "completion" / "gambatte"
SOURCE_ROOT = BUILD_ROOT / "source"
WIDTH = 160
HEIGHT = 144
SAMPLES_PER_FRAME = 35112
MAX_SLICES_PER_FRAME = 240
AREA_IDS = {
    "VRAM": 0,
    "ROM": 1,
    "WRAM": 2,
    "CartRAM": 3,
    "OAM": 4,
    "HRAM": 5,
    "BG Palette RGB": 6,
    "OBJ Palette RGB": 7,
}
REQUIRED_DOMAIN_NAMES = (
    "WRAM",
    "ROM",
    "VRAM",
    "VRAM Bank 0",
    "VRAM Bank 1",
    "OAM",
    "HRAM",
    "CartRAM",
    "System Bus",
    "BG Palette RGB",
    "OBJ Palette RGB",
)
EXPECTED_DOMAIN_LENGTHS = {
    "VRAM": 0x4000,
    "VRAM Bank 0": 0x2000,
    "VRAM Bank 1": 0x2000,
    "WRAM": 0x8000,
    "CartRAM": 0x8000,
    "OAM": 0xA0,
    "HRAM": 0x7F,
    "System Bus": 0x10000,
    "BG Palette RGB": 32 * 4,
    "OBJ Palette RGB": 32 * 4,
}
REGISTER_INDICES = {
    "PC": 0,
    "SP": 1,
    "A": 2,
    "B": 3,
    "C": 4,
    "D": 5,
    "E": 6,
    "F": 7,
    "H": 8,
    "L": 9,
}
REQUIRED_REGISTERS = ("A", "F", "B", "C", "D", "E", "H", "L", "SP", "PC")
REQUIRED_SYMBOLS = (
    "gambatte_create",
    "gambatte_destroy",
    "gambatte_loadbuf",
    "gambatte_runfor",
    "gambatte_setinputgetter",
    "gambatte_setexeccallback",
    "gambatte_setcgbpalette",
    "gambatte_settimemode",
    "gambatte_settime",
    "gambatte_getmemoryarea",
    "gambatte_cpuread",
    "gambatte_getregs",
)


class GambatteError(RuntimeError):
    pass


def load_pins() -> dict[str, Any]:
    import tomllib

    try:
        with PINS_PATH.open("rb") as stream:
            pins = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise GambatteError(f"cannot load pins: {exc}") from exc
    if pins.get("schema") != 1:
        raise GambatteError("Gambatte pin schema is not 1")
    return pins


def resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def digest(path: Path) -> str:
    result = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                result.update(chunk)
    except OSError as exc:
        raise GambatteError(f"cannot hash {path}: {exc}") from exc
    return result.hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def file_status(pin: dict[str, Any]) -> dict[str, Any]:
    path_text = pin.get("path", "")
    expected = pin.get("sha256", "")
    row: dict[str, Any] = {"status": "UNAVAILABLE", "path": path_text, "sha256": expected}
    if not isinstance(path_text, str) or not path_text:
        row["reason"] = "pin path is not configured"
        return row
    if not isinstance(expected, str) or len(expected) != 64:
        row["reason"] = "pin SHA-256 is not configured"
        return row
    path = resolve(path_text)
    if not path.is_file():
        row["reason"] = "pinned file is missing"
        return row
    actual = digest(path)
    row["actual_sha256"] = actual
    if actual != expected:
        row["status"] = "DRIFT"
        row["reason"] = "pinned file hash differs"
        return row
    row["status"] = "PASS"
    return row


def core_capabilities(path: Path) -> dict[str, Any]:
    try:
        library = ctypes.CDLL(str(path))
    except OSError as exc:
        return {"status": "FAIL", "reason": str(exc), "symbols": {}}
    symbols = {name: hasattr(library, name) for name in REQUIRED_SYMBOLS}
    missing = [name for name, present in symbols.items() if not present]
    return {
        "status": "PASS" if not missing else "FAIL",
        "symbols": symbols,
        **({"reason": f"missing symbols: {', '.join(missing)}"} if missing else {}),
    }


def health_report(pins: dict[str, Any]) -> dict[str, Any]:
    files = {name: file_status(pins.get(name, {})) for name in ("source", "core", "rom")}
    requirements = pins.get("requirements", {})
    required_domains = list(REQUIRED_DOMAIN_NAMES)
    required_registers = list(REQUIRED_REGISTERS)
    capabilities = {
        "core": core_capabilities(resolve(pins.get("core", {}).get("path", "")))
        if files["core"]["status"] == "PASS"
        else {"status": "UNAVAILABLE", "symbols": {}},
        "domains": {
            "required": required_domains,
            "pinned": requirements.get("domains"),
            "status": "PASS" if requirements.get("domains") == required_domains else "DRIFT",
        },
        "registers": {
            "required": required_registers,
            "pinned": requirements.get("registers"),
            "status": "PASS" if requirements.get("registers") == required_registers else "DRIFT",
        },
        "trace": {
            "required": "anchored-exec-v1",
            "pinned": requirements.get("trace"),
            "status": "PASS" if requirements.get("trace") == "anchored-exec-v1" else "DRIFT",
        },
        "framebuffer": {
            "required": "rgba8888-160x144",
            "pinned": requirements.get("framebuffer"),
            "status": "PASS" if requirements.get("framebuffer") == "rgba8888-160x144" else "DRIFT",
        },
        "boot": {
            "required": "no-bios",
            "pinned": pins.get("boot", {}).get("mode"),
            "status": "PASS" if pins.get("boot", {}).get("mode") == "no-bios" else "DRIFT",
        },
    }
    status = "PASS" if all(row["status"] == "PASS" for row in files.values()) and all(
        row["status"] == "PASS" for row in capabilities.values()
    ) else "FAIL"
    return {
        "schema": 1,
        "status": status,
        "api": pins.get("api"),
        "files": files,
        "capabilities": capabilities,
    }


def download_source(pin: dict[str, Any]) -> Path:
    destination = resolve(pin["path"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and digest(destination) == pin["sha256"]:
        return destination
    descriptor, temporary = tempfile.mkstemp(prefix=".gambatte-source.", dir=destination.parent)
    os.close(descriptor)
    try:
        request = urllib.request.Request(pin["url"], headers={"User-Agent": "poketcg-completion"})
        with urllib.request.urlopen(request, timeout=120) as response, open(temporary, "wb") as stream:
            shutil.copyfileobj(response, stream)
        if digest(Path(temporary)) != pin["sha256"]:
            raise GambatteError("downloaded Gambatte source hash differs from pin")
        os.replace(temporary, destination)
    except (OSError, urllib.error.URLError) as exc:
        raise GambatteError(f"cannot download Gambatte source: {exc}") from exc
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return destination


def extract_source(archive: Path) -> None:
    BUILD_ROOT.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".gambatte-extract.", dir=BUILD_ROOT))
    try:
        with tarfile.open(archive, "r:gz") as bundle:
            bundle.extractall(temporary, filter="data")
        roots = [entry for entry in temporary.iterdir() if entry.is_dir()]
        if len(roots) != 1:
            raise GambatteError("Gambatte archive does not contain one source root")
        if SOURCE_ROOT.exists():
            shutil.rmtree(SOURCE_ROOT)
        roots[0].replace(SOURCE_ROOT)
    except (OSError, tarfile.TarError) as exc:
        raise GambatteError(f"cannot extract Gambatte source: {exc}") from exc
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def bootstrap(pins: dict[str, Any]) -> dict[str, Any]:
    source_pin = pins["source"]
    archive = download_source(source_pin)
    extract_source(archive)
    command = [
        "uvx",
        "--from",
        f"scons=={source_pin['scons_version']}",
        "scons",
        "shlib",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=SOURCE_ROOT / "libgambatte",
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GambatteError(f"cannot build Gambatte: {exc}") from exc
    if completed.returncode:
        raise GambatteError((completed.stderr or completed.stdout).strip() or "Gambatte build failed")
    core = resolve(pins["core"]["path"])
    actual = digest(core)
    if actual != pins["core"]["sha256"]:
        raise GambatteError(f"source-built Gambatte hash differs: {actual}")
    report = health_report(pins)
    if report["status"] != "PASS":
        raise GambatteError("Gambatte health failed after bootstrap")
    return report


def configure_library(path: Path) -> ctypes.CDLL:
    library = ctypes.CDLL(str(path))
    library.gambatte_create.restype = ctypes.c_void_p
    library.gambatte_destroy.argtypes = [ctypes.c_void_p]
    library.gambatte_loadbuf.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_ubyte),
        ctypes.c_uint,
        ctypes.c_uint,
    ]
    library.gambatte_loadbuf.restype = ctypes.c_int
    library.gambatte_runfor.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int16),
        ctypes.POINTER(ctypes.c_uint),
    ]
    library.gambatte_runfor.restype = ctypes.c_int
    library.gambatte_setinputgetter.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    library.gambatte_setexeccallback.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    library.gambatte_setcgbpalette.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    library.gambatte_settimemode.argtypes = [ctypes.c_void_p, ctypes.c_bool]
    library.gambatte_settime.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong]
    library.gambatte_getmemoryarea.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_int),
    ]
    library.gambatte_getmemoryarea.restype = ctypes.c_bool
    library.gambatte_cpuread.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
    library.gambatte_cpuread.restype = ctypes.c_ubyte
    library.gambatte_getregs.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    return library


def register_snapshot(library: ctypes.CDLL, core: int) -> dict[str, int]:
    values = (ctypes.c_int * 10)()
    library.gambatte_getregs(core, values)
    return {name: int(values[index]) for name, index in REGISTER_INDICES.items()}


def memory_area(library: ctypes.CDLL, core: int, name: str) -> bytes:
    pointer = ctypes.c_void_p()
    length = ctypes.c_int()
    if not library.gambatte_getmemoryarea(core, AREA_IDS[name], ctypes.byref(pointer), ctypes.byref(length)):
        raise GambatteError(f"Gambatte does not expose {name}")
    byte_length = length.value * 4 if name.endswith("Palette RGB") else length.value
    if not pointer.value or byte_length <= 0:
        raise GambatteError(f"Gambatte exposed empty {name}")
    return ctypes.string_at(pointer.value, byte_length)


def color_lut() -> ctypes.Array[ctypes.c_int]:
    values = (ctypes.c_int * 32768)()
    for blue in range(32):
        for green in range(32):
            for red in range(32):
                index = red | green << 5 | blue << 10
                r8 = red * 255 // 31
                g8 = green * 255 // 31
                b8 = blue * 255 // 31
                values[index] = ctypes.c_int(0xFF000000 | r8 << 16 | g8 << 8 | b8).value
    return values


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", binascii.crc32(body) & 0xFFFFFFFF)


def encode_png(framebuffer: ctypes.Array[ctypes.c_uint32]) -> bytes:
    rows = bytearray()
    for y in range(HEIGHT):
        rows.append(0)
        for x in range(WIDTH):
            pixel = int(framebuffer[y * WIDTH + x])
            rows.extend(((pixel >> 16) & 0xFF, (pixel >> 8) & 0xFF, pixel & 0xFF, 0xFF))
    header = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", header) + png_chunk(
        b"IDAT", zlib.compress(bytes(rows), level=9)
    ) + png_chunk(b"IEND", b"")


def capture_record(pins: dict[str, Any], scenario: str, frames: int, anchor: int, screenshot: Path) -> dict[str, Any]:
    library = configure_library(resolve(pins["core"]["path"]))
    rom = resolve(pins["rom"]["path"]).read_bytes()
    rom_buffer = (ctypes.c_ubyte * len(rom)).from_buffer_copy(rom)
    framebuffer = (ctypes.c_uint32 * (WIDTH * HEIGHT))()
    sound = (ctypes.c_int16 * ((SAMPLES_PER_FRAME + 2064) * 2))()
    input_callback_type = ctypes.CFUNCTYPE(ctypes.c_uint, ctypes.c_void_p)
    exec_callback_type = ctypes.CFUNCTYPE(None, ctypes.c_uint, ctypes.c_ulonglong)
    trace: list[dict[str, int]] = []
    current_frame = 0

    @input_callback_type
    def neutral_input(_: int) -> int:
        return 0

    @exec_callback_type
    def execution(address: int, cycle_offset: int) -> None:
        if address == anchor:
            trace.append({
                "sequence": len(trace),
                "frame": current_frame,
                "address": int(address),
                "cycle_offset": int(cycle_offset),
            })

    core = library.gambatte_create()
    if not core:
        raise GambatteError("gambatte_create returned null")
    try:
        flags = 1 | 16 | 32
        if library.gambatte_loadbuf(core, rom_buffer, len(rom), flags) != 0:
            raise GambatteError("gambatte_loadbuf failed")
        library.gambatte_setinputgetter(core, ctypes.cast(neutral_input, ctypes.c_void_p), None)
        library.gambatte_setexeccallback(core, ctypes.cast(execution, ctypes.c_void_p))
        library.gambatte_setcgbpalette(core, color_lut())
        library.gambatte_settimemode(core, True)
        library.gambatte_settime(core, 0)
        registers_before = register_snapshot(library, core)
        frame_slices: list[list[int]] = []
        for frame in range(frames):
            current_frame = frame
            slices: list[int] = []
            for _ in range(MAX_SLICES_PER_FRAME):
                emitted = ctypes.c_uint(SAMPLES_PER_FRAME)
                rendered_at = library.gambatte_runfor(
                    core, framebuffer, WIDTH, sound, ctypes.byref(emitted)
                )
                slices.append(int(emitted.value))
                if rendered_at >= 0:
                    break
            else:
                raise GambatteError(f"no rendered frame after {MAX_SLICES_PER_FRAME} slices")
            frame_slices.append(slices)
        registers_after = register_snapshot(library, core)
        domains = {name: memory_area(library, core, name) for name in AREA_IDS}
        domains["VRAM Bank 0"] = domains["VRAM"][:0x2000]
        domains["VRAM Bank 1"] = domains["VRAM"][0x2000:]
        domains["System Bus"] = bytes(library.gambatte_cpuread(core, address) for address in range(0x10000))
        expected_rom_length = len(rom)
        expected = {**EXPECTED_DOMAIN_LENGTHS, "ROM": expected_rom_length}
        for name, length in expected.items():
            if len(domains[name]) != length:
                raise GambatteError(f"{name} length {len(domains[name])} != {length}")
        atomic_write(screenshot, encode_png(framebuffer))
        return {
            "schema": 1,
            "format": "gambatte-raw-v1",
            "scenario": scenario,
            "frames": frames,
            "input_rle": [{"buttons": 0, "frames": frames}],
            "domains": {name: value.hex() for name, value in sorted(domains.items())},
            "registers_before": registers_before,
            "registers_after": registers_after,
            "trace": trace,
            "trace_filter": {"schema": "anchored-exec-v1", "anchor": anchor},
            "frame_slices": frame_slices,
            "framebuffer": {"schema": "rgba8888-160x144", "width": WIDTH, "height": HEIGHT},
            "screenshot": str(screenshot.relative_to(ROOT)),
            "capture_order": ["frames", "registers", "direct-domains", "system-bus", "screenshot"],
            "provenance": {
                "oracle": "gambatte-headless",
                "source_commit": pins["source"]["commit"],
                "source_sha256": pins["source"]["sha256"],
                "core_sha256": pins["core"]["sha256"],
                "rom_sha256": pins["rom"]["sha256"],
                "boot_mode": pins["boot"]["mode"],
            },
        }
    finally:
        library.gambatte_destroy(core)


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise GambatteError("capture screenshot is not a PNG")
    return struct.unpack(">II", data[16:24])


def load_capture(path: Path, pins: dict[str, Any]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise GambatteError(f"invalid raw capture: {exc}") from exc
    if not isinstance(value, dict) or value.get("format") != "gambatte-raw-v1":
        raise GambatteError("raw capture format is not gambatte-raw-v1")
    if value.get("schema") != 1:
        raise GambatteError("raw capture schema is not 1")
    domains = value.get("domains")
    if not isinstance(domains, dict) or set(domains) != set(REQUIRED_DOMAIN_NAMES):
        raise GambatteError("raw capture domains differ from the required set")
    expected = {**EXPECTED_DOMAIN_LENGTHS, "ROM": resolve(pins["rom"]["path"]).stat().st_size}
    decoded: dict[str, bytes] = {}
    for name, length in expected.items():
        try:
            decoded[name] = bytes.fromhex(domains[name])
        except (TypeError, ValueError) as exc:
            raise GambatteError(f"raw capture has invalid {name}") from exc
        if len(decoded[name]) != length:
            raise GambatteError(f"raw capture {name} length differs")
    required_registers = set(REGISTER_INDICES)
    for field in ("registers_before", "registers_after"):
        registers = value.get(field)
        if not isinstance(registers, dict) or set(registers) != required_registers or any(
            not isinstance(item, int) for item in registers.values()
        ):
            raise GambatteError(f"raw capture has invalid {field}")
    input_rle = value.get("input_rle")
    if not isinstance(input_rle, list) or input_rle != [{"buttons": 0, "frames": value.get("frames")}]:
        raise GambatteError("raw capture has invalid neutral input RLE")
    trace = value.get("trace")
    if not isinstance(trace, list) or not trace or any(
        not isinstance(event, dict)
        or set(event) != {"sequence", "frame", "address", "cycle_offset"}
        or event["sequence"] != index
        or any(not isinstance(item, int) for item in event.values())
        for index, event in enumerate(trace)
    ):
        raise GambatteError("raw capture has invalid anchored execution trace")
    trace_filter = value.get("trace_filter")
    if not isinstance(trace_filter, dict) or trace_filter.get("schema") != "anchored-exec-v1":
        raise GambatteError("raw capture trace filter is invalid")
    frame_slices = value.get("frame_slices")
    if not isinstance(frame_slices, list) or len(frame_slices) != value.get("frames") or any(
        not isinstance(slices, list)
        or not slices
        or any(not isinstance(item, int) or item <= 0 for item in slices)
        for slices in frame_slices
    ):
        raise GambatteError("raw capture frame slices are invalid")
    provenance = value.get("provenance")
    expected_provenance = {
        "oracle": "gambatte-headless",
        "source_commit": pins["source"]["commit"],
        "source_sha256": pins["source"]["sha256"],
        "core_sha256": pins["core"]["sha256"],
        "rom_sha256": pins["rom"]["sha256"],
        "boot_mode": "no-bios",
    }
    if provenance != expected_provenance:
        raise GambatteError("raw capture provenance differs from pins")
    screenshot_text = value.get("screenshot")
    if not isinstance(screenshot_text, str):
        raise GambatteError("raw capture screenshot path is invalid")
    screenshot = resolve(screenshot_text)
    if not screenshot.is_file() or png_dimensions(screenshot) != (WIDTH, HEIGHT):
        raise GambatteError("raw capture screenshot dimensions differ")
    value["_decoded_domains"] = decoded
    return value


def import_capture(path: Path, output: Path, pins: dict[str, Any]) -> dict[str, Any]:
    record = load_capture(path, pins)
    domains = record.pop("_decoded_domains")
    screenshot = resolve(record["screenshot"])
    imported = {
        "schema": 1,
        "format": "gambatte-import-v1",
        "scenario": record["scenario"],
        "frames": record["frames"],
        "input_rle": record["input_rle"],
        "input_sha256": hashlib.sha256(
            json.dumps(record["input_rle"], sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "domain_sha256": {name: hashlib.sha256(value).hexdigest() for name, value in sorted(domains.items())},
        "registers_before": record["registers_before"],
        "registers_after": record["registers_after"],
        "trace": record["trace"],
        "trace_filter": record["trace_filter"],
        "framebuffer": record["framebuffer"],
        "screenshot_sha256": digest(screenshot),
        "raw_capture_sha256": digest(path),
        "provenance": record["provenance"],
        "oracle": "gambatte-headless",
        "savestate_canonical": False,
    }
    atomic_write(output, (json.dumps(imported, sort_keys=True, separators=(",", ":")) + "\n").encode())
    return imported


def workspace_output(path: Path) -> Path:
    resolved = path if path.is_absolute() else ROOT / path
    resolved = resolved.resolve()
    if not resolved.is_relative_to(ROOT):
        raise GambatteError("capture output must stay inside the workspace")
    return resolved


def capture(args: argparse.Namespace, pins: dict[str, Any]) -> dict[str, Any]:
    report = health_report(pins)
    if report["status"] != "PASS":
        raise GambatteError("Gambatte health is not PASS")
    output = workspace_output(args.output or Path(f"build/completion/gambatte/{args.scenario}.json"))
    screenshot = output.with_suffix(".png")
    imported_output = workspace_output(args.import_output or output.with_suffix(".imported.json"))
    for stale in (output, screenshot, imported_output):
        stale.unlink(missing_ok=True)
    record = capture_record(pins, args.scenario, args.frames, args.anchor, screenshot)
    atomic_write(output, (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode())
    imported = import_capture(output, imported_output, pins)
    return {"status": "PASS", "scenario": args.scenario, "raw": str(output.relative_to(ROOT)), "import": imported}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("bootstrap", "health", "capture", "import"))
    parser.add_argument("scenario", nargs="?")
    parser.add_argument("--frames", type=int, default=1)
    parser.add_argument("--anchor", type=lambda value: int(value, 0), default=0x0150)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--import-output", type=Path)
    parser.add_argument("--input", type=Path)
    args = parser.parse_args(argv)
    try:
        pins = load_pins()
        if args.command == "bootstrap":
            print(json.dumps(bootstrap(pins), sort_keys=True))
            return 0
        if args.command == "health":
            report = health_report(pins)
            print(json.dumps(report, sort_keys=True))
            return 0 if report["status"] == "PASS" else 2
        if args.command == "import":
            if not args.input or not args.output:
                parser.error("import requires --input and --output")
            imported = import_capture(args.input, workspace_output(args.output), pins)
            print(json.dumps({"status": "PASS", "import": imported}, sort_keys=True))
            return 0
        if not args.scenario:
            parser.error("capture requires a scenario")
        if args.frames < 1:
            parser.error("--frames must be positive")
        print(json.dumps(capture(args, pins), sort_keys=True))
        return 0
    except (GambatteError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
