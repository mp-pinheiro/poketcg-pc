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
uv sync --project tools/oracle --frozen        # pinned PyBoy oracle environment
just oracle-build-gbref                        # tools/oracle/gbref/build/gbref_runner
just build-barrier                             # warm central build
just issues-fetch                              # schema-2 Forgejo cache
python3 tools/factory/driver.py reset-stale     # crashed in-flight -> pending
python3 tools/factory/driver.py reset-infra     # harness-failed escalations -> pending
python3 tools/factory/integrate.py                 # checked recovery integration
python3 tools/factory/driver.py status          # queue state
```

A stale working copy is the one case needing judgement: `jj new main` if `@` is
empty on an old base.

`packet.py build` refuses to run without a fresh issue cache, so `issues-fetch`
is enforced by code, not by memory.

## 2. The loop
```python
import re, sys, subprocess, json, time
sys.path.insert(0, "tools/factory")
from driver import run_wave

def one(prompt):
    for attempt in range(3):
        try:
            return completion(prompt, model="default")
        except Exception as exc:
            message = str(exc)
            if attempt == 2 or not ("429" in message or "rate_limit" in message):
                raise
            delay = re.search(r"retry-after-ms=(\d+)", message)
            time.sleep(min(float(delay.group(1)) / 1000 if delay else 5.0, 15) + attempt * 2)

def translate_many(prompts):
    replies = []
    for start in range(0, len(prompts), 10):
        replies.extend(parallel([
            (lambda p=p: one(p)) for p in prompts[start:start + 10]
        ]))
    return replies

def build(limit=20, extra=()):
    argv = ["python3", "tools/factory/packet.py", "build", "--max-routines", "3",
            "--max-asm-lines", "140", "--limit", str(limit), "--json", *extra]
    return json.loads(subprocess.run(argv, capture_output=True, text=True,
                                     check=True).stdout)

subprocess.run(["python3", "tools/factory/integrate.py"], check=True)
pending = build()
while pending:
    wave = run_wave(
        pending, translate_many, lanes_count=10, verify_width=6, max_rounds=3,
        model="default", max_wall_s=3600,
        on_event=lambda event: print(json.dumps(event), flush=True),
    )
    print(json.dumps(wave), flush=True)
    subprocess.run(["python3", "tools/factory/integrate.py"], check=True)
    if wave["status"] != "complete":
        break
    pending = build()
