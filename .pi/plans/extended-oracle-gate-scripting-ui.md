# Goal
Make Extended oracle gate cases pass for scripting, deck_machine_room, deck_machine, menus, load_animation, and screen_effects, including contract fixes for Extended register behavior and primary-case metadata. Keep each owned basename clean under the Extended PyBoy lane.

# Files in scope
- src/profiles/extended/home/scripting.c, scripting.h: Extended script command bodies and declarations.
- src/profiles/extended/probe/scripting.c: scripting probe adapters and table rows.
- tests/profiles/extended/cases/scripting.py: scripting contracts, cases, and mutations.
- src/profiles/extended/home/deck_machine_room.c, deck_machine_room.h: deck machine room routines.
- src/profiles/extended/probe/deck_machine_room.c: deck machine room adapters.
- tests/profiles/extended/cases/deck_machine_room.py: script VM case metadata.
- src/profiles/extended/home/deck_machine.c, deck_machine.h: deck machine routines.
- src/profiles/extended/probe/deck_machine.c: deck machine adapters.
- tests/profiles/extended/cases/deck_machine.py: deck machine cases.
- src/profiles/extended/home/menus.c, menus.h: menu input routines.
- src/profiles/extended/probe/menus.c: menu adapters.
- tests/profiles/extended/cases/menus.py: menu cases and mutations.
- src/profiles/extended/home/load_animation.c, load_animation.h and probe/load_animation.c: animation routines and adapters.
- tests/profiles/extended/cases/load_animation.py: animation cases.
- src/profiles/extended/home/screen_effects.c, screen_effects.h and probe/screen_effects.c: screen animation routines and adapters.
- tests/profiles/extended/cases/screen_effects.py: screen animation cases.

# Contracts
- Extended asm and symbols are authoritative: poketcg-extended/src/** and poketcg-extended/poketcg_ext.sym.
- Follow docs/factory-contract.md for bus access, signatures, adapters, cases, and mutations.
- Use build-ext-GateScripts with POKETCG_NINJA_JOBS=-j1, configured by just extended-configure-lane and built by just build-extended-incremental.
- Reference failures guide fixes: REFERENCE_DIVERGENCE changes preserve/compare; PORT changes C and needs RED mutation evidence; BUDGET_EXHAUSTED cases need entry completion, keys, or valid budgets; no-primary cases need a finishing primary case.

# Pattern to copy
- tests/profiles/extended/cases/grass_club.py, including its SCHEMA2_CASES completion assignments for script routines.

# Non-goals
- Do not edit shared src/home, src/probe, tests/cases, tools, CMakeLists.txt, justfile, or another lane's basenames.
- Do not edit case inputs or expectations to hide C/ROM differences.
- Do not run full gate commands, git/jj commands, or builds above -j1.

# Acceptance
- [ ] Each owned module has no gbref primary failures :: POKETCG_PROFILE=extended python3 /tmp/extpilot/gbref_check.py --build build-ext-GateScripts --module scripting --module deck_machine_room --module deck_machine --module menus --module load_animation --module screen_effects
- [ ] Each owned basename passes the PyBoy lane :: just extended-check scripting deck_machine_room deck_machine menus load_animation screen_effects
- [ ] Constants and adapters pass lint :: python3 tools/lint_constants.py --profile extended src/profiles/extended/home/scripting.c src/profiles/extended/home/deck_machine_room.c src/profiles/extended/home/deck_machine.c src/profiles/extended/home/menus.c src/profiles/extended/home/load_animation.c src/profiles/extended/home/screen_effects.c && python3 tools/lint_adapters.py src/profiles/extended/probe/scripting.c src/profiles/extended/probe/deck_machine_room.c src/profiles/extended/probe/deck_machine.c src/profiles/extended/probe/menus.c src/profiles/extended/probe/load_animation.c src/profiles/extended/probe/screen_effects.c
- [ ] Routine case audit passes :: POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only scripting --only deck_machine_room --only deck_machine --only menus --only load_animation --only screen_effects
- [ ] Repo's green-check item :: POKETCG_PROFILE=extended just oracle-fn-gate
