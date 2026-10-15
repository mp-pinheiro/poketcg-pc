# Porting a profile

This page owns profile authoring: catalog identity, composed source, profile-native cases, evidence isolation, and readiness gates. Player profile selection and saves belong in [playing](playing.md); build and packaging prerequisites belong in [building](building.md). The shared translation and memory invariants belong in [port-contract](port-contract.md), and quartet/output derivation rules belong in [factory-contract](factory-contract.md).

## Catalog and source identity

Add the profile to `profiles/profiles.json`. Record its source repository, checkout, full commit, ROM, map, sym file, and RGBDS version; build binary/probe names, generated header, build directory, overlay root, and removed basenames; inventory and data-pack paths; oracle, session, case, and mutation-receipt namespaces; and save identity and supported features.

`just bootstrap-profile <profile>` checks out the catalog commit, uses the pinned RGBDS version, applies an optional `profiles/<profile>/source-fixes.patch`, verifies ROM hash and reproducibility, and records the hash in the catalog. Build prerequisites and the normal single- or multi-profile build commands are owned by [building](building.md).

`profiles.json` and `tools/profile_path.py` are the source of profile paths and identities. Keep each profile's generated inventory, data pack, save identity, cases, fixtures, sessions, and mutation receipts in its own configured namespace. Never let one profile's evidence or generated outputs masquerade as another's.

## Routine composition

Run `POKETCG_PROFILE=<profile> python3 tools/profile_audit.py --routines --all`. The audit compares normalized assembly routines, not filenames. Semantic or new routines need profile-specific C or an explicit shared implementation declaration; identical, local-label, tail-call, jump-to-next, and constant-spelling differences use shared code; routines removed from a profile use removal declarations where shared C still defines them. Check the profile ROM and symbols for register contracts, data layout, and routine locations before authoring. A moved assembly routine keeps its C block at its existing shared path.

Shared source and profile overlays use paired named blocks:

| Block | Marker pair | Content |
|---|---|---|
| Routine | `/* >>> factory <Routine> */` / `/* <<< factory <Routine> */` | Routine, declaration, or probe adapter. |
| Named part | `/* >>> part <name> */` / `/* <<< part <name> */` | Includes, defines, types, helpers, and tables. |

A profile block replaces the shared block of the same name. A new block follows the nearest preceding block named by its fragment. `/* --- factory <Routine> */` removes a routine; `/* === factory <Routine> */` declares that shared C already implements it.

Keep shared routines profile-neutral. Express differences through overlays, named parts, and the appropriate feature axis; do not add per-profile `#ifdef` branches inside shared game logic. Start an override with `just profile-override <profile> <basename> <routine>`.

Check composition with `python3 tools/compose_profile.py check --profile <profile>` and block boundaries with `python3 tools/factory_blocks.py lint`. After a shared fix makes override bodies identical, `python3 tools/compose_profile.py deduplicate --profile <profile>` replaces identical C bodies with shared declarations and removes identical header/adapter blocks. Update affected mutation sources and regenerate receipts after deduplication.

## Card IDs and cases

Shared C uses `CardId` and card-ID accessors for semantic IDs. The `nine_bit_card_ids` feature determines ID width and whether accessors read or write one or two bytes.

- Use generated `<Label>_BANK` and `<Label>_ADDR` symbols for ROM data.
- Do not narrow a still-semantic ID to `uint8_t`. The lint follows lexical scope and wide integer aliases.
- Extract a byte intentionally with `id & 0xFFu` or `id >> 8`; boolean comparisons remain byte-sized.
- Use `card_id_compare_a(id, CONSTANT)` when returning the byte compared by `cp` or `cp16`; a rejected nine-bit comparison must expose the high byte.
- Use `cgb_only` for console restrictions. Unrelated behavior needs its own feature or named-part constant, not `nine_bit_card_ids`.

