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
    if [ -f poketcg/poketcg.gbc ]; then
        python3 tools/verify_oracle_artifacts.py
    fi
    make -C poketcg DEBUG=1
    python3 tools/verify_oracle_artifacts.py


# Per-clone VCS setup: jj --repo config lives outside the repo, so a fresh
# clone loses trunk auto-advance until this runs. Idempotent.
init-repo:
    #!/usr/bin/env bash
    set -euo pipefail
    jj config set --repo experimental-advance-branches.enabled-branches '["main"]'
    jj bookmark list --all-remotes | grep -q '^main@origin:' && jj bookmark track main --remote=origin || true
    just verify-hooks

# Prove the PreToolUse guards still block what they must and allow the workflow.
verify-hooks:
    #!/usr/bin/env bash
    set -euo pipefail
    fail=0
    check() {  # check <expected-exit> <hook> <command>
        rc=0
        printf '{"tool_input":{"command":"%s"}}' "$3" | bash ".claude/hooks/$2" >/dev/null 2>&1 || rc=$?
        [ "$rc" = "$1" ] || { echo "hook $2: [$3] want exit $1, got $rc" >&2; fail=1; }
    }
    check 2 enforce-jj.sh                     'git commit -m x'
    check 2 enforce-jj.sh                     'git push origin main'
    check 0 enforce-jj.sh                     'jj git push'
    check 0 enforce-jj.sh                     'git status --short'
    check 0 enforce-jj.sh                     'git tag v1.0.0'
    check 2 enforce-conventional-commits.sh   'jj commit -m wip'
    check 0 enforce-conventional-commits.sh   'jj commit -m "feat: x"'
    exit $fail

# Python venv holding PyBoy, used only by the oracle.
oracle-venv:
    #!/usr/bin/env bash
    set -euo pipefail
    export UV_PROJECT_ENVIRONMENT=/tmp/pbenv
    uv python install 3.12.3
    uv sync --project tools/oracle --python 3.12.3 --managed-python --frozen --reinstall-package pyboy

# Validate the installed PyBoy execution path before replacing it.
oracle-health-pyboy:
    PYTHONPATH=tools/oracle /tmp/pbenv/bin/python tools/oracle/pyboy_health.py

oracle-health-gbref: oracle-build-gbref build-barrier
    python3 tools/oracle/gbref_health.py
oracle-health: oracle-health-gbref oracle-health-pyboy
oracle-build-gbref:
    #!/usr/bin/env bash
    set -euo pipefail
    runtime="${GBRT_RUNTIME_DIR:-$HOME/.local/gbrecomp/gb-recompiled-linux/runtime}"
    cmake -G Ninja -S tools/oracle/gbref -B tools/oracle/gbref/build -DGBRT_RUNTIME_DIR="$runtime" -DCMAKE_BUILD_TYPE=Debug
    ninja -C tools/oracle/gbref/build gbref_runner

oracle-audit-cases STAGE:
    python3 tools/audit_oracle_cases.py --stage {{STAGE}}


# Configure + build the C side (gbmem, poketcg_probe).
build:
    cmake -G Ninja -B {{build_dir}} -DCMAKE_BUILD_TYPE=Debug -DPORT_FILES="{{port_files}}"
    ninja -C {{build_dir}}

# Fixed central barrier build; ignores slice-scoped environment variables.
build-barrier:
    cmake -G Ninja -B build-barrier -DCMAKE_BUILD_TYPE=Debug -DPORT_FILES=""
    ninja -C build-barrier

# Legacy full inventory remains PyBoy-backed until the GBRT driver lands.
oracle-fn-all-legacy: build-barrier lint-adapters
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --all --probe build-barrier/poketcg_probe


# Rebuild an already configured private tree without re-running CMake.
build-incremental:
    #!/usr/bin/env bash
    set -euo pipefail
    cache="{{build_dir}}/CMakeCache.txt"
    [ -f "{{build_dir}}/build.ninja" ] && [ -f "$cache" ] || {
        echo "run just build after choosing a new POKETCG_BUILD or POKETCG_PORTS" >&2
        exit 2
    }
    grep -Fqx 'PORT_FILES:STRING={{port_files}}' "$cache" || {
        echo "run just build after choosing a new POKETCG_BUILD or POKETCG_PORTS" >&2
        exit 2
    }
    ninja -C "{{build_dir}}"

oracle-warm FN: build-incremental
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --fn {{FN}} --oracle-mode refresh --cache-dir {{build_dir}}/oracle-cache --probe {{build_dir}}/poketcg_probe

oracle-warm-group GROUP: build-incremental
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --group {{GROUP}} --oracle-mode refresh --cache-dir {{build_dir}}/oracle-cache --probe {{build_dir}}/poketcg_probe

oracle-diff-fast FN: build-incremental
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --fn {{FN}} --oracle-mode cache --cache-dir {{build_dir}}/oracle-cache --probe {{build_dir}}/poketcg_probe

oracle-diff-fast-group GROUP: build-incremental
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --group {{GROUP}} --oracle-mode cache --cache-dir {{build_dir}}/oracle-cache --probe {{build_dir}}/poketcg_probe

oracle-diff-group GROUP: build
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --group {{GROUP}} --oracle-mode live --probe {{build_dir}}/poketcg_probe



