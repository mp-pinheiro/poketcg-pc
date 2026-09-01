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
    # printf built the payload by hand, so any command containing a double quote
    # produced invalid JSON, jq inside the hook returned empty and the hook fell
    # open -- every such case passed without exercising the guard at all. The
    # payload is materialised before the pipe on purpose: a hook that exits
    # before draining stdin (the derived-data guard does, wherever jj is absent)
    # would hand jq a SIGPIPE and pipefail would report 141 as the hook's verdict.
    payload() { jq -n --arg c "$1" '{tool_input:{command:$c}}'; }
    check() {  # check <expected-exit> <hook> <command>
        rc=0
        json=$(payload "$3")
        printf '%s' "$json" | bash ".claude/hooks/$2" >/dev/null 2>&1 || rc=$?
        [ "$rc" = "$1" ] || { echo "hook $2: [$3] want exit $1, got $rc" >&2; fail=1; }
    }
    check_stub() {  # check_stub <expected-exit> <hook> <command> <dirty-paths>
        # The derived-data guard reads the working copy, so its verdict is only
        # deterministic against a stub jj; the real binary is absent in CI, where
        # the guard fails open.
        rc=0
        stub=$(mktemp -d)
        printf '#!/usr/bin/env bash\nprintf "%%b" "%s\\n"\n' "$4" > "$stub/jj"
        chmod +x "$stub/jj"
        json=$(payload "$3")
        printf '%s' "$json" \
            | PATH="$stub:$PATH" bash ".claude/hooks/$2" >/dev/null 2>&1 || rc=$?
        rm -rf "$stub"
        [ "$rc" = "$1" ] || { echo "hook $2: [$3] dirty=[$4] want exit $1, got $rc" >&2; fail=1; }
    }
    check 2 enforce-jj.sh                     'git commit -m x'
    check 2 enforce-jj.sh                     'git push origin main'
    check 0 enforce-jj.sh                     'jj git push'
    check 0 enforce-jj.sh                     "jj --config 'experimental-advance-branches.enabled-branches=[]' git push --bookmark main"
    check 0 enforce-jj.sh                     "jj --config 'experimental-advance-branches.enabled-branches=[]' git fetch"
    check 0 enforce-jj.sh                     'git status --short'
    check 0 enforce-jj.sh                     'git tag v1.0.0'
    check 2 enforce-conventional-commits.sh   'jj commit -m wip'
    check 0 enforce-conventional-commits.sh   'jj commit -m "feat: x"'
    check 0 enforce-derived-data.sh            'jj log -r @'
    check 0 enforce-derived-data.sh            'python3 tools/progress/report.py build'
    check_stub 2 enforce-derived-data.sh 'jj commit -m "chore(factory): block x"' '.factory/blocked.toml'
    check_stub 0 enforce-derived-data.sh 'jj commit -m "chore(factory): block x"' '.factory/blocked.toml\nsite/data/progress.json'
    check_stub 0 enforce-derived-data.sh 'jj commit -m "feat(port): land 1 routines"' 'src/home/menus.c\ntests/cases/menus.py'
    exit $fail

# Python venv holding PyBoy, used only by the oracle.
oracle-venv:
    #!/usr/bin/env bash
    set -euo pipefail
    uv python install 3.12.3
    uv sync --project tools/oracle --python 3.12.3 --frozen --reinstall-package pyboy



oracle-venv-release: oracle-venv
    #!/usr/bin/env bash
    set -euo pipefail
    tarball=/tmp/pyboy-prebuilt.tar.zst
    sitepkg=tools/oracle/.venv/lib/python3.12/site-packages
    echo "packing pyboy → $tarball ..."
    tar -caf "$tarball" -C "$sitepkg" pyboy
    echo "uploading to GitHub release oracle-venv ..."
    if gh release view oracle-venv &>/dev/null; then
        gh release upload oracle-venv "$tarball" --clobber
    else
        gh release create oracle-venv "$tarball" \
            --title "Pre-built PyBoy" \
            --notes "Compiled PyBoy extension for Copilot setup." \
            --prerelease
    fi
    echo "done"
# Validate the installed PyBoy execution path before replacing it.
oracle-health-pyboy:
    uv run --project tools/oracle --frozen --python 3.12.3 python tools/oracle/pyboy_health.py

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
    uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --fn {{FN}} --oracle-mode refresh --cache-dir {{build_dir}}/oracle-cache --probe {{build_dir}}/poketcg_probe

