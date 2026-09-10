#!/usr/bin/env python3
"""Two native consoles over one serial link, and a scripted printer peer.

`loopback` runs two `poketcg --link-fd` processes over a socketpair: side A
arms an internal-clock transfer, side B an external-clock one, and the
transport swaps their $FF01 bytes and runs SerialHandler on both, the way the
hardware's serial interrupt does. What it proves is the transport and the
ROM's own serial state: the first byte each side received, wSerialCounter advancing
(the ISR ran), and wSerialFlags bit 7 clear (no four-tick ROM timeout). A
transport timeout on the side that outlives its peer is teardown, not a
defect: it is the console left armed with the cable pulled. A duel
across the link needs a recorded route to the Battle Center; see
docs/reach-harness.md and tracker #3390.

`printer` puts a scripted responder on the far end of the same socket, so the
printer packet sequence has something to answer it (#3391).
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
import scenario as scenario_module
import session

FRAME_MAGIC = 0x5A
FRAME_SIZE = 3
RSB = 0xFF01
RSC = 0xFF02
SC_START = 0x80
SC_INTERNAL = 0x01
WRAM = {"wSerialCounter": 0xCB92, "wSerialFlags": 0xCB93, "wSerialRecvBuf": 0xCB95,
        "wSerialOp": 0xCB94}
PRINTER_STATUS = 0x00
PRINTER_ALIVE = 0x81


class PeerError(RuntimeError):
    pass


def wram_addresses() -> dict[str, int]:
    """The serial WRAM symbols this driver reads, from the disassembly's map."""
    wanted = set(WRAM)
    found: dict[str, int] = {}
    for line in (ROOT / "poketcg" / "poketcg.sym").read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] in wanted and parts[0].startswith("00:"):
            found[parts[1]] = int(parts[0].split(":")[1], 16)
    missing = wanted - set(found)
    if missing:
        raise PeerError(f"symbols absent from poketcg.sym: {', '.join(sorted(missing))}")
    return found


def side_directory(root: Path, name: str, masks: list[int], pokes: refstream.Pokes,
                   save: bytes | None) -> Path:
    directory = root / name
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "input.txt").write_text("\n".join(str(m) for m in masks) + "\n")
    (directory / "pokes.txt").write_text(refstream.pokes_text(pokes))
    if save is not None:
        (directory / "save.pksr").write_bytes(session.native_save_file(save))
    return directory


def run_side(directory: Path, ordinals: int, lag: Path, fd: int, dump: int) -> dict[str, Any]:
    state = directory / "state.json"
    command = [
        str(scenario_module.BINARY), "--headless",
        "--data-pack", str(scenario_module.PACK),
        "--frames", "0", "--stop-ordinal", str(ordinals),
        "--input-ordinal", str(directory / "input.txt"),
        "--poke-ordinal", str(directory / "pokes.txt"),
        "--lag-track", str(lag),
        "--dump-state", str(state),
        "--dump-state-ordinals", str(dump),
        "--link-fd", str(fd),
    ]
    save = directory / "save.pksr"
    if save.is_file():
        command += ["--load-save", str(save)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                            pass_fds=(fd,), timeout=600, check=False)
    row: dict[str, Any] = {"side": directory.name, "returncode": result.returncode,
                           "stderr": result.stderr.strip()[-600:]}
    for line in result.stderr.splitlines():
        if line.startswith("link: "):
            row.update(dict(part.split("=") for part in line[6:].split()))
    dump_path = state.with_name(f"{state.stem}-f{dump}.json")
    if dump_path.is_file():
        payload = json.loads(dump_path.read_text())
        wram = bytes(payload["wram"])
        row["wram"] = {name: wram[address - 0xC000] for name, address in wram_addresses().items()}
        row["rsb"] = payload["io"][RSB - 0xFF00]
        row["rsc"] = payload["io"][RSC - 0xFF00]
    return row


