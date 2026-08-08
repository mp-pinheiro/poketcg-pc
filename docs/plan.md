# Home-bank completion plan

## Status

| slice | routines | state | commit |
|---|---|---|---|
| Step 0 — substrate | — | landed | a5a8bf56 |
| W1-A tiles | 16/21 (5 excluded) | landed | 9fa8e9bd |
| W1-B duel | 35/36 | landed | 8322f430 |
| W1-C substatus | 19/19 | landed | 5c8e9257 |
| W1-D save + card_collection | 9/9 | landed | 5274fae5 |
| W1-E serial + printer | 16/18 (2 excluded) | landed | 2af7b747 |
| W1-F map + load_animation | 9/9 | landed | 0603005d |
| W1-G menus cursor/text-box | 11/12 (1 internal-only) | landed | 1e265e48 |
| W1-H small leaves (8 files) | 8/11 (3 excluded) | landed | 876d82ea |
| W1-I setup + palettes | 9/9 | landed | 2056acad |
| W1-J harness: keys | — | landed | 9e383124 |
| W2-K input waiters + scrollable text | 10 | pending | — |
| W2-L damage modifiers + colours | 6 | pending | — |
| Wave 3 — inline (4 routines) | 4 | pending | — |

This table is the resumption point for a compacted or cleared session: each
slice flips its own row to `landed` (with the jj commit id) when its barrier
check passes.

**Barrier 1 (Wave 1)**: `just oracle-diff-all` — 354/354 routines clean,
`just build` warning-free, `just data-verify` and `just oracleb-replay` both
exit 0. Also fixed at the barrier: `src/home/input.c`'s `read_joypad()`
unconditionally OR'd in `0x0F`, so `ReadJoypad` could never observe a held
button regardless of W1-J's `g_keys` model (commit `73154dd8`); and one
hazardous `Func_0e8e` case whose poisoned `rIE`/`rIF` seed enabled real
interrupt sources with pending IF bits, causing PyBoy to dispatch an actual
interrupt mid-call — re-seeded with only unused/non-hazardous bits.

## Working agreement — applies to every slice

Read `docs/port-contract.md` in full before writing C — it is complete and
normative, and `AGENTS.md` §2 routes to it. This section only adds what is
specific to this wave.

### Build and diff loop

Each slice owns a private build directory and a private file subset so no
slice can red-light another:

```sh
export POKETCG_BUILD=build-<slice>
export POKETCG_PORTS="tiles;card_data"     # semicolon list of pret basenames this slice owns
just oracle-diff <PretSymbol>              # iterate until PASS
```

- Slices **MUST NOT** run `just oracle-diff-all`. A routine registered in
  `tests/routines.py` with no cases is a hard FAIL, so mid-flight registrations
  would red the shared gate for everyone. Only the barrier runs the full gate.
- `just build` must stay warning-free under `-Wall -Wextra`.
- `python3 tools/lint_adapters.py` must exit 0: no integer literal `>= 0x8000`
  in an adapter body, and exactly one routine call per adapter. Do not add
  allowlist entries.

### Files per pret source (unchanged, four files)

`src/home/<file>.{c,h}`, `src/probe/<file>.c` (array `probe_entries_<file>[]`,
name must match the basename), `tests/cases/<file>.py`. CMake globs both
directories; no build edit is needed.

### `tests/routines.py` is shared

Each slice edits **only** the `ROUTINES["<its own pret basename>"]` tuple.
Distinct line ranges, so concurrent edits resolve. Never reformat neighbouring
entries.

### Per-routine definition of done

1. Contract re-derived from the asm **without reading the C**: `CONTRACT`
   names every real output and every register the asm preserves; loop residue
   that the callable contract does not promise stays out.
2. Coverage per `docs/port-contract.md`: an all-zero case, a poisoned-register
   case (`a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234`), and
   every boundary the routine has.
3. `just oracle-diff <Fn>` prints PASS.
4. **Mutation test, mandatory**: apply one shape-preserving mutation
   (structure intact, meaning corrupted), confirm the diff goes RED, restore,
   confirm PASS. Record mutation and result. A routine whose cases cannot go
   red is not done — five false greens have shipped here already.

### Traps this repo has already paid for

- **`ld a, [hl]` is a bus read, not a ROM-image read.** Use `gb_read8` under
  whatever bank the *caller* mapped. Never `rom_ptr(BANK(Table), addr)` for a
  table the routine does not bank-switch for itself.
- **A wrong signature presents as a scatter of unrelated register mismatches**
  and reads like "unportable". Derive exit registers from the asm tail before
  concluding anything is blocked.
