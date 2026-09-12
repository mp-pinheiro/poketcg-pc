# The coverage program

Five loops that turn "which routines has no recorded route ever executed" into
recorded, verified, landed sessions without anyone typing a route by hand. Each
loop is one `just` recipe with one input artifact, one output artifact and one
stop condition; they compose through files, and every one is idempotent.

```
Discover ─┐
          ├─► Intake ─► Fix ─► Prove ─► Ledger ─► (Discover, Target)
Target ───┘
```

The Fix loop is `docs/grind.md`, unchanged: it is the one loop with judgement
in it. Everything else here is mechanical.

## The prompt

Paste this into a fresh session. Work selection is deterministic; every branch
is a lookup here or in `docs/grind.md`.

```text
Advance the poketcg-pc native port by closing coverage. Read completely, in
this order: docs/coverage-program.md (this file), docs/grind.md ("Issues: the
worklist", "The session loop" and its decision table, "Reach", "Throughput
rules"), AGENTS.md (file ownership, commands).

Once, before the loop: export POKETCG_BUILD=build-<your name>
POKETCG_SESSION=<your name>; just build; just build-trace.

The loop, until a stop condition holds:
  1. just issues-next 1 --claim
     Work any p0/p1/p2/p3 fact per docs/grind.md, land the fix, just
     issues-sync, back to 1. Two classes are deferred, not yours to start:
     ISR-placement facts (#3387, #3392, #3393 - a divergence whose writer is
     an interrupt body in an interval with no sync point; a new sync site
     re-keys every cached reference and costs ~1.5-2 h of blocked
     verification) and link/IR audit facts (#3217-#3252 - they need a
     dual-core linked reference build, a capability this repo does not have).
     Say so in the report; do not open either.
  2. No workable fact: just coverage-status. It prints an UNMEASURABLE row -
     those routines are a registration gap, never coverage work. While
     src/engine/duel/effect_functions.asm still misses routines:
     just coverage-target --limit 20 --land
     A carrier the AI refuses to play needs a board, not button search:
     just session-board-seed <name> --card <CARD> --attack N --then
     "Bx5,DOWN,A,DOWN,A,Ax5"   records the seed and the play in ONE session
     (a seed recorded separately has its pokes fire past its own length and is
     inert); 22 of the first 25 attack carriers hit on that tail.
  3. Cheap reach search before recording anything new:
     just coverage-probe <landed session> --tail "<explore labels>" --mark <Fn>
     One native run per tail (~0.5 s, no reference replay), reporting the
     unexecuted routines it reaches. Iterate tails, then record the winner
     with the same labels (session.py seeded/board-seed --then) and verify.
     Probing a session the ledger already folded must report nothing but DMA;
     anything else is a port defect (an invented call) or a measurement gap.
  4. Then the search loops, from the ranked clean seeds:
     just coverage-discover --limit 2 --jobs 2
     just coverage-intake <seed> --top 3 --land
  5. Seeded content route items (just issues-next, label route):
     just savegen base NAME --from SESSION --at N
     just savegen edit <sav> --out <sav> --medals N --pack 0=1 --event EVENT_X=1
     just session-seeded NAME <sav> --then A,Ax5   (verify, land, then use it
     as a coverage-discover seed)
  6. After every landing: just coverage-ledger --jobs 8, then just issues-sync.

Proof obligations per landing:
  - a C fix: just oracle-diff <Fn> PASS, just lint-constants clean, a fixture
    case at the real entry and one red mutation, the sweep window that
    reported it comes back with the routine gone, then
    just sessions-verify-affected <Fn> --jobs 5
    A defect no case can observe (an invented call, a text header outside the
    compared set) is landed with its real proof named - the reach probe or the
    session - and no fake mutation.
  - a sound-driver change: just audio-tickdiff  (66 seeds, must be all clean)
  - a new session: just session-verify <name> --write-ratchet; land it clean
    OR diverged - a diverged session is how a fact enters the tracker.
  - a landing batch: just sessions-sweep --jobs 8 --write-ratchet

Throughput rules (each of these cost hours once; docs/grind.md measures them):
  - Never hand-roll a serial verify loop in bash. sessions-sweep <names>
    --jobs N --write-ratchet freezes the lane and parallelises: 26 sessions
    1m15s against 17 min serial, all 470 in 7m04s at --jobs 8.
  - Never pass --force to coverage-ledger after a C fix. The ledger replays
    the REFERENCE, keyed by stream key plus confirmed ordinal, so coverage is
    ROM-derived and a C fix cannot invalidate it. Two forced re-traces cost
    3 h and changed nothing; an ordinary fold is 32 s to 2 min.
  - just session-sweep (singular, per-routine, forks its own PyBoy workers)
    runs alone. just sessions-sweep (plural, batch verify) is the parallel one.

Rules:
  - Unattended: never ask; when two options exist take the boring one.
  - The batch loops snapshot the binary into build/completion/verify-lane, so
    editing and building while one runs is safe. A bare just session-verify
    uses the live build directory: a divergence at a tiny ordinal on
    wVBlankCounter is that contamination, not a fact - re-verify.
  - Never run just oracle-release-gate, a formatter, a linter, or any git
    command. Commit with jj only, naming your own paths:
    jj commit <paths> -m "type(scope): subject"   (subject <= 50 chars)
  - Never widen an exclusion ledger and never edit a case to match the C.
  - Never hand-close a fact issue.

Report at the end: sessions landed (name, clean/diverged), the ledger's
executed count before and after, issues closed and opened, and anything left
open with the reason.
```

