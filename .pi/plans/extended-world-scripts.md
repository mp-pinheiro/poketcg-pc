# Goal
Close all remaining Extended oracle failures for overworld, script, scripting, map, main_menu, mason_laboratory, grass_club, pokemon_dome, pokemon_dome_entrance, psychic_club_entrance, science_club_lobby, and challenge_machine, with overlay C/header/probe changes and matching numeric Extended cases.

# Files in scope
src/profiles/extended/home/overworld.c/.h: Extended overworld routines.
src/profiles/extended/probe/overworld.c: overworld adapters and table.
src/profiles/extended/home/script.c/.h: script routines.
src/profiles/extended/probe/script.c: script adapters and table.
src/profiles/extended/home/scripting.c/.h: scripting routines.
src/profiles/extended/probe/scripting.c: scripting adapters and table.
src/profiles/extended/home/map.c/.h: map routines.
src/profiles/extended/probe/map.c: map adapters and table.
src/profiles/extended/home/main_menu.c/.h: main menu routines.
src/profiles/extended/probe/main_menu.c: main menu adapters and table.
src/profiles/extended/home/mason_laboratory.c/.h: Mason routines.
src/profiles/extended/probe/mason_laboratory.c: Mason adapters and table.
src/profiles/extended/home/{grass_club,pokemon_dome,pokemon_dome_entrance,psychic_club_entrance,science_club_lobby,challenge_machine}.{c,h}: club, dome, entrance, and challenge routines.
src/profiles/extended/probe/{grass_club,pokemon_dome,pokemon_dome_entrance,psychic_club_entrance,science_club_lobby,challenge_machine}.c: matching adapters and tables.
tests/profiles/extended/cases/{overworld,script,scripting,map,main_menu,mason_laboratory,grass_club,pokemon_dome,pokemon_dome_entrance,psychic_club_entrance,science_club_lobby,challenge_machine}.py: Extended oracle contracts, cases, and mutations.

# Contracts
Use local://extended-lane-brief.md for setup, loop, wedge handling, and reporting.
Use docs/factory-contract.md for bus access, signatures, adapters, case coverage, and mutations.
Use tools/profile_audit.py --routines <b> to classify routines.
Use just extended-check <b>, tools/lint_constants.py, tools/lint_adapters.py, and audit_oracle_cases.py for acceptance.
Use run_mutation.py for every changed C routine; do not touch shared files or other lanes.

# Pattern to copy
Use src/profiles/extended/home/grass_club.c with its matching probe and case structure as the closest existing Extended overlay quartet.

# Non-goals
Do not edit shared src/home or src/probe files, tools, justfile, CMake files, or other basenames. Do not alter cases to hide C mismatches. Do not add prose comments, stubs, or hard-coded Extended addresses/constants.

# Acceptance
- [ ] Lane configured in private build directory :: export POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-WorldScripts POKETCG_NINJA_JOBS=-j2 && just extended-configure-lane && just build-extended-incremental
- [ ] Each target basename is oracle-clean :: just extended-check <basename>
- [ ] Target overlays pass constant lint :: python3 tools/lint_constants.py --profile extended <target trio>
- [ ] Target probes pass adapter lint :: python3 tools/lint_adapters.py <target probe>
- [ ] Target cases pass audit :: POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <basename>
- [ ] Every changed C routine has a RED mutation receipt :: POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/<basename>.py --build build-ext-WorldScripts
- [ ] Final report includes summaries, ported routines, RED receipts, lint/audit, and grounded blockers :: just extended-check <basename>