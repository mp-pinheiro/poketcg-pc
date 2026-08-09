# Pokétcg sprite-animation Phase 2 execution plan

## Context

Start from committed revision `b3a37679`, with a clean working copy and the
central **480/480** gate recorded in `docs/vision.md` and `docs/plan.md`. The
current `tests/routines.py` parses to exactly 480 registered names and contains
no `sprite_animations` tuple. The failed Wave 2 draft was removed completely;
none of its C, adapter, case, or contract choices are reusable evidence.

Port exactly the 22 global labels in
`poketcg/src/engine/gfx/sprite_animations.asm`, in source order:

1. `_ClearSpriteAnimations`
2. `CreateSpriteAndAnimBufferEntry`
3. `FillNewSpriteAnimBufferEntry`
4. `DisableCurSpriteAnim`
5. `DisableSpriteAnim`
6. `GetSpriteAnimCounter`
7. `_HandleAllSpriteAnimations`
8. `LoadSpriteDataForAnimationFrame`
9. `TryHandleSpriteAnimationFrame`
10. `StartNewSpriteAnimation`
11. `StartSpriteAnimation`
12. `Func_12ac9`
13. `LoadSpriteAnimPointers`
14. `HandleAnimationFrame`
15. `GetAnimFramePointerFromOffset`
16. `SetAnimationCounterAndLoop`
17. `Func_12ba7`
18. `Func_12bcd`
19. `ClearSpriteVRAMBuffer`
20. `Func_12c05`
21. `Func_12c4f`
22. `Func_12c5e`

The arithmetic target is fixed: `480 + 22 = 502`. All 22 labels are callable
and none is excluded. The dependency routines are landed, but one latent helper
bug must be repaired in the same wave: `GetFirstSpriteAnimBufferProperty`
currently hardcodes slot 0 instead of reading `wWhichSprite`. All other direct
dependencies are already available from `load_animation`, `load_gfx`,
`objects`, `copy`, `memory`, `switch_rom`, and `switch_sram`.
`sprites.asm`, `tilemaps.asm`, and `tilesets.asm` are ROM data, not additional
C-port basenames.

Owned implementation paths are:

- `src/home/sprite_animations.c`
- `src/home/sprite_animations.h`
- `src/probe/sprite_animations.c`
- `tests/cases/sprite_animations.py`
- only `ROUTINES["sprite_animations"]` in `tests/routines.py`

The prerequisite helper repair owns only:

- `src/home/load_animation.c`
- `tests/cases/load_animation.py`

`CMakeLists.txt` already globs the home and probe sources. Do not edit it. Apart
from the two prerequisite helper paths, do not edit callers, existing port
basenames, shared memory/probe code, generated headers, ROM-data-only ASM, or
any neighbouring registry tuple.

## Approach

After one clean-baseline check, fan out four workers in one batch. The helper
semantics, ABI, and case contracts in this plan are the shared contract; workers
do not invent a second convention.

| worker | exclusive paths | deliverable |
|---|---|---|
| helper repair | `src/home/load_animation.c`, `tests/cases/load_animation.py` | call `GetSpriteAnimBufferProperty(0)` and add slot `0/15/16/255` oracle witnesses |
| implementation | `src/home/sprite_animations.c`, `src/home/sprite_animations.h` | all 22 bodies and public types/prototypes |
| adapter | `src/probe/sprite_animations.c` | literal one-call marshalling for all 22 symbols |
| oracle matrix | `tests/cases/sprite_animations.py`, `ROUTINES["sprite_animations"]` only | exact contracts, explicit cases, 22-name registry tuple |

The four slices are file-disjoint and may run concurrently. They must not run
formatters, builds, oracle diffs, project-wide tests, or commits. The
orchestrator reviews and integrates all four results, fixes cross-slice
compile/contract mismatches centrally, and performs every validation command.
If one slice fails, re-dispatch only that failed ownership set with the concrete
failure evidence; do not restart successful slices.

Use one private integration directory:

```sh
export POKETCG_BUILD=build-gfx-sprites
export POKETCG_PORTS=""
```

