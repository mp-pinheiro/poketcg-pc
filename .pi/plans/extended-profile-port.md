# Extended profile port context

## Goal
Add an isolated native Pokémon TCG Extended profile at pinned upstream v2.0.0, preserving vanilla outputs and paths, with profile-aware builds, generated data, oracle evidence, 9-bit cards, presentation and behavior ports, tagged saves, launcher selection, and a blocked public package until permission is recorded.

## Files in scope
- CMakeLists.txt: profile target construction and generated include roots.
- justfile: bootstrap, build, package, launcher, and profile gates.
- profiles/profiles.json: build-time profile catalog and immutable pins.
- profiles/extended/provenance.toml: source attribution and distribution status.
- tools/profiles.py: selected-profile paths and metadata.
- tools/gen_layout.py, tools/gen_symbols.py, tools/gen_data.py: selected ROM headers and packs.
- tools/profile_audit.py, tools/check_profile_distribution.py: source and package gates.
- tools/progress/inventory.py and dispatch generators: profile inputs.
- src/home/card_id.h and card data/deck/collection overlays: CardId and 9-bit paths.
- src/persistence.[ch]: PKSR v1/v2 profile validation.
- src/launcher.c and launcher headers: SDL chooser and child execution.
- tests/profiles/extended and tests/sessions/extended: boundary, presentation, behavior, and campaign evidence.
- README.md: local bootstrap and profile selection.

## Contracts
- AGENTS.md: four-file ownership, jj-only VCS, real runtime verification.
- docs/port-contract.md: memory model, adapter signatures, case coverage, mutation evidence.
- docs/factory-contract.md: generated case/module format.
- docs/grind.md: no ROM/data mixing and verification discipline.
- Vanilla pack hash, ROM hash, and size are fixed by the approved plan.
- Extended packaging must fail without recorded written permission; vanilla packaging remains unchanged.

## Pattern to copy
Use the existing vanilla CMake target and `tools/gen_data.py` sparse-pack pipeline as the implementation pattern, retaining current vanilla names and on-disk paths.

## Non-goals
- Do not change vanilla save bytes, ROM/data-pack hashes, package contents, case paths, or default direct-game behavior.
- Do not publish Extended code or assets without permission evidence.
- Do not add profile-specific `#ifdef` branches inside shared game routines or bundle ROM/disassembly artifacts.

## Acceptance
Current results belong in source-bound release and profile evidence. The acceptance commands are:

- Catalog and selected-path parsing work :: python3 tools/profiles.py --profile vanilla
- Vanilla build remains green :: POKETCG_BUILD=build just build
- Extended source/bootstrap and profile build work :: just build-extended
- Extended routine gate is clean :: POKETCG_PROFILE=extended POKETCG_BUILD=build-extended just oracle-fn-gate
- Distribution block is enforced :: ! just appimage-profiles
- Save and selector smoke paths work :: just build-profiles
- Repository green-check passes :: just build