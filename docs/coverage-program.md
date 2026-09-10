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
