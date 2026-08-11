# Autonomous port workflow

This runbook is the execution contract for an Oh My Pi session triggered by the
exact user message `start`. It ports the lowest-complexity actionable issues in
parallel, then integrates them one at a time. It is not the existing
`just launch-port` Copilot path.

## Invariants

- The orchestrator selects and claims distinct issues. Workers never select,
  claim, or steal issues.
- Workers use isolated workspaces, private build directories, and disjoint
  owned files. They never run a central gate.
- Only the orchestrator runs `just oracle-diff-all` and `just oracle-release-gate`.
- Every mutating jj command uses the command-local prefix below. Never mutate
  the caller's local `main` or use plain git writes.

```sh
jj --config 'experimental-advance-branches.enabled-branches=[]'
```

## Phase 1: preflight and deterministic selection

Before any GitHub or VCS write:

1. Read `skill://guarded-execution`, `AGENTS.md`, `docs/port-contract.md`,
   `docs/vision.md`, `docs/plan.md`, `docs/jj-workflow.md`,
   `.github/workflows/ci.yml`, `.github/workflows/release.yml`, and
   `.github/workflows/pages.yml`. Read the complete body of every candidate
   issue.
2. Read live repository state. Fetch remote metadata without allowing the
   repository's auto-advancing `main` to follow worker changes:

   ```sh
   jj --config 'experimental-advance-branches.enabled-branches=[]' git fetch
   ```

   Record the preflight local `main` and remote `main@origin` commit IDs. Base
   all workspaces on `main@origin`, never an unpublished local `main`.
3. Enumerate every open issue labeled `port` and every open PR. An issue is
   rejected when any of these predicates holds:
   - it is closed, lacks exactly one `tier-1` through `tier-4` label, or has an
     assignee;
   - an open PR body contains a closing reference for the issue;
   - its generated body is malformed;
   - one of its routines is already registered; or
   - it is no longer actionable according to
     `python3 tools/progress/report.py frontier --limit 0 --json`.
4. Validate each generated body against `tools/progress/gen_port_issues.py`:
   pinned Pret source and link, a non-empty unique routine table, four owned
   paths, the `ROUTINES["<basename>"]` partition, a validation block, and four
   acceptance checkboxes. Parse tier and total bytes from the generated title.
5. Build a selection manifest containing a run ID, snapshot timestamp, and one
   row for every candidate inspected through the fourth selection. Each row
   records issue, tier, bytes, number, and either `selected` or the exact
   rejection predicate and evidence. Sort eligible issues by numeric tier,
   total bytes, and issue number. Select four from the first tier with work;
   fill from the next tier only when that lower tier has fewer than four. If
   fewer than four eligible issues exist, launch only those issues. If none
   exist, report queue exhaustion and perform no writes.
6. Immediately before every claim, refresh its manifest row. Re-read issue
   state, assignees, comments, and open-PR links. Abort that candidate if the
   snapshot changed. Assign it to the authenticated user and add a claim
   comment containing the literal marker `<!-- omp-port-claim -->`, run ID,
   worker name, issue number, intended bookmark `port-issue-<N>`, and timestamp.
   Re-read and accept the claim only while the issue is open, the assignee is
   present, no competing active claim or open PR appeared, and the marker is
   this run's marker. On conflict, remove only this run's assignment/comment
   when safe; never steal another user's assignment.

### Auditable manifest

Keep the manifest in the session output. It must be sufficient to reproduce
why each inspected candidate was selected or rejected. Runtime selection must
recompute live state; a prior manifest never authorizes a later claim.

## Phase 2: isolated worker setup

For each claimed issue, create the bookmark and workspace with these exact
commands, replacing `<N>`, `<run-id>`, and the absolute path:

```sh
jj --config 'experimental-advance-branches.enabled-branches=[]' bookmark create port-issue-<N> -r main@origin
jj --config 'experimental-advance-branches.enabled-branches=[]' workspace add --name port-issue-<N> -r main@origin /tmp/poketcg-port-<run-id>-<N>
```

After each operation, use read-only `jj bookmark list` and `jj log` to verify:

- local `main` still equals the preflight local commit;
- `port-issue-<N>` equals `main@origin`; and
- the workspace `@` has exactly `main@origin` as parent.

Abort setup on any mismatch. Do not use `just launch-port`; it has a
list-then-assign race and does not create isolated Oh My Pi workers.

Give each worker an immutable manifest containing issue number, tier, basename,
routine list, Pret path and pin, issue URL, workspace path, bookmark, and:

```sh
export POKETCG_BUILD=build-issue-<N>
export POKETCG_PORTS="<basename>"
```

