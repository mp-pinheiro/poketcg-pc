# Porting guide & contract

How to port a pret/poketcg routine to C and prove it byte-equivalent against the
PyBoy oracle. Read in full before writing any C. The 19 `home/` leaf routines
already follow this; every later phase should too.

## The loop

```sh
just bootstrap                 # one-time: builds poketcg.gbc + poketcg.sym
just oracle-venv               # one-time: PyBoy into /tmp/pbenv
just oracle-diff <PretSymbol>  # configures, builds, diffs C vs PyBoy
just oracle-diff-all           # all routines; exits non-zero on any failure
```

`just oracle-diff` runs cmake+ninja itself. Iterate until `PASS`. When porting
concurrently with other agents, build in a private directory over a private file
subset so neither ninja state nor someone else's in-flight compile error touches
you:

```sh
export POKETCG_BUILD=build-<file>      # private build dir
export POKETCG_PORTS=<file>            # semicolon-list of pret basenames to compile
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

`ProbeState` is `{ uint8_t a, f, b, c, d, e; uint16_t hl; }`. Two hard rules:

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
CONTRACT = {"Foo": ("a", "b", "c", "d", "e", "hl")}   # fields the diff compares
CASES = {"Foo": [ {...}, {...} ]}
```

`CONTRACT` names exactly the registers the asm contract makes meaningful: real
outputs plus every register the asm claims to preserve. Leave out loop residue
(`a==0` after a `ld a,c / or b` exit, `bc==0` after a counted loop) — it is not
part of the callable contract and forcing it would push a hardcoded value into
the adapter. Flag-preservation guarantees belong in `CONTRACT` only when every
instruction on the path is flag-neutral; seed `f=0xF0` (the low nibble is always
0 on hardware, and both probe and oracle mask it).

Case dict keys:

- `a f b c d e hl` — entry registers, default 0.
- `wram` — `{addr: bytes}` seeded before the call **and** diffed after.
- `read` — `{addr: count}` diffed after the call without seeding.
- `oracle: False` + `why: "..."` + `expect: {addr: bytes}` — for a boundary the
  oracle physically cannot run; diffed against the C alone using values derived
  from the asm.

Required coverage per routine:

1. an all-zero case,
2. a poisoned-register case
   (`a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234`, overriding only
   the fields the routine consumes) proving every preservation claim,
3. every boundary — `n=0` for counted routines (must behave as maximum, never a
   no-op), plus counts of 1 and 256/257. 256/257 is where a port that decrements
   only the low byte breaks.

**Reserved WRAM: `$CE00-$CFFF`.** That window holds the oracle's synthesized call
frame; the oracle raises if a case writes into it. Use `$C100-$CA00` for buffers,
or the real pret WRAM symbol when the routine has one.

**`bc == 0` on a 16-bit counted routine is not oracle-testable:** 65536 bytes
overwrites the whole address space including the call frame, on real hardware as
much as here. Use the `oracle: False` form, with `why` stating that, and an
`expect` map derived from the asm that proves the routine wrote far more than zero
bytes.

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
