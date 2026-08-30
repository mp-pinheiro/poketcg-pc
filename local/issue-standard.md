# Engineering issue standard

This is the single standard for completion work. It is intentionally independent of any prior tracker state.

## Identity and granularity

Every issue represents one independently closable outcome. Stable IDs use:

```text
completion:v1:p<3|4|5|6|7|8|x>:<area>:<kebab-slug>
```

Routine-backed issues list their `port:v1:<source>:<symbol>` work IDs. Group routines only when they share one root mechanism, implementation boundary, acceptance contract, and close evidence. A true dependency cycle is one dependency-group issue, not mutually blocking issues.

## Title

```text
<type>(<scope>): <imperative outcome>
```

Titles are 50 characters or fewer, imperative, without phase, priority, status, issue number, emoji, or trailing punctuation. Allowed types: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`. Controlled scopes: `runtime`, `ppu`, `audio`, `text`, `tiles`, `menus`, `duel`, `effects`, `ai`, `overworld`, `scripts`, `maps`, `link`, `ir`, `printer`, `widescreen`, `data`, `oracle`, `factory`, `progress`, `build`, `docs`, `release`.

## Tags

Every issue has exactly one tag from each required dimension:

- Phase: `phase-3`, `phase-4`, `phase-5`, `phase-6`, `phase-7`, `phase-8`, or `phase-crosscut`.
- Kind: `kind-port`, `kind-bug`, `kind-feature`, `kind-infra`, `kind-validation`, `kind-docs`, or `kind-epic`.
- Area: `area-factory`, `area-oracle`, `area-progress`, `area-runtime`, `area-data`, `area-ppu`, `area-audio`, `area-save`, `area-gameplay`, `area-link`, `area-printer`, or `area-release`.
- Priority: `priority-p0`, `priority-p1`, `priority-p2`, or `priority-p3`.

Optional `risk-security` is only for untrusted save or peer/protocol input. Lifecycle and status tags are prohibited. Priority is P0 for false-green proof, data loss, security exposure, or an all-work blocker; P1 for a current phase/frontier blocker without a safe workaround; P2 for required completion work outside the current critical path; P3 for additive polish.

## Required body

Every body uses these headings and contains final text, never placeholders:

```markdown
## Outcome

## Classification
- ID: `completion:v1:...`
- Source findings: `FG-...`
- Phase / kind / area / priority: ...
- Work IDs: ... | `none`

## Problem and contract

## Repository evidence
### Observed facts
### Inference

## Scope
### In scope
### Out of scope

## Constraints

## Relationships
- Parent: `completion:v1:...` | `none`
- Blocked by: direct stable IDs only | `none`
- Related: non-blocking stable IDs only | `none`

## Acceptance criteria
- [ ] AC-1: observable result

## Verification and close evidence
| AC | Scenario or command | Required signal/artifact |
|---|---|---|
```

Evidence names exact repository paths, symbols, and revision-keyed artifacts. Observed facts and inference are separate. Compilation or an implementation claim is never sufficient acceptance. Each AC has exactly one verification row. Close evidence names the landed revision and required gate/runtime/mutation/scene artifact.

## Relationships

Use stable IDs in body text, not tracker-specific numbers:

- one optional `Parent`;
- direct causal blockers only under `Blocked by`;
- non-blocking context under `Related`;
- reverse `Blocks` is derived, never stored;
- parent membership does not imply a blocking edge;
- the dependency graph must be acyclic;
- an epic aggregates children and has no implementation finding of its own.

## Manifest contract

`docs/full-game-findings.json` is the source for publication. Each issue object has `id`, `source_finding_ids`, `title`, `type`, `scope`, `phase`, `kind`, `area`, `priority`, `flags`, `parent_id`, `blocked_by_ids`, `related_ids`, `work_ids`, `evidence_refs`, `acceptance`, `verification`, `scope_boundaries`, `fully_rendered_body`, `body_sha256`, `remote_number`, and `remote_url`.

`tools/validate_issue_manifest.py` rejects duplicate or unresolved IDs, duplicate finding ownership, title or tag violations, parent/dependency cycles, missing evidence, missing headings, placeholders, unpaired acceptance criteria, unresolved work IDs, remote-number collisions, and body-hash mismatches. Every actionable assessment finding has exactly one primary issue. Non-actionable observations remain in the evidence register with a reason; they are not silently dropped and are never represented as remote duplicate claims.

## Publication

Create labels from this file before issues. Create issues only from the validated manifest, in topological order. Record each returned number and URL immediately. Read back only those newly created numbers and require exact title, body hash, labels, open state, and stable relationship text. A failed create or label application stops publication; successful issues are not deleted. Existing tracker issues, labels, milestones, and duplicate searches are outside this standard.
