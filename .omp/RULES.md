# Exact `start` session rule

When, and only when, the user's trimmed message is exactly `start`, treat it as
the port-factory trigger. This is not a normal porting request.

Immediately read `docs/factory-workflow.md` and execute the loop it defines. Do
not create a routine-port todo list, dispatch a scout to choose work, or
hand-port a routine: work selection is deterministic — `just factory-next`
selects from the ready frontier and respects `.factory/blocked.toml`. Keep
running the loop until `factory-next` reports an empty pool or a gate failure
needs escalation.

The orchestrator session owns every repository and jj write, and is the only
session that runs a central gate (`just oracle-release-gate`). Candidate lanes
are stateless, disposable, and receive no credentials.

Messages such as `/start`, `Start`, `start <issue>`, or prose containing `start`
are ordinary requests and do not activate this rule.