- **Reserved WRAM `$CF00-$CFFF`** holds the oracle's synthesized frame
  (`tools/oracle/pyboy_oracle.py:33-38`). Cases must not write it. A routine
  whose own state lives there uses `oracle: False` + `why` + `expect`/
  `expect_regs` derived from the asm — and those cases must still be
  mutation-tested, because they are the easiest place to write a test that
  cannot fail.
- **CGB paths write tiles to VRAM bank 0 and attributes to bank 1, then
  restore bank 0.** A plain `read` sees only half. Use
  `vread: {bank: {addr: count}}` on both banks for anything that writes tiles.
- **Warm state uses a `setup` prelude**, not a hand-written expectation:
  `"setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]`. Anything driving the
  text engine needs it.
- **A `_b` suffix on a pret symbol is a different adjacent field**, not the
  high byte of a pair.
- **Adapters marshal, they never compute.** A literal address or a
  re-derived answer in an adapter is a defect, not a shortcut.

### What is excluded from this wave, and why

State these as exclusions in the issue comment; never stub them.

| Excluded | Reason |
|---|---|
| `sgb.asm` (20 labels), `DrawRegularTextBoxSGB`, `ColorizeTextBoxSGB`, `AttrBlkPacket_*` | SGB path dropped by #2. Packets are data, not code. |
| `farcall.asm`, `jumptable.asm`, `call_regs.asm`, `interrupt.asm`, `hblank.asm`, `vblank.asm`, `double_speed.asm`, `vram.asm`, `dma.asm:CopyDMAFunction`, `lcd.asm:WaitForVBlank` | Deleted or dissolved by the Phase-1 transform (`docs/phase1-transform.md`). |
| `write_number.asm` BCD family, `math.asm:HLTimes10`/`ADividedBy10`, `list.asm:GetNextElementOfList`/`SetListToNextPosition`, `serial.asm:Unreferenced*`, `process_text.asm:Unknown_2589` | Dead code — zero callsites in `poketcg/src`, already recorded in `docs/port-contract.md`. |
| `RunOverworldScript`, `AIDoAction*`, `TryExecuteEffectCommandFunction`, `map.asm:_ExecuteGameEvent` | Tails are `jp hl` / `CallHL` / `JumpToFunctionInTable` into **unported engine** targets. They become C function-pointer tables when their targets land, not before. |
| Anything reaching `PlaySFX`/`PlaySong` (`HandleMenuInput`, `HandleYesOrNoMenu`, `YesOrNoMenu*`, `HandleDuelMenuInput`, `PlayDefaultSong`) | `_PlaySFX`/`_PlaySong` are bank `$3d` — Phase 3 (#4). |
| Anything reaching `TossCoin`/`_TossCoin`, `DrawDuelHUDs`, `DrawDuelMainScene`, `_CopyCardNameAndLevel`, `GetEventValue` | Unported `engine/`. |
| `start.asm:Start` | Ends in `jp GameLoop` (engine) and calls `SetupSound` (Phase 3). |
| Data labels: `PowersOf2`, `InvertedPowersOf2`, `NoDamageOrEffectTextIDTable`, `GameEventPointerTable`, `PlayerMovementOffsetTable*`, `OverworldMapNames`, `CardSymbolTable`, `DuelMenuCursorCoords`, `NarrowTextBoxMenuParameters`, `WideTextBoxMenuParameters`, `InitialPalette`, `BGScrollData` | Data, read through the bus by the routines that index them. Not registered as routines. |

**Fallthrough is a dependency.** `StopMusic` falls into `PlaySong`,
`PlaySFX_InvalidChoice` into `PlaySFX`, `DrawPlayerPortrait` into
`DrawPortrait`, `LoadSymbolsFont` into `CopyFontsOrDuelGraphicsTiles`,
`SetCursorParametersForTextBox_Default` into `WaitForButtonAorB`. A label with
no terminator before the next label inherits the next label's blockers. The
first three are blocked and stay out; the last two are inside their slices.

## Wave 1 — nine parallel slices

All nine are file-disjoint and independent. Dispatch as one `tasks[]` batch —
**after Step 0 is committed**, so every subagent's first read (`AGENTS.md` →
`docs/port-contract.md` → `docs/plan.md`) resolves. Each task's brief names
its slice heading below and the routine list verbatim; subagents have no
conversation history and will not infer it.

### W1-A · `tiles.asm` — complete the file (21 routines)

`POKETCG_PORTS=tiles`. Port in this order; the file is one cascade off a
single copier.

