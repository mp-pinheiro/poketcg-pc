# Porting guide & contract

How to port a pret/poketcg routine to C and prove it byte-equivalent against the
PyBoy oracle. Read in full before writing any C. The 19 `home/` leaf routines
already follow this; every later phase should too.

## The loop

```sh
just bootstrap                 # one-time: builds poketcg.gbc + poketcg.sym
uv sync --project tools/oracle --frozen
export POKETCG_BUILD=build-<slice>
export POKETCG_PORTS=<file>    # semicolon-list of pret basenames
just build                     # configure this private tree once
just oracle-warm-group <basename>
just oracle-diff-fast <PretSymbol>
just oracle-diff-group <basename>
just oracle-release-gate       # central release barrier; exits non-zero on any failure
```

`just oracle-diff` remains the live, configure-and-build authority command.
`oracle-warm` captures PyBoy references; `oracle-diff-fast` compares only against
those references and never falls back to PyBoy. Any case, contract, ROM, symbol,
PyBoy, or harness change causes a cache miss; warm the affected routine or group
again. A refresh can retain valid references even when the C probe is red.

During implementation, run `just oracle-diff-fast <PretSymbol>` after each
correction and shape-preserving mutation. Require RED for the mutation and PASS
after restoration. Once the group is fast-green, run the live group check, then
the unchanged full live gate. Cached results accelerate iteration; they are not
accepted evidence without the live checks.

`just oracle-diff` runs cmake+ninja itself. Iterate until `PASS`. When porting
concurrently with other agents, build in a private directory over a private
file subset so neither ninja state nor someone else's in-flight compile error
touches you:

```sh
export POKETCG_BUILD=build-<file>      # private build dir
export POKETCG_PORTS=<file>            # semicolon-list of pret basenames
```

## Files per pret source

CMake globs `src/home/*.c` and `src/probe/*.c`, so new files are picked up with
no build edit. Four files per pret `<file>`:

| path | content |
|---|---|
| `src/home/<file>.h` | prototypes |
| `src/home/<file>.c` | the ported C |
| `src/probe/<file>.c` | adapters + `const ProbeEntry probe_entries_<file>[]` |
| `tests/cases/<file>.py` | `CONTRACT` and `CASES` |

The array name `probe_entries_<file>` must match the filename exactly or the link
fails. Shared infrastructure you do not own: `CMakeLists.txt`, `src/mem.*`,
`src/probe.c`, `src/probe.h`, `src/probe_table.c`, `tests/test_leaves.py`,
`tests/routines.py`, `tools/`, `justfile`.

## Memory model — `src/mem.h`

```c
extern uint8_t g_wram[0x2000];   /* $C000-$DFFF */
extern uint8_t g_hram[0x80];     /* $FF80-$FFFF */
extern uint8_t g_sram[0x8000];   /* 4 banks, windowed at $A000-$BFFF */
extern uint8_t *g_rom; extern size_t g_rom_size;
extern uint8_t g_rom_bank, g_sram_bank;

const uint8_t *rom_ptr(uint8_t bank, uint16_t addr);
uint8_t *gb_ptr(uint16_t addr);
uint8_t  gb_read8(uint16_t addr);
void     gb_write8(uint16_t addr, uint8_t v);   /* writes below $8000 are dropped */
void     BankswitchROM(uint8_t bank);           /* src/home/switch_rom.h */
```

Named locations come from generated headers. Every pret symbol yields three
macros — `wListPointer_ADDR` ($CB72), `wListPointer` (a `uint8_t` lvalue), and
`wListPointer_PTR` (a `uint8_t *`):

```c
#include "generated/wram.h"   /* also hram.h, sram.h */
```

**Representation rule, non-negotiable:** every routine that touches memory takes
and returns **`uint16_t` Game Boy addresses**, never host pointers, and
reads/writes through `gb_read8`/`gb_write8`. Pointers the asm advances become
`uint16_t *` in/out parameters. This is what makes the advance observable in the
diff; it matches the fact that `wListPointer`/`wTempPointer`/`wDecompSourcePosPtr`
store GB addresses in WRAM; and it reproduces 16-bit wraparound exactly. Do not
add a host-pointer variant "for speed".

## Three rules for the C

1. **Zero means maximum.** Every counted loop in this codebase is post-test.
   `bc==0` → 65536 bytes (`CopyDataHLtoDE`, `FillMemoryWithA`, `DecompressData`);
   65536 *pairs* (`FillMemoryWithDE`); `b==0` → 256 blocks and `c==0` → 256
   bytes/block (`CopyGfxData`). Encode as `uint32_t n = n_raw ? n_raw : 0x10000;`
   (or `0x100` for the 8-bit counters).
2. **Advanced pointers are load-bearing.** Routines whose asm advances `hl`/`de`
   past the copied block must write the advanced addresses back through `uint16_t
   *` parameters — callers read past the block (e.g. `card_data.asm:194-198`,
   `sprite_animations.asm:447-452`). By-value wrappers take plain values.
3. **Carry is only sometimes an output.** Model carry as a return value only for
   real outputs. It is *not* an output for `DivideBCbyDE` (exit carry == entry
   carry), nor for routines that end in `pop af` restoring the caller's flags
   (`GetFarByte`, `DecompressDataFromBank`, `CopyBankedDataToDE`). When in doubt,
   check the callsites with grep.

## Probe adapters — `src/probe/<file>.c`

```c
#include "home/<file>.h"
#include "probe.h"

static void adapt_Foo(ProbeState *s) { ... }

const ProbeEntry probe_entries_<file>[] = {
    { "Foo", adapt_Foo },
    { NULL, NULL },
};
```

`ProbeState` is `{ uint8_t a, f, b, c, d, e; uint16_t hl;
uint16_t stack[PROBE_MAX_STACK_WORDS]; uint8_t stack_count; }`
(`src/probe.h`). The native side has no GB frame, so an adapter for a routine
entered mid-frame reads the words its asm would have popped out of
`s->stack[0 .. s->stack_count - 1]` — index 0 is the caller's first push, so
`s->stack[s->stack_count - 1]` is what the routine's first `pop` reads — and
writes them back into whichever registers the asm leaves them in. Two hard rules:

- A register the asm **preserves** must be left untouched by the adapter, so a C
  body that clobbers it shows up as a diff.
- The adapter must never hardcode an output. `s->b = 0;` because "the loop always
  ends with bc==0" is cheating: leave such incidental residue out of `CONTRACT`.

16-bit pairs are assembled and split by hand:

```c
static void adapt_CopyDataHLtoDE(ProbeState *s)
{
    uint16_t de = (uint16_t)(s->d << 8 | s->e);
    CopyDataHLtoDE(&s->hl, &de, (uint16_t)(s->b << 8 | s->c));
    s->d = (uint8_t)(de >> 8);
    s->e = (uint8_t)de;
}
```

Local pret labels carry a `.` (e.g. `DecompressData.Decompress`); register them
under that exact string.

## Cases — `tests/cases/<file>.py`

```python
CONTRACT = {"Foo": {"compare": ("a", "b", "c", "d", "e", "hl"),
                    "preserve": ("d", "e")}}
CASES = {"Foo": [ {...}, {...} ]}
```

`CONTRACT` names exactly the registers the asm contract makes meaningful: real
outputs plus every register the asm claims to preserve. Leave out loop residue
(`a==0` after a `ld a,c / or b` exit, `bc==0` after a counted loop) — it is not
part of the callable contract and forcing it would push a hardcoded value into
the adapter. Flag-preservation guarantees belong in `CONTRACT` only when every
instruction on the path is flag-neutral; seed `f=0xF0` (the low nibble is always
0 on hardware, and both probe and oracle mask it).

### Case-key reference

One line each, matching `diff_case` (`tests/test_leaves.py:95-169`), the
authoritative source:

- `a f b c d e hl` — entry registers, default 0.
- `wram` — `{addr: bytes}`, seeded before the call **and** diffed after.
- `read` — `{addr: count}`, diffed after the call as a live bus read.
- `sram` — `{bank: {addr: bytes}}`, seeded before the call **and** diffed
  after (readback size = seed length).