def loopback(base: str, *, at: int, ordinals: int, byte_a: int, byte_b: int) -> int:
    masks, meta = session.load_session(base)
    if not 1 <= at < ordinals <= len(masks):
        raise PeerError(f"need 1 <= --at < --ordinals <= {len(masks)}")
    frames = session.reference_frames(masks, meta)
    lag = ROOT / session.build_reference(base, masks, frames, pokes=meta["pokes"],
                                         save=meta["save"])["directory"] / "lag.txt"
    prefix = masks[:ordinals]
    left, right = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="peer-") as tmp:
        root = Path(tmp)
        sides = []
        for name, sock, byte, control in (("master", left, byte_a, SC_START | SC_INTERNAL),
                                          ("slave", right, byte_b, SC_START)):
            pokes: refstream.Pokes = {k: list(v) for k, v in meta["pokes"].items() if k <= at}
            pokes.setdefault(at, []).extend([(RSB, byte), (RSC, control)])
            sides.append((side_directory(root, name, prefix, pokes, meta["save"]), sock))
        threads = []
        for directory, sock in sides:
            def worker(directory: Path = directory, sock: socket.socket = sock) -> None:
                rows.append(run_side(directory, ordinals, lag, sock.fileno(), ordinals))

            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    left.close()
    right.close()
    rows.sort(key=lambda row: row["side"])
    failed = 0
    for row in rows:
        wram = row.get("wram", {})
        ok = (row["returncode"] == 0 and int(row.get("exchanges", 0)) >= 1
              and wram.get("wSerialCounter", 0) >= 1
              and not wram.get("wSerialFlags", 0xFF) & 0x80)
        failed += not ok
        print(f"LINK {row['side']} exchanges={row.get('exchanges')} "
              f"timeouts={row.get('timeouts')}/{row.get('drained')} "
              f"first=0x{int(row.get('first', -1)) & 0xFF:02X} serial_counter={wram.get('wSerialCounter')} "
              f"serial_flags=0x{wram.get('wSerialFlags', 0):02X} status={'ok' if ok else 'fail'}")
        if not ok and row["stderr"]:
            for line in row["stderr"].splitlines()[-3:]:
                print(f"NATIVE {row['side']} {line}")
    if len(rows) == 2 and not failed:
        received = {row["side"]: int(row.get("first", -1)) & 0xFF for row in rows}
        crossed = received["master"] == byte_b and received["slave"] == byte_a
        print(f"LOOPBACK crossed={crossed} master_received=0x{received['master']:02X} "
              f"slave_received=0x{received['slave']:02X}")
        failed += not crossed
    return 1 if failed else 0


def printer_responder(sock: socket.socket, stop: threading.Event) -> list[int]:
    """Answers every framed byte with the printer's status pair, which is what
    the ROM's packet sequence polls for."""
    seen: list[int] = []
    sock.settimeout(0.2)
    while not stop.is_set():
        try:
            frame = sock.recv(FRAME_SIZE)
        except TimeoutError:
            continue
        except OSError:
            break
        if len(frame) != FRAME_SIZE or frame[0] != FRAME_MAGIC:
            continue
        seen.append(frame[2])
        reply = PRINTER_ALIVE if len(seen) % 2 else PRINTER_STATUS
        try:
            sock.sendall(bytes([FRAME_MAGIC, 1, reply]))
        except OSError:
            break
    return seen


def printer(base: str, *, at: int, ordinals: int) -> int:
    masks, meta = session.load_session(base)
    if not 1 <= at < ordinals <= len(masks):
        raise PeerError(f"need 1 <= --at < --ordinals <= {len(masks)}")
    frames = session.reference_frames(masks, meta)
    lag = ROOT / session.build_reference(base, masks, frames, pokes=meta["pokes"],
                                         save=meta["save"])["directory"] / "lag.txt"
    console, peer = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
    stop = threading.Event()
    seen: list[int] = []

    def serve() -> None:
        seen.extend(printer_responder(peer, stop))

    thread = threading.Thread(target=serve)
    thread.start()
    with tempfile.TemporaryDirectory(prefix="peer-printer-") as tmp:
        pokes: refstream.Pokes = {k: list(v) for k, v in meta["pokes"].items() if k <= at}
        pokes.setdefault(at, []).extend([(RSB, 0x88), (RSC, SC_START | SC_INTERNAL)])
        directory = side_directory(Path(tmp), "console", masks[:ordinals], pokes, meta["save"])
        row = run_side(directory, ordinals, lag, console.fileno(), ordinals)
    stop.set()
    thread.join()
    console.close()
    peer.close()
    print(f"PRINTER exchanges={row.get('exchanges')} timeouts={row.get('timeouts')} "
          f"responder_bytes={len(seen)} first={[f'0x{b:02X}' for b in seen[:4]]}")
    if row["returncode"] != 0 and row["stderr"]:
        for line in row["stderr"].splitlines()[-3:]:
            print(f"NATIVE {line}")
    return 0 if row["returncode"] == 0 and seen else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    loop_parser = sub.add_parser("loopback", help="two natives over one socketpair")
    loop_parser.add_argument("--from", dest="base", default="boot-menu")
    loop_parser.add_argument("--at", type=int, default=600, help="ordinal that arms the transfer")
    loop_parser.add_argument("--ordinals", type=int, default=1000)
    loop_parser.add_argument("--byte-a", type=lambda v: int(v, 0), default=0x5A)
    loop_parser.add_argument("--byte-b", type=lambda v: int(v, 0), default=0xA5)
    printer_parser = sub.add_parser("printer", help="one native against a scripted printer responder")
    printer_parser.add_argument("--from", dest="base", default="boot-menu")
    printer_parser.add_argument("--at", type=int, default=600)
    printer_parser.add_argument("--ordinals", type=int, default=1000)
    args = parser.parse_args(argv)
    try:
        if args.command == "loopback":
            return loopback(args.base, at=args.at, ordinals=args.ordinals,
                            byte_a=args.byte_a, byte_b=args.byte_b)
        return printer(args.base, at=args.at, ordinals=args.ordinals)
    except (PeerError, session.SessionError, refstream.RefstreamError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