1. `CopyFontsOrDuelGraphicsTiles` (`tiles.asm:347`) — `BankpushROM(BANK(Fonts))`,
   `c = TILE_SIZE`, `CopyGfxData`, `BankpopROM`. `hl <= $3fff` reads Gfx1 at
   `hl+$4000`; `$4000..$7fff` reads Gfx2 at `hl`.
2. `LoadSymbolsFont` (`:337`) — falls through into (1).
3. The eleven three-line wrappers that `jr`/`call` into (1): `LoadCardSet2Tiles`
   (`:215`), `LoadDuelDrawCardsScreenTiles` (`:240`),
   `LoadCardOrDuelMenuBorderTiles` (`:248`), `LoadCardTypeHeaderTiles` (`:256`),
   `LoadDuelCardSymbolTiles` (`:266`), `LoadDuelCardSymbolTiles2` (`:279`),
   `LoadDuelCheckPokemonScreenTiles` (`:296`), `LoadDuelFaceDownCardTiles`
   (`:291`), `LoadPlacingThePrizesScreenTiles` (`:309`),
   `LoadDeckAndDiscardPileIcons` (`:318`), `LoadDuelCoinTossResultTiles` (`:330`).
4. `Func_212f` (`:356`) — same copier into `sGfxBuffer1`/`sGfxBuffer4`; needs
   `sread` on the SRAM bank.
5. `DrawDuelBoxMessage` (`:386`) — `HtimesL`, copier, then `jp FillRectangle`.
6. `LoadFullWidthFontTiles` (`:406`) — three `Copy1bppTiles` calls into
   `v0Tiles0/2/1`.
7. `Func_2057` (`:200`), `Func_2055` (`:196`), `Func_2051` (`:192`), `Func_2046`
   (`:182`), `Func_1f96` (`:49`) — the `add sp,-10` / `ld hl,sp+N` stack-frame
   group. These build a local frame on the GB stack; in C the frame is locals,
   and the `sp+N` offsets identify which local each accessor reads. Port
   `Func_1f96` last, once the four accessors pin the frame layout.

Every routine here writes VRAM: **`vread` on both banks** in the cases, not
`read`.

### W1-B · `duel.asm` — 36 routines

`POKETCG_PORTS=duel`. Appends to the existing `src/home/duel.c` (28 routines
already ported). Order:

Deck and hand (`:60`-`:364`): `CopyDeckData`, `CountPrizes`, `ShuffleDeck`,
`DrawCardFromDeck`, `ReturnCardToDeck`, `SearchCardInDeckAndAddToHand`,
`AddCardToHand`, `RemoveCardFromHand`, `MoveHandCardToDiscardPile`,
`PutCardInDiscardPile`, `MoveDiscardPileCardToHand`, `CheckPrizeTaken`.

Sort helper (`:650`): `SortCardsInListByID_CheckForListTerminator`.

Play area (`:814`-`:1221`): `CheckIfCanEvolveInto`,
`CheckIfCanEvolveInto_BasicToStage2`, `EvolvePokemonCardIfPossible`,
`EvolvePokemonCard`, `ClearAllStatusConditions`, `PutHandCardInPlayArea`,
`PutHandPokemonCardInPlayArea`, `EmptyPlayAreaSlot`,
`MovePlayAreaCardToDiscardPile`, `SwapPlayAreaPokemon`,
`ShiftTurnPokemonToFirstPlayAreaSlots`, `ShiftAllPokemonToFirstPlayAreaSlots`,
`SwapArenaWithBenchPokemon`, `GetPlayAreaCardAttachedEnergies`.

Attack data (`:1415`-`:1442`): `CopyAttackDataAndDamage`,
`CopyAttackDataAndDamage_FromDeckIndex`, `CopyAttackDataAndDamage_FromCardID`.

Tails and modifiers (`:1621`-`:2273`): `ReturnCarry`,
`LoadNonPokemonCardEffectCommands`, `ApplyAttachedPlusPower`,
`ApplyAttachedDefender`, `PrintKnockedOutIfHLZero`,
`MoveCardToDiscardPileIfInPlayArea`.

Contract notes derived from the file's already-ported neighbours: exit
**flags are outputs** here far more often than they look (the existing
entries pin `$90` = Z+C on empty-list exits, `$C0` = Z+N after a terminating
`dec`), and loop residue in `b`/`c`/`de` frequently survives to the caller.
Seed `hWhoseTurn` explicitly — a probe entering with `hWhoseTurn = 0` reads a
different duelist page than the cases intend, which already produced one
green mutation.