- `sread` — `{bank: {addr: count}}`, diffed without seeding and read directly
  from the selected SRAM bank.
- `vread` — `{bank: {addr: count}}`, diffed without seeding and read directly
  from the selected VRAM bank. VRAM has no seeding key — routines that read
  pre-existing tile data drive it through a `setup` prelude instead.
- `ramg` — `bool`, applied **after every seed**. The only way a routine's own
  `EnableSRAM`/`DisableSRAM` becomes observable; without it every case starts
  SRAM-enabled and the latch's own effect is invisible.
- `setup` — `[{"fn": ..., <regs>}]`, preludes that run after seeding, in
  order, with RAM **not** reset between them. Use this for warm state a routine
  depends on (e.g. `SetupText` before anything that drives the text engine)
  rather than hand-deriving the expected warm values.
- `oracle: False` + `why` + one or more of `expect`, `expect_regs`,
  `expect_sram`, and `expect_vram` — a boundary the oracle physically cannot
  run. `expect` is `{addr: bytes}`, while `expect_sram` is
  `{bank: {addr: bytes}}` and `expect_vram` has the same shape. All are derived
  from the asm, never read off the oracle; seeded `wram`/`sram` and requested
  banked reads are not compared automatically in a C-only case.
- `keys` — `int`, buttons held for the whole call, or `[int, ...]` (up to 16), a
  per-frame timeline that cycles. Bit layout matches the game's own `hKeysHeld`
  (`poketcg/src/constants/hardware.inc:88-105`): bit0 `A`, 1 `B`, 2 `SELECT`, 3
  `START`, 4 `RIGHT`, 5 `LEFT`, 6 `UP`, 7 `DOWN`.
  The only way to test a routine that spins on `ReadJoypad`/
  `WaitForButtonAorB` — with `keys` unset (0) it waits forever.
  A scalar is held from the first instruction and is therefore *newly pressed
  exactly once*, which is invisible to every wait that starts after that first
  frame. The game's waits read edge-triggered `hKeysPressed`, so a routine with
  more than one wait needs a cycle: `keys=[0x00, 0x01]` taps `A` forever. All
  three lanes cycle it — the reference per rendered frame
  (`tools/oracle/gbref/runner.c`), PyBoy per tick (`tools/oracle/pyboy_oracle.py`),
  and the native probe per completed joypad poll (`src/mem.c`, which has no
  frames). A one-entry timeline never advances, so it is exactly a held scalar.
  "Waits forever" is now bounded on the PyBoy lane. Frames cap emulated time,
  not wall clock, and the two came apart badly: a wedged frame (`mb.tick` spins
  on `while not lcd.frame_done` while `PyBoy._tick` re-enters it per breakpoint)
  never returns, and `PyBoy.tick` holds `cython.nogil` throughout, so neither
  the frame loop nor a signal could end it — seven such processes once burned 12
  CPU-hours after their driver died. `_run` now checks a deadline of
  `max(120 s, 0.25 s x allotted frames)` between frames and raises `OracleError`
  (`verify.py` reads that as a `timeout` verdict naming the spinner), and a
  watchdog thread — which runs because `nogil` released the GIL — hard-exits 30 s
  later if a single frame never came back. Measured cost is ~10 ms/frame, so the
  deadline is 25x headroom; `POKETCG_ORACLE_WALL_FLOOR` moves the floor.
- `stack` — `[int, ...]`, at most four caller-pushed words below the synthesized
  return address, in push order (`stack[-1]` is what the routine's first `pop`
  reads). Declare it only for a routine entered mid-frame — a `jp` target whose
  epilogue pops words its own caller pushed, or a routine that reads `sp+N` above
  its own frame. `_CopyCardNameAndLevel_HalfwidthText`
  (`tests/cases/copy_card_name.py`) is the worked example: its parent does
  `push bc` / `push de` before the `jp`, so its cases declare
  `stack: [saved_bc, saved_de]`. A wrong `stack` produces a red, never a false
  green.

Required coverage per routine:

1. an all-zero case,
2. a poisoned-register case
   (`a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234`, overriding only
   the fields the routine consumes) proving every preservation claim,
3. every boundary — `n=0` for counted routines (must behave as maximum, never a
   no-op), plus counts of 1 and 256/257. 256/257 is where a port that decrements
   only the low byte breaks.

**Legacy `hram` seeds use absolute addresses.** Schema-2 seeds true HRAM
through the absolute-address `wram` bus map, so `legacy_to_schema` merges
`hram={$FF80..$FFFE: ...}` after `wram`. Before 2026-08-26 those entries were
silently dropped; this produced false hangs such as `AITryToRetreat`, whose
`hWhoseTurn=$C2` case actually ran with zero. Legacy cases also misuse `hram`
for `$FF00-$FF7F` hardware IO and `$FFFF` IE; those are deliberately not
migrated as plain RAM because their reads require register-specific masking.

**Reserved WRAM: `$CFF0-$CFF5` and `$DC30-$DCFF`.** Only the PyBoy backend
synthesizes a call frame in WRAM. Its return sentinel and parking loop remain
at `$CFF0` / `$CFF4` in fixed WRAM, where PyBoy execution hooks capture the
exit immediately. Its stack grows down from `$DCC0` inside pret's unallocated
`$D69C-$DD7F` gap. The GBRT runner uses `sp=$FFFE` and sentinel `$FEA0`, both
outside WRAM.

The deep stack was moved from `$CF30-$CFFF` on 2026-08-26 because that range
overlapped live deck and card symbols. Stack depth was measured over the 31
largest registered routines: the deepest call used 86 bytes below entry SP,
reaching `$DC68`; the `$DC30` floor leaves another 57 bytes of margin.

PyBoy cannot hook execution in switchable WRAM, so moving the sentinel itself
to `$DCF0` was rejected: parked-PC capture at the next frame boundary let
serial interrupts mutate state after return. Keeping the six-byte hook stub in
fixed WRAM preserves immediate snapshot semantics. It overlaps part of
`wNamingScreenBuffer`, so `$CFF0-$CFF5` remains unavailable; no current
reserved-window blocker uses that subrange.

Cases may use all formerly-blocked symbols through `$CFD2`, including
`wCurDeckCards` `$CF17`, `wOwnedCardsCountList` / `wUniqueDeckCardList`
`$CF68`, `wCurDeckName` `$CFB9`, `wMaxNumCardsAllowed` `$CFD1`, and
`wSameNameCardsLimit` `$CFD2`. Both backends zero them during reset. A direct
PyBoy probe seeded and read every one back unchanged.

Stack relocation changes wide WRAM cases, not production code. `npc_core.py`
omits `$DC30-$DCFF` from its poison sweep while preserving payload offsets on
both sides. `Func_0bcb` uses SRAM `$A000-$AFFF` as its timing-neutral 4 KiB
source; `$C000-$CFFF` includes `wVBlankCounter`, which PyBoy advances during
the copy. The seven measured regressions all pass after those changes:
`DetectConsole`, `FlamesOfRage_AIEffect`, `ApplyRandomCountToNPCAnim`,
`Func_0bcb`, `UpdateNPCAnimation`, `CometPunch_AIEffect`, and
`UpdateArenaCardIDsAndClearTwoTurnDuelVars`.

Note when measuring: `compare_one.py` cannot show this. It runs GBRT plus the C
probe, and GBRT enters at `sp = 0xfffe` with its stack in HRAM, so neither side
touches `$CFxx` and any seeded pattern survives regardless. Only the PyBoy path
(`tests/test_leaves.py`, `oracle-diff`) exercises the frame.

**The frame boundary: what is already testable and what is not.** A large
blocker cluster (51 stanzas, 3109 B as of 2026-08-26) cites
`DoFrameIfLCDEnabled`/`DoFrame` and asks for "multi-frame VBlank simulation".
That framing is too coarse; measured, the boundary sits elsewhere.

- With the LCD **off** — which `seed_call_environment` guarantees by writing
  `rLCDC = 0` — `DoFrameIfLCDEnabled` is a no-op: it does `bit
  B_LCDC_ENABLE` / `jr z, .done` and returns without calling `DoFrame`
  (`lcd_enable_frame.asm:1-15`). `DoFrameIfLCDEnabled`, `DoFrame`,
  `ExecuteNPCMovement` and `CheckIsAnNPCMoving` are all registered and green,
  and `ExecuteNPCMovement`'s body *is* the `DoFrameIfLCDEnabled` wait loop.
