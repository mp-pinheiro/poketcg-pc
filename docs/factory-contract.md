# Factory translation contract

You translate Game Boy assembly routines from pret/poketcg into C11 for the
poketcg-pc port. Your output is verified byte-for-byte against the real ROM
running in an emulator, then mutation-tested. Follow this contract exactly;
the completed example in the prompt shows every convention working.

## Memory model

All game state lives behind a bus. Never take host pointers into it.

```c
uint8_t  gb_read8(uint16_t addr);            /* any bus read  */
void     gb_write8(uint16_t addr, uint8_t v);/* writes below $8000 are dropped */
const uint8_t *rom_ptr(uint8_t bank, uint16_t addr);
void     BankswitchROM(uint8_t bank);        /* home/switch_rom.h */
```

- Named RAM locations come from generated headers (`generated/wram.h`,
  `generated/hram.h`, `generated/sram.h`, included by the file skeleton).
  Every pret symbol `wFoo`/`hFoo` yields `wFoo` (a `uint8_t` lvalue you can
  read/assign), `wFoo_ADDR` (its numeric address), and `wFoo_PTR`.
  Use the lvalue for single-byte access, `_ADDR` for address arithmetic.
- **Representation rule:** routines that walk memory take and return
  `uint16_t` Game Boy addresses, never host pointers. A pointer the asm
  advances (`hl`/`de` past a copied block) becomes a `uint16_t *` in/out
  parameter — callers read the advanced value. 16-bit wraparound must be
  exact: do arithmetic in `uint16_t`.

## The three C rules

1. **Zero means maximum.** Counted loops are post-test: a 16-bit count of 0
   means 65536, an 8-bit count of 0 means 256. Encode as
   `uint32_t n = n_raw ? n_raw : 0x10000u;` (or `0x100u`).
2. **Advanced pointers are load-bearing.** If the asm leaves `hl`/`de`
   advanced past what it processed, write the advanced address back through a
   `uint16_t *` parameter.
3. **Carry is only sometimes an output.** Model flags (`f`) as an output only
   when the asm contract really produces them (`scf`/`or a` before `ret`, a
   comparison result callers branch on). A routine ending in `pop af`
   restores the CALLER's flags — then `f` is preserved, not produced.
   Flag bit layout: Z=0x80, N=0x40, H=0x20, C=0x10; the low nibble is always 0.

## Signatures

- Inputs = the registers the asm reads before writing; outputs = registers
  meaningful to callers at `ret`. Multiple outputs use a small returned
  struct (see the example). Preserved registers (push/pop pairs) are neither.
- `ld a,[hl]` under a bank the routine did NOT switch itself is a **bus
  read**: `gb_read8(hl)` — never `rom_ptr` for a table the caller banked.
- `farcall`/`bank1call` become plain C calls to the named routine.
- A wrong signature shows up as a scatter of unrelated register mismatches
  in the diff. Re-derive the exit registers from the asm tail before
  changing logic.
- A `_b`-suffixed pret symbol is a distinct adjacent byte field, not the
  high byte of a 16-bit pair.

## Probe adapter (===PROBE block)

`ProbeState` is `{ uint8_t a, f, b, c, d, e; uint16_t hl; }`.

```c
static void adapt_Foo(ProbeState *s)
{
    uint16_t de = (uint16_t)(s->d << 8 | s->e);
    Foo(&s->hl, &de, (uint16_t)(s->b << 8 | s->c));
    s->d = (uint8_t)(de >> 8);
    s->e = (uint8_t)de;
}
```

Hard rules (CI-linted):
- Marshal only. Exactly ONE routine call. Never recompute or hardcode an
  answer; never write a register the routine does not produce.
- A register the asm preserves must be left untouched by the adapter.
- No integer literal >= 0x8000 in the adapter body.
- Name it `adapt_<RoutineName>` with `.` replaced by `_`.

## Cases (===CASES block)

Two statements, exactly:

```python
CONTRACT["Foo"] = {"compare": ("a", "f", "hl"), "preserve": ("b", "c")}
CASES["Foo"] = [
    {"wram": {0xC100: b"\x00\x00"}, "read": {0xC200: 2}},
    dict(POISON, wram={0xC100: b"\x01\x02"}),
    {"b": 1, "c": 0, "wram": {0xC100: b"\xFF"}},
]
```

- `compare` = registers the diff checks (real outputs + everything the asm
  preserves). `preserve` = the subset the routine must not change. Leave
  incidental loop residue (`bc==0` after a counted loop) OUT of compare.
- Case keys: `a f b c d e hl` (entry registers, default 0); `wram`
  `{addr: bytes}` seeded AND diffed; `read` `{addr: count}` diffed only;
  `sram` `{bank: {addr: bytes}}` seeded+diffed; `sread`/`vread`
  `{bank: {addr: count}}` diffed only (vread for VRAM, banks 0/1); `ramg`
  bool (SRAM enable latch state); `setup` `[{"fn": "SetupText", "d": 0x20}]`
  preludes for warm state; `keys` int (held buttons, bit0 A, 1 B, 2 SELECT,
  3 START, 4 RIGHT, 5 LEFT, 6 UP, 7 DOWN — required for input-waiting
  routines, which otherwise spin forever).
- Required coverage per routine:
  1. an all-zero case;
  2. a poisoned case — `dict(POISON, ...)` overriding only consumed fields —
     proving every preservation claim;
  3. every boundary: count 0 (must act as maximum, never no-op), 1, and
     256/257 for 16-bit counters.
- **Python case files use NUMERIC addresses only.** The C `_ADDR` macros do
  not exist in Python. The prompt lists every RAM symbol's address; define
  module-level constants (`wFoo = 0xCCED`) inside your CASES block if it
  helps readability.
- **Reserved WRAM $CF00-$CFFF** belongs to the oracle's call frame: never
  seed or write it. Use $C100-$CA00 for scratch buffers, or the routine's
  real pret symbols.
- A case the live oracle physically cannot run uses `"oracle": False` plus
  `"why": "..."` plus asm-derived `"expect": {addr: bytes}` /
  `"expect_regs": {...}` — derived from the asm, never guessed.

## Mutation (===MUTATION block)

One statement declaring a shape-preserving corruption of YOUR C that the
cases must catch:

```python
MUTATIONS["Foo"] = {
    "source_symbol": "Foo",
    "before": "if (flags & 0x10u)",     # exact substring of the C file,
    "after": "if (flags & 0x20u)",      # occurring exactly once
    "case_ids": ["Foo-0", "Foo-1"],     # cases that go RED under it
}
```

Pick a mutation that changes observable behavior (flip a comparison, wrong
constant, dropped term). If no case can catch a corruption of some line,
you are missing a case — add it.

## Output discipline

- C body only inside your blocks; the file skeleton (includes, header
  guard, probe table, POISON, schema tail) already exists.
- Local constants: `#define NAME 0x..u` lines at the top of the ===STATICS
  block, with values from the prompt's constant table.
- Extra headers (`#include "home/x.h"` for callees) also go at the top of
  ===STATICS. NEVER invent include paths: the only valid quoted includes are
  `home/<basename>.h` for callees named in the prompt, `generated/wram.h`,
  `generated/hram.h`, `generated/sram.h`, and `mem.h` — there are no
  constants headers; `#define` constants locally from the prompt's table.
- Comment each function with its pret source range:
  `/* foo.asm:12-34 */`.
- Tabs for C indentation, `u` suffix on unsigned literals, no TODOs, no
  placeholders, no dead code.
