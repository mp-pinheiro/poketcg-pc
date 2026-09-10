# The grind

Every branch here is a lookup. Work the loop, match the failure to a row, apply
that row's action. Nothing in this file requires a design decision; if you need
one, stop and report (see Stop conditions).

The target is `docs/vision.md`: a native, playable port verified against the ROM.

## The prompt

Paste this into a fresh session. It is the whole brief; everything else is a
lookup in this file.

```text
Advance the poketcg-pc native port by working its issue tracker.

Read completely, in this order:
  docs/grind.md          <- the runbook; authoritative. "Issues: the worklist" first,
                            then "The session loop" and its decision table
  docs/port-contract.md  <- case coverage, items 4 and 5 especially
  AGENTS.md              <- file ownership and the command table

Before the loop, once: export POKETCG_BUILD=build-<your name> POKETCG_SESSION=<your name>
(a private build directory; the tracker's claims carry the name). just build.

The loop, until a stop condition in docs/grind.md holds or issues-next is empty:
  1. just issues-next 1 --claim         # the fact to work, marked yours; its body has the repro
  2. run the repro; match the output to a decision-table row and do what it says
  3. land it:
     - the routine's C follows its asm (the asm is the truth, never the case or the C)
     - a fixture case at the real entry (tests/cases/_fixtures.py; the capture command
       is on the issue) and one red mutation for the line you changed
     - just oracle-diff <Fn> PASS; just lint-constants clean
     - p0: just session-verify <session named on the issue> - confirmed must rise
       p1/p2: just session-sweep <session> --after <ordinal> --until <ordinal> lists it ok
       p3: the composition audit named on the issue no longer reports it
  4. jj commit <only your paths> -m "type(scope): subject"      # <= 50 chars, no body
  5. just issues-sync                   # the issue closes itself; new facts open
  6. back to 1. Giving an item up: just issues-release <N>. Past six hours on one
     item: just issues-claim <N> renews it.

Route items (label route): record exactly as the issue body says, with
just session-pilot / session-ai-duel / session-derive; verify; then
just session-sweep <name> so the region's facts enter the tracker. A route item that
needs a human at the window is left open; take the next item and name it in the report.

Rules:
- Unattended: never ask; when two options exist take the boring one.
- Memory: one reference lane at a time in this session. Never run two of session-verify,
  session-sweep, oracle-diff-all concurrently; leave no background job running when you
  stop. WSL has OOM-crashed on this repo.
- Never run just oracle-release-gate, a formatter, a linter or any git command.
- Never widen an exclusion ledger (scenario.py, _fixtures.py _HOLES, test_leaves.py
  AUTO_OBSERVE_IGNORED) and never edit a case to match the C.
- Never hand-close a fact issue or write progress into one. noise / wontfix only with a
  comment naming the harness artefact.
- Files you did not change are not yours.

Report at the end: issues closed (numbers), sessions whose ratchet moved (name, from -> to),
issues the sync opened, items left open and why.
```

## Setup, once per session

```sh
cd /home/matheus/git/poketcg
```

Read `docs/port-contract.md` (case coverage, items 4 and 5 especially) and
`AGENTS.md` (file ownership, command table).

Never run `just oracle-release-gate`, a formatter, or any `git` command.
Commit with `jj` only, naming your own paths:

```sh
jj commit <paths> -m "type(scope): subject"      # subject <= 50 chars, no body
```

Another session shares this checkout. Files you did not change are not yours;
never revert, stage, or commit them.

## Issues: the worklist

The Forgejo issues are the loop's worklist, and nothing else: every open issue
is a measured fact with the command that reproduces it, opened and closed by
`just issues-sync` from the tooling's own reports. Nobody writes progress into
them and no plan is projected onto them - the two earlier trackers did that,
nobody working the loop had a reason to read them, and both rotted in a week.

```sh
just issues-next          # the highest-priority open facts and their repro commands
just issues-sync          # after a landing: opens new facts, closes resolved ones
just issues-status        # milestones (the route, in play order) and their sessions
just issues-route S T H   # a human's one issue kind: the next content to record
```

Four fact kinds, in priority order:

| label | fact | source | closes when |
|---|---|---|---|
| `p0-divergence` | a session leaves the ROM's trajectory at DoFrame N | `just session-verify` | the session verifies clean past N |
| `route` | content nobody has recorded yet (`session:` names the recording) | a human, `just issues-route` | that session verifies clean end to end |
| `p1-memory` | a routine computes different game state from a live seed | `just session-sweep` | the latest sweep that enters it lists it ok |
| `p2-registers` | a routine leaves different exit registers, memory agrees | `just session-sweep` | same |
| `p3-audit` | a body is an echo, a stub or a cut | `composition_audit.py` | the audit no longer reports it |

Within a priority the order is the route's play order, then the DoFrame the
fact was seen at: `issues-next` starts at boot. A milestone is a region of the
game (`Boot and Mason's lab`, `Fighting Club`, ... `Pokemon Dome and credits`,
then `Engine` for facts no route session reaches); its counts answer "how far".

Working an issue is the loop below with the issue's repro as the first command.
Land the fix (fixture case at the real entry, red mutation, ratchet), then
`just issues-sync`; the issue closes itself with the landing named. Two labels
are yours to apply and hold an issue out of `issues-next` and out of the sync:
`noise` (a harness artefact - say which, in a comment) and `wontfix`. Never
close a fact issue by hand: if the fact is still in the latest report the next
sync reopens it.

The reports the sync reads live in `build/completion/tracker/` and are written
by every `session-verify` and `session-sweep` run, so a sweep of a new session
(`just session-sweep <name>`) is how a whole region's facts enter the tracker.

### Parallel sessions

Several sessions can work the tracker at once; each is one process on this
box and the tracker is the only coordination they need:

- `just issues-next --claim` labels the item `claimed` with a comment naming the
  session (`POKETCG_SESSION`, else host:pid) and the time; other sessions'
  `issues-next` skip it for six hours, `just issues-claim N` renews, `just
  issues-release N` gives it back, and the sync drops expired claims. Two
  sessions never hold the same item unless one outlives its claim.
- `issues-sync` takes a file lock (`build/completion/tracker/.lock`), so two
  syncs cannot create the same fact twice.
- Each session builds in its own `POKETCG_BUILD` directory (`justfile:4-7`;
  `tools/completion/scenario.py` reads it for the binary and the pack, and
  `just build-trace` builds `$POKETCG_BUILD-trace`). The
  reference caches under `build/completion/sessions/` are shared on purpose:
  a stream is keyed by its inputs and identical when rebuilt, so a race costs
  time, not truth.
- One checkout, one working copy: commit only your own paths with `jj commit
  <paths>`; a colleague's uncommitted edits stay in the working copy.
- The box, not the tooling, sets the count: 15 GB, and every agent session is
  about 1 GB before it runs anything, a PyBoy probe a few hundred MB more. Check
  `free -g` before adding a session and stop stale sessions first; the reference
  lane's OOM crashes took WSL down, not just the run.

The `ai-duel-*` sessions poke a duelist type at the practice duel's first turn,
so they exercise a deck's AI *table* against the practice cards, not the deck:
decks whose tables only differ in card lists the practice hand never matches
play the identical duel (the reference call streams of `ai-duel-11`/`12`,
`13`/`15` and `16`..`1a` were byte-identical; one of each is kept). Real
boss-deck coverage is the route's own duels.

## The gates, every iteration

Three mechanical checks, in this order, before a ratchet moves. Together they
take under four minutes and each one has caught a class of defect the session
loop bisected to one routine at a time:

```sh
just lint-constants        # <1 s: every #define that names an asm symbol carries
                           #       the asm's value; banked literals name data
just oracle-diff-all       # ~150 s: every routine against PyBoy; the baseline is
                           #       all-green and a red line is the next fix
just session-verify        # ~100 s: the digest stream against the reference
```

`oracle-diff-all` was once forbidden to sessions because parallel slices
registered routines before their cases existed. One session owns the checkout
now, and a red baseline is how twenty routines sat broken while `confirmed`
climbed: run it.

Two diagnostics narrow a divergence before any bisection, both from the same
PyBoy run the oracle already makes:

```sh
just oracle-diff R --auto-observe   # compare every byte the ROM wrote in R, not just
                                    # the case's spans (tests/test_leaves.py)
just blind-spots --fn R             # which of R's writes no case observes
```

A `DIVERGE ... writer=R` line names the routine; `--auto-observe` on `R` and
its callees shows the wrong bytes without replaying the session. Timing
counters the probe cannot match (`wVBlankCounter`, the cursor blink counters,
the key-edge bytes) are excluded; anything else it prints is a defect or a
case that never looked. A whole-tree sweep (`just blind-spots --all`, ~90 s)
ranks the routines whose cases observe none of their writes; those are where
the next session divergence comes from.

## The session loop

The primary gate. A session is one byte of input per DoFrame. The reference
replays it once and caches a CRC-32 of the masked game state (WRAM, HRAM,
OAM, VRAM) at every DoFrame; the port writes the same digest stream; the first
ordinal whose digests differ is exact, found in one native run (~5 s of CPU
for 340k DoFrames: the lanes build `RelWithDebInfo`, the pack is a per-bank
map, and a headless replay never renders). Only then does one targeted
reference capture name the bytes, their RAM symbols and the routine that last
wrote them; the reference seeks to a savestate checkpoint below the ordinal
(every 5,000 anchors, written by the stream build), so a capture or a
`routines` listing takes seconds, not a boot replay. A clean verify of the
longest session is ~40 s wall; a diverged one about two minutes.

Sessions come from the ROM, not from a human:

```sh
just session-derive tas-5530s build/completion/tas/input.txt   # once; ~2 min
just session-verify                                             # lowest confirmed session
just session-status
```

`derive` has the reference play the frame-indexed TAS and log the byte its own
`ReadJoypad` read at every DoFrame; the log replayed on the DoFrame axis is
digest-identical to the movie run (`axis_match=True`). The movie is 78,207
frames and 71,396 DoFrames, boot to wherever the ROM goes on it: even past the
point where luck manipulation stops matching the runner's intent the ROM is
still executing legal input, and the port has to match it byte for byte.
There is no length cap and no re-recording: the session is a function of the
movie and the reference alone, and every fix re-verifies against the cached
reference in a native-only run.

