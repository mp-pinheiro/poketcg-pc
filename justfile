# poketcg-pc — build, release, and oracle helpers.
# Conventional Commits → auto changelog + auto semver via git-cliff.

# Concurrent ports set POKETCG_BUILD to a private directory and POKETCG_PORTS to
# their own pret basenames, so neither ninja state nor a compile error is shared.
build_dir := env_var_or_default("POKETCG_BUILD", "build")
port_files := env_var_or_default("POKETCG_PORTS", "")
# default recipe
default:
    @just --list

# Clone + build the pret/poketcg disassembly the port is diffed against.
# Build-time input only: never a submodule, never committed.
bootstrap:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d poketcg ]; then
        git clone https://github.com/pret/poketcg poketcg
        git -C poketcg checkout 0e7157e
    fi
    make -C poketcg DEBUG=1
    cd poketcg && sha1sum -c rom.sha1

# Python venv holding PyBoy, used only by the oracle.
oracle-venv:
    uv venv /tmp/pbenv
    uv pip install --python /tmp/pbenv/bin/python pyboy

# Configure + build the C side (gbmem, poketcg_probe).
build:
    cmake -G Ninja -B {{build_dir}} -DCMAKE_BUILD_TYPE=Debug -DPORT_FILES="{{port_files}}"
    ninja -C {{build_dir}}

# Diff one routine's C port against PyBoy running the real ROM.
oracle-diff FN: build
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --fn {{FN}} --probe {{build_dir}}/poketcg_probe

# Diff every routine in tests/routines.py. Non-zero if any fails or has no cases.
oracle-diff-all: build
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --all --probe {{build_dir}}/poketcg_probe


oracleb-regenerate:
    #!/usr/bin/env bash
    set -euo pipefail
    generator="${POKETCG_GBRECOMP:-$HOME/.local/gbrecomp/gb-recompiled-linux/gbrecomp}"
    output="${POKETCG_ORACLEB_DIR:-$HOME/.local/share/gbrecompiled/poketcg}"
    "$generator" poketcg/poketcg.gbc --symbols poketcg/poketcg.sym -o "$output" -j 8
    cmake -G Ninja -S "$output" -B "$output/build"
    ninja -C "$output/build"
    cp "$output/build/poketcg" "$output/poketcg"

oracleb-scene:
    #!/usr/bin/env bash
    set -euo pipefail
    args=(--frames "${POKETCG_SCENE_FRAMES:-30}")
    if [ -n "${POKETCG_SCENE_INPUT:-}" ]; then
        args+=(--input "$POKETCG_SCENE_INPUT")
    fi
    python3 tests/scene_diff.py "${args[@]}"
data-verify:
    python3 tools/gen_data.py --verify
    python3 tools/gen_data.py --check

# Print the next version git-cliff derives from unreleased Conventional Commits.
next-version:
    @git cliff --bump --unreleased --context 2>/dev/null \
        | jq -r 'map(select(.version != null and ((.commits // []) | length > 0))) | .[0].version // empty | ltrimstr("v")'

# Regenerate the full CHANGELOG.md (all releases + the bumped unreleased section).
changelog:
    git cliff --bump -o CHANGELOG.md

# Cut a release locally: bump VERSION, regenerate CHANGELOG, commit, tag, push.
# Requires a clean working copy. Run after merging feature work to main.
# (CI also auto-releases on push to main; this is the manual path.)
release:
    #!/usr/bin/env bash
    set -euo pipefail
    next="$(just next-version)"
    [ -n "$next" ] || { echo "nothing to release (no unreleased Conventional Commits)"; exit 0; }
    cur="$(cat VERSION 2>/dev/null || echo none)"
    [ "$next" != "$cur" ] || { echo "VERSION already at $next; nothing to release"; exit 0; }
    printf '%s\n' "$next" > VERSION
    git cliff --bump -o CHANGELOG.md
    jj commit VERSION CHANGELOG.md -m "chore(release): v${next}"
    sha="$(jj log -r '@-' --no-graph -T 'commit_id' | head -1 | tr -d ' \n')"
    git tag "v${next}" "$sha"
    jj git push --bookmark main
    git push origin "v${next}"
    echo "released v${next}"
