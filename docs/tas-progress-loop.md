# The TAS progress loop

The runbook for advancing the native port. One number, one ordered worklist, no
judgement calls about what to work on next.

## The gate

```sh
just build-trace                      # instrumented lane, once per source change
just completion-tas-progress          # ~34 s; --skip-run reuses the last trace (~4 s)
```

It replays a 21-minute completion TAS (`build/completion/tas/input.txt`, 78,207
frames) on both lanes and reports how far the port tracks the ROM:

```
reached_ordinal / reference_ordinals   progress_pct
frontier_misses                        blockers[]
```

`reached_ordinal` is the highest reference DoFrame ordinal at which the port still
executes what the ROM executes. It is monotone: a fix either moves it or does not.
At `reached_ordinal == reference_ordinals` with `frontier_misses == 0`, the port
plays the game from boot to the end of the movie.

Baseline when this loop was written: **ordinal 15,379 / 70,999 = 21.66%**, 362 of
898 comparable routines reached, 466 frontier misses.

## Attributing a crash: use the debugger

`gdb` 15.1 is installed and speaks DAP, so a `MISSING_DATA bank:addr` abort is
attributable in about two minutes instead of by inference. Break on
`missing_product_data` (`src/mem.c:469`) and read the backtrace; the caller chain
names the routine, and `poketcg.sym` names what lives at the address.

That loop found three real bugs in one sitting. `DisplayPauseMenu` read
`PauseMenuParams` (`$04:4D98`) with bank 1 selected because the port called
`InitAndPrintMenu` directly where `overworld.asm:1151-1155` uses `farcall`; the
sibling `DisplayPCMenu` 35 lines below had the bank switch and was the model.
`PauseMenu_Status`/`_Diary`/`_Config`/`_Exit` are each a bare `farcall X / ret`
(`overworld.asm:1165-1199`) and all four were missing it, so `StatusScreenLabels`
(`$04:4095`) read from bank 1. `LoadMap` never called `Func_c4b9`
(`overworld.asm:42`).

## Two decisions the loop is blocked on

**1. Non-returning scene loops cannot be probed.** `LoadMap`'s `.overworld_loop`
(`overworld.asm:54-61`) exits only when `wOverworldTransition` gets bit 4 or 6,
which no isolated case can arrange, so a faithful C loop hangs the native probe
at 30 s. The reference lanes are bounded by `cycle_budget`; the native probe has
no equivalent, which is why the routine ships flattened to a single pass with a
bare `return` — the same shape as the documented `GameLoop` flattening. The seam
for a fix already exists: `frame_boundary_install` (`src/home/frames.h:7`), unused
by `src/probe.c`. Giving the probe a frame budget would bound the native lane the
way `cycle_budget` bounds the reference, and would unblock this whole class. It
changes the verification substrate, so it is not a basename fix.

**2. `jp hl` to a script entry needs a derived dispatch table.** `EnterScript`
(`overworld.asm:122-127`) ends in `jp hl` with `hl` from `wNextScript`. Of 247
`Script_*` labels, 212 open with `start_script` (`rst $20`, so they are bytecode
and want `RST20(target + 1)`) and 35 are real code needing a C function — 23 of
those are ported, 12 are not (`Script_dead`, `Script_e61c`,
`Script_Mitch_GiveBoosters`, …). Deciding at runtime by reading the target's
opcode is wrong: it reads code as data, which the product data pack cannot serve,
and it aborts on `00:0000` the moment a null `wNextScript` is reached. The table
must be derived at build time from `poketcg.sym` plus the ROM, like
`ScriptDispatchLookupOpcode` is for opcodes.

Until both land, `HandleOverworldMode` stays unreachable and the gate stays at
its baseline. The wiring itself is proven: with a blocking loop plus an opcode
trampoline, the port ran the overworld, opened the pause menu and drew the status
screen — `LoadMap → HandleOverworldMode → CallHandlePlayerMoveMode →
OpenPauseMenu → PauseMenu → DisplayPauseMenu` — before dying on the null script
pointer. That evidence is why the two items above are the next work, not a
re-diagnosis.