An empty port filter is intentional: this basename calls landed helpers across
multiple pret files. Only the orchestrator runs `just oracle-diff-all`.

### ABI and exact adapter contract

Use a result type only for the cache lookup, whose caller-visible result is the
complete `AF` pair:

```c
typedef struct { uint8_t a, f; } SpriteAnimLookupResult;
```

The header declarations and `CONTRACT` tuples are fixed:

| routine | C declaration | `CONTRACT` |
|---|---|---|
| `_ClearSpriteAnimations` | `void _ClearSpriteAnimations(void)` | `("b", "c", "d", "e", "hl")` |
| `CreateSpriteAndAnimBufferEntry` | `uint8_t CreateSpriteAndAnimBufferEntry(uint8_t a, uint8_t f)` | `("f", "b", "c", "d", "e", "hl")` |
| `FillNewSpriteAnimBufferEntry` | `void FillNewSpriteAnimBufferEntry(uint16_t hl)` | `("b", "c", "d", "e", "hl")` |
| `DisableCurSpriteAnim` | `void DisableCurSpriteAnim(void)` | `("b", "c", "d", "e", "hl")` |
| `DisableSpriteAnim` | `void DisableSpriteAnim(uint8_t a)` | `("b", "c", "d", "e", "hl")` |
| `GetSpriteAnimCounter` | `uint8_t GetSpriteAnimCounter(void)` | `("a", "b", "c", "d", "e", "hl")` |
| `_HandleAllSpriteAnimations` | `void _HandleAllSpriteAnimations(void)` | `("a", "f", "b", "c", "d", "e", "hl")` |
| `LoadSpriteDataForAnimationFrame` | `void LoadSpriteDataForAnimationFrame(uint16_t hl)` | `("b", "c", "hl")` |
| `TryHandleSpriteAnimationFrame` | `void TryHandleSpriteAnimationFrame(uint16_t hl)` | `("b", "c", "d", "e", "hl")` |
| `StartNewSpriteAnimation` | `void StartNewSpriteAnimation(uint8_t a)` | `("b", "c", "d", "e", "hl")` |
| `StartSpriteAnimation` | `void StartSpriteAnimation(uint8_t a)` | `("b", "c", "d", "e", "hl")` |
| `Func_12ac9` | `void Func_12ac9(uint8_t a, uint8_t c)` | `("b", "c", "d", "e", "hl")` |
| `LoadSpriteAnimPointers` | `uint16_t LoadSpriteAnimPointers(uint8_t a)` | `("b", "c", "d", "e", "hl")` |
| `HandleAnimationFrame` | `void HandleAnimationFrame(uint16_t hl)` | `("b", "c", "d", "e", "hl")` |
| `GetAnimFramePointerFromOffset` | `void GetAnimFramePointerFromOffset(uint8_t a, uint16_t hl)` | `("b", "c", "d", "e", "hl")` |
| `SetAnimationCounterAndLoop` | `uint8_t SetAnimationCounterAndLoop(uint8_t a, uint16_t hl)` | `("f", "b", "c", "d", "e", "hl")` |
| `Func_12ba7` | `void Func_12ba7(void)` | `("b", "c", "d", "e", "hl")` |
| `Func_12bcd` | `void Func_12bcd(void)` | `("b", "c", "d", "e", "hl")` |
| `ClearSpriteVRAMBuffer` | `void ClearSpriteVRAMBuffer(void)` | `("b", "c", "d", "e", "hl")` |
| `Func_12c05` | `SpriteAnimLookupResult Func_12c05(uint8_t a)` | `("a", "f", "b", "c", "d", "e", "hl")` |
| `Func_12c4f` | `uint8_t Func_12c4f(uint8_t a, uint8_t d)` | `("a", "b", "c", "d", "e", "hl")` |
| `Func_12c5e` | `void Func_12c5e(void)` | `("b", "c", "d", "e", "hl")` |

`LoadSpriteDataForAnimationFrame` deliberately omits `d` and `e`:
`DrawSpriteAnimationFrame` clobbers them on the draw path. Every other omitted
`a` or `f` is incidental residue no inspected caller consumes.