Use a semicolon-separated `POKETCG_PORTS` only when the issue explicitly owns
multiple Pret basenames. Ownership is limited to
`src/home/<basename>.c`, `src/home/<basename>.h`,
`src/probe/<basename>.c`, `tests/cases/<basename>.py`, only that basename's
`ROUTINES` tuple, its mutation receipts, and generated
`site/data/progress.json`/`site/data/history.jsonl` changes produced by
`just progress`. No worker edits shared infrastructure or another manifest.

## Phase 3: parallel implementation

Launch one `task` batch, exactly one general worker per claimed issue, normally
named `PortIssue<N>`. Wait for every initial result and retain each live agent
ID. Do not poll settled jobs or replace a successful worker identity. Re-dispatch
only a failed ownership set, with the concrete failure.

Use this batch context:

```text
# Goal
Complete the claimed issues end to end.
# Constraints
Use only the assigned workspace and ownership manifest. Prefix every mutating
jj command with jj --config 'experimental-advance-branches.enabled-branches=[]'.
Phase 1 is exploration and implementation only: no build, test, lint, format,
commit, push, PR, or merge commands. Workers never run just oracle-diff-all or
just oracle-release-gate. The orchestrator owns central gates and merge order.
# Contract
Each worker receives the complete JSON manifest for every worker: issue, tier,
basename, routines, Pret path/pin, issue URL, workspace, bookmark, build
folder, POKETCG_PORTS, and owned paths.
```

Use this task template for each worker:

```text
# Target
Issue #<N>; workspace <absolute-path>; owned paths and ROUTINES partition from
this worker's manifest.
# Change
Read the required docs and complete issue. Derive the ASM ABI, callers,
fallthrough, and dependencies. Inspect neighboring C ports, adapters, and
schema-2 cases. Implement every routine, literal one-call adapter, schema-2
zero/poison/boundary/input case, mutation declaration, and only this registry
partition.
# Acceptance
Return derived ABI, case, and mutation evidence plus changed paths. No build,
test, lint, format, commit, push, PR, or merge command has run. No unresolved
stub, TODO, alias, dead path, or unsupported exclusion remains.
```

Each worker must read the normative docs and full issue; inspect exact ASM
routine bodies, all callers, fallthrough/dependencies, neighboring ports,
adapters, and schema-2 cases; derive the ABI from ASM before touching the
adapter; and leave no changes outside its manifest. Initial assignments perform
no validation because concurrent Task work must not validate mid-flight.

## Phase 4: private proof and publication

After every implementation worker is idle, send the same agents fire-and-forget
Phase 2 messages through `hub send`, then wait for one terminal reply from each
agent. The message must be copy-ready and begin exactly with:

```text
VALIDATE_AND_PUBLISH issue=<N> workspace=<path>

Use this worker's private environment:
POKETCG_BUILD=build-issue-<N>
POKETCG_PORTS="<basename>"
Bookmark: port-issue-<N>
Every mutating jj command must start with:
jj --config 'experimental-advance-branches.enabled-branches=[]'
Never run just oracle-diff-all or just oracle-release-gate.

Proof and publication loop:
1. Bootstrap only if the pinned Pret checkout is absent and build this private slice.
2. Run just oracle-diff <PretSymbol> for every routine; require literal PASS.
3. For every routine, choose its declared witness case, run
   just oracle-fn <PretSymbol> tests/cases/<basename>.py <index>, then
   python3 tools/run_mutation.py <PretSymbol> tests/cases/<basename>.py --index <index>.
   Require MUTATION_RED, retain the routine receipt, and rerun the unchanged
   witness plus live just oracle-diff with PASS.
4. Run python3 tools/audit_mutations.py --stage release, python3
   tools/lint_adapters.py, and just progress; inspect generated progress files.
5. Fix failures at source and repeat the complete per-issue proof set.
6. Review the diff against the ownership manifest.
7. Commit, set the named bookmark to @-, and push that bookmark using the safe
   jj prefix. Never rewrite a pushed commit or create a duplicate PR.
8. Open one non-draft PR titled feat(port): <basename>, with every routine PASS,
   mutation RED/restored PASS, audit, adapter lint, progress, and standalone
   Fixes #<N> evidence.
9. Capture headRefOid, run `gh pr checks <PR> --watch --fail-fast`, query
   `gh pr checks <PR> --json name,bucket,state,link` and capture headRefOid
   again. Restart if the SHA changed. Require the single `quality` check with
   bucket `pass`.

Return exactly one terminal status:
READY_FOR_MERGE issue=<N> workspace=<path> routines=<list> commit=<SHA>
bookmark=port-issue-<N> pr=<URL-or-number> changed_paths=<list>
receipts=<list> ci_links=<list>
or:
BLOCKED issue=<N> failed=<command-or-API> evidence=<full-evidence>
preserved_state=<PR-and-bookmark-state>

Do not merge. A merge request is valid only when it is:
MERGE_APPROVED issue=<N> pr=<PR> head=<SHA>
and its SHA equals live headRefOid.
```

