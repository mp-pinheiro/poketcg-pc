# docs/

Nine documents, each with one job. Nothing here is a task list — work is selected
deterministically by the factory from open Forgejo work issues.

| doc | role |
|---|---|
| `port-contract.md` | **Normative.** The porting contract: memory model, the three C rules, adapter rules, required case coverage, mutation testing, exclusion taxonomy. Read in full before writing any C. |
| `factory-contract.md` | **Normative.** The exact `CONTRACT` / `CASES` / `MUTATIONS` blocks a translator lane must emit. |
| `grind.md` | The porting runbook: the loop, the decision table, one row per failure class. Every branch is a lookup; a branch that needs a design decision is a stop condition. |
| `factory-workflow.md` | The orchestrator runbook: preflight, the loop, reconciliation, escalation, invariants. The `start` trigger reads this and nothing else. |
| `jj-workflow.md` | VCS workflow and Forgejo authentication (Cloudflare Access + PAT helper). |
| `tas-progress-loop.md` | Reference for one tool, `just completion-tas-progress`: replaying the completion TAS on both lanes. Not the runbook; `grind.md` is. |
| `integration-plan.md` | The program for closing the 26 `completion:v2` requirements and `vision.md` phases 3-8. Its ranked root causes are dated; the state block names which are closed. |
| `vision.md` | Descriptive: architecture, phase order, prior-art rationale. Not normative. |
| `phase1-transform.md` | Per-routine delete/dissolve/port verdicts for the hardware-removal transform. |

Machine-readable state lives outside `docs/` and always wins over prose:
`site/data/gate.json` (last central gate), `site/data/progress.json` (work
records), `tools/progress/scope.toml` (exclusions), and the Forgejo issue
ledger itself. `.factory/` holds only rebuildable caches: the issue snapshot,
verified artifacts, and issued prompts.

The Forgejo issues are a projection of the loop's measured facts - session
divergences, sweep rows, composition audits - kept by `just issues-sync`
(`docs/grind.md`, "Issues"). The tracker does not contribute evidence.

The wave-era slice plan (`plan.md`) is deleted. Its per-slice history is in jj
history and `site/data/history.jsonl`; its conventions live in
`port-contract.md`; its exclusion table is `tools/progress/scope.toml`.
