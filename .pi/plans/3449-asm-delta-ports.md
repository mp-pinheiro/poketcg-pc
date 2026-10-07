# Issue #3449: make mod ports cost only their asm delta

Issue body: `fj issue view 3449`. Measurements behind this plan: `/tmp/i3449/` (overlay block table `overlays/table.md`, asm routine classes `asm/routines.tsv`, lane maps `Map*.md`).

## Measured baseline (2026-10-07)

- Extended overlays: 139 basenames, 556 files. `.c` pairs 137: 46 identical, 12,912 changed lines of 65,708.
- Asm, over inventory code functions (vanilla plus Extended, 3,207): 1,476 identical, 330 differ only by tail calls, 40 only by constant spelling, 11 only by a jump to the next label, 12 identical but moved, 582 semantic (11 moved), 611 vanilla-only, 145 Extended-only.
- Extended C blocks of semantic routines: 489 blocks, 19,221 lines (98 identical to shared). Extended-only blocks: 129, 1,529 lines. Differing blocks whose asm is identical or normalizable: 59, about 1,200 lines.
- Shared C: 50 `.c` files have no factory block, 104 define routines outside blocks, 95 probe files have adapters outside blocks, markers are broken in 8 shared and 13 overlay files, nothing lints C markers.

## Decisions

1. Block grammar. Every top-level construct of `src/home/*.c|h` and `src/probe/*.c` lives in a named block. `/* >>> factory <Routine> */` for an asm routine (same name across `.c`, `.h`, probe), `/* >>> part <name> */` for everything else (include runs, defines, typedefs, static helpers, tables, the probe table). Only include guards and blank lines sit outside blocks. Existing tools match `factory (\w+)` only, so `part` blocks stay invisible to case and hatch audits.
2. Override files keep their paths (`<overlay_root>/home/<b>.c|h`, `<overlay_root>/probe/<b>.c`) and hold only blocks. A same-name block replaces the shared one; a new block is placed after the nearest preceding override block that exists in shared (head if none); `/* --- factory <Name> */` or `/* --- part <name> */` removes a block; `/* === factory <Name> */` declares that a routine whose normalized asm differs is served by the shared C. The probe table is composed: shared rows whose adapter survives, plus the rows of the override's `part probe_entries` block.
3. `tools/compose_profile.py` writes composed sources to `${profile_build_root}/compose/{home,probe}`; CMake compiles those for every basename with an override file and puts `compose` first on the include path. Vanilla compiles shared files directly. Every path comes from `profiles.json` (`overlay_root`), nothing hardcodes `extended`.
4. Conversion is proven by text: for every overlay file, `compose(shared, override)` must reproduce the pre-conversion overlay byte for byte, so the Extended binary is unchanged. Wrapping is proven by object code: `.text` of vanilla and Extended binaries unchanged.
5. `profile_audit.py` normalizes asm (comments, case, local-label names, `jr`/`jp`, `call X`+`ret` and non-local `jp X` as one tail call, farcall/bank1call tail calls, jumps to the next label or routine, constants evaluated per tree with `gen_constants.evaluate` when the value is spelled differently, `lb`/split 16-bit loads, `ld`/`ldh` to HRAM), keyed by routine name over the inventories. It fails on a routine whose normalized body differs, or that is new, without an override, removal or `===` declaration, and on a vanilla routine missing from the profile whose C block is not removed.
6. Card-id width comes from features: CMake turns `profiles.json` features into `generated/profile_features.h` (`PROFILE_NINE_BIT_CARD_IDS`, `PROFILE_THREE_PALETTE_CARDS`, `PROFILE_MULTI_BANK_SCRIPTS`), replacing `POKETCG_PROFILE_EXTENDED` in shared code.
7. Cases resolve addresses with `tests/cases/_symbols.py` (stdlib only, avoids the shadowed `copy`/`random`/`math`/`time`): `sym("wFoo") + n` against the active profile's sym file, cached per process. Case groups compose per routine: shared module, minus the profile's removed routines, updated by the profile module's routines.
8. Harness defaults come from the profile: `entry_sp` defaults to the reserved stack window in every lane, fixture holes and spans resolve by symbol name, and every lane advances a `keys` timeline once per completed joypad poll.

## Phases

1. Audit: normalized routine diff (decision 5).
2. Blocks: `tools/factory_blocks.py` parser, marker lint, marker repair, wrap pass on shared and overlay trees; object-code identity.
3. Compose: composer, CMake, every tool that reads overlay paths, conversion of the Extended overlays, receipts regenerated for changed mutation sources.
4. Shared code: placement-constant lint and fixes (action 6), card-id width lint and fixes (action 3); delete override blocks that become identical; vanilla mutations re-anchored with receipts.
5. Cases: symbol helper, codemod of vanilla case modules with record identity, raw-literal lint, per-routine case composition, Extended case modules reduced to overridden routines, `transpose_cases.py` and `relocate_case_pointers.py` deleted.
6. Harness: decision 8, DevolutionSpray cases 1 and 2 back on `[0,1,0,2,0,1,0,2]` as primary evidence.
7. Docs and generality: `docs/porting-a-profile.md`, `extended_fixes.py` generalized, bootstrap and CMake generic.
8. Verification: every acceptance item of the issue, vanilla release gate, every Extended gate and session.

## Rules for every lane

- jj only, integrator commits; lanes never run jj or git, `just build`, `oracle-fn-gate`, the release gate or `test_leaves --all`.
- Private build dirs, `POKETCG_NINJA_JOBS=-j1`; memory is about 5 GB free.
- No authored comments in C or Python; no profile `#ifdef` in shared code.
- Vanilla pack sha256 `b3c1036a2ac2b410f47a4ed47fd28264ae7087a84c29fc6bbc14864155a92d27`, size 945154.