The duel engine has a second source, the ROM's own AI. `just session-ai-duel
ai-duel-NN DECK` branches `practice-win` at the practice duel's start
(DoFrame 23227, after `StartDuel_VSAIOpp` and before the first turn), pokes
both duelist types and `wDuelType` to `DUELIST_TYPE_AI_OPP | DECK`,
`wOpponentDeckID` to `DECK` and `wIsPracticeDuel` to 0
(`tests/sessions/<name>/pokes.txt`, applied by `--poke-ordinal` on the native
lane and by `refstream.Core(pokes=...)` on the reference), then has the
reference play the duel to `wDuelFinished` plus 1500 DoFrames of aftermath.
Every turn of both duelists is then AI code under the digest, and every
`AIDecide_*`, scoring and damage-estimate routine the deck pair reaches is
verified byte for byte -- `ai-duel-02` alone named nine stubs and mis-branched
bodies. `--seed`, `--prizes` and `--period` vary the run; one session per deck
id is the natural matrix.

`just play --record-input PATH` still records a human, and `session-meta`
files it as a session; it is a way to reach a screen the movie does not, not
the loop.

`just session-verify` prints one line, then the evidence:

```text
SESSION NAME status=<clean|diverged|native-short|ref-short> confirmed=<K> ordinals=<n>
WINDOW ordinal=<K+1> regions=<wram,...> reference_frames=<f> reference_vblanks=<v> [LAG ...]
DIVERGE ordinal=<K+1> field=<f> address=0x<AAAA> symbol=<sym> native=<n> reference=<r> writer=<Routine>
```

`confirmed` is the number to move, per session, in
`tools/completion/session_ratchet.json`. It may only rise; a fall is
`REGRESSION` and exit 3, and the change that caused it does not land.

The comparison covers WRAM, HRAM, OAM and both VRAM banks under `scenario.py`'s
exclusion ledger plus two spans of its own: `SECTION "WRAM Audio"`
($DD80-$DEE4) and `wPlayTimeCounter` ($CAC5-$CAC9). The sound driver and the
play-time clock run from the timer interrupt (`time.asm:9-26`), asynchronous
to DoFrame, so their counters sit ticks apart between lanes on a schedule no
asm instruction decides; `audio-catalog` owns audio parity. `hDPadRepeat` is
compared even though the ledger excludes it: its exclusion is a frame-axis
argument. IO readback and palette RAM are the scenario census's. Do not add to
either list to move `confirmed`.

### The sweep: every routine the ROM ran, diffed at once

```sh
just session-sweep NAME [--after K] [--until K] [--json PATH]
```

One reference replay of the session (from its savestate checkpoints) captures
the first entry of every ported routine the ROM enters in the window; each
entry becomes a fixture case in memory and is oracle-diffed with the
observation widened to every byte the reference wrote. ~1,100 routines in ~20
minutes, no model in the loop. Rows come out with memory mismatches first:

```
ROW ordinal=<K> routine=<R> status=fail memory   $CCB9: oracle 2800 != C 1400 | ...
ROW ordinal=<K> routine=<R> status=fail registers f: oracle $80 != C $00
ROW ordinal=<K> routine=<R> status=frames memory $C000: oracle ... | $CAB8: ...
ROW ordinal=<K> routine=<R> status=error|wedged  OracleError: ...
SWEEP <name> after=0 until=<n> routines=1140 failing=82 frames=12 errors=15 wedged=6
```

Read the rows in this order:

- `memory` rows are game state the port computes differently from a live
  seed. A coin-toss routine (`PinMissile_MultiplierEffect`,
  `HandleSandAttackOrSmokescreenSubstatus`) is noise here: the PyBoy lane runs
  many DoFrames per tick, so `UpdateRNGSources` advances differently inside
  the routine and the tosses land differently. Every other memory row is a
  lead: `capture` the entry, build the fixture case, port from the asm.
- `registers` rows are exit registers no caller may read (a screen routine's
  leftovers threaded out of an effect). Real, low priority: the session loop
  never reports them because WRAM is identical. One shape inside this class is
  not portable at all: a routine whose tail is `FillRectangle` exits with
  `add sp, $24`'s flags (`tiles.asm:40`), whose H and C come from the stack
  pointer's own low byte, so the byte encodes the call depth rather than
  anything the routine computed (`ApplyBGP6OrSGB3ToCardImage` on its CGB path:
  the reference leaves `f=$20`, and its two DMG cases pass). Leave the row;
  widening the C body cannot reach it without modelling SP.
- `frames` rows looped on DoFrame: the PyBoy lane skips the halt and runs its
  own VBlank service in place of the ISR, so such a routine counts frames,
  advances the RNG and animates sprites unlike the probe, and every
  frame-driven byte differs (`HandleYesOrNoMenu`, the script `AskQuestion`
  commands). Not comparable this way; the session loop is their gate, and the
  tracker does not open an issue for them.
- every entry carries the two save banks, so a routine that reads or writes
  SRAM (`PrintSortNumberInCardList_CallFromPointer`) compares against the
  game's own save, not an empty one.
- `error` rows hit the oracle's frame budget: the routine waits for input the
  case's two-entry `keys` timeline does not supply. Not comparable this way.
- `wedged` rows hung the PyBoy frame; the sweep marks them and moves on.

The sweep is the worklist for a cheaper model: each row carries the routine,
the ordinal to `capture` at, and the bytes that differ.

### Session decision table

| the line contains | what it means | what to do |
|---|---|---|
| `status=diverged` and `DIVERGE ... writer=R` | the reference's `R` produced a byte the port did not | read `R`'s asm against its C body; the defect is in `R` or in what `R` reads. Fix, `just oracle-diff R`, add a case that observes the byte (`read`), rerun `just session-verify NAME`; `confirmed` must rise |
| `DIVERGE ... writer=R` and `R`'s cases are green | `R` is accepted through a hatch, or a callee is: the case never ran the ROM to `ret` | `just hatch-status` names it; port it with a fixture case (`## The hatch queue`). Check every callee the reference entered in that ordinal against the native's counts (`native_trace.native_counts` vs `refstream.routine_trace`); the one the native never entered is the stub |
| `WINDOW ... LAG` (`reference_frames` > 1) | the ROM spent extra VBlanks between these two DoFrames -- a routine heavy enough to lag, or an LCD-off stretch | if the divergent bytes are `wVBlankCounter`-timed (a `cp N` wait, `FadeScreenToTempPals`), model the extra VBlanks with `frame_boundary_consume_services(reference_vblanks - 1)` at the site, as `src/home/start.c:290` does |
| `DIVERGE ... writer=Func_3e44` (or another LCDC-interrupt function) after a scene arms `rLYC`, the port one ISR short | the STAT ISR fired more than once between two VBlank increments: LYC=0 armed as the LCD turns on fires at line 0 and again at line 153, which reads as 0 (`credits.asm` `.Func_1d73a`); the lag track's `s<mask>` bit cannot count it | a track built since 2026-09-09 counts them (`stat-repeats.txt`, `S<segment>:<count>`, `X` on line 1) and the port runs its handler exactly that many times (`src/runtime.c` `stat_service`); an older cache lacks the file -- delete its `stats.bin` and rerun `session-verify` to regenerate. `credits-1` `wd658` was this |
| `DIVERGE ... writer=` empty | no reference write to that address before that ordinal | the port invented a write. Run `build-trace/poketcg --input-ordinal ... --stop-ordinal K` for K-1 and K with `--trace-calls`, diff the counts with `tools/completion/native_trace.native_counts` against `refstream.routine_trace(..., ordinals=K, axis="ordinal")`; the routines only the port entered are the suspects |
| `status=diverged` and both lanes name the same routines | same code, different bytes | dump both lanes at K-1 and K (`--dump-state-ordinals`, `session.reference_capture`) and read the writer's asm with those inputs |
| `status=native-short` | the port aborted or hung before the session ended | the `NATIVE` lines carry stderr; take `blocked_by` from them and use the decision table below |
| `NATIVE cannot load lag track` | the native rejected `lag.txt`: a line it could not parse, or (before 2026-09-09) one longer than its 4 KiB buffer -- a save or the credits' set-up runs ten thousand driver calls between two DoFrames | `src/main.c` `read_line` now grows the buffer; if it recurs, the line is malformed: print it (`sed -n '<K+1>p' <stream>/lag.txt`) and fix `session.py lag_track` |
| `status=ref-short` | the reference produced fewer DoFrames than the session has entries | a hand recording outran its `reference_frames`; refresh `session-meta`. A derived session cannot do this |
| `status=clean` | the whole session is confirmed | every session clean means the loop has no frontier: work `just hatch-status` until a new recording exists. A recording is `just play --record-input tests/sessions/<name>/input.txt` from boot (a human), or `just session-derive` from a movie; `session-meta` files it. Do not invent one by hand-editing input bytes |
| `REGRESSION NAME key=confirmed_ordinal` | your change lowered a session's confirmed ordinal | revert your change; do not land it |
| `DIVERGE field=vram` only, both lanes ran the same routines | a tile the port drew wrong, not a control-flow fork | dump both lanes' BG map rows around the address; the writer's asm decides the tile from a status byte or a coordinate. Today's two: `CheckPrintPoisoned` printed the raw status byte where `and POISONED` leaves 0; `PrintDuelResultStats` took d/e from a text-print result that the asm preserves (`ProcessText` pushes de) |
| the native's `--trace-calls` interval looks one DoFrame ahead of the reference's | it is: the stop is honoured at the next boundary, so `trace(stop K) - trace(stop K-1)` is the work after anchor K, i.e. the reference's ordinal-K list | compare native `[K-1 -> K]` against reference `K`. State dumps (`--dump-state-ordinals K`) are taken at the anchor and are not shifted |
| `run_mutation.py ... --index 0` prints `MUTATION_GREEN` for a fixture-backed routine | `--index` is the case index, not the mutation index; case 0 may not observe the mutated line | pass the index of the case that reads the byte the mutation flips (usually the fixture case), and name it in `case_ids` |
| `MUTATION_BASELINE_FAILED ... "bus": {"address": 32768, "reference": "ffff...` | the gbref lane read VRAM while the PPU was in mode 3 -- the routine returns mid-frame | build the case with `vram=False` (`Fixture.case`); VRAM is then neither seeded nor compared for that case, so add a `read` on the WRAM the routine writes |
| a reference routine is "never entered" by `session.py capture --after K` | the session's later stretch takes the other branch (e.g. `Func_c17a` returns early in script mode, so `Func_c9b8` is only entered at the session's first map load) | retry with `--after 0`, or capture from the session that reaches it (`just hatch-status` prints the first ordinal per routine) |
| `DIVERGE` rows are all scratch (`wLoadedCard2*`, `wAIMinDamage`, `wTempTurnDuelistCardID`, `wDuelTempList`) and `WINDOW` has `reference_vblanks` in the tens or hundreds | an AI turn: the ROM thought for many VBlanks between two DoFrames and the two lanes ran different decision routines. The named writer is the last loader, never the defect | `python3 tools/completion/session.py routines NAME K` lists the reference's routine entries in that interval with the plumbing hidden; `session.py diff NAME K+1` prints every differing byte. Capture the first AI routine of the interval (`capture NAME --routine R --after K`), give it a fixture case, `just oracle-diff R`: a live-state failure with green registers and scratch bytes is a subtree that ran different callees -- descend into the callees the same way. Every AI stop this far was a body that skipped a branch of its asm (`AIProcessEnergyCards`, `DetermineAIScoreOfAttackEnergyRequirement`, `AIDecideBenchPokemonToSwitchTo`) or a constant (`AIDecideEvolution`, `GetAIScoreOfAttack`) |
| `session.py capture` returns an entry whose `stack=` return address is in the wrong caller | the routine is entered from several places in the same DoFrame (`CheckIfDefendingPokemonCanKnockOut` runs in the retreat phase and again in the energy phase) | `--nth N` picks the Nth entry at or after `--after`; the printed `stack=` words are the return addresses, `poketcg.sym` names their routines |
| `status=native-short` and `NATIVE MISSING_DATA 00:0000` from `LoadCardDataToBuffer1_FromDeckIndex (a=255)` under an AI routine | the AI evaluated an empty play area slot: a C loop let a callee's registers overwrite the counter and pointer the asm keeps on the stack (`push hl / push bc` around the calls) | read the asm loop for `push`/`pop` pairs and stop copying those registers out of the callee's result (`retreat.c` `.loop_ko_1`). The ROM never reads card $ff there, so this is never a data-pack gap |
| `DIVERGE symbol=wAITrainerCardParameter` | `_AIProcessHandTrainerCards` stores the decision routine's `a` register when its carry says play; the C decision returned only `f` | the `AIDecide_*` routine returns `AIDecideParameterResult` with the `a` the asm leaves on every exit, even where the card ignores it (`AIDecide_Bill` leaves the deck count); its contract compares `a` |
| a routine is green on every case and still wrong in play | its C body is a fraction of its asm (`AIDecideEvolution` was `return 0xff` for 290 asm lines; `GetAIScoreOfAttack` scored every attack 0x50) | `just hollow-ratio` lists factory blocks by asm-to-C size ratio, most suspicious first: the proactive queue. Port from the asm, give the routine a fixture case at a real entry, retarget its mutation |
| a routine is green on every case, its body has several statements and no callee, and its `factory-completion` is a `pre-ret` pc | an echo: the body writes the bytes the oracle observed before the cut and returns the registers it reported (eleven recoil effects wrote `wDamage`/`wLoadedAttackAnimation` by hand and never called `DealRecoilDamageToSelf`; `WeezingSelfdestructEffect` was nine statements for three calls). The cut at `PlayAttackAnimation_DealAttackDamageSimple` sat three calls down, so `cuts` did not list it | `python3 tools/completion/composition_audit.py echoes` ranks them; `cuts` now follows calls to any depth. Port the calls, delete the completion block, and give the routine a fixture case with a large `cycle_budget` (the animation needs ~1,100 frames); the oracle then runs to the real `ret` and both lanes agree on the KO |
| `DIVERGE symbol=wAIScore` and `wOpponentDeckID` selects a branch in the writer | a `*_DECK_ID` constant typed as the `*_DECK` value: the ids are the deck constants minus two (`deck_constants.asm`'s `deck_const` macro), and the packet table did not expand that macro, so the translator invented them | `python3 tools/audit_constants.py` now knows every `*_DECK_ID`; `tools/lint_constants.py` always did. Fix the define; the gate's `constant_lint` would have caught it, so run the lint after any AI routine lands |
| `NATIVE MISSING_DATA 00:0000` from `CheckIfCanEvolveInto` under `CheckCardEvolutionInHandOrDeck(a=<an HP>)` | the asm `push de` / `pop de` around the HP compare restores the deck index into `d` before the evolution search; the C passed the HP it had just read | pass the deck index (`CheckIfArenaCardIsFullyPowered`, `CountNumberOfSetUpBenchPokemon`); make the fixture case observe it by putting the evolution in the deck and setting `CAN_EVOLVE_THIS_TURN` on the arena flags |
| the port plays a trainer the ROM holds, and the AI decision's C "checks the active card" where the asm's `.default` reuses the loop's terminal `e` | a ROM quirk corrected by the translator: `AIDecide_EnergyRemoval` never resets `e`, so its "active card" fallback inspects the first empty slot and always fails | reproduce the quirk, comment it, and anchor the mutation on the corrected form so nobody re-fixes it |
| `DIVERGE symbol=wAITrainerLogicCard writer=_AIProcessHandTrainerCards`, one byte, after an AI turn whose trainer decision returned no carry | `trainer_cards.asm:12-98`: the phase lives in `d`, the decide routine is called through `CallIndirect` with no `push de`, and every refusal (`jr nc, .inc_hl_by_4`, `jr c, .inc_hl_by_2`) rescans the rest of the table with the decide's exit `d` as the phase for the same hand card; a played card jumps to `.loop_hand`, which reloads `d` from `wAITrainerCardPhase` (`AIDecide_EnergySearch` leaves the play-area count, so PHASE_12 finishes matching PHASE_04 rows and the byte ends as ITEM_FINDER; `AIDecide_ProfessorOak` leaves 0; `AIDecide_Defender_Phase13` preserves it) | fixed: `_AIProcessHandTrainerCards` sets `phase = decision.d` after every decide, and all 50 `AIDecide_*` take `d` and report their exit `d` (`TrainerDecision` carries it), derived from the callees' `de` behaviour and claimed in each contract's `compare`. The helper web reports `d` too: the five `core.c` wrappers (`CheckIfAnyAttackKnocksOutDefendingCard`, `CheckIfCanDamageDefendingPokemon`, `LookForEnergyNeededForAttackInHand`, `CheckIfDefendingPokemonCanKnockOut`, `CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHP`), `CheckIfNoSurplusEnergyForAttack`, `FindHighestBenchScore`, `AIDecideBenchPokemonToSwitchTo` and `AIDecideWhetherToRetreat` (entry `d` in; 0 after `.check_active_id`'s `GetCardIDFromDeckIndex`), `AICheckIfAttackIsHighRecoil` (`wPlayAreaAIScore + 6`'s page from `RetrievePlayAreaAIScoreFromBackup2`), `LookForCardIDInHandList_Bank8` and the energy picks (`wDuelTempList`'s page from the list builders, 0 once a card id is fetched), `HandleNoDamageOrEffectSubstatus` (`ld d, $0` on the Neutralizing Shield path), `PickPokedexCards` (`wce1a`'s page). `GetCardIDFromDeckIndex` is `ld d, $0`, `LoadCardDataToBuffer1/2_*` and `GetCardDamageAndMaxHP` preserve `de`, `CopyAttackDataAndDamage` leaves `wLoadedAttack`'s page. `grass-club` 544666 -> 549326 |
| `DIVERGE symbol=wLoadedCard1Atk2Flag1..wLoadedCard1AIInfo writer=LoadCardDataToHL_FromCardID`, tail bytes of the buffer, `reference=255` where the native holds tile-shaped bytes | `card_data.asm:59-77` copies `PKMN_CARD_DATA_LENGTH` (65) bytes for every card. `GamblerCard` ($0C:7FC5) and `RecycleCard` ($0C:7FD3) sit at the end of the card bank, so the copy runs past $7FFF into VRAM at $8000: the ROM reads $FF for each byte the PPU holds (mode 3) and the tile bytes otherwise, so the tail is the LCD phase of each `ld a, [hli]`, not the asm's (`psychic-club` 545891: 43 Recycle copies in one AI interval, each with its own phase) | the reference records it: `overreads.txt` next to the lag track (session.py `OverreadRecorder`, one `<interval> <hex tail>` per copy whose CardPointers entry spills, hooked at `$2F14`/`$2F31`), the port replays the tails in order through `frame_boundary_overread` (`src/home/card_data.c`) under `--overread-track`, and `overread track: N card copies off schedule` on stderr names a desync. Live play reads VRAM as the ROM does outside mode 3. Every copy goes through `LoadCardDataToHL_FromCardID`; the buffer wrappers used to carry a second copy loop that never spilled and the routine itself popped bank 0 |
| `DIVERGE field=hram symbol=hSCX writer=ApplyBackgroundScroll`, one byte off by one `BGScrollData` step, `WINDOW reference_frames` about 1.7 with one VBlank | the final `hSCX` is `BGScrollData[wVBlankCounter & $3f]` (`scroll.asm:95-101`, `a` is zero), so a one-step slip is a one-count slip in which counter the STAT ISR read. The LYC=0 coincidence fires ~2000 cycles after the VBlank ISR entered; when that ISR ran long (a palette flush), the next frame's STAT lands *before* DoFrame reaches `$0552`, so the anchor already holds the next step (`science-club` 539292, timed with `refstream.Core` at `$0040`/`$0048`/`$0552`) | the lag track carries it: `s<mask>` per interval (session.py `lag_track`), bit n set when a STAT ISR followed n VBlank increments; `src/runtime.c stat_wanted` runs the LCDC handler on that schedule and at the anchor for the trailing bit. A cached reference gains the column on its next verify (`ensure_stat_track`, one replay) |
| `DIVERGE symbol=wDamageAnimAmount writer=PlayAttackAnimation`, one or two bytes, right after the AI played a trainer (`GustOfWind_SwitchEffect`, `ImakuniEffect`, `FullHeal_ClearStatusEffect`) or an effect that put a card in play (`FriendshipSong`) | `PlayAttackAnimation` stores its entry `de` into `wDamageAnimAmount` and the trainer animations never load `de`: the byte is whatever the effect was entered with. For the AI that is the decide routine's exit `de` (`trainer_cards.asm:74-98`: `pop de` after `PLAY_TRAINER` restores it, the play routine passes it to `AIMakeDecision`, `OppAction_ExecuteTrainerCardEffectCommands` and `TryExecuteEffectCommandFunction` leave it, `CallHL` enters the effect with it) | fixed: `_AIProcessHandTrainerCards` keeps a running `e` (the list copy's exit, then each decide's exit) and hands `(d, e)` to the play routine, which passes it to `AIMakeDecision`; the effects take the full register set and pass it to `PlayTrainerEffectAnimation`. `AIDecide_GustOfWind` reports its exit `e`; the other decide routines pass their entry `e` through, exact where the asm never touches `de`, unmodeled otherwise (the next such row names the decide routine to model). `PickRandomBasicCardFromDeck` returns `CreateDeckCardList`'s `de` for the same store |
| `status=native-short`, `NATIVE MISSING_DATA 00:0000`, under `DuelistSelectForcedSwitch` in an AI-versus-AI duel | `wPlayerAttackingCardID` is only written on the player's attack path (`UseAttackOrPokemonPower`); when both duelists are AI it is stale, here 0, and `CopyAttackDataAndDamage_FromCardID` follows `CardPointers[0]` = NULL: the ROM copies 65 bytes of the rst vectors at $0000 into the card buffer | fixed: `null_card` in `tools/gen_data.py`'s `NATIVE_DATA_SPANS` declares those bytes; `just completion-data-pack` rebuilds the pack |
| `DIVERGE ... writer=InitializeDuelVariables`/`AddCardToHand` at the duel's first draw, native arena set where the reference still holds $FF | `ShuffleDeckAndDrawSevenCards` enters `IsLoadedCard1BasicPokemon` at `.skip_mysterious_fossil_clefairy_doll` (`core.asm:2032`): an opening hand whose only Pokemon-like card is a Mysterious Fossil or Clefairy Doll is redrawn, and the port counted them as basic | fixed; the Fossil-hand case in `tests/cases/core.py` guards it |
| `just session-ai-duel` fails with `deck id N expands to 63 cards` | `ReshuffleDeck` really lists 63 (`data/decks.asm:1823`) and `CopyDeckData` writes every one past the 60-card array | `deck_cards` writes the whole list; ids 53+ have no deck (NULL entry, then garbage), so the batch stops at 52 |

## The TAS loop (secondary)

A breadth signal over the 21-minute movie, kept because it reaches code no
recorded session has yet. It cannot localise: past the first duel the movie
desyncs for reasons that are not port defects (see "When the divergence is the
movie"). Work the session loop first; run this to see nothing regressed.

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
| `script entry miss target=$XXXX` | an address the table does not carry | `just build` regenerates the table; if it persists, `grep -i "XXXX" poketcg/poketcg.sym` names the symbol, and it needs adding to `tools/gen_script_entry_dispatch.py`'s inputs (a `Script_X.local` that opens with code is collected from the `set_next_npc_and_script` operands in `poketcg/src/scripts`; port it as `Script_X_local` with a `_START_SCRIPT` define so the thunk continues into its bytecode, as `Script_f631.ows_f63c` does) |
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
| `MUTATION_BASELINE_FAILED` whose `bus` mismatch names an HRAM address (`65431` = `hWhoseTurn`, `65440`+ = `hTemp_*`), or `BUDGET_EXHAUSTED` with `halted:1` | the gbref runner's default stack starts at `$FFFE`, inside HRAM, and `Bank1Call` pushes 12 bytes per trampoline level, so a coin toss or any nested `bank1call` chain overwrites the HRAM the case seeded; the PyBoy lane keeps its stack in WRAM and passes | add `"entry_sp": 0xDCBE` to the case (the PyBoy frame's location, inside `RESERVED`); the mutation then evaluates. `Heal_RemoveDamageEffect` and `FriendshipSong_AddToBench50PercentEffect` are the worked examples |

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

## The reference lane's stub is game state

PyBoy stops a probed routine by hooking its synthesized return address, and
`hook_register` implements that by patching the target byte to `$DB`. The stub
is therefore live memory the ROM can read: it sat at `$CFF0-$CFF5`, twelve bytes
into the 24-byte `wNamingScreenBuffer`, so every routine that copied a player
or deck name copied `$DB` out of the middle of it. `FinalizeInputName` produced
`$C509 = $DB` on the PyBoy lane while gbref and the port both produced `$00`;
two references disagreeing is the signature of this class.

Fixtures cannot paper over it. `_fixtures._SPANS` skips the reserved window on
both lanes, so the port reads its own zeros while PyBoy reads the trap byte,
and a case that seeds the window is rejected outright by `_reserved_overlap`.

Every fixed-WRAM address is live game state, so relocating the stub inside WRAM
only moves the collision: `$CD20` (the unlabelled `ds $78` pad) broke the cases
that seed `$C000+3840` and any routine that clears the `$CD00` page, and the
naming buffer's dead tail is wiped wholesale by `InitializeInputName`'s
24-byte clear, which kills the hook and wedges the lane. HRAM's `$FFB8` tail is
already the gbref runner's setup stack.

The return address is now `$3F80`, inside bank 0's `$FF` padding: the patched
byte is ROM, which is not game state, so no routine can read it. `_capture`
snapshots inside the hook callback and only then parks the CPU, so the park
needs execution but not hooking -- it sits at `$DCF0`, inside the reserved
relocated-stack window, where no comparison and no seed reaches it. A
`post_call_byte` case still needs a writable, hookable return address for the
opcode it executes after the `ret`, so those cases alone keep `$CFF0`.

Four files carry the address and must move together --
`pyboy_oracle.SENTINEL`/`SPIN`/`POST_CALL_SENTINEL`/`RESERVED`, the
`verify.py` mirror, `_fixtures._SPANS`, and the return PC `gbref/runner.c`
pushes. The naming cases used to seed `\x18\xfe` at the exact source offset
whose copy reinstated the spin at `$CFF4`; that compensation is gone with the
stub out of WRAM.

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

All three shadows in `duel_animation_core.c` are gone, and removing them moved
the gate further than anything else this session:

| after | reached | executed | frontier | ordinal | pct |
| --- | --- | --- | --- | --- | --- |
| sprite anim shadow | 607 | 742 | 189 | 24,677 | 34.76 |
| screen update shadow | 608 | 743 | 189 | 24,677 | 34.76 |
| coords shadows | 628 | 800 | 149 | 37,879 | **53.35** |

Each shadow was a truncated or mis-sourced copy, and the truncations were the
point:

- `DefaultScreenAnimationUpdate`'s copy omitted `DisableInt_LYCoincidence` and
  the `hSCX`/`rSCX`/`hSCY` zeroes the real routine performs
- `LoadAnimCoordsAndFlags`'s copy read the sprite index from `wWhichSprite`
  (`$D4CF`) where the asm reads `wAnimationQueue` (`$D423`, `animations/core.asm:151`).
  It only ever agreed because its caller writes that same value into the queue
  head immediately before -- a coincidence, not a translation
- the copy also composed the attribute flags the other way round, keeping the
  existing flip bits and OR-ing all of `flags`, where the real routine takes
  `flags`' flip bits and OR-s the existing byte

The byte offsets did agree: the real routine starts from sprite property `$01`,
so its `hl, +1, +2, +$0C` walk lands on the same four bytes as the copy's
`+1, +2, +3, +15`. Checking that before assuming a defect is what made the
redirect safe.

One shadow remains -- `ApplyStatusConditionToArenaPokemon`, `duel_core.c:135`
against `core.c:3543` -- and its signatures genuinely differ, a two-argument
form against a three-argument one, so its callers decide whether it is a
mis-named helper or a fourth second implementation. The ratchet holds at 1.

The lesson is about ordering. Four turns went into AI register contracts that
moved no gate number, while a class the audit could enumerate in one pass was
sitting on 19 percentage points of progress. When a defect class is
*enumerable*, clear it before hand-porting anything.

## The duel loop was a one-line stub

With the shadows cleared, the gate's earliest blockers moved to ordinal 37,879:
`UpdateSubstatusConditions_StartOfTurn` and `DisplayDuelistTurnScreen`, called
adjacently at `core.asm:76-77`. Their caller is `MainDuelLoop`, whose entire
port body was `EnableLCD();` -- the `truncated` audit's second-largest row at 25
dropped calls, and the thing gating everything past that ordinal.

Ported in full (`core.asm:73-217`): the per-turn sequence, the two
`wDuelFinished` checks around the between-turns work, the fifteen-turn practice
cutoff, the result screen with its win/loss/draw animation and song, and the
tie path that reruns the whole loop as a one-prize sudden death match. All 26
callees already existed; the constants came from the disassembly's own tables
(`BOXMSG_DECISION` is index 3 of its `const_def`, `OPPONENT_TURN` is
`HIGH(wOpponentDuelVariables)`).

| after | reached | executed | frontier | ordinal | pct |
| --- | --- | --- | --- | --- | --- |
| shadows cleared | 628 | 800 | 149 | 37,879 | 53.35 |
| MainDuelLoop | 645 | 853 | **42** | 43,575 | **61.37** |

**A non-returning routine breaks its callers' contracts.** The stub returned
immediately, so `MainDuelLoop`'s own row and both `StartDuel` rows used
`pre-ret` pcs. Once the real loop landed, the native lane ran into a loop that
only exits when the duel ends while the reference sat at those pcs: the loop's
own probe timed out at 30 s, and `StartDuel`/`StartDuel_VSLinkOpp` went red on
`$D423` and `hWhoseTurn` -- state the port had reached and the reference had
not. `core` fell 369 -> 367 and the group check caught it.

All three now stop both lanes with `entry` mode at
`UpdateSubstatusConditions_StartOfTurn` (`00:35E6`), the loop's first call.
Raising frame budgets was not enough on its own: stopping at `HandleTurn`
instead still exceeded 1,140 frames, because reaching it draws the turn screen
and needs duel state the seeds do not build. So the row verifies that the loop
is entered and reaches its first call, and the gate's 19-point jump is what
verifies the body.

Worth noting for the next stub of this shape: check every caller's completion
mode *before* landing a body that stops returning, not after the group check
goes red.

## An orphan chain four levels deep

With `MainDuelLoop` landed the earliest blockers became five `duel` routines at
ordinal 43,575, each called 109-218 times: `DrawInPlayArea_ActiveCardGfx`,
`DrawInPlayArea_Icons`, `DrawPlayArea_PrizeCards`,
`GetDuelInitialPrizesUpperBitsSet` and `LoadCursorTile`. High call counts on
several routines at one ordinal means a single un-called caller, not several
bugs, so the work is to walk up until something is missing.

Walking up found three consecutive truncated callers, each fully ported except
for the one call that mattered:

- `DuelCheckMenu_InPlayArea` (`menus/duel.asm:36-40`) set
  `wInPlayAreaFromSelectButton` and omitted `farcall OpenInPlayAreaScreen`
- `OpenInPlayAreaScreen_FromSelectButton` (`duel_menus.asm:11-20`) set the same
  flag to 1 between two bankswitches and omitted the call between them
- `OpenDuelCheckMenu` (`duel_menus.asm:1-9`) switched to bank 2 and straight
  back, omitting `call _OpenDuelCheckMenu`

All three are fixed and green; `duel` 134/134, `duel_menus` 8/8.
`DrawInPlayAreaScreen`, `OpenInPlayAreaScreen` and `_OpenDuelCheckMenu` were
already complete underneath them, dispatch table and all -- three empty wrappers
were keeping an entire screen unreachable.

**The gate did not move.** Ordinal stays 43,575 and frontier 42, because
neither entry point has a caller either: nothing in the port calls
`OpenDuelCheckMenu` or `OpenInPlayAreaScreen_FromSelectButton`. The break is one
level higher again, in whatever handles the duel menu's Check item and the
Select button.

Two things worth carrying forward. `DuelCheckMenu_InPlayArea` needed its
contract moved to `entry` mode at `DrawInPlayAreaScreen` once the call was
restored, for the same reason `MainDuelLoop` did -- restoring a call into an
input loop breaks every caller still using a `pre-ret` pc. And a fix can be
correct, provable and still not move the gate: these three were real
truncations, but the chain above them is broken too, so the reachability payoff
arrives only when the last orphan is connected.

The orphan root turned out to be two more stubs, both bare `return;`:
`DuelMenu_Check` (`core.asm:747-750`) and `DuelMenuShortcut_BothActivePokemon`
(`:752-756`). `DuelMenu_Check` is fixed -- `FinishQueuedAnimations`,
`OpenDuelCheckMenu`, then the `jp DuelMainInterface` tail jump -- and needed the
same `entry`-mode move as everything else on this path, stopping at
`OpenDuelCheckMenu` (`00:3096`) because `DuelMainInterface` never returns
either. `core` stays 369/371.

**Still no gate movement**, which now says something specific: the TAS reaches
the play area through the Select-button shortcut, not the Check item. That path
is `DuelMenuShortcut_BothActivePokemon` ->
`OpenVariousPlayAreaScreens_FromSelectPresses` (`:758-777`), and it is blocked
on registers rather than on missing calls. Its body is
`call OpenInPlayAreaScreen_FromSelectButton` / `ret c`, then a local helper
twice around a `SwapTurn`, each with `ret c` -- but the wrapper's port returns
`void`, and the carry it needs comes from `OpenInPlayAreaScreen`, also `void`.

So the Select path needs two register contracts before its body can be written:
`OpenInPlayAreaScreen` must report the carry its input loop exits with, and
`OpenInPlayAreaScreen_FromSelectButton` must pass it through -- `BankswitchROM`
sets no flags (`switch_rom.asm:90-93`), so the wrapper's carry is exactly its
callee's. That is the same shape as the AI energy chain and should be done
bottom-up, not by guessing a value at the top.

Bottom-up on that chain reached a floor worth naming. `OpenInPlayAreaScreen`'s
carry is derivable and landed: two exits, `scf; ret` when B backs out and
`or a; ret` on the Select-button skip (`play_area.asm:62-78`). The result type
carries `f`, the probe adapter reports it, and its contract now compares `("f",)`
where it compared nothing. `play_area` 9/9, `duel_menus` 8/8, gate exit 0.

It is derived rather than proven: the two cases never reach the skip exit, so
inverting that carry leaves them passing. Landed anyway because the derivation
is a two-line asm reading, and left labelled as such.

The floor below it is `DisplayPlayAreaScreen`, and it is a stub -- `(void)0;`.
So the Select path is five deep:

`DuelMenuShortcut_BothActivePokemon` (stub) ->
`OpenVariousPlayAreaScreens_FromSelectPresses` (stub) ->
`OpenPlayAreaScreenForViewing` (stub, two lines: `ld a, PAD_START + PAD_A` and a
tail jump) -> `DisplayPlayAreaScreen` (stub, **91 asm lines**).

That last one is the substantive routine and a turn's work on its own, which is
why this turn stopped at the carry rather than starting it. The three above it
are two-to-six lines each and become mechanical once it exists, so the order is
forced: port `DisplayPlayAreaScreen` first, then the three wrappers upward, then
expect the ordinal to move.

Nine stubs and shadows have now been found on one path from the duel menu to the
play area screen. The region was never "ported and buggy"; it was outlined.

`SelectingBenchPokemonMenu` sits between the two, and its stub was returning
invented flags with no `a` at all -- which matters because
`DisplayPlayAreaScreen` branches on both its carry *and* `cp $02`. Its three
early exits derive (`core.asm:5052-5088`) and are now landed with a real
`{a, f}` result, contract widened from `("f",)` to `("a", "f")`, adapter
reporting both. The menu loop past them is still unported and says so in the
body rather than implying otherwise.

One flag detail earned its keep. The two early exits differ by a single bit: the
first leaves via `or a`, which clears H, so it is `$80`; the second leaves via
`and PAD_SELECT`, and **`and` sets H**, so it is `$A0`. I wrote `$80` for both
and the oracle caught it immediately -- `f: oracle $A0 != C $80`. The old stub
happened to return `$A0` on that path by luck, so widening the contract to
compare `a` is what made the difference visible at all.

So the order for next turn is fixed and mechanical: `DisplayPlayAreaScreen`
(`core.asm:4933-5022`, 91 lines) can now be written against real callee
contracts -- it takes the allowed-keys byte in `a`, stores it to
`wNoItemSelectionMenuKeys`, and its two exits differ only by `or a` versus
`scf`. Its menu-parameter tables are at `01:60BE` and `01:60C6`. Check every
caller's completion mode before landing it: it contains an input loop, and that
trap has now bitten three times on this path.

## The play area screen is ported; the carry above it is not derivable yet

`DisplayPlayAreaScreen` (`core.asm:4933-5022`) is landed in full, along with
both entry wrappers (`OpenPlayAreaScreenForViewing` /
`ForSelection`, which differ only in the key mask they pass) and the
`OpenInPlayAreaScreen_FromSelectButton` carry passthrough. All four green,
`core` 369/371, `duel_menus` 8/8, `play_area` 9/9, gate exit 0.

The pre-check written down last turn paid for itself immediately: all three
screen rows carried `pre-ret` pcs, all three hung the native lane the moment the
input loop became real, and all three needed `entry` boundaries at
`SelectingBenchPokemonMenu` (`01:60DD`) plus 20M/80M budgets, because redrawing
the play area does not fit in 240 frames. That trap is now 4-for-4 on this path.

**Where it stopped, and why the row was reverted rather than landed.**
`OpenVariousPlayAreaScreens_FromSelectPresses` (`core.asm:758-766`) is a clean
transcription -- `SwapTurn` is `push af ... pop af` (`duel.asm:2364-2372`), so it
preserves flags and the fall-through `ret` carries the second view's, with
nothing to guess. It still failed, and the measurement is the useful part:

- at its real `ret` the reference reports `f = $20` -- H set, no carry, no Z
- its first callee, `OpenInPlayAreaScreen_FromSelectButton`, reports `f = $90`
- the port's threading yields `$10` and `$00` respectively

`$20` is the state left by an `and` with nothing after it, so it is not any exit
this routine can produce. The screen below exits via `scf; ret` and `or a; ret`
(`play_area.asm:62-78`), which means **the Z bit is inherited from whatever ran
inside the screen** and the port models none of it. Both available row shapes
are therefore dishonest: `pre-ret` asserts a byte that cannot be derived, and
`entry` compares a result register that does not exist yet because the routine
has not returned.

So the body is reverted to its stub with those three measurements written into
the comment, and the contract was left alone. Worth noting **the old stub
returned `$20` -- the reference's exact byte -- by coincidence**, which is the
same class as `CheckIfDefendingPokemonCanKnockOut` passing while wrong. A stub
agreeing with the reference is not evidence that anything was translated.

I also widened `OpenInPlayAreaScreen_FromSelectButton`'s contract to `("f",)`
to locate the disagreement, then reverted it: comparing a whole `f` byte whose Z
is inherited would fail forever. The carry alone is what its callers read, and
that is what it now returns.

## The root of the duel-menu region, and one rejected body

Walking the chain up finally reached the floor. `PrintDuelMenuAndHandleInput`
(`core.asm:301-349`) was a **one-line stub**, and above it `DuelMainInterface`
(`core.asm:282-299`) was an empty body. Every one of the nine stubs found below
them over the previous two turns sat under a menu handler that never ran.

Landed and green this turn:

| routine | asm | what was wrong |
| --- | --- | --- |
| `OpenInPlayAreaScreen` | `play_area.asm:73-81` | both exit flag bytes invented |
| `OpenInPlayAreaScreen_FromSelectButton` | `duel_menus.asm:11-20` | carry dropped; adapter discarded it |
| `OpenVariousPlayAreaScreens_FromSelectPresses` | `core.asm:758-777` | stub |
| `DuelMenuShortcut_BothActivePokemon` | `core.asm:753-756` | stub |
| `PrintDuelMenuAndHandleInput` | `core.asm:301-349` | one-line stub |
| `UnreferencedDrawCardFromDeckToHand` | `core.asm:365` | entered the handler's head, not `.menu_items_printed` |

**The flag bytes were derivable after all.** Last turn I recorded the screen's Z
bit as inherited and unmodellable. It is inherited -- from `SetupText`, which
ends in a clear loop exiting when `inc l` wraps (`process_text.asm:154-159`).
That leaves `a = 0` with Z and H set, so `scf; ret` gives **`$90`** and
`or a; ret` gives **`$80`**. `$90` is exactly the byte the reference reported.
"Inherited" is not the same as "unknowable"; it means read one routine further.

**Four consecutive rows carried mis-sourced completion pcs.** Not stale --
wrong: `0x1F72` was `FillRectangle.next_tile` in bank 0, `0x4547` in bank 2
named no symbol at all, `0x237D` was another routine's `ret`, and `0x238C` sits
below `0x4000` where a bank number is meaningless. Every one belonged to a
routine whose body was a stub, so nothing had ever executed far enough to
notice. Addresses recomputed from the sym file and the instruction lengths, and
`01:4294`/`01:4295` corroborating each other is what gave confidence.

**An `entry` boundary does not assert which callee was entered.** I mis-routed
the B+Up shortcut to a different one and the row still passed, because all six
shortcut bodies are empty stubs and nothing observable distinguishes them. The
handler's branch selection is therefore transcribed, not verified, and it stays
that way until those bodies write something. The `DuelMainInterface` dispatch,
by contrast, does discriminate (1/6 fail misrouted, 2/2 after).

**`DuelMainInterface`'s body is landed after all, and the trace says why the
gate first refused it.** The body verified cleanly on both arms with
discrimination proven, but it moved `reached_routines` 645 -> 649 while
`executed_routines` fell 853 -> 788, which the rising ratchet scored as a
regression. The unmatched remainder (`executed - reached`) fell 208 -> 139, so
the arithmetic is a trade: more matched execution, less unmatched. The ratchet
now allows exactly that one direction and drops the ceiling when it is taken
(`tas_progress.py`, `RATCHET_TRADE`); a fall that does not buy a match is still
a regression.

**I first wrote that the port had "stopped running past a duel the ROM stays
inside". That was not measured, and tracing disproved the picture.** Reading the
native counts against the reference:

| routine | native | ROM |
| --- | --- | --- |
| `DuelMainInterface` | 1 | 9 |
| `DrawDuelMainScene` | 1 | 9 |
| `DrawDuelHUDs` | 0 | 9 |
| `PrintDuelMenuAndHandleInput` | 0 | 28 |
| `HandleDuelMenuInput` | 0 | 1,036 |
| `OpenInPlayAreaScreen` | 0 | 13 |

The port enters the interface once, draws once, never reaches `DrawDuelHUDs`,
and never runs the menu handler at all. Yet `DoFrame` runs 57,542 times, so it
is alive the whole while -- and the top native counts name where those frames
go:

| routine | native | ROM |
| --- | --- | --- |
| `TryHandleSpriteAnimationFrame` | 312,918 | 45,252 |
| `GetPermissionOfMapPosition` | 310,862 | 43,046 |
| `UpdateNPCSpritePosition` | 271,999 | 37,660 |
| `UpdateNPCMovementStep` | 271,992 | 37,653 |

**The port spins in the overworld at roughly seven times the ROM's rate.** That
is the actual blocker, and it is upstream of every duel-region row worked this
turn and the last two. The five `duel` routines at the head of the worklist and
`OpenInPlayAreaScreen_HandleInput` all already have real bodies -- there is no
stub work left on the frontier. It is purely reachability, and the reachability
is lost in overworld movement, not in the duel menu.

`HandleDuelMenuInput` was checked and cleared on the way: its A-press exit is a
faithful transcription of `HandleMenuInput.A_pressed` (`menus.asm:125-131`), and
`HandleDPadRepeat` composes `hDPadHeld` correctly including the
`hKeysPressed & PAD_BUTTONS` overwrite (`frames.asm:45-65`) that carries the A
bit the loop's only exit tests. Neither is the stall.

## The overworld spin was one script command, and the port now runs the movie

The 7x overworld overcount was not an overworld defect at all. Ranking every
routine by native/ROM ratio put a uniform 6.9-7.2x across the whole movement
path, which is the shape of one wrapping loop, not four bugs. Following it up:
`OverworldDoFrameFunction` ran on 68% of the port's frames against 8% of the
ROM's, so nothing ran twice per frame -- the port simply never left the
overworld. Inside the script VM the cluster was unmistakable:
`ScriptCommand_JumpIfEventEqual` 239 against 29, `Jump` 40/4, `CloseTextBox`
84/12, `ShowSamRulesMultichoice` 41/5, while `MovePlayer`, `EndScript` and a
dozen others matched exactly. A print/ask/close/jump cycle re-asking forever.

**`ShowMultichoiceTextbox` never returned the B-press value.** At
`scripting.asm:1665-1670`, when `wd417` is non-zero the asm sets `e` and
`hCurMenuItem` and **falls through into `.got_result`**. The port set both and
then continued its `for (;;)`, waiting for an input that could never satisfy the
equality test. One `break`.

That collapsed the loop and exposed the next stop, which the gate had been
hiding under a clean-looking run: `blocked_by = MISSING_DATA 00:0000`, an abort
on a null data pointer. A gdb backtrace named it in one shot --
`DrawDuelMainScene` -> `WriteDataBlocksToBGMap0` -> `gb_read8(0)`. The port
declared its arguments as `tile_data = 0`, `bg_map = 0` and passed their
addresses, where `core.asm:2394` passes `DuelEAndHPTileData` ($01:5188). A
placeholder that could only fire once the routine was actually reached.

| measurement | before | after both |
| --- | --- | --- |
| `reached_routines` | 649 | 677 |
| `executed_routines` | 788 | 868 |
| `RunOverworldScript` | 497 (ROM 107) | 149 |
| `GetPermissionOfMapPosition` | 310,862 (ROM 43,046) | 18,958 |
| `DrawDuelHUDs` | 0 (ROM 9) | 7 |
| `DoFrame` | 57,542 | **78,167** |
| `blocked_by` | `MISSING_DATA 00:0000` | *(clean)* |

**The port now runs the whole 78,207-frame movie without aborting or hanging.**

**Neither fix is discriminated by its case matrix, and that is stated rather
than papered over.** `ShowMultichoiceTextbox`'s cases all carry a zero B-press
value at byte +6, so the fallthrough is unreachable by construction; adding a
case with a non-zero value and a B press still did not discriminate, because the
seeded `wCurMenuItem` equals what `HandleMenuInput`'s B exit reports, so the row
leaves by the equality break instead. `DrawDuelMainScene`'s cases seed
`wDuelDisplayedScreen` to the main scene and take the early return, so they
never reach the call that was dereferencing zero. Both fixes are asm-derived --
a fallthrough is not a loop, and a placeholder is not an address -- and the
evidence is the gate, which is the honest signal to cite for a defect no case
can reach.

## The player's turn: three fallthroughs and one unmapped bank

`PrintDuelMenuAndHandleInput` was called 0 times against the ROM's 28, so the
duel menu was never reached even with the interface and the whole chain below it
live. Four defects between `HandleTurn` and the menu, found by measurement
rather than reading:

**The AI arm was taken every time** -- `AIDoAction_Turn` native 14, ROM **0**,
while `HandleTurn` ran 30 times against the ROM's 1. But a gdb probe at the
first `HandleTurn` showed the state was *correct*: `hWhoseTurn=C2`, player slot
`00`. `SwapTurn`, `GetTurnDuelistVariable` and `LoadOpponentDeck`'s framing all
checked clean. Probing the first `DuelMainInterface` call instead showed
`hWhoseTurn=C3` -- so the player's turn was leaving `HandleTurn` before ever
reaching the interface, and only opponent turns got there.

**`StartDuel_VSAIOpp` dropped its tail jump.** `core.asm:42` is `jr StartDuel`;
the port set up both decks and returned. Its recorded stop pc `0x40CA` *is*
`StartDuel`'s address -- the boundary had always been the jump target, mislabelled
`pre-ret`, which is why nothing had noticed.

**`RestartPracticeDuelTurn` was an empty stub, and it sits on two
fallthroughs.** `core.asm:270` falls from `.player_turn` into it, and
`core.asm:277` falls from it into `DuelMainInterface`. Both were missing, so the
player's path ended at `SaveDuelStateToSRAM`. Porting it (one
`DoPracticeDuelAction` call plus the fallthrough) is what finally ran the menu.

