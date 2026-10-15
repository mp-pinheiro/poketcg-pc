# Porting a profile

A profile adds one pinned TCG1 ROM to the native port. Its C code is the shared `src/home` and `src/probe` code composed with named routine blocks under `src/profiles/<profile>/`. Its cases use the same routine-level rule: shared modules supply unchanged routines, while profile modules contain only routines with profile-specific evidence.

## Pin the source inputs

Add the profile to `profiles/profiles.json`. Record the source repository, checkout directory, full commit, ROM, map, sym and RGBDS version under `source`; record the binary and probe names, generated-header path, default build directory, overlay root and removed basenames under `build`; record inventory and data-pack paths under `artifacts`; record oracle, session, case and mutation-receipt namespaces under `evidence`; and record save identity and supported features under `save` and `features`.

Clone and build the pinned source with `just bootstrap-profile <profile>`. The bootstrap checks out the catalog commit, uses the catalog's RGBDS version, applies `profiles/<profile>/source-fixes.patch` when present, verifies the resulting ROM hash and reproducibility, then records the hash in the catalog.

The generated CMake option is `POKETCG_ENABLE_<PROFILE_IN_UPPERCASE>`. `just build-profile <profile>` regenerates the inventory and data pack, configures the profile and builds its catalog `binary` and `probe` targets. For a probe-only build, run `cmake -G Ninja -B build-<profile> -DPOKETCG_ENABLE_<PROFILE_IN_UPPERCASE>=ON -DPORT_FILES=""`, then build those two targets with Ninja. CMake gets the source, ROM, map, sym, inventory, data pack and override root from `profiles.json` and `tools/profile_path.py`.

## Find the routines to port

Run `POKETCG_PROFILE=<profile> python3 tools/profile_audit.py --routines --all`. The audit compares normalized assembly routines, not basenames. `semantic` and `new` routines need profile-specific C or an explicit `===` declaration when shared C already implements them; `identical`, `local-label`, `tail-call`, `jump-to-next` and `constant-spelling` routines use shared code; `removed` routines are declared with `---` when shared C still defines them.

Check the profile's source and sym files before porting. Confirm each normalized routine's register contract, data layout and routine location against the profile ROM. A routine that moved between asm files keeps its C block at its existing shared path.

## Add routine overrides

Start an override file with `just profile-override <profile> <basename> <routine>`. The shared and profile files use `/* >>> factory <Routine> */` blocks. Replacing a block uses the same routine name; new blocks follow the nearest preceding shared block. A `/* --- factory <Routine> */` directive removes a routine from the composed unit, and a `/* === factory <Routine> */` directive records that shared C serves the routine without a replacement block.

Use the same block grammar for declarations in `src/home/*.h` and probe adapters in `src/probe/*.c`. Composition is checked with `python3 tools/compose_profile.py check --profile <profile>`; block boundaries are checked with `python3 tools/factory_blocks.py lint`.

After a shared fix makes override bodies identical, run `python3 tools/compose_profile.py deduplicate --profile <profile>`. It replaces identical C bodies with shared declarations and removes identical header and adapter blocks. Update affected mutation sources to the shared file and regenerate their receipts.

Shared C uses `CardId` and the card-id accessors for semantic IDs. `nine_bit_card_ids` selects `CardId`'s width and whether the accessors read or write one byte or two. Shared C names ROM banks and data with generated `<Label>_BANK` and `<Label>_ADDR` symbols. `lint_card_ids.py` resolves `CardId` locals, parameters and calls by lexical scope and rejects any `uint8_t` declaration, assignment, return or cast whose complete operand still carries a semantic ID. Byte extraction for registers or storage uses an explicit `id & 0xFFu` or `id >> 8`, and boolean comparisons remain byte-sized. A routine that leaves the compared byte in `a` after `cp` or `cp16` returns `card_id_compare_a(id, CONSTANT)`, which yields the high byte when a nine-bit compare rejects on it. Run `python3 tools/lint_card_ids.py` and `python3 tools/lint_placement.py` after changing these paths.

The CardId checker retains semantic-ID provenance through wide integer aliases such as `uint16_t`. Console restrictions use `cgb_only`; behavior differences unrelated to ID width use their own feature or named-part constant rather than `nine_bit_card_ids`.

## Write cases for the changed routines

Shared case modules resolve RAM addresses from the active profile's sym file with `sym("wVariable")` or `sym("wVariable") + offset`. `python3 tools/case_symbols.py --profile <profile>` rewrites a profile's case namespace, and `python3 tools/lint_case_literals.py` rejects raw RAM addresses in all profile case namespaces.

Use `const("NAME")` and `text_id("NameText")` for generated constants and text identifiers. The constant generator includes `deck_const` declarations and their derived `_DECK_ID` values.

A profile case module imports the shared records with `inherit("<basename>", remove=(...))`, then defines only its own routines in `OWN`. Routines with unchanged assembly and no profile-specific C use the shared cases. Routines absent from the profile ROM are listed in `remove`. The `deck_entry(index, card_id)` helper in `tests/cases/_symbols.py` writes one or two bytes according to `nine_bit_card_ids`; profile-specific layout helpers belong there or in a small typed helper module, and case expectations remain tied to ROM behavior.

Use `sym_pointer("Callback")` for stored routine pointers and `map_script_offset(slot)` for map-script selectors whose entries are two or three bytes. A literal pointer or selector from another profile can name a different routine or the middle of an entry.

Raw reference captures retain the data layout and game state of their source profile. Shared case logic selects profile-native captures with `profile_fixture({...})`; the captures are data, not copied case modules. Generate a missing capture with `POKETCG_PROFILE=<profile> python3 tools/completion/session.py capture <session> --routine <routine> --out tests/profiles/<profile>/fixtures/<name>.json`. Preserve the original exercised path and observations when selecting an entry. An early-exit input cannot replace a live movement, script-dispatch or callback scenario.

Every overridden routine needs a profile mutation whose `before` text resolves to the override source and whose `after` mutation makes a case fail. Run `POKETCG_PROFILE=<profile> python3 tools/run_mutation.py <Routine> tests/profiles/<profile>/cases/<basename>.py --build build-<profile> --index <case-index>` and require `MUTATION_RED`. Mutation receipts are written to the namespace in `profiles.json`.

If the source documents profile-specific upstream fixes, add `profiles/<profile>/fixes.toml` with one row for each documented heading and revert proofs for fixed routines. Run `python3 tools/profile_fixes.py --profile <profile>` after the profile scoreboard is current.

## Verify the profile

Run `python3 tools/profile_audit.py`, `python3 tools/factory_blocks.py lint`, `python3 tools/compose_profile.py check --profile <profile>`, `python3 tools/lint_card_ids.py`, `python3 tools/lint_placement.py` and `python3 tools/lint_case_literals.py`.

Run `POKETCG_PROFILE=<profile> python3 tools/audit_oracle_cases.py --stage routine`, `POKETCG_PROFILE=<profile> python3 tools/audit_mutations.py`, then the profile's complete gbref and PyBoy case suites. Run the configured profile gates and every session in `evidence.session_namespace` before recording the profile as ready.

Run the vanilla `just oracle-release-gate` after shared C changes. The vanilla sparse data-pack hash and size are fixed in `profiles/profiles.json`; a profile port must leave both unchanged.
