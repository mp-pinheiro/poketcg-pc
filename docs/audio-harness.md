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
The corpus runs in seconds: 128 seeds at 4096 ticks is 20 s at `--jobs 3`.

Corpus *breadth* is a real gate, not a formality. For its first week the
corpus was 66 seeds taken from one session (`first-duel`), so the driver was
proven only on the states that session reaches. `just audio-seeds ai-duel-01
boot-menu` added 62 more (46 and 16) and all 128 stay clean, which is what
exonerated the driver for #3415: that session's own seeds prove its own
states. When a driver-state fact cannot be localised, add its session to the
corpus before suspecting the driver.

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

`src/audio/music2.asm` reports 34 unexecuted routines and **none of them is
coverage work**, which is worth stating once with the measurement because the
file otherwise sits near the top of `coverage-status`. The two drivers are
parallel ROM copies at identical bank offsets (`poketcg.sym`: `3d:40e9`
Music1_Update, `3e:40e9` Music2_Update), and ten songs are banked `$3e`
(`audio/music2_headers.asm`: PC main menu, Pokemon Dome, Challenge Hall,
Club 1-3, Ronald, Imakuni, Hall of Honor, Credits). A song *starts* through
`_PlaySong` in driver 1's bank and only the per-tick update chain banks into
`wCurSongBank`, so the `$3e` copy is only ever entered at the update offset.
That is why 41 of 75 execute and the rest do not: of the 34, three are the
`_2` trampolines at `3e:400c`, `3e:4015` and `3e:4018` that nothing in the
disassembly references, and the remaining entry points (`Music2_Init`,
`Music2_PlaySong`, `Music2_BeginSong`, `Music2_StopAllChannels`,
`Music2_PauseSong`, `Music2_ResumeSong`, the `Assert*` pair,
`Music2_CheckForNewSound`, `Music2_Update` itself) are reachable only through
those trampolines. 31 of the 34 share their bank offset with a Music1 twin,
and 16 of those twins already execute - the same instructions, entered in the
other bank. This is the `sgb.asm` shape: a scope row, not a session to record.

## What is left

- `credits-1` itself is clean to its last ordinal (864,424). The residue is in
  its two extensions, `credits-1-explore-1` and `-2`, which confirm to
  871,294 and report `audio_first_divergence=858149`: driver state inside a
  66-frame LCD-off block where the ROM's ISRs land between instructions the
  port runs in one block (`docs/grind.md`, "An ad-hoc native run"). Requests
  and placement are correct there and the tick oracle proves the driver from
  every seed it has. Note the audio address is *not* the gated fact: both
  sessions' recorded divergence is at 871,295 on `CopyDataHLtoDE` (#3392,
  #3393, ISR-placement, deferred). Audio is a tolerance class only if the tick
  oracle proves state equivalence under both interleavings; otherwise it is a
  new sync site, paid once.
- #3415 (`ai-duel-01`, DoFrame 32,336) is the same class reached from a
  different direction, and its chain is worth keeping because every link was
  measured. The gated symptom is game state: `wSongOverride` 0 against 9 and
  `wCursorBlinkCounter` 22 against 0. `MainDuelLoop`'s duel-end wait is `do
  DoFrame while (AssertSongFinished())`, and the reference leaves that loop one
  frame before the port, so only the reference runs `PlayDefaultSong`,
  `GetDefaultSong`, `PlaySong` and `InitializeMenuParameters` in that interval
  (per-routine interval counts, reference 1 against native 0 for each).
  `AssertSongFinished` reads `wCurSongID`, which `Music1_CheckForEndOfSong`
  sets from `wMusicIsPlaying[0..3]`; both routines are faithful. Those flags
  follow the per-channel counters `wddbb`/`wddc3`, which already differ at the
  session's *second* DoFrame, and the root byte is
  `wSFXCommandPointers + 2`: a constant +2 in the port from ordinal 2 onward,
  one 2-byte SFX command consumed early on one channel. The driver is
  exonerated - `SFX_Play`, `SFX_Update`, `ExecuteNextSFXCommand`,
  `SFX_ApplyPitchOffset` and `Func_fc26c` all pass `oracle-diff
  --auto-observe`, and 128/128 tick seeds are clean including 46 from this
  session - so what is left is where the tick lands relative to the game
  block, which is ISR placement.
- `p3:audio-pcm`: from the APU write stream with tick timestamps through a
  deterministic APU model, against gambatte's PCM. The write stream is what
  the tick oracle already compares; the model is the one producer still to
  write.