**`bank1call` was not modelled.** `map.asm:111` enters the duel with
`bank1call StartDuel_VSAIOpp`, so bank 1 stays mapped for the entire duel --
which is what makes `DuelMenuData` ($01:54E9) readable. Without it,
`PlaceTextItems` read text id `$970F` out of whatever bank happened to be
mapped, and the offset lookup aborted with `MISSING_DATA 00:04FD`. The same fix
removed a duplicate `StartDuel()` call the tail-jump repair had made redundant.

| measurement | turn start | now |
| --- | --- | --- |
| `reached_routines` | 677 | 682 |
| `executed_routines` | 868 | 907 |
| `PrintDuelMenuAndHandleInput` | 0 (ROM 28) | runs |
| `blocked_by` | clean | clean |

Worth keeping: **two of the four had a mis-sourced completion pc sitting on
top of them**, and in both cases the recorded address was a jump target rather
than a `ret`. A stub that never runs far enough cannot notice that its boundary
is nonsense, so the two defects hid each other.

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

The derived session `tas-5530s` does replay from boot, and it is byte-exact
through the practice duel, the duel menu, every Check submenu, the glossary,
the save and the second duel, to DoFrame 69,494. At 69,495 the movie presses
Down+A in the In Play Area screen with an empty bench, so the cursor moves to
`INPLAYAREA_PLAYER_PLAY_AREA` ($10): the 16-entry `.PositionsJumpTable`
(`play_area.asm:214`) is indexed past its end, the ROM jumps to `6:52FA` and
executes `AttackAnimation_*` data, then bank 23 text, as instructions -- the
Duel Escape glitch the run is built on. A port does not follow arbitrary code
execution, so the session declares `ceiling: 69494` in its `session.json` and
`session-verify` reports it `clean` there. Everything the movie does after that
is the glitch's aftermath, not the game. (The reference stream is keyed by the
boot ROM and the timer sync points; under the earlier key the same glitch fired
at 48,438.)

Coverage past that point comes from sessions that play the game. Two ways:

- `just play --record-input PATH` records a human; `session-meta` files it.
- `just session-pilot FROM SCRIPT OUT "goal"` drives the reference core from a
  script (`tools/completion/pilot.py`): replay session `FROM`, then `press A`,
  `hold DOWN 2`, `idle` (release everything until the ROM has sat still for
  150 DoFrames under the session mask), `shot name` (a PNG of the screen,
  `build/completion/pilot/name.png`). `idle` is what makes a route robust --
  the script names presses, not frame counts -- and the shots are how a route
  is checked by eye before the port is asked to follow it. `practice-win`
  (`tests/sessions/practice-win/route.txt`) was built this way: it extends
  `first-duel` through the whole practice duel to the win and back to the lab.

Every session verifies the same way (`just session-verify NAME`) and ratchets
the same `confirmed_ordinal`.

`fighting-club` (`tests/sessions/fighting-club/route.txt`) was piloted this
way from `practice-win`: Dr. Mason's closing talk and the starter deck choice,
out of the lab, the overworld map east to the Fighting Club, Ronald's entrance
scene, up to Mitch and back to the lobby. Aim a walk with the script's `peek`
verb -- it prints the player's tile, facing and map and every loaded NPC's
tile -- rather than by reading sprites off a screenshot; the club room's
"pupils" are floor tiles, and the pupils are only loaded once defeated
(`Preload_*InFightingClub`). Walking runs 8 DoFrames per tile.

The AI-versus-AI generator (`session.py ai-duel`) only produces a duel for
deck id 2: it makes both duelists `DUELIST_TYPE_AI_OPP | deck` but leaves the
player's cards as the practice deck, and every club deck's AI script hands the
turn back to the human interface on that hand. A deck other than 2 needs the
player's deck poked to the same card list first.

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

## The hatch queue: where the stubs are, and why they passed

Every stub found on the duel path this far had a green `oracle-diff` and a red
mutation receipt, and was still a one-line constant. Two case mechanisms let
that happen: a `completion` of `pre-ret`/`entry` stops the reference at a
program counter before the routine's own `ret`, and a non-`primary`
`evidence` never runs the reference at all. `tools/audit_hatches.py` now
rejects both unless the routine is declared in `tests/hatches.py`, and also
flags a C body with no calls and no bus access whose asm is more than a
`ret` (`HOLLOW`). Declared `unaudited` entries pass the routine stage; at
release the count is a ratchet against `tools/oracle/hatch_ratchet.json` --
it may only fall, so a landing that adds no debt is not blocked by the debt
it inherited, and a landing that adds one is. The registry is the queue:

```sh
just hatch-status                                   # the queue, session-reached routines first
just hatch-ratchet                                  # after deleting entries: lower the ceiling
```

