# Context pack

## Goal
Finish the Extended profile port for LaneCore basenames core, duel_core, and duel_init in order, matching Extended assembly with oracle cases, probes, contracts, and mutation coverage.

## Files in scope
- `src/profiles/extended/home/core.c` - port core and AI core routines.
- `src/profiles/extended/home/core.h` - align core declarations.
- `src/profiles/extended/probe/core.c` - marshal core probe routines.
- `tests/profiles/extended/cases/core.py` - rewrite Extended core cases and mutations.
- `src/profiles/extended/home/duel_core.c` - port synthetic duel_core routines.
- `src/profiles/extended/home/duel_core.h` - align duel_core declarations.
- `src/profiles/extended/probe/duel_core.c` - marshal duel_core routines.
- `tests/profiles/extended/cases/duel_core.py` - rewrite duel_core cases and mutations.
- `src/profiles/extended/home/duel_init.c` - port duel initialization routines.
- `src/profiles/extended/home/duel_init.h` - align duel_init declarations.
- `src/profiles/extended/probe/duel_init.c` - marshal duel_init routines.
- `tests/profiles/extended/cases/duel_init.py` - rewrite duel_init cases and mutations.

## Contracts
- `docs/factory-contract.md` requires bus-only memory access, exact register contracts, numeric case addresses, POISON and boundary coverage, and exact mutation substrings.
- Extended assembly under `poketcg-extended/src` is authoritative; use `python3 tools/profile_audit.py --routines <basename>` before each basename.
- Setup uses `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneCore POKETCG_NINJA_JOBS=-j2`, then `just extended-configure-lane` and `just build-extended-incremental`.
- Each basename requires `just extended-check <basename>`, `lint_constants`, `lint_adapters`, and `audit_oracle_cases --only <basename>`.
- Every changed C body requires `run_mutation.py` with the LaneCore build.

## Pattern to copy
Use the existing factory blocks and probe adapters in `src/profiles/extended/home/core.c`, `src/profiles/extended/probe/core.c`, and `tests/profiles/extended/cases/core.py`, with generated headers for all symbols.

## Non-goals
Do not edit shared sources, tooling, build files, vanilla cases, or another lane's overlays. Do not restore removed serial, link, Card Pop, SGB, printer, or related paths. Do not add stubs or hard-coded Extended addresses.

## Acceptance
- [ ] Extended build configured :: `just extended-configure-lane`
- [ ] Incremental Extended build passes :: `just build-extended-incremental`
- [ ] Core oracle cases are clean :: `just extended-check core`
- [ ] Duel core oracle cases are clean :: `just extended-check duel_core`
- [ ] Duel init oracle cases are clean :: `just extended-check duel_init`
- [ ] Each basename passes constant, adapter, and oracle audits :: `python3 tools/lint_constants.py --profile extended ... && python3 tools/lint_adapters.py ... && POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <basename>`
- [ ] Every changed body is mutation RED :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/<basename>.py --build build-ext-LaneCore`
- [ ] Repo green check is run by the integrator after landing :: `just extended-check core && just extended-check duel_core && just extended-check duel_init`
