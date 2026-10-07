# Extended world3 port context

## Goal
Port the listed Extended world and save routines in basename order, using Extended assembly as oracle truth, until each group is clean or failures are reported with exact diffs and cross-lane callees.

## Files in scope
- src/profiles/extended/home/scripting.c, scripting.h, probe/scripting.c, tests/profiles/extended/cases/scripting.py: script dispatch and RST20.
- src/profiles/extended/home/overworld.c, overworld.h, probe/overworld.c, tests/profiles/extended/cases/overworld.py: overworld wedge and callers.
- src/profiles/extended/home/common.c, common.h, probe/common.c, tests/profiles/extended/cases/common.py: promotional/common routines.
- src/profiles/extended/home/pokemon_dome.c, pokemon_dome.h, probe/pokemon_dome.c, tests/profiles/extended/cases/pokemon_dome.py: dome routines.
- src/profiles/extended/home/npc_data.c, npc_data.h, probe/npc_data.c, tests/profiles/extended/cases/npc_data.py: NPC data routines.
- src/profiles/extended/home/save.c, save.h, probe/save.c, tests/profiles/extended/cases/save.py: save and SRAM routines.
- src/profiles/extended/home/credits_sequence_commands.c, credits_sequence_commands.h, probe/credits_sequence_commands.c, tests/profiles/extended/cases/credits_sequence_commands.py: credits script entries.
- src/profiles/extended/home/credits.c, credits.h, probe/credits.c, tests/profiles/extended/cases/credits.py: credits routines.
- Remaining listed club, map, load_overworld, challenge, mason, and entrance overlay trios and case modules.

## Contracts
- local://extended-lane-brief.md: setup, per-basename loop, ownership, oracle, lint, audit, mutation, and report rules.
- local://extended-scoreboard-failures.md: current wedges and failing routines.
- docs/factory-contract.md: bus accesses, signatures, adapters, cases, mutation evidence, numeric addresses.
- Generated headers under build-ext-LaneWorld3/generated/extended/generated: symbols and constants only.

## Pattern to copy
Use the completed Extended overlay trio and case module for a nearby basename, preserving factory markers, asm range comments, adapter marshalling, and MUTATIONS entries.

## Non-goals
- Do not edit shared src/home or src/probe, tools, justfile, build files, or another lane's overlays.
- Do not change vanilla behavior, invent constants or addresses, add stubs, or leave wedging oracle cases.

## Acceptance
- [ ] Each target basename is checked :: POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneWorld3 just extended-check <basename>
- [ ] Overlay constants and adapters lint :: python3 tools/lint_constants.py --profile extended <overlay trio>
- [ ] Cases audit :: POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <basename>
- [ ] Changed bodies mutate RED :: POKETCG_PROFILE=extended python3 tools/run_mutation.py <routine> tests/profiles/extended/cases/<basename>.py --build build-ext-LaneWorld3
- [ ] Repository green-check item :: just extended-check <basename>
