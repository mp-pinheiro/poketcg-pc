# Autonomous Port Factory

Forgejo issues and append-only factory comments are the source of truth. The
exact user message `start` launches a normal top-level OMP session through
`tools/factory/run.sh`; the script executes `omp --print start`. There is no
nested SDK session manager or factory watchdog.

## Control protocol

The top-level session must run `factory preflight` before `run-claim`. Preflight
must resolve concrete model IDs for `@smol` and `@task`, verify the current gate,
and reject a dirty central checkout. After `run-claim` succeeds, the extension
allows only `factory`, `task`, and `hub` until `run-release` or `complete`.

Each loop iteration:

1. Call `factory reconcile` with the winning run lease.
2. Call `factory frontier`; claim only the returned work IDs.
3. Pass `agent_name` and the resolved `model_id` to `factory claim`.
4. Dispatch one exact generator task with the issued packet and attempt ID.
5. Join that exact task job with `hub wait`; never accept unrelated async
   delivery. Heartbeat both run and work leases while a synchronous check runs.
6. Validate the returned `TranslationReplyV2` and call `factory check`. The
   control process applies the candidate in its disposable lane, runs the full
   verifier, and writes an immutable check receipt. A malformed reply stops
   before lane mutation.
7. Send a normalized `VerdictV2` and candidate hash to the same generator for a
   bounded repair round. `@smol` gets two rounds; `@task` gets three. A red
   final receipt is recorded once; a green receipt is recorded immediately.
8. Call `factory record` with only the receipt `check_id`. It re-hashes the
   receipt and lane and appends exactly one attempt result.
9. Integrate a green artifact immediately for the canary and first three pilot
   greens. Later integration uses at most four artifacts or fifteen minutes of
   age, whichever comes first.

A timeout, unrelated job result, attempt mismatch, lease loss, missing receipt,
corrupt receipt, or unverifiable integration phase is fatal. Only a work-claim
election conflict may be dropped. Never consult worker prose or worker-edited
central files.

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