Send that text with `hub send` to the original worker identity. Wait for one
terminal reply from each; do not spawn replacements for successful workers.
The worker loops until all proof and publication conditions pass:

1. In its workspace, export the private `POKETCG_BUILD` and `POKETCG_PORTS`.
   Bootstrap only if the pinned Pret checkout is absent, then build the private
   slice.
2. Run `just oracle-diff <PretSymbol>` for every routine and require literal
   `PASS`.
3. For every routine, select a declared witness case. Run
   `just oracle-fn <PretSymbol> tests/cases/<basename>.py <index>` to create the
   workspace's `build-barrier` baseline, then run
   `python3 tools/run_mutation.py <PretSymbol> tests/cases/<basename>.py
   --index <index>`. Require `MUTATION_RED` and retain
   `tools/oracle/mutation_receipts/<PretSymbol>.json`. Rerun the unchanged
   witness and live `just oracle-diff` and require `PASS` for both. The mutation
   helper uses a workspace-local `build-barrier` and temporary full build with
   empty `PORT_FILES`; workspace isolation, not `POKETCG_BUILD`, prevents races.
4. Run `python3 tools/audit_mutations.py --stage release`,
   `python3 tools/lint_adapters.py`, and `just progress`. Inspect generated
   progress changes.
5. Correct failures at their source and repeat the affected proof plus the full
   per-issue proof set.
6. Review the diff against the ownership manifest.
7. Commit and publish only with this sequence, verifying after each command
   that local `main` did not move and the named bookmark/head is correct:

   ```sh
   jj --config 'experimental-advance-branches.enabled-branches=[]' commit -m 'feat(port): <basename>'
   jj --config 'experimental-advance-branches.enabled-branches=[]' bookmark set port-issue-<N> -r @-
   jj --config 'experimental-advance-branches.enabled-branches=[]' git push --bookmark port-issue-<N>
   ```

8. Open one non-draft PR to `main`, titled `feat(port): <basename>`. Its
   verification checklist lists every routine PASS, every mutation RED and
   restored PASS, mutation audit, adapter lint, and progress result, followed
   by standalone `Fixes #<N>`.
9. Capture `headRefOid` with `gh pr view`; run `gh pr checks <PR> --watch
   --fail-fast`; query `gh pr checks <PR> --json name,bucket,state,link`; and
   capture `headRefOid` again. Restart the watch if the SHA changed. Require
   the single `quality` check with bucket `pass`; missing, pending, skipped,
   cancelled, and failed checks block the PR.
10. Fix CI, scope, body, or evidence gaps with additive Conventional Commits,
    advance and push the same bookmark using the safe prefix, and restart the
    complete current-head watch. Never rewrite a pushed commit or create a
    duplicate PR.
11. Return exactly one terminal status. `READY_FOR_MERGE` includes issue,
    workspace, routines, commit/head SHA, bookmark, PR URL/number, changed
    paths, command outputs, receipts, and CI links. `BLOCKED` includes the
    failed command/API, full evidence, and preserved PR/bookmark state. Workers
    never merge before receiving the orchestrator token.

The distinct merge token must be exactly shaped as:

```text
MERGE_APPROVED issue=<N> pr=<PR> head=<SHA>
```

Reject a token missing any value or whose SHA differs from live `headRefOid`.

## Phase 5: serialized central gate and merge

Process ready PRs one at a time in original selection order. This is the only
serialized part of the four-worker workflow.

### Stabilize automation

Before each merge, capture current `main` SHA as the integration target. Require
terminal success for the `quality` check from `ci` on that exact SHA. Then
require successful `release` and `pages` workflow-run events whose triggering
`ci` run has the same exact head SHA. Normal merge stabilization accepts only
these event/SHA pairs; manual runs, missing, pending, skipped, cancelled, or
failed checks do not satisfy the barrier.

Re-read `main` after the automation settles. The release workflow may append
one generated `chore(release): vX.Y.Z` commit containing only `VERSION` and
`CHANGELOG.md`. Verify its tag and GitHub Release, then adopt that generated
commit as the next integration base without demanding a second full CI/Pages
cycle. If `main` advanced with any other commit, discard the cycle and restart
from the new target SHA. Never inspect unrelated historical runs.

### Resynchronize a stale PR

If the next PR is behind current `main`, wake its original worker. In its
workspace run the safe-jj fetch, then:

```sh
jj --config 'experimental-advance-branches.enabled-branches=[]' new port-issue-<N> main@origin
```

Before editing, require `jj log -r 'parents(@)'` to show exactly the prior
`port-issue-<N>` head first and current `main@origin` second. Resolve only
registry/progress conflicts by preserving their union. Rerun every per-issue
oracle, mutation, audit, and progress proof; commit with subject
`chore(port): sync issue <N>`, set the same bookmark to `@-`, push it, and
require `jj log -r 'parents(@-)'` to retain those two parents. Drive all four PR
checks green again. Abort rather than guess on parent order/count, bookmark, or
local `main` mismatch.

