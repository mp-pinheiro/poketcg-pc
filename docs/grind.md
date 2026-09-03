# The grind

Every branch here is a lookup. Work the loop, match the failure to a row, apply
that row's action. Nothing in this file requires a design decision; if you need
one, stop and report (see Stop conditions).

The target is `docs/vision.md`: a native, playable port verified against the ROM.

## Setup, once per session

```sh
cd /home/matheus/git/poketcg
```

Read `docs/port-contract.md` (case coverage, items 4 and 5 especially) and
`AGENTS.md` (file ownership, command table).

Never run `just oracle-diff-all`, `just oracle-release-gate`, a formatter, a
linter, or any `git` command. Commit with `jj` only, naming your own paths:

```sh
jj commit <paths> -m "type(scope): subject"      # subject <= 50 chars, no body
```

Another session shares this checkout. Files you did not change are not yours;
never revert, stage, or commit them.

## The loop

```sh
just build && just build-trace
just completion-tas-progress --json build/completion/tas/progress.json
```

Read `blocked_by` in the output first, then the numbers. The run is measured even
when it aborts: `src/trace.c` flushes the trace on `SIGABRT`, so every iteration
produces comparable numbers.

`native_overflow` must be `false`. The tracer aggregates one count and one first
frame per routine, so a full-movie replay cannot fill it — it is bounded by the
routine count, not the call count. It was a 20,000,000-entry call log until that
cap started binding the headline number instead of the port: two consecutive
gate runs filled it to exactly 20,000,000 and reported ordinals that measured
the buffer. Uncapped, the same tree read 21,337 rather than 21,074, and 694
routines ever executed rather than 645.

Both lanes must also be fed the movie the same way. The reference replays it per
rendered frame and the native loop counter tracks that frame, so `--masks` goes
to both unchanged. `refstream.py axis` re-checks the pairing by measurement, and
says re-indexing the movie onto the DoFrame anchor axis is worse (ordinal
20,212, 583 executed); do not do it.

Baseline at the time of writing: `reached_routines` 607, `executed_routines`
742 of 3009 translated, `frontier_misses` 189, `reached_ordinal` 24677 of 70999
(34.76%), audits `loops` 37, `banks` 14, `jumps` 4.

**`reached_ordinal` is not progress.** It is a max over the reference
`first_ordinal` of every routine the port reached, so one incidental call to a
routine the ROM first runs late sets it arbitrarily high while the port is stuck
far earlier. It reported 66.15% off a single `GoToPreviousCardPage` call
(reference ordinal 46,969) when the port tracked to 24,677, and completing
`SwitchCardPage`'s dispatch removed that call and looked like a 22,000-ordinal
regression while `reached_routines` and `executed_routines` did not move at all.
It is therefore reported but not ratcheted; the two set sizes are the gate. Read
it as a ceiling on depth.

`blockers[]` inherits the same flaw: it drops every miss below `reached_ordinal`
and calls those structural, so an inflated max hides real misses. One
`DisableSpriteAnim` call at reference ordinal 21,337 once hid `StartDuel` and
twenty duel-setup routines at 21,074, and `blockers[0]` pointed at a sprite
routine instead. Read `misses[]` too — the same data unfiltered, so nothing is
silently dropped. Both lists have legitimate rows: `misses[]` is headed by the
bank trampolines the guard dissolved (`BankpopROM`, 24,250 reference calls) and
the inlined audio leaf labels, so triage each row against the asm rather than
taking row zero.

## Decision table

Match `blocked_by`, or stderr from an `oracle-diff`.

| the message contains | what it means | what to do |
|---|---|---|
| `script entry unported name=N` | `N` is a script or map-script entry with no C body | Port `N` in its own basename quartet per `docs/port-contract.md`. Find the asm with `grep -rln "^N:" poketcg/src`. `MasonLabLoadMap`/`MasonLabPressedA` in `src/home/mason_laboratory.c` are the worked examples, including the case matrix. |
| `script entry miss target=$XXXX` | an address the table does not carry | `just build` regenerates the table; if it persists, `grep -i "XXXX" poketcg/poketcg.sym` names the symbol, and it needs adding to `tools/gen_script_entry_dispatch.py`'s inputs |
| `script entry ram opcode=$OO` | a RAM jump stub that is neither `ret` nor `rst $20` | a probe case stubbed a jump destination the dispatcher cannot decode; report it |
| `script opcode miss opcode=$OO` | a script command with no handler | the opcode's handler is named by entry `$OO` of `poketcg/src/data/script_table.asm`; port it in the basename owning that asm file |
| `MISSING_DATA BB:AAAA` and the reading routine's inputs look sane | the pack does not carry that byte, or the bank is wrong | `grep -i " AAAA" poketcg/poketcg.sym` names what is really there. Attribute it with the debugger (below), then apply the **banks recipe** to the frame that computed the address. |
| `MISSING_DATA BB:AAAA` but the reading routine's inputs are garbage | a divergence upstream, not a bank fault | Do not touch banks. The address is a symptom: some earlier routine produced a bad pointer or index. Apply the **divergence recipe**. |
| `HANG no exit within Ns` | a wait loop the port never satisfies | The trace was still written, so `blockers[0]` and the counts are valid. Attribute it by attaching the debugger and reading the backtrace of thread 2: the innermost loop is the wait. Compare its exit condition against the asm; the usual cause is a flag the port never sets. |
| `indirect dispatch miss site=S target=$XXXX` | a RAM function pointer with no case in `S`'s switch | add a `case` for the symbol at `XXXX` to the switch named by `S`; `CallDoFrameFunction` in `src/home/frames.c` is the model |
| `bank guard depth exceeded at` | farcall recursion deeper than 512 | raise `BANK_GUARD_DEPTH` in `src/bank_guard.c` to 2048 and rerun; if it recurs, report |
| `probe timed out after 30 seconds` | a loop no case can exit | apply the **loops recipe** |
| `REGRESSION` with a `key` | your change lowered a ratcheted number | revert your change; do not land it |
| nothing — the run was clean | no abort | take `blockers[0]` from `progress.json` and treat its `routine` as `script entry unported` |

## Attributing a crash with the debugger

`gdb` 15.1 speaks DAP, so a `MISSING_DATA` abort is attributable in about two
minutes rather than by inference. Break on `missing_product_data`
(`src/mem.c`), continue, and read the backtrace. The game runs on thread 2, not
thread 1.

The frame to act on is the shallowest one outside `src/mem.c` — the frames below
it (`rom_ptr_product`, `rom_ptr`, `gb_ptr`, `gb_read8`) are the bus itself and
are never the defect. That frame is the routine that computed the address; read
its local holding the address (`evaluate` with its `frame_id`) and compare it
against the asm the routine was ported from. If it looks right, the bank is
wrong and the defect is in whichever ancestor frame should have switched.

## Finding who wrote a byte

When the address looks right and the bank is right, the byte it was built from
is stale or garbage and the question becomes which routine wrote it. The gdb
*DAP adapter* has no data watchpoints, and a conditional breakpoint on
`gb_write8` is evaluated on every bus access and does not finish a replay. The
gdb *CLI* does have them, which is the shortest route when the address is known
and reachable: stop somewhere near the moment, arm a hardware watchpoint on the
host array, and continue.

