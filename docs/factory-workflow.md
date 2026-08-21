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
`generation < --retry-limit`; the default autonomous limit is `1`. Retry order
is `(generation, -cascade, size, name)`, so every red receives its bounded retry
before any routine receives another. A quarantined artifact, including a
`stale-owned-path` artifact, does not suppress reissuance.

Each `factory-next` invocation prints one deterministic status line:

```text
NEXT status=<selected|active|stalled|complete> selected=<n> fresh=<n> retry=<n> active=<n> preflight_blocked=<n> exhausted=<n> eligible=<n>
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

## Landing and stale ownership

`factory-land` first requires a clean checkout synchronized with `main@origin`.
Before copying any artifact, it reads the identity `base_commit` and exact
owned quartet plus mutation-receipt paths. It compares `base_commit..main` only
for those paths. An unrelated landing is compatible. If an owned path changed,
the artifact is not copied; a quarantine record is appended with
`failure_class="stale-owned-path"`, the changed paths, and the artifact hash.
Other compatible artifacts continue through the batch.

For compatible artifacts, the driver applies bundles, commits, runs
`just oracle-release-gate`, requires a complete gate naming the checked source
revision, refreshes progress, commits, pushes, and records
`.factory/landings.jsonl`. Gate failures split batches; a singleton gate
failure is quarantined. The release gate and clean-tree/origin guards are
unchanged.

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
