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