### Approve and merge

Re-read the PR and abort on draft/closed state, wrong base/head, changed head
SHA, conflicts, unresolved requested changes, unexpected paths, missing
`Fixes #<N>`, or any absent/pending/skipped/cancelled/failed CI job.

In the worker workspace at the exact PR head, the orchestrator alone runs:

```sh
just oracle-release-gate
```

On red, send the full evidence to the owning worker, require source fixes and
all targeted proofs/CI again, then rerun the barrier. Add the approved SHA and
central-gate PASS to the PR checklist before the final PR re-read.

Send the original worker the exact merge token, after which it re-runs guarded
execution preconditions and executes:

```sh
gh pr merge <PR> --squash --delete-branch --match-head-commit <SHA>
```

Never use `--admin`. If branch rules require a merge queue or prohibit squash,
use the required non-admin queue method while retaining exact-head protection.

Verify the PR is `MERGED`, its squash commit is reachable from the default
branch, and issue `<N>` closed automatically through `Fixes #<N>`. Failure to
auto-close after the default-branch state is visible is a hard blocker: never
manually close the issue or merge the next PR.

After automatic closure, edit the issue body itself: preserve generated content,
change all four Acceptance lines to `[x]`, replace the stale final `git commit`
command with truthful `jj commit -m "feat(port): <basename>"`, and add an
evidence comment containing PR URL, approved SHA, all routine PASS results,
every mutation RED/restored PASS, `just progress`, and
`just oracle-release-gate`. Re-read the closed issue and require all four boxes
checked. Retry API/edit failures; do not advance while the definition of done is
stale.

Run the post-merge automation cycle again. If a required run fails because of
the port, reopen the issue and return the same worker for a follow-up PR. If it
is a confirmed unrelated infrastructure/baseline failure, pause the remaining
queue with the exact blocker and never falsify evidence.

After the final selected merge, stabilize `main`, run
`just oracle-release-gate` once more there, and verify every selected PR is
merged and every selected issue is auto-closed with checked Acceptance lists.
Report the actual selected count plus issue, PR, commit, Actions, and final
gate URLs/output. If the queue was exhausted before four claims, report the
reduced count; if no issue was eligible, report queue exhaustion and no writes.

## Operational contingencies

- A claim by the authenticated user is reclaimable only after 24 hours with no
  open PR and no newer activity. The new run must post an explicit takeover
  comment before reuse.
- Re-check authenticated permissions, repository merge settings, branch rules,
  push/issue/PR permissions, and observable current-head checks before acting.
  Any 401/403, unknown head, or unobservable branch rule pauses the affected
  worker without weakening a gate.
- Squash is fixed for this workflow. If live branch rules require a merge queue
  or prohibit squash, use its required non-admin method with
  `--match-head-commit`; keep every other barrier unchanged.
- Generated issues contain a stale `git commit` checkbox. Replace it with
  `jj commit` before checking it and never run the prohibited git command.
- A worker may use only a contract-supported exclusion with exact source
  evidence. If a listed routine cannot meet Acceptance, leave the PR unmerged
  and issue open/assigned; do not check boxes, reduce the routine list, or
  substitute another issue after implementation begins.

## Installation verification

Do not execute a real `start` while installing this workflow; it claims, pushes,
and merges production issues. Verify the installation read-only:

1. Read `AGENTS.md` and confirm one exact-match `start` trigger points to this
   runbook, states orchestrator issue selection/claims, and forbids worker
   central gates. Confirm `/start`, arguments, and containing prose do not match.
2. Instantiate a timestamped read-only selection manifest from one live queue
   snapshot. Record every candidate inspected through the fourth selection with
   parsed tier/bytes/number and rejection evidence. Verify deterministic sorting,
   then discard the manifest without claims. Runtime selection must refresh each
   row immediately before claiming.
3. Verify the task batch has exactly one `PortIssue<N>` per eligible issue,
   distinct workspaces/bookmarks/build directories/registry partitions, and
   initial assignments explicitly skip validation. Verify Phase 4 wakes those
   same workers with the `VALIDATE_AND_PUBLISH` contract.
4. Verify each Acceptance checkbox maps to observed routine PASS, mutation
   RED/restored PASS, progress, and a real jj Conventional Commit. The workflow
   edits the issue body, not only the PR checklist.
5. Verify the merge barrier requires the `quality` CI check plus successful
   release and Pages workflow-run events on the approved source head, central
   release-gate PASS, exact-head squash merge, automatic issue closure, and
   green post-merge Actions before the next PR.
6. Do not alter `just launch-port` or `.github/copilot-instructions.md`.
