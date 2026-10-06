# Context pack

## Goal
Port the Extended core, hand_pokemon, and start overlays to match Extended assembly, remove all serial/link/Card Pop references from assigned C, and add numeric-address factory cases for newly ported core routines.

## Files in scope
- `src/profiles/extended/home/core.c` - remove serial/link calls and align changed core routines.
- `src/profiles/extended/home/core.h` - expose existing Extended routine signatures.
- `src/profiles/extended/probe/core.c` - marshal newly covered core routines.
- `tests/profiles/extended/cases/core.py` - add CONTRACT/CASES/MUTATIONS for core routines.
- `src/profiles/extended/home/hand_pokemon.c` - port changed AI hand routines and renamed callee.
- `src/profiles/extended/home/hand_pokemon.h` - keep hand routine declarations aligned.
- `src/profiles/extended/probe/hand_pokemon.c` - marshal hand outputs.
- `tests/profiles/extended/cases/hand_pokemon.py` - update changed routine cases.
- `src/profiles/extended/home/start.c` - call ValidateSavedDuelData.

## Contracts
- `docs/factory-contract.md` requires exact C factory behavior, numeric Python addresses, POISON coverage, and exact mutation substrings.
- Extended truth is in `poketcg-extended/src/engine/duel/core.asm`, `engine/duel/ai/core.asm`, `engine/duel/ai/hand_pokemon.asm`, and `engine/menus/start.asm`.
- Generated RAM addresses come from `build-ext-cmake/generated/extended/generated/wram.h`.
- Use `python3 tools/overlay_check.py core hand_pokemon start`; inspect only assigned files and no link/build commands.

## Pattern to copy
Use existing factory/probe/case blocks in `src/profiles/extended/home/core.c`, `src/profiles/extended/probe/core.c`, and `tests/profiles/extended/cases/core.py`, especially `ValidateSavedDuelData` and neighboring card palette routines.

## Non-goals
Do not edit shared `src/home`, `src/probe`, `tests/cases`, tooling, build files, or other overlays. Do not add stubs for removed hardware paths or run ninja, cmake, just, emulators, git, or jj.

## Acceptance
- [ ] Assigned C has no removed serial/link symbols :: `! grep -nE 'SetOppAction_SerialSendDuelData|ExchangeRNG|SerialRecv|SerialSend|DuelTransmissionError|CanArenaCardUseNonResidualAttack|ValidateSavedNonLinkDuelData' src/profiles/extended/home/core.c src/profiles/extended/home/hand_pokemon.c src/profiles/extended/home/start.c src/profiles/extended/probe/core.c src/profiles/extended/probe/hand_pokemon.c`
- [ ] Overlay units pass :: `python3 tools/overlay_check.py core hand_pokemon start`
- [ ] Case modules import :: `python3 -c "import importlib.util,sys; sys.path.insert(0,'.'); [(__import__('importlib').util.spec_from_file_location('m',p)) for p in []]"`
- [ ] Repo green check is run by the integrator after landing :: `python3 tools/overlay_check.py core hand_pokemon start`