Porting an entry means: a return-mode case that observes the routine's real
outputs, `PASS`, a red receipt on a line the real body owns, and deleting the
entry. Never add an entry to make a routine pass.

The case that observes a routine's real outputs is a fixture, not a hand-built
seed. `tests/cases/_fixtures.py` seeds the reference's own captured state
(WRAM, HRAM, VRAM bank 0, SP) at a routine's entry in a recorded session,
patches the bytes the case varies (`attack_fixture(**{"C3C8": b"\x00"})`),
observes both duelists' variables and the BG map, and taps `A` through every
wait. Capture a new state at another routine's entry with
`tools/completion/session.py capture NAME --routine R`. Bytes the lanes
cannot agree on are holes in the fixture, listed and explained there:
`wVBlankCounter`, the cursor blink counters, `wIE`, `wFlushPaletteFlags`,
`wVBlankOAMCopyToggle`. Do not widen that list for a byte the game computes.

| the line contains | what it means | what to do |
|---|---|---|
| `HATCH R: pre-ret case without a declared hatch` | a case stops the reference before `R`'s own `ret` | delete the `factory-completion R` block and give `R` a fixture case that runs to `ret`; if `R` truly never returns, declare it `never-returns` with the asm line of the loop |
| `HATCH R: native-stress ... without a declared hatch` | a case never runs the reference | replace it with a fixture case; `hardware-only`/`link-only` are the only kinds that may stay |
| `HOLLOW R: ... is N instructions` | the C body does nothing while the asm does | port `R`; its cases were authored against the stub and must be rewritten from the asm's branches |
| `HATCH unaudited=N exceeds the ratchet ceiling` | a landing declared new debt | it does not land; port the routine instead |

