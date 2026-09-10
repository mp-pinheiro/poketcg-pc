# The audio harness

Phase 3 (timer, APU, audio) is proven by three checks, none of which is a
full-session replay:

1. **Tick oracle** — the sound driver, one timer tick at a time, from seeds
   taken on the reference. `just audio-seeds`, `just audio-tickdiff`.
2. **Request window** — the four bytes game code asks the driver through
   (`wCurSongID`, `wCurSongBank`, `wCurSfxID`, `wSfxPriority`), compared on
   both lanes at the first anchor the audio region differs. The `AUDIO` row of
   `just session-verify`.
3. **Placement** — the port delivers every recorded tick at every recorded
   sync point. The `SCHEDULE` row of `just session-verify`; a non-zero
   `off_schedule` count fails the verify.

Anchor-level audio equality (`GATED = 5` in `tools/completion/session.py`)
stays an integration check at the landing gate, not a per-change cost.

## Why

Audio proof used to be the whole-session replay under the recorded tick
schedule: every driver change cost an 84-session sweep and every new sync site
re-keyed `stream_key`, a ~2 h re-derivation of every reference. The region was
ungated the whole time, so the proof was also incomplete, and the anchor
digests never see the APU registers at all: a driver that writes the right
WRAM and the wrong register is invisible to them.

The driver is a closed state machine. State: `SECTION "WRAM Audio"`
($DD80-$DEE4, 357 bytes) plus the APU registers' readback ($FF10-$FF3F; the
SFX driver reads NR11/NR21/NR41 back and rewrites their duty bits). Input:
song and SFX data in ROM banks $3D-$3F and one tick, `SoundTimerHandler`
(3d:4003). Output: the next state and the APU register writes. Game code
touches it only through the request bytes at already-recorded sync points. So
the driver is provable per tick in isolation, and the game's part reduces to
the request bytes and tick placement.

## Tick oracle

`tools/audio/tickdiff.py seeds [SESSION...] [--every K]` replays sessions on
the reference (gambatte) through their confirmed ordinal and writes a seed at
every K-th tick (default 1024) and at the first tick after each `PlaySong` or
`PlaySFX`: driver WRAM, APU readback, `hBankROM`, song and SFX ids, keyed by
the SHA-256 of the state (`build/audio/seeds/<digest>.json`). One session of
20,000 ticks yields ~66 distinct seeds in 17 s; `--jobs` runs sessions in
worker processes.

`tools/audio/tickdiff.py diff [DIGEST...] [--ticks N]` runs each seed N ticks
(default 4096, ~70 s of music) on both lanes with no game code:

- reference: `tools/oracle/gbref/runner.c` in `completion: tick` mode with
  `repeat: N`. The runner seeds WRAM and the APU registers, sets `rom_bank`
  and `hBankROM` to $3D, disables IME (no VBlank ISR interleaves), enables
  gbrt's APU model (with `enable_audio = false` every APU register reads back
  $FF, which turned the SFX driver's `and $c0` readback into a constant duty 3
  and diverged every seed at tick 1), and calls the entry `repeat` times from
  a fresh sentinel stack. `gbrt-mbc5.patch` adds `oracle_apu_hook` to the
  runtime, called on every write to $FF10-$FF3F.
- native: `src/probe.c` with `repeat: N`, calling the adapter for
  `SoundTimerHandler` N times with `apu_trace_clear()` before each call; the
  write stream comes from `mem.c`'s `apu_trace_record`.

After every tick both lanes emit the driver WRAM and the (address, value)
write stream; the first tick where either differs is reported with the RAM
symbols and both write streams. `build/audio/tickdiff.json` holds the rows.
The corpus runs in seconds: 66 seeds at 4096 ticks is 15 s at `--jobs 3`.

The first run found a defect no anchor gate could: `update_ch_output` in
`src/home/music1.c` and `src/home/music2.c` wrote `rAUD1SWEEP` on the
channel-2 path, where the asm (`Music1_f475a`) writes no sweep register. The
WRAM after the tick was identical on both lanes, so every session was
byte-exact at every anchor; only the write stream showed the extra `$FF10 =
$08`. The tick oracle went red on 62 of 66 seeds before the fix and clean on
all 66 after it; the per-routine oracle passes on both, because case
contracts observe registers and RAM spans, not IO writes. For a driver change
the tick corpus is the canary.

## Request window and placement

`session-verify` prints `SCHEDULE <name> off_schedule=<n>` on every run and
exits 1 when it is not zero: the lane reported a recorded sync point it did
not deliver the recorded tick count at. When the audio region diverges before
any gated region, it also prints `AUDIO ordinal=<k> requests=<same|differ>
...` from one native dump and one reference capture at that anchor: `same`
means the driver was asked the same thing on both lanes and diverged on its
own, which the tick oracle then localises; `differ` means game code asked for
the wrong song, which is an ordinary `DIVERGE`-class fact.

## What is left

- `credits-1` diverges at 858,149 on driver state inside a 66-frame LCD-off
  block where the ROM's ISRs land between instructions the port runs in one
  block (`docs/grind.md`, "An ad-hoc native run"). Requests and placement are
  correct there; the tick oracle proves the driver from every seed it has. It
  is a tolerance class only if the tick oracle proves state equivalence under
  both interleavings; otherwise it is a new sync site, paid once.
- `p3:audio-pcm`: from the APU write stream with tick timestamps through a
  deterministic APU model, against gambatte's PCM. The write stream is what
  the tick oracle already compares; the model is the one producer still to
  write.