Stop conditions: `coverage-status` shows only routines with a reason in
`tools/progress/scope.toml` or a peer-harness dependency
(`docs/reach-harness.md`); `issues-next` is empty apart from blocked
placement facts; or a gate needs a decision the loop cannot take.

## Ledger — `just coverage-ledger`

`site/data/coverage.json`: per session the routines it executes, per routine
the sessions that execute it, per file `executed/total`, and the totals.
`tools/completion/coverage_ratchet.json` pins `executed` and may only rise
(`REGRESSION`, exit 3, unless `--write-ratchet`).

The executed set is measured on the **reference**, not the native lane: one
routine-entry trace of the ROM per session (`refstream.routine_trace`),
through the session's confirmed ordinal from `session_ratchet.json`. On a clean
prefix the port matches the ROM at every anchor, so what the ROM executes there
is what the port has proven. The native call trace was measured against it and
undercounts by ~80 routines on `first-duel` alone: the port passes call-site
arguments directly (`GetByteAfterCall`, `GetStackEventValue`), dispatches the
sound driver's command handlers inline (`Music1_note` and its siblings) and
inlines helpers, none of which is a coverage gap. The "60 of 75 `music2.asm`
routines never execute" figure was that artefact.

Each trace is cached in `build/completion/coverage/<session>.json` keyed by the
session's stream key and its confirmed ordinal, so a rebuilt binary costs
nothing and a fix that moves a ratchet re-traces exactly that session. The
corollary is a rule: **never pass `--force` after a C fix.** Coverage is
ROM-derived, so a change to the port cannot invalidate a trace; two forced
re-traces cost 3 h and changed nothing. Measured on the current corpus (493
sessions): a full cold pass is ~7 min at `--jobs 8`, an ordinary incremental
fold 32 s to 2 min. A session that has never been verified has no confirmed
ordinal and is refused: verify it first.

`just coverage-status` ranks files by the routines no session executes, and
prints an `UNMEASURABLE` row first: 26 inventory routines have no entry
address in the reference tracer's table (`coverage_ledger.unnameable`) - the
12 the registration bijection misses, the four `DuelAnim15*` slots,
`FadePalIntoAnother`, the Man1 and legendary-card script commands,
`SetOBP1OrSGB3ToCardPalette`. No replay can report them, so the ledger marks
them `unmeasurable`, holds them out of the worklist, and counts them per file.
`scripting.asm` reads 27 real misses instead of 44 because of it. Closing one
means registering the routine, not recording a session.

## Reach — `just coverage-probe <session> --tail <labels> --mark <Fn>`

The cheapest question in the program, and the only proof class that sees an
invented call. One native run per tail (~0.5 s, no reference replay) answers
"which unexecuted routines does this input reach"; the labels are
`explore.py`'s, so a winning tail records verbatim through `--then`. Probing a
session the ledger already folded must come back with nothing but `DMA`;
`duel-screens` came back with `Func_14323`, which the asm marks
`; unreferenced`, and the defect was a call the translator invented in
`ConvertColorToEnergyCardID`. `docs/grind.md` "Reach" has the full rules and
the three measurement traps.


## Discover — `just coverage-discover [SEED...]`

