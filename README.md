# poketcg-pc

A hand-port of the Pokémon Trading Card Game for Game Boy Color to C11 + SDL2. The C routines are checked against the original ROM through PyBoy; the build-time disassembly checkout is created by `just bootstrap` and is not committed.

## Dependencies

On Linux, install:

```sh
sudo apt install \
  build-essential cmake ninja-build python3 python3-venv \
  git libsdl2-dev
```

The project also uses:

- `just` for repository commands.
- `jj` for version control writes.
- `tools/git-credential-forgejo` (in-repo) for non-interactive Forgejo HTTPS
  authentication; verify with `just forgejo-auth-check`.
- `uv` for the PyBoy virtual environment.
- `git-cliff` for the generated `CHANGELOG.md` and release recipe.
- Python packages installed by `just oracle-venv`.

The CMake project requires CMake 3.20 or newer, C11, Python 3, and usable SDL2 headers and libraries. The native build uses Ninja.

## Initial setup

From the repository root:

```sh
just bootstrap
uv sync --project tools/oracle --frozen
just build
```

`just bootstrap` clones the pinned `pret/poketcg` disassembly and verifies its ROM checksum. `uv sync --project tools/oracle --frozen` installs the pinned PyBoy project.

## Verification

```sh
export POKETCG_BUILD=build
export POKETCG_PORTS=""
just oracle-diff <RoutineName>
just oracle-fn-gate
just oracle-audit-all
just oracle-release-gate
```
`just progress-serve` serves a port-progress dashboard at `http://127.0.0.1:8765`.
Published at `https://poketcg-pc.pages.dev` via Cloudflare Pages.

The release gate requires the ROM produced by `just bootstrap`; it runs the
GBRT primary inventory, the independent PyBoy audit, schema and mutation
audits, and the data round-trip. Concurrent work should use a private
`POKETCG_BUILD` directory and a semicolon-separated `POKETCG_PORTS` list.

## Factory dispatch

Routine packet eligibility comes from the Forgejo issue snapshot:

```sh
just issues-fetch
just issues-plan
just issues-verify
python3 tools/factory/packet.py build --max-routines 3 --max-asm-lines 140 --json
```

`issues-fetch` replaces `.factory/issues-cache.json` only after the paginated
Forgejo listing stabilizes and covers every non-excluded canonical routine.
`issues-plan` writes a read-only desired-state audit; `issues-verify` refreshes
the listing and checks marker coverage. Packet construction then selects only
ready routines whose managed issue is open and labeled `port-ready`. These
commands do not mutate Forgejo issues. See `docs/factory-workflow.md` for the
orchestrator loop and `docs/factory-contract.md` for translator constraints.

## GB Recompiled replay oracle

`just oracleb-replay` runs `tests/scene_diff.py` in replay-only mode. It expects the generated executable at:

```text
$HOME/.local/share/gbrecompiled/poketcg/poketcg
```

The project’s `just oracleb-regenerate` recipe expects the recompiler at:

```text
$HOME/.local/gbrecomp/gb-recompiled-linux/gbrecomp
```

A Linux x64 prebuilt recompiler is available in the upstream `GB Recompiled 0.1.0` release:

<https://github.com/arcanite24/gb-recompiled/releases/tag/v0.1.0>

Install the verified archive into the path expected by this repository:

```sh
mkdir -p "$HOME/.local/gbrecomp"
curl -L --fail --silent --show-error \
  -o /tmp/gb-recompiled-linux-x64.tar.gz \
  https://github.com/arcanite24/gb-recompiled/releases/download/v0.1.0/gb-recompiled-linux-x64.tar.gz
printf '%s  %s\n' \
  b77fbf8913a9dd770097df81e8e0f84cf2e0d9e3a44dc1a1ee4d1846c5035535 \
  /tmp/gb-recompiled-linux-x64.tar.gz | sha256sum -c -

tar -xzf /tmp/gb-recompiled-linux-x64.tar.gz -C "$HOME/.local/gbrecomp"
"$HOME/.local/gbrecomp/gb-recompiled-linux/gbrecomp" --version
```
For a lower-memory build, set `POKETCG_GBRECOMP_JOBS=1`; the regeneration
recipe defaults to one job.

Then regenerate and build the replay executable:

```sh
just oracleb-regenerate
just oracleb-replay
```

`oracleb-regenerate` analyzes the pinned ROM and builds generated native code. It can be substantially more resource-intensive than the routine oracle; stop it if system load becomes unacceptable. The ROM and symbol inputs remain the locally bootstrapped files under `poketcg/`.

GB Recompiled does not include ROMs. Use only ROM images you are legally allowed to use.

## Repository guidance

Read `AGENTS.md` before making changes. The normative porting contract is `docs/port-contract.md`; a port run is orchestrated from `docs/factory-workflow.md`; architecture is in `docs/vision.md`.
