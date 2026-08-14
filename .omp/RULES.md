# Exact `start` session rule

When, and only when, the user's trimmed message is exactly `start`, treat it as
the port-factory trigger. This is not a normal porting request.

Immediately read `docs/factory-workflow.md` and execute the loop it defines. Do
not create a routine-port todo list, dispatch a scout to choose work, or
hand-port a routine: work selection is deterministic — `tools/factory/packet.py
build` consumes open `port-ready` Forgejo issues and emits packets. Keep running
the loop until the frontier is empty or a STOP-THE-LINE gate fires.

The orchestrator session owns every repository, jj, and Forgejo write, and is
the only session that runs a central gate (`just oracle-release-gate`).
Translator lanes are stateless, disposable, and receive no credentials.

Messages such as `/start`, `Start`, `start <issue>`, or prose containing `start`
are ordinary requests and do not activate this rule.
