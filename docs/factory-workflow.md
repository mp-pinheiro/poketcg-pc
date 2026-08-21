# Autonomous Port Factory

The factory keeps no external state. Work selection is deterministic tooling
over the repository itself — inventory, gate record, and `.factory/blocked.toml`
— and the oracle is the sole acceptance authority. The orchestrating session
owns every repository and jj write; candidate generators are stateless, run in
disposable lanes, and receive no credentials.

The exact user message `start` launches the loop below in a normal top-level
session. There is no run lease, no issue tracker authority, and no nested
session manager.

## The loop

1. `just factory-next 4` — select the next ready routines. Selection reads
   `work_records` (state `ready`, no operational blocker), so a name listed in
   `.factory/blocked.toml` is never selected. Routines whose artifacts already
   exist, and routines with a recorded `.factory/try/<Fn>/result.json`, are
   skipped; ordering prefers the routine that unblocks the most dependents,
   then the smallest. Each line prints the routine, its lane, and the exact
   verification command.
2. Dispatch `k=3` `port-candidate` agents per routine. Each agent reads
   `.factory/try/<Fn>/prompt.txt` and writes one TranslationReplyV2 JSON object
   to `.factory/try/<Fn>/candidate-<i>.json`. Candidates are dispatched by the
   session itself; there is no model client in the repository.
3. `just factory-try <Fn>` — or the printed command with the right `--lane` —
   verifies candidates in lane order with the real verifier. The first green
   candidate stages a verified artifact in `.factory/artifacts/`. There is no
   repair round: a routine red on all `k` candidates returns to the pool for a
   later wave with fresh candidates (`python3 tools/factory/try_one.py --next
   --retry-red` re-includes recorded reds).
4. `just factory-land` — land every eligible verified artifact. Per batch, the
   driver requires a clean tree synced with `main@origin`, applies the bundles,
   commits, runs `just oracle-release-gate`, asserts the gate names the source
   commit and is complete, refreshes the progress report, commits, pushes, and
   appends one record per artifact to `.factory/landings.jsonl`. A gate failure
   splits the batch; a lone failing artifact is quarantined to
   `.factory/quarantine.jsonl` with the gate tail.
5. `just factory-eta` — deterministic forecast computed from recorded landings
   only.

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

Routine names must exactly match packet order. The session-owned surgery layer
is the only writer of the four source files. Generator agents hold read-only
tools (`read`, `grep`, `glob`) to confirm generated-header macros exist; they
never write files, run VCS, hold credentials, or spawn agents.

## Failure and completion

A red candidate is a phase verdict, never a traceback; the routine simply
returns to the pool. A gate failure never leaves the tree dirty: the landing
driver abandons the batch commit and restores `main`. Progress is measured from
`site/data/gate.json` plus `site/data/progress.json`; the dashboard reads the
same files. There is no completion ceremony — the loop is done when
`factory-next` reports an empty pool.
