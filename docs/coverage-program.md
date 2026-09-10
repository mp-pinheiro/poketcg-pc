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
worklist", "The session loop" and its decision table), AGENTS.md (file
ownership, commands).

Once, before the loop: export POKETCG_BUILD=build-<your name>
POKETCG_SESSION=<your name>; just build.

The loop, until a stop condition holds:
  1. just issues-next 1 --claim
     A p0/p1/p2/p3 fact that is NOT an ISR-placement fact: work it per
     docs/grind.md, land the fix, just issues-sync, back to 1.
     ISR-placement facts (a divergence whose writer is an interrupt body and
     whose interval has no sync point: #3387, #3392, #3393) are BLOCKED on a
     user decision -- they need a new sync site and a full re-derivation.
     Skip them; do not start one.
  2. No workable fact: just coverage-status. While
     src/engine/duel/effect_functions.asm still misses routines:
     just coverage-target --limit 20 --land
     Each carrier becomes one arranged AI duel, verified and landed; a carrier
     the AI never plays becomes an effect-<card>-seed search seed instead.
  3. Then the search loops, from the ranked clean seeds:
     just coverage-discover --limit 2 --jobs 2
     just coverage-intake <seed> --top 3 --land
  4. Then the seeded content route items (just issues-next, label route):
     just savegen base NAME --from SESSION --at N
     just savegen edit <sav> --out <sav> --medals N --pack 0=1 --event EVENT_X=1
     just session-seeded NAME <sav> --then A,Ax5   (then verify, land, and use
     it as a coverage-discover seed)
  5. After every landing: just coverage-ledger --jobs 3 (folds the new
     sessions in, ratchets `executed`), then just issues-sync.

Proof obligations per landing:
  - a C fix: just oracle-diff <Fn> PASS, just lint-constants clean, a fixture
    case at the real entry and one red mutation, then
    just sessions-verify-affected <Fn>   (the ledger picks the sessions)
  - a sound-driver change: just audio-tickdiff  (66 seeds, must be all clean)
  - a new session: just session-verify <name>; land it clean OR diverged --
    a diverged session is how a fact enters the tracker.
  - a landing batch: just sessions-sweep

Rules:
- Unattended: never ask; when two options exist take the boring one.
- ONE reference lane at a time. Never run two of session-verify, session-sweep,
  oracle-diff-all, coverage-target, coverage-intake concurrently.
- NEVER rebuild the binary (just build, build-trace, oracle-build-gbref) while
  any loop is verifying. It fabricates facts: a substrate experiment compiled
  under a running coverage-target produced two false `diverged` reports whose
  signature was wVBlankCounter off by one at ordinal 1. If you see a
  divergence at a tiny ordinal on wVBlankCounter, it is contamination --
  re-verify, do not report it.
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
nothing and a fix that moves a ratchet re-traces exactly that session. Tracing
is ~1,000 ordinals/s per worker process; the first full pass over 84 sessions
(19.2 M ordinals) is about 80 minutes at `--jobs 4`, and incremental after
that. A session that has never been verified has no confirmed ordinal and is
refused: verify it first.

`just coverage-status` ranks files by the routines no session executes.

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

## Prove — `just sessions-affected` / `sessions-verify-affected` / `sessions-sweep`

`just sessions-affected <Routine|stem...>` lists, from the ledger, every
session executing one of the routines (a pret file stem such as
`effect_functions` expands to the file's routines), plus the sessions each was
branched from (`derived_from`, followed transitively) and the core set
`boot-menu`, `first-duel`; shortest first. `sessions-verify-affected` verifies
exactly those, one reference lane at a time; `sessions-sweep` is every
session, the landing-batch check. AI, timing and audio changes still sweep
everything: a change to the driver is executed by every session.

## Stop condition

The ledger's unexecuted set contains only routines with a reason in
`tools/progress/scope.toml` (SGB hardware-only, the Phase-1 transform,
dead code) or a peer-harness dependency named in `docs/reach-harness.md`.
Until then `just coverage-status` is the worklist and the order is Target
(largest file, deterministic), Intake of the ranked seeds, then Discover again
against the new ledger.

## Milestones

`tools/completion/tracker.py` files sessions by prefix: `effect-` under *Card
effects*, `seed-` under *Seeded content*, `audio-` under *Audio*, `link-`,
`printer-` and `ir-` under *Transport*; `<seed>-explore-<k>` inherits the
seed's route milestone. These families are milestones but not route order: the
ordinal-to-milestone map that sweep rows use is built from the route sessions
only.
