# Maintenance and diagnostics

This page owns issue triage, the session loop, diagnosis, safe verification lanes, and release publication procedure. For routine implementation rules see [the port contract](port-contract.md); for quartet generation see [the factory contract](factory-contract.md). Use [building](building.md) for installation and builds, and [jj workflow](jj-workflow.md) for ordinary version control.

## Issues: the worklist

Forgejo issues are generated facts, not a plan. `just issues-sync` projects current tracker reports by opening new facts and closing resolved ones. Do not edit fact bodies, hand-close issues, or widen the measurement exclusions to silence a fact. The only human-authored issue kind is `route`, representing content to record.

```sh
just issues-next
just issues-sync
just issues-status
just issues-route SESSION TITLE HOW
```

Fact priority is p0 divergence, route, p1 memory mismatch, p2 exit-register mismatch, then p3 composition audit. `issues-next` orders facts by priority, route play order, and observed frame. A fact closes only when its source report no longer contains it. Reports are in `build/completion/tracker/`; `session-verify` and `session-sweep` update them. Sweeping a new session imports that region's facts.

When there is no workable non-deferred issue, run `just coverage-next` and execute only its printed producer branch. `kind=done` means the measurable coverage worklist is exhausted; it does not mean all routines, release requirements, or publication are complete. `kind=gate` is an evidence-backed route or harness boundary, not completion. Producer no-ops do not stop the overall loop. Coverage producer details belong to [coverage program](coverage-program.md).

### Parallel sessions

`just issues-next --claim` claims the first issue for six hours; `just issues-claim N` renews it and `just issues-release N` releases it. Sync drops expired claims and takes a file lock to prevent duplicate facts. Each process needs its own `POKETCG_BUILD` and `POKETCG_SESSION`; reference caches are shared by input identity. There is one working copy: commit only paths you changed. Check available memory before adding concurrent processes; reference probes are memory-heavy and can take down the host under OOM.

## The session loop

A session is one input byte per DoFrame. The reference records a CRC-32 digest of masked game state at each DoFrame; the native lane replays the same input and reports the first differing ordinal. The reference stream is cached by its inputs and checkpointed, allowing targeted captures without replaying from boot. `confirmed` is the verified prefix in `tools/completion/session_ratchet.json`; it may rise but must never fall.

```sh
just session-verify NAME
just session-status
just session-sweep NAME
```

The session sweep captures routine entries from one reference replay and compares them against the port, with observations widened to reference-written bytes. It is a routine-fix worklist, not a replacement for a clean session. For a C fix, rerun the sweep over the affected window and verify affected sessions against a frozen lane before landing. A session's inputs are recorded or derived from the reference; do not invent or hand-edit them. AI-duel sessions exercise the ROM's AI through a controlled duel. Human recordings can reach screens not represented by existing inputs.

The digest compares WRAM, HRAM, OAM, and both VRAM banks under the scenario exclusion ledger. Audio-driver state and play-time counters are asynchronous to DoFrame and have their own [audio proof owner](audio-harness.md). Do not alter exclusions to move a ratchet.

### Session decision table

| Observation | Meaning and action |
|---|---|
| `status=diverged`, `DIVERGE ... writer=R` | Compare R's assembly, C, inputs, and reads. Run `just oracle-diff R`; add an observing fixture case and mutation as required by the port contract, then verify the session again. |
| Divergence writer has green cases | A case or completion cut may hide the body, or a callee may not run. Check `just hatch-status`, compare reference and native routine entries at the ordinal, then capture the actual failing path. |
| `WINDOW ... LAG` | The reference spent extra VBlanks between DoFrames. Determine whether the differing state is frame-timed; do not treat timing counters as ordinary routine output. |
| `DIVERGE ... writer=` empty | No reference write explains the native byte. Trace native routine entries around the ordinal and compare against the reference entries; investigate an invented write or call. |
| Same routines, different bytes | Capture both states at the failing and preceding ordinal, then compare the writer's assembly and inputs. |
| `status=native-short` | Read the `NATIVE` diagnostic and stderr. A missing-data address with sane inputs suggests pack coverage or bank selection; garbage inputs indicate an upstream divergence. |
| `status=ref-short` | A hand-recorded input outlasts the reference timeline; refresh its session metadata. A derived input should not have this mismatch. |
| `REGRESSION` | The change lowered a ratchet. Do not land it; identify and fix the regression. |
| `status=clean` | The session has no digest divergence. It is confirmed only when verification exits successfully and reports no `off_schedule` sync points; otherwise diagnose the failed check. If no facts remain, use `coverage-next` rather than inventing a new input or declaring completion. |
| `MUTATION_GREEN` | The chosen case did not observe the mutated behavior. Select a case that reads the changed value; do not accept a green mutation as proof. |
| Divergence confined to VRAM | Inspect the rendered map/tile inputs and writer logic. A memory-only case may not observe what was drawn. |

## Focused diagnostics

Use `just coverage-probe BASE --tail "LABELS" --mark ROUTINE` to test whether an input tail reaches unexecuted routines. This is a native-only diagnostic, not proof; record and verify a winning input. Probe labels are individual buttons and cannot express chords. For chord masks, use the [reach harness](reach-harness.md). A probe can also reach native-only routines the reference trace cannot name; do not count such a mark as ledger coverage or hand-label it unmeasurable.

Use `just call-window NAME ORDINAL` when both lanes enter a window but appear to perform work in a different order. It aligns bounded, anchored routine-entry traces; boundary-touching slices and names absent from one lane are not evidence by themselves. Audio interrupt placement belongs to [audio harness](audio-harness.md).

For data-address failures, distinguish bad inputs from a bad bank before changing bank handling. A missing-data address calculated from sane inputs suggests data-pack coverage or bank selection; an address derived from garbage points upstream. For an address with a known value but unknown writer, `POKETCG_WATCH=ADDR:VALUE[/SKIP]` can stop at the write; ordinary bus breakpoints may miss direct memory macros. Debugger findings must be checked against assembly and a reproducer.

Live lessons: a `wVBlankCounter` mismatch at a tiny ordinal can indicate a build changing under an unprotected verification run; rerun against a frozen binary before diagnosing it. A PyBoy routine probe that loops over frames does not model the ROM's halted CPU and ISR scheduling, so frame-driven behavior belongs to the session gate. A case can pass while missing an effect outside its observed spans; mutation proof must target the affected value. A routine's final registers can reflect stack-pointer-derived flags rather than its computation; do not model SP merely to match an incidental register.

## Verification lanes and publication

Keep builds private with a per-session `POKETCG_BUILD`. Build the trace lane with `just build-trace` only for trace-based diagnostics. Batch verification freezes the binary and data pack into its own lane; do not edit that lane during a run.

Run heavy work serially by default and increase jobs only against measured cgroup headroom. Do not hand-roll a verification loop in the shell.

### Acceptance after a C fix

1. Clear the reporting sweep window with `just session-sweep NAME --after K --until K`.
2. Verify affected sessions against a frozen lane with `just sessions-verify-affected ROUTINE --jobs 1`.
3. Before landing a batch, run `just sessions-sweep --jobs 1`. Shared AI, timing, and audio changes need the complete applicable set, including AI-duel sessions.
4. Sound-driver changes also need `just audio-tickdiff`. Session verification must exit successfully with no off-schedule synchronization points.

Singular `session-sweep` diagnoses routine entries in a reported window. Plural `sessions-sweep` verifies a batch; a single reproducer does not substitute for it.

### Source-bound release

Install the [verification tools](building.md#verification-tools) first when execution inputs change. Finish and commit those changes before measuring them. The attestation retains that measured revision; its validity follows the execution inputs rather than later documentation commits.

Use the canonical Vanilla paths because some completion producers use `build/` directly:

```sh
export POKETCG_PROFILE=vanilla POKETCG_BUILD=build POKETCG_PORTS='' POKETCG_NINJA_JOBS=-j1
just build
just completion-data-pack
python3 tools/completion/completion.py validate-requirements
just completion-chain
```

The chain refreshes stale records and their dependencies. Code, comparator, corpus, runtime, and semantic acceptance changes invalidate proof. Documentation source hashes and requirement anchors are validated separately. Check freshness before starting the full gate; never rebind hashes or bypass validators.

Require a clean tree, then generate and publish the attestation and dashboard:

```sh
just oracle-release-gate
python3 tools/progress/report.py build
python3 tools/progress/report.py check
jj commit site/data/gate.json site/data/history.jsonl site/data/progress.json -m "chore(progress): refresh release evidence"
jj git push --remote origin --bookmark main
```

Only the existing generators maintain gate, history, and progress data. Preserve their audit history and never publish an incomplete attestation. The [jj workflow](jj-workflow.md) owns ordinary VCS operations.

### Documentation-only publication

For `README.md`, `CHANGELOG.md`, or Markdown under `docs/`, commit the edits and run the snapshot check before pushing:

```sh
python3 tools/progress/report.py check
jj git push --remote origin --bookmark main
```

Editing `vision.md` also requires updating `manifest.source_sha256` and any moved requirement anchors in `tools/completion/requirements.toml`. These metadata changes preserve the executable contract. The snapshot check validates the current binding and recorded proof without requiring a ROM, build, or local evidence.

CI compares the complete push or pull-request range. Documentation-only changes run source-binding, changelog, and progress checks without ROM bootstrap or game tooling. Source, cases, configuration, agent instructions, and changed acceptance rules take the full check path. A matching local `oracle-release-gate` call can also reuse its original attestation; it additionally checks the current private runtime artifacts.


