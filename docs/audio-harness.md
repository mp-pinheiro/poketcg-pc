# Audio proof

The audio harness separates three claims: the sound driver produces the same state and register writes per tick, game code requests the same song and effects, and the recorded ticks occur at the same synchronization points. These are distinct checks; none is a whole-session audio replay.

## Driver tick proof

`just audio-seeds` derives driver states from recorded reference sessions; `just audio-tickdiff` compares the native and reference drivers from those states. The underlying commands are `python3 tools/audio/tickdiff.py seeds [SESSION...] [--every K]` and `python3 tools/audio/tickdiff.py diff [DIGEST...] [--ticks N]`. Seeds include driver WRAM, APU register readback, bank state, song and effect identifiers. Add sessions when the corpus does not represent the states relevant to a change; a narrow seed corpus is not broad proof.

Each tick comparison checks both driver WRAM and the ordered `(address, value)` APU write stream. WRAM equality alone is insufficient: the driver can write an incorrect register without changing observed RAM. The reference runner must model APU readback and trace writes; disabling its APU model makes reads return `$FF` and can create false divergence. Tick runs disable interrupt interleaving so the driver is compared as an isolated state machine.

The isolated tick oracle establishes driver behavior for its seeds. It does not prove when the game invokes the driver or whether the request was correct. Nor does routine-case register observation necessarily capture every IO write; use the tick write stream for driver changes.

## Game requests and placement

At the first relevant audio divergence, compare the four game request bytes: `wCurSongID`, `wCurSongBank`, `wCurSfxID`, and `wSfxPriority`. `just session-verify` reports the `AUDIO` row when a relevant region differs. Matching requests point toward driver behavior; differing requests point toward game behavior.

The `SCHEDULE` row reports `off_schedule`. A nonzero value fails verification: the port did not deliver the recorded number of ticks at a recorded sync point. Correct requests and correct isolated ticks do not excuse incorrect placement.

## Async timer and ISR limits

The tick oracle disables IME and therefore does not exercise an asynchronous timer interrupt or a VBlank ISR interleaving with the sound handler. Session-level proof must retain the recorded synchronization schedule. If the ROM services an ISR between instructions inside a block that the port executes atomically, the resulting audio state can differ despite matching requests and clean isolated ticks. Treat this as an interrupt-placement question, not automatically as a driver defect or as permission to waive placement proof.

Tickdiff is an isolated driver-state and write-stream comparison, not a PCM comparison. PCM is covered by the separate `completion:v2:p3:audio-pcm` evidence producer, which compares native and Gambatte APU trace/PCM censuses against its configured PCM-window thresholds. Keep those claims distinct: tickdiff does not replace PCM evidence, and PCM evidence does not establish game request values or tick placement.
