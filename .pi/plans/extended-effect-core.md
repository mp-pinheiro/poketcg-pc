# Goal
Bring the Extended `effect_functions` and `core` overlays and case modules to oracle parity, including the named shared callee ports, input wait contracts, indirect dispatch labels, lint/audit compliance, and RED mutation coverage.

# Files in scope
- `src/profiles/extended/home/effect_functions.c`: Extended effect routine bodies and statics.
- `src/profiles/extended/home/effect_functions.h`: Effect signatures.
- `src/profiles/extended/probe/effect_functions.c`: Effect adapters and probe rows.
- `tests/profiles/extended/cases/effect_functions.py`: Effect contracts, cases, and mutations.
- `src/profiles/extended/home/core.c`: Extended core routine bodies and callee implementations.
- `src/profiles/extended/home/core.h`: Core signatures and result structs.
- `src/profiles/extended/probe/core.c`: Core adapters and probe rows.
- `tests/profiles/extended/cases/core.py`: Core contracts, cases, and mutations.
- `poketcg-extended/src/**`: Read-only Extended asm truth.
- `build-ext-LaneEffects4/generated/extended/generated/*.h`: Generated symbols and constants.

# Contracts
- Follow `local://extended-lane-brief.md`, especially the per-basename loop and wedge rules.
- Follow `docs/factory-contract.md` for bus access, signatures, adapters, cases, and mutations.
- Do not edit shared `src/home`, `src/probe`, vanilla tests, tools, build files, or another lane's overlays.
- Relevant checks are `just extended-check effect_functions`, `just extended-check core`, both lint commands, and `audit_oracle_cases --only`.

# Pattern to copy
Use existing completed Extended overlay routines and their nearby `===PROBE` and `===CASES` blocks, especially the generated-header based bus access and result-struct adapter pattern.

# Non-goals
Do not alter routines outside the two basenames except by messaging the owning lane with an exact callee mismatch. Do not change oracle inputs to hide a C mismatch, add shims, or edit generated files.

# Acceptance
- [ ] Effect oracle parity :: `just extended-check effect_functions`
- [ ] Core oracle parity :: `just extended-check core`
- [ ] Effect constants and adapters lint :: `python3 tools/lint_constants.py --profile extended src/profiles/extended/home/effect_functions.c src/profiles/extended/home/effect_functions.h src/profiles/extended/probe/effect_functions.c && python3 tools/lint_adapters.py src/profiles/extended/probe/effect_functions.c`
- [ ] Core constants and adapters lint :: `python3 tools/lint_constants.py --profile extended src/profiles/extended/home/core.c src/profiles/extended/home/core.h src/profiles/extended/probe/core.c && python3 tools/lint_adapters.py src/profiles/extended/probe/core.c`
- [ ] Effect case audit :: `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only effect_functions`
- [ ] Core case audit :: `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only core`
- [ ] Every changed C body has RED mutation evidence :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/<basename>.py --build build-ext-LaneEffects4`
- [ ] Repository green-check item :: both `just extended-check` commands report all routines clean
