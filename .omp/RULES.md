# Exact `start` session rule

When, and only when, the user's trimmed message is exactly `start`, treat it as the autonomous port workflow trigger. This is not a normal porting request.

Before selecting, reading, or claiming an issue, immediately read and execute `docs/autonomous-port-workflow.md`. Do not create a routine-port todo list, dispatch a scout to choose an issue, implement a routine, or stop after issue selection. The run must continue through issue claims, isolated worker dispatch, worker validation/publication, terminal `READY_FOR_MERGE` or `BLOCKED` replies, serialized central gates, and merge/issue verification as specified by the runbook.

The orchestrator selects and claims distinct issues. Workers never select or claim issues. Only the orchestrator runs `just oracle-diff-all` and `just oracle-release-gate`.

Messages such as `/start`, `Start`, `start <issue>`, or prose containing `start` are ordinary requests and do not activate this rule.