- **But that only holds while the LCD stays off.** A routine that calls
  `EnableLCD` itself — `Func_c2a3` does `EnableLCD -> DoFrameIfLCDEnabled ->
  DisableLCD` — makes the call live and lands on the LCD-on boundary below.
  Merely *calling* `DoFrameIfLCDEnabled` is therefore not sufficient evidence
  either way; check whether anything on the path enables the LCD.
- With the LCD **on** a routine parks at `pc=0x0271`
  (`WaitForVBlank.wait_vblank+1`) with `lcdc=128`, `ie=1`, `ime=1`, `halted=1`
  and `if=224`. **This is NOT a runner HALT deadlock.** That diagnosis was
  recorded here on 2026-08-26 and is disproven by measurement on the same day;
  it cost one reverted runner change (below) and should not be re-derived.
  Corrected findings, each measured on `Script_BeatAaron` (bank `03:5903`) via
  `compare_one.py` with `read` spanning `wVBlankCounter` (`0xCAB8`):
  - **The PPU does advance while halted.** `gb_debug_step` calls `gb_tick(ctx, 4)`
    for a halted CPU (`gbrt.c:5485`), the two PPU-skipping fast paths are gated
    behind `gbrt_benchmark_fast_tick_enabled` which is `false` (`gbrt.c:35`), so
    the normal path reaches `gb_sync` → `ppu_tick`. `ppu_ly` samples 35 / 95 / 69
    / 53 at rising budgets — it moves. The earlier "frozen at 21" claim was a
    single sample mistaken for a constant.
  - **VBlank is requested every frame.** `ppu.c:1669` does `ctx->io[0x0F] |= 0x01`
    on entering VBlank. `if=224` in a report means the request was already
    *consumed*, not that it never fired.
  - **The ISR runs every frame.** Seed `wVBlankCounter = 0` and read it back:
    114 frames → 112, 569 → 56, 1708 → 171, 5696 → 62, 23203 → 161. Every value
    is `frames mod 256` — it is a one-byte counter and it increments on *every*
    frame. Non-monotonic samples are wraparound, not a stalling interrupt.
  - So `WaitForVBlank` exits correctly each time, and the routine still runs
    23,000+ frames without completing. It is not blocked on frames: **nothing
    ever presses a button.** `Script_BeatAaron` runs `print_npc_text`, whose text
    box waits on edge-triggered `hKeysPressed`. Supplying a `keys` timeline moves
    `pc` off `0x0271` entirely (to `0xEF7D`) and drops the frame-wait count from
    153 to 14 — proof the wait loop was healthy and idle, not stuck.
  - The input run then lands in WRAM (`0xEF7D` is past `wMusicCh1StackBackup`),
    i.e. it executes garbage. A script *entry point* needs whole-scene ambient
    state that a probed per-routine call does not provide. That is the real
    blocker for this class — scene state and input, not frame simulation.
  **The reverted experiment.** Raising `IF` bit 0 at a synthetic 70224-cycle
  boundary whenever the CPU is halted with the LCD on was tried and reverted: it
  reddens four cases across `CreditsSequenceCmd_FadeIn` and `FadeScreenFromWhite`,
  because fade routines *count* frames and an off-cadence interrupt changes their
  output. Given the corrected findings above it was also solving a non-problem.
  Budget note for anyone re-measuring: `compare_one.py` kills the backend after
  **30 s**, which caps a probed call near ~1.6 B cycles (≈23,000 frames); a `keys`
  timeline costs extra wall time per frame and lowers that ceiling.
- **Triage recipe for this cluster, and its measured result.** These routines are
  unported, so `compare_one.py` cannot drive them (it resolves the native adapter
  first and exits `unknown routine`). Pipe a request JSON straight into
  `tools/oracle/gbref/build/gbref_runner --rom <ABSOLUTE>` instead — that is the
  whole CLI, everything else rides on stdin — and vary one thing at a time:
  `bare`, then `setup=[{fn=SetupText, d=0x30, e=0x7F}]`, then the same plus
  `keys=[0,1,0,1,...]`. Run against
  `DuelCheckMenu_OppPlayArea`/`_HandlePeekSelection`/`OpenGlossaryScreen`/`_DebugLookAtSprite`
  on 2026-08-26 this decomposed the "needs multi-frame VBlank" claim into four
  *different*, non-frame blockers:
  - All four hang bare at `Func_235e.asm_238a+2` (the glyph-cache linked-list
    spin) and **all four are moved past it by `SetupText` in `setup`**. Solved.
  - `DuelCheckMenu_OppPlayArea`: idle at `WaitForVBlank` until input, then
    advances to `CreateCardCollectionListWithDeckCards.deck_4+2` (`02:6405`) and
    spins over unseeded deck state → deck/card-list seeding, the `wCurDeckCards`
    family, i.e. case authoring.
  - `_HandlePeekSelection`: A presses change nothing (byte-identical pc and
    instruction count) → it waits on some other edge or flag; find the predicate.
  - `OpenGlossaryScreen`: now fully terminates with real ambient state:
    `SetupRegisters`, `SetupText(d=0x30,e=0x7F)`, `hWhoseTurn=$C2`, and input
    timeline `[release, SELECT, release, B]` (`[0,$04,0,$02]`). This toggles
    the glossary page, redraws it, and exits through the normal B path;
    `REFERENCE_OK` reaches the `$FEA0` sentinel in under one second. The old
    `$160B` `GetTurnDuelistVariable` loop was missing turn state, not a frame,
    text, or budget limitation. The routine is ordinary translation work now.
  - `_DebugLookAtSprite`: unbounded copy at `CopyDataHLtoDE_SaveRegisters` over an
    unseeded length, and adding `keys` makes it *crash* to `pc=0x0038` (RST 38 —
    no symbol means it is executing `$FF` filler). Do not drive this one with input.
  The lesson generalises: a park at `pc=0x0271` says only "idle", so vary setup and
  input before believing any stanza that blames frame simulation.
- **The cluster's first REFERENCE_OK, and what it took (2026-08-26).**
  `DuelCheckMenu_OppPlayArea` (`02:40da`) runs to the `0xFEA0` sentinel in
  2,291,409 instructions with exactly two case ingredients:
  `setup=[{fn=SetupText, d=0x30, e=0x7F}]` and `keys=[0x00, 0x02]`. Both details
  matter and neither is guessable:
  - **Press B, not A.** The menu tail is `cp MENU_CANCEL` / `ret z`, so B returns
    while A dispatches through `.jump_table` into the hand/discard sub-screens.
    An A-press probe therefore looks like an unrelated hang deep in
    `CreateCardCollectionListWithDeckCards` — that is the A path working, not a
    harness gap. `PAD_B = 1 << B_PAD_B = 0x02` (`hardware.inc:94-104`).
  - **The press must be a new edge.** `keys=[0x02]` held from frame 0 still
    `BUDGET_EXHAUSTED`s at `WaitForVBlank`, because `hKeysPressed` is
    edge-triggered; frame 0 must be `0x00`. `ram_enable` changes nothing.
  So a menu routine that parks at `WaitForVBlank` needs the *right button on the
  right frame*, not frame simulation and not SRAM/deck seeding.
