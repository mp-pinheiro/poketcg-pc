# Goal
Bring the Extended `trainer_cards` overlay and cases to oracle parity for the EnergySearch, Maintenance, LegendaryArticuno trader, EnergyRemoval, GustOfWind, ProfessorOak, FullHeal, and PowerGenerator work, including Extended two-byte card ids, fixture-backed EnergySearch coverage, RED mutations, lint, and audit.

# Files in scope
- `src/profiles/extended/home/trainer_cards.c`: Extended trainer decision/play bodies and statics.
- `src/profiles/extended/home/trainer_cards.h`: trainer result signatures.
- `src/profiles/extended/probe/trainer_cards.c`: adapters and probe rows.
- `tests/profiles/extended/cases/trainer_cards.py`: contracts, fixtures, cases, mutations.
- `poketcg-extended/src/engine/duel/ai/trainer_cards.asm`: Extended asm truth.
- `build-ext-LaneAITrainer/generated/extended/generated/*.h`: generated symbols/constants.
- `tests/sessions/extended/extended-fixes`: captured-session source for EnergySearch fixture.

# Contracts
- Follow `local://extended-lane-brief.md` for setup, per-basename order, wedge handling, reserved frame, and reporting.
- Follow `docs/port-contract.md` and `docs/factory-contract.md` for two-byte card ids, bus access, adapters, cases, and mutations.
- Only edit the trainer_cards overlay trio and Extended case module; never edit shared vanilla files, tools, generated files, or other basenames.
- Checks: `just extended-check trainer_cards`; both trainer_cards lint commands; `audit_oracle_cases --stage routine --only trainer_cards`; RED mutation commands for every changed C body.

# Pattern to copy
Imitate nearby completed Extended trainer decision cases and fixture use in `tests/profiles/extended/cases/trainer_cards.py`, with generated-header symbols in C and marshal-only result adapters.

# Non-goals
Do not change routines outside `trainer_cards`, weaken or mark live cases oracle-false to hide C mismatches, seed the oracle frame ranges, or edit derived case registries/tools.

# Acceptance
- [ ] Extended trainer oracle parity :: `just extended-check trainer_cards`
- [ ] Trainer constants and adapters lint :: `python3 tools/lint_constants.py --profile extended src/profiles/extended/home/trainer_cards.c src/profiles/extended/home/trainer_cards.h src/profiles/extended/probe/trainer_cards.c && python3 tools/lint_adapters.py src/profiles/extended/probe/trainer_cards.c`
- [ ] Trainer case audit :: `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only trainer_cards`
- [ ] Every changed C body has RED mutation evidence :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/trainer_cards.py --build build-ext-LaneAITrainer`
- [ ] Repository green-check item :: `just extended-check trainer_cards` reports all routines clean