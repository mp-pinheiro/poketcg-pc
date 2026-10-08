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
7. Docs and generality: `docs/porting-a-profile.md`, `profile_fixes.py` generalised from Extended, profile-driven bootstrap and CMake.
8. Verification: every acceptance item of the issue, vanilla release gate, every Extended gate and session.

## Rules for every lane

- jj only, integrator commits; lanes never run jj or git, `just build`, `oracle-fn-gate`, the release gate or `test_leaves --all`.
- Private build dirs and `POKETCG_NINJA_JOBS=-j1`. Check `omp.slice` cgroup headroom before spawning workers, language servers or runtime jobs; host `free -m` does not measure this cap.
- No authored comments in C or Python; no profile `#ifdef` in shared code.
- Vanilla pack sha256 `b3c1036a2ac2b410f47a4ed47fd28264ae7087a84c29fc6bbc14864155a92d27`, size 945154.

## Recovery checkpoint

- Live `omp.slice` limits were increased to 12 GiB memory and 12 GiB swap. Builds use `--parallel 1`; emulator, oracle and mutation runs stay serial. No memory-check loop is needed.
- `src/profiles/extended/home/scripting.c` now reproduces `FarCallHL` restoring caller AF. CMake uses `POKETCG_DISASM` for save-import inputs, and `tools/profile_path.py` honors `POKETCG_PROFILE`. The entry-stop path in `src/probe.c` truncates bank guards without unwinding the callee bank before snapshot.
- Verified current targeted paths: 26 movement/map cases in each profile; 22 Extended practice-scene cases with full returns (card page, attack, knockout, prize selection); six Extended Heal cases; five Sand Attack cases in each profile; four Slowbro cases in each profile; ten Extended deck-header, machine-entry and Nidoran cases. The earlier 7,920-case pass is not final acceptance.
- Shared Slowbro case 2 retains its original undamaged-arena guard; case 3 exercises a live counter transfer. The C API returns semantic AF rather than incidental clobbered register residue, and the final `a` comes from `AIMakeDecision`. Native practice captures reproduce the original Goldeen-versus-Machop board, HP 40/50 and play-area counts 2/1. Their completed-poll recordings replay to byte-identical entry snapshots.
- Native fixture aliases now cover movement, map scripts, text/menu callbacks, recoil, Heal, Slowbro, Sand Attack, AI evolution/damage/energy removal, the deck header, the visible save-machine entries and the trainer card page.
- CardId lint now rejects narrowed call results, variables and parameters, including multiline assignments and casts before comparisons. The reproduced regression tests pass; the current tree passes all three issue lints, and actual CLI negative examples reject a narrowed CardId, raw RAM literal, literal bank select and ROM-label offset. Shared Nidoran comparison now keeps the full CardId; its identical Extended block was removed and machine ownership declared.
- Composition and normalized assembly audit pass; the audit now resolves `EQUS` label constants (`PLAYER_TURN`), and a planted copy of the Extended checkout shows tail-call and constant-spelling edits pass while a semantic edit without an override fails. `profile_audit.py` audits every non-default catalog profile when no profile is named.
- Witness campaign: 640 overridden routines. 516 proved RED with existing mutations; 122 had never had a RED receipt. Those gaps were closed by stronger observation (full music state, VRAM, duel variables, `STACK_CANARY` for APU-only routines as in vanilla `music1`), by inheriting passing shared records instead of weak profile copies (HandleAfterDamageEffects, LoadTilesetGfx, ProcessSpecialTextCharacter, Func_c9c7, ScriptCommand_ShowCardReceivedScreen, GamblerEffect, HandleDeckBuildScreen), by Extended dispatch cases for GenerateBoosterEnergies, and by synthesized override mutations written into the profile modules. The Music_note adapter now takes the stream pointer from the stack. `/tmp/i3449/prove_overrides.py` (hash-bound receipts, PASS/PORT/PASS) is the acceptance runner.
- DevolutionSpray cases 1 and 2 keep `[0,1,0,2,0,1,0,2]` in the Extended module and pass gbref and PyBoy. Vanilla `_GetCardIDFromDeckIndex` mutation was re-anchored and is RED.
- Remaining acceptance: final witness proof, full Extended `oracle-fn-gate`, the five Extended gates and every Extended session, vanilla rebuild and `oracle-release-gate`, final deterministic review. Local `main` is conflicted with an upstream progress snapshot that also appends `site/data/history.jsonl`; resolve before any push.
