# docs/

There is no autonomous runbook. Every document here is a contract, the
architecture, or a technical diagnostic reference for hand-porting.

| doc | role |
|---|---|
| `port-contract.md` | Normative routine-port contract. |
| `factory-contract.md` | Normative `CONTRACT`/`CASES`/`MUTATIONS` case-module format. |
| `grind.md` | Diagnostic interpretations and repair recipes. |
| `coverage-program.md` | Coverage ledger, Target, Discover, and Intake diagnostics. |
| `tas-progress-loop.md` | TAS diagnostic reference. |
| `audio-harness.md` | Audio evidence mechanics. |
| `reach-harness.md` | Save, peer, link, IR, and printer reach mechanics. |
| `jj-workflow.md` | jj and Forgejo mechanics. |
| `vision.md` | Normative architecture and release destination. |
| `phase1-transform.md` | Hardware-transform record. |

Machine-readable state wins over prose: `site/data/coverage.json`,
`site/data/progress.json`, `site/data/gate.json`, `tools/progress/scope.toml`,
and `.factory/workflow.sqlite3`. Forgejo is an idempotent projection, not a
scheduler or evidence source.

The Forgejo issues are a projection of the loop's measured facts - session
divergences, sweep rows, composition audits - kept by `just issues-sync`
(`docs/grind.md`, "Issues"). The tracker does not contribute evidence.

The wave-era slice plan (`plan.md`) is deleted. Its per-slice history is in jj
history and `site/data/history.jsonl`; its conventions live in
`port-contract.md`; its exclusion table is `tools/progress/scope.toml`.