Adapters are literal marshalling:

- assign only `s->f` from `CreateSpriteAndAnimBufferEntry`;
- assign both `s->a` and `s->f` from `Func_12c05`;
- assign only `s->a` from `GetSpriteAnimCounter` and `Func_12c4f`;
- assign only `s->hl` from `LoadSpriteAnimPointers`;
- assign only `s->f` from `SetAnimationCounterAndLoop`;
- call every void routine once and leave all other probe fields untouched.

No adapter may derive a slot address, carry flag, cache offset, or returned
register from WRAM. `LoadSpriteAnimPointers` returns the actual HL produced by
the C body. `CreateSpriteAndAnimBufferEntry` must receive entry `f` because its
global-disabled path returns that original F unchanged; A is incidental and is
not part of its callable contract.

### Implementation sequence and behavioral decisions

#### 1. Repair the existing slot helper

Change `GetFirstSpriteAnimBufferProperty` to call
`GetSpriteAnimBufferProperty(SPRITE_ANIM_ENABLED)`. Do not call
`GetSpriteAnimBufferProperty_SpriteInA(SPRITE_ANIM_ENABLED, 0)`: that hardcodes
slot 0. Strengthen its existing oracle cases with `wWhichSprite` values
`0`, `15`, `16`, and `255`; `16` and `255` clamp to slot 15 through the existing
helper. No signature, adapter, or registry change is needed.

#### 2. Buffer and control leaves

Use generated address macros and `gb_read8`/`gb_write8`. All pointer parameters
are 16-bit Game Boy bus addresses; never cast them to host pointers and never
derive a slot number from raw HL.

- `_ClearSpriteAnimations`: if `wAllSpriteAnimationsDisabled != 0`, return
  without changing anything. Otherwise set `wWhichSprite = 0`, clear the
  enabled byte of exactly 16 entries, leave `wWhichSprite = 16`, clear the
  64-byte sprite-VRAM cache and its size, call `ZeroObjectPositions`, and
  increment `wVBlankOAMCopyToggle` modulo 256.
- `CreateSpriteAndAnimBufferEntry`: on global disable return input F unchanged.
  Otherwise call `Func_12c05`, store its returned A in `wCurrSpriteTileID` even
  if its carry is set, scan all 16 enabled bytes, and create the first free
  slot. Success returns `F=$00`; a full animation buffer returns `F=$90`. BC,
  DE, and HL are preserved on every path.
- `FillNewSpriteAnimBufferEntry`: clear raw addresses `hl+1..hl+15`, then write
  `wCurrSpriteTileID` at `hl+5`, `$ff` at `hl+6`, and `$ff` at `hl+14`.
  Preserve caller HL. Do not clamp or translate the raw address.
- `DisableCurSpriteAnim` loads `wWhichSprite` and delegates to
  `DisableSpriteAnim`. The explicit form clamps indices `16..255` to slot 15
  through `GetSpriteAnimBufferProperty_SpriteInA`; both are no-ops while all
  sprite animations are globally disabled.
- `GetSpriteAnimCounter` reads `slot+14` for the clamped current slot and
  returns only A.
- `ClearSpriteVRAMBuffer` writes size 0 and clears exactly 64 cache bytes.

#### 3. SRAM persistence and sprite-VRAM cache

- `Func_12ba7` enables the already-selected SRAM bank and writes exactly
  `$100` sprite-buffer bytes, `$40` cache bytes, and the one-byte cache size to
  `sGeneralSaveDataEnd` (`$B900..$BA40`), then disables SRAM.
- `Func_12bcd` performs the exact inverse copy from the already-selected bank
  and disables SRAM. Neither routine selects a bank itself.
- `Func_12c4f` forces `wWhichVRAMBank=0`, stores input D in
  `wVRAMTileOffset`, calls `LoadSpriteGfx(a)`, and returns its tile count in A.