```

A wave's cohort may exceed `lanes_count`: the first `lanes_count` packets are
admitted immediately, the rest stay `pending` on disk and are pulled into a lane
as soon as one frees up (`refill` events). `max_wall_s` is 3600 because a
refilled wave of 20 packets across 10 lanes runs roughly twice as long as the
old fixed cohort of 10 — it is a safety bound, not the expected duration.
`integrate.py` touches jj, git, and the gate; it must never run while a wave
holds `.factory/wave.lock` — only between waves, as above.

Bundles are composable (`surgery.extract`/`apply`, additive per-routine
fragments), so two packets of the same basename can run in one wave and both
land. A returned `deadline` or `stopped` wave is a clean partial return; the
outer loop stops instead of retrying an outage.

A lane runs the central comparator (`compare_one.py`) over every case in the
packet before the PyBoy lane, so `oracle-fn-all` cannot reject what a packet
already landed. `run_mutation` covers only the witness case.

`integrate.py` lands green bundles FIFO, then runs adapter lint, the constant
audit, `just oracle-release-gate`, and a progress rebuild before pushing. A red
gate stops the push.

Translation and verification run inside one continuous scheduler, not
alternating phases: a packet whose lane is free and whose translation parsed
is submitted for verification immediately, while the next translate batch is
forming from whichever other packets are ready. `python3 tools/factory/driver.py
progress` inspects a live wave (per-packet state, round, phase, time-in-phase)
without taking `.factory/wave.lock`.

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
| `escalated` | hit the repair limit, repeated one verdict verbatim, or failed translation | `driver.py escalate` writes task briefs; integration ignores it until an explicit state change |
| `rejected-format` | failed the initial parse and one free reformat | terminal; not re-offered |
| `parked` | timed out behind a dependency | adds the routine to `.factory/blocked.toml`; no reset command exists |

Harness gaps — a missing case key, an oracle limitation — are orchestrator work
on shared files. Never delegate them into a packet or work around them there.

## 5. Invariants

- Lanes never run jj, git, or a central gate, and hold no credentials. Only the
  scheduler thread inside `run_wave` reads or mutates packet state; pool jobs
  (lane provisioning, verification, salvage) are pure functions of their
  arguments and return values only.
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
- `.factory/blocked.toml` is the one tracked factory file: `site/data/progress.json`
  embeds its entries, so a park must reach git together with a progress rebuild
  or CI's `report.py check` goes red.

## 6. Calibration

Production config: `build(limit=20)`, `model="default"`, `max_rounds=3`,
`lanes_count=10`, `verify_width=6`, and `max_wall_s=3600`. A wave admits ten
packets immediately and refills from the rest as lanes free up; factory
subprocess work shares the wall-clock deadline. The synchronous harness
callback remains cooperative and may exceed that bound until its provider
request returns.

Translate and verify run in one continuous scheduler, not alternating phases: a
packet whose translation parsed is submitted for verification as soon as a lane
and a verify slot are free, and finished packets' lanes are refilled from the
queued remainder instead of idling until the wave ends.

**The provider is the only bottleneck that matters.** Wave `a4745708` (14
packets, completed) measured `translate 60% verify 2% salvage 0% lane 0%
idle 38%` of packet-time, with `/proc/loadavg` between 0.18 and 2.17 (median
0.46) on 8 CPUs. Verification is seconds; translation is minutes. Two
consequences:

- `verify_width` is not a throughput lever at these ratios. It defaults to
  `cpu_count() - 2` only to stop ten concurrent verifies oversubscribing 8
  cores (lane builds run `ninja -j2`; `compare_one.py`, `test_leaves.py`,
  `gbref_runner`, and PyBoy are each single-threaded). Raising it buys nothing
  while verify is 2% of the work.
- **Translate batch width is the lever.** Continuous dispatch initially issued a
  batch the instant any one packet was ready, fragmenting wave `a4745708` into
  widths `10,1,6,4,6,3,3,1,3,1,3` (mean 3.7) where even a width-1 call cost
  24-48 s — about 1183 s of that 1196 s wave was translation. `_decide`'s cheap
  verdicts are therefore drained before a batch is issued
  (`TRANSLATE_COALESCE_S`, 45 s cap so one slow verify cannot stall the batch),
  which restored widths `10,10` (mean 10.0) on the next wave.

`translate_many` runs only on the scheduler thread, blocking it; verify and
salvage jobs keep running in the pool throughout. A worker-thread probe
confirmed the harness completion bridge is not thread-safe outside its calling
thread (`RuntimeError: Missing session/run/name`), so translation cannot move
onto the pool without a session-context bridge that does not exist yet.

Phase timings come from `.factory/events.jsonl` (per-packet `verify-phase`
records written by the verify subprocess) and the per-packet `translate_s`,
`verify_s`, `salvage_s`, `lane_s`, and `idle_s` fields in `.factory/metrics.jsonl`;
`driver.py metrics` prints the split and `driver.py progress` reports a live
wave. Job durations are measured inside each job, not at harvest, because the
scheduler can block in `translate_many` long after a job finished.

Translate all ten prompts in one `parallel()` wave: measured 107-123 s per round
at width 10 against ~170 s as two batches of five, with no rate limiting, which
took a 3-round wave from 604 s to 377 s. A packet that returns a byte-identical
verdict two rounds running is not reading its feedback, so `_decide` salvages or
escalates it there instead of buying two more translations: measured 4 of 10
packets in one wave, and no packet that ever repeated verbatim went on to green.

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
