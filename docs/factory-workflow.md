# Factory workflow

The execution contract for an orchestrator session triggered by the exact
message `start`. It replaces the retired per-issue claim/PR/merge protocol:
workers are stateless translators with zero VCS or GitHub access; all trust
comes from the oracle plus mutation testing; one serial integrator owns every
repo, jj, and GitHub write.

```
frontier -> packets -> [N lanes: translate -> surgery -> verify -> repair<=4]
        -> green bundles -> serial integrate (gate BEFORE push) -> repeat
```

## Roles

- **Orchestrator (this session):** runs the loop below, wires the translator,
  handles escalations. The only jj/GitHub writer, via `integrate.py`/`issues.py`.
- **Lanes:** disposable directory copies under `/tmp/poketcg-factory/lane-N`
  (no `.jj`, no `.git`). Refreshed from the repo tip per packet; builds stay
  incremental. Nothing a lane does can corrupt the repo.
- **Translator:** a stateless `prompt -> tagged blocks` function. Default:
  the session's `completion(prompt, model="smol")`. Swapping models or
  backends is a one-line change at the call site.

## Preflight

1. `jj git fetch`; require `main` == `main@origin` and a clean working copy
   (`jj new main` if the working copy is stale/empty-on-old-base).
2. Prerequisites: `poketcg/poketcg.gbc` + `.sym` (`just bootstrap`),
   `/tmp/pbenv` (`just oracle-venv`), `tools/oracle/gbref/build/gbref_runner`
   (`just oracle-build-gbref`), warm `build-barrier` (`just build-barrier`).
3. Resume state: `python3 tools/factory/driver.py reset-stale` returns
   crashed in-flight packets to `pending`; `driver.py status` shows the queue.

## The loop

```python
# eval-kernel wiring inside the orchestrator session
import sys; sys.path.insert(0, "tools/factory")
import subprocess, json
from driver import run_wave

ids = json.loads(subprocess.run(
    ["python3", "tools/factory/packet.py", "build", "--limit", "16", "--json"],
    capture_output=True, text=True, check=True).stdout)
run_wave(ids, lambda p: completion(p, model="smol"), lanes_count=8, model="smol")
```

Then, serially, in the repo root:

```sh
python3 tools/factory/integrate.py            # land greens, gate, push
python3 tools/factory/issues.py sync          # close fully-landed issues
python3 tools/factory/driver.py metrics       # token/wall/round telemetry
```

Repeat `packet build -> run_wave -> integrate` until the frontier is empty;
landing routines widens the next frontier. `integrate.py` runs the adapter
lint, the full GBRT inventory gate (~12 s), and the schema audit BEFORE any
push; a red stops the line. Run `just oracle-release-gate` (adds the full
PyBoy audit sweep and the data round-trip) at session start and session end.

## Escalation lane

- `escalated` packets (4 failed repair rounds, surgery refusal, or format
  rejection) go to agentic `task` subagents — default model, one packet per
  agent, confined to the packet's four files inside a lane, no VCS, the full
  verdict history in the brief. Their green bundles enter the same
  `integrate.py` queue; nothing ships weaker than the mechanical bar.
- `parked` packets hit a real dependency wall (oracle timeout: a callee never
  returns — e.g. the script VM). They are recorded in `.factory/blocked.toml`
  with an unblock condition and stop being offered by `packet.py`. Clear the
  entry when the blocker lands.
- Harness gaps (a missing case key, an oracle limitation) are orchestrator
  work on shared files — never delegated, never worked around in a packet.

## Milestones that unlock frontier mass

1. Finish Phase-3 audio (`src/audio`, 50/75) — unblocks every
   `PlaySFX`/`PlaySong` dependent across menus and duel.
2. Script-VM interpreter core — unblocks `src/scripts` (1,927 B), the parked
   salvage bundles (mason_laboratory, specs2), and every `Script_*` routine.
3. Duel pointer-table hubs (`jp hl` tails) — become C function-pointer tables
   once their targets land; until then their targets dominate the frontier.

## Retired paths

`docs/autonomous-port-workflow.md` (issue claims, per-issue bookmarks, PRs,
CI watching, merge tokens) is deleted. `just launch-port` and
`.github/copilot-instructions.md` are deprecated dead paths, kept untouched.
GitHub issues are a reporting mirror closed in batch by `issues.py sync`;
nothing dispatches from them, nothing claims them, no new ones are generated.

## Invariants

- Lanes never run jj, git, gh, or any central gate.
- The integrator gates strictly before pushing; a red gate stops the line.
- `tests/routines.py` is derived from case modules — never hand-edited.
- Every landed routine carries live-oracle PASS and a mutation receipt.
- `jj bookmark list` shows exactly one bookmark: `main`.
