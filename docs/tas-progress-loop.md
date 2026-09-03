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

## Running the loop

`docs/grind.md` is the runbook: one row per failure message, one action each,
plus the recipes for the three composition classes and the debugger workflow.
This file stays as the gate's rationale.

Baseline recorded here when the loop was written was ordinal 15,379; the wiring
described below moved it to 17,193. `tools/completion/tas_ratchet.json` holds the
current floor, and the gate exits 3 on any regression.

One ratchet key is not plain-monotone. `executed_routines` counts every routine
the native lane runs, matched against the reference or not, so the only way to
raise it is to execute more code -- including code the ROM never executes at
that point. So an `executed_routines` fall passes only when `reached_routines`
strictly rises in the same run, and the ceiling then drops to the measured
value. Landing `DuelMainInterface`'s body is the case it was written for: the
matched count went 645 -> 649 while the unmatched remainder fell by 69. What
those 69 were was not established -- tracing showed the port spends most of the
movie spinning in overworld movement code either way -- so the claim behind the
rule is only the arithmetic, matched up and unmatched down. Any fall that does
not buy a match is still a regression, and `reached_routines` itself is never
tradeable.

## Why composition needs its own mechanisms

Per-routine verification calls one routine in a synthesized environment, so it
cannot see a defect that only exists between routines. Three classes were
invisible to it and between them kept 85% of the port from ever executing. Each
now has a mechanism, not an audit.

**`farcall` selects the callee's bank; the port used to forget.**
`tools/gen_bank_guard.py` resolves every ported farcall target's bank from
`poketcg.sym` and `src/bank_guard.c` applies it on entry through the function
instrumentation, restoring the caller's on exit. A target entered on its own bank
already is an ordinary same-bank call and is left alone, so a bank the asm
deliberately leaks still leaks. Five hand-found instances
(`DisplayPauseMenu` reading `PauseMenuParams` at `$04:4D98` from bank 1, and the
four bare `farcall X / ret` pause-menu wrappers) are what showed the class was
systematic.

**A routine whose asm never returns must keep its loop.** `LoadMap`'s
`.overworld_loop` (`overworld.asm:54-79`) leaves only when `wOverworldTransition`
gets bit 4 or 6, which no isolated case can arrange, so a faithful C loop used to
hang the probe — which is why it shipped flattened to a single pass, the same
shape as the documented `GameLoop` flattening, and why `HandleOverworldMode` had
never once been called. `frame_boundary_install_watchdog` (`src/home/frames.h`)
now bounds the native lane, with the allowance derived in `tests/test_leaves.py`
from the case's own `cycle_budget` so both lanes read state at the same frame.
It is deliberately separate from the host hook, because
`frame_boundary_is_installed()` means "the runtime host is driving frames" and
eight routines branch on it.

**Computed jumps are resolved at build time.** Deciding at run time by reading
the target's first opcode is wrong: it reads ROM code as data, which the product
pack does not carry. `tools/gen_script_entry_dispatch.py` resolves every target
from `poketcg.sym`, the ROM and `data/map_scripts.asm`, splitting them into
bytecode entries (a lone `rst $20`, interpreted by `RST20(target + 1)`), ported
routines, and the handful with no C body, which abort by name. Only the code
slots of `MapScripts` are entries — slots 0 and 4 are data tables that
`Func_c943` and `HandleMoveModeAPress` walk — and a local label inside a script
counts only when it opens with `start_script`.

`EnterScript` and `CallMapScriptPointerIfExists` still return their target
rather than jumping, because their own oracle cases are captured at the entry
(completion mode `pre-ret`). The consumer that runs past it dispatches:
`HandleOverworldMode`, `Func_c17a` and `HandleMoveModeAPress` each call
`ScriptEntryEnter`, whose returned flags are the carry `FindNPCOrObject` reads.

`just completion-composition-audit` counts what is left of all three, and those
counts are ratcheted.


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
