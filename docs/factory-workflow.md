# Factory workflow

The execution contract for an orchestrator session triggered by the exact
message `start`. It replaces the retired per-issue claim/PR/merge protocol:
workers are stateless translators with zero VCS or Forgejo access; all trust
comes from the oracle plus mutation testing; one serial integrator owns every
repo and jj write.

```
frontier -> packets -> [N lanes: translate -> surgery -> verify -> repair<=max_rounds]
        -> green bundles -> serial integrate (gate BEFORE push) -> repeat
```

## Roles

- **Orchestrator (this session):** runs the loop below, wires the translator,
  handles escalations, refreshes the read-only Forgejo issue cache, and integrates.
- **Lanes:** disposable directory copies under `/tmp/poketcg-factory/lane-N`
  (no `.jj`, no `.git`). Refreshed from the repo tip per packet; builds stay
  incremental. Nothing a lane does can corrupt the repo.
- **Translator:** a stateless `prompt -> tagged blocks` function supplied by
  the orchestrator. The production loop below uses
  `completion(prompt, model="default")`.

## Preflight

1. `jj git fetch --remote origin`; require `main` == `main@origin` and a clean
   working copy (`jj new main` if the working copy is stale/empty-on-old-base).
2. Prerequisites: `poketcg/poketcg.gbc` + `.sym` (`just bootstrap`),
   `/tmp/pbenv` (`just oracle-venv`), `tools/oracle/gbref/build/gbref_runner`
   (`just oracle-build-gbref`), warm `build-barrier` (`just build-barrier`).
