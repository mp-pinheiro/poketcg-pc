# Extended world lane port

## Goal
Port the Extended world, map, scripting, NPC, and club basenames listed by the lane brief into the overlay quartet, then obtain oracle-clean routine groups with lint, audit, and RED mutation evidence.

## Files in scope
- src/profiles/extended/home/{scripting,overworld,map,script,npc_data,npc_core,overworld_map,map_events,load_overworld,load_map_header,warp,objects}.c and .h: world routine bodies and declarations.
- src/profiles/extended/home/{pokemon_dome,pokemon_dome_entrance,mason_laboratory,challenge_hall,challenge_machine,common}.c and .h: world and facility routines.
- src/profiles/extended/home/{fire_club_lobby,water_club,water_club_lobby,science_club,science_club_lobby,rock_club,rock_club_lobby,psychic_club,psychic_club_entrance,psychic_club_lobby,lightning_club,lightning_club_lobby,grass_club,grass_club_lobby,fighting_club,fighting_club_lobby,fire_club}.c and .h: club routines.
- src/profiles/extended/probe/<same basenames>.c: marshal-only probe adapters and table rows.
- tests/profiles/extended/cases/<same basenames>.py: numeric oracle cases and mutation entries.
- poketcg-extended/src/**: authoritative Extended assembly and symbols, read-only.
- build-ext-LaneWorld/generated/extended/generated/{wram,hram,sram,rom,constants,text_ids}.h: generated labels and constants, read-only.

## Contracts
- local://extended-lane-brief.md: setup, per-basename loop, wedge handling, ownership, and report.
- docs/factory-contract.md: bus access, signatures, adapters, cases, comments, and mutations.
- Each changed routine needs `just extended-check <basename>`, lint_constants, lint_adapters, audit_oracle_cases, and RED mutation evidence.

## Pattern to copy
Use the existing Extended `scripting` overlay, probe, and case module structure, correcting it from `poketcg-extended/src` rather than inventing a new convention.

## Non-goals
- Do not edit shared vanilla files, other lanes' overlays, tools, build files, or unrelated generated data.
- Do not patch around cross-lane callees or leave wedging cases in place.
- Do not run prohibited full-repository gates or version-control commands.

## Acceptance
- [ ] Lane setup completes :: just extended-configure-lane && just build-extended-incremental
- [ ] Every assigned basename has an oracle summary :: just extended-check <basename>
- [ ] Every assigned basename passes static checks :: python3 tools/lint_constants.py --profile extended src/profiles/extended/home/<basename>.c src/profiles/extended/home/<basename>.h src/profiles/extended/probe/<basename>.c && python3 tools/lint_adapters.py src/profiles/extended/probe/<basename>.c
- [ ] Cases are audited :: POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <basename>
- [ ] Changed routine mutations are RED :: POKETCG_PROFILE=extended python3 tools/run_mutation.py <routine> tests/profiles/extended/cases/<basename>.py --build build-ext-LaneWorld