oracle-warm-group GROUP: build-incremental
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --group {{GROUP}} --oracle-mode refresh --cache-dir {{build_dir}}/oracle-cache --probe {{build_dir}}/poketcg_probe

oracle-diff-fast FN: build-incremental
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --fn {{FN}} --oracle-mode cache --cache-dir {{build_dir}}/oracle-cache --probe {{build_dir}}/poketcg_probe

oracle-diff-fast-group GROUP: build-incremental
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --group {{GROUP}} --oracle-mode cache --cache-dir {{build_dir}}/oracle-cache --probe {{build_dir}}/poketcg_probe

oracle-diff-group GROUP: build
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --group {{GROUP}} --oracle-mode live --probe {{build_dir}}/poketcg_probe



# Run one schema-2 case through the GBRT primary and native probe.
oracle-fn FN CASE INDEX="0": oracle-build-gbref build-barrier
    python3 tools/oracle/gbref/compare_one.py --fn {{FN}} --index {{INDEX}} --case {{CASE}} --rom "$(realpath poketcg/poketcg.gbc)" --symbols "$(realpath poketcg/poketcg.sym)" --probe "$(realpath build-barrier/poketcg_probe)" --runner "$(realpath tools/oracle/gbref/build/gbref_runner)"
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
    uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --all --oracle-mode live --probe build-barrier/poketcg_probe

# Sharded PyBoy audit: 4 processes over the sorted census; same verdicts as --all.
oracle-audit-all-parallel: oracle-health-pyboy
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    tmp=$(mktemp -d)
    pids=()
    for i in 0 1 2 3; do
        uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --all --oracle-mode live --probe build-barrier/poketcg_probe --shard "$i/4" >"$tmp/$i.log" 2>&1 &
        pids+=("$!")
    done
    rc=0
    for pid in "${pids[@]}"; do
        wait "$pid" || rc=1
    done
    cat "$tmp"/0.log "$tmp"/1.log "$tmp"/2.log "$tmp"/3.log
    rm -rf "$tmp"
    exit "$rc"

# Advisory differential fuzz over the thinnest landed matrices; never gates.
oracle-fuzz-thin: oracle-build-gbref build-barrier
    python3 tools/oracle/fuzz_one.py --thinnest 20 --variants 16

# Aggregate function gate adds the independent PyBoy audit.
oracle-gate: oracle-fn-gate oracle-audit-all-parallel
    python3 tools/audit_oracle_cases.py --stage routine

# Sole release authority. It records an immutable run and an atomic pointer.
oracle-release-gate:
    python3 tools/oracle/release_gate.py

# Diff one routine's C port against PyBoy running the real ROM.
oracle-diff FN: build
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --fn {{FN}} --probe {{build_dir}}/poketcg_probe

# Diff every routine in tests/routines.py. Non-zero if any fails or has no cases.
oracle-diff-all: build lint-adapters
    #!/usr/bin/env bash
    set -euo pipefail
    export POKETCG_ROM=poketcg/poketcg.gbc
    uv run --project tools/oracle --frozen --python 3.12.3 python tests/test_leaves.py --all --probe {{build_dir}}/poketcg_probe

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


# Truthful completion audit and revision-pinned obligation checks.
completion-audit:
    python3 tools/completion/completion.py audit
completion-status *ARGS:
    python3 tools/completion/completion.py status {{ARGS}}
completion-check ID:
    python3 tools/completion/completion.py check "{{ID}}"
completion-baseline:
    python3 tools/completion/completion.py baseline
completion-rom-coverage:
    python3 tools/completion/completion.py rom-coverage
completion-routine-mapping:
    python3 tools/completion/completion.py routine-mapping
completion-representation:
    python3 tools/completion/completion.py representation
completion-truthful-accounting:
    python3 tools/completion/completion.py truthful-accounting
completion-substrate:
    python3 tools/completion/completion.py substrate
completion-next:
    python3 tools/completion/completion.py next

completion-mutation-campaign *ARGS:
    python3 tools/completion/mutation_campaign.py {{ARGS}}
# Generate only declared ROM data spans for the local product package.
completion-data-pack:
    just progress-inventory
    just data-verify
    python3 tools/gen_data.py --sparse-pack --verify
completion-data-pack-check:
    python3 tools/gen_data.py --pack-check

package-smoke:
    just build
    just completion-data-pack
    python3 tools/completion/package_smoke.py

