# Seeded state and peer reach

This reference covers stateful scenarios that ordinary button exploration cannot construct, plus bounded peer-transport proof. It does not replace the session and coverage workflow in [grind](grind.md) or [coverage-program](coverage-program.md).

## Seeded SRAM and backups

A session may carry `save.sav`, a raw 32 KiB cartridge-RAM image. The reference seeds cartridge RAM before the first instruction; the native session runner loads the corresponding `PKSR` container generated from that raw image. The save participates in the stream key, so sessions with different seeded state do not share reference cache identity. Derived sessions such as `ai-duel`, `deck-seed`, and `from-script` inherit their base save; seeded state is likewise used by explorers and evidence replay.

`just savegen base NAME --from SESSION --at N` captures the reference save at an ordinal. `just savegen edit SAVE --out FILE` edits collection, packs, medals, events, or deck slots; see `just savegen edit --help` for the supported switches. Editing recomputes general save validation data and refreshes the SRAM2 backup copies the game may use for recovery. A seeded saved-deck slot needs a non-empty name. `just session-seeded NAME SAVE --then ACTIONS` records a session from the save, including the boot prefix needed for valid saves.

Seeded sessions can seed further exploration from their constructed world. They are evidence inputs, not permission to treat generated save state as a route through the game's ordinary menus.

## Peer scope and proof

Link duels use serial registers `rSB`/`rSC`; Card Pop uses the bit-banged IR path through `rRP`; printer traffic uses the same peer transport with a scripted responder. The native peer transport is exercised over a socketpair supplied through `--link-fd`, which is available on Linux only. The no-peer path remains the ordinary session path and does not require that descriptor.

`just peer-loopback` checks two native instances exchanging serial bytes, including ISR progress and absence of the ROM's serial timeout; it is native transport proof, not a linked-reference session. `just peer-printer` checks the scripted responder, likewise distinct from printer-session proof.

Separate linked-reference evidence now proves full link-duel sessions `link-duel-a` and `link-duel-b` against native and linked Gambatte lanes. The `printer-card-list` session similarly passes with native and linked-reference lanes, including matching printer pages. These session results establish behavior for those recorded routes; they do not establish Card Pop/IR proof or every possible peer route.

The current boundary is specifically IR/Card Pop, whose reference evidence and routes remain unproven here. Do not infer oracle proof from loopback transcripts, or generalize the recorded link/printer sessions beyond their exercised routes.

## Other scope boundaries

Save-seeded sessions address state requirements such as owned packs, cards, medals, and event flags. They do not by themselves prove every menu or script route.

Super Game Boy code is excluded: the target behavior is CGB, and the ROM's SGB path is hardware-specific. This is a scope decision, not an unmeasured session failure.