## The loop

1. `just completion-tas-progress --json build/completion/tas/progress.json`
2. Take `blockers[]`. Each row is `{routine, reference_first_ordinal,
   reference_calls, source, basename}` — already the packet a fix agent needs.
   They are sorted by reference ordinal, so the top row is the *earliest* thing the
   port fails to do.
3. Group the top blockers by `basename`. One agent per basename, each owning only
   `src/home/<b>.c`, `src/home/<b>.h`, `src/probe/<b>.c`, `tests/cases/<b>.py`.
   Read `docs/port-contract.md` required coverage, items 4 and 5 especially.
4. Land serially: `just build`, `just oracle-diff <Fn>` per changed routine,
   `just oracle-diff-group <basename>`, then the gate again. Require
   `reached_ordinal` to rise or `frontier_misses` to fall.
5. Repeat.

Work the frontier in order. A defect behind an unreachable gate cannot be observed
and cannot be verified: of thirteen port bugs fixed on 2026-09-02, six were latent
because they were found by byte comparison rather than by progression order.

## Why the blocker list is trustworthy

A reference routine is comparable only if the native binary exports a symbol for
it, which excludes bank trampolines and the local labels the port inlines.

Among those, a routine the ROM first runs at an ordinal the port **already passed**
cannot be what stops it — the port demonstrably got there without it. Those are
reported as `structural_misses` (70 at baseline) and kept out of `blockers`.
Everything at or beyond the frontier is a genuine miss (466 at baseline).

## Supporting tools

| command | use |
|---|---|
| `just completion-trace-diff <scenario> --trace <raw>` | per-routine call-count diff; **positive** deltas are real, negative ones are usually the port expressing a called loop as internal C |
| `just completion-frame-census <scenario>` | earliest anchor ordinal each byte goes wrong, joined to the reference write before it |
| `just completion-writers <scenario> <addrs>` | which reference routine wrote an address, ranked by last write |
| `just completion-reftrace <scenario> --routines A,B` | reference call counts for named routines |
| `just completion-explore --corpus DIR` | coverage-guided input search; writes savestate checkpoints and replay scripts |
| `--load-checkpoint PATH` | inject a reference checkpoint and skip boot, so a subsystem can be exercised before the path to it works. A fixture, never evidence the game works |

## Invariants

- The gate is a progression measure, not a byte measure. Do not substitute the
  scene census for it; the census answers "is this byte right", the gate answers
  "does the game get further".
- Never widen `tools/completion/scenario.py`'s exclusion ledger to move a number.
  Each entry needs an asm citation, and the largest single census movement on
  2026-09-02 (−95 bytes) was an exclusion, not a fix.
- Agent reports are not evidence. Rerun the gate and compare against the claim: one
  agent reported 8 bytes fixed where the rerun measured 5.
- The two references disagree in places. PyBoy is the arbiter for per-routine
  contracts (`docs/port-contract.md`); Gambatte is the arbiter for whole-game
  progression. When they conflict on hardware fabric — TAC's unused bits, `$FF75` —
  the routine contract wins and the census carries the difference.

## The movie

`tools/completion/tas_movie.py` converts any BizHawk `.bk2` and refuses to trust one
whose ROM SHA1 does not match `poketcg/poketcg.gbc`. Two are known good, both
Gambatte-core and both exact ROM matches:

- TASVideos `5530S`, 78,207 frames, BizHawk 1.11.4 — the current input.
- TASVideos `4189M`, 61,687 frames, BizHawk 2.4.1, console-verified. Declares
  `GBC_Firmware_World`, so it needs the CGB boot ROM our lane does not load.

Neither replays to the end in our lane: no credits, booster packs or deck edits on
either, because this is a luck-manipulated run where RNG advances every frame and a
single frame of boot difference shifts every manipulated duel. That costs depth, not
validity — the reference defines truth for whatever input it is given, and 70,999
ordinals is a fixed target. Closing the last stretch needs a boot ROM, not tooling.