```sh
gdb -batch -ex "break src/home/core.c:7817" -ex run -ex "delete 1" \
  -ex "watch g_hram[0x18]" -ex continue -ex "bt 6" --args build-trace/poketcg \
  --headless --data-pack build/completion/data-pack.bin --frames 78207 \
  --input build/completion/tas/input.txt
```

`g_wram` is indexed from `$C000` and `g_hram` from `$FF80`. That named the
writer of `hTempCardIndex_ff98` in one 40-second run, where four rounds of
reading asm had not.

`POKETCG_WATCH` remains the tool for a byte whose *moment* is unknown, since a
watchpoint needs somewhere to stop first.

`POKETCG_WATCH=ADDR:VALUE[/SKIP]` polls that byte at every bus access and aborts
in `watch_hit` (`src/mem.c`) once it holds `VALUE`, so a plain function
breakpoint yields the backtrace. `SKIP` passes over that many earlier matches.
Polling rather than trapping the store is deliberate: most WRAM writes reach
`g_wram` through a `wram.h` macro and never touch the bus, so a store trap misses
them.

```sh
export POKETCG_WATCH=CE40:D1
gdb -batch -ex run -ex "bt 22" --args build-trace/poketcg --headless \
  --data-pack build/completion/data-pack.bin --frames 78207 \
  --input build/completion/tas/input.txt
```

Export it in the shell and run gdb there. The DAP `launch` request's `env` field
does not reach the process, so a watch set that way never arms and the run looks
clean. This named `MapNames`, which the port had at `0x7080` instead of
`03:5153`: `ScriptCommand_LoadCurrentMapNameIntoTxRamSlot` read two code bytes
(`11 D1`) into `wTxRam2`, and `$D111` is not a text id, so the text engine
resolved it to `$7FFF` and read past the end of bank `$0C`.

## Two limits of the `entry` completion mode

`entry` stops both lanes at a named routine's entry, which is the answer to a
`cuts` row whose subject has no reachable `ret`. It does not make every such
row verifiable, and two limits decide whether it helps.

**No register is comparable.** The native lane leaves the routine through a
`longjmp`, so it never produces a return value and the probe reports whatever
the adapter left in `a`/`f`/`d`/`e`. A case using `entry` therefore needs
`compare: ()`, the way `tests/cases/medal.py` already declares it. If the
routine's only observable contract was its exit registers, `entry` buys nothing:
`FriendshipSong_AddToBench50PercentEffect` writes nothing at all before its coin
toss, so stopping there verifies an empty prefix.

**A single pc cannot cover an RNG-chosen exit.** That routine has three
(effect_functions.asm:8809, 8818, 8830) and the toss picks between them. The
toss is pinnable -- the RNG words live at `$CACA` and a case can seed them, as
`TossCoin_BankB`'s own cases do -- and with them zeroed the reference does take
the tails exit at `0b:7127`. What still blocks it is the coin-toss state: `de`
is not preserved across `TossCoin_BankB` (the reference leaves `$12/$11`, not
the prompt id the entry `ldtx` loaded) and `$CAC2` diverges too, so porting the
body needs that routine's register and counter contract established first.
Attempting the body without it produces a red row, not a fix.

**A routine with several exits needs one reachable per case.** `pre-ret` takes a
single pc, but the pc may differ per case, since the completion block iterates
the records: `enumerate(SCHEMA2_CASES[...])` assigns one pc to case zero and
another to the rest. That is what `Prophecy_PlayerSelectEffect`'s two exits
need (effect_functions.asm:4746 at `0b:5A2E`, asm:4754 at `0b:5A3B`), and two of
its three cases pass at the non-turn exit once the body actually calls
HandleProphecyScreen -- which the port omitted, along with the trailing
SwapTurn, and which its pc at that callee's entry concealed.

Case zero reaches neither exit under any seed tried: its own keys, the
three-key timeline the others use, and the non-turn duelvar seeds it lacks. So
it stops mid-flight at HandleProphecyScreen's entry instead, and a mid-flight
stop has no comparable registers -- which used to fail the routine's `a`/`f`
contract and made the row unlandable.