Runs `explore.py --seed-session <seed> --known site/data/coverage.json` per
seed, budget 6000, two at a time by default (`--jobs`; each search holds a
gambatte core and up to 4,000 savestates). `--known` seeds the search's "seen"
set with the ledger's executed set, so a discovery is a routine **no session**
executes rather than one the seed's own prefix had not reached; before it, two
seeds rediscovered each other's routines. The corpus
(`build/completion/explore-<seed>/`) now carries the routine names each script
found, which is what Intake scores.

Without seeds, every session is ranked by the unexecuted routines in the files
it already touches and the top four (`--limit`, 0 for all) are searched. A
corpus is stamped with the ledger's executed-set digest and skipped while that
digest holds, so a landing that changes nothing about coverage never re-runs a
search.

## Intake — `just coverage-intake <seed> [--top K] [--land]`

The seed must be clean: a session extending a diverged seed can only
re-report the seed's fact, which two recorded `ronald-explore-explore-*`
sessions demonstrated before the guard existed. Diverged sessions are also
scored 0 as Discover seeds, so the ranked frontier stays on seeds whose
scripts can land clean.

Greedy over the seed's corpus: the script whose found routines add most to the
ledger's executed set, then the next given that one landed, up to `--top`
(default 3), stopping when nothing new is left. Each becomes a session
`<seed>-explore-<k>` via `session.py from-script`: the script is the seed's
input plus a suffix, so the seed's pokes apply unchanged and the goal is
generated from the corpus entry. Then `session-verify`, then the commit line
`jj commit tests/sessions/<name> tools/completion/session_ratchet.json` is
printed, or run with `--land`. A diverged session lands too: that is how a fact
enters the tracker (`issues-sync` projects it). A script already recorded under
another name (same input hash) is skipped.

## Target — `just coverage-target [ROUTINE|STEM...] [--limit N] [--land]`

Button search cannot reach most card effects: the AI chooses attacks, and a
deck without the card never plays it. The map is static and
`tools/completion/effects.py` inverts it: `cards.asm` names every attack's,
trainer's and energy's `EffectCommands` table, `effect_commands.asm` names
every table's `EFFECTCMDTYPE_*` routines (228 cards, 317 tables, 566 routine
names). `just effects carriers <Routine>` lists the cards that carry one.