Deferred to Wave 2 (cross-file): `ApplyDamageModifiers_DamageToTarget`,
`ApplyDamageModifiers_DamageToSelf`, `GetPlayAreaCardRetreatCost`,
`PrintKnockedOut`, `PrintPlayAreaCardKnockedOutIfNoHP`,
`DrawWideTextBox_WaitForInput_ReturnCarry`.

### W1-C · `substatus.asm` — 19 routines

`POKETCG_PORTS=substatus`. Order (the file closes over itself once the two
pkmn-power checks land):

`CheckIsIncapableOfUsingPkmnPower` (`:502`),
`CheckIsIncapableOfUsingPkmnPower_ArenaCard` (`:495`, falls through into it),
then `HandleDoubleDamageSubstatus` (`:3`),
`HandleDamageReductionExceptSubstatus2` (`:63`), `HandleDamageReduction`
(`:34`), `HandleCantAttackSubstatus` (`:286`), `HandleAmnesiaSubstatus`
(`:308`), `HandleNoDamageOrEffectSubstatus` (`:370`),
`CheckNoDamageOrEffect` (`:451`), `IsClairvoyanceActive` (`:484`),
`GetLoadedCard1RetreatCost` (`:592`), `CheckUnableToRetreatDueToEffect`
(`:625`), `CheckCantUseTrainerDueToEffect` (`:640`),
`IsPrehistoricPowerActive` (`:651`), `ClearDamageReductionSubstatus2`
(`:664`), `UpdateSubstatusConditions_StartOfTurn` (`:685`),
`UpdateSubstatusConditions_EndOfTurn` (`:699`), `IsRainDanceActive` (`:717`),
`ClearChangedTypesIfMuk` (`:840`).

Cases must drive both duelist sides — the opponent-side count reads the
opponent deck, and an unterminated bench walk falls off into ROM and
terminates at a different `$FF` per side (both already bit this file).
Status-condition masks need a case with a non-zero condition (e.g. `$08`
paralyzed) or the mask mutation stays green.

Deferred to Wave 2: `CheckRainDanceScenario`,
`HandleStrikesBack_AgainstDamagingAttack`.

### W1-D · `save.asm` + `card_collection.asm` — 9 routines

`POKETCG_PORTS="save;card_collection"`. Appends to `src/home/save.c` and
`src/home/card_collection.c`.

`save.asm` (whole file, 5): `SaveGeneralSaveData` (`:1`),
`LoadGeneralSaveData` (`:5`), `ValidateGeneralSaveData` (`:9`),
`AddCardToCollectionAndUpdateAlbumProgress` (`:15`), `SaveGame` (`:19`). Each
is a `farcall` into an engine routine **already ported**
(`_SaveGeneralSaveData`, `_LoadGeneralSaveData`, `_ValidateGeneralSaveData`,
`_AddCardToCollectionAndUpdateAlbumProgress`, `_SaveGame` are all in
`tests/routines.py`), so the farcall becomes a plain C call. `SaveGame`
additionally pushes/pops all four register pairs and passes `c = 0` — its
CONTRACT preserves everything.

`card_collection.asm` (4): `GetAmountOfCardsOwned` (`:2`),
`GetCardCountInCollectionAndDecks` (`:46`), `GetCardCountInCollection`
(`:97`), `RemoveCardFromCollection` (`:177`). These read/write SRAM through
the enable latch — cases need `sram` seeds, `sread` readback, and a
`ramg: False` case so the routine's own `EnableSRAM` is observable.

### W1-E · `serial.asm` + `printer.asm` — 18 routines

`POKETCG_PORTS="serial;printer"`. Appends to `src/home/serial.c`
(`SerialTimerHandler` already ported).

`serial.asm` (14, excluding the two `Unreferenced*` dead labels): `Func_0cc5`
(`:38`), `SerialHandler` (`:97`), `SerialHandleRecv` (`:151`),
`SerialHandleSend` (`:213`), `SerialSendByte` (`:263`), `Func_0e32` (`:294`),
`SerialRecvByte` (`:302`), `SerialExchangeBytes` (`:335`), `Func_0e8e`
(`:372`), `ResetSerial` (`:387`), `ClearSerialData` (`:397`),
`SerialSendBytes` (`:410`), `SerialRecvBytes` (`:431`),
`LinkOpponentTurnFrameFunction` (`:504`).

`printer.asm` (4): `SendNextPrinterPacketByte` (`:184`),
`SendByteThroughSerialData` (`:206`), `SendPrinterPacket`,
`ExecutePrinterPacketSequence`.