Case modules resolve RAM with `sym("wVariable")` or `sym("wVariable") + offset`; use `const("NAME")` and `text_id("NameText")` for generated constants and text identifiers. `python3 tools/case_symbols.py --profile <profile>` rewrites the profile case namespace and `python3 tools/lint_case_literals.py` rejects raw RAM addresses. Use `sym_pointer("Callback")` for stored routine pointers and `map_script_offset(slot)` for variable-width map-script selectors.

A profile case module imports shared records with `inherit("<basename>", remove=(...))` and declares profile-specific records in `OWN`. Unchanged routines use inherited cases; absent routines go in `remove`. Do not add a profile module when it owns or removes nothing: the profile loader uses the shared module directly.

`deck_entry(index, card_id)` writes the profile-correct one- or two-byte ID. Shared schema inventories, including `SCHEMA2_CASES`, are derived; never hand-author derived entries.

## Fixtures and proof inputs

Reference captures retain the data layout and game state of their source profile. Shared case logic selects native captures with `profile_fixture({...})`; fixtures are data, not copied case modules. Generate a missing capture with `POKETCG_PROFILE=<profile> python3 tools/completion/session.py capture <session> --routine <routine> --out tests/profiles/<profile>/fixtures/<name>.json`. Preserve the exercised path and observations: an early exit cannot substitute for live movement, script dispatch, or callback behavior.

Every overridden routine needs a profile mutation whose `before` text resolves to the override source and whose `after` mutation causes a case failure. Run `POKETCG_PROFILE=<profile> python3 tools/run_mutation.py <Routine> tests/profiles/<profile>/cases/<basename>.py --build build-<profile> --index <case-index>` and require `MUTATION_RED`. Receipts belong in the profile's configured mutation namespace.

When source documentation records profile-specific upstream fixes, `profiles/<profile>/fixes.toml` records one row per documented heading and revert proofs for fixed routines. Run `python3 tools/profile_fixes.py --profile <profile>` only after the profile scoreboard is current.

## Gates and fixture variants

The implemented Extended gates are an example of separate proof obligations:

| Recipe | Contract |
|---|---|
| `just extended-boundary-gate` | Stress nine-bit IDs using the padded `CardPointers` fixture, lookup limits, collection, deck SRAM, and card UI. |
| `just extended-presentation-gate` | Require the configured presentation routines and full recorded sessions. |
| `just extended-animation-gate` | Verify animation/SFX scenes derived from confirmed session evidence. |
| `just extended-fixes-gate` | Prove documented upstream fixes and their behavioral reverts. |
| `just extended-reference-gate` | Verify the required profile sessions, fields, ratchets, and fixture variants. |

The boundary fixture pads `CardPointers` through `0x1ff`, checks `0x00fe`, `0x00ff`, `0x0100`, and `0x01ff`, and rejects `0x0200`. It tests width and boundary behavior; it does not define a subset of supported routines.

Gate contracts live in profile TOMLs and executable recipes in `justfile`. Inspect both rather than copying another profile's paths.

Fixture variants preserve meaningfully different source-profile layouts or state. Select the correct native fixture for a case rather than coercing another profile's bytes. Campaign evidence is cumulative and depends on its configured session namespace; a partial campaign, fixture-only check, or stale scoreboard is not complete profile evidence.

## Readiness

Run `python3 tools/profile_audit.py`, `python3 tools/factory_blocks.py lint`, `python3 tools/compose_profile.py check --profile <profile>`, `python3 tools/lint_card_ids.py`, `python3 tools/lint_placement.py`, and `python3 tools/lint_case_literals.py`. Run `POKETCG_PROFILE=<profile> python3 tools/audit_oracle_cases.py --stage routine` and `POKETCG_PROFILE=<profile> python3 tools/audit_mutations.py`, then the configured complete gbref and PyBoy case suites, gates, and every session in `evidence.session_namespace`.

After shared C changes, run the vanilla `just oracle-release-gate`. The vanilla sparse data-pack hash and size are fixed in `profiles/profiles.json`; a profile port must leave both unchanged. Profile readiness requires the complete configured evidence set, not a changed scoreboard count alone.
