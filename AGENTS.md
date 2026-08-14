# poketcg-pc — agent contract

## 1. What this repo is

A hand-port of [`pret/poketcg`](https://github.com/pret/poketcg) (Pokémon Trading
Card Game, Game Boy Color) to C11 + SDL2, verified function-by-function against a
PyBoy oracle running the real ROM. `poketcg/` is a build-time clone of the
disassembly (`just bootstrap`), never a submodule, never committed.

## 2. Read before writing any C

In this order:

1. `docs/port-contract.md` — the contract, in full. Memory model, the three C
   rules, adapter rules, case-key reference, mutation testing, exclusion
   taxonomy. Normative.
2. `docs/factory-contract.md` — the exact `CONTRACT`/`CASES`/`MUTATIONS` block
   format a translator must emit. Normative for case modules.
3. `docs/vision.md` — architecture and phase order. Descriptive, optional.

Orchestrating a port run instead of writing C? `docs/factory-workflow.md` is the
only runbook you need.

## 3. Dependencies

Linux setup requires `build-essential`, CMake 3.20+, Ninja, Python 3, Git,
SDL2 development headers/libraries, `just`, `jj`, `uv`, and `git-cliff`.
Forgejo credentials come from the in-repo helper `tools/git-credential-forgejo`
(`just forgejo-auth-check` proves them); no browser or OAuth helper is involved.

`just bootstrap` creates the pinned `poketcg/` disassembly checkout.
`just oracle-venv` creates `/tmp/pbenv` and installs PyBoy.

The optional replay oracle uses GB Recompiled 0.1.0. Install its Linux x64
prebuilt archive so the generator is executable at
`$HOME/.local/gbrecomp/gb-recompiled-linux/gbrecomp`; `just oracleb-regenerate`
then emits the replay binary under
`$HOME/.local/share/gbrecompiled/poketcg/poketcg`. Verify the archive against
the SHA256 value in `README.md` before extracting it.

`oracleb-regenerate` performs whole-ROM static analysis and is substantially
more resource-intensive than the routine oracle. It defaults to one build job;
set `POKETCG_GBRECOMP_JOBS` to raise parallelism. A run that exhausts available
resources may terminate before producing the replay binary; in that case
`just oracleb-replay` remains unavailable.

## 4. Commands

The commands that matter, from the `justfile`:

| command | what |
|---|---|
| `just bootstrap` | clone + build the disassembly (one-time) |
| `just oracle-venv` | PyBoy into `/tmp/pbenv` (one-time) |
| `just build` | configure + build the C side |
| `just oracle-diff <Fn>` | diff one routine against the PyBoy oracle — the per-routine check |
| `just oracle-release-gate` | **the gate.** Central barrier; the only producer of `site/data/gate.json` |
| `just oracle-diff-all` | older PyBoy-only full sweep. Orchestrator only; writes no gate record |
| `just progress` | rebuild the progress report from registry + gate |
| `just frontier` | print unported routines whose callees are all ported |
| `just forgejo-auth-check` | prove git + REST credentials work non-interactively |
| `just issues-fetch` | refresh the read-only Forgejo issue cache |
| `just issues-plan` | write the desired-state issue audit (no writes to Forgejo) |
| `just issues-sync` | dry-run the Forgejo reconciliation |
| `just issues-sync-apply` | apply it — the only command that mutates Forgejo issues |
| `just data-verify` | data/asset extraction round-trip |
| `just progress-serve` | serve the dashboard at http://127.0.0.1:8765 |

## 5. Concurrency protocol

Each concurrent agent owns a private build directory and a private file subset:

```sh
export POKETCG_BUILD=build-<slice>
export POKETCG_PORTS="<pret basenames>"   # semicolon list; see CMakeLists.txt:34-60
```

Agents **never** run `just oracle-diff-all`. A routine registered in
`tests/routines.py` without cases is a hard FAIL for everyone, so only the
barrier — run centrally, after every slice lands — runs the full gate.

## 6. File ownership

Four files per pret source: `src/home/<f>.c`, `src/home/<f>.h`, `src/probe/<f>.c`,
`tests/cases/<f>.py`.

Shared, not owned by any slice: `CMakeLists.txt`, `src/mem.*`, `src/probe.c`,
`tools/progress/`, `site/`, `src/probe.h`, `src/probe_table.c`, `tests/test_leaves.py`, `tools/`, `justfile`.

`tests/routines.py` is **derived** — it registers `tuple(CONTRACT.keys())` from
every `tests/cases/<basename>.py` at import time. Never hand-edit it;
registration is a side effect of the cases module existing.

## 7. Definition of done

- `just oracle-diff <Fn>` prints `PASS`.
- Required case coverage exists (`docs/port-contract.md`): an all-zero case, a
  poisoned-register case, every boundary.
- A **recorded mutation test**: corrupt the routine, confirm the diff goes RED,
  restore, confirm PASS.
- An input-waiting routine (drives `ReadJoypad`/`hKeysHeld`) is tested by passing
  `keys` in its case — see `docs/port-contract.md`'s case-key reference.
- No stubs, no `TODO`, no dead routines, no changes outside the four owned files.

## 8. VCS

jj only — git writes are hook-blocked (`.claude/hooks/enforce-jj.sh`). Commit with

```sh
jj commit -m "type(scope): subject"
```

≤50-char subject, no body, no emoji, no bullet lists
(`.claude/hooks/enforce-conventional-commits.sh`). `main` auto-advances on every
commit; never `git commit` / `git push` — use
`jj git push --remote origin --bookmark main`. Full workflow:
`docs/jj-workflow.md`.

## 9. Factory port start

When, and only when, the user's trimmed message is exactly `start`
(case-sensitive), immediately read and execute `docs/factory-workflow.md`.
`/start`, `Start`, `start <issue>`, and prose containing `start` follow normal
request handling.

The factory model: deterministic tooling under `tools/factory/` builds
self-contained packets from open `port-ready` Forgejo issues, stateless
small-model translators fill them in disposable lanes, the oracle plus mutation
harness accepts or rejects mechanically, and one serial integrator — the
orchestrator — owns every repo and Forgejo-origin write, gating strictly before
each push. Lanes never run jj, git, or a central gate and receive no remote
credentials. Translation prompts are governed by `docs/factory-contract.md`.

## 10. `tests/cases/*.py` are not unit tests


They are the oracle's input matrix — the thing that makes the port provable. The
ambient house rule says never write unit tests; it does not apply here. An agent
that thins or deletes `tests/cases/*.py` under that rule destroys the
verification substrate this whole repo is built on.
