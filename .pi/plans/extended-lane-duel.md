# Extended lane duel context

## Goal
Complete LaneDuel's Extended profile port in basename order, starting with duel and trainer_cards, then every listed AI and duel support basename, with oracle-clean routines, lint, case audit, and RED mutations.

## Files in scope
src/profiles/extended/home/<b>.c/.h: Extended implementations and signatures for assigned basenames.
src/profiles/extended/probe/<b>.c: Marshal-only adapters and probe rows.
tests/profiles/extended/cases/<b>.py: Extended oracle cases and one mutation per changed body.
docs/factory-contract.md: C, adapter, case, and mutation contracts.
local://extended-lane-brief.md: Lane setup, loop, rules, and report format.

## Contracts
Use generated Extended headers and numeric case addresses only.
Keep factory markers and asm range comments, and edit only overlay trios plus cases.
`just extended-check <b>` must report N/N routines clean.
`python3 tools/lint_constants.py --profile extended src/profiles/extended/home/<b>.c src/profiles/extended/home/<b>.h src/profiles/extended/probe/<b>.c` must exit 0.
`python3 tools/lint_adapters.py src/profiles/extended/probe/<b>.c` must exit 0.
`POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <b>` must print AUDIT_OK.

## Pattern to copy
Use src/profiles/extended/home/trainer_cards.c and src/profiles/extended/probe/trainer_cards.c for factory blocks and marshal-only adapters; use tests/profiles/extended/cases/trainer_cards.py for Extended cases and mutations.

## Non-goals
Do not edit shared vanilla sources, tools, build files, or another lane's overlays. Do not port vanilla-only routines or removed basenames. Do not add shims, stubs, hard-coded Extended addresses, or comments beyond required asm ranges and factory markers.

## Acceptance
- [ ] Every assigned basename has an oracle-clean summary :: `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneDuel just extended-check <b>`
- [ ] Extended constants are lint-clean :: `python3 tools/lint_constants.py --profile extended src/profiles/extended/home/<b>.c src/profiles/extended/home/<b>.h src/profiles/extended/probe/<b>.c`
- [ ] Probe adapters are lint-clean :: `python3 tools/lint_adapters.py src/profiles/extended/probe/<b>.c`
- [ ] Oracle cases are audited :: `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <b>`
- [ ] Every changed C body has a RED mutation :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/<b>.py --build build-ext-LaneDuel`
- [ ] Repo's own green-check item :: `N/N routines clean` for each assigned basename
