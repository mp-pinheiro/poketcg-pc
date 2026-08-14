# docs/

Reading order for porting work: `vision.md` → `port-contract.md` → `plan.md`.
Factory orchestration then uses `factory-workflow.md`; translator lanes use
`factory-contract.md`. Repository writes follow `jj-workflow.md`.

- `vision.md` — architecture and phase order. Descriptive: the plan of record
  for what the port becomes, updated at each phase boundary. Not normative.
- `port-contract.md` — the porting contract. Memory model, the three C rules,
  adapter rules, required case coverage, mutation testing, exclusion
  taxonomy. **Normative** — read in full before writing any C.
- `plan.md` — the live execution plan for the wave currently in flight: slice
  breakdown, ownership, barrier checks, per-slice status table.
- `phase1-transform.md` — the per-routine delete/dissolve/port verdicts for
  the hardware-removal transform (Phase 1 / #2).
- `jj-workflow.md` — the jj + git VCS workflow this repo enforces.
- `factory-workflow.md` — Forgejo-backed packet selection, disposable lanes,
  serial integration, and the commands used by an orchestrator session.
- `factory-contract.md` — the C, probe, case, and output contract given to a
  stateless translator lane.

`docs/port-contract.md` is normative; `docs/vision.md` is descriptive.
