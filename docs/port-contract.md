# Port contract

This page owns routine translation, memory, ABI, observation strength, and mutation proof. The [factory contract](factory-contract.md) owns quartet/output structure and schema derivation. The [maintenance workflow](grind.md) owns diagnosis, verification, and publication.

## Ownership and addresses

Work within the basename's quartet defined by the factory contract. Do not hand-edit shared infrastructure, derived `tests/routines.py`, or derived `SCHEMA2_CASES`.

| Access | Rule |
|---|---|
| Game memory | Use `gb_read8(uint16_t)` and `gb_write8(uint16_t, uint8_t)`. Writes below `$8000` are dropped. |
| Caller-bank ROM reads | An instruction such as `ld a,[hl]` uses `gb_read8(hl)`. |
| Deliberate direct banked ROM | Use `rom_ptr(bank, addr)` only for intentionally mapped ROM access. |
| Memory-walking interfaces | Pass and return 16-bit Game Boy addresses, not host pointers; preserve wraparound. |
| Advanced `hl`/`de` | Expose the resulting address through a `uint16_t *` in/out argument when callers observe it. |
| Named memory | Use generated layout symbols. A `_b` symbol is an adjacent byte, not a pair's high byte. |

`farcall` and `bank1call` resolve to ordinary C calls. Use the existing constants tooling for assembly-named constants; do not invent their values.

## Registers, flags, and counts

Derive inputs from registers read before write, outputs from values meaningful to callers at return, and preservation from assembly push/pop behavior. Exclude incidental loop residue.

| Contract field | Meaning |
|---|---|
| `compare` | Every meaningful output and every preserved register. |
| `preserve` | The unchanged subset of `compare`. |

Carry is an output only when produced for callers. A return path restoring `af` preserves entry carry; `DivideBCbyDE` also preserves its entry carry. Flag bits are Z=`0x80`, N=`0x40`, H=`0x20`, C=`0x10`; the low nibble is zero.

Counted loops are post-test. Expand their iteration count without narrowing it:

| Counter | Meaning of zero |
|---|---|
| 8-bit | 256 iterations |
| 16-bit | 65,536 iterations |
| `FillMemoryWithDE` `bc` | 65,536 pairs |
| `CopyGfxData` byte/block counters | Each independent 8-bit counter means 256 |

## Probes and completion

Adapters marshal inputs, call the routine, and marshal its real outputs. They do not implement logic or manufacture results. Leave preserved registers untouched.

Entry-completion snapshots retain the callee's current ROM bank. Ordinary returns and frame-budget exits restore saved bank guards.

`_completion` on a loaded case is inspection/readback state. Author a cutpoint through the [factory completion hook](factory-contract.md#cases-and-mutation-declarations), not by assigning an ignored legacy key. An entry completion executes only code before the named entry; it cannot prove behavior below that boundary.

## Case-key reference

Use `tests/cases/_symbols.py`: `sym()` for addresses, `data()` for values numerically in RAM ranges, and harness constants for reserved frame/stack locations. Unknown symbols fail resolution.

| Input | Shape and role |
|---|---|
| `a f b c d e hl` | Initial registers. |
| `wram` | Seed-and-observe WRAM/HRAM spans. |
| `read` | Observe-only live bus spans. |
| `sram` | Banked seed-and-observe SRAM spans. |
| `sread`, `vread` | Observe-only banked SRAM/VRAM spans. |
| `vram` in schema-2/gbref | Banked seeds with their seeded lengths observed; the older PyBoy call interface lacks the equivalent seed argument. |
| `ramg` | SRAM enable-latch override applied after seeding. |
| `setup` | Ordered warm-state calls after seeding, without resetting RAM between preludes. |
| `keys` | Held integer or cycling poll timeline, up to 16 values. |
| `entry_sp` | Synthesized entry stack pointer. |
| `stack` | At most four 16-bit caller-pushed words below the return address. Index zero is pushed first; the last word is popped first. |
| `post_call_byte` | Independent 0..255 inline operand immediately after the synthesized CALL. It is not a stack word or `hl`. |

Spans are compared at their declared lengths. The observed bus includes seeded WRAM/HRAM, explicit live/banked reads, and seeded SRAM/VRAM; register observation comes from `CONTRACT.compare`. State outside those observations is invisible.

### SRAM latch

Seeding SRAM enables its latch as a side effect. Apply `ramg` afterward when testing enable/disable behavior. Direct banked SRAM reads bypass that latch, so latch-sensitive cases must observe the live enabled/disabled bus behavior instead.

### Input edges

Input bits 0 through 7 are A, B, SELECT, START, RIGHT, LEFT, UP, and DOWN. `ReadJoypad` polls advance the timeline; setup polls are excluded. Other direct JOYP reads and the physical pad state see entry zero.

A held scalar supplies the initial press edge. Repeated waits needing another press require release/press cycling.

### C-only expectations

Oracle-backed `expect` is inert. A C-only case declares `oracle: False`, a nonempty `why`, and at least one explicit assembly-derived expectation family: `expect`, `expect_regs`, `expect_sram`, or `expect_vram`.

Seeded bytes and requested bank reads are not automatically compared in C-only mode. Expectations must establish the claimed behavior themselves.

### Reserved memory

Never seed or write call-frame `$CFF0-$CFF5` or stack `$DC30-$DCFF`. Use the supplied harness constants rather than raw addresses.

## Required case strength

Each routine needs:

- An all-zero case and poisoned-register preservation case.
- Relevant count boundaries, including zero, one, and 256/257 where applicable.
- Cases for every meaningful internal path and observations for every claimed behavior.
- Observed output spans for memory writes; register comparisons alone do not prove memory correctness.
- Inputs that activate terms in derived expressions and dispatch branches rather than repeatedly taking one early exit.

Branch-label count is a screening heuristic, not path-coverage proof.

## Mutation evidence

Require a passing baseline, a behavioral mismatch/RED under the mutation, and a passing restored implementation. Harness failures do not count as RED. Retain the RED receipt and repeat the execution proof after re-anchoring.

The `before` substring must be unique within its `source_symbol` factory block. When the block is absent or the anchor is outside it, the resolver requires a unique whole-file fallback match.

## Exclusions and dispatch

A home routine can remain unported only for a documented reason:

- SGB-only behavior.
- Deleted or dissolved Phase 1 hardware plumbing.
- Dead code with no source callsites.
- Runtime tail dispatch into unported engine code.
- An unported callee.

Do not add stubs or no-op shims. The [bounded hardware-disposition record](phase1-transform.md) owns the original transform results.

Fallthrough is a dependency: a label without an unconditional terminator inherits the following label's blockers. Static call graphs do not see `jp hl`, `CallHL`, or table dispatch. Keep those targets blocked until their implementations and C dispatch table are present. A static report saying ready does not remove an operational blocker.