- `Func_12c05` scans exactly the 8-bit
  `wSpriteVRAMBufferSize` count without clamping it to 16. A hit increments the
  entry's valid byte modulo 256. A miss appends only when size is below 16,
  calls `Func_12c4f`, and stores `{valid,id,offset,size}`. Tile end `$80` is
  accepted; `$81` is failure. Success returns the prior cumulative offset in A
  with F from `or a` (`$80` for offset 0, `$00` otherwise). Failure returns
  `A=$00,F=$90`. Preserve the assembly's writes on late tile-overflow failure;
  do not roll them back.
- `Func_12c5e` visits exactly 16 four-byte cache records. For every nonzero
  valid byte, reload that record's sprite ID at its stored tile offset through
  `Func_12c4f`; holes remain untouched.

#### 4. Animation pointers and frame state

Reuse the landed helpers rather than duplicating their logic:
`GetFirstSpriteAnimBufferProperty`, `GetSpriteAnimBufferProperty`,
`GetSpriteAnimBufferProperty_SpriteInA`, `GetAnimationFramePointer`,
`DrawSpriteAnimationFrame`, `CopyBankedDataToDE`, `CopyDataHLtoDE`,
`ZeroObjectPositions`, `GetMapDataPointer`, `LoadGraphicsPointerFromHL`, and
`LoadSpriteGfx`.

- `LoadSpriteAnimPointers(a)` selects the clamped current slot, writes the
  animation ID at `+5`, resolves graphics-table 6 through
  `GetMapDataPointer` and `LoadGraphicsPointerFromHL`, writes bank/pointer at
  `+6..+8`, writes pointer plus 3 at `+9..+10` with 16-bit carry, and returns
  that selected slot base in HL.
- `GetAnimFramePointerFromOffset(a,hl)` writes
  `wWhichAnimationFrame=a`, copies the animation bank/pointer from raw
  `hl+6..hl+8` to `wTempPointerBank/wTempPointer`, and calls
  `GetAnimationFramePointer(hl)`.
- `SetAnimationCounterAndLoop(a,hl)` always stores A at raw `hl+14`. For
  nonzero A it returns `F=$00`. For zero A it rewinds raw `hl+9..hl+10` to the
  animation pointer at `hl+7..hl+8` plus 3 and returns exact F after `scf`:
  carry is set, while Z is the high-byte ADC result. The counter remains zero;
  do not replace it with `$ff`.
- `HandleAnimationFrame(hl)` preserves caller HL, advances the raw frame-offset
  pointer by 4 with 16-bit carry, copies exactly four bytes through
  `CopyBankedDataToDE`, resolves the frame pointer, and sets the counter. A
  zero-duration frame rewinds and retries exactly as ASM does; there is no
  artificial loop guard. On the first non-looping frame, apply signed X/Y
  offsets modulo 256, independently negating them for the X/Y-inverted flags.
- `LoadSpriteDataForAnimationFrame(hl)` always copies attributes, X, Y, and tile
  ID from raw `hl+1..hl+4` to the current-sprite globals. Bit 7 at `hl+15`
  skips drawing. Otherwise copy frame bank from `hl+11`; bank 0 also skips.
  A nonzero bank loads the raw pointer at `hl+12..hl+13` and calls
  `DrawSpriteAnimationFrame`.
- `TryHandleSpriteAnimationFrame(hl)` subtracts 1 from counter `hl+14`, or 2
  when centered. Counter `$ff` is the sentinel no-op. Result zero or an
  underflow calls `HandleAnimationFrame`; any other result returns.
- `StartSpriteAnimation(a)` must pass the HL returned by
  `LoadSpriteAnimPointers` directly to `HandleAnimationFrame`.
  `StartNewSpriteAnimation(a)` returns early only when the selected slot's
  current animation ID equals A. `Func_12ac9(a,c)` takes the normal start path
  for `c=0`; otherwise it loads pointers, selects frame offset `$ff`, and stores
  C through `SetAnimationCounterAndLoop`.
