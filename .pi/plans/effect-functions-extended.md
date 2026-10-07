# Goal
Finish the Extended profile port for basename `effect_functions`, including the GustOfWind_SwitchEffect wedge, so every Extended routine in the basename passes oracle comparison and changed C bodies have RED mutation coverage.

# Files in scope
- `src/profiles/extended/home/effect_functions.c`: Extended factory routine bodies and generated-label statics.
- `src/profiles/extended/home/effect_functions.h`: signatures and result structs for changed routines.
- `src/profiles/extended/probe/effect_functions.c`: marshal-only adapters and probe table rows.
- `tests/profiles/extended/cases/effect_functions.py`: Extended numeric cases, contracts, and mutation entries.
- `poketcg-extended/src/**`: Extended asm truth, read-only source for routine behavior.
- `build-ext-<lane>/generated/extended/generated/rom.h`: Extended ROM labels for dispatch targets.
- `docs/factory-contract.md`: bus, flags, adapters, cases, and mutation rules.
- `local://extended-lane-brief.md`: lane loop, wedge handling, and scope rules.

# Contracts
Use generated headers for symbols and numeric addresses in Python cases. Keep factory markers and asm range comments. Adapters make exactly one routine call and only marshal produced registers. Wedges require asm-derived setup, keys, or an explicit oracle false contract. Run `lint_constants.py`, `lint_adapters.py`, and `audit_oracle_cases.py --stage routine --only effect_functions`.

# Pattern to copy
Use the existing `effect_functions` factory blocks, adapters, and case contracts as the local pattern, with `docs/factory-contract.md` as the definitive implementation example.

# Non-goals
Do not edit shared `src/home/*`, shared `src/probe/*`, vanilla cases, tools, build scripts, justfile, or another basename's overlay. Do not patch cross-lane callees.

# Acceptance
- [ ] All Extended effect routines oracle-clean :: `just extended-check effect_functions`
- [ ] Named constants and adapter lint clean :: `python3 tools/lint_constants.py --profile extended src/profiles/extended/home/effect_functions.c src/profiles/extended/home/effect_functions.h src/profiles/extended/probe/effect_functions.c && python3 tools/lint_adapters.py src/profiles/extended/probe/effect_functions.c`
- [ ] Extended cases audit clean :: `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only effect_functions`
- [ ] Every changed C body has RED mutation coverage :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/effect_functions.py --build build-ext-<lane>`
- [ ] Repo green-check item :: `just extended-check effect_functions`