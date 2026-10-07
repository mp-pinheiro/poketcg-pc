# Extended AI and card ID audit

## Goal
Audit and complete the Extended port basenames energy, ai, sams_practice, hand_pokemon, and legendary_articuno against the Extended assembly, including each named documented fix, required high-byte card ID handling, and red mutation proofs.

## Files in scope
src/profiles/extended/home/energy.c: energy scoring and AI energy selection.
src/profiles/extended/home/ai.c: AI action wrappers and dispatch.
src/profiles/extended/home/sams_practice.c: Sam scripted actions.
src/profiles/extended/home/hand_pokemon.c: evolution scoring and card ID checks.
src/profiles/extended/home/legendary_articuno.c: Articuno scoring and turn logic.
tests/profiles/extended/cases/{energy,ai,sams_practice,hand_pokemon,legendary_articuno}.py: oracle cases and mutations.
profiles/extended/fixes.toml: documented fix headings and revert contract.
src/home/card_id_bus.h: full-width card ID helpers.
poketcg-extended/src/engine/duel/ai/{energy,hand_pokemon}.asm: truth for target routines.
poketcg-extended/src/{home/ai.asm,engine/duel/ai/decks/sams_practice.asm,engine/duel/ai/decks/legendary_articuno.asm}: truth for target routines.

## Contracts
Use local://extended-lane-brief.md. Setup uses POKETCG_PROFILE=extended, an own build-ext lane, and POKETCG_NINJA_JOBS=-j2. C edits are whole-function edits and require overlay_check after each C edit. Card IDs use card_id_read_at/card_id_write and generated constants. Documented fixes need a RED revert receipt using run_mutation.py. Each changed routine needs a failing mutation case. Finish each basename with just extended-check, lint_constants.py, lint_adapters.py, and audit_oracle_cases.py.

## Pattern to copy
Use src/profiles/extended/home/energy.c card_id_read/card_id_write usage in AI card-list scoring, and src/profiles/extended/home/retreat.c for full-width loaded card ID comparisons.

## Non-goals
Do not edit shared src/home or src/probe, tests/cases, tools, build configuration, another lane's files, or profiles/extended/fixes.toml. Do not change cases to fit C. Do not run forbidden git, jj, full build, release gates, or all-leaves checks.

## Acceptance
- [ ] All named documented fixes have one RED revert :: POKETCG_PROFILE=extended python3 tools/run_mutation.py <routine> tests/profiles/extended/cases/<basename>.py --build build-ext-<lane> --mutation /tmp/<lane>/<routine>.json --receipt /tmp/<lane>/<routine>-receipt.json
- [ ] Target C routines and 16-bit IDs match Extended asm :: python3 tools/overlay_check.py <basename>
- [ ] Target basenames pass oracle checks :: just extended-check <basename>
- [ ] Constants, adapters, and oracle case audits are clean :: python3 tools/lint_constants.py --profile extended; python3 tools/lint_adapters.py; POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <basename>
- [ ] Repository green check :: just extended-check <basename>
