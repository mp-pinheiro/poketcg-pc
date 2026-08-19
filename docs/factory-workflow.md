# Factory workflow

The exact message `start` runs this adapter, and `just launch-port`
(`tools/factory/run.sh`) runs the same loop headless. Work selection is
exclusively `control.py frontier`; never hand-pick a routine and never
materialise a packet outside a claim.

## Authority

Forgejo is the only durable authority. Every state transition is an
append-only comment on the work's own issue, written through
`tools/factory/ledger.py` and read back by `control.py` before any decision:

| fact | where it lives |
|---|---|
| what work exists | one open issue per work ID, `poketcg-port-work:v1` marker |
| what is claimed | `claim` event comment + its lease expiry |
| what an attempt produced | `attempt-result` event comment (`productive` / `diagnostic`) |
| what landed | `landed` event comment naming the pushed revision |
| who owns the factory run | `run-claim` / `run-heartbeat` / `run-release` on the control issue |
| the port frontier | derived from `site/data/inventory.json` + `site/data/gate.json` |

There is no local queue, no `.factory/state.sqlite3`, and no supervisor
journal. Local disk holds only reproducible caches: `.factory/issues-cache.json`
(ETag-validated snapshot), `.factory/artifacts/<sha256>/` (immutable verified
bundles), `.factory/v2/prompts/<packet_sha256>.json` (the exact prompt an
attempt was issued), and lanes under `/tmp/poketcg-factory/`. Deleting any of
them costs a refetch, never a decision.

Every control response is one JSON object on stdout:

```json
{"schema":1,"op":"frontier","status":"ok|waiting|conflict|stop|complete",
 "run_id":"…","snapshot_sha256":"…","data":{…},
 "error":{"class":"…","detail":"…","retry_at":null}}
```

`status` is the whole protocol: `ok` proceed, `waiting` sleep until
`data.waiting_until`, `conflict` another runner owns it, `stop` a human must
look, `complete` the port is finished and proven.

## Preflight

```sh
just build-barrier
just factory-preflight
just factory-status
```

`preflight` proves REST auth, that `site/data/gate.json` was produced at the
current `main` revision, and that the issue snapshot is stable. `status`
prints the reduced ledger: per-work state counts and the live run lease.

Stop on unavailable authorization, a gate record from a different revision,
remote divergence, or an existing live run lease you do not own.

## The run lease

One runner at a time. `run-claim` writes a lease comment on the control issue
and wins only if `ledger.elect_lease` picks it; `run-heartbeat` extends it
every tick; `run-release` ends it. A crashed runner's lease simply expires, and
the next `run-claim` wins. `conflict` from `run-claim` means another runner is
alive - exit, do not steal.

## The loop

`tools/factory/run.ts` is the loop. Each tick, in order:

1. `run-heartbeat` - extend the lease. A failed heartbeat aborts the tick.
2. `reconcile` with `adopt: true` - re-attach `.factory/artifacts/` bundles to
   their `attempt-result` events, and report bundles whose event is missing.
3. `frontier` - `scheduler.plan(...)` over the reduced ledger and the declared
   capacity (`job_slots`, `verifier_slots`, `active_jobs`,
   `provider_throttled`, `verifier_queue_p95`, `healthy_completions`). Exactly
   one of `assignments`, `integration`, `blocker_review`,
   `dependency_analysis`, `waiting_until`, or `complete` is populated, so a
   tick has exactly one job.
4. The orchestrator session executes exactly one tick against that frontier
   using only the `factory` tool.

The session is persistent (`SessionManager.continueRecent`) and restricted to
`factory`, `read`, `grep`, `glob`, `eval`, `task`, `hub`. It cannot run `bash`,
write files, or touch VCS: the control plane owns every write.

### Per assignment

```text
claim   -> dispatch a port-worker subagent in the issued lane
record  -> verify the lane, publish the artifact, append attempt-result
```

`claim` materialises the packets, provisions the disposable lane, stores the
prompt artifact, and appends the `claim` event. It returns `attempt_id`,
`claim_comment_id`, `packet_sha256`, `lane_index`, `lane_capability`,
`owned_paths`, the deadlines, and the exact `prompt`. `conflict` means another
claim won: drop it, do not retry in place.