3. Issue inventory: `just issues-fetch` must produce a schema-2 Forgejo cache
   before packet construction. The defaults are
   `https://forgejo.yfrit.com`, repository `mpp/poketcg-pc`, and token file
   `~/.config/yfrit-forgejo/api/poketcg-issues.token`.
   `POKETCG_FORGEJO_URL` and `POKETCG_FORGEJO_TOKEN_FILE` override the endpoint
   and credential for both audit and dispatch. `POKETCG_FORGEJO_OWNER` and
   `POKETCG_FORGEJO_REPO` affect the issue client only; packet consumption still
   requires cache repository `mpp/poketcg-pc`. The token file accepts a raw
   token, `token ...`, `bearer ...`, or an `Authorization:`-prefixed value.
   `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET` add Cloudflare Access
   headers and must be set together; they do not replace the Forgejo token.
   These credentials cover the issue REST client only. Git and jj authenticate
   to Forgejo through the host-scoped `git-credential-oauth` configuration in
   `docs/jj-workflow.md`.
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
python3 tools/factory/integrate.py             # land greens, gate, push origin
just issues-fetch                             # replace the stable Forgejo cache
just issues-plan                              # write the desired-state audit
just issues-verify                            # refetch and verify marker coverage
python3 tools/factory/driver.py metrics        # token/wall/round telemetry
python3 tools/factory/driver.py status         # queue state
```

Forgejo is the operational issue authority. `issues-fetch` requests open and
closed issues in 50-item pages until the final short page, requires two
consecutive listings with the same semantic fingerprint, validates unique
routine markers and full non-excluded canonical coverage, then atomically
replaces `.factory/issues-cache.json`. Unmarked issues remain outside the
managed routine set. Packet construction refuses a missing, wrong-backend, or
malformed cache and dispatches only ready routines whose managed issue is open
and labeled `port-ready`.

`issues-plan` compares the cache with the progress work-record projection,
writes `.factory/issues-plan.json`, and reports create, update, and explicit
work-ID migration actions without applying them. `issues-verify` refetches
Forgejo and checks complete, unique marker coverage; it does not require zero
desired-state drift. No repository command mutates issue titles, bodies, labels,
or state, and integration does not refresh issue lifecycle state.

Forgejo labels and open/closed state are the operational dispatch inputs.
`report.py` and a trusted release gate derive the desired semantic lifecycle
(`complete`, `failing`, `awaiting-gate`, `active`, `blocked`, or `ready`).
Packet construction intersects both sources: a routine must be locally ready
and have an open Forgejo issue labeled `port-ready`.

Remote reconciliation is manual:

1. Run `just issues-fetch`, then `just issues-plan`.
2. Inspect `.factory/issues-plan.json`.
3. Apply its title, body, label, state, or explicit work-ID changes in Forgejo.
4. Fetch and plan again; reconciliation is complete when the plan has zero
   actions.

`just issues-verify` is not the final step of this procedure: it checks marker
coverage, not desired-state drift.

Factory pushes target the Forgejo `origin`; translator lanes receive no remote
credentials. `github-mirror` is a checkout-local GitHub remote name, not proof
of a Forgejo server-side mirror, and the live Forgejo API currently reports no
configured push mirror. GitHub therefore does not automatically receive factory
pushes from Forgejo.

GitHub still has direct ref writers: `.github/workflows/release.yml` pushes its
generated release commit and tag, while `.github/workflows/progress.yml` pushes
its daily progress commit. The GitHub CI workflow validates the progress report
and managed issue model offline, without fetching Forgejo or dispatching
packets.

## Escalation lane

- `escalated` packets reach the configured repair limit or fail translation.
  `python3 tools/factory/driver.py escalate` writes agentic task briefs only for
  packets in that state. A separately verified escalation writes a bundle but
  leaves the packet terminal; `integrate.py` selects only `green`, so the
  escalation cannot integrate without an explicit state transition.
- `rejected-format` packets fail both the initial parse and one free reformat
  attempt. They are terminal and are not selected by `driver.py escalate`.
- `parked` packets time out behind a dependency and add that routine to
  `.factory/blocked.toml`. Removing the blocker entry alone does not reoffer the
  packet: `reset-stale` ignores `parked`, and packet construction skips its
  existing terminal queue entry. There is no dedicated parked-reset command.
- Harness gaps (a missing case key, an oracle limitation) are orchestrator
  work on shared files — never delegated or worked around in a packet.

## Milestones that unlock frontier mass

1. Finish Phase-3 audio (`src/audio`, 50/75) — unblocks every
   `PlaySFX`/`PlaySong` dependent across menus and duel.
2. Script-VM interpreter core — unblocks `src/scripts` (1,927 B), the parked
   salvage bundles (mason_laboratory, specs2), and every `Script_*` routine.
3. Duel pointer-table hubs (`jp hl` tails) — become C function-pointer tables
   once their targets land; until then their targets dominate the frontier.

## Retired paths

The former issue-claim workflow (per-issue bookmarks, PRs, CI watching, and
merge tokens) is deleted. `just launch-port` prints the packet dispatch command,
while `just generate-port-issues` is a compatibility name for the read-only
desired-state plan. The old title/group generator and remote migration writer
no longer exist.

Forgejo issues are keyed by `port:v1:<source>:<symbol>`. Packet identity and
claim deduplication use that immutable work ID rather than mutable issue titles.

## Invariants

- Lanes never run jj, git, or any central gate and receive no remote credentials.
- The integrator runs the release gate before each batch push; a red gate stops
  the push.
- A fetched managed issue has exactly one valid `port:v1` marker, and duplicate
  work IDs are rejected.
- Coverage requires an issue for every non-excluded canonical work record and
  rejects marked IDs outside the current projection.
- Packet batching may contain several issue numbers, but one work ID cannot be
  claimed by two non-terminal packets.
- Packet construction consumes only open `port-ready` issues; integration never
  mutates their Forgejo lifecycle.
- `tests/routines.py` is derived from case modules and is never hand-edited.
- Every landed routine carries live-oracle PASS and a mutation receipt.

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

Before every batch push, `integrate.py` fetches and aborts when `main@origin`
contains commits absent from local `main`; it does not rebase automatically.
That guard reads the Forgejo `origin`, not `github-mirror`, so commits created
directly by the GitHub release or progress workflows are outside this
fast-forward check.
