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

Baseline at the time of writing: `reached_ordinal` 17193 of 70999 (24.22%),
`reached_routines` 457, `executed_routines` 562 of 3009 translated,
`frontier_misses` 370, audits `loops` 38, `banks` 14, `jumps` 4.

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

## Two worklists, not gates

`just completion-composition-audit backedges` and `… stubs` find what the three
ratcheted classes cannot.

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

These two are why a routine can be green on its oracle and still do nothing: a
stub with a `compare: ()` contract and no `read` span passes every check the
substrate has. That is `docs/port-contract.md` item 5 at scale.

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