completion-lanes-health:
    python3 tools/completion/oracle_lanes.py --health

completion-gambatte-bootstrap:
    python3 tools/completion/gambatte_runner.py bootstrap
completion-gambatte-health:
    python3 tools/completion/gambatte_runner.py health
completion-capture SCENARIO *ARGS:
    python3 tools/completion/gambatte_runner.py capture "{{SCENARIO}}" {{ARGS}}

completion-cfg-audit:
    python3 tools/completion/cfg.py --trace "${POKETCG_CFG_TRACE:?CFG trace is required}"

completion-tracker-sync:
    python3 tools/completion/sync_tracker.py --apply
completion-tracker-check:
    python3 tools/completion/sync_tracker.py --check
completion-scenario SCENARIO:
    python3 tools/completion/scenario.py "{{SCENARIO}}"
# Recompute site/data/progress.json + history point from the registry and gate record.
progress:
    python3 tools/progress/report.py build

# Unported routines whose callees are all ported — the porting work queue.
frontier LIMIT="30":
    python3 tools/progress/report.py frontier --limit {{LIMIT}}

# Serve the dashboard at http://127.0.0.1:8765
progress-serve:
    python3 -m http.server 8765 --directory site

# Publish site/ to Cloudflare Pages, falling back to the `cf` OAuth session.
publish-dashboard:
    #!/usr/bin/env bash
    set -euo pipefail
    export CLOUDFLARE_ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID:-70e78683a3a8f9c4dce4343d65b091d7}"
    if [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
        cf auth whoami >/dev/null 2>&1 || true
        CLOUDFLARE_API_TOKEN="$(python3 -c "import json,pathlib;p=pathlib.Path.home()/'.config/cloudflare/config/default.json';print(json.loads(p.read_text())['oauth_token'])")"
        export CLOUDFLARE_API_TOKEN
    fi
    npx wrangler@4 pages deploy site/ --project-name poketcg-pc --branch main

# Rehearse the real pipeline on a landed routine: packet, prompt, reply
# validation, surgery. Offline, no compiler, no model, no Forgejo.
factory-smoke:
    python3 tools/factory/smoke.py

# The same rehearsal plus lane build, oracle verify, artifact bundle, and the
# landing driver against a throwaway git remote.
factory-smoke-full:
    python3 tools/factory/smoke.py --full


# One routine, k candidates, the real verifier. No Forgejo, no ledger.
factory-try FN:
    python3 tools/factory/try_one.py --fn {{FN}}


# Next N ready routines (blocked.toml respected), prompts prepared.
factory-next N="4":
    python3 tools/factory/try_one.py --next {{N}}


# Reconcile the ledgers against the tree: reap issued attempts that can never be
# verified, re-offer landings whose content is missing, retire exhausted reds.
# Writes .factory/blocked.toml (tracked) when a red is retired; an operational
# blocker is an input to the derived work records, so the snapshot is rebuilt in
# the same breath and both are committed together.
factory-heal:
    python3 tools/factory/heal.py --apply
    python3 tools/progress/report.py build

# What the ledgers would repair, without touching anything.
factory-heal-dry:
    python3 tools/factory/heal.py

# Rank the remaining obstructions by how many routines clearing each one frees.
factory-capabilities N="5":
    python3 tools/factory/try_one.py --capabilities {{N}}

# Land every verified artifact: gate, commit, push, record.
factory-land:
    python3 tools/factory/land.py --all

# Forecast from recorded landings only.
factory-eta:
    python3 tools/factory/land.py --eta

# Prove the push credential without a browser prompt.
forgejo-auth-check:
    git ls-remote origin main


# Autonomous port factory: one persistent OMP session driving claimed work.
launch-port:
    tools/factory/run.sh



# Supervised loop: auto-restarts until `.factory/STOP` exists (500 max).
launch-port-supervised:
    tools/factory/supervise.sh


# Start N supervised loop sessions in a dedicated detached tmux session.
fleet-start panes="4":
    tools/factory/fleet.sh start {{panes}}

# Graceful fleet stop: every loop session exits after its current pass.
fleet-stop:
    tools/factory/fleet.sh stop

# Immediate fleet stop: also terminates in-flight sessions (state is safe).
fleet-halt:
    tools/factory/fleet.sh halt

# Loop-session count, STOP-file state, and fleet tmux session state.
fleet-status:
    tools/factory/fleet.sh status

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
