# Factory workflow

The exact message `start` runs this adapter. Work selection is exclusively
`tools/factory/supervisor.py next`; never rebuild a frontier with
`packet.py build`.

## Authority

`.factory/state.sqlite3` is the scheduler authority. It contains canonical work
rows, immutable attempts, leased actions, append-only failure evidence,
publication phases, blockers, and the Forgejo projection backlog. Queue JSON,
the old supervisor journal, and Forgejo labels are migration evidence or
projections; they do not suppress eligible work.

Create the authority once:

```sh
python3 tools/factory/driver.py migrate-recovery-state --dry-run --json
python3 tools/factory/driver.py migrate-recovery-state --dry-run --json
python3 tools/factory/driver.py migrate-recovery-state --json
```

Both dry runs must report `ok: true`, identical source and partition digests,
zero residual or repeated work IDs, zero active invalid identities, an empty
foreign-key check, and `["ok"]` integrity. The apply command refuses to
overwrite an existing database and publishes the audited image atomically.

## Preflight

Run these checks before the first action in a session:

```sh
just forgejo-auth-check
jj git fetch --remote origin
just bootstrap
uv sync --project tools/oracle --frozen
just oracle-build-gbref
just build-barrier
just issues-fetch
python3 tools/factory/supervisor.py status --json
```

Stop on unavailable authorization, remote divergence, unknown dirty files, or
database identity/integrity errors. Do not stop because work is blocked,
deferred, or not immediately productive.

## Bounded action loop

Start one persistent supervisor process and retain its stdin/stdout for the
whole exact-`start` session:

```sh
python3 tools/factory/supervisor.py session \
  --lease-owner orchestrator --lease-seconds 7200 --lanes 16
```

The process acquires `.factory/supervisor.lock` before printing its `ready`
record and holds it until a `{"command":"close"}` request or process exit. Send
one JSON line `{"command":"next"}` for each iteration. `next` first resumes a
live action owned by this orchestrator, then recovers an expired action, then
plans one new action. A returned empty frontier, `blocked`, or `stalled` result
is diagnostic state, not completion. Continue through the appropriate recovery
action. Stop successfully only when the response value is:

```json
{"status":"complete","message":"PORT COMPLETE"}
```

That value comes from one predicate: the gate is current and green,
`verified_code == verified_code/total`, and
`verified_functions == verified_functions/total`.

Programmatic orchestrators call
`supervisor.supervise(translate_many, recover_many, analyze_failure,
lanes_count=16, verify_width=8)`. Those three callbacks are the only model
seams; the supervisor owns action leases, lanes, verification, bundle
publication, integration, projection, and the completion decision.


### Worker wave

For `fresh-wave`, `retry-wave`, `worker-wave`, and `dependency-scc` actions:

1. Call `workers.translation_assignments(action, lane_indices=...)` for
   attempts at recovery tier 0-3. `supervise(...)` runs one worker per
   assignment; each calls `translate_many([assignment])` — which calls
   `completion(prompt, model=assignment["model"])` outside SQLite
   transactions — then `workers.verify_reply(...)`. A non-green verdict
   re-renders the packet with the verifier's failure detail and calls
   `translate_many` again on the same worker, up to 3 rounds, before the
   assignment escalates. Every assignment already names its disposable lane
   and packet, and every verify subprocess has a hard process-tree deadline.
2. For tier-4 attempts, call `workers.recovery_analysis_requests(action)`
   through the independent `analyze_failure` callback and parse each response
   with `workers.parse_recovery_analysis(...)`. Then call
   `workers.agent_assignments(...)`, passing those analyses, for attempts at
   recovery tier 4. Dispatch every returned assignment in one `task`
   batch. Agents edit only the listed lane and owned paths, run no VCS command,
   and receive no repository, Forgejo, or git credentials. Verify each returned
   lane with `workers.verify_agent_lane(...)`.
3. Tier 4 produces two independent lane assignments carrying the analysis.
   Pass their results in completion order to `workers.first_green(...)`; the
   first verified result wins, otherwise both failure records form one
   diagnostic fingerprint and the work remains retry-ready.
