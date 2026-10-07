# Extended oracle retreat and hand lane

## Goal
Bring Extended retreat and hand_pokemon oracle behavior into agreement with the captured sessions, then provide required proof receipts, lints, and audits for the listed AI basenames without changing unrelated overlays or tests.

## Files in scope
- `src/profiles/extended/home/retreat.c`: Extended retreat C bodies.
- `src/profiles/extended/home/retreat.h`: retreat result declarations.
- `src/profiles/extended/probe/retreat.c`: retreat probe adapters.
- `tests/profiles/extended/cases/retreat.py`: retreat cases, fixtures, mutations.
- `src/profiles/extended/home/hand_pokemon.c`: Extended hand AI C bodies.
- `src/profiles/extended/home/hand_pokemon.h`: hand AI result declarations.
- `src/profiles/extended/probe/hand_pokemon.c`: hand AI probe adapters.
- `tests/profiles/extended/cases/hand_pokemon.py`: hand AI cases, fixtures, mutations.
- Listed proof basenames under `src/profiles/extended/{home,probe}` and `tests/profiles/extended/cases`.

## Contracts
Use `docs/factory-contract.md`, numeric case addresses, generated Extended headers, and no oracle frame seeds. Use the lane brief loop: `extended-check`, mutation RED receipts for changed C, `lint_constants`, `lint_adapters`, and routine `audit_oracle_cases`.

## Pattern to copy
Use the existing fixture-backed routine cases and mutation declarations in `tests/profiles/extended/cases/retreat.py` and `hand_pokemon.py`.

## Non-goals
Do not edit shared `src/home`, shared `src/probe`, vanilla cases, tools, build files, other basenames, or code to mask an outside-basename callee defect. Do not run forbidden repository commands.

## Acceptance
- [ ] lane config succeeds :: `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneAIRetreatHand POKETCG_NINJA_JOBS=-j2 just extended-configure-lane`
- [ ] lane incremental build succeeds :: `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneAIRetreatHand POKETCG_NINJA_JOBS=-j2 just build-extended-incremental`
- [ ] retreat oracle is clean :: `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneAIRetreatHand just extended-check retreat`
- [ ] hand oracle is clean :: `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneAIRetreatHand just extended-check hand_pokemon`
- [ ] listed basenames pass lints and routine audits :: `python3 tools/lint_constants.py --profile extended ... && python3 tools/lint_adapters.py ... && POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only ...`
- [ ] required mutation runs are RED :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <routine> tests/profiles/extended/cases/<basename>.py --build build-ext-LaneAIRetreatHand`