- **`ready=true` is unreliable for indirect dispatch — measured, 7 routines.**
  `site/data/progress.json` builds its callee graph from direct `call`/`jp`, so a
  body that dispatches through `JumpToFunctionInTable` reports `ready=true` with
  `blockers=[]` while its `dw` targets are still `status=todo` and have no C body.
  A candidate issued for such a routine cannot compile a faithful port and must
  not stub the table. Of the 164 `ready`+no-blocker todo routines, **7 dispatch
  this way (1083 B)**: `_DebugLookAtSprite`, `_HandlePeekSelection`,
  `Preload_Clerk9`, `DuelCheckMenu_OppPlayArea`, `AIDoAction`, `Func_c141`,
  `_ExecuteGameEvent`. Three have confirmed unported targets —
  `DuelCheckMenu_OppPlayArea` → `OpenYourOrOppPlayAreaScreen_NonTurnHolder{PlayArea,Hand,DiscardPile}`,
  `Func_c141` → `Func_c9bc`/`Func_fcad`, `_ExecuteGameEvent` → the `GameEvent_*` set.
  (The scan only sees `dw` rows inside the routine's own body, so routines whose
  table sits elsewhere in the file — `_DebugLookAtSprite`, `_HandlePeekSelection` —
  are undercounted, not exonerated.) Check the `dw` targets by hand before
  trusting `ready` on any `JumpToFunctionInTable` user; P4's `OppActionTable` is
  the same pattern at 32 stanzas' scale.
- **The graph now follows `dw` jump tables (`tools/progress/inventory.py`,
  landed 2026-08-26), which finally names P4's real prerequisites.** Callee
  scanning used to see only direct `call`/`jp`, so a body dispatching through a
  pointer table reported `ready=true` with `blockers=[]` while its targets had no
  C body. A third inventory pass now attributes two table sources to a routine: a
  table under one of its own sub-labels, and a top-level table the routine *names*.
  A table that merely *follows* a routine is deliberately not attributed — that
  distinction is load-bearing, because `AnimationCommand_AnimScreen` is
  immediately followed by `AnimationCommandPointerTable`, which belongs to the
  dispatcher, and a naive "dw rows after the label" rule falsely blocks it.
  Effect: 42 routines gained real deps; `ready` went 159 → 154 with **zero**
  status, `code`, or `verified_functions` change — the five newly-blocked routines
  (`DuelCheckMenu_OppPlayArea`, `RunOverworldScript`, `HandleOverworldMode`,
  `Func_c141`, `_ExecuteGameEvent`) were all uncompilable-as-faithful already.
  The payoff is scoping the two big clusters:
  - **P4** — `AIMakeDecision` dispatches to **20** `OppAction_*` handlers, of which
    only **9 are unported, 291 B total**, and 6 of those are `ready=true` today
    (`OppAction_UseMetronomeAttack` 63 B, `OppAction_AttemptRetreat` 36 B,
    `OppAction_PlayEnergyCard` 32 B, `OppAction_PlayBasicPokemonCard` 31 B,
    `OppAction_EvolvePokemonCard` 27 B,
    `OppAction_ExecuteTrainerCardEffectCommands` 25 B). So the 31 stanzas that cite
    `AIMakeDecision` are gated on ~291 B of ordinary leaf ports, not on a dispatch
    rewrite; the reviewed transform is the *last* step, as P4 always specified.
  - **Script/overworld** — `RunOverworldScript` dispatches to **88**
    `ScriptCommand_*` handlers, **26 unported, 617 B**.
  Read these numbers off `site/data/inventory.json` (`functions.<Fn>.deps`), not
  off `blockers`, which `report.py` clears for anything already ported.
- **P5 and the whole indirect-dispatch class need ONE mechanism, and the expensive
  half of it already exists (measured 2026-08-26).** `TryExecuteEffectCommandFunction`
  (`effect_commands.asm:6`) is registered and `verified` with a stub body
  (`effect_commands.c:48-56`) that folds `CheckMatchingCommand`'s carry/`hl` into
  `a`/`f` and **never performs the `call CallHL`**. A faithful port needs to call an
  effect function identified only by a runtime address, and neither `CallHL` nor any
  address→function mapping exists in the tree. The same missing mechanism appears in
  **23 stanzas / 1,216 B** (19 of them `ready=True`), citing `CallHL`, `CallIndirect`,
  `CallBC`/`retbc`, `JumpToFunctionInTable`, `jp hl` or `rst $20` — including
  `RunOverworldScript`, which additionally gates 617 B of `ScriptCommand_*` handlers.
  Three measurements make this much cheaper than it looks:
  1. **Addresses are unambiguous.** 469 of the 470 ported effect functions have a
     symbol address, with **zero** `bank:addr` collisions *and* zero 16-bit address
     collisions across banks — so a plain `uint16_t` key identifies a target exactly.
  2. **The 155-signature problem is already solved.** Those 470 functions span 155
     distinct `(return, params)` shapes, which rules out a naive uniform function
     pointer — but `src/probe/effect_functions.c` already contains a uniform-signature
     shim for **all 470** (`static void adapt_<Fn>(ProbeState *s)`), all 470 registered
     in a name→adapter table. The register marshalling is written; only the *keying*
     (name, not address) and the *linkage* (`static`, probe-local) are wrong for
     runtime use.
  3. **The reference side is not the blocker for P5's dependents.** Both
     `EstimateDamage_*` routines run to completion — `REFERENCE_OK` after 2,623,510
     and 5,223,651 instructions — so their stanzas' "raise the budget" option only
     needs `instruction_budget ≥ 2.7M` / `≥ 5.3M`, with no card-ID investigation.
  So the build is: generate an address→shim table from the existing adapter set, give
  those shims external linkage, and implement `CallHL` on top. That is a real design
  decision rather than a port — it changes how ported code reaches ported code and it
  restructures a probe file all four fleet sessions depend on — so it wants explicit
  sign-off before anyone starts. Do not attempt a per-callsite `switch` instead: with
  470 possible targets keyed by ROM address, hand-written dispatch is how
  `AIMakeDecision`-class stub debt gets recreated at scale.

- **Sweep completed over all 90 `ready=True` stanza-blocked routines (2026-08-26).**
  37 of 84 probed returned `REFERENCE_OK`; only **6 stanzas** were deletable on that
  evidence, which is the ratio to expect. The rest hold for reasons a termination
  probe cannot see, and the recurring categories are worth knowing before probing:
  - **Former reserved-window blockers** — `TryAddCardToDeck`,
    `CreateCardSetList`, `PrintCurDeckNumberAndName`,
    `WriteCardListsTerminatorBytes`, and `CreateCurDeckUniqueCardList` were
    blocked while the PyBoy frame occupied `$CF30-$CFFF`. The frame moved to
    `$DC30-$DCFF` on 2026-08-26; their stanzas were deleted.
  - **Indirect trampolines** — `AIDoAction` (`JumpToFunctionInTable` with
    `DeckAIPointerTable`), `InitScreenAnimation` (`CallBC`/`retbc`),
    `HandleSelectUpAndDownInList` (`CallIndirect` on a WRAM function-pointer slot),
    `Func_1f96`, `EnterScript` (`jp hl`). A short `REFERENCE_OK` here usually means
    the *unseeded* pointer happened to reach the sentinel — `HandleSelectUpAndDownInList`
    "passes" in 11 instructions and `TryAddCardToDeck` in 7, i.e. they early-returned
    without doing their work. **Treat any `REFERENCE_OK` under ~100 instructions as
    an early-exit artifact, not a portability proof.**
  - **Stub-debt callees** — both `EstimateDamage_*` routines run fine (5.2M and 2.6M
    instructions) but wait on `TryExecuteEffectCommandFunction` (P5).
  - **Register threading** — `PrintPokemonCardWeight`, `LoadNPCForCreditsSequence`:
    the register-clobber debt class documented below, not termination.
  - **Genuinely expensive, not blocked** — `UnusedCopyrightScreen` needs
    `instruction_budget ≥ 5.4M`; `ScriptCommand_WalkPlayerToMasonLaboratory` ≥ 12M;
    `CreateCardSetList` 108,882; `EstimateDamage_VersusDefendingCard` 5.2M. Declare a
    big budget rather than assuming a harness gap.
  - **Tooling-only retirements** — a distinct and fully deletable class: the stanza's
    recorded failure is a *candidate* bug, not a project blocker. Exactly two exist,
    both `SurgeryError: cases module is not valid Python`:
    `UnusedCopyrightScreen` (deleted — `REFERENCE_OK` proven) and
    `PokemonTrader_TradeCardsEffect` (kept — it derails to `pc=0x0038`/RST 38 unseeded,
    so portability is unproven). When an `AUTO-RETIRED` note cites `failure_class=schema`
    or a Python syntax error, no capability gap was ever diagnosed there.

