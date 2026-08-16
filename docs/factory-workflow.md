# Factory workflow

The runbook for an orchestrator session. The exact message `start` triggers this
file and nothing else.

```
frontier -> packets -> [N lanes: translate -> surgery -> verify -> repair<=3]
        -> green bundles -> serial integrate (gate BEFORE push) -> reconcile -> repeat
```

Roles: **orchestrator** (this session) owns every repo, jj, and Forgejo write, and
is the only session that runs a central gate. **Lanes** are disposable directory
copies under `/tmp/poketcg-factory/lane-N` with no `.jj`, no `.git`, and no
credentials. **Translator** is a stateless `prompt -> tagged blocks` function;
production uses `completion(prompt, model="default")`.

## 1. Preflight

Run in order. Every step is a hard gate — do not proceed past a failure.

```sh
just forgejo-auth-check
jj git fetch --remote origin
just bootstrap
uv sync --project tools/oracle --frozen
just oracle-build-gbref
just build-barrier
just issues-fetch
just oracle-release-gate
just progress
python3 tools/factory/driver.py migrate-recovery-state --dry-run --json
python3 tools/factory/driver.py status
```

The migration dry-run must partition every managed work ID exactly once and
report zero duplicate claims. Apply it once, then rerun the dry-run; the second
run must report zero legacy packets and zero conversions. A failed barrier stops
the run and preserves the timestamped backup.

## 2. The loop

The exact `start` adapter supplies only the model completion seam. The
supervisor owns translation waves, recovery waves, verification, queue
transitions, candidate integration, gates, pushes, and Forgejo reconciliation:

```python
from supervisor import start

result = start(completion, lanes_count=10, verify_width=6)
```

`completion(prompt, model=...)` is called only on the orchestrator thread.
Recovery lanes remain credential-free and disposable. The returned result is
the supervisor action object; the adapter keeps invoking journaled actions until
the completion predicate or a typed stop-the-line condition is reached.

The supervisor invokes the existing lane/verifier machinery and only delegates
model text generation through `completion`. Its journal makes each action
replayable after a crash.

`429` and `5xx` provider failures persist a retry delay and keep the supervisor
alive. Authentication, authorization, remote divergence, unknown dirty files,
and corrupt or ambiguous identity are typed stop-the-line failures.

`packet.py build` returning `[]`, zero green bundles, blocked work, or no
progress is never successful termination. Literal `PORT COMPLETE` is emitted
only by the supervisor completion predicate after a current green gate and
both verified measures reach their totals.


A wave's cohort may exceed `lanes_count`: the first `lanes_count` packets are
admitted immediately, the rest stay `pending` on disk and are pulled into a lane
as soon as one frees up (`refill` events). `max_wall_s` is 3600 because a
refilled wave of 20 packets across 10 lanes runs roughly twice as long as the
old fixed cohort of 10 — it is a safety bound, not the expected duration.
`integrate.py` touches jj, git, and the gate; it must never run while a wave
holds `.factory/wave.lock` — only between waves, as above.

Bundles are composable (`surgery.extract`/`apply`, additive per-routine
fragments), so two packets of the same basename can run in one wave and both
land. A returned `deadline` or `stopped` wave is a clean partial return; the
outer loop stops instead of retrying an outage.

A lane runs the central comparator (`compare_one.py`) over every case in the
packet before the PyBoy lane, so `oracle-fn-all` cannot reject what a packet
already landed. `run_mutation` covers only the witness case.

`integrate.py` lands green bundles FIFO, then runs adapter lint, the constant
audit, `just oracle-release-gate`, and a progress rebuild before pushing. A red
gate stops the push.

Translation and verification run inside one continuous scheduler, not
alternating phases: a packet whose lane is free and whose translation parsed
is submitted for verification immediately, while the next translate batch is
forming from whichever other packets are ready. `python3 tools/factory/driver.py
progress` inspects a live wave (per-packet state, round, phase, time-in-phase)
without taking `.factory/wave.lock`.

## 3. Reconcile Forgejo

Forgejo issue labels and open/closed state are projections of factory truth.
The supervisor's live progress and claim index remain the dispatch authority;
reconciliation updates the dashboard and managed issue markers after each
successful integration.

```sh
just issues-fetch          # refresh the cache
just issues-sync           # dry run: what would change
just issues-sync-apply     # apply it
just issues-verify         # marker coverage
```

`issues-sync` refuses to run when a gate input (`src/`, `tests/`, `include/`,
`tools/oracle/`, `CMakeLists.txt`, `poketcg/`) changed after the last gate — a
stale gate would let it close an issue whose routine is no longer passing. Fix by
re-running `just oracle-release-gate && just progress`.

`--apply` is the only switch that writes to Forgejo. It self-verifies by
re-fetching and re-planning; a non-empty residual plan is an error.

## 4. Recovery and blockers

Failures are structured outcomes, not terminal queue states. `retry-ready`
returns to the recovery ladder with a new attempt generation; `blocked` carries
structured dependency or harness evidence and is revalidated every supervisor
iteration. `landed` and `superseded` are the only historical states.

The recovery ladder is ordinary retry, a fresh one-routine retry, a slow-model
retry, then disposable agentic recovery. Repeated agentic fingerprints invoke
`analyze_failure` and independent repair assignments. Provider failures use
persisted backoff; code, schema, bundle, dependency, and gate failures remain
actionable supervisor work.

Recovery lanes receive the exact quartet, failure history, owned paths, and
verifier command. They have no credentials or VCS metadata. Bundle acceptance
requires all marker blocks, importable cases, mutation receipts, identity, and
SHA-256 hashes before a packet can become `green`.