These drive `rSB`/`rSC` (`$FF01`/`$FF02`) and the serial state block in WRAM.
`$FF01`/`$FF02` are plain `g_io` bytes on the C side and real registers in
PyBoy: with **no link partner attached**, a transfer started by writing
`$FF02` never completes on either side, so model exactly what the asm writes
and diff the WRAM state machine plus the `g_io` bytes via `read`. If a
routine busy-waits on a transfer-complete bit the oracle will time out at
`MAX_FRAMES` — that routine is not standalone-callable; give it a `setup`
prelude that leaves the state block in the branch you want, and if that still
cannot terminate, exclude it with the timeout as the recorded reason rather
than stubbing it.

### W1-F · `map.asm` + `load_animation.asm` — 9 routines

`POKETCG_PORTS="map;load_animation"`. Appends to `src/home/map.c` and
`src/home/load_animation.c`.

`map.asm` (7): `GameEvent_Overworld` (`:61`), `CopyGfxDataFromTempBank`
(`:209`), `GetLoadedNPCID` (`:262`), `GetItemInLoadedNPCIndex` (`:268`),
`FindLoadedNPC` (`:291`), `GetNextNPCMovementByte` (`:321`), `GetDefaultSong`
(`:361`).

`load_animation.asm` (2): `DrawSpriteAnimationFrame` (`:27`),
`GetAnimationFramePointer` (`:144`).

`_ExecuteGameEvent` and the other `GameEvent_*` handlers stay out — the
pointer table's targets reach `StartDuel_VSAIOpp`, `HandleGiftCenter`,
`PlaySong` and `GetEventValue`, all unported.

### W1-G · `menus.asm` cursor and text-box group — 12 routines

`POKETCG_PORTS=menus`. Appends to `src/home/menus.c` (10 routines already
ported).

`DrawCursor` (`:191`), `EraseCursor` (`:186`), `DrawCursor2` (`:213`),
`RefreshMenuCursor` (`:173`), `DrawCardSymbol` (`:654`),
`DrawTextBox_PrintTextNoDelay` (`:775`), `DrawNarrowTextBox` (`:800`),
`DrawWideTextBox` (`:832`), `DrawNarrowTextBox_PrintTextNoDelay` (`:769`),
`DrawWideTextBox_PrintText` (`:788`), `DrawWideTextBox_PrintTextNoDelay`
(`:761`), `PrintYesOrNoItems` (`:965`).

These drive the text engine, so **every case needs a `SetupText` prelude**
and `vread` on both VRAM banks. `NarrowTextBoxMenuParameters` /
`WideTextBoxMenuParameters` are the parameter *data* the box routines read —
bus reads, not ports.

The input-waiting siblings (`WaitForButtonAorB`, `WaitForWideTextBoxInput`,
`DrawWideTextBox_WaitForInput`, `DrawNarrowTextBox_WaitForInput`,
`DrawWideTextBox_PrintTextNoDelay_Wait`) are Wave 2 — they need W1-J's joypad
support. `PrintCardListItems`, `HandleMenuInput`, `CardListMenuFunction` and
the `YesOrNo*` drivers stay out (`_CopyCardNameAndLevel` / `PlaySFX`).

### W1-H · Small leaves across eight files — 11 routines

`POKETCG_PORTS="card_data;card_color;damage;objects;scroll;effect_commands;ai;sound"`.

| pret file | routines |
|---|---|
| `card_data.asm` | `GetCardPointer` (`:142`), `LoadCardDataToHL_FromCardID`, `CopyFontsOrDuelGraphicsTiles2` (`:208`) |
| `card_color.asm` | `GetArenaCardColor` (`:2`) |
| `damage.asm` | `SubtractFromDamage` (`:14`) |
| `objects.asm` | `SetManyObjectsAttributes` (`:3`) |
| `scroll.asm` | `ApplyBackgroundScroll` (`:60`) |
| `effect_commands.asm` | `CheckMatchingCommand` (`:41`) |
| `ai.asm` | `LoadOpponentDeck` (`:4`) |
| `sound.asm` | `Func_37c5` (`:56`), `Func_37a5` (`:35`) |

`CheckMatchingCommand` walks the `EffectCommands` list through the bus under
`BANK(EffectCommands)`, writes `wEffectFunctionsBank`, and returns the
function pointer in `hl` with **nc on match, c on miss or NULL** — the
pointer is an output, the dispatch (`TryExecuteEffectCommandFunction`) is not
ported.

`LoadOpponentDeck` calls the already-ported `SwapTurn`, `LoadDeck` and
`GetTurnDuelistVariable`, and seeds `wRNG1/2/wRNGCounter` to `$57` on the Sam
path only — cases must cover Sam-normal, Sam-practice and a plain deck ID,
plus the `NUM_DECK_IDS + 1` clamp.

