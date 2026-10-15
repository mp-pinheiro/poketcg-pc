# Coverage program

The coverage ledger measures reference-executed routines and dispatches current work among Reach diagnostics, Discover, Intake, and Target. Issue triage and fixing belong to [grind](grind.md); seeded saves and peer transport belong to the [reach harness](reach-harness.md), and audio evidence belongs to the [audio harness](audio-harness.md).


## Ledger identity and accounting

`just coverage-ledger` generates `site/data/coverage.json`; `tools/completion/coverage_ratchet.json` pins the executed total and may only rise. `just coverage-status` ranks files by routines not executed and reports unmeasurable inventory separately.

The ledger uses reference-side routine-entry traces through each session's confirmed ordinal, not native call counts. A clean prefix means the native lane has matched that reference prefix. Cache entries in `build/completion/coverage/` are keyed by the session stream key and confirmed ordinal. A changed confirmed prefix requires re-tracing that session; a native C change alone does not change the reference trace. Never force a cache refresh merely because C changed.

Measured executed coverage and unmeasurable accounting are distinct. Unmeasurable names lack an attributable reference entry in the tracer's address table; the ledger derives and reports these separately and holds them out of the executable worklist. Closing a registration gap requires correcting registration or the reference-side name mapping, not inventing a session. A native probe can likewise reach a routine absent from the reference entry table; that is a diagnostic signal, not measured coverage.

## Deterministic dispatch

```sh
just coverage-next
just coverage-discover [SEED...]
just coverage-intake SEED [--top K] [--land]
just coverage-target [ROUTINE|STEM...] [--limit N] [--land]
just effects map
just effects carriers ROUTINE
```

`coverage-next` selects one producer branch from the current ledger state, or reports `kind=done` or `kind=gate`. Execute only its selected branch. Done means the measurable worklist is exhausted; it does not mean every inventory routine has a measurable entry, every release requirement is satisfied, or publication is complete. Gate means measurable routines remain but producers have no unconsumed work for the current executed-set digest; report the decision boundary, never completion. A producer no-op is not a program stop condition.

Discover searches ledger-ranked sessions or supplied seeds for input scripts reaching routines not already in the known set. It distinguishes the `producer_key` for a seed's search inputs from the `scored_ledger_digest` used to rank newly found routines; the corpus is reused only while its producer inputs remain identical, and scoring is interpreted against the current ledger. Intake greedily selects scripts from one seed's corpus that add measured coverage, records them as sessions, and verifies them; seeds must be clean. A diverged session is not a useful Discover seed.

Target maps unexecuted card-effect routines to carriers, then arranges a controlled AI duel and watches for the target routines. If none fire, it records a player-controlled seed for Discover. A null reached result is a consumed Target outcome at that ledger state: do not retry arbitrary seeds or rewrite the canonical session. Target and Discover results become ordinary recorded sessions; session verification and issue synchronization follow [grind](grind.md).

## Reach diagnostics and boundaries

`just coverage-probe BASE --tail "LABELS" --mark ROUTINE` is a fast native-only reach check, not evidence. Probe labels are single-button actions, so chord-only menus require a mask timeline as documented by the [reach harness](reach-harness.md). Always record and verify a winning input.

Reach probes may report native executions for which the reference tracer has no entry address. These are not ledger credit and must not be manually marked unmeasurable. Likewise, a target carrier that does not execute its effect is a Discover seed rather than a successful target. Input generation does not replace save-seeded or peer-transport scenarios, which have their own owners.

After landing new coverage, refresh the ledger and synchronize tracker facts:

```sh
just coverage-ledger --jobs 1
just issues-sync
```

The ledger's per-session trace cache is separate from completion evidence caches. Changes to declared test or specification inputs can invalidate cached evidence and dependent rows; follow [grind's canonical completion refresh and publication procedure](grind.md#verification-lanes-and-publication). Never rebind stale hashes, bypass validators, or edit generated coverage/dashboard/history outputs by hand.