Dispatch that prompt to a `port-worker` subagent (model `@task`/`@smol`) whose
only job is to write the four owned files inside `FACTORY_LANE_ROOT`. Lanes
carry no `.git`, no `.jj`, no credentials, and no repository config.

`record` re-validates the lane manifest against `packet_sha256`, runs the
oracle verification, and - only on green - stages and stores the immutable
artifact, then appends the `attempt-result` event. A `diagnostic` outcome
carries the normalized verdict; the work becomes recoverable at the next tick
with a higher recovery tier. Record every finished attempt immediately: an
unrecorded attempt is invisible work and its lease will expire.

### Integration

When `frontier` returns `integration`, call `integrate` with those issue
numbers. Integration is the only writer of the repository:

1. append `integration-start` on the control issue with the batch identity and
   expected remote revision,
2. apply the artifacts into `.factory/integration-repo/`, run the candidate
   proof (`just`-driven build + gate), commit, and push to `main`,
3. refresh `site/data/progress.json` and the factory projections,
4. append `landed` on every member issue with the published revision, then
   close it.

A heartbeat thread holds the run lease for the whole push. A remote revision
that moved under the batch aborts before the push, never after.

## Recovery ladder

Every tier comes from the work's own event history - `diagnostic_count` and
`repeat_fingerprints` in `ledger.reduce_work`, folded by
`scheduler.recovery_tier(...)`. No tier is chosen by prose, and a productive
result or an `unblock` resets both counters.

| tier | trigger | route / kind |
|---|---|---|
| 0 | fresh work | `smol` / `completion` |
| 1 | one diagnostic | `smol` / `completion`, verdict as feedback |
| 2 | two diagnostics, or one repeated fingerprint | `task` / `task` |
| 3 | three diagnostics, or two repeated fingerprints | `task` / `repair` (`factory-helper` in the lane) |
| 4 | four diagnostics | escalated: `block` event, no further claims |

A tier-4 `record` appends a `block` event with reason `recovery-exhausted` and
projects `port/blocked` + `attention/human`. The scheduler then refuses to
claim it and lists it in `blocker_review`; an authorized `/factory unblock`
comment clears the escalation and its counters.

Complexity also routes: a cohort or a `tier >= 2` routine starts on the `task`
route, because a one-shot completion cannot carry it.

An expired lease is not a failure: the work returns to `ready` at the next
frontier with its diagnostic history intact.

When at least three works are in recovery with two or more infrastructure
failures each, `frontier` reports `infrastructure_incident: true` and waits
instead of dispatching - a broken harness must not burn the queue.

## Blocked and dependencies

`dependency_analysis` means the work's callees are unported - a dependency fact
from the inventory, not a judgement. Forgejo issue dependencies mirror it so
the human view matches the scheduler. Cohorts (`cohort:v1:<digest>`) exist for
genuine dependency cycles: one issue, one claim, one artifact group, all
members landing together.

## Reconciliation

`factory-migrate` (dry run) and `factory-migrate-apply` reconcile Forgejo with
the current inventory: create missing work issues, create cohort issues for
cycles, mark excluded routines, and attach dependency edges. It is idempotent
and refuses to run when the gate record and `main` disagree.

## Forecast

`just factory-forecast` runs a Monte Carlo over the remaining work using
measured per-work throughput, dependency depth, and lane concurrency. It
reports p50/p85/p95 dates with a confidence label, and `site/data/factory-forecast.json`
feeds the dashboard. A forecast without measured throughput is reported as
`low` confidence, never as a date.

## Invariants

- One runner: the control-issue lease is elected, heartbeated, and released.
- One claim per work: `ledger.elect_lease` decides, the writer verifies it won.
- Attempts are immutable: an `attempt-result` event is never rewritten.
- Artifacts are content-addressed and verified before they are trusted;
  `reconcile` re-attaches them and reports orphans.
- Lanes are disposable and credential-free; only the control plane writes the
  repository, jj state, or Forgejo.
- Integration gates before push and records the exact pushed revision.
- Forgejo labels are a projection; a stale label never suppresses dispatch.
- `PORT COMPLETE` comes only from `complete`, which requires an empty frontier,
  no unfinished work, no blocked work, and a green gate at the pushed revision.
