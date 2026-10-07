# Goal
Audit the documented Extended fixes for energy, ai, sams_practice, substatus, and hand_pokemon, make each overlay match Extended asm, add or correct mutation evidence, and prove one red revert per named heading. Also make energy AIProcessEnergyCards and legendary_articuno ScoreLegendaryArticunoCards mutation receipts red.

# Files in scope
src/profiles/extended/home/energy.c: energy routines and fixed score behavior.
src/profiles/extended/home/energy.h: energy routine declarations if required.
src/profiles/extended/probe/energy.c: energy adapters and table rows if required.
tests/profiles/extended/cases/energy.py: energy oracle cases and mutations.
src/profiles/extended/home/ai.c: AIDoAction_StartDuel and related AI routines.
src/profiles/extended/home/ai.h: AI declarations if required.
src/profiles/extended/probe/ai.c: AI adapters and table rows if required.
tests/profiles/extended/cases/ai.py: AI oracle cases and mutations.
src/profiles/extended/home/sams_practice.c: scripted-turn implementation.
src/profiles/extended/home/sams_practice.h: scripted-turn declarations if required.
src/profiles/extended/probe/sams_practice.c: scripted-turn adapter/table if required.
tests/profiles/extended/cases/sams_practice.py: scripted-turn cases and mutations.
src/profiles/extended/home/substatus.c: damage reduction and 16-bit card-id behavior.
src/profiles/extended/home/substatus.h: substatus declarations if required.
src/profiles/extended/probe/substatus.c: substatus adapters/table if required.
tests/profiles/extended/cases/substatus.py: damage and card-id cases/mutations.
src/profiles/extended/home/hand_pokemon.c: AIDecideEvolution behavior.
src/profiles/extended/home/hand_pokemon.h: hand AI declarations if required.
src/profiles/extended/probe/hand_pokemon.c: hand AI adapters/table if required.
tests/profiles/extended/cases/hand_pokemon.py: evolution cases and mutations.
src/profiles/extended/home/legendary_articuno.c: secondary mutation evidence only.
tests/profiles/extended/cases/legendary_articuno.py: secondary mutation evidence only.

# Contracts
The lane contract is local://extended-lane-brief.md. Use generated Extended headers and 16-bit card ids. Read each bug heading and Fix section in poketcg-extended/bugs_and_glitches.md, then compare Extended asm and overlay C. Mutation JSON must revert exact unique C text and compile. Follow docs/factory-contract.md for adapters, cases, and mutations. Run overlay_check after every C edit.

# Pattern to copy
Use existing fixture-backed cases and MUTATIONS in tests/profiles/extended/cases/energy.py, ai.py, and hand_pokemon.py, plus the fixed 16-bit card-id comparisons in the current Extended overlays.

# Non-goals
Do not edit profiles/extended/fixes.toml, shared src/home or src/probe, tools, justfile, CMakeLists, unrelated basenames, or add comments. Do not run forbidden global gates or git/jj commands.

# Acceptance
- [ ] Lane configured and incremental build succeeds :: just extended-configure-lane && just build-extended-incremental
- [ ] Each touched basename is clean :: just extended-check energy && just extended-check ai && just extended-check sams_practice && just extended-check substatus && just extended-check hand_pokemon
- [ ] Constants and adapters lint clean :: python3 tools/lint_constants.py && python3 tools/lint_adapters.py
- [ ] Oracle case audit is clean :: POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only energy,ai,sams_practice,substatus,hand_pokemon
- [ ] Every named revert is red :: POKETCG_PROFILE=extended python3 tools/run_mutation.py ...
- [ ] Repository lane checks are green :: just extended-check <basename>
