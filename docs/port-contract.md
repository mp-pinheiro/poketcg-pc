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

**Reserved WRAM: `$CF00-$CFFF`.** That window holds the oracle's synthesized
call frame; the oracle raises if a case writes into it. Use `$C100-$CA00` for
buffers, or the real pret WRAM symbol when the routine has one.

That window is not free real estate: 24 live symbols resolve inside it
(`wCurDeckCards` `$CF17`, `wCurDeckName` `$CFB9`, `wMaxNumCardsAllowed` `$CFD1`,
`wNamingScreenBufferLength` `$CFFF`, ...), so every routine that touches deck or
naming state is currently unobservable and ten `.factory/blocked.toml` stanzas
cite it. Relocating the frame was measured on 2026-08-26 and is viable but not
free, so record what it costs before trying again:

- Only the PyBoy backend parks a frame there. The GBRT runner enters with
  `ctx->sp = 0xfffe` and sentinel `0xfea0` (`tools/oracle/gbref/runner.c:589`),
  both outside WRAM, so `state_exclusions.toml`'s `GBRT/native call-frame
  scratch` label is inaccurate — moving PyBoy's frame alone does free the window.
- The destination is already known: `src/wram.asm` leaves a bare `ds $6e4`
  between `wd698` (`$D698`) and the WRAM Audio section (`$DD80`), so
  `$D69C-$DD7F` carries no game symbol, and no existing case references
  `$DC00-$DCFF`.
- What blocks it is wide-sweep WRAM comparisons tuned to the *old* hole. Cases
  that assert "nothing else in WRAM changed" read `$C100+3584` and `$D000+4096`
  — every byte except `$CF00-$CFFF`. Moving the frame to `$DC00` landed it
  inside their second span and reddened seven registered routines:
  `DetectConsole`, `FlamesOfRage_AIEffect`, `ApplyRandomCountToNPCAnim`,
  `Func_0bcb`, `UpdateNPCAnimation`, `CometPunch_AIEffect`,
  `UpdateArenaCardIDsAndClearTwoTurnDuelVars`.
- So relocating *within* WRAM is not a fix on its own: it also needs those seven
  routines' sweep spans re-cut around the new window, in the same commit that
  moves `RESERVED` in both `tools/oracle/pyboy_oracle.py` and
  `tools/factory/verify.py`.
- Leaving WRAM does not help either. HRAM is the only region outside WRAM with
  room (game symbols stop at `hffb7`, so `$FFB8-$FFFE` is unallocated and
  executable), but cases already observe `$FFED`, `$FFEF`, `$FFFC`, `$FFFE`, and
  `$FFFF` is the IE register. There is no free 256-byte window anywhere.
- `tools/oracle/state_exclusions.toml` has NO consumer in `tools/` or `tests/`.
  Nothing reads it, so editing it changes nothing; the compare spans come from
  each case's own seeds (`tests/test_leaves.py:123` derives reads from the seed
  map). Treat that file as documentation until something consumes it.

The reservation, not the placement, is the real over-reach. The frame occupies
three bytes — one NOP at `SENTINEL`, two for the `jr -2` at `SPIN` — plus
however deep the routine under test drives the stack down from `STACK_TOP`
(`$CFC0`). Reserving 256 bytes buys stack headroom, and it is that headroom, not
the frame, that hides `wCurDeckCards` `$CF17` and the `$CF68` list symbols the
stanzas actually need.

So the cheap unblock is to shrink `RESERVED` from below rather than move it, and
how far is now measured rather than guessed. Seed a pattern across the window,
run a routine through the PyBoy oracle, and read it back; the lowest clobbered
byte is the stack's low-water mark. Measured 2026-08-26 over the 31 largest
registered routines: the deepest is **86 bytes** below the entry SP (`$CFBE`),
reaching **`$CF68`**, in `_AIProcessHandTrainerCards`. Text rendering is much
shallower — 46 bytes for `DrawNarrowTextBox_PrintTextNoDelay`, 34 for
`PrintTextNoDelay`.

Two consequences. The floor at `$CF30` tolerates 143 bytes, so it clears the
measured worst case by 57 bytes and is safe. And raising it much further is not
available: a floor of `$CF69` would tolerate only 85 bytes, under the measured
86. The low-water mark lands exactly on `wUniqueDeckCardList` /
`wOwnedCardsCountList` (`$CF68`), which is why the deck-*list* routines cannot be
unblocked by shrinking at all — the stack genuinely reaches their buffer. Those
need the frame relocated; only routines whose data terminates below `$CF30`
benefit from the floor.

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
- With the LCD **on** the path is genuinely unavailable. `CASES["DoFrame"]`'s
  third case seeds `0xFF40: 0x80` and is `oracle: False` with the reason "LCD-on
  DoFrame reaches the dissolved VBlank boundary". That is the real gap: a
  routine needing actual frame *progress* — an animation or NPC movement
  completing, printer timing — cannot be oracle-run.
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
- **The oracle's synthesized call frame occupies `$CF00-$CFFF`**
  (`tools/oracle/pyboy_oracle.py:33-38`). Cases must not write it.


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