- `_HandleAllSpriteAnimations` preserves all seven probe registers, calls
  `ZeroObjectPositions`, visits exactly 16 slots, and for each nonzero enabled
  byte calls `TryHandleSpriteAnimationFrame` followed by
  `LoadSpriteDataForAnimationFrame`. It leaves `wWhichSprite=16` and increments
  `wVBlankOAMCopyToggle`. The global-disabled path is an exact no-op.

### Explicit oracle matrix

Define constants for the real generated regions and use finite raw-WRAM
fixtures:

- animation buffer `$D4D0` (256 bytes), cache `$D5D8` (64 bytes), cache size
  `$D618`, OAM shadow `$CA00` (160 bytes), OAM offset `$CAB5`, and OAM toggle
  `$CAC0`;
- SRAM save range `$B900..$BA40` (321 bytes);
- raw entries at `$C100` and `$C1F8` so `+15` crosses a low-byte boundary;
- synthetic animation header at `$C200`, four-byte frame records beginning at
  `$C203`, frame table at `$C280`, and frame graphics pointer data at `$C300`.

Every routine gets an all-zero-register case and a poison-register case
(`a=$aa,f=$f0,b=$bb,c=$cc,d=$dd,e=$ee,hl=$1234`), overriding only consumed
inputs with a valid ID, count, or finite raw pointer. For
`HandleAnimationFrame`, literal `hl=0` loops forever on the ROM's zero reset
padding, so its zero-register baseline overrides consumed HL with `$C100` and a
finite frame fixture. This remains a direct oracle case, not `oracle: False`.

Add these mutation-sensitive cases:

| cluster | required cases and readback |
|---|---|
| helper repair | `GetFirstSpriteAnimBufferProperty` with current slots `0`, `15`, `16`, `255`; diff returned HL and preserved registers |
| clear/fill | active and globally-disabled `_ClearSpriteAnimations`; read all 256 entry bytes, all 65 cache bytes, all 160 OAM bytes, OAM offset, current slot, and toggle; fill `$C100` and `$C1F8` with nonzero sentinels and read exact 16-byte outputs plus untouched guard bytes |
| create/disable/counter | create into free slot 0 and slot 15, animation buffer full, cache-load failure still followed by slot creation, global-disable exact input F; disable/current-counter selection at `0`, `15`, `16`, `255`; read the selected full entry and returned contract registers |
| frame draw | unskippable set, frame bank 0, and nonzero frame bank; draw-record counts `0`, `1`, and `$ff`; read current-sprite globals, complete OAM shadow, OAM offset, both edge checks, restored ROM bank, and raw entry |
| counter dispatch | counters `$ff`, `0`, `1`, `2` crossed with centered clear/set; supply a finite next frame for every zero/underflow path; read counter, frame-offset pointer, frame globals, X/Y, and raw entry |
| global dispatch | global disabled, all 16 slots disabled, enabled slot 0, and enabled slot 15; read complete animation buffer, current frame state, complete OAM shadow, OAM offset, final current slot, and OAM toggle |
| start/pointers | same versus changed animation ID; current slots `0`, `15`, `16`, `255`; valid ROM animation IDs `0` and `7` (`AnimData7` starts at `$4ffe`, so pointer plus 3 carries); read returned HL, selected full entry, temp pointer/bank, frame state, and restored ROM bank |
| frame pointer | frame offsets `0`, `1`, `$fe`, `$ff`; raw entry bases `$C100` and `$C1F8`; read `wWhichAnimationFrame`, temp pointer/bank, frame bank/pointer fields, and exact preserved registers |
| counter/loop | A `0`, `1`, `$ff`; base pointers with high byte zero/nonzero and low byte `$fd`; read stored counter, rewound pointer, guard bytes, and exact F (`$00`, `$10`, or `$90` as selected by the fixture) |
| frame advance | frame-offset low byte `$fd`, a zero-duration record followed by a finite nonzero record, positive and negative X/Y movement, coordinate wrap at `$00/$ff`, and X/Y inversion independently and together; read the full raw entry and four-byte loaded-frame scratch |
| SRAM | save and restore in bank 0 and one nonzero bank selected by setup; use distinct 321-byte patterns, `sread` the selected bank, verify the other bank stays unchanged, read the full WRAM regions on restore, and read `$A000` after return to prove final open bus |
| cache clear | zero and nonzero cache/size patterns; read all 65 bytes and guards |
| cache lookup | size `0`, `1`, `15`, `16`; empty add, first/middle/last hit, miss, valid-byte `$ff` wrap, tile end `$80` success and `$81` failure; add a size-`$ff` fixture with 255 seeded records and the only matching ID in record 254, then read that record and returned AF; read all 65 ordinary cache bytes, size, loader globals, and bank-0 VRAM |
| direct sprite load | valid sprite IDs with D `0`, `$7f`, `$80`, `$ff`; read returned A, `wWhichVRAMBank`, tile offset, temp/VRAM pointers, full touched bank-0 VRAM span, and preserved registers |
| cache reload | all invalid, holes between active entries, active slots 0 and 15, and valid byte `$ff`; read all cache bytes unchanged plus loader globals and every touched bank-0 VRAM span |

