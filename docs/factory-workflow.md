# Factory workflow

The execution contract for an orchestrator session triggered by the exact
message `start`. It replaces the retired per-issue claim/PR/merge protocol:
workers are stateless translators with zero VCS or Forgejo access; all trust
comes from the oracle plus mutation testing; one serial integrator owns every
repo and jj write.

```
frontier -> packets -> [N lanes: translate -> surgery -> verify -> repair<=4]
        -> green bundles -> serial integrate (gate BEFORE push) -> repeat
```

## Roles

- **Orchestrator (this session):** runs the loop below, wires the translator,
  handles escalations, refreshes the read-only Forgejo issue cache, and integrates.
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
3. Issue inventory: `python3 tools/factory/issues.py fetch` must produce a
   schema-2 Forgejo cache before packet construction.
   The default endpoint is `https://forgejo.yfrit.com` and the default token
   file is `~/.config/yfrit-forgejo/api/poketcg-issues.token`; override them
   with `POKETCG_FORGEJO_URL` and `POKETCG_FORGEJO_TOKEN_FILE`. The token needs
   only `read:issue`. Direct requests through Cloudflare Access also accept
   `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET`.
4. Resume state: `python3 tools/factory/driver.py reset-stale` returns
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

def build(limit=16, extra=()):
    argv = ["python3", "tools/factory/packet.py", "build", "--max-routines", "3",
            "--max-asm-lines", "140", "--limit", str(limit), "--json", *extra]
    return json.loads(subprocess.run(argv, capture_output=True, text=True,
                                     check=True).stdout)

pending = build()
while pending:
    wave = run_wave(pending, translate_many, lanes_count=10, max_rounds=3,
                    model="default")
    subprocess.run(["python3", "tools/factory/integrate.py"], check=False)
    pending = build()
```

`run_wave` returns `{"results": [...]}`. Bundles are composable
(`surgery.extract`/`apply`, additive per-routine fragments): two packets of
the same basename may run in the same wave and both land without one
overwriting the other, so the loop simply rebuilds the frontier each
iteration — no deferral bookkeeping needed.

Serial, in the repo root:

```sh
python3 tools/factory/integrate.py            # land greens, release gate
python3 tools/factory/issues.py fetch         # read every Forgejo issue page
python3 tools/factory/issues.py plan --json  # deterministic drift audit
python3 tools/factory/issues.py verify --live # refetch and verify full coverage
python3 tools/factory/driver.py metrics       # token/wall/round telemetry
python3 tools/factory/driver.py status        # queue state
```

Forgejo is the operational issue authority. `issues.py fetch` reads every
repository issue through the paginated Forgejo API, normalizes issue number,
title, body, state, labels, and URL, validates unique routine markers and full
canonical coverage, then atomically replaces `.factory/issues-cache.json`.
Packet construction refuses a missing, stale-backend, or malformed cache and
dispatches only open issues carrying `port-ready`.

`issues.py plan` is a read-only semantic comparison against the progress model;
it may report differences that operators intentionally manage in Forgejo.
`issues.py verify --live` refetches Forgejo and requires complete, unique
canonical coverage. There is no issue apply or migration command and integration
never mutates issue state. Human and agent lifecycle decisions happen in
Forgejo; the release gate remains the authority for whether a routine is
actually verified.

Repository pushes go to the Forgejo `origin`. Forgejo's push mirror replicates
Git refs to GitHub; GitHub issues and Actions are not part of factory dispatch.
Translator lanes receive neither Forgejo nor GitHub credentials.

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
CI watching, merge tokens) is deleted. `just launch-port` remains only as a
compatibility hint for packet dispatch.

Forgejo issues are keyed by `port:v1:<source>:<symbol>` and are the operational
source for dispatch. GitHub receives mirrored Git refs only. The completed
legacy backfill is not replayed by repository tooling.

## Invariants

- Lanes never run jj, git, or any central gate and receive no remote credentials.
- The integrator runs one release gate per batch before pushing to Forgejo; a
  red gate stops the push.
- Every managed routine has exactly one issue, tier, and lifecycle state.
- Packet batching may contain several atomic issue IDs, but one work ID cannot
  be claimed by two non-terminal packets.
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