- **Sweep results, and why `REFERENCE_OK` is necessary but NOT sufficient to delete a
  stanza (2026-08-26).** Probing every `ready=True` stanza-blocked routine with
  `setup=[{fn: SetupText, …}]` is cheap (~2 s each) and 19 of the first 40 returned
  `REFERENCE_OK`. Deleting those 19 would have been a mistake: most of them block for
  reasons orthogonal to termination, and the reference terminating says nothing about
  them. Reading each stanza before acting found only **one** genuine contradiction:
  - `ScriptCommand_WalkPlayerToMasonLaboratory` — stanza claims an *unbounded*
    `DoFrameIfLCDEnabled` walk loop; measured **`REFERENCE_OK` after 11,559,566
    instructions**. It completes, just expensively, so it needs a case declaring a
    large `instruction_budget` (≥12M), not frame simulation. Stanza corrected.
  - Genuinely unaffected by termination: `EnterScript` (ends `jp hl` into
    `wNextScript`, a computed-jump trampoline that never returns to its caller — a
    short `REFERENCE_OK` just means the unseeded jump happened to reach the
    sentinel); `StartIRCommunications` (`di`, then `stop` for the CGB speed switch,
    then raw `rJOYP`/`rRP` IR hardware — no C equivalent); `PokeBall_AddToHandEffect`
    (mismatch is an RNG-derived byte at `$FFA0`, non-deterministic);
    `CanArenaCardUseNonResidualAttack` (two-call structure, already root-caused);
    `PrintVisibleDeckMachineEntries` (stack-sensitive SRAM loop);
    `WriteCardListsTerminatorBytes` and `CreateCurDeckUniqueCardList` (at the
    time, both overlapped the old PyBoy frame in `$CF30-$CFFF`; resolved by
    the `$DC30-$DCFF` relocation on 2026-08-26).
  So the sweep is a good *filter* — a `BUDGET_EXHAUSTED` result confirms a
  termination blocker and a `REFERENCE_OK` refutes one — but the stanza's own stated
  reason decides whether the routine is portable. Three stanzas were deleted this way
  on solid evidence (`Func_c268` pc=0x2385 → `REFERENCE_OK` 9,007 instr;
  `DrawCollectedMedals` pc=0x238D → 6,672 instr; `InitializeInputName`
  `REFERENCE_OK` in 155 instructions **bare**, its stanza having no basis at all).

- **A script ENTRY POINT is portable via a `pre-ret` split, and PyBoy's pre-ret
  hook was bank-blind until 2026-08-26.** `Script_BeatAaron`
  (`deck_machine_room.asm:62`) is 8 bytes of real code followed by `rst $20`
  script bytecode; `set_event_value` is `call SetStackEventValue` + `db <event>`,
  and the callee returns PAST the db, so the code ends exactly at the `rst`.
  Declaring `completion = {"mode": "pre-ret", "pc": <rst addr>}` verifies the whole
  code portion faithfully — no simplification, no scene state, no frame budget.
  Running past the `rst` needs ambient overworld state a probed call cannot supply.
  The harness gap this exposed: `pyboy_oracle.py::_arm` registered every hook as
  `hook_register(0, addr, …)`. PyBoy keys hooks on `(bank, address)`, and a hook in
  the switchable `$4000-$7FFF` window only fires while that bank is mapped — so a
  banked pre-ret pc **silently never fired** and the case died on the frame cap
  instead. Every pre-existing pre-ret case used a home-bank pc (`copy.py` 0x0731 /
  0x0744 / 0x073b, `setup.py` 0x0403), which is why it went unnoticed. `_arm` now
  takes a bank and the call site passes `0 if stop_pc < 0x4000 else fn_bank`.

- **`SetupText` in `setup` is the single highest-yield case ingredient, and it is
  routinely mistaken for a text-pipeline defect (measured 2026-08-26).** Without it
  the reference spins in `Func_235e`'s glyph cache around `pc=0x2380-0x238C`, which
  reads as "the text pipeline hangs on real card data" and has had stanzas written
  blaming `ProcessTextFromID` / `CountLinesOfTextFromID`. It is not those routines.
  Proven this session by adding only `setup=[{fn: SetupText, d: 0x30, e: 0x7F}]`:
  - `PrintFailedEffectText`'s two non-degenerate paths (`wEffectFailed` = 1 and 2 —
    the second loads real card data through `LoadCardDataToBuffer1_FromCardID` and
    `CopyCardNameAndLevel`) go from `BUDGET_EXHAUSTED` at `pc=0x2380` to **PASS**.
    Its landed cases had only ever seeded `wEffectFailed=0`, the early `ret z`, so
    the real-text path was documented as untestable when it simply lacked setup.
    Both cases are now registered.
  - `DisplayOpponentUsedAttackScreen` (`01:6635`, a P4 root): `BUDGET_EXHAUSTED` at
    `pc=0x238C` → **`REFERENCE_OK` in 16,582 instructions**.
  - `DisplayPCMenu`: `BUDGET_EXHAUSTED` at `pc=0x2381` → **`REFERENCE_OK` in 28,134
    instructions**. Both stanzas were deleted as resolved.
  **But do not over-apply it — there is a second, unrelated class.** The 26
  `AIPlay_*` stanzas cite the same text routines yet hang at `DoFrame`
  (`pc=0x0542`/`0x056E`/`0x0571`) or `CallIndirect` (`pc=0x05B7`), and adding
  `SetupText` changes *nothing* — byte-identical pc and instruction count. Those are
  genuinely frame-blocked and need the LCD-on/frame treatment, not setup. So when a
  stanza blames the text pipeline, resolve the reported `pc` against `poketcg.sym`
  first: `0x2380`-ish means `Func_235e` and `SetupText` fixes it; `0x05xx` means
  `DoFrame` and it does not.

- **Register-clobber debt is transitive, and `compare: ()` is where it hides
  (measured 2026-08-26).** A routine registered with a narrow `compare` was never
  checked on the registers it destroys, so its C body legitimately returns `void`.
  That is invisible until some *caller* needs those values, at which point the
  caller looks like a bad port when it is in fact faithful. `Func_1bb4`
  (`duel.asm:2214`) is the worked example: a straight call sequence whose reference
  returns `b=0x00 c=0x00 d=0xD8 f=0x80` while a faithful forwarding port returns its
  own arguments. Probing each callee alone with `compare=(a,f,b,c,d,e,hl)` through
  a throwaway `/tmp` case (registers nothing, costs seconds) gives the real effects:
  - `FinishQueuedAnimations` → `PORT` (`a`=0x01, `c`=0x00, `hl`=0xCAA0)
  - `DrawDuelMainScene` → `PORT` (`a`=0x01, `f`=0xC0, `hl`=0xC2F1)
  - `DrawDuelHUDs` → `PORT` (`f`=0x40, `b`=0x0B, `c`=0x04, `d`=0x07, `e`=0x00, `hl`=0xC3F0)
  - `WaitForWideTextBoxInput` → `PORT` (`f`=0x80, `b`=0x12, `c`=0x11, `d`=0x12, `e`=0x11, `hl`=0xCD12)
  - `PrintFailedEffectText` → `PASS`, already faithful on every register; its
    `compare: ("f",)` merely understates what it models.
  **Two things make "just widen the callees" more expensive than it sounds.** First
  it cascades: widening `FinishQueuedAnimations` needs *its* callees to carry
  registers, and `ZeroObjectPositions` and `BankswitchROM` return `void` and are not
  registered at all, so each widening pulls in a fresh subtree of ports. Second,
  isolated probes do not compose — `ExchangeRNG` alone with `wDuelType=0` returns
  `f=0x70` and `PASS`es, yet in `Func_1bb4`'s context the reference leaves `f=0x80`,
  because the clobbered inputs change what the tail computes. So do not use one
  callee's measured exit state to predict a caller's.
  Practical rule: on a b/c/d/e mismatch in a trivial call-sequence port, grep the
  callees for `compare: ()` before touching the caller, then decide deliberately
  between widening the subtree and a narrower caller contract justified by these
  measurements. Narrowing a contract until the oracle passes, without that
  evidence, is how `AIMakeDecision`-class stub debt was created.

