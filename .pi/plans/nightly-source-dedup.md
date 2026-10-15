# Goal
Stop progress-only commits from creating nightly releases, and remove the 16 duplicate nightly releases and tags explicitly approved by the user. Preserve four distinct source snapshots, all stable releases and Git history.

# Files in scope
- `tools/nightly_release.py`: new source-ref comparison CLI using the shared derived-path exclusions.
- `tests/test_nightly_release.py`: isolated real-Git regressions for source, derived-only, revert, deletion, mode and error cases.
- `.forgejo/workflows/ci.yml`: use the comparison before tagging, install Python in the nightly job and run the new regression module in quality.
- `docs/jj-workflow.md`: document source-only nightly decisions and stable-tag fallback.
- `tools/completion/revision.py`: reuse `DERIVED_PATHS` unchanged.
- `site/data/gate.json`, `site/data/history.jsonl`, `site/data/progress.json`: regenerate with the existing release gate and report tool after committing the final source.
- `/tmp/private-packages/nightly-prune-manifest.json`: exact approved keep/remove tags and commit identities for both hosts.

# Contracts
- CLI: `python3 tools/nightly_release.py FROM_REF TO_REF` prints exactly `changed` or `unchanged` for successful comparisons; Git errors fail nonzero.
- API: `source_changed(root: Path, previous: str, current: str) -> bool`; compare Git content and modes, excluding only shared `DERIVED_PATHS`.
- Latest nightly for the current VERSION is the baseline; use the matching stable version tag when that series has no nightly; an absent baseline permits the initial nightly.
- User selected keeping distinct source snapshots, authorizing deletion of exactly the 16 manifest entries on Forgejo and GitHub. Preserve every stable release and every keep entry.
- Canonical host is configured HTTPS Forgejo, owner fairfruit. Use `fj api` for API access; never extract credentials, mint tokens, alter Cloudflare or push to GitHub.
- Delete GitHub release objects only. Tag deletions originate on Forgejo and propagate through its configured push mirror.
- Source changes must retain valid source-bound completion evidence before publication; never hand-edit generated data.
- Builds and oracle verification stay serial with `POKETCG_NINJA_JOBS=-j1`, under a memory-limited scope.
- No authored comments or unrelated changes. Implementation slices skip build, lint, tests and formatters; the integration owner runs checks afterward.

# Pattern to copy
Reuse `DERIVED_PATHS` from `tools/completion/revision.py`, temporary Git fixtures from `tests/test_source_revision.py`, and the existing nightly tag/Release publication path.

# Non-goals
Do not change game behavior, alter stable releases, publish binary artifacts, rewrite Git history, add retries, or change which source files count beyond the existing derived exclusions.

# Acceptance
- [ ] Source comparison regressions pass :: python3 -m unittest tests.test_nightly_release
- [ ] A historical progress-only update is skipped :: test "$(python3 tools/nightly_release.py 3fb060ce155a7f1af4fcdc1494c6826b23172c0f 9fb8fb76a9ad541de8b14dc93d03abe7bbc13c2f)" = unchanged
- [ ] A historical source update is detected :: test "$(python3 tools/nightly_release.py 9fb8fb76a9ad541de8b14dc93d03abe7bbc13c2f 2de321c65dc080927d2f90e96d06f19a45d934bd)" = changed
- [ ] Published progress matches the current attestation :: python3 tools/progress/report.py check
- [ ] Repository green check passes :: POKETCG_BUILD=build-cmake-generic2 POKETCG_NINJA_JOBS=-j1 just build
