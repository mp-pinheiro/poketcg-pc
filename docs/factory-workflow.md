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
import sys, subprocess, json
sys.path.insert(0, "tools/factory")
from driver import run_wave

def translate_many(prompts):                     # translation MUST be one
    return parallel([(lambda p=p: completion(p, model="default"))
                     for p in prompts])          # parallel() batch per round

def build(limit=8, extra=()):
    argv = ["python3", "tools/factory/packet.py", "build", "--max-routines", "3",
            "--max-asm-lines", "140", "--limit", str(limit), "--json", *extra]
    return json.loads(subprocess.run(argv, capture_output=True, text=True,
                                     check=True).stdout)

pending = build()
while pending:
    wave = run_wave(pending, translate_many, lanes_count=10, max_rounds=3,
                    model="default")
    subprocess.run(["python3", "tools/factory/integrate.py"], check=False)
    # deferred packets need a landed tip; re-run them after integrating
    pending = wave["deferred"] or build()
```

`run_wave` returns `{"results": [...], "deferred": [ids]}`. **Deferred ids are
not optional to handle** — a second packet of the same basename is skipped
until the first lands, and dropping them silently strands work. The loop above
re-runs them after `integrate.py`.

Serial, in the repo root:

```sh
python3 tools/factory/integrate.py            # land greens, gate, push
python3 tools/factory/issues.py sync          # close fully-landed issues
python3 tools/factory/driver.py metrics       # token/wall/round telemetry
python3 tools/factory/driver.py status        # queue state incl. deferred
```

`integrate.py` runs the adapter lint, the full GBRT inventory gate (~12 s), and
the schema audit BEFORE any push; a red stops the line. Run
`just oracle-release-gate` (adds the full PyBoy audit sweep and the data
round-trip) at session start and session end.

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

## Pilot calibration (measured 2026-08-12)

| configuration | packets | green | tokens/routine | notes |
|---|---|---|---|---|
| smol, 8 routines/packet | 8 | 0 | ~4.4k | all-or-nothing gate over 8 routines is fatal |
| smol, 3 routines/packet | 8 | 3 (38%) | ~6.8k | 2 of the 3 were partial salvage |
| default, 3 routines/packet | 3 | 2 (67%) | ~8.3k | frontier guard + compile-cause feedback active |

Production configuration: `--max-routines 3`, `model="default"`, `max_rounds=3`,
`lanes_count=10`. Waves run ~5 min wall regardless of lane count because
translation is one `parallel()` batch per round.

Calibration findings worth keeping:
- Packet size dominates. A packet is green only when every routine in it is
  green, so success decays as p^n; 3 is the working size.
- Partial salvage matters: escalating packets still land their passing
  routines and spill the failures into `<id>-rest`.
- Every early wave failure was a packet-content gap, not model weakness:
  missing RAM symbol addresses, unparsed `const_def`/`DEF..EQU` constants,
  missing struct typedefs for struct-returning callees, invented include
  paths, and ninja's link-command echo crowding out the real compile cause.

**Push cadence note.** The release workflow appends a `chore(release): vX.Y.Z`
commit to `main` after every push, so the next local commit is a sibling of a
tip you have not seen. `integrate.py` push failures of the form "Failed to push
some bookmarks" mean exactly this: `jj git fetch`, `jj rebase -s <your first
commit> -d main@origin`, `jj bookmark set main -r <new head>`, push again.