- **The attack-animation command interpreter is ONE state machine, not 7 routines,
  and that is why its members deadlock (measured 2026-08-26).**
  `poketcg/src/engine/duel/animations/commands.asm` implements a command loop out
  of mutual tail-jumps: `PlayAttackAnimationCommands_NextCommand` (`asm:41`) is
  `ld a, [de]` / `inc de` / `ld hl, AnimationCommandPointerTable` /
  `jp JumpToFunctionInTable`, every handler tail-jumps back into it, and
  `AnimPlayArea`/`AnimPlayer`/`AnimOpponent` additionally `jr` straight into
  `AnimNormal`. Ported label-at-a-time this cannot converge, and the three stanzas
  involved each point at one of the others:
  - `AnimationCommand_AnimNormal` / `AnimScreen` say their remaining obstacle is
    that they tail-call `NextCommand`, whose landed C body is wrong. That is a
    **verification** block: the reference walks the real command chain while the C
    switches on its incoming `a`.
  - `PlayAttackAnimationCommands` asks for a reviewed transform of `NextCommand`.
    But writing the faithful dispatch needs all **7** table targets *defined* to
    link, and 5 are unported — a **compilation** block. 3 of those 5
    (`AnimPlayer` 19 B, `AnimOpponent` 25 B, `AnimPlayArea` 10 B) are blocked
    solely on `AnimNormal`.
  So neither side can move alone. The resolution is a **single co-port commit**, and
  the boundary is provably closed: the only routines the family reaches outside
  itself are `PlayDuelAnimation`, `UpdateDuelAnimationScreen` and `SwapTurn` (all
  `verified`) plus `JumpToFunctionInTable` (`excluded`), and `AnimEnd`/`AnimEnd2`
  are already ported. The unit is therefore exactly six routines, ~177 B plus the
  transform:
  `PlayAttackAnimationCommands_NextCommand` (8 B, **re-port** — it is registered
  and `verified` today with a wrong body, so this is stub debt, not a new port),
  `AnimationCommand_AnimNormal` (101 B, the hub),
  `AnimationCommand_AnimScreen` (22 B), `AnimationCommand_AnimOpponent` (25 B),
  `AnimationCommand_AnimPlayer` (19 B), `AnimationCommand_AnimPlayArea` (10 B).
  Natural C shape: one interpreter that reads the opcode from `de` and switches,
  with the handlers as functions that return to the loop rather than tail-calling
  it — the same "shared blocks become helpers" move that landed
  `ScriptCommand_JumpIfEventTrue`/`False`. The hBankROM knob those stanzas needed
  already exists and is behaviourally proven, so the harness is not the obstacle.
  Downstream payoff: this unblocks `PlayAttackAnimationCommands` (56 B) →
  `PlayAttackAnimation` → `PlayAttackAnimation_DealAttackDamageSimple` →
  `DealConfusionDamageToSelf` → `HandleConfusionDamageToSelf` →
  `OppAction_UseAttack`, i.e. it is on P4's critical path.

- **Dependency cycles: the 2026-08-26 escalation below is SUPERSEDED — most of it
  was tooling artefact, not mutual recursion.** Three later measurements shrank it
  from 62 routines / 3,866 B to **6 components / 46 routines / 2,599 B**, and the
  part a co-issuance policy would actually unblock is **175 B**, not 3,866:
  - **A phantom-fallthrough bug accounted for 3 components (14 routines, 1,233 B).**
    `inventory.py` judged fallthrough by the kind of a routine's *first* body line,
    so a routine ending in a data table (`tx`/`db`/`dw`/`assert_table_length`) still
    looked like code running into its neighbour. `GetPCPackNameTextID` is the
    worked example: it is a pure table lookup ending in `ret` followed by
    `.PCPackNameTextIDs`, yet it "depended on" `PrintPCPackName` purely because
    `assert_table_length NUM_MAILS` is not a terminator. Fixed by also requiring
    the *last* body line to classify as code; that freed **10 routines** into the
    frontier immediately, with no status/`verified_functions` change.
  - **One component was a sub-label false cycle and is now landed.**
    `ScriptCommand_JumpIfEventTrue`/`False` (34 B) — see the technique note below.
  - **Only 2 of the remaining components are self-contained**, i.e. every unported
    blocker lies inside the component: `GetPCPackNameTextID`/`PrintPCPackName`
    (69 B) and `DrawDeckNamingScreenBG`/`PrintDeckNameFromInput` (106 B) — and both
    were freed by the fallthrough fix anyway. The other 7 components are gated by
    outside unported work regardless of any issuance change (`GameLoop`/`Start`/`Reset`
    still waits on `_GameLoop`; the 19-routine duel-menu component waits on 12 more).
  So **cycle-aware issuance is no longer the top structural item** — it would buy
  175 B at most today. Before escalating a cycle again, re-measure with the edge
  classifier that skips `z`/`nz`/`c`/`nc` operands, and check whether the component
  is self-contained; a component gated from outside is ordinary dependency work.
  Historical record follows.
