# Autonomous Port Factory

Forgejo issues and append-only factory comments are the source of truth. The
exact user message `start` launches a normal top-level OMP session through
`tools/factory/run.sh`; the script executes `omp --print start`. There is no
nested SDK session manager or factory watchdog.

## Control protocol

The top-level session must run `factory preflight` before `run-claim`.
Project-local model roles are pinned to
`@smol = openai-codex/gpt-5.4-mini:medium` and
`@task = openai-codex/gpt-5.6-luna:medium`; preflight must resolve both
selectors, verify the current gate, and reject a dirty central checkout. After
`run-claim` succeeds, the extension allows only `factory`, `task`, and `hub`
until `run-release` or `complete`.

Each loop iteration:

1. Call `factory reconcile` with the winning run lease.
2. Call `factory frontier`; claim only the returned work IDs.
3. Pass `agent_name` and the resolved `model_id` to `factory claim`.
4. Dispatch one exact generator task with the issued packet and attempt ID.
5. Capture the task completion, then call `hub wait` with `ids: [job_id]`.
   Every 120-second wait timeout heartbeats both the run and work leases.
6. Call `factory join` with the exact joined fields below. It selects the
   newest unused persisted delivery and rejects caller-supplied delivery data
   that differs from that entry. Then call `factory check`; the control process
   applies the candidate in its disposable lane, runs the full verifier, and
   writes an immutable check receipt. A malformed reply stops before lane
   mutation.
7. Send a normalized `VerdictV2` and candidate hash to the same generator for
   a bounded repair round. `@smol` gets rounds `0..1`; `@task` gets rounds
   `0..2`. A red final receipt is recorded once; a green receipt is recorded
   immediately.
8. Call `factory record` with only the receipt `check_id`. It re-hashes the
   receipt and lane and appends exactly one attempt result.
9. Integrate a green artifact immediately for the canary and first three pilot
   greens. Later integration uses at most four artifacts or fifteen minutes of
   age, whichever comes first.

### Joined delivery contract

`factory join` accepts exactly:

```json
{
  "run_id": "<run>",
  "run_claim_comment_id": 123,
  "work_id": "<work>",
  "packet_sha256": "<sha256>",
  "claim_comment_id": 123,
  "round": 0,
  "delivery": {
    "kind": "task-job",
    "id": "<Hub job ID>",
    "agent_id": "<agent>",
    "respawned_from": null,
    "resolved_model": "<resolved model>",
    "duration_ms": 1234,
    "settled_at": "<timestamp>",
    "usage": {
      "input_tokens": null,
      "output_tokens": null,
      "cached_tokens": null,
      "cost_usd": null,
      "source": "omp-hub-v17.4-unavailable"
    },
    "reply": "<TranslationReplyV2 JSON>"
  }
}
```

The delivery `kind` is `task-job` or `agent-message`. A task delivery is
usable only when the captured result has `status:"completed"`, exact `id`,
`durationMs`, `resolvedModel`, and `resultText`. A message delivery is usable
only when targeted `hub wait` returned `waited.id`, `waited.from`, `waited.ts`,
and `waited.body`; its `kind` is `agent-message`, `id` is the waited message
ID, `agent_id` is `waited.from`, `settled_at` is `waited.ts`, and `reply` is
`waited.body`. Both forms are persisted as
`poketcg.factory.delivery.v1` entries. Usage fields are nullable and must use
the literal unavailable source above.

A delivery ID may be joined once only. The join operation verifies the active
run and work leases, claim attempt, packet identity, expected agent, exact
resolved model, and round before storing its immutable receipt. Round zero is
always a task job. Repair rounds are targeted messages from the round-zero
agent; if it disappears, one replacement task job may set `respawned_from` to
that prior agent ID.

A timeout or lease loss cancels only the captured task job and stops before
`join`, `check`, or `record`; it must not cancel unrelated jobs or accept a
later unrelated result.

Only a work-claim election conflict may be dropped. Never consult worker prose
or worker-edited central files.

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

Routine names must exactly match packet order. The control-owned surgery layer is
the only writer of the four source files. Generator agents have no tools and no
access to files, URLs, credentials, Forgejo, VCS, or nested agents.

## Failure and completion

`status:"stop"` is fatal. `waiting` retries the same idempotent operation after
its `retry_at`. The run lease is released only after the completion predicate
proves remote `main`, publication revision, gate record, generated projections,
and Forgejo state converge. Completion is `PORT COMPLETE`; an ETA remains
unavailable until a validated productive route and the publication thresholds
are met.
