# Autonomous Port Factory

The factory keeps orchestration state in the repository. The orchestrating
session owns repository and jj writes; candidate generators are stateless,
run in disposable lanes, and receive no credentials. `.factory/blocked.toml`
is the temporary operational-disposition file. It is not a scope exclusion.

The exact user message `start` launches the loop in a normal top-level session.
The loop stops only at `complete` or `stalled`.

## Attempt lifecycle

`factory-next` issues an immutable attempt. Issuance creates one directory:

```text
.factory/try/<Fn>/current.json
.factory/try/<Fn>/attempts/<attempt_id>/packet.json
.factory/try/<Fn>/attempts/<attempt_id>/prompt.txt
.factory/try/<Fn>/attempts/<attempt_id>/candidate-<i>.json
.factory/try/<Fn>/attempts/<attempt_id>/result.json
```

`current.json` contains exactly `schema`, `fn`, `attempt_id`, `generation`,
`context_sha256`, `base_commit`, and `state`. State is `issued`, `red`,
`green`, or `stale`. Flat packet, prompt, candidate, and result files from the
old layout are ignored; they are not compatibility aliases.

An issued attempt is never rewritten into a new UUID merely because another
basename lands. Verification rebuilds the packet against the current tree and
hashes only translation-relevant context. If the hash is unchanged, the
original attempt ID and generation are retained and the packet is rebased to
the current `base_commit`. The artifact therefore names the actual tree being
verified. If the context hash changes, the attempt becomes `stale`; no
candidate is verified and the next selection issues a new prompt.

A candidate is read only from the current attempt directory. A flat candidate,
or a candidate whose `attempt_id` belongs to another attempt, prints
`stale candidate ignored` and never becomes a schema/model failure.

## Selection and retry order

Normal selection issues only ready routines without a current attempt. It
preflights the target case module before counting a routine as selected:

- `new`: the case file will be created by surgery;
- `legacy-appendable`: `SCHEMA2_CASES` is derived through
  `legacy_to_schema(CASES, CONTRACT)` and legacy fragments can append;
- `native-migration-required`: the module is hand-written schema-native and
  must be migrated by an orchestrator-owned repository change.

A native module is reported as
`NEXT <Fn> blocked phase=preflight detail=native-migration-required`; it is not
dispatched, and the selector backfills from the next basename. Direct
`factory-try <Fn>` applies the same preflight and operational-blocker policy.

`--retry-red` is a disjoint mode. It selects only current `red` attempts whose
`generation < --retry-limit`; the default is `8`. Retry order
is `(generation, -cascade, size, name)`, so every red receives its bounded retry
before any routine receives another. A quarantined artifact does not suppress
reissuance. A red that exhausts the limit, or repeats one diagnostic, is retired
to a `blocked.toml` stanza by `factory-heal` so it stops occupying the frontier.

Each `factory-next` invocation prints one deterministic status line:

```text
NEXT status=<selected|active|stalled|complete> selected=<n> fresh=<n> retry=<n> active=<n> preflight_blocked=<n> exhausted=<n> eligible=<n> reaped=<n> revoked=<n>
```

Exit codes are `0` when an attempt was selected, `3` when issued attempts are
still active, `4` when ready work is stalled by blockers, exhausted retries, or
preflight failures, and `5` when no eligible or unresolved work remains.

The exact-`start` loop drains fresh work first, then performs one bounded retry
pass. It never hand-repairs a red candidate and never repeats an exhausted
retry pass.

## Candidate and verification flow

1. Run `python3 tools/factory/try_one.py --next 4` and dispatch the printed
   candidate commands. Each command names the attempt-scoped prompt and
   candidate directory.
2. Run the printed `factory-try` command. It validates the exact
   TranslationReplyV2 shape, applies marker fragments in a disposable lane,
   and validates the whole issued wave before any `factory-land` invocation.
   Whole-wave validation minimizes packet churn while unrelated landings remain
   compatible.
3. The verifier inspects schema evidence. Every routine needs at least one
   `evidence == "primary"` record. Only primary indices are sent to
   `compare_one.py`; scene, intentional-transform, native-stress, and
   dependency-blocked records are supplemental. Mutation witnesses must also
   resolve to primary records. A routine with no primary record returns
   `phase=cases failure_class=unsupported-evidence detail=no primary oracle case`.
4. The first green candidate stages an immutable artifact in
   `.factory/artifacts/`. Red results stay attached to their attempt and are
   eligible only for the bounded retry mode.

## Landing

`factory-land` first requires a clean checkout synchronized with `main@origin`.
It then grafts each bundle: `surgery.extract` reads the bundle's own marker
blocks and `surgery.apply` writes them into the checkout, replacing a block in
place when its marker exists and appending otherwise, merging statics
append-only against the destination. Two artifacts for one basename therefore
compose, whatever each was verified against, so there is no `base_commit..main`
path comparison and no `stale-owned-path` quarantine class. Mutation receipts
are copied, being one file per routine.

Landing is monotone in the marker census: the set of routines carrying a
`/* >>> factory <Fn> */` block under `src/home/` may only grow. A batch that
shrinks it, or whose graft raises, is discarded with `jj restore` before any
commit and rejected as `marker-regression` or `graft-failed`.