The `$ff` frame-draw count uses a bounded `$C100..$C4fc` record fixture. The
zero-duration animation fixture puts a terminating nonzero record at the
rewound base pointer plus 3. No case relies on a default-zero frame loop.

All ordinary cases run against PyBoy. This matrix requires no
`oracle: False`, `expect`, `expect_regs`, `expect_sram`, or `expect_vram`.
Memory observables come from `read`, `sread`, and `vread` against the oracle,
not from expected bytes copied out of the C implementation.

## Critical files & anchors

- `poketcg/src/engine/gfx/sprite_animations.asm:1-605` — source of truth for all
  22 bodies, fallthroughs, flags, raw-HL arithmetic, fixed loop lengths, SRAM
  copies, cache behavior, and OAM dispatch.
- `poketcg/src/home/load_animation.asm:1-243` — exact landed helper ABIs for
  sprite-slot addressing, frame-pointer lookup, and OAM frame drawing.
- `src/home/load_animation.c:GetFirstSpriteAnimBufferProperty` — latent slot-0
  hardcode to repair before the new source depends on it.
- `tests/test_leaves.py:34-193` — authoritative case serialization, contract
  comparison, direct oracle, and C-only expectation rules.
- `src/probe.c:170-499` — live bus `read`, bank-qualified `sread`/`vread`,
  `ramg`, setup-call, and register-seeding semantics used by the matrix.

## Verification

After all four workers return:

1. confirm only their declared paths changed and the registry tuple contains
   the 22 names in assembly order;
2. compile both case modules with
   `python3 -m py_compile tests/cases/load_animation.py
   tests/cases/sprite_animations.py`;
3. run `just build` with the private integration environment;
4. run `just oracle-diff GetFirstSpriteAnimBufferProperty`;
5. run `just oracle-diff <name>` once for each of the 22 names and require
   `PASS` for every command before mutation testing.

If a direct diff fails, repair the source, adapter, or case at the contract
boundary that failed. Do not hide a timeout or mismatch with `oracle: False`.

### Mutation verification

First prove the helper repair: temporarily restore the old slot-0 hardcode,
confirm `GetFirstSpriteAnimBufferProperty` goes RED, restore the fixed call, and
confirm PASS.

Then run the following 22 mutations sequentially. They share one C source, so
parallel edits would invalidate one another's binaries and restoration state.
For each row: apply only the named temporary corruption, run that routine's
direct diff and require RED, restore the file, rerun the same diff and require
PASS, then record the result in an ephemeral session artifact.