A worked example, the map-script family (`CallMapScriptPointerIfExists` and
its four `ld l, MAP_SCRIPT_*` wrappers, `Func_c141`): the C returned the
script pointer and stopped, every consumer re-implemented the `jp hl`, and two
of them forgot to -- so Sam's after-duel script never ran and the practice
session diverged in the lab. The fix is one `ScriptEntryEnter` in the callee,
the consumers' copies deleted, and fixture cases at the real entries
(`practice-win-after-duel-entry`, `practice-win-load-map-entry`). Only the
flags survive the jump in C, so those contracts compare `f` and the state
block; no caller reads more.

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

## Menus under a bare seed: the PyBoy lane spins

The PyBoy lane services `WaitForVBlank` by skipping the `halt`
(`pyboy_oracle.py`, `_VBLANK_HALT`), so one rendered frame -- one entry of
the case's `keys` timeline -- holds as many `DoFrame`s as the CPU fits in it.
Two consequences for any routine that polls a menu:

- A held direction auto-repeats inside one rendered frame (`HandleDPadRepeat`
  counts polls, not frames): one `DOWN` entry moves the cursor `1 + k` items on
  that lane and exactly one on the port and on gbref. Which item an `A` lands
  on is therefore not lane-independent.
- The ROM spends rendered frames where the port spends none:
  `SetupPlayAreaScreen` under `DisableLCD`, every `PrintPlayAreaCardList`
  redraw. Edges that fall inside those frames are lost on the reference and
  seen by the port, so the phase of a cycled timeline differs per lane.

A menu case is admissible only when its end state is the same from every phase
and under any number of dropped edges. What passes that bar: `[0, A]` on a
screen whose first `A` completes it; `[0, A, 0, DOWN]` on a multi-pick whose
*count* and terminator are read but whose pick *order* is not; a Select-closed
screen driven by `[SELECT, 0, SELECT]`. What does not: any cycle that contains
`B` on a screen where `B` undoes a pick -- a pick/undo alternation exists for
some dead-time pattern, proven by simulating the asm's state machine over all
phases and deterministic dead times 0-7 (`Gigashock_PlayerSelectEffect`). Such
a branch is left uncased with the reason at the case block, and the sessions
are its evidence. Reading the PyBoy lane's real cadence is a ten-line hook on
`HandleMenuInput` (`pb.hook_register`, log `pb.frame_count` and `hKeysPressed`);
do that before tuning a timeline by trial.

`hollow-ratio` names suspects, not stubs: `LookForCardThatIsKnockedOutOnDevolution`
and `PlayerNamingScreen_GetCharInfoFromPos` are complete ports written on
three lines. Read the C before rewriting.

## Two sessions, one checkout: verify in a workspace, commit by hunk

With another session editing the same tree, `session-verify` measures the
union of both in-flight edits, and a shared file (`core.c`, `core.h`, the
probe adapters, `tests/cases/core.py`) cannot be committed by path without
taking the other session's hunks along. The pattern that keeps a landing
honest:

```sh
jj workspace add --name verify ../poketcg-verify -r <main head>
cd ../poketcg-verify && ln -s ../poketcg/poketcg poketcg && mkdir build && ln -s ../poketcg/build/completion build/completion
# copy in, or re-apply as a script, only your own hunks; then
just build && just build-trace && just session-verify <session>    # each session, in isolation
```

To commit only your hunks of a shared file, hand `jj commit -i` a scripted
diff editor that copies the workspace's file over jj's right-hand tree:

```sh
jj commit -i --tool pick --config 'merge-tools.pick.program="/tmp/pick.sh"' \
  --config 'merge-tools.pick.edit-args=["$left","$right"]' <paths> -m "..."
```

where `pick.sh` does `cp ../poketcg-verify/$f "$2/$f"` for each path. The other
session's hunks stay in the working copy untouched; afterwards re-apply your
block to the working copy so it does not shadow the commit. Check the
committed file equals the verified one (`jj file show -r @- $f > /tmp/c; cmp /tmp/c ../poketcg-verify/$f`).
The editor only sees files that already differ in the working copy: a file
with no foreign hunks is not in `$right`, so copy it over and commit it by
path instead, or the commit lands empty. "No foreign hunks" is not "safe to
copy": if the other session landed while your workspace sat on an older base,
the workspace file lacks their commit and copying it reverts them (measured:
`duel.c` lost the substatus call sites, `main` did not build). Before any
copy, rebase the workspace onto the current head (`jj new <head>`, re-apply
your blocks as a script), or compose the file as `jj file show -r <head>`
plus your factory blocks. Afterwards check every file of their last landing
still equals `HEAD` except the ones you meant to touch. Never `jj abandon` that empty commit
while `main` sits on it -- the bookmark goes with it; `jj bookmark set main -r <head>`
brings it back.

## Canaries rot silently: re-anchor whatever you rewrite

A `MUTATIONS` entry names its target by a literal `before` string. Rewrite the
body it points at and the anchor stops resolving — `tools/run_mutation.py`
refuses to run it and `tools/audit_mutations.py` counts it, but nothing else
notices, so the routine sits unguarded while every other number stays green.
Measured on 2026-09-09: 45 of 2529 declared canaries were dead, and the release
gate had never run the audit at all. It is a `mutations` constituent of
`just oracle-release-gate` now, so the count is enforced.

The loop for one dead anchor:

```sh
python3 tools/audit_mutations.py | grep '^MUTATION anchor'   # the list
python3 tools/run_mutation.py <Fn> tests/cases/<mod>.py --index <i>
```

`MUTATION_RED` is the only accepted outcome. Four rules earn it:

| symptom | cause | action |
|---|---|---|
| `anchor is not unique: 0 occurrences` | the body was rewritten | pick a line that exists now, keep the same defect class |
| `anchor is not unique: N occurrences` | siblings share the line | extend the anchor with an adjacent line until it is unique inside the factory block |
| `MUTATION_GREEN` on every index | nothing observes the byte the defect moves | seed it, or add it to `read`; the compared bus is every seeded span plus `read` plus `vread` plus `CONTRACT` registers |
| `MUTATION_GREEN` and the line looks observable | the case stops before the line | read the case's `_completion` record: `mode: entry` stops both lanes at a named callee's *entry*, so only lines above that call are provable |

Two traps that cost a session each. A case's `expect` map is inert for an
oracle-backed case (`tests/cases/_schema_migration.py:218-234` never copies it
into the schema record and `compare_one.py` never reads it), so an `expect`
showing a byte preserved proves nothing about which arm ran. And a seed can be
*degenerate*: `DisplayCardPageOnLeftOrRightPressed` seeded page `0x0E`, whose
LEFT and RIGHT handlers both answer `0x0D`, so inverting the branch changed
nothing — page `0x0C` separates them.

## Never run two mutation sweeps at once

`run_mutation.py` edits the source file in place, rebuilds, compares, restores.
Two sweeps in one checkout therefore compile each other's corruption: verdicts
flip between runs (measured — the same canary reported RED, GREEN and
`EXECUTION_FAILED` across three overlapping sweeps). The same applies to a
sweep racing `just session-verify` or `just oracle-diff-all`, which build the
same tree. Parallelise the *analysis* — a read-only agent per case module works
well — and keep every prover run serial.

## `MUTATION_BASELINE_FAILED`: the two references disagree, not the port

The mutation lane compares the native probe against **gbref** (statically
recompiled ROM), while `just oracle-diff` compares it against **PyBoy**. When a
case passes `oracle-diff` and its mutation baseline fails, the port is not the
suspect — read the mismatch and classify:

| mismatched byte | class | action |
|---|---|---|
| `0xCAB8` (wVBlankCounter), `0xCD0F`, `0xCEA3` | frame counters the two lanes service differently, already listed in `tests/cases/_fixtures.py` `_HOLES` | stop seeding it in the case; a fixture never seeds it either |
| the case's own seed, unchanged in native | the probe stopped before the reference did | check the case's completion record; an `entry` stop and a frame cap are two terminators and the cap can truncate the run |
| a live game byte on a link/serial path | gbref and PyBoy model serial differently | leave the canary declared and unproven, and say so |

Worked example of the last row: `StartDuel_VSLinkOpp` case 0 seeds `hWhoseTurn`
(`0xFF97`), so it is compared. gbref leaves `0x01` there; PyBoy and the native
port both leave `0xC2`, and `just oracle-diff StartDuel_VSLinkOpp` passes. Two
references disagreeing on one ROM is a lane defect, so the honest disposition is
to record it here rather than delete the seed and weaken a real case. It is the
one canary of 2529 that is declared, anchored and unproven.

## What the audit still cannot see

`audit_mutations.py` proves an anchor *resolves*; it cannot prove the canary was
ever red. A receipt exists per routine
(`tools/oracle/mutation_receipts/<Fn>.json`, 2530 of them) but records only
`fn`/`case`/`index`/`status` and the three payloads — never the `before`/`after`
it was produced from. So a declaration can be rewritten and its receipt still
says RED about text that no longer exists. Closing that means adding the
declaration's digest to the receipt and regenerating all 2529, which is a
migration, not a fix; until then "0 failures" means "every anchor resolves",
and nothing more.

## The audio exclusion hid six defects

`GATED` is 4, so `SECTION "WRAM Audio"` ($DD80-$DEE4) is digested as the
`audio` region and reported, not gated. The stated reason until 2026-09-09 was
that the port batches timer ISRs at the frame boundary while the ROM
interleaves them with game code. That reason was wrong: the lag track already
replays the ISR count per interval and `src/runtime.c` `schedule_close`
delivers an interval's remainder before the digest, so the region was
comparable all along. Flipping `GATED` to 5 and sweeping is the measurement,
and it found six defects. Five are fixed and the sweep now stands at 80 of 81
sessions clean *with audio gated* -- `challenge-hall` byte-exact through all
702,945 of its ordinals, sound driver included.