The driver then commits, runs `just oracle-release-gate`, requires a complete
gate naming the checked source revision, refreshes progress, commits, pushes,
and records `.factory/landings.jsonl`. Every rejection - gate, census, graft -
splits the batch in half and recurses; a rejected singleton is quarantined with
its `failure_class` and moves on.

## Concurrent orchestrators

Any number of top-level sessions may run this loop in one checkout. There is no
session id and no registration; every guard is a `flock` under
`.factory/locks/`, so a killed session releases everything it held.

Selection and issuance hold `select.lock`. A session never issues a routine
already claimed by another session's issued attempt, and never issues a second
routine of a basename that another issued attempt owns — surgery is per
basename, so two live attempts on one basename would waste one of the two
greens on a translation the other has already superseded.

Each verifying process claims one lane by `flock` under
`/tmp/poketcg-factory/`. `factory-next` no longer prints a lane and
`factory-try` no longer accepts `--lane`: a lane index derived from position in
a wave collides across sessions, and two rsyncs into one lane can green an
artifact built from another attempt's tree.

`factory-land` holds `land.lock` and is the only central-gate runner. A second
session gets `LAND busy detail=another session holds the land lock` and exit
`3`. That is not a failure: keep generating and verifying, artifacts persist in
`.factory/artifacts/`, and whichever session next acquires the lock lands them.
`just factory-land` will additionally print its own recipe-failed line for exit
3; that is expected for a busy lander.

A session whose translation context changes under it because another session
landed gets `stale` on its next verification and reissues. An artifact whose
`base_commit` names a revision the gate later rejected and abandoned still
grafts, because grafting never resolves the base; the release gate is what
decides whether that translation still holds, and a rejected singleton is
quarantined and reissued. Both paths self-heal.

## Self-healing

Three failure classes strand the loop without failing anything, so nothing
retries them and the frontier reports work that can never move. Every loop
iteration starts with `just factory-heal`, which repairs all three from on-disk
evidence and prints

```text
HEAL status reaped=<n> revoked=<n> retired=<n> half_landed=<n> blocked_toml_dirty=<0|1>
```

- **revoked** — a landing recorded in `.factory/landings.jsonl` whose marker
  blocks are not in the tree. The artifact payload is immutable and
  gate-verified, so the repair is to re-land it, not to re-port: a record in
  `.factory/revocations.jsonl` removes it from `select_artifacts`' exclusion set
  and from the attempted-names set, and the next `factory-land` grafts it back.
  A routine present in exactly one of the two censuses is reported
  `HEAL half-landed <fn>` and left for the gate to diagnose.
- **reaped** — an `issued` attempt that can never be verified, because its
  routine picked up an operational blocker, left the ready frontier, or its
  issuing session died. It becomes `stale`, which is what the fresh pool
  accepts, so the routine re-enters selection with its generation intact.
- **retired** — a `red` that both pools have abandoned gains an `AUTO-RETIRED:`
  stanza in `.factory/blocked.toml` carrying its last diagnostic. An operational
  blocker is an input to the derived work records, so `factory-heal` also
  refreshes `site/data/progress.json` and `site/data/history.jsonl`; commit
  `.factory/blocked.toml` together with `site/data/` in one `chore(factory):`
  commit when `blocked_toml_dirty=1`, before `factory-land`, which requires a
  clean checkout. Committing the blocker alone publishes a snapshot that
  disagrees with its own blocker file, and `report.py check` fails the push.

`factory-next` performs the revoke and reap steps inline under `select.lock`, so
a bare selection is self-healing; only retiring needs the explicit command.

`--capabilities N` (`just factory-capabilities N`) ranks what is left by
*marginal* unblock count — how many routines become reachable if that one
obstruction is cleared and every other stays. A routine gated by four blocked
roots is freed by none of them alone, so a transitive-dependents count
overstates a capability's value by an order of magnitude. Two obstruction kinds
are ranked: an operational blocker, and a routine whose C body already exists
(`already-implemented`, which preflight rejects forever).

## TranslationReplyV2

Generators return one JSON object with no additional fields:

```json
{
  "schema": 2,
  "attempt_id": "<issued attempt>",
  "statics": null,
  "cases_statics": null,
  "routines": [
    {
      "name": "<packet routine>",
      "c": "...",
      "header": "...",
      "probe": "...",
      "cases": "...",
      "mutation": "...",
      "completion": null
    }
  ]
}
```

Routine names must exactly match packet order. Session-owned surgery is the
only writer of the four source files. Candidate agents never write source,
run VCS, hold credentials, or spawn agents.

## Stop states

`active` means issued attempts still need candidates. `stalled` means ready work
exists but every candidate is operationally blocked, preflight-blocked, or has
exhausted its retry limit. `complete` means no eligible or unresolved work
remains. Progress is measured from `site/data/gate.json` and
`site/data/progress.json`; the dashboard reads those same files.

A `stalled` verdict is followed by the `CAPABILITY` block, so the stall names
its own remedy instead of requiring a forensic dive:

```text
CAPABILITY <blocked|implemented> <name> marginal=<n> unblock=<text>
CAPABILITY status reachable=<n> blocked_roots=<n> already_implemented=<n>
```

With more than one session running, `stalled` and `complete` are per-session
verdicts and are not authoritative while another session still holds issued
attempts; the same status line reports that as `active=<n>`.