`Func_37a5`/`Func_37c5` are a pure 2bpp→shifted-tile converter (`sound.asm`
only by accident of placement). The rest of `sound.asm` is `farcall` into
bank `$3d` and stays for Phase 3.

### W1-I · `setup.asm` + `palettes.asm` — 9 routines

`POKETCG_PORTS="setup;palettes"`. Appends to `src/home/palettes.c` (8
routines already ported).

`palettes.asm`: `CopyCGBPalettes` (`:93`), `FlushAllCGBPalettes`.

`setup.asm`: `NoOp` (`:31`), `ZeroRAM` (`:140`), `FillTileMap` (`:112`),
`SetupVRAM` (`:92`), `SetupRegisters` (`:3`), `SetupPalettes` (`:55`),
`DetectConsole` (`:35`).

Three resolutions, decided here:

- **`DetectConsole` drops the SGB branch**, exactly as `DrawRegularTextBox`
  already does: `a == BOOTUP_A_CGB` → `CONSOLE_CGB` (then `rWBK = 1`; the
  `SwitchToCGBDoubleSpeed` call is deleted per Phase 1), otherwise
  `CONSOLE_DMG`. Cases cover CGB and DMG only and say in the case file that
  the SGB gap is by design, not an oversight.
- **`ZeroRAM` zeroes `$C000-$DFFF` and `$FF80-$FFEF`.** On the oracle that
  erases the synthesized call frame's own stack, so it cannot run there: use
  `oracle: False` + `why` + an `expect` map proving a seeded pattern at both
  ends of each region became zero, and mutation-test it.
- **`FillTileMap` / `SetupVRAM` write both VRAM banks** and restore bank 0 —
  `vread` on banks 0 and 1, and note that `FillTileMap` clears BG map 0 only
  (`v0BGMap1 - v0BGMap0` = `$400`); running to `$800` destroys BG map 1 and is
  the silently-plausible wrong constant.

`Start` itself stays out (see exclusions).

### W1-J · Harness: joypad input in cases (no routine ports)

Owns `src/mem.c`, `src/mem.h`, `src/probe.c`, `tools/oracle/pyboy_oracle.py`,
`tests/test_leaves.py`. Touches no `src/home/*`, no `src/probe/<file>.c`, and
**not** `tests/routines.py`.

Today `gb_read8(0xFF00)` returns a raw `g_io[0]` byte, so `ReadJoypad` always
reports "nothing held" and every input-waiting routine spins forever on the C
side. Add a held-keys case key.

1. **`src/mem.h` / `src/mem.c`** — add `extern uint8_t g_keys;` (1 =
   pressed), zeroed in `mem_reset()`. In `gb_read8`, special-case `$FF00` next
   to the existing `$FF41` case:

   ```c
   if (addr == 0xFF00u) {
       uint8_t sel = (uint8_t)(*gb_ptr(addr) & 0x30u);
       uint8_t low = 0x0Fu;
       if (!(sel & 0x10u))                    /* P14 low: d-pad */
           low &= (uint8_t)~(g_keys >> 4);
       if (!(sel & 0x20u))                    /* P15 low: buttons */
           low &= (uint8_t)~(g_keys & 0x0Fu);
       return (uint8_t)(0xC0u | sel | low);
   }
   ```

   `g_keys` uses the game's own `hKeysHeld` layout
   (`poketcg/src/constants/hardware.inc:88-105`): bit0 `A`, 1 `B`, 2
   `SELECT`, 3 `START`, 4 `RIGHT`, 5 `LEFT`, 6 `UP`, 7 `DOWN`. That matches
   `ReadJoypad` (`src/home/input.c:29-40`), which reads the d-pad group and
   shifts it into the high nibble.

2. **`src/probe.c`** — parse a top-level `"keys"` number alongside `"ramg"`,
   and assign `g_keys` after every seed and before any `setup` prelude, so
   preludes see the same held state.

3. **`tools/oracle/pyboy_oracle.py`** — `Oracle.call(..., keys: int = 0)`. At
   the top of `call()`, queue `button_release` for all eight buttons, then
   `button_press` for each bit set in `keys`, in that order (`self.events` is
   consumed at the start of the next `_tick` and cleared after, so
   releases-then-presses in one list resolve to the intended final state;
   `no_input=True` only bypasses the *window* plugin, API events still reach
   `mb.buttonevent`). PyBoy names: `a b select start right left up down`.

