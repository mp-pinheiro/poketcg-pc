# Context pack

## Goal
Finish the Extended profile oracle port for the assigned deck, menu, mail, naming, and related basenames, including wedges, cases, adapters, and mutation evidence.

## Files in scope
- `src/profiles/extended/home/deck_configuration.{c,h}`: deck configuration overlay.
- `src/profiles/extended/probe/deck_configuration.c`: deck configuration adapters and table.
- `tests/profiles/extended/cases/deck_configuration.py`: contracts, cases, mutations.
- `src/profiles/extended/home/deck_machine.{c,h}`: deck machine overlay.
- `src/profiles/extended/probe/deck_machine.c`: deck machine adapters and table.
- `tests/profiles/extended/cases/deck_machine.py`: deck machine cases.
- `src/profiles/extended/home/deck_machine_room.{c,h}` and matching probe/cases: room overlay.
- `src/profiles/extended/home/menus.{c,h}` and matching probe/cases: menu overlay.
- `src/profiles/extended/home/deck_selection.{c,h}` and matching probe/cases: selection overlay.
- Matching overlay trio and cases for `mail`, `main_menu`, `deck_check`, `glossary`, `give_booster_pack`, `promotional_card`, `auto_deck_machines`, `medal`, `naming`, and `input_name`.
- `poketcg-extended/src/**`: authoritative Extended asm and script prologues.
- `build-ext-LaneDecks3/generated/extended/generated/*.h`: generated symbols/constants used by C.

## Contracts
Follow `docs/port-contract.md` and `docs/factory-contract.md`; use numeric case addresses, bus accessors, exact factory markers, adapter marshal-only rules, and one RED mutation per changed body. Use `python3 tools/profile_audit.py --routines <b>`, `just extended-check <b>`, both Extended linters, `audit_oracle_cases --only <b>`, and `run_mutation.py`.

## Pattern to copy
Use the existing Extended `src/profiles/extended/home/auto_deck_machines.c` plus its probe and cases as the nearest small changed-basename exemplar.

## Non-goals
Do not edit shared `src/home`, `src/probe`, `tests/cases`, tools, build files, justfile, or another lane's overlays. Do not port vanilla-only routines or add shims/stubs.

## Acceptance
- [ ] Every listed basename has an oracle-clean summary or exact remaining diff :: `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneDecks3 just extended-check <b>`
- [ ] Overlay constants and adapters are clean :: `python3 tools/lint_constants.py --profile extended <overlay trio>` and `python3 tools/lint_adapters.py <probe>`
- [ ] Case schema is clean :: `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <b>`
- [ ] Changed bodies have RED mutation evidence :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/<b>.py --build build-ext-LaneDecks3`
- [ ] Repo lane check is green :: `just extended-check <b>`