Dependency blockers are structured records in `.factory/blocked.toml`. Cleared
dependencies move packets to `retry-ready`. A dependency cycle is dispatched as
one SCC recovery group and integrates atomically; partial SCC integration is
forbidden. External blockers remain explicit stop-the-line records.

## 5. Invariants

- Lanes never run jj, git, or a central gate, and hold no credentials. Only the
  supervisor mutates packet state; callbacks return structured outcomes.
- `site/data/gate.json` has exactly one producer: `just oracle-fn-all`, via the
  release-gate chain. `just oracle-diff-all` deliberately writes no gate record.
- The integrator gates before every push; a red gate keeps packets non-landed.
- `integrate.py` aborts when `main@origin` diverges and never rebases
  automatically.
- A managed issue carries exactly one valid `port:v1:<source>:<symbol>` marker.
  Packet identity and claim dedup use that work ID, never mutable titles.
- One work ID cannot be claimed by two nonhistorical packets.
- Packet construction uses live progress and claims; Forgejo labels are only a
  projection.
- `tests/routines.py` is derived from `tests/cases/*.py` `CONTRACT` keys at
  import time. Never hand-edit it. `SCHEMA2_CASES` is generated by surgery.
- Every landed routine carries a live-oracle PASS and a mutation receipt.
- `.factory/blocked.toml` records structured blockers and is rebuilt with the
  trusted progress projection.

## 6. Calibration

Production config: `build(limit=20)`, `model="default"`, `max_rounds=3`,
`lanes_count=10`, `verify_width=6`, and `max_wall_s=3600`. A wave admits ten
packets immediately and refills from the rest as lanes free up; factory
subprocess work shares the wall-clock deadline. The synchronous harness
callback remains cooperative and may exceed that bound until its provider
request returns.

Translate and verify run in one continuous scheduler, not alternating phases: a
packet whose translation parsed is submitted for verification as soon as a lane
and a verify slot are free, and finished packets' lanes are refilled from the
queued remainder instead of idling until the wave ends.

**The provider is the only bottleneck that matters.** Wave `a4745708` (14
packets, completed) measured `translate 60% verify 2% salvage 0% lane 0%
idle 38%` of packet-time, with `/proc/loadavg` between 0.18 and 2.17 (median
0.46) on 8 CPUs. Verification is seconds; translation is minutes. Two
consequences:

- `verify_width` is not a throughput lever at these ratios. It defaults to
  `cpu_count() - 2` only to stop ten concurrent verifies oversubscribing 8
  cores (lane builds run `ninja -j2`; `compare_one.py`, `test_leaves.py`,
  `gbref_runner`, and PyBoy are each single-threaded). Raising it buys nothing
  while verify is 2% of the work.
- **Translate batch width is the lever.** Continuous dispatch initially issued a
  batch the instant any one packet was ready, fragmenting wave `a4745708` into
  widths `10,1,6,4,6,3,3,1,3,1,3` (mean 3.7) where even a width-1 call cost
  24-48 s — about 1183 s of that 1196 s wave was translation. `_decide`'s cheap
  verdicts are therefore drained before a batch is issued
  (`TRANSLATE_COALESCE_S`, 45 s cap so one slow verify cannot stall the batch),
  which restored widths `10,10` (mean 10.0) on the next wave.

`translate_many` runs only on the scheduler thread, blocking it; verify and
salvage jobs keep running in the pool throughout. A worker-thread probe
confirmed the harness completion bridge is not thread-safe outside its calling
thread (`RuntimeError: Missing session/run/name`), so translation cannot move
onto the pool without a session-context bridge that does not exist yet.

Phase timings come from `.factory/events.jsonl` (per-packet `verify-phase`
records written by the verify subprocess) and the per-packet `translate_s`,
`verify_s`, `salvage_s`, `lane_s`, and `idle_s` fields in `.factory/metrics.jsonl`;
`driver.py metrics` prints the split and `driver.py progress` reports a live
wave. Job durations are measured inside each job, not at harvest, because the
scheduler can block in `translate_many` long after a job finished. The phase
totals legitimately overlap — a lane rsync runs while the scheduler is blocked
translating — so `idle_s` is wall time minus the *union* of a packet's busy
intervals, never the wall-minus-sum that overlap drives negative.

Translate all ten prompts in one `parallel()` wave: measured 107-123 s per round
at width 10 against ~170 s as two batches of five, with no rate limiting, which
took a 3-round wave from 604 s to 377 s. A packet that returns a byte-identical
verdict two rounds running is not reading its feedback, so `_decide` salvages or
escalates it there instead of buying two more translations: measured 4 of 10
packets in one wave, and no packet that ever repeated verbatim went on to green.

Packet size dominates: a packet is green only when every routine in it is green,
so success decays as p^n. Measured 8 routines/packet → 0 green; 3/packet → 67%
green on `model="default"`. Escalating packets still land their passing routines
and spill failures into `<id>-rest`.

Early wave failures were packet-content gaps, not model weakness: missing RAM
symbol addresses, unparsed `const_def`/`DEF..EQU` constants, missing struct
typedefs for struct-returning callees, invented include paths, and ninja's
link-command echo crowding out the real compile cause.

## Notes

One-time, for a queue predating persisted work identity:
`python3 tools/factory/packet.py migrate-work-ids` (read-only), then
`--apply`. Require a zero-change dry run before dispatching.

Factory pushes target Forgejo `origin`. `github-mirror` is a checkout-local
remote, not a server-side mirror, so GitHub does not receive factory pushes.
`.github/workflows/release.yml` and `progress.yml` push to GitHub directly, which
is why `integrate.py`'s fast-forward check can see origin advance.