4. **`tests/test_leaves.py`** — pass `keys` through `run_probe` (into the
   JSON request) and `oracle.call`, and include it in `describe()` so a
   failing case prints which buttons were held.

**Acceptance for this slice** — it must be proven, not just compiled:

```sh
export POKETCG_BUILD=build-keys POKETCG_PORTS="menus;input;frames;text_box;print_text;process_text"
just oracle-diff ReadJoypad     # still PASS with keys=0
```
plus a scratch case with `keys: 0x01` (A held) on `ReadJoypad` asserting
`hKeysHeld=$01`, `hKeysPressed=$01` on both sides. Wave 2 turns this into
permanent coverage on `WaitForButtonAorB`. If PyBoy's held state turns out
not to survive into a synthesized call, do **not** work around it by forcing
`hKeysHeld` — report that and leave Wave 2's input group unported.

## Barrier 1 — run centrally, not per slice

```sh
unset POKETCG_BUILD POKETCG_PORTS
just build            # exit 0, warning-free
just oracle-diff-all  # every routine, exit 0
just data-verify
just oracleb-replay
```

Expect roughly **223 → 367** routines. Any FAIL is fixed here, at the
barrier — the pattern in this repo is that a slice's own checks pass and the
shared gate finds the real defect. Then commit; the repo uses jj with
Conventional Commits, a ≤50-char subject and no body (`docs/jj-workflow.md`),
one commit per slice, e.g. `feat: port tile loaders and font copiers`.

## Wave 2 — two parallel slices (needs Barrier 1 green)

### W2-K · Input waiters and scrollable text — 10 routines

`POKETCG_PORTS="menus;print_text"`. Needs W1-G (cursor group) and W1-J
(`keys`).

`menus.asm`: `WaitForButtonAorB` (`:716`), `WaitForWideTextBoxInput` (`:846`),
`DrawWideTextBox_WaitForInput` (`:841`), `DrawNarrowTextBox_WaitForInput`
(`:809`), `DrawWideTextBox_PrintTextNoDelay_Wait` (`:755`).

`print_text.asm`: `WaitForPlayerToAdvanceText`, `PrintScrollableText`,
`PrintScrollableText_NoTextBoxLabel`,
`PrintScrollableText_WithTextBoxLabel_NoWait`,
`PrintScrollableText_WithTextBoxLabel`.

`WaitForButtonAorB` returns **carry set if B, clear if A**
(`menus.asm:716-730`) and erases the cursor on both paths — cases need
`keys: 0x01` (A) and `keys: 0x02` (B) and must diff the erased cursor tile,
not just the flag. `PrintScrollableText`'s delay loop runs zero `DoFrame`
calls when `wTextSpeed = 0`; seed it. This closes issue #17.

### W2-L · Damage modifiers and play-area colours — 6 routines

`POKETCG_PORTS="card_color;substatus;duel"`. Needs W1-C (substatus) and W1-H
(`GetArenaCardColor`).

`card_color.asm`: `GetPlayAreaCardColor`, `HandleEnergyBurn`.
`substatus.asm`: `CheckRainDanceScenario` (`:728`).
`duel.asm`: `ApplyDamageModifiers_DamageToTarget` (`:1848`),
`ApplyDamageModifiers_DamageToSelf` (`:1933`), `GetPlayAreaCardRetreatCost`
(`:2262`).

`ApplyDamageModifiers_DamageToTarget` composes `ApplyAttachedPlusPower`,
`ApplyAttachedDefender`, `GetPlayAreaCardColor`, `HandleDamageReduction` and
`HandleDoubleDamageSubstatus` — cases must drive each modifier independently
*and* in combination, or a dropped term still diffs clean.

## Wave 3 — inline after Barrier 2 (4 routines)

Depends on both W2 slices, so run it directly rather than as a tenth agent:
`duel.asm` `PrintKnockedOut` (`:2062`), `PrintPlayAreaCardKnockedOutIfNoHP`
(`:2034`), `DrawWideTextBox_WaitForInput_ReturnCarry` (`:1617`);
`substatus.asm` `HandleStrikesBack_AgainstDamagingAttack` (`:185`).

## Critical files & anchors

- `docs/port-contract.md` — the contract: memory model, the three C rules,
  adapter rules, required case coverage. Non-optional reading before any C.
- `tests/test_leaves.py:95-169` (`diff_case`) — the authoritative list of case
  keys: `wram`, `read`, `sram`/`sread`, `vread`, `ramg`, `setup`, `keys`,
  `oracle: False` + `why` + `expect` / `expect_regs`.