# Run one schema-2 case through the GBRT primary and native probe.
oracle-fn FN CASE INDEX="0": oracle-build-gbref build-barrier
    python3 tools/oracle/gbref/compare_one.py --fn {{FN}} --index {{INDEX}} --case {{CASE}} --rom "$(realpath poketcg/poketcg.gbc)" --symbols "$(realpath poketcg/poketcg.sym)" --probe "$(realpath build-barrier/poketcg_probe)" --runner "$(realpath tools/oracle/gbref/build/gbref_runner)"
# Diff one routine's C port against PyBoy running the real ROM.

# Run migrated schema-2 cases; intentionally incomplete until registry migration closes.
oracle-fn-migrated: oracle-build-gbref build-barrier lint-adapters
    python3 tools/oracle/fn_all.py --rom "$(realpath poketcg/poketcg.gbc)" --symbols "$(realpath poketcg/poketcg.sym)" --probe "$(realpath build-barrier/poketcg_probe)" --runner "$(realpath tools/oracle/gbref/build/gbref_runner)"
# Fixed GBRT primary inventory barrier.
oracle-fn-all: oracle-build-gbref build-barrier lint-adapters
    mkdir -p site/data
    python3 tools/oracle/fn_all.py --rom "$(realpath poketcg/poketcg.gbc)" --symbols "$(realpath poketcg/poketcg.sym)" --probe "$(realpath build-barrier/poketcg_probe)" --runner "$(realpath tools/oracle/gbref/build/gbref_runner)" --report site/data/gate.json
# Primary function gate: GBRT health, adapters, schema, and inventory.
oracle-fn-gate: oracle-health-gbref oracle-fn-all
    python3 tools/audit_oracle_cases.py --stage routine


# Run the GBRT primary gate and regenerate the progress report from the result.
gate-report: oracle-fn-all
    python3 tools/progress/report.py build

# Independent PyBoy audit lane; a health failure quarantines this lane.
oracle-audit-all: oracle-health-pyboy
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --all --oracle-mode live --probe build-barrier/poketcg_probe

# Aggregate function gate adds the independent PyBoy audit.
oracle-gate: oracle-fn-gate oracle-audit-all
    python3 tools/audit_oracle_cases.py --stage routine
oracle-diff FN: build
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    /tmp/pbenv/bin/python tests/test_leaves.py --fn {{FN}} --probe {{build_dir}}/poketcg_probe

# Diff every routine in tests/routines.py. Non-zero if any fails or has no cases.
oracle-diff-all: build lint-adapters
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    mkdir -p site/data
    /tmp/pbenv/bin/python tests/test_leaves.py --all --probe {{build_dir}}/poketcg_probe --report site/data/gate.json

# Reject probe adapters that reimplement the routine they marshal (issue #19).
lint-adapters:
    python3 tools/lint_adapters.py


oracleb-regenerate:
    #!/usr/bin/env bash
    set -euo pipefail
    generator="${POKETCG_GBRECOMP:-$HOME/.local/gbrecomp/gb-recompiled-linux/gbrecomp}"
    output="${POKETCG_ORACLEB_DIR:-$HOME/.local/share/gbrecompiled/poketcg}"
    jobs="${POKETCG_GBRECOMP_JOBS:-1}"
    "$generator" poketcg/poketcg.gbc --symbols poketcg/poketcg.sym -o "$output" -j "$jobs"
    cmake -G Ninja -S "$output" -B "$output/build"
    ninja -C "$output/build" -j "$jobs"
    cp "$output/build/poketcg" "$output/poketcg"

oracleb-scene:
    #!/usr/bin/env bash
    set -euo pipefail
    args=(--frames "${POKETCG_SCENE_FRAMES:-30}")
    if [ -n "${POKETCG_SCENE_INPUT:-}" ]; then
        args+=(--input "$POKETCG_SCENE_INPUT")
    fi
    # A scene diff without a C state vector compares nothing, so this recipe demands
    # one. Use `just oracleb-replay` for the determinism half on its own.
    if [ -z "${POKETCG_SCENE_CSTATE:-}" ]; then
        echo "oracleb-scene needs POKETCG_SCENE_CSTATE=<snapshot.json>" >&2
        echo "for the replay-determinism half alone, run: just oracleb-replay" >&2
        exit 2
    fi
    args+=(--c-state "$POKETCG_SCENE_CSTATE")
    python3 tests/scene_diff.py "${args[@]}"

# Replay-determinism half only: run a scene twice and require identical state.
oracleb-replay:
    #!/usr/bin/env bash
    set -euo pipefail
    args=(--frames "${POKETCG_SCENE_FRAMES:-30}" --replay-only)
    if [ -n "${POKETCG_SCENE_INPUT:-}" ]; then
        args+=(--input "$POKETCG_SCENE_INPUT")
    fi
    python3 tests/scene_diff.py "${args[@]}"
data-verify: assets-verify
    python3 tools/gen_data.py --verify
    python3 tools/gen_data.py --check
assets-verify:
    python3 tools/gen_assets.py --verify
    python3 tools/gen_assets.py --check
    python3 tools/gen_lz.py --verify
    python3 tools/gen_lz.py --check
# Regenerate the pret code inventory (needs `just bootstrap`; rerun when the pret pin moves).
progress-inventory:
    python3 tools/progress/inventory.py

# Recompute site/data/progress.json + history point from the registry and gate record.
progress:
    python3 tools/progress/report.py build

# Unported routines whose callees are all ported — the porting work queue.
frontier LIMIT="30":
    python3 tools/progress/report.py frontier --limit {{LIMIT}}

# Serve the dashboard at http://127.0.0.1:8765
progress-serve:
    python3 -m http.server 8765 --directory site


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