**The flip does not land yet: `credits-1` diverges at 858,149 of 864,424.**
Its window is `reference_frames=65.99`, one interval spanning 66 frames of the
credits' LCD-off stretch, so ~264 timer ISRs land in a single
`schedule_close` batch while the ROM interleaves them with the credits code.
The bytes are `wMusicChannelPointers` (51 against 26), `wMusicCh1CurPitch` and
`wMusicCh3CurOctave`, i.e. the stream is at a different note, and no
`lag track: N sync points off schedule` row appears, so the port delivered
exactly the recorded schedule. It is the same class as the `PlaySFX` fix
below -- a game write to driver state mid-interval that the port applies at a
different tick -- and closing it means another sync point, which means another
full re-derivation. Landing `GATED = 5` before that would drop `credits-1`'s
ratcheted floor from 864,424 to 858,148.

**The $3F SFX driver row is fixed, and it was the sync model.** `ai-duel-0c`
was byte-exact through anchor 30831 and at 30832 the port's
`wSFXCommandPointers` for channel 1 sat six bytes ahead of the ROM's ($DE4D
`0xd7` against `0xd1`) with `wde2b + 1` at `0x80` against `0x00` -- an
envelope command the ROM had not reached. It began exactly where the duel's
SFX id changes ($DD82 `0x91` -> `0xb4`) and oscillated for the rest of the
sound; five other sessions diverged on the same two bytes.

Ruled out by reading, all faithful to the asm: the dispatch table
(`sfx.asm:103-138`, high nibble, unused 9-14 re-dispatching), every handler's
operand length (frequency, envelope, pitch-offset, wait and pan take one byte,
duty and wave none), `SFX_Play`'s mask walk -- which advances `de` but not the
header pointer for a channel whose bit is clear -- and both loop commands,
including `SFX_endloop` leaving `wde3f` unwritten on the finishing pass.

The cause is the sync model, not the SFX driver, and it is proven. A sync
point is recorded and replayed at the *home wrapper's entry*
(`TIMER_SYNC` `(None, 0x3796)` `PlaySFX`), but the store the driver makes is
several instructions later, in bank $3d, and on hardware a timer ISR fits in
between. Traced on the reference across the interval closed by anchor 30832,
whose lag line is `86450 5 1 0` -- five ticks, one sync at offset zero:

```text
SYNC PlaySFX ticks_so_far=0 counter=0x28 sfx=0x91
ISR #1 counter=0x28 sfx=0x91      <- old id still stored, so this update
ISR #2 counter=0x29 sfx=0x34         runs the old stream (0x4ae8...)
```

`0x28 & 3 == 0`, so ISR #1 *is* a sound update, and it ran before the request
became visible. The port has no interrupts inside a C statement: it delivers
the recorded zero ticks, stores the id atomically, then delivers all five at
`schedule_close`, so its first update already sees `0x34` and starts the new
sound one update early. Six bytes of stream is what that one update consumes.

The sync is recorded and replayed at the driver's store instead of at the
wrapper: `3d:4028`/`3e:4028` for `wCurSongID` and `3d:4048`/`3e:4048` for
`wCurSfxID`, found by searching the bank for `EA 80 DD` / `EA 82 DD` inside
the routine's span, since `poketcg.sym` names labels and not instructions.
`TIMER_SYNC_ADDRESSES` had to become a set of banks per address, because the
parallel $3d/$3e copies sit at identical offsets and a plain
`{address: bank}` map silently kept only one of them.

**Place the port's `frame_boundary_timer_sync()` before the routine's *first*
store, not before the one the reference records.** `Music1_PlaySFX` writes
`wSfxPriority` and then `wCurSfxID`; syncing between them delivers the
interval's ticks after the priority write, and the driver update inside that
tick runs `Func_fc26c`, which clears `wSfxPriority` because no SFX channel is
claimed yet. `challenge-hall` caught it at 186,470: `wSfxPriority` 0 against
the ROM's 10, writer `Music1_PlaySFX`. The recorded count is "ticks before the
last store", so delivering them before the first store is right whenever no
tick falls between the two -- and when one does, the reference shows the same
clobber. The port's `Music1_PlaySFX` also stored the id on two paths where the
asm has one (`.play_sfx` handles SFX_STOP with `b = 0`); it is one store now,
which is what a sync point can attach to.

**A gated region needs an attribution mapping or its divergence is silent.**
`region_field` knew `vram` and nothing else, so with `audio` gated `attribute`
raised `KeyError: 'audio'` after printing `WINDOW` and every audio divergence
reported zero `DIVERGE` rows. It maps `audio` onto the `wram` field now, which
is where those bytes live, and the rows name `wSfxPriority` and friends with
their writers.

**The regeneration is automatic, and that is by design.** `stream_key` hashes
`TIMER_SYNC`, `TIMER_SYNC_HL` and `VBLANK_SYNC` (`session.py:296`), so moving
a sync point changes every session's stream key and the next `session-verify`
re-derives that session from boot rather than replaying against a schedule the
port no longer follows. There is nothing to invalidate by hand and no
call-track patcher to write -- one was written here and deleted as dead code
once the key was read properly. What it costs is the replay: the sessions run
0.8M to 1.7M anchors each, about 1750 anchors per second per worker, so warming
all 81 with four workers is hours of wall time. Warm them in parallel before a
sweep (`build_reference` per session in a process pool) instead of letting a
serial sweep pay for it one session at a time.

**Fix both driver copies, and check the other one before believing a sweep.**
`Music1_UpdateVibrato` and `Music2_UpdateVibrato` are the same routine in two
song banks. Only music1's was purified in the first pass, and the gated sweep
put 29 sessions at the identical ordinal 100,243 -- one shared cause on the
common route prefix -- with `wMusicCh1CurPitch` two off. A watchpoint on
`g_wram[0x1DA5]` named `Music2_UpdateVibrato` in one stop. An identical
ordinal across many sessions means one defect on the shared prefix, not many.

**The boot interval's sync offsets were clamped.** `lag_track` derives each
driver call's tick offset with `unwrap(counter - prev, elapsed / TICK_TIME)`.
At index 0 `prev` is zero and `elapsed` spans the whole boot, but the timer is
only enabled for its last stretch: 14 ticks against an 840-tick estimate, so
`unwrap` added three modulus turns and `min(dt, ...)` pinned every offset to
`dt`. The port then ran all 14 ticks at the first driver call, before
`HandleTitleScreen`'s `PlaySong(MUSIC_STOP)`, where the ROM runs ISRs 2-5 after
that write and its driver marks the song finished. One byte, `wCurSongID`
`0x00` against `0x80`, at anchor 1 of every session. Index 0's counters are
absolute, so they need no unwrapping at all.

**`Music1_UpdateVibrato` is a pure function and the port stored its result.**
The asm returns the modulated pitch in `de` (`music1.asm:1437-1465`) and leaves
`wMusicCh1CurPitch` holding the base pitch; the port wrote the modulated value
back, so vibrato accumulated into the base and the high byte lost its `and $7`
mask. `Music1_f490b` then read the pitch from WRAM instead of taking `de`. Both
signatures now match the asm. Its four cases all seeded a zero vibrato delay,
so every modulated arm was unreachable by construction, and the probe adapter
read the result back out of WRAM -- the port and its adapter written to the same
wrong assumption, which no case matrix can catch. Six cases now cover positive
and negative deltas, the carry into the masked high byte, the `$80` chain and
the `$80,$80` restart.

**Channel 3's stop arm writes channel 1's tie byte.** `Music1_f479c`'s
instrument-zero exit is `ld hl, wMusicTie` -- offset zero (`music1.asm:1271`) --
where `f4714` writes `wMusicTie` and `f475a` writes `wMusicTie + 1`. The port
folded all four channels into one helper keyed by `wMusicTie_PTR[ch]`, so it
wrote `+2` and left `+0` alone, which is the ROM's behaviour inverted on two
bytes at once. The same fold also tested the instrument before the wave-change
block, where the asm loads the wave instrument first. Both copies of the driver
(`music1.c`, `music2.c` -- parallel ROM banks, not a duplication defect) had it.

A ROM asymmetry between four parallel routines is exactly what a shared helper
erases. When the port collapses `Music1_f4714`/`f475a`/`f479c`/`f480a` into one
body, diff each arm against its own asm before trusting the parameterisation.

`tools/run_mutation.py` compared its baseline before rebuilding, so a source
edit not yet compiled into `build-barrier` was attributed to the mutation: the
first canary run here reported `MUTATION_BASELINE_FAILED` naming the *old*
body's output. It rebuilds first now.


## `entry` mode is the discriminator a `cuts` row needs

A `cuts` row whose recorded pc is a callee's entry is usually declared
`pre-ret`, and that declaration hides a truncated body: the reference stops at
the callee while the native lane runs on to its own return, and with
`compare: ()` and no observable write in between the row passes. Re-declaring
the same pc as `entry` -- same address, same bank, plus the callee's name --
makes `compare_one.py` compare the two lanes' stop points, and a body that
never reaches the call fails with `mismatches: {"completion": ["<callee>",
"return"]}`. That is a real discriminator for the truncation, and it needs no
new case.

Converting the seven `cuts` rows this way found six truncated bodies. Two are
fixed: `SendCard` was an empty body where the asm is `farcall _SendCard`
(`menus/common.asm`), and `GameEvent_GiftCenter` was missing
`farcall HandleGiftCenter`, the `wGiftCenterChoice & $ef` clear, `ResumeSong`,
the bank restore and the `scf` -- its cases were `oracle: False`, so no lane
had ever compared it to the ROM; they are oracle-backed at the handler's entry
now and the dispatch returns its carry like `GameEvent_BattleCenter` does.

**Boundary and body land together.** The other four (`_SendCard`,
`_SendDeckConfiguration`, `GiftCenter_SendCard`, `GiftCenter_SendDeck`) were
reverted to `pre-ret` rather than left in `entry` mode with a failing baseline:
a canary whose baseline fails cannot run at all, and `audit_mutations` only
proves that an anchor resolves, so leaving them converted would have left four
routines silently unguarded.

They are blocked on an entry-register contract, not on missing callees -- all
sixteen callees of the four tails are ported. `RequestDataReceivalThroughIR`
reaches `TransmitRegistersThroughIR`, which stores *every* register into
`wIRDataBuffer` and transmits it, and the caller then does `add b`
(`link/ir_core.asm`), so `b` at `_SendDeckConfiguration`'s entry is observable
on the wire. The asm never sets it: it belongs to the deck-machine caller
(`menus/deck_machine.asm:2202`, `bank1call SendDeckConfiguration` then
`ret c`), whose own body is one of the four truncations. So this is one
bottom-up region port with `b` threaded from the deck machine down, and
everything below `LoadLinkConnectingScene`'s entry is transcription-only for
the same reason `ChallengeMachine_Duel` is: no IR peer answers, so no lane can
reach those exits.