4. For tier-2 diagnostics, call
   `workers.failure_review_requests(action, results)` through the independent
   `analyze_failure` callback. Parse each response with
   `workers.parse_failure_review(...)`, then call
   `workers.merge_failure_reviews(...)`. The review classifies routine-local
   versus shared-harness failures before the next immutable recovery child is
   scheduled.
5. Build one result for every attempt. On model `429` or `5xx`, use
   `{"outcome":"provider-failure","retry_after":N}`. Do not convert provider
   failure into code failure.
6. Send one session request with `command: "accept"` and the action result as
   `payload`. Include `action_id`, `lease_owner`, `lease_token`, and
   `result: {"attempts": {...}, "work": {}}`. Acceptance first validates and
   atomically publishes staged bundles, then commits the result transaction.

`workers.salvage_children(...)` never changes an attempt's membership. A partial
green result creates immutable child attempts whose work IDs exactly partition
the parent; the parent becomes `superseded`.

### Blocker review

For `blocker-review`, call `workers.blocker_requests(action)` through an
independent slow reasoning completion. Parse each response with
`workers.parse_blocker_result(...)`, then submit
`result: {"attempts": {}, "work": {work_id: outcome}}` through the session
`accept` command.

A dependency cycle is not reviewed one routine at a time. The planner creates
one `dependency-scc` attempt; its members share one lane, one verification
result, and one integration action.

### Publication

For `gate-refresh` or `integration`, send one session request with
`command: "integrate"`, the three lease fields in `payload`, and `push: true`.
The action replays the phases `prepared -> applied -> source-committed ->
gate-passed -> progress-committed -> pushed -> finalized`. The central
orchestrator alone applies bundles, runs the candidate proof, runs adapter lint,
the constant audit, `just oracle-release-gate`, rebuilds progress, commits, and
pushes. A failed gate cannot mark work landed. Candidate state, hashes, and the
exact published revision stay attached to the same action ID.

If a crash leaves a prepared candidate dirty, replay permits only paths owned by
the action. It backs those derived files up under `.factory/recovery/<action>`
before restoring the recorded baseline. Any other dirty path is a
stop-the-line condition.

### Forgejo projection

Publication finalization enqueues a Forgejo projection row; it does not make
issue labels part of scheduler eligibility. For `projection-reconcile`, send a
session request with `command: "reconcile"` and the three lease fields in
`payload`.

This runs `issues-sync-apply` and `issues-verify`, then clears the backlog and
finishes the action transaction. Transient projection failure leaves canonical
work state intact and the action resumable.

## Recovery ladder

Each diagnostic records its class, detail, model, and SHA-256 fingerprint.
Recovery advances on new evidence or a repeated fingerprint, through
`recovery_tier` 0-4:

1. tier 0 — ordinary retry, default model;
2. tier 1 — one-routine fresh retry, default model;
3. tiers 2-3 — slow-model retry, the same in-lane repair loop as tiers 0-1
   (up to 3 rounds before escalating);
4. tier 4 — independent analysis followed by two editing agents, first
   verified result wins. Repeated code failure stays at this tier with its
   full history; it does not become a terminal queue state.

Fresh work and recovery use separate capacity. While both exist, roughly 80% of
lanes remain available to fresh attempts and 20% to recovery; every fifth
single-lane tick serves recovery. A generation-4 backlog cannot monopolize all
lanes.

`provider-failure`, `infrastructure-failure`, `blocked`, and `external-stop` are
different outcomes. Provider backoff does not advance a code recovery tier.
Dependency blockers name canonical `blocked_on` work IDs. Harness failures
remain actionable work instead of being hidden in packet terminal states.

## Invariants

- One canonical work ID has at most one current attempt.
- Attempt identity and membership are immutable; salvage creates children.
- An action has one lease owner, token, deadline, input digest, and result.
- Model and agent execution occurs outside database transactions.
- Lanes contain no `.git`, `.jj`, credential helper, config, secret file, or
  repository-auth environment variable.
- Bundle acceptance requires exact identity, marker coverage, importable cases,
  mutation receipts, and a stable payload hash.
- Only the orchestrator writes the repo, jj state, canonical bundles, the state
  database, or Forgejo.
- Integration gates before push and records the exact remote revision before
  work becomes landed.
- Forgejo is a projection. Stale labels cannot suppress dispatch.
- `PORT COMPLETE` is never inferred from no packets, no green bundles, blocked
  work, or a successful action.