- `tools/oracle/pyboy_oracle.py:33-38, 191-263` — reserved window, `_run`,
  and where `keys` hooks in.
- `src/mem.c:149-189` — `gb_read8`/`gb_write8`; the `$FF41` special case is
  the pattern W1-J copies for `$FF00`.
- `docs/phase1-transform.md` — the per-routine delete/dissolve/port verdicts
  this wave's exclusion table refers to.

## Verification

Barrier command set, from the repo root, after every wave:

```sh
unset POKETCG_BUILD POKETCG_PORTS
just build && just oracle-diff-all && just data-verify && just oracleb-replay
```

`just oracle-diff-all` also runs `lint-adapters`. Prerequisites: `just
bootstrap` (builds `poketcg/poketcg.gbc` + `.sym`) and `just oracle-venv`
(PyBoy into `/tmp/pbenv`) — both already satisfied in this checkout.

New-behaviour checks, beyond "the suite is green":

0. **Step 0** is verified by its own acceptance block: `CLAUDE.md` resolves
   to `AGENTS.md`, `docs/plan.md` and `docs/README.md` exist, `docs/vision.md`
   has a `## Status` block, `docs/port-contract.md` mentions `vread` and
   mutation testing, `just verify-hooks` exits 0, and `jj status` shows
   `.claude/hooks/*` + `.claude/settings.json` newly tracked. The gate must
   be *unchanged* at 223 routines — Step 0 touches no port.
1. **W1-J**, the only harness change in Wave 1, must be exercised directly.
   With A held, a `ReadJoypad` case with `keys: 0x01` must produce
   `hKeysHeld = $01` and `hKeysPressed = $01` on **both** oracle and C, and
   `keys: 0` must keep the existing `ReadJoypad` cases green. Then W2-K's
   `WaitForButtonAorB` must terminate and return **nc on `keys: 0x01`, c on
   `keys: 0x02`** — before W1-J it cannot terminate at all on the C side, so
   this single case is the end-to-end proof.
2. **Every routine added anywhere in this plan** carries a recorded
   mutation: stub or corrupt it, the diff goes RED, restore, PASS. Report the
   mutation and the red/green counts per routine group.
3. **Routine count** goes 223 → ~387. A number below that means routines
   were silently dropped; list any you excluded and why.

Reporting: one comment per slice on the epic it advances — #6 (duel,
substatus), #5/#18 (tiles, menus), #7 (map), #8 (serial, printer),
#3-successor (save, card_collection) — following the existing comment style
in those threads: what landed, the gate number, the contract defects the
oracle caught, and the explicit exclusion list. #17 closes with W2-K.

## Assumptions & contingencies

- **`.claude/hooks/` and `.claude/settings.json` become tracked files.** The
  repo currently gitignores all of `.claude/`, which is the common convention
  for machine-local editor state — but it is also why the jj enforcement does
  not survive a clone, and enforcement that does not travel is not
  enforcement. Only those three paths are un-ignored; everything else under
  `.claude/` stays ignored.
- **`AGENTS.md` is canonical and `CLAUDE.md` is a symlink to it**, not the
  reverse and not two copies. Symlink, because two files drift and the drift
  is silent.
- **`docs/plan.md` duplicates the wave sections rather than linking to a
  session artifact.** Session `local://` artifacts do not survive a cleared
  context; the tracked file is what a fresh agent can actually read.
- **PyBoy held-button state survives a synthesized call.** Verified
  structurally (`pyboy.py:520,621-625,694-699`: `no_input` only bypasses the
  window plugin, API events reach `mb.buttonevent` at the start of the next
  tick), not yet at runtime. If it does not hold, W1-J reports the failure
  and W2-K's five menu waiters plus the five `print_text` scrollable routines
  stay unported — the other 154 routines are unaffected.
- **`serial.asm` is diffable without a link partner.** If a
  transfer-complete busy-wait makes the oracle time out at `MAX_FRAMES`,
  exclude that specific routine with the timeout recorded as the reason and
  port the rest of the file; do not fake a partner.
- **The 164-routine set was derived mechanically** (transitive closure over
  `call`/`jp`/`jr`/`farcall`/`bank1call` plus fallthrough, against
  `tests/routines.py` and the Phase-1 delete list). Individual routines may
  turn out to reach unported code through a pointer table the sweep could not
  see. Drop such a routine from its slice, record the specific unported
  target, and keep going — do not stub it and do not block the slice on it.
- **Wave 1's slices are file-disjoint by construction**, so concurrent edits
  collide only in `tests/routines.py`, and only in distinct per-file tuples.
  If two slices do collide there, the barrier rebuild is the resolution
  point.