**A case may now narrow its own comparison.** `"compare": ()` on a case entry,
beside its `read` spans, replaces the routine contract's field tuple for that
case alone. It may only narrow -- a superset is rejected, since a case must not
assert fields the routine does not claim -- and the harness prints the narrowed
tuple in that case's result line, so it can never become a quiet exclusion.
`fields` is part of the cache key (`normalize_case`'s `"contract"`), so an
override keys separately and cannot poison a sibling's reference.

That is what a routine whose exits are chosen by input or RNG needs: the cases
that reach a `ret` compare everything, and the one that cannot still compares
its memory spans. Prophecy went 2/3 failing on the stub to 3/3 passing.

**Seed a card list before narrowing it.** Narrowing is the last resort, not the
first: `PokemonTrader_PlayerDeckSelection` also failed to reach its `ret` on
both cases, and two seed bytes fixed it instead. A card-list loop that rejects
non-Pokemon picks cannot terminate on a zeroed duelvars page, because a card
index resolves to a card id through the deck array at `0xC400` and the low card
ids are the energies (`card_constants.asm:1-9`: `$01`-`$07` energy, `BULBASAUR`
`$08` the first Pokemon). Seeding `0xC400`/`0xC401` to `$08` let both cases
reach `0b:788C` and compare every field -- no override needed.

Related: the duelvars page is worth reading before trusting a seed's address.
Card locations are `0xC200`-`0xC23B`, deck cards `0xC27E`-`0xC2B9`, and
`DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK` is `0xC2BA` immediately after them --
which is how the stand-in's invented `gb_write8(0xC2BAu, 0x39u)` was recognised
for what it was: a hand-computed net effect of the two callees the port skipped
(`RemoveCardFromHand` then `ReturnCardToDeck`, one card moving into the deck).

## A hole in the harness that reads the port

Every hiding mechanism found before this one lived in the port or its case
matrix. `PokemonTrader_TradeCardsEffect` had a third kind: its probe adapter
copied all seven registers out of the result struct and then assigned
`s->f = 0x70u` over the top (`src/probe/effect_functions.c`). No case matrix
can catch that -- the matrix is compared against whatever the probe reports, so
the routine's exit flags were unverifiable for the port's life, and widening
cases or seeding harder would never have surfaced it.

`composition_audit.py overrides` now enumerates the class: a probe adapter that
assigns a register constant *after* copying a real result. A constant is
legitimate when the adapter never copied one, which is why the copy must be
seen first. The count is 1 on the pre-fix tree with exact `file:line`, 0 after,
and `overrides` is in `RATCHET_FALLING` at zero so it cannot come back.

The lesson generalises past this audit: when a routine's field disagrees and
the port's chain provably produces the right value, read the probe adapter
before re-reading the asm. Here `ShuffleCards` -> `ShuffleDeck` ->
`ShuffleCardsInDeck` all propagated `f=$C0` correctly and the port still
reported `$70`, which is only possible below the port.

## Push a narrowing down to the routine that owns the gap

The trade row shipped for one turn with `c` narrowed away on a case, blamed on
`PlayDeckShuffleAnimation`. That narrowing is now gone, and the way it closed
is the reusable part: the clobber was derivable after all. Its animation path
ends in `FinishQueuedAnimations` (`script.asm:166`), whose `ZeroObjectPositions`
counts `c` down from `OAM_COUNT` to zero (`objects.asm:76-84`), and whose
closing `BankswitchROM` preserves `bc` (`switch_rom.asm:90-93`). So `c` is
zero, provably, with no measurement.

Two things made it cheap. First, the output belongs on the routine that
produces it, not on the 16 callers of `FinishQueuedAnimations` or the 31 of
`ZeroObjectPositions` -- widening either signature would have churned 47
callsites to move one byte. Second, the gap was path-local: the same routine's
`.one_card_in_deck` branch calls neither of those and its `c` really does come
out of the DoFrame chain unmodelled.

That is what the narrowing hatch is for. `PlayDeckShuffleAnimation`'s contract
now compares `("a", "c")`, its two one-card cases narrow to `("a",)` with the
reason cited, and a third case seeding twelve cards in the deck covers the
animation path and compares `c` with nothing dropped. The gap ends up declared
on the branch that owns it instead of on a consumer two levels up, and the
consumer compares every field again. Restoring `c` as a pass-through makes the
trade row fail, so the derived zero is load-bearing.

## The coin toss `de`: measured, not yet derived

`_TossCoin`, `TossCoin` and `TossCoin_BankB` all pass today, and all three
contracts omit `d` and `e`. That omission is the whole defect class: `de` is
not preserved across a toss, so any caller whose own contract compares those
registers after one fails, which is what stopped
`FriendshipSong_AddToBench50PercentEffect`.

Widening the three contracts is the acceptance test, and it currently fails
2/2, 3/3 and 3/3. The reference leaves **`de = $1211` on every case**, the same
value for heads and tails and for either duelist type.

That constant disproves the obvious model, which I wrote and reverted. The last
`de` writes inside the routine are the SFX block (`core.asm:7988-7992`: `d` the
result sound `$54`/`$55`, `e` the Player-adjusted result) and, on a multiple
toss, the tally draw offset (`:8005-8021`). Both are input-dependent and the
port already computes them as locals, so exposing them is a two-line change --
and it is wrong. `$1211` is input-independent, so `de` is produced *after* the
loop, by the exit chain at `:8066-8068`.

Ruled out by reading, all of them preserving `de`: `_ResetAnimationQueue`
(`animations/core.asm:1-26`) pops `bc` and `hl` but never `de`; `Set_OBJ_8x8`
(`lcd.asm:58-62`), `DefaultScreenAnimationUpdate` (`screen_effects.asm:60-72`),
`_ClearSpriteAnimations` (`sprite_animations.asm:3-36`), `ClearSpriteVRAMBuffer`
(`:480-493`, `c` only), `GetSpriteAnimBufferProperty` (`load_animation.asm:208-225`,
pushes `bc`) and `DisableInt_LYCoincidence` (`scroll.asm:158-166`).
`ClearAndDisableQueuedAnimations` (`animations/core.asm:431-434`) pushes `de`
outright. So the whole exit chain is innocent and the write is inside the loop.

Two measurements narrow it to the audio driver. A temporary case seeding
`wCoinTossNumTossed` non-zero skips the entire text block and still yields
`$1211`, so the text engine is innocent. And `PlayDeckShuffleAnimation`'s
one-card path -- sixty `DoFrame` calls then `ret`, with no `PlaySFX` -- leaves
`de = $0000` (and the `c = $C1` its own narrowing already declares), so
`DoFrame` is innocent too. That leaves `PlaySFX`, a `farcall _PlaySFX` into the
audio driver (`sound.asm:23-25`), as the only remaining `de` writer between the
text block and the proven-clean exit chain.

Note the earlier claim of input-independence is not yet established: every case
may simply have landed the same coin face. Confirm that before assuming one
derivation covers all callers. Either way, do not land `$1211` as a constant --
that is the invented-magic-value shape this session has been removing all along.

Reading registers without a correct port: widening a CONTRACT alone prints
`d: oracle $12 != C $DD`, so the oracle's value at any boundary is readable
without touching a struct, an adapter or the port body. That is how both
measurements above were taken, and it costs one line and one probe run.

## Widening a read span found a real divergence

`ScriptCommand_GiveBoosterPacks` and `ScriptCommand_GiveOneOfEachTrainerBooster`
both cut at `WaitForSongToFinish` (`00:3C96`) under `pre-ret`, which stops the
reference there while the native lane runs on to its own return -- two different
moments. Both now use `entry` mode at `AssertSongFinished`, matching the landed
`GiveBoosterPack`, `ShowMedalReceivedScreen` and `ChallengeMachine_Duel` rows,
and `cuts` fell 14 -> 12.

No discriminator exists for the boundary change itself: both contracts compare
`()` -- registers are not comparable when the routine never returns -- and the
cases observe two TxRam bytes each. Dropping `Func_c2a3` from the body is not
caught, so the boundary switch is correctness by construction, as with the
earlier song-wait rows.

Widening the span is where it got interesting. `wAnotherBoosterPack` (`$D117`)
is written to zero before the first `GiveBoosterPack`, so an `entry` boundary
can observe it even though the routine never returns. Adding it fails both rows
**2/2**: oracle `00`, port `01`. The reference is still inside the first booster
pack at `AssertSongFinished`, before `ld a, TRUE` (`scripting.asm:945`), while
the port has already run past it -- so the port's `GiveBoosterPack` never enters
`AssertSongFinished` on this path and the native stop never fires.

The cause was a truncated body, and it was fixed. `GiveBoosterPack`'s port
stopped at `PlaySong` (`give_booster_pack.asm:38`) with a comment declaring
everything past it unmeasurable, so `pop bc`, `GenerateBoosterPack`, the
`wAnotherBoosterPack` text choice, `WaitForSongToFinish`, `ResumeSong`, the
second scrollable text, `SetDefaultPalettes`, `ZeroObjectPositions`,
`OpenBoosterPack`, `WhiteOutDMGPals` and `DoFrameIfLCDEnabled` were all absent.
With the wait absent, the native lane never entered `AssertSongFinished`, so the
`entry` stop never fired and the port ran on to write `TRUE`. All eleven callees
already existed; the tail is a straight transcription.

**A truncated body is invisible to its own cases.** `GiveBoosterPack` passes 4/4
*with the tail deleted*: nothing it does after the cut is observable at its own
boundary, which is exactly what its comment asserted and exactly why the
truncation survived. The only witness is a caller that runs past the cut --
here the two script commands, whose `$D117` write happens after the callee
returns and therefore straddles it.

So the boundary comment was self-fulfilling: it declared the tail unmeasurable,
which was true of that routine alone and false of the program. When a row's
contract says "nothing past here is measurable", that is a claim about the
chosen boundary, never a licence to stop porting. Check a caller before
believing it.

`composition_audit.py truncated` now enumerates the class by matching its shape
rather than its symptom: an unbroken prefix of the asm's call sequence present
in the body, an unbroken suffix absent. Interleaved gaps are excluded, because
those are a folded branch or an inlined helper rather than a stopped
transcription. It dropped from 36 to 35 the moment `ChallengeMachine_Duel` was
completed, which is the same in-repo validation the `overrides` audit got.

**As first landed it was wrong on a third of its rows, and refining it is what
found the next bug.** The asm parser cannot see local labels, so a `.helper`'s
calls accumulate onto its parent -- and the port decomposes those labels into
its own functions, so the parent's body legitimately does not name them.
`LoadTilemap` read as truncated because all four of its missing callees sit in
`LoadTilemap_InitAndDecompressBGMap`, and `PrintText` because its three sit in
`print_text_body`. The rule that covers both namings: expand through anything
the body calls that is absent from `poketcg.sym`, since only port-local
decomposition can be missing from the symbol table. That took the count 35 ->
24 and removed eleven false positives, including both graphics rows.

Three further false-positive classes remain, all of them judgement rather than
parsing, and none worth detecting:

- **A side-effect-free ROM callee inlined.** `SetupVRAM` is flagged for not
  calling `CheckForCGB`, which is `wConsole`, `cp CONSOLE_CGB`, carry
  (`time.asm:88-93`) -- the port's inline test is exactly equivalent.
- **A pure copy helper inlined.** `FadeScreenFromWhite` is flagged for
  `CopyDataHLtoDE_SaveRegisters`, which its helper replaces with a 128-byte loop
  -- sixteen palettes of eight bytes, the same span, and the callee restores the
  registers it saved anyway.
- **A wait routed through a real sibling.** `PrintKnockedOut` is flagged for
  `DoFrame` because the port calls `DoAFrames(40)` where the asm inlines its own
  `.wait_frames` loop. `DoAFrames` is itself a ROM routine (`00:0536`) whose
  body is that loop, so the behaviour matches; only the routine-entry trace
  differs, by one extra entry the ROM does not make.

So the count is a worklist, not a ratchet, and triage before belief remains
mandatory.

Triage of the three largest rows says the detector measures real work.
`GetAIScoreOfAttack` (91 dropped) is nine body lines, `HandleAIEnergyTrans`
(21) is seven -- and both of its `if` branches return the identical value, so
the condition is dead code shaped to satisfy a boundary -- and
`AIEnergyTransTransferEnergyToBench` (17) is six. These are the duel AI, the
region the TAS never reaches, so nothing else measures them at all.

A fourth class was real and is fixed. `call Other.label` jumps into another
routine's local label, and `ASM_CALL_TARGET` captured only the parent token, so
it recorded a call that was never a call. `ScriptCommand_JumpIfNPCLoaded`
reaches `ScriptCommand_JumpIfEventTrue.pass_try_jump` and the port models that
as `script_jump_event_pass`; both `ScriptCommand_Jump*` rows were phantoms.
Excluding dotted targets took the count 24 -> 21. Across two refinements the
audit went 35 -> 21, so **two of every five rows it first reported were noise**.

**Do not make the reachability transitive through ROM siblings.** Two of the
classes above are only clearable by following calls further than the parent's
own body, so I tried exactly that and measured it against the three AI rows as
positive controls, since those are known real truncations:

| hops through the port call graph | rows | controls kept |
| --- | --- | --- |
| 1 | 30 | all three |
| 2 | 17 | one |
| 3 | 15 | one |

Past one hop the closure swallows `GetAIScoreOfAttack` and
`AIEnergyTransTransferEnergyToBench` -- it stops measuring truncation and starts
measuring whether a name appears anywhere nearby. The landed rule is therefore
the right shape and stays: unbounded through *port-local* helpers, which are the
same routine split up, and never through a ROM sibling, which is a different
routine the port chose to call.

One implementation note, because it nearly cost a machine. The first attempt
accumulated each helper's body text into a growing string; that is quadratic in
total source size across ~3,000 bodies and had to be killed after two minutes.
Building the call graph once with a single `findall` per body and closing over
the graph instead runs in 0.3 s. Reachability questions on this tree are graph
problems, not string problems.

**The three AI rows were blocked on a register contract two levels down, and
that contract is now landed.** `AIEnergyTransTransferEnergyToBench`
(`pkmn_powers.asm:269-402`) branches on the carry of
`AIProcessButDontPlayEnergy_SkipEvolutionAndArena` twice, at `:289` and `:373`.
That routine returned `void`, and its asm ends `jr AIProcessEnergyCards`
(`energy.asm:66`) -- a tail jump, so the callee's flags are its exit -- and
`AIProcessEnergyCards` returned `void` too. All nine other callees of the AI row
already existed with real signatures; this one register was the whole
obstruction, and porting 143 asm lines on top of an unmodelled carry would have
been a guess dressed as a port.

`AIProcessEnergyCards`' exits are now enumerated, and the wrapper's half of the
contract is fully derived. The routine has one `ret` and four exit paths
(`energy.asm:265-285`):

- highest score found and `wAIEnergyAttachLogicFlags` non-zero: `scf` then
  `jp RetrievePlayAreaAIScoreFromBackup1`, which is `push af` ... `pop af; ret`
  (`:71-85`) and so preserves flags -- **carry set**
- none found and flags non-zero: the same tail jump with no `scf`, reached past
  `or a` -- **carry clear**
- none found and flags zero: `or a; ret` -- **carry clear**
- found and flags zero: `.play_card`, `jp AITryToPlayEnergyCard`

All three `AIProcessButDontPlayEnergy_*` wrappers write a non-zero flag byte, so
only the first two paths are reachable through them and their carry is exactly
"a card was chosen". The asm says so itself at `energy.asm:22-23`, and
`FindPlayAreaCardWithHighestAIScore` already returns an `f` the port can read.

The fourth path closed too, and no placeholder was needed. Its carry is
`AITryToPlayEnergyCard`'s, and enumerating that routine's five exits shows the
carry is set on exactly one of them: `.play_energy_card` ends `scf; ret`
(`energy.asm` relative `:138-145`), while `:61` and `:70` leave via `ret nc` and
`:154` and `:159` return straight after an `or a`, which clears carry. The
routine's own comment states it. The port's existing `uint8_t` return is already
that boolean -- `1` on the play path, `0` on every other -- so it was the carry
all along, merely typed as a value.

So `AIProcessEnergyCards` now returns `AIEnergyResult { f }`, the two
`AIProcessButDontPlayEnergy_*` wrappers return it unchanged because they tail
jump, and the three contracts compare `f` where they compared nothing.
Inverting the `scf` path fails `AIProcessEnergyCards` 2/2, so the carry is
discriminated rather than coincidentally agreeing. The wrappers' own two cases
do not reach that path, so their carry rests on the callee's proof plus a
one-line tail jump -- worth knowing before trusting them alone.

Only `f` is modelled. `a` at exit differs per path and has no consumer, so
inventing a value for it would have been the same defect in a smaller costume.

**That carry was not the last obstruction: `a` is.**
`AIEnergyTransTransferEnergyToBench`'s contract compares `("a", "f")`, and its
six exits split by whether `a` is derivable:

- `pkmn_powers.asm:273` `ret nc` -- `a` is CheckIfDefendingPokemonCanKnockOut's,
  which its result already carries
- `:285` `ret z` after `ld a, [wAttachedEnergies + GRASS]` / `or a` -- `a` is
  zero on that path by construction
- `:311` `ret z` -- `a` is the loop counter `b`, which reached zero
- `.done_transfer` -- `a` is AIMakeDecision's, already modelled
- `:278` `ret c` -- `a` is AIProcessButDontUseAttack's, and
  `AIProcessAttacksResult` carries only `f`
- `:289` `ret nc` -- `a` is the wrapper's, and `AIEnergyResult` carries only `f`

The last two are the blocker, and tracing it further this turn made it deeper,
not shallower. `AIProcessButDontUseAttack` tail-calls `AIProcessAttacks`
(`attacks.c:132`), whose four exits are:

- `.attack_chosen` with `wAIExecuteProcessedAttack` non-zero: `scf` then
  `jp RetrievePlayAreaAIScoreFromBackup2`, which is `push af` ... `pop af`
  (`attacks.asm:26-35`) -- `a` is the flag byte just loaded, **derivable**
- `.dont_attack` with that byte non-zero: the same tail jump without `scf` --
  **derivable**
- `.failed_to_use`: only `inc [hl]` and `or a` follow, neither touching `a`, so
  it is that byte, zero on this path -- **derivable**
- `.use_attack`: `call AITryUseAttack` then `scf; ret` -- `a` is the callee's

So three of four derive, and the fourth descends again: `AITryUseAttack`
(`ai/core.asm:133`) has three exits and every one returns straight out of
`AIMakeDecision`.

**`AIMakeDecision` is the bottom, and it is now landed.** Its three exits are
each derivable from bytes the port already computes (`core.asm:6229-6263`):

- `.turn_ended` -- `a` is the `wDuelFinished | wOpponentTurnEnded` OR the branch
  itself tested, so it is non-zero by construction
- the `ret nz` -- `a` is the re-read `wSkipDuelistIsThinkingDelay`, which the
  dispatch may have set, non-zero on this path
- the fall-through -- `a` is `DrawWideTextBox_PrintTextNoDelay`'s own `a`, and
  `TextResult` already carries it

`AIMakeDecisionResult` gained `a`, the probe adapter reports it, and the
contract compares `("a", "f")` where it compared only `f`. Zeroing the
fall-through fails 1/6, so it discriminates. `core` stays 369/371, the two
pre-existing failures bisected earlier as not mine.

The attack side above it is now threaded and proven.
`AITryUseAttackResult` gained `a` -- all three of its exits already held the
`AIMakeDecisionResult` they return from -- and `AIProcessAttacksResult` gained
it too: the two flag tests leave `a` as the `wAIExecuteProcessedAttack` byte
they read, `.failed_to_use` is that byte at zero, and `.use_attack` takes
`AITryUseAttack`'s. Four contracts moved from comparing `f` to `("a", "f")`,
the probe adapters report it, and zeroing the `.attack_chosen` value fails
`AIProcessAttacks` 2/4. `attacks` 5/5, `core` 369/371.

That closes `AIEnergyTransTransferEnergyToBench`'s `:278` exit, and `:289` is
closed now too -- along with every link below it. The last two unknowns turned
out not to be unknowns: `CheckIfEvolutionNeedsEnergyForAttackResult` and
`GetEnergyCardForDiscardOrEnergyBoostAttackResult` both already carry `a`, so
all five of `AITryToPlayEnergyCard`'s exits derive -- the two `ret nc` paths
from those callees, `.play_energy_card` from `AIMakeDecision` with the trailing
`scf`, and the two `or a` exits from the `wTempAI` and `wSelectedAttack` bytes
they tested (`energy.asm` relative `:61-159`).

So `AITryToPlayEnergyCard` returns `{ a, f }` instead of a bare `uint8_t`, and
`AIEnergyResult` gained `a`: the `wAIEnergyAttachLogicFlags` byte the `or a`
tests read on the three flag-dependent paths, zero on the no-flags exit, and
the play path's own `a`. Six call sites cut over -- `core.c`, the three
legendary handlers, `AIProcessEnergyCards` and the probe adapter. Zeroing the
`scf` path's `a` fails `AIProcessEnergyCards` 2/2. `energy` 12/12, `attacks`
5/5, `core` 369/371.

Two process notes from landing it. First, widening the contracts *before*
patching the probe adapters produced `a: oracle $02 != C $AA` -- the `$AA` being
the poison case's seeded input, still sitting in `s->a` because the adapter
reported only `f`. A new output is unobservable until the adapter carries it,
and the failure looks like a wrong derivation rather than a missing wire.

Second, the gate caught a `loops` regression, 36 -> 37, on
`AITryToPlayEnergyCard`. It was not behavioural: `audit_loops` flags a `return`
at two-tab depth followed by two closing braces as a fake loop, and the braced
blocks I wrapped the new locals in made exactly that shape. Hoisting the two
declarations to the function head flattened it back. The ratchet earned its
keep on a change that every per-routine oracle called clean.

**The first AI body is landed.** `AIEnergyTransTransferEnergyToBench`
(`pkmn_powers.asm:269-402`) is ported in full: the Venusaur Lv67 search down the
play area, the transfer loop that rescans the deck for a Grass energy still on
the Arena card each pass, the 30-frame and 60-frame waits, and all six exits
returning the registers derived over the previous three turns. `truncated`
17, `pkmn_powers` 11/11, `loops` 36, gate exit 0.

**Its two cases do not reach past the first exit, so the body is unverified.**
Inverting the very first condition -- `CheckIfDefendingPokemonCanKnockOut`'s
carry test -- still passes 2/2, which is the proof that everything after it is
dead as far as the matrix is concerned. There is no completion pc cutting it;
the seeds simply stop there.

A discriminating case has to satisfy four things at once, which is why none
exists yet: `CheckIfDefendingPokemonCanKnockOut` returning carry, then
`AIProcessButDontUseAttack` returning *no* carry, then a non-zero Grass count at
`$CC1C`, then `AIProcessButDontPlayEnergy_SkipEvolutionAndArena` returning carry
-- and it must also afford the 30- and 60-frame `DoFrame` waits inside its frame
budget. Until then this row is in the same position as
`ChallengeMachine_Duel`: a literal transcription whose callees all exist, landed
because leaving the truncation is worse, and honestly not proven.

**Attempted and failed: seeding a way into that body.** The obvious lever is
the turn duelist's arena HP -- `CheckIfDefendingPokemonCanKnockOut` asks whether
the Defending Pokemon's attacks reach it -- so I added a case with
`DUELVARS_ARENA_CARD_HP` on page `$C2` set to ten, otherwise identical to the
existing seed. It passes 3/3, and inverting the first condition *still* passes
3/3, so the new case exits in the same place as the other two. Reverted rather
than kept: a case that implies coverage it does not have is worse than no case.

Two things were learned that are worth more than the attempt cost. First, the
old stub passed **by coincidence**: marking the first exit with a sentinel shows
the reference returning `a=$00, f=$80`, which is exactly what
`CheckIfDefendingPokemonCanKnockOut` hands back there -- and also exactly what
two of the deeper exits return. Sentinel-marking each exit in turn is a cheap
way to learn which one the reference actually takes, and it is how this was
settled: markers on the grass-count and Venusaur-not-found exits leave the row
passing, so neither is reached.

Second, the note already sitting beside `HandleAIEnergyTrans` -- that the deeper
paths "drive live duel state and are not reproducibly exitable from this
schema" -- is correct, and now has evidence behind it rather than assertion. The
predicate needs the defending card's attack data loaded and a damage estimate
computed, which is further than a wram seed list reaches. Verifying these bodies
wants a duel state captured from a running game, not a hand-written seed; that
is a different instrument from the case matrix and should be recognised as such
before more turns go into seeds.

**`$CD0F` disagreed, and the cause was the key timeline, not the port.** I
wrote this up as a live lead and it was wrong; here is the correction.

`PlayerPickFireEnergyCardToDiscard` skipped `HandleEnergyDiscardMenuInput`
entirely (`effect_functions.asm:3517-3524`) and synthesized a `$90` exit; the
two trailing `ldh` moves set no flags, so the exit flags are the handler's and
only `a` is the card index it leaves in `hTempCardIndex_ff98`. Fixed, row green,
`truncated` 17 -> 16.

Observing the cursor counter then failed in the *opposite* direction -- port
`01`, reference `00` -- which looked like the reference resetting the counter
somewhere the port does not. It is not. The no-A/B path returns through
`RefreshMenuCursor_CheckPlaySFXRegs` (`menus.c:681`, `menus.asm` past
`.check_A_or_B`), which increments; with the case's two-entry timeline
`[0x00, 0x02]` the first poll sees no keys, so exactly one refresh happens
before B registers, and the two lanes do not poll in step. Reseeding the case
with a constant B press makes the counter agree and the row pass with the span
in place, which is the proof.

But that same configuration destroys the instrument: with B held from the first
poll neither lane ever refreshes, so the counter is zero whether the handler
runs or not. `$CD0F` can therefore expose the parity seam or discriminate the
call, never both at once, and for this row it cannot do the second. Both the
span and the reseed were reverted; the faithful call stays, landed unproven.

The general shape is worth remembering: a byte that only moves inside an input
loop is hostage to the timeline that drives the loop. `hKeysHeld` had the same
problem earlier in the session. Prefer an observation the routine writes
*outside* its wait loop.

## Three ROM routines are implemented twice

`duel_animation_core.c` carries its own copies of routines that already exist
ported elsewhere, and one of them has drifted. This is the `music1`/`music2`
class again, found this time by the `truncated` audit rather than by a bug
report.

`_UpdateQueuedAnimations` was flagged for not calling
`PlayBufferedDuelAnimations`. It does not call it because the file defines a
file-local `play_buffered_duel_animations` that reimplements it. The two are not
equivalent:

- the copy advances `wDuelAnimBufferCurPos` *after* the eight field copies;
  `core.c:2281` advances it before
- the copy returns a re-read of `wDuelAnimBufferCurPos` on both exits, where the
  real routine returns `CheckAnyAnimationPlaying`'s `a` on the carry exit
  (`core.c:2293-2299`) and only the buffer position on the drained exit

So the copy is wrong on the carry path. `PlayBufferedDuelAnimations` has its own
cases and passes; the copy has none, because nothing knows it exists.

Cutting `_UpdateQueuedAnimations` over to the real routine needs `core.h`, and
including it fails to compile: this same file also defines
`GetAnimCoordsAndFlags` and `LoadAnimCoordsAndFlags` with signatures that
conflict with the ported declarations. That is three duplicated ROM routines in
one file, so the fix is a file-scoped de-duplication rather than a one-line
redirect, and it was left un-attempted rather than half-done.

What makes this worth its own section: no oracle case can find it. Both
implementations are reachable, both are green where they are tested, and the
divergence only appears when the two are compared against each other. The
`truncated` audit found it as a side effect of asking a different question --
which is the third distinct defect class that audit has surfaced, after the
stopped transcriptions and the invented writes.

`composition_audit.py shadows` now enumerates the class directly: a name that
`poketcg.sym` knows as a ROM routine and that the port defines in more than one
`src/home/*.c`. It reports the routine and both `file:line` sites, and it is in
`RATCHET_FALLING`, so the count can only go down.

It found five, and four of them are `static` reimplementations shadowing a
routine that exists ported elsewhere:

| routine | shadow | real |
| --- | --- | --- |
| `ApplyStatusConditionToArenaPokemon` | `duel_core.c:135` | `core.c:3543` |
| `DefaultScreenAnimationUpdate` | `duel_animation_core.c:66` | `screen_effects.c:104` |
| `EnableAndClearSpriteAnimations` | `duel_animation_core.c:74` | `load_animation.c:253` |
| `GetAnimCoordsAndFlags` | `duel_animation_core.c:41` | `core.c:2246` |
| `LoadAnimCoordsAndFlags` | `duel_animation_core.c:56` | `core.c:4836` |

`EnableAndClearSpriteAnimations` is fixed and is the proof the audit tracks
removals: 5 -> 4. Its shadow called `_ClearSpriteAnimations` directly where the
real routine calls `ClearSpriteAnimations`, i.e. it skipped the bank switch the
wrapper performs. Deleting it and including `load_animation.h` leaves
`duel_animation_core` 5/5 and `load_animation` 15/15 clean.

The other four are not one-line redirects and should not be treated as such.
Two have different signatures from the routine they shadow --
`LoadAnimCoordsAndFlags(uint8_t slot)` against `LoadAnimCoordsAndFlags(void)`,
and `ApplyStatusConditionToArenaPokemon(uint8_t, uint16_t *)` against a
three-argument form -- so each needs its callers read before deciding whether
the shadow is a mis-named helper or a genuine second implementation. Sizing that
is what the ratchet is for; guessing is how the `music1` fork survived.

**A seed can hide an invented write.** `ComputerSearch_PlayerDeckSelection`
skipped `.loop_input` (`effect_functions.asm:9478-9482`) and substituted three
things the asm never does: `wLCDC = $80`, `hKeysPressed = $01`, and reading the
chosen card out of `wDuelTempList`'s first entry instead of taking
`DisplayCardList`'s no-carry return. Its two cases already observe `$CABB` and
`$FF91`, so they should have caught the first two outright -- except
`DISPLAY_SEED` and `DISPLAY_KEYS` seed those addresses to `$80` and `$01`, so
each invented write stores the value already there and is invisible.

That is a new way for a case to fail to discriminate, distinct from the earlier
ones: the span is right, the case reaches the code, and the write is still
unobservable because the seed pre-agrees with it. When a fix deletes an invented
write, check the seed for that address before concluding the observation is
sound. The loop is landed as a transcription that deletes invented state; 2/2
pass both before and after, and no discriminator was found.

`HandleAIEnergyTrans` is the same wait and stays a stub for the same reason. Its
two identical `if` arms are gone: both returned the same value, so the condition
was dead code that read as a modelled branch. Removing it changes no behaviour
and removes the disguise.

`ChallengeMachine_Duel` was the second row of that class and is fixed --
`challenge_machine.asm:177-181`, the song wait, the `wSongOverride` clear,
`SaveGeneralSaveData` and `StartDuel_VSAIOpp`, the duel entry itself, all
absent. **No discriminator exists for it, unlike the booster row.** Its own
three cases pass with the tail deleted, as the class predicts, and the caller
trick does not transfer: `ChallengeMachine_Start`'s reference stops at
`04:71EE`, early in its own body and before `call ChallengeMachine_Duel`
(`:67`), so nothing it observes straddles that return. An SRAM span over
`sPlayerInChallengeMachine` -- written `$ff` before the call and `0` at
`.resume_challenge` right after, the exact `$D117` shape -- passes either way
for that reason, so it was reverted rather than kept as decoration. The tail is
landed as a literal transcription of four asm lines whose callees all already
existed; that is the whole of its justification.

`HandleNoDamageOrEffect` was the row the refinement exposed, and this one is
proven. The asm's `call nz, DrawWideTextBox_PrintText`
(`effect_functions.asm:454-461`) was absent: the port synthesized the exit flags
and never drew the box. Its flags happen to be right -- carry from the trailing
`scf`, `Z` only on the zero text id, and `TextResult` carries no `f` -- so the
observable loss was the box itself and the callee's `hl`.

All four existing cases were structurally unable to reach that call, which is
why nothing detected it. `CheckNoDamageOrEffect` (`substatus.asm:451-474`) exits
at `ret z` when `wNoDamageOrEffect` is zero, and takes `.dont_print_text` with
`hl = 0` when bit 7 is already set; the cases seeded only `$00` and `$80`, one
of each. A fifth case seeding `$01` -- any `NO_DAMAGE_OR_EFFECT_*` with bit 7
clear -- is the first to pass the guard, and it discriminates on `wLCDC`
(`$CABB`), which `DrawWideTextBox_PrintText` writes via `EnableLCD`
(`menus.asm:788-797`). 1/5 fails before, 5/5 passes after.

Two spans went in before that one and neither discriminated: `$D41C`, which was
simply the wrong address for `wLCDC`, and then the right address on cases that
still could not reach the call. Check that a case can reach the code before
concluding a span is useless.

`SetDefaultConsolePalettes` is the same story on the console axis rather than
the flag axis. Its SGB arm was a bare `return`, so the frame type, the packet
build and `SendSGB` were all absent (`core.asm:4158-4170`). No case seeded
`wConsole = CONSOLE_SGB`: two cases used DMG and one CGB, so the arm was
unreachable by construction and could stay empty indefinitely.

The ROM settled the one ambiguity rather than rgbasm precedence guessing. In
`ld a, PAL01 << 3 + 1` with `PAL01 = $00` the header byte is `$00` or `$01`
depending on how `<<` and `+` bind; the bytes at `01:5B28` read `3E 01`, so it
is `$01`. The rest of the block confirms the shape outright -- `11 6C 5B` the
source, `0E 0E` the count, `71` (`ld [hl], c`) the terminator using the zero the
copy loop leaves in `c`. The packet data is read from ROM at `01:5B6C` rather
than transcribed, matching what the CGB arm beside it already does with
`CGBDefaultPalettes`. A fourth case seeding SGB and observing the 16 packet
bytes fails 1/4 before and passes 4/4 after.

`ShowCardPopCGBDisclaimer` is the reachable-arm variant, and shows that a
reachable arm is not the same as an observed one. Its cases already seeded
`wConsole = $00` with keys, so all three DMG cases ran the arm -- yet the port
dropped `call WaitForButtonAorB` (`start.asm:399`) and returned a bare `$10`,
and the cache and VRAM spans could not tell. The notice therefore flashed past
without waiting for input on every DMG and SGB console.

The discriminator is one byte. `WaitForButtonAorB` calls `RefreshMenuCursor`,
which increments `wCursorBlinkCounter` (`$CD0F`) once per frame
(`menus.asm:173-176`), so observing it separates running the wait from skipping
it: 3/4 fail before, 4/4 pass after. The exit is the callee's `Z` with carry
forced on, since `scf` clears N and H and leaves Z alone.

## When the divergence is the movie, not the port

`5530S` is luck-manipulated: the RNG advances every frame, so the hand a duel
deals depends on the whole frame history before it. Once the port reaches a duel,
a divergence can therefore be a desync from the movie rather than a defect, and
it looks like a livelock: the ROM's cursor sits on a card the player may select
and the port's does not.

The initial Pokemon placement is the worked example. The port stalls in
`DisplayPlaceInitialPokemonCardsScreen` because every card it offers is judged
non-basic, and all five routines on that path match the asm line for line
(`DisplayCardList`'s branches, both `GetCardInDuelTempList` variants,
`IsLoadedCard1BasicPokemon`, `CardListItemSelectionMenu`). `Random` is called 8
times on both lanes and `ShuffleDeckAndDrawSevenCards` twice, so the shuffle is
not missing; the permutation differs.

Recognise the shape before spending a session on it: a routine on the stalled
path whose native and reference call counts differ by a factor rather than being
zero, with every routine on that path matching its asm. Closing this class needs
a movie our lane can replay from boot, not more porting -- `4189M` declares
`GBC_Firmware_World` and needs the CGB boot ROM we do not load.

## The banks recipe

The asm reaches a routine in another bank one of two ways.

`farcall` / `bank1call` is already handled: `tools/gen_bank_guard.py` gives every
ported farcall target its own bank on entry and restores the caller's on exit,
so a missing switch at a farcall site cannot happen. Do not add one by hand.

A manual `ld a, BANK(X)` / `call BankswitchROM` must be reproduced in the C:

```c
uint8_t saved_bank = hBankROM;
BankswitchROM(0xBBu);          /* BANK(X), read from poketcg.sym */
...
BankswitchROM(saved_bank);     /* only where the asm restores it */
```

`DisplayPCMenu` in `src/home/overworld.c` is the model. `just
completion-composition-audit banks` lists every routine still missing one.

## The divergence recipe

When a routine reads a garbage address, the routine is usually correct and its
input is not. Walk backwards to the producer rather than patching the reader.

For the overworld script interpreter, the producer is almost always a command
that advanced `wScriptPointer` by the wrong amount, which leaves the next fetch
mid-command. Establish the truth first, then compare:

1. Read `wScriptPointer` ($D413) at the failure and the script entry the run
   came from (`target` in `ScriptEntryEnter`'s frame).
2. Derive the real command boundaries from the asm: each `ScriptCommand_X` ends
   in `IncreaseScriptPointerByN`, resolved through tail-jumps
   (`jr`/`jp` to a helper). Walk from the entry, adding each `N`.
3. If the failing pointer is not one of those boundaries, one command advanced
   wrong. Break on `IncreaseScriptPointer` with a condition on the offending
   `low` byte and read `a` — the requested advance — plus the backtrace, which
   names the command that asked for it.
4. If the command named there is not the one the asm has at that address, the
   *opcode fetch* read the wrong bank, not the wrong address: compare the byte
   the port saw against that address in each bank to identify which bank leaked,
   then fix whatever selected it (see the banks recipe).

That last step is how the audio leak was found: the interpreter fetched an
opcode out of bank `$3D` because the sound wrappers did not restore the caller's
bank, so `CloseTextBox` was dispatched as `SetChallengeHallNPCCoords` and
advanced 3 instead of 1.

## The loops recipe

A routine whose asm never returns must not be flattened to a single pass with a
bare `return` — that is what kept the overworld from ever running. Restore the
loop:

1. Find the back-edge in the asm (`jr .label` / `jp .label` to a label above).
2. The C `do { … } while (cond)` condition is the back-edge condition, negated
   exactly as the asm negates it.
3. Every `ret` or `jr` leaving the loop body becomes `return` or `break` at the
   same statement. Change nothing else.

`LoadMap` in `src/home/overworld.c` is the worked example
(`overworld.asm:54-79`). `just completion-composition-audit loops` lists the
candidates.

The probe bounds such a routine by frames, so it no longer hangs: the allowance
is derived from the case's own `cycle_budget` with the arithmetic that bounds
PyBoy, and the response reports `frame_budget_reached`. If a restored loop times
out, its cases need a `cycle_budget`; copy the value `EnterScript`'s cases use in
`tests/cases/overworld.py`.

## Landing rule

For every fix, in order:

```sh
just oracle-diff <Fn>                 # per changed routine -> PASS
just oracle-diff-group <basename>     # -> N/N routines clean
just build && just build-trace
just completion-tas-progress --json build/completion/tas/progress.json
```

Land only if `reached_ordinal`, `reached_routines` or `executed_routines` rose,
or an audit count fell. Then raise the ratchet and commit it with the fix:

```sh
just completion-tas-ratchet
jj commit <your paths> tools/completion/tas_ratchet.json -m "fix(scope): subject"
```

A batch that moves nothing was not the cause. Revert it and take the next row.

## Stop conditions

Report rather than improvise when any of these holds:

- the same `blocked_by` survives two consecutive fixes;
- a fix needs `tools/completion/scenario.py`'s exclusion ledger widened;
- a fix needs a file outside your basename's quartet plus the ratchet file;
- the gate reports `reference_ordinals` other than 70999;
- a routine's oracle case disagrees with the asm and you cannot tell which is
  right.

## Why the numbers are trustworthy

Per-routine verification is blind to composition by construction: it calls one
routine in a synthesized environment, so a missing bank switch, an undispatched
computed jump, and a flattened scene loop all pass it. Those three classes are
what kept 85% of the port from ever executing. Each now has a mechanism rather
than an audit — the bank guard, the generated script entry table, the probe frame
budget — and the residual counts are ratcheted so they cannot grow back.

## Three worklists, not gates

`just completion-composition-audit backedges`, `… stubs` and `… cuts` find what
the three ratcheted classes cannot.

**`backedges`** lists routines whose asm branches backwards but whose C has no
loop construct at all. That is not the same shape as `loops`, which finds a loop
flattened *in place* (`for (;;) { … return; }`); a loop replaced by an `if` has
no loop syntax to detect. `ExecuteGameEvent` was exactly that — `map.asm:31-35`
loops event → `LoadMap` → event, the port ran it once, and the whole duel engine
sat behind it. 99 rows today, 23 of which the ROM executes on the TAS.

**`stubs`** lists routines with at least 8 asm instructions and at most one C
statement. 55 rows today. Each row carries `asm_calls`, `c_calls` and
`dropped_calls`: routines the asm calls that the C body does not. Rank by that,
because statement count alone cannot separate missing work from a transform that
condensed the asm legitimately — `SwapTurn`'s eight instructions are seven
push/pop and one assignment, and it is a complete port.

Neither is ratcheted, because both have legitimate rows. A back-edge is absent
from the C when the asm loop was hardware the Phase 1 transform deletes
(`DisableLCD` spinning on `rLY`) or arithmetic a C operator expresses directly.
A one-statement body is right when it delegates to the routine it wraps, which
is also why `dropped_calls` over-counts a delegation: `ProcessText` calls
`process_text_core`, and the five calls the asm makes live one level down. Triage
each row against the asm, and order the work by whether the ROM executes the
routine: cross-reference `build/completion/tas/ref-5530b.json`, whose `calls`
entries carry `count` and `first_ordinal`. Ten rows with dropped calls are
executed on the TAS, and the four largest — `MainDuelLoop` (34),
`DuelMenu_Attack` (18), `DisplayPlayAreaScreen` (15), `OpenPlayerHandScreen`
(8) — are the duel engine.

**`cuts`** lists `factory-completion` overrides whose `pre-ret` pc is the entry
of a routine the subject calls, directly or one level down. The oracle then
stops on the first such call, so the contract covers only what runs before it —
which is exactly where a stub ends. A pc outside the routine's own span is
legitimate when the asm tail-jumps, so this is a worklist and not a gate; 27
rows today.

The duel entry chain was four of them. `StartDuel`'s pc was `SetupDuel`'s entry
(`core.asm:59`, its first call), `StartDuel_VSAIOpp`'s and `GameEvent_Duel`'s
were `LoadPlayerDeck`'s. Each cut the reference exactly where the C stub's last
write was, so `void StartDuel(uint16_t) { wCurrentDuelMenuItem = 0u; }` and its
three stubbed siblings passed for the life of the port while the entire duel
engine sat unreachable behind them.

`Duel_Init` was the fifth, cut inside `WaitForSongToFinish`. Six routines share
that shape, because the wait only ends when `wCurSongID` reaches `$80`
(`music1.asm:73-79`) and a looping song never gets there. The way out is a theme
id past `NumberOfSongs1`: `music1.asm:36-39` then skips the `wCurSongID` write,
the seeded `$80` survives, and the wait returns on its first pass.

These three are why a routine can be green on its oracle and still do nothing: a
stub with a `compare: ()` contract, no `read` span, and a completion pc at its
own first call passes every check the substrate has. That is
`docs/port-contract.md` item 5 at scale.

## Clearing stubs: bottom-up only

A stub high in a call tree cannot be verified until its callees exist, so the
`stubs` worklist must be worked from the leaves up. Measured the hard way on
`MainDuelLoop`: the port against `engine/duel/core.asm:73-218` compiles and is
faithful, and it still cannot pass, because `MainDuelLoop` always runs
`HandleTurn` before it tests `wDuelFinished`, and `HandleTurn`'s subtree is
itself stubbed (`HandleBetweenTurnsEvents` is empty, `DisplayPlayAreaScreen`
and `DuelMenu_Attack` are one-liners). The probe times out with no frame
boundary to bound it. That work was reverted rather than landed red.

Order a subtree by callee depth, not by how important the routine looks. For
the duel engine that means the leaves in `core.c`, `effect_functions.c` and
`trainer_cards.c` first, and `MainDuelLoop` last.

Expect to rewrite the case matrix of every stub you fill in. A stub's cases were
authored against the stub: `MainDuelLoop`'s two cases seeded `wLCDC` and
expected `EnableLCD`'s `$80`, which the body `{ EnableLCD(); }` satisfies
trivially, and its mutation receipt corrupted that same call. Both passed for
the life of the port. Re-derive the matrix from the asm's branches, and retarget
the mutation at a line the real body owns.
