# jj workflow

This repository uses colocated jj and Git. jj owns ordinary repository mutations; the Git working-copy branch is intentionally detached. Read-only Git commands and the release recipe's tag operations are exceptions. Use `jj git` for normal remote operations.

## Remotes and topology

`origin` is the canonical Forgejo repository, `https://forgejo.yfrit.com/fairfruit/poketcg-pc.git`. A configured GitHub remote may be a read-only mirror; inspect Forgejo's configured push-mirror state when topology matters. Do not publish directly to a mirror. The canonical HTTPS host is already configured; this page does not provide credential provisioning or authentication repair instructions.

Forgejo mirrors refs to GitHub, not Release objects. The repository workflow creates GitHub Release objects after mirrored stable or nightly tags appear. Nightly comparison uses tracked source against the latest nightly tag for the current version, falling back to the matching stable tag when no nightly baseline exists. Generated completion/dashboard data paths do not independently trigger a nightly release; without a matching baseline tag, the first nightly is created.

In a fresh maintained colocated checkout, `just init-repo` restores canonical `main` tracking, trunk auto-advance, and guard checks. This does not provision network credentials.

## Normal change cycle

jj snapshots edits continuously into `@`; there is no staging area. Commit finished logical changes with a Conventional Commit message, then push the canonical `main` bookmark:

```sh
jj status
jj diff
jj commit -m "docs(readme): clarify usage"
jj git push --remote origin --bookmark main
```

Repository configuration auto-advances `main`. If it does not, advance the bookmark to the finished change before pushing. Fetch remote updates and rebase in-progress work onto `main`:

```sh
jj git fetch --remote origin
jj rebase -d main
```

For a review, push a feature bookmark rather than trunk, and update that bookmark when adding review changes:

```sh
jj git push --remote origin -c @-
```

Pushed history is immutable. Add new commits for review updates; do not rewrite commits already pushed to shared bookmarks. `jj op log` and `jj undo` provide operation-level recovery for local mistakes.

## Releases and changelog

Release tags and generated release history have separate ownership from ordinary commits. `CHANGELOG.md` is generated and must not be edited by hand. Stable and nightly release objects follow the repository release workflow; nightly source comparison and stable-tag fallback are described above. Do not treat a mirror's refs as proof that it carries release objects.

For issue reconciliation and verification/publication evidence ordering, follow [grind](grind.md). This page covers configured-clone jj operations, not the verification or publication runbook.
