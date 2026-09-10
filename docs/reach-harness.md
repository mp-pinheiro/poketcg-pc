# The reach harness

The parts of the game no button search reaches, and what reaches them.

| class | why unreachable | mechanism | state |
|---|---|---|---|
| booster packs, auto deck machines, credits variants, gift center | need state: packs owned, collection, medals, event flags | save-seeded sessions | built |
| link duels, Card Pop (IR) | need a peer console | native peer transport, two-console loopback | transport built and smoke-verified; the duel needs a route to the Battle Center (#3390) |
| printer | needs a printer peer | scripted printer responder on the same transport | responder built; the packet sequence needs the printer menu (#3391) |
| SGB | only when `wConsole == CONSOLE_SGB`; the ROM on CGB hardware never takes it | excluded, hardware-only | decided |

## Save-seeded sessions

A session directory may hold `save.sav`, the raw 32 KiB cartridge RAM. Both
lanes start from it: the reference seeds CartRAM before the first instruction
(`refstream.Core(save=...)`, through gambatte's memory-area pointer) and the
native lane takes `--load-save` (the port's `PKSR` container, written by
`session.py` from the raw image at run time). The save is part of the stream
key, so a session with a save never shares a reference cache with one
without; `ai-duel`, `deck-seed`, `from-script` and `pilot.py` inherit the base
session's save, and the coverage ledger, the explorer and the audio seed pass
replay with it.

`just savegen base NAME --from SESSION --at N` takes the image from the
reference at an ordinal of a recorded session and reports whether the general
save data validates (`engine/save.asm`: magic `$08 $00`, byte count, 16-bit
sum over the mapped block). `just savegen edit SAVE --out FILE` changes the
collection (`--card CHARMANDER=2`, `--all-cards 4`), the PC packs
(`--pack 0=1`), the medal count (`--medals 3`) and event variables
(`--event EVENT_BEAT_MITCH=1`, decoded through `EventVarMasks` in
`overworld/scripting.asm`), then recomputes the checksum and refreshes the
SRAM2 backups the game falls back to. `just session-seeded NAME SAVE --then
A,Ax5` records the session: the boot prefix (`boot-menu`, where a valid save
adds Continue to the menu) plus `explore.py` action labels. Measured: a
seeded session from `practice-win`'s save with three medals and three packs
verifies clean on both lanes, and both lanes read the same SRAM at ordinal
1,200.

Seeded sessions are ordinary Discover seeds afterwards: `just
coverage-discover seed-packs` searches the buttons from the poked world.
Route items #3388 (packs) and #3389 (deck machines) name the first two.

## The peer: link, IR, printer

Neither oracle has a serial partner: the gbref runner has no serial surface
and the gambatte runner exposes none. The protocols are request/response over
`rSB`/`rSC` (`home/serial.asm`: `SerialTimerHandler` starts a transfer under
`wSerialOp = $29`, `SerialHandler` is the ISR that consumes the received byte,
answers, and re-arms the external clock; a transfer that sees no serial
interrupt within four timer ticks sets bit 7 of `wSerialFlags`) and over
`rRP` for IR (`link/ir_core.asm`, bit-banged; the native already models the
sampled receive stream in `src/mem.c`, `g_ir_*`, and the gbref patch mirrors
it for the per-routine oracle). The link duel starts from the Battle Center
(`home/map.asm GameEvent_BattleCenter` → `link/link_duel.asm`
`_SetUpAndStartLinkDuel`), which decides master and slave from `wSerialOp`,
exchanges names, decks, the prize count and the RNG, and then runs the duel
with the remote side's turns through `DoLinkOpponentTurn`.

Built, native first:

1. `src/link.c` is the transport, hooked into the bus: a write to `rSC` with
   bit 7 set arms a transfer (`link_note_sc_write`), and every bus read pumps
   it (`link_pump` off `mem.c`'s poll, which is what breaks the ROM's own
   spins on `rSC` bit 7 and `wSerialRecvCounter` — on hardware those spin
   until the serial interrupt fires). An armed side sends one 3-byte frame
   (magic, armed, `rSB`) over the socketpair given by `--link-fd`; when the
   peer's frame arrives, `rSB` takes the peer's byte, `rSC` bit 7 clears and
   `SerialHandler()` runs, exactly where the hardware ISR would. An armed
   internal-clock side whose peer never answers within two seconds completes
   with `$FF`, the way a master clocking an absent slave does; `link_drain`
   settles the pending transfer at exit so a run that ends mid-transfer is
   not a lost byte. The port with no `--link-fd` is unchanged: `link_pump`
   returns on one compare, `session-verify boot-menu` is clean and
   `oracle-diff SerialHandler` passes.
2. `just peer-loopback` runs two natives over one socketpair from a recorded
   session's prefix, one poked to arm an internal-clock transfer and one an
   external-clock one. Measured: 1,095 and 1,096 exchanges, `crossed=True`
   (each side's first received byte is the other's), `wSerialCounter`
   advancing on both (the ISR ran) and `wSerialFlags` bit 7 clear (no
   four-tick ROM timeout). A transport timeout on the side that outlives its
   peer is teardown, not a defect. `just peer-printer` puts a scripted
   responder on the far end: 569 exchanges, 569 bytes answered.
3. What is still missing is the *route*, not the transport: the ROM opens the
   link only from the Battle Center (`GameEvent_BattleCenter`), and the
   printer only from its menu. Both are save-seeded-session plus Discover
   work (#3390, #3391). With the route, the invariant is the duel one: both
   consoles end with complementary `wDuelResult` and prize counts, and each
   console's view of the other's play area equals the other's own at every
   turn boundary.

Oracle proof waits for a reference with a serial partner: the BizHawk-style
dual-core link (`gambatte_linkstatus`) in the reference build. Until then the
link, IR and printer routines stay in the ledger's unexecuted set with this
document as their reason; no peer transcript is invented and called an
oracle.

## SGB

`engine/sgb.asm` (19 routines) is excluded as hardware-only in
`tools/progress/scope.toml`, consistent with `docs/vision.md` (CGB target) and
the exclusion taxonomy: the ROM on CGB hardware never takes the path and
neither oracle emulates the Super Game Boy.
