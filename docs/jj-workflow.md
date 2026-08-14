# Version Control Workflow

This repo is a **colocated [Jujutsu](https://jj-vcs.github.io/jj/) + git** repository: `jj` is
the primary interface and a real `.git/` directory sits alongside `.jj/`. Plain `git` still
works for **reading** (`log`/`status`/`diff`/`show`), but a hook (`.claude/hooks/enforce-jj.sh`)
blocks mutating git — every VCS change goes through jj.

> Git's `HEAD` is left **detached** on purpose — jj drives the working copy, so there is no
> checked-out git branch. Don't `git push`; use `jj git push --remote origin`.

**The jj mindset.** `@` (the working copy) is snapshotted continuously; commit early and often
with `jj commit`, because commits are local, cheap, and fully reversible. Every commit and
operation is a point you can travel back to (`jj op log`, `jj undo`). Never hoard finished work
in an uncommitted `@` — a step you didn't commit is a restore point you don't have. Committing
is free and local; pushing to Forgejo `origin` is the step that publishes a local change.

## One-time user config

Set once per machine with `jj config edit --user` (`~/.config/jj/config.toml`):

```toml
[revset-aliases]
# Protect already-pushed history: rewriting a commit on a remote breaks review
# and shared history, so treat every remote bookmark as immutable.
'immutable_heads()' = 'builtin_immutable_heads() | remote_bookmarks()'

[aliases]
# `jj tug`: advance the nearest bookmark (e.g. main) to your latest finished change.
tug = ['bookmark', 'advance', '--to', '@-']
```

`jj b` is a built-in shorthand for `jj bookmark`.

**This repo also enables auto-advance for `main`** — repo-scoped, applied via:

```
jj config set --repo experimental-advance-branches.enabled-branches '["main"]'
```

With it, `main` follows every `jj commit` / `jj new` automatically (Git-style), so trunk work
is just `jj commit` then `jj git push --remote origin --bookmark main` — no manual `jj tug`.
`jj tug` stays the tool for feature bookmarks, which are deliberately *not* auto-advanced.

## Model: trunk-based on `main`

- `main` is a **bookmark** (jj's word for a branch), not a moving `HEAD`, configured to
  **auto-advance** on `jj commit` / `jj new`, so it tracks your latest finished change with no
  manual step (it also follows commits rewritten by `jj rebase` or amend).
- Work lands directly on `main`. Use a feature bookmark only when you want a PR/review.
- Keep the remote in sync: push after finishing a change.

## Remotes

- `origin` is `https://forgejo.yfrit.com/mpp/poketcg-pc.git`. Local and factory
  repository writes target this Forgejo remote.
- This maintained checkout also has
  `github-mirror = https://github.com/mp-pinheiro/poketcg-pc.git` for reading
  GitHub-side refs. `just init-repo` tracks `main@origin` but does not create
  this optional remote.

No Forgejo push mirror is currently configured. GitHub's `release` and
`progress snapshot` workflows independently push generated release/tag and
progress commits to GitHub `main`. `main@origin` and `main@github-mirror` can
therefore differ; fetch the remote whose state you are inspecting.

## One-time Forgejo HTTPS authentication

Git smart HTTP passes through two independent authentication layers:

1. Cloudflare Access accepts a service token on the scoped Git routes.
2. Forgejo accepts the short-lived token produced by `git-credential-oauth`.

Install the credential helper:

```sh
sudo apt-get install git-credential-oauth # Debian/Ubuntu
# brew install git-credential-oauth       # macOS
```

Configure the Cloudflare edge credential for this host. Obtain the two values
from the Forgejo infrastructure operator; neither value belongs in this
repository:

```sh
git config --global http.https://forgejo.yfrit.com/.extraHeader \
  "CF-Access-Client-Id: <client-id>.access"
git config --global --add http.https://forgejo.yfrit.com/.extraHeader \
  "CF-Access-Client-Secret: <client-secret>"
```

The second command uses `--add` because `extraHeader` is multi-valued. Then
configure Forgejo OAuth:

```sh
git config --global credential.https://forgejo.yfrit.com.helper ""
git config --global --add credential.https://forgejo.yfrit.com.helper \
  "cache --timeout 3600"
git config --global --add credential.https://forgejo.yfrit.com.helper oauth
git config --global credential.https://forgejo.yfrit.com.oauthClientId \
  a4792ccc-144e-407e-86c9-5e7d8d9c3269
git config --global credential.https://forgejo.yfrit.com.oauthAuthURL \
  /login/oauth/authorize
git config --global credential.https://forgejo.yfrit.com.oauthTokenURL \
  /login/oauth/access_token
```

The empty helper entry clears inherited helpers for this host, preventing a
global plaintext credential store from receiving the OAuth token. The cache
keeps the one-hour Forgejo token in memory. The first fetch or push opens a
browser for authorization; later operations reuse the cached token until it
expires. Forgejo remote URLs contain no username, because the OAuth helper
requires `https://forgejo.yfrit.com/<owner>/<repo>.git`.

The token file used by `just issues-fetch` is separate read-only REST
authentication; Git and jj do not read it.

## The change cycle

jj has no staging area — edits are snapshotted continuously into `@`. A fresh empty `@` with
"no description set" is normal; it is where your next edits go. Commit each finished step as you
go — not once at the end:

```
# edit files for one logical step — `jj status` / `jj diff` show what's in @
jj commit -m "type: subject"      # finalize this step; main auto-advances to it
```

Messages **must be [Conventional Commits](https://www.conventionalcommits.org)** —
`type(scope): subject` (`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`,
`chore`, `revert`; append `!` for a breaking change). A PreToolUse hook rejects `jj commit` /
`describe` / `squash` messages that don't match.

Use path-scoped `jj commit <files> -m "…"` to split unrelated changes sitting together in `@`.
When work is ready to leave your machine:

```
jj git push --remote origin --bookmark main
```

If this reports **"Nothing changed"**, `main` did not move. `jj tug`
(`jj bookmark advance --to @-`) advances it before the next push. Repository
configuration auto-advances `main`; feature bookmarks remain manual.

## Navigating through time (jj's core power)

| To … | Do |
|------|----|
| See every operation (incl. auto-snapshots), newest first | `jj op log` |
| Undo the last operation | `jj undo` |
| Rewind the **whole repo** to a past operation | `jj op restore <op-id>` |
| Inspect the commit graph | `jj log` |
| Amend an earlier commit in place | `jj edit <rev>` |
| Start a new change on top of any commit | `jj new <rev>` |
| Pull specific files from another revision into `@` | `jj restore --from <rev> [paths]` |
| Drop `@`'s uncommitted edits (reset to parent) | `jj restore` |
| Discard a whole commit | `jj abandon <rev>` |
| Diff any two points | `jj diff --from <rev> --to <rev>` |

`jj op log` + `jj op restore` is the safety net: any botched change is one command from being
rewound, **provided the good state was committed**.

## Sending a review branch to Forgejo

```
jj git push --remote origin -c @-  # creates a push-<change-id> bookmark

# or a named bookmark:
jj bookmark set my-feature -r @-
jj git push --remote origin --bookmark my-feature
```

Address review comments by adding a commit on top, then `jj tug` (or
`jj bookmark set my-feature -r @-`) and push the bookmark to `origin` again.
Because pushed bookmarks are immutable under the config above, jj refuses to
rewrite them accidentally.

## Updating from the remote (there is no `git pull`)

```
jj git fetch --remote origin
jj rebase -d main             # move your in-progress work onto the updated main
```

## Gotchas

- If jj reports a non-tracking `main@origin`, run once:
  `jj bookmark track main --remote=origin`.
- `jj undo` reverts the last jj operation — the safety net for a botched move or rebase.
- Read-only git (`log`/`status`/`diff`/`show`) and release `git tag` /
  `git push origin vX.Y.Z` stay allowed by the hook; everything else mutating
  goes through jj.

## Cheat sheet

| Task | Command |
|------|---------|
| Working-copy status | `jj status` |
| History (graph) | `jj log` |
| Finalize a change | `jj commit -m "…"` |
| Advance trunk to your change | automatic on commit (else `jj tug`) |
| Push trunk to Forgejo | `jj git push --remote origin --bookmark main` |
| Push a Forgejo review branch | `jj git push --remote origin -c @-` |
| Fetch Forgejo | `jj git fetch --remote origin` |
| Undo last jj op | `jj undo` |
| Operation log (time-travel) | `jj op log` |
| Rewind repo to a past op | `jj op restore <op-id>` |
| Amend an earlier commit | `jj edit <rev>` |