| routine | deterministic temporary mutation |
|---|---|
| `_ClearSpriteAnimations` | invert the global-disabled predicate |
| `CreateSpriteAndAnimBufferEntry` | set carry in the successful returned F |
| `FillNewSpriteAnimBufferEntry` | clear 14 trailing bytes instead of 15 |
| `DisableCurSpriteAnim` | delegate with `wWhichSprite ^ 1` |
| `DisableSpriteAnim` | invert the global-disabled predicate |
| `GetSpriteAnimCounter` | read raw counter offset `+15` instead of `+14` |
| `_HandleAllSpriteAnimations` | omit `ZeroObjectPositions` |
| `LoadSpriteDataForAnimationFrame` | XOR the copied attributes with 1 |
| `TryHandleSpriteAnimationFrame` | subtract 1 even when centered |
| `StartNewSpriteAnimation` | invert the same-animation early-return predicate |
| `StartSpriteAnimation` | omit `HandleAnimationFrame` |
| `Func_12ac9` | invert the `c==0` path split |
| `LoadSpriteAnimPointers` | write base pointer plus 2 instead of plus 3 |
| `HandleAnimationFrame` | omit the X-coordinate update |
| `GetAnimFramePointerFromOffset` | store frame offset `a ^ 1` |
| `SetAnimationCounterAndLoop` | store 1 instead of 0 on the loop path |
| `Func_12ba7` | copy `$3f` cache bytes instead of `$40` |
| `Func_12bcd` | restore `$3f` cache bytes instead of `$40` |
| `ClearSpriteVRAMBuffer` | clear `$3f` bytes instead of `$40` |
| `Func_12c05` | omit the valid-byte increment on a cache hit |
| `Func_12c4f` | store `d ^ 1` as the VRAM tile offset |
| `Func_12c5e` | visit 15 cache slots instead of 16 |

A green mutation means the listed case/readback is insufficient. Strengthen
only that routine's oracle matrix and repeat until the mutation is RED and the
restored body is PASS. No temporary mutation may remain in the working copy.

### Final barrier, commits, and status update

With every direct diff and mutation restored green, run centrally:

```sh
export POKETCG_BUILD=build-gfx-sprites
export POKETCG_PORTS=""
python3 -m py_compile tests/cases/load_animation.py tests/cases/sprite_animations.py
just build
just oracle-diff-all
just data-verify
just oracleb-replay
```

Acceptance:

- warning-free build;
- adapter lint PASS as part of the full gate;
- exactly **502/502** routines clean;
- helper regression reproduced RED and restored PASS;
- all 22 sprite mutations recorded RED and restored PASS;
- data verification exit 0;
- replay determinism exit 0;
- only the seven declared paths changed, with `tests/routines.py` limited to
  the partitioned `sprite_animations` tuple;
- no stub, alias, TODO, generated C data table, ROM-data-only ASM edit, or
  temporary mutation remains.

Commit the verified code and oracle matrix:

```sh
jj commit -m "feat(gfx): port sprite animations"
```

Use that new commit ID to update `docs/vision.md` to the 502-routine gate and
add `W1-L sprite animations | 22/22 | landed | <commit>` to `docs/plan.md`.
Confirm the registry still parses to 502 names and the working copy contains
only those two documentation edits, then commit:

```sh
jj commit -m "docs(plan): record sprite animations"
```

Finish with a clean `jj status`. Do not push.

## Assumptions & contingencies

- Execution starts from `b3a37679` or a descendant with the same 480-name
  registry and no sprite-animation tuple. If the remote advanced, re-count the
  registry and re-read every changed anchor before editing; retain the fixed
  target `current count + 22` and do not silently merge a second implementation.
- ROM animation IDs 0 and 7 are valid at this revision, and `AnimData7` begins
  at `$4ffe`. If a fresh `just bootstrap` produces different symbols, select
  the first valid table entry whose pointer low byte is `$fd..$ff`, record that
  exact symbol in the case comment, and keep the pointer-plus-3 carry witness.
- The explicit fixtures require no `oracle: False`. If PyBoy times out, first
  repair the fixture so every zero-duration path reaches its seeded nonzero
  record; never convert an ordinary timeout or mismatch into a C-only case.
- If direct oracle use exposes another landed-helper mismatch, prove it against
  that helper's ASM, add a regression in its existing case module, and include
  only the minimal helper fix in the feature commit. Do not duplicate the helper
  inside `sprite_animations.c`.
- Unrelated working-copy changes are user-owned. Leave them untouched and use
  path-scoped jj commits for the declared implementation, test, and docs paths.
