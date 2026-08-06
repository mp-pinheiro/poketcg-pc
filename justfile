# poketcg-pc — build, release, and oracle helpers.
# Conventional Commits → auto changelog + auto semver via git-cliff.

# default recipe
default:
    @just --list

# Print the next version git-cliff derives from unreleased Conventional Commits.
next-version:
    @git cliff --bump --unreleased --context 2>/dev/null \
        | jq -r 'map(select(.version != null and ((.commits // []) | length > 0))) | .[0].version // empty | ltrimstr("v")'

# Regenerate CHANGELOG.md from Conventional Commits (bumped, unreleased).
changelog:
    git cliff --bump --unreleased -o CHANGELOG.md

# Cut a release locally: bump VERSION, regenerate CHANGELOG, commit, tag, push.
# Requires a clean working copy. Run after merging feature work to main.
# (CI also auto-releases on push to main; this is the manual path.)
release:
    #!/usr/bin/env bash
    set -euo pipefail
    next="$$(just next-version)"
    [ -n "$$next" ] || { echo "nothing to release (no unreleased Conventional Commits)"; exit 0; }
    cur="$$(cat VERSION 2>/dev/null || echo none)"
    [ "$$next" != "$$cur" ] || { echo "VERSION already at $$next; nothing to release"; exit 0; }
    printf '%s\n' "$$next" > VERSION
    git cliff --bump --unreleased -o CHANGELOG.md
    jj commit VERSION CHANGELOG.md -m "chore(release): v$${next}"
    sha="$$(jj log -r '@-' --no-graph -T 'commit_id' | head -1 | tr -d ' ')"
    git tag "v$${next}" "$$sha"
    jj git push --allow-new
    git push origin "v$${next}"
    echo "released v$$next"