Per unexecuted carried routine the loop picks a carrier (basic Pokémon before
evolutions before trainers), builds a deck and records `effect-<card>[-<slot>]`
with `session.py ai-duel --cards <deck> --arrange --watch <routines>`, six
prizes, opponent deck 2 (Sam's normal deck, the general AI), branched from
`practice-win` at 23,227 like every `ai-duel-*` session. Two mechanisms make
it deterministic:

- The duel's `DUELVARS` hold deck **indices**; card ids are looked up in
  `wPlayerDeck` at every access (`home/duel.asm _GetCardIDFromDeckIndex`), so
  poking the list after the shuffle changes the cards without touching the
  shuffle.
- `--arrange` reads the player's shuffled order at the first
  `DrawCardFromDeck` after the branch in one short reference pass, then pokes
  the deck file's cards onto those indices in order. The deck file is a draw
  order: the carrier's basic, the attack's energy, its evolutions, more energy,
  then a bench basic on the first turn draw, the remaining copies and the
  fillers. Measured on Ekans: an unarranged four-copy deck never played Spit
  Poison in eight turns; the arranged one reached
  `SpitPoison_Poison50PercentEffect` and `PoisonEffect` on the first attack.

`--watch` records each routine's first ordinal in `session.json`. A carrier
none of whose routines fired is not landed as a duel: the directory is replaced
by `effect-<card>-seed`, a player-controlled duel with the same poked deck and
no input past the branch (`session.py deck-seed`), which the Discover loop
then searches with the player pressing the buttons. Every outcome is written
to `build/completion/effects/targets.json`. This loop is the
`completion:v2:p5:duel-state` producer's input: its duel vectors are the
sessions it lands.

## Peer and seeded content

`docs/reach-harness.md` covers what neither Discover nor Target can reach:
save-seeded sessions (`just savegen`, `just session-seeded`) for the packs,
deck machines, credits variants and gift center, and the native serial
transport (`just peer-loopback`, `just peer-printer`) for link, IR and
printer.

These run **in parallel against a frozen lane**. A verify is one native
process reading a cached reference, so sessions are independent; the only
shared mutable state is `session_ratchet.json`, which every verify updates
under a file lock (`session.py ratchet_lock`), and `--write-ratchet` is
therefore safe from a worker. Measured on the current corpus: 26 sessions in
**1m15s** against 17 min serial, 57 in **10m47s**, all 470 in **7m04s** at
`--jobs 8`. `coverage-target` parallelises the same way (8 carriers: 3m23s
against ~12 min serial), with `jj commit` kept in the parent because two
concurrent commits would race the repo.

The lane is a snapshot of the binary and the data pack in
`build/completion/verify-lane/`, taken when the batch starts and used by every
worker through `POKETCG_BUILD`. That removes the hazard by construction: a
rebuild landing mid-batch can no longer swap the binary under a running
verify, which is what fabricated two false facts earlier
(`docs/grind.md`, "ISR placement"). Editing and building are safe while a
batch runs.

`--sample N` verifies only the cheapest N affected sessions. An exit-register
fix cannot change a digest the sweep has already proved at the routine's live
entries, so the full set belongs to the landing batch (`sessions-sweep`), not
to every fix. Changes to timing, audio, the AI or anything shared still take
the full set.


`just sessions-affected <Routine|stem...>` lists, from the ledger, every
session executing one of the routines (a pret file stem such as
`effect_functions` expands to the file's routines), plus the sessions each was
branched from (`derived_from`, followed transitively) and the core set
`boot-menu`, `first-duel`; shortest first. `sessions-verify-affected` verifies
exactly those with `--jobs` workers against the frozen lane; `sessions-sweep`
is every session, the landing-batch check. AI, timing and audio changes still
sweep everything: a change to the driver is executed by every session.

## Stop condition

The ledger's unexecuted set contains only routines with a reason in
`tools/progress/scope.toml` (SGB hardware-only, the Phase-1 transform,
dead code) or a peer-harness dependency named in `docs/reach-harness.md`.
Until then `just coverage-status` is the worklist and the order is Target
(largest file, deterministic), Intake of the ranked seeds, then Discover again
against the new ledger.

### What the unexecuted set is made of

Measured at ledger revision `f012a64a` (619 unexecuted of 3,012, 574 sessions),
by counting every reference to each routine name in the disassembly outside its
own definition line — macro-driven tables count, which a `call|jp|dw` regex
misses and which reports 213 false deads instead of 79:

|count|class|what unblocks it|
|---|---|---|
|266|reachable game code|Discover/Intake/Target: the worklist|
|108|transport|a peer console; the oracle needs a linked reference build|
|106|card effects|board state per card, not tail variation (below)|
|79|dead: no reference anywhere|`scope.toml` rows, e.g. `DoAFrames`, `*_Unreferenced`, `CommentedOut_2c086`|
|26|unmeasurable|a tracer registration gap, never coverage|
|23|`music2` entries|bank-parallel driver copies, `docs/audio-harness.md`|
|11|debug menu|unreachable: its entry `Func_12661` in `debug_main.asm` has no reference either|

So 266 of 619 are coverage work; the rest are typed. The card-effect residue is
not a tail problem: 27 carrier/slot pairs were recorded with the board poke and
both attack-menu shapes (`Bx5,DOWN,A,Ax20,Ax20` for slot 1, the extra `DOWN` for
slot 2) and probed for their own effect routines — **zero** new hits. Those
effects fail a precondition the board poke does not express: a basic Pokémon
left in the deck (`KrabbyCallForFamily_PutInPlayAreaEffect`), an evolved
Pokémon in play (`DevolutionBeam_*`, `PokemonBreeder_*`), damage on the bench
(`DamageSwap_*`), or a populated discard pile (`Scavenge_*`). The next lever is
`--hand`/`--discard` plus a bench poke, one shape per precondition class.

## Milestones

`tools/completion/tracker.py` files sessions by prefix: `effect-` under *Card
effects*, `seed-` under *Seeded content*, `deck-machine-` under *Deck
machines*, `duel-` under *Duel surface*, `audio-` under *Audio*, `link-`,
`printer-` and `ir-` under *Transport*; `<seed>-explore-<k>` inherits the
seed's route milestone. These families are milestones but not route order: the
ordinal-to-milestone map that sweep rows use is built from the route sessions
only.

The gate's milestone set is `tools/completion/requirements.toml`, and coverage
is not what closes it. Audited at content key `f911fc50`: 4 pass, 2 failing,
20 with no evidence artifact at all (`docs/vision.md` "Status" carries the
table and both failures byte-for-byte). Two of the 20 are the ones this
program feeds — `p5:duel-state` and `p5:seeded-duel` take the `effect-*` and
board-seed sessions as their duel vectors — but the producers that turn those
sessions into evidence do not exist yet. A landed session does not move a
requirement until one does; never report coverage as gate progress.