- **Mutual recursion permanently starves the frontier — 62 routines, 3,866 B,
  measured 2026-08-26 (SUPERSEDED, see above). This was reported as the single
  largest structural blocker needing a human decision on issuance policy.** `report.py` computes
  `ready = status == "todo" and not unported_blockers`. Two routines that call each
  other therefore each wait on the other forever: no member of a dependency cycle
  can ever be `ready`, so `factory-next` can never select one. Of the 62 trapped
  routines exactly **one** has ever been issued an attempt
  (`DuelCheckMenu_OppPlayArea`, and only while it was *falsely* ready before the
  `dw`-table fix above corrected it). A further **50 routines / 3,038 B** are
  directly gated by a cycle member, so **6,904 B — 15.4% of the remaining 44,879 B
  — is unreachable**, dwarfing P4's 291 B. The ten components:
  - **17 routines, 1187 B** (4 files): `OpenInPlayAreaScreen`, `DisplayPlayAreaScreen`, `SelectingBenchPokemonMenu`, `DuelCheckMenu_OppPlayArea`, +13 more
  - **19 routines, 679 B** (same file): `DuelMenu_Attack`, `DuelMenu_Retreat`, `PrintDuelMenuAndHandleInput`, `PlayEnergyCard`, +15 more
  - **10 routines, 1058 B** (same file): `HandleDeckBuildScreen`, `PrintConfirmationCardList`, `HandleSendDeckConfigurationMenu`, +7 more
  - **3 routines, 347 B** (same file): `DeckSelectionSubMenu`, `DeckSelectionSubMenu_SelectOrCancel`, `DeckSelectionMenu`
  - **3 routines, 162 B** (3 files): `GameLoop`, `Start`, `Reset` — the game's own entry point
  - **2 routines, 137 B**: `HandlePrinterMenu`, `PrinterMenu_PrintQuality`
  - **2 routines, 106 B**: `PrintDeckNameFromInput`, `DrawDeckNamingScreenBG`
  - **2 routines, 87 B**: `HandleDeckConfigurationMenu`, `ModifyDeckConfiguration`
  - **2 routines, 69 B**: `GetPCPackNameTextID`, `PrintPCPackName`
  - **2 routines, 34 B**: `ScriptCommand_JumpIfEventTrue`, `ScriptCommand_JumpIfEventFalse`
  Why it cannot be fixed by relaxing `ready` alone: C mutual recursion needs only
  forward *declarations* to compile, but it needs both *definitions* to link, so a
  candidate that ports one member while its peer has no C body cannot produce a
  green artifact. The cycle must be ported as a unit. The mechanism for that
  already exists — `packet.build_packets` groups ready routines **by file** into
  multi-routine chunks — and **8 of the 10 components are single-file (2,517 B),
  with 5 being mere pairs totalling 433 B**, so the small end is tractable today.
  Two decisions are required before touching this, because the change alters what
  every fleet session is issued: (a) readiness must become cycle-aware (ready when
  every unported blocker lies inside the routine's own component) *and* the
  component must be kept intact in one packet, which today's `max_routines` /
  `max_asm_lines` chunking would happily split; (b) the 19- and 17-routine
  components exceed any sane packet, so they need either a raised ceiling for
  cycle packets or a documented decision to hand-port them outside the loop.
  Start with the 433 B of pairs to prove the path before touching the big ones.
  **Important refinement: some of these are not real function-level recursion.**
  The inventory collapses a jump to `Target.sub_label` onto its parent `Target`, so
  two routines that merely jump into each other's *sub-labels* manufacture a cycle
  that does not exist between the function entries. `ScriptCommand_JumpIfEventTrue`
  / `ScriptCommand_JumpIfEventFalse` (34 B) is confirmed by direct reading to be
  exactly this: `True` does `jr z, ScriptCommand_JumpIfEventFalse.fail` and `False`
  does `jr z, ScriptCommand_JumpIfEventTrue.pass_try_jump`. Neither ever calls the
  other's entry point. Such a pair is **portable today with no factory change** —
  factor the two shared sub-label blocks (`.pass_try_jump`, `.fail`) into `static`
  helpers in the basename's `.c` and have both entries call them, which is what the
  asm structure already means. All six callees
  (`GetEventValue`, `SetScriptControlBytePass`, `GetScriptArgs2AfterPointer`,
  `SetScriptPointer`, `IncreaseScriptPointerBy4`, `SetScriptControlByteFail`)
  already exist in `src/home/scripting.h`.
  How much of the 3,866 B is this artifact is **not yet measured**: a quick
  classifier over intra-component edges is unreliable because `jr z, Target.sub`
  makes a naive "first identifier after the mnemonic" regex capture the condition
  token `z` rather than the target. Anyone continuing here should classify edges
  properly (skip the `z`/`nz`/`c`/`nc` operand) before assuming a component needs
  co-issuance at all — the real-recursion set may be much smaller than 10
  components, and `Reset`/`Start`/`GameLoop` (3 bare edges) is the clearest case of
  a genuine one.
- Arming does not help by itself. `runner.c` sets IE/IME when
  `input_events` is declared or `rLCDC & 0x80`, but with the LCD off the PPU
  publishes no frames, and the synthetic 70224-cycle boundary only advances the
  input timeline; it never raises the VBlank request. Declaring `input_events`
  on an LCD-off case changed nothing measurably (identical pc and instruction
  count).
- Not every hang in this cluster is a frame wait. `pc=3085` resolves to
  `Wait.loop` (`sgb.asm:258`), a busy delay of 1750 inner iterations times `bc`
  — a cycle-budget/parameter matter, fixed by seeding `bc` small or raising
  `instruction_budget`/`cycle_budget`, not by interrupts. Always resolve a
  reported `pc` against `poketcg.sym` before believing a stanza's mechanism, and
  note stanzas write it both as `"pc": 3085` and as prose `pc=0x51a4`.

Measured decomposition of the 51 (2026-08-26): only **13 stanzas / 1451 B**
actually name a frame routine in their `reason`; the other 38 matched on
`unblock` boilerplate and belong to other classes, mostly the `AIPlay_*` P4
cluster. Of the 13: 4 (139 B) enable the LCD themselves and genuinely need the
LCD-on work (`Func_c2a3`, `DeleteSaveDataForNewGame`,
`ScriptCommand_WalkPlayerToMasonLaboratory`, `StartIRCommunications`); 4 (276 B)
have a measured hang or an unbounded frame loop (`Duel_Init`, `SendPrinterPacket`,
`DebugDuelMode`, `ExecuteArbitraryNPCMovementFromStack` — whose cited pc is the
`Wait.loop` busy delay, so it is mis-attributed); and 5 (1036 B) name a frame
routine with **no recorded hang evidence at all** and are the retest candidates:
`_DebugLookAtSprite`, `OpenGlossaryScreen`, `DuelCheckMenu_OppPlayArea`,
`_PauseMenu_Config`, `PlayCreditsSequence`. Retest those five before building
anything; the LCD-on feature is worth roughly 400 B, not 3109 B.

Those five were then retested by driving the reference directly (pipe a request
into `tools/oracle/gbref/build/gbref_runner --rom ...`, which works on unported
routines because it never resolves a native adapter). All five still hang, so
none is stale — but three of them, plus `_HandlePeekSelection` from the group
above, stall at the *same* site: **`Func_235e`** (`process_text.asm:327`), at
`.asm_237d`/`.asm_238a`. That is **1182 B behind one routine**
(`_DebugLookAtSprite` 387, `_HandlePeekSelection` 350, `OpenGlossaryScreen` 319,
`DuelCheckMenu_OppPlayArea` 126), and it is not a frame wait at all.
`Func_235e` walks a linked list held in parallel WRAM pages — key1 at `$C6xx`,
key2 at `$C7xx`, next at `$C8xx`, prev at `$C9xx` — following `l <- next[l]`
until `key1[l]` is NULL. **The cause is a missing `setup` call, and the fix is
case authoring, not a harness feature.**

The glyph cache has a sentinel invariant: slot 0 must carry `key1[0] == 0`,
because the search loop (`Func_235e.asm_238a`) only ever stops on a NULL key,
while the *insert* loop (`Func_2325.asm_2337`) stops on `next[l] == 0`. New nodes
are allocated from a counter in `wcd04`, so real data never lands in slot 0.
`SetupText` (`process_text.asm:139-160`) establishes all of it: head
`hffa9 = 0`, `wcd04 = d - 1`, and a 256-byte clear of the key1 page
`$C600-$C6FF`. It does **not** touch the `next` page.

Enter one of these routines without running `SetupText` first and the very first
insert writes a real glyph pair into slot 0 with `next[0] = 0`, so the next
search spins on a one-element cycle. Measured at the hang: `hffa9 = 0`,
`key1[0] = 0x6F`, `next[0] = 0x00`. Adding
`setup: [{"fn": "SetupText", "d": 0x30, "e": 0x7F}]` fixes it — `OpenGlossaryScreen`
then shows `hffa9 = 0x65` with `key1[0] = 0` and walks past `Func_235e`
entirely, its hang relocating to `pc=0x1BD3`. So all four routines need
`SetupText` in `setup` and then a fresh diagnosis of whatever they hit next;
none of them is evidence for the VBlank feature.

**`bc == 0` on a 16-bit counted routine is not automatically excluded.** Use
`oracle: False` only when the actual path overwrites `$CF00-$CFFF` (or reaches
another documented dissolved execution context). Otherwise run the case against
the oracle. A C-only case still needs expectations derived from the asm that
prove its observable writes or register outputs.


For a configured private build, the equivalent iteration uses the cache:
`just oracle-diff-fast <Fn>`. Warm once with `just oracle-warm <Fn>` (or the
group warmer), require the mutation to go RED and restoration to return PASS,
then use the live routine/group command as the authority check.

## Mutation testing is mandatory

Five false greens have shipped in this repo, every one a routine whose only
effect was invisible to its cases: `GetPointerToTextHeader` (register-only
output hidden under `oracle:False`), the CGB textbox chain (attributes landed
in VRAM bank 1, cases only read bank 0), `LoadTxRam2`/`LoadTxRam3` (no case
read any memory the routine touched), `Func_22ca` (every field was
push/pop-preserved, so a broken body never showed), and
`TwoByteNumberToTxSymbol_PadSpace` (the adapter recomputed the answer instead
of marshalling it).

The check, for every routine, before it counts as done: **what happens if I
delete this body?** Apply one shape-preserving mutation — structure intact,
meaning corrupted (flip a comparison, drop a term, swap an operand) — run
`just oracle-diff <Fn>`, confirm it goes RED, restore the body, confirm PASS.
Record the mutation and the result. A routine whose cases cannot go red is
not done.

## Adapter rules

Enforced by `tools/lint_adapters.py` and the `quality` check in CI (`ci.yml`):

- **R1** — no integer literal `>= 0x8000` in an adapter body. `0x8000` is
  VRAM's origin; a marshalling layer has no business hardcoding an address in
  that range.
- **R3** — exactly one routine call per adapter. `pair`/`split` helpers that
  assemble or break down 16-bit register pairs are marshalling, not calls;
  casts and C keywords do not count either. An adapter calling more than one
  routine is reimplementing logic instead of marshalling it.

The allowlist in `tools/lint_adapters.py` is deliberately tiny. A stale entry
is itself a lint failure — do not add to it as a shortcut.

## Concurrency protocol

```sh
export POKETCG_BUILD=build-<slice>          # private build dir
export POKETCG_PORTS="<pret basenames>"     # semicolon list this slice owns
```

`CMakeLists.txt:34-60` restricts the build to `POKETCG_PORTS`. Agents working
concurrently never run `just oracle-release-gate` — a routine registered in
`tests/routines.py` without cases is a hard FAIL for everyone, so mid-flight
registrations would red the shared gate. Only the barrier, run centrally
after every slice lands, runs the full release gate.

## Exclusion taxonomy

A home-bank routine is legitimately unported for exactly one of five reasons.
Record the reason; never stub, never no-op-shim:

1. **SGB path**, dropped by Phase 1 (#2) — SGB packets and their senders.
2. **Deleted or dissolved by the Phase-1 transform** (`docs/phase1-transform.md`)
   — banking trampolines, HBlank gating, interrupts, DMA busy-waits, speed
   switching.
3. **Dead code** — zero callsites in `poketcg/src`.
4. **Tail dispatch into unported engine** — `jp hl` / `CallHL` /
   `JumpToFunctionInTable` whose targets are not yet ported. Becomes a C
   function-pointer table once the targets land, not before.
5. **Callee still unported** — the routine itself is portable but calls
   something that is not yet ported (e.g. `_PlaySFX`/`_PlaySong` in bank
   `$3d`, or an unported `engine/` routine).

## Fallthrough is a dependency

A label with no terminator (`ret`/`jp`/`jr` unconditional) before the next
label falls through into it and inherits its blockers. A call-graph sweep
that ignores fallthrough reports routines as ready when they are not.
Examples already hit in this repo: `StopMusic` → `PlaySong`,
`PlaySFX_InvalidChoice` → `PlaySFX`, `DrawPlayerPortrait` → `DrawPortrait`,
`LoadSymbolsFont` → `CopyFontsOrDuelGraphicsTiles`,
`SetCursorParametersForTextBox_Default` → `WaitForButtonAorB`.

## Indirect dispatch is invisible to the sweep

Reason 4 above has no static callee edge, so the call-graph sweep cannot see it:
`jp hl`, `call CallHL`, and `JumpToFunctionInTable` resolve at runtime. Those
routines are reported `ready=true` with `blockers=[]` in `site/data/progress.json`
while being unportable — the frontier would offer them as packets.

`.factory/blocked.toml` is the enforcement point. An entry there sets
`operational_blocker`, which makes the work record `state=blocked` and keeps
packet construction away. `AIDoAction` (indexes `DeckAIPointerTable`),
`RunOverworldScript` (`OverworldScriptTable`), `TryExecuteEffectCommandFunction`
(`CallHL` into `[wEffectFunctionsBank]`), and `_ExecuteGameEvent`
(`GameEventPointerTable`) are blocked this way. A `ready=true` routine that is
also `state=blocked` is correct, not a bug — do not remove the entry to make the
frontier look larger.

Writing an entry by hand is a write to a *derived-data input*, not just to a
ledger: `state=blocked` is recomputed into `site/data/progress.json`, so run
`python3 tools/progress/report.py build` and commit the refreshed `site/data/`
in the same `chore(factory):` commit. A blocker committed alone publishes a
snapshot that contradicts its own blocker file, and `report.py check` then fails
that push and every later one until somebody republishes. The
`enforce-derived-data.sh` PreToolUse guard blocks that commit for this reason.

## The four recurring traps

- **`ld a,[hl]` is a bus read**, resolved under the *caller's* bank via
  `gb_read8` — never `rom_ptr(BANK(Table), addr)` for a table the routine
  does not bank-switch for itself.
- **A wrong signature presents as a scatter of unrelated register
  mismatches** and reads like "unportable". Derive the exit registers from
  the asm tail before concluding a routine is blocked.
- **A `_b`-suffixed pret symbol is a distinct adjacent field**, not the high
  byte of a pair.
- **The oracle's synthesized call frame uses `$CFF0-$CFF5` for its hooked
  sentinel and `$DC30-$DCFF` for its stack** (`tools/oracle/pyboy_oracle.py`).
  Cases must not write either span; the former deck/card symbols through
  `$CFD2` are case-addressable.


## Verification is not just the oracle

A clean oracle diff is necessary, not sufficient. A port and its adapter can be
written to the same wrong assumption, and a `CONTRACT` that omits a field means
the oracle never compares it. Before closing a routine, re-derive its register
contract from the asm alone (without reading the C) and check:

- `CONTRACT` names every output and every preservation guarantee,
- the adapter hardcodes nothing,
- the cases actually drive every set bit of every derived expression — if a carry
  term is 0 in every case, deleting it still diffs clean.

## Definition of done

- `just oracle-diff <Fn>` prints `PASS`.
- A `CONTRACT` entry and the required coverage exist for every routine.
- No stubs, no `TODO`, no dead routines added, no changes outside the four files.

---

## Reference: the 19 leaf signatures

```c
void    CopyGfxData(uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c);
void    CopyDataHLtoDE(uint16_t *hl, uint16_t *de, uint16_t bc);
void    CopyDataHLtoDE_SaveRegisters(uint16_t hl, uint16_t de, uint16_t bc);
uint8_t ATimes10(uint8_t a);
typedef struct { uint16_t quotient, remainder; } DivResult;
DivResult DivideBCbyDE(uint16_t bc, uint16_t de);
void    SetListPointer(uint16_t de);
void    SetNextElementOfList(uint8_t a);
void    DecompressDataFromBank(uint16_t bc, uint16_t de);
void    CopyBankedDataToDE(uint16_t bc, uint16_t de);
void    FillMemoryWithA(uint16_t hl, uint16_t bc, uint8_t a);
void    FillMemoryWithDE(uint16_t hl, uint16_t bc, uint8_t d, uint8_t e);
uint8_t GetFarByte(uint8_t bank, uint16_t addr);
uint16_t HtimesL(uint16_t hl);
uint8_t  Random(uint8_t a);
uint8_t  UpdateRNGSources(void);
void    InitDataDecompression(uint16_t de, uint8_t b);
void    DecompressData(uint16_t bc, uint16_t de);
uint8_t DecompressData_Decompress(void);
void    TwoByteNumberToText(uint16_t hl, uint16_t *de);
```

## Reference: leaf-slice resolutions

Decisions made for these 19; carry the principle, not the letter, into later phases.

- `GetFarByte`'s `ld hl,sp+$05` / `sp+$03` (`memory.asm:75,80`) patches its own
  saved register frame to return a value. In C it is a banked **bus** read
  (`gb_read8` under the switched bank, restored after), not `*rom_ptr` —
  addresses at or above `$8000` reach RAM. `hl`, `bc`, `de`, the caller's flags
  and `hBankROM` are all preserved.
- `DivideBCbyDE`: divisor 0 yields quotient `0xFFFF`, remainder = dividend.
  Bug-compatibility, not a defect. The `ldh [hffb6]` scratch counter has no
  reader; use a local.
- `CopyGfxData`'s hblank path matches `.next_tile` for every `c != 0` but
  **diverges at `c == 0`** (measured). The port takes `.next_tile` unconditionally.
- `DecompressData` is a **streaming** API (`sgb.asm:295-298`,
  `overworld.asm:509-525` decompress one strided row at a time against persistent
  `wDecomp*` state). Do not collapse it into a one-shot decompressor.
- `ATimes10` truncates to 8 bits at every intermediate add: `26 -> 4`.
- Not ported (dead code, zero callsites): `HLTimes10`, `ADividedBy10`,
  `GetNextElementOfList`, the five `Write*Number` display routines,
  `WriteBCDNumberInTextFormat`, `WriteBCDDigitInTextFormat`. Trampolines
  (`JumpToFunctionInTable`, `CallIndirect`, `CallHL`, `CallHL2`, `CallBC`) become
  direct C function-pointer calls at their callsites.
- `SetListToNextPosition` is exported but not callable (pops words its fallthrough
  callers pushed); its two-byte writeback is inlined into `SetNextElementOfList`.
