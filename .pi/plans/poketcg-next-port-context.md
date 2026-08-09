# Pokétcg sprite-animation Phase 2 context pack

## Goal

Resume from committed revision `b3a37679` and port all 22 global routines in `poketcg/src/engine/gfx/sprite_animations.asm`, including the prerequisite current-slot helper repair, to move the central oracle gate from 480/480 to exactly 502/502 without changing unrelated basenames.

## Files in scope

- `.pi/plans/poketcg-next-port-plan.md` — decision-complete execution spec; read first and follow top to bottom.
- `src/home/load_animation.c` — repair `GetFirstSpriteAnimBufferProperty` to honor `wWhichSprite`.
- `tests/cases/load_animation.py` — add slot 0/15/16/255 witnesses for that helper.
- `src/home/sprite_animations.c` — implement all 22 ASM bodies.
- `src/home/sprite_animations.h` — exact ABI and result types from the execution plan.
- `src/probe/sprite_animations.c` — literal one-call register marshalling.
- `tests/cases/sprite_animations.py` — zero, poison, boundary, SRAM, VRAM, OAM, and mutation-sensitive oracle fixtures.
- `tests/routines.py` — add only `ROUTINES["sprite_animations"]`, in ASM order.
- `docs/vision.md`, `docs/plan.md` — record the verified 502 gate after the feature commit.

## Contracts

- `AGENTS.md` — read the three required docs before C; private build directory; only the orchestrator runs the full gate; jj-only commits.
- `docs/port-contract.md` — 16-bit GB bus addresses, exact meaningful-register contracts, explicit oracle cases, adapter lint, and one RED/restored-PASS mutation per routine.
- `docs/vision.md` — C11/software-PPU architecture and phase ordering.
- `docs/plan.md` — current 480-routine baseline and the `W1-L` status row to add after landing.
- No `.substrate`, `substrate.json`, or `docs/contracts.md` is vendored; the repository-native central gate is `just oracle-diff-all`.

## Pattern to copy

Copy the four-file conventions from `src/home/load_animation.c`, `src/home/load_animation.h`, `src/probe/load_animation.c`, and `tests/cases/load_animation.py`; reuse their sprite buffer, frame pointer, OAM, ROM-bank, and probe patterns rather than introducing a second abstraction.

## Non-goals

Do not edit CMake, shared memory/probe code, generated headers, callers, neighbouring registry tuples, ROM-data-only gfx ASM, animation-engine core, menus, duel scenes, or any routine outside the 22-name tuple and the explicit helper repair.

## Acceptance

- [ ] fresh-machine disassembly available :: just bootstrap
- [ ] fresh-machine PyBoy environment available :: just oracle-venv
- [ ] warning-free integration build :: just build
- [ ] helper current-slot behavior matches PyBoy :: just oracle-diff GetFirstSpriteAnimBufferProperty
- [ ] every registered routine matches PyBoy :: just oracle-diff-all
- [ ] extracted data round-trips :: just data-verify
- [ ] replay remains deterministic :: just oracleb-replay
- [ ] gate green :: just oracle-diff-all
