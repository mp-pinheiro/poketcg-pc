# Goal
Port the assigned Extended overworld lane basenames against the Extended ROM, preserving oracle behavior and closing the current overworld entry divergence. The lane covers overworld, load_overworld, load_map_header, warp, npc_core, map, map_events, objects, and common failures listed in the Extended scoreboard.

# Files in scope
- `src/profiles/extended/home/{overworld,load_overworld,load_map_header,warp,npc_core,map,map_events,objects,common}.{c,h}`: Extended C overlays.
- `src/profiles/extended/probe/{overworld,load_overworld,load_map_header,warp,npc_core,map,map_events,objects,common}.c`: probe adapters/tables.
- `tests/profiles/extended/cases/{overworld,load_overworld,load_map_header,warp,npc_core,map,map_events,objects,common}.py`: oracle cases and mutations.
- `src/home/{overworld,load_overworld,load_map_header,warp,npc_core,map,map_events,objects,common}.{c,h}`: vanilla patterns and signatures.
- `src/probe/{overworld,load_overworld,load_map_header,warp,npc_core,map,map_events,objects,common}.c`: shared adapter patterns.
- `tests/cases/{overworld,load_overworld,load_map_header,warp,npc_core,map,map_events,objects,common}.py`: seeded case patterns.
- `docs/factory-contract.md`: bus, adapter, case, and mutation rules.
- `local://extended-scoreboard-failures.md`: current failing and wedged routines.

# Contracts
Use Extended asm and generated headers as truth. Run `python3 tools/profile_audit.py --routines <b>`, `just extended-check <b>`, `python3 tools/lint_constants.py --profile extended ...`, `python3 tools/lint_adapters.py ...`, and `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <b>`. Changed C bodies require RED mutation via `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/<b>.py --build build-ext-LaneWorld4`.

# Pattern to copy
Use the existing Extended overlay quartet for `overworld` and the nearest completed Extended overlay with factory markers, generated-header access, probe marshalling, numeric cases, and mutation entries as the implementation pattern.

# Non-goals
Do not edit shared `src/home`, shared `src/probe`, vanilla tests, tools, build files, or another lane's overlays. Do not patch around callees owned by LaneEffects4. Do not add stubs, compatibility branches, or unrelated cleanup.

# Acceptance
- [ ] Every assigned routine matches Extended oracle :: `just extended-check <b>`
- [ ] Each assigned basename has clean lints and audit :: `python3 tools/lint_constants.py --profile extended ... && python3 tools/lint_adapters.py ... && POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <b>`
- [ ] Every changed C body has a RED mutation :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/<b>.py --build build-ext-LaneWorld4`
- [ ] New-game completion reaches the Extended oracle finish :: `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneWorld4 python3 tools/completion/session.py verify new-game --no-publish`
