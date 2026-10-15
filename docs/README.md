# Documentation

Choose the task, then use its owning guide. Commands are implemented in `justfile` and `tools`; current verification state comes from tracked evidence rather than repeated status claims in prose.

## Play and build

| Task | Guide |
|---|---|
| Controls, profiles, save locations, and diary import | [Playing](playing.md) |
| Dependencies, source builds, local packages, and oracle installation | [Build and package](building.md) |

## Change and verify

| Task | Guide |
|---|---|
| Reproduce a defect, diagnose a session, refresh evidence, and publish | [Maintenance and diagnostics](grind.md) |
| Commit, fetch, review, push, and understand release/mirror ownership | [jj workflow](jj-workflow.md) |
| Add or maintain a game profile and its isolated evidence | [Porting a profile](porting-a-profile.md) |

## Contracts

| Authority | Document |
|---|---|
| Current architecture and the machine-bound completion claims | [Architecture and acceptance](vision.md) |
| Routine translation, memory, ABI, observations, and mutation proof | [Port contract](port-contract.md) |
| Quartet, factory output markers, and derived case inventories | [Factory translation contract](factory-contract.md) |
| Bounded hardware-disposition audit | [Phase 1 transform](phase1-transform.md) |

## Specialist references

| Mechanism | Reference |
|---|---|
| Coverage ledger, Discover, Intake, and Target | [Coverage program](coverage-program.md) |
| Driver ticks, game requests, scheduling, and PCM proof | [Audio proof](audio-harness.md) |
| Seeded saves, peer transport, and linked reference evidence | [Seeded state and peer reach](reach-harness.md) |
| TAS metrics and composition diagnostics | [TAS diagnostic reference](tas-progress-loop.md) |

## Sources of truth

- [`requirements.toml`](../tools/completion/requirements.toml) declares the executable completion contract and checks its documentation binding to `vision.md`.
- [`gate.json`](../site/data/gate.json) records the measured source and reusable execution identity; [`progress.json`](../site/data/progress.json) is its generated dashboard projection.
- [`scope.toml`](../tools/progress/scope.toml) owns exclusions. Coverage and session ledgers own measured execution and confirmed prefixes.
- Forgejo issues project measured worklist facts. Tracker state does not establish correctness.

