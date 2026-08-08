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
2. `docs/vision.md` — architecture and phase order. Descriptive.
3. `docs/plan.md` — what is being worked on right now, and by which slice.

## 3. Commands

The six that matter, from the `justfile`:

| command | what |
|---|---|
| `just bootstrap` | clone + build the disassembly (one-time) |
| `just oracle-venv` | PyBoy into `/tmp/pbenv` (one-time) |
| `just build` | configure + build the C side |
| `just oracle-diff <Fn>` | diff one routine's C port against the PyBoy oracle |
| `just oracle-diff-all` | the gate — every registered routine, also runs `lint-adapters` |
| `just data-verify` | data/asset extraction round-trip |
| `just oracleb-replay` | replay-determinism half of the gb-recompiled oracle |

## 4. Concurrency protocol

Each concurrent agent owns a private build directory and a private file subset:

```sh
export POKETCG_BUILD=build-<slice>
export POKETCG_PORTS="<pret basenames>"   # semicolon list; see CMakeLists.txt:34-60
```

Agents **never** run `just oracle-diff-all`. A routine registered in
`tests/routines.py` without cases is a hard FAIL for everyone, so only the
barrier — run centrally, after every slice lands — runs the full gate.

## 5. File ownership

Four files per pret source: `src/home/<f>.c`, `src/home/<f>.h`, `src/probe/<f>.c`,
`tests/cases/<f>.py`.

Shared, not owned by any slice: `CMakeLists.txt`, `src/mem.*`, `src/probe.c`,
`src/probe.h`, `src/probe_table.c`, `tests/test_leaves.py`, `tools/`, `justfile`.

`tests/routines.py` is shared but **partitioned** — a slice edits only its own
`ROUTINES["<basename>"]` tuple, never a neighbouring entry.

## 6. Definition of done

- `just oracle-diff <Fn>` prints `PASS`.
- Required case coverage exists (`docs/port-contract.md`): an all-zero case, a
  poisoned-register case, every boundary.
- A **recorded mutation test**: corrupt the routine, confirm the diff goes RED,
  restore, confirm PASS.
- An input-waiting routine (drives `ReadJoypad`/`hKeysHeld`) is tested by passing
  `keys` in its case — see `docs/port-contract.md`'s case-key reference.
- No stubs, no `TODO`, no dead routines, no changes outside the four owned files.

## 7. VCS

jj only — git writes are hook-blocked (`.claude/hooks/enforce-jj.sh`). Commit with

```sh
jj commit -m "type(scope): subject"
```

≤50-char subject, no body, no emoji, no bullet lists
(`.claude/hooks/enforce-conventional-commits.sh`). `main` auto-advances on every
commit; never `git commit` / `git push` — use `jj git push`. Full workflow:
`docs/jj-workflow.md`.

## 8. `tests/cases/*.py` are not unit tests

They are the oracle's input matrix — the thing that makes the port provable. The
ambient house rule says never write unit tests; it does not apply here. An agent
that thins or deletes `tests/cases/*.py` under that rule destroys the
verification substrate this whole repo is built on.
