# Factory workflow

The runbook for an orchestrator session. The exact message `start` triggers this
file and nothing else.

```
frontier -> packets -> [N lanes: translate -> surgery -> verify -> repair<=3]
        -> green bundles -> serial integrate (gate BEFORE push) -> reconcile -> repeat
```

Roles: **orchestrator** (this session) owns every repo, jj, and Forgejo write, and
is the only session that runs a central gate. **Lanes** are disposable directory
copies under `/tmp/poketcg-factory/lane-N` with no `.jj`, no `.git`, and no
credentials. **Translator** is a stateless `prompt -> tagged blocks` function;
production uses `completion(prompt, model="default")`.

## 1. Preflight

Run in order. Every step is a hard gate — do not proceed past a failure.

```sh
just forgejo-auth-check                        # credentials, non-interactive
jj git fetch --remote origin                   # then require main == main@origin
just bootstrap                                 # poketcg/poketcg.gbc + .sym
just oracle-venv                               # /tmp/pbenv
just oracle-build-gbref                        # tools/oracle/gbref/build/gbref_runner
just build-barrier                             # warm central build
just issues-fetch                              # schema-2 Forgejo cache
python3 tools/factory/driver.py reset-stale     # crashed in-flight -> pending
python3 tools/factory/driver.py status          # queue state
```

A stale working copy is the one case needing judgement: `jj new main` if `@` is
empty on an old base.

`packet.py build` refuses to run without a fresh issue cache, so `issues-fetch`
is enforced by code, not by memory.

## 2. The loop

```python
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

Bundles are composable (`surgery.extract`/`apply`, additive per-routine
fragments), so two packets of the same basename can run in one wave and both
land. The loop just rebuilds the frontier each iteration — no deferral
bookkeeping.

`integrate.py` lands green bundles FIFO, then runs adapter lint, the constant
audit, `just oracle-release-gate`, and a progress rebuild before pushing. A red
gate stops the push.

## 3. Reconcile Forgejo

Forgejo issue labels and open/closed state are the dispatch inputs for the next
cycle, so this is part of the loop, not an afterthought. Skipping it silently
starves packet construction: routines already ported keep their `port-active`
label and are never re-offered, while the dashboard under-reports progress.

```sh
just issues-fetch          # refresh the cache
just issues-sync           # dry run: what would change
just issues-sync-apply     # apply it
just issues-verify         # marker coverage
```

`issues-sync` refuses to run when a gate input (`src/`, `tests/`, `include/`,
`tools/oracle/`, `CMakeLists.txt`, `poketcg/`) changed after the last gate — a
stale gate would let it close an issue whose routine is no longer passing. Fix by
re-running `just oracle-release-gate && just progress`.

`--apply` is the only switch that writes to Forgejo. It self-verifies by
re-fetching and re-planning; a non-empty residual plan is an error.

## 4. Escalation

| state | meaning | action |
|---|---|---|
| `escalated` | hit the repair limit or failed translation | `driver.py escalate` writes task briefs; integration ignores it until an explicit state change |
| `rejected-format` | failed the initial parse and one free reformat | terminal; not re-offered |
| `parked` | timed out behind a dependency | adds the routine to `.factory/blocked.toml`; no reset command exists |

Harness gaps — a missing case key, an oracle limitation — are orchestrator work
on shared files. Never delegate them into a packet or work around them there.

## 5. Invariants

- Lanes never run jj, git, or a central gate, and hold no credentials.
- `site/data/gate.json` has exactly one producer: `just oracle-fn-all`, via the
  release-gate chain. `just oracle-diff-all` deliberately writes no gate record —
  it may run against a slice-private build.
- The integrator gates before every push; a red gate stops the push.
- `integrate.py` aborts when `main@origin` holds commits absent from local `main`
  (usually a release bot) and never rebases automatically.
- A managed issue carries exactly one valid `port:v1:<source>:<symbol>` marker.
  Packet identity and claim dedup use that work ID, never mutable titles.
- One work ID cannot be claimed by two non-terminal packets.
- Packet construction consumes only open `port-ready` issues.
- `tests/routines.py` is derived from `tests/cases/*.py` `CONTRACT` keys at import
  time. Never hand-edit it. `SCHEMA2_CASES` is likewise generated by `surgery.py`.
- Every landed routine carries a live-oracle PASS and a mutation receipt.

## 6. Calibration (measured 2026-08-12)

Production config: `--max-routines 3`, `model="default"`, `max_rounds=3`,
`lanes_count=10`. Waves run ~5 min wall regardless of lane count, because
translation is one `parallel()` batch per round.

Packet size dominates: a packet is green only when every routine in it is green,
so success decays as p^n. Measured 8 routines/packet → 0 green; 3/packet → 67%
green on `model="default"`. Escalating packets still land their passing routines
and spill failures into `<id>-rest`.

Early wave failures were packet-content gaps, not model weakness: missing RAM
symbol addresses, unparsed `const_def`/`DEF..EQU` constants, missing struct
typedefs for struct-returning callees, invented include paths, and ninja's
link-command echo crowding out the real compile cause.

## Notes

One-time, for a queue predating persisted work identity:
`python3 tools/factory/packet.py migrate-work-ids` (read-only), then
`--apply`. Require a zero-change dry run before dispatching.

Factory pushes target Forgejo `origin`. `github-mirror` is a checkout-local
remote, not a server-side mirror, so GitHub does not receive factory pushes.
`.github/workflows/release.yml` and `progress.yml` push to GitHub directly, which
is why `integrate.py`'s fast-forward check can see origin advance.
