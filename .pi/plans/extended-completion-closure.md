# Goal
Finish Extended end to end, resolve every grounded implementation gap, keep published completion evidence truthful after daily snapshots, and verify every requirement before publication.

# Files in scope
- `tools/oracle/release_gate.py`: self-contained attestation validation and derived-file-independent source identity.
- `tools/completion/revision.py`: identical source revision selection under git and jj.
- `tools/progress/report.py`: dashboard completion and verification state from tracked attestations.
- `.forgejo/workflows/ci.yml` and `.forgejo/workflows/progress.yml`: cached RGBDS and pinned pret inputs, reproducible snapshots.
- `src/home/*.c|h` and `src/probe/*.c`: shared defects reproduced by audit witness cases.
- `src/profiles/extended/home/*.c|h` and `src/profiles/extended/probe/*.c`: Extended-specific assembly behavior and adapter conventions.
- `tests/cases/*.py` and `tests/profiles/extended/cases/*.py`: additive ROM-backed regression cases.
- `tools/lint_card_ids.py` and `tests/test_lint_card_ids.py`: semantic CardId provenance through integer aliases.
- `tools/gen_constants.py` and `tests/test_gen_constants.py`: exported `deck_const` values and opponent IDs; remove obsolete hand-coded deck constants.
- `tools/compose_profile.py` and `tests/test_compose_profile.py`: deduplicate identical blocks without moving additions ahead of their include anchors.
- `justfile`: honor `POKETCG_NINJA_JOBS` in all native builds and run routine gates serially by default.
- `tools/profile_path.py` and `tests/test_profile_path.py`: selected build roots and boundary variants must match the profile resolver.
- `tools/oracle/pyboy_oracle.py`, `pyboy_health.py`, `fingerprint.py`, dependency pins and `vendor/`: preserve SRAM mapper state during snapshots and correct the pinned emulator's JOYP selector bits.
- `.pi/plans/3449-asm-delta-ports.md`: replace stale recovery and open-risk claims after verification.
- `site/data/gate.json`, `site/data/progress.json`, `site/data/history.jsonl`: regenerated verified publication data.

# Contracts
- The user's completion criterion is Extended implemented end to end, no open gaps, and all requirements verified.
- Audit inputs are `/tmp/i3449/declared/index.json`, `findings-all.json`, and per-routine `.diff` files: 128 unique routines, 92 candidate matches, 36 candidate mismatches, plus shared defects noted inside matching findings. Reproduce findings before treating them as confirmed defects.
- Preserve the pinned Extended ROM's actual behavior, including upstream mistakes. Never edit cases, expectations, seeds or compare lists to conceal a mismatch.
- Follow `docs/porting-a-profile.md`: routine-level composition, symbolic fixtures, feature-generic shared C, and mutation witnesses for overrides.
- Existing tests remain; new tests must expose consumer-visible behavior. Lanes edit disjoint files in isolated jj workspaces and never commit.
- Memory-sensitive commands use one compiler or emulator per lane under explicit memory limits; all full-suite and session runs are serial.
- Forgejo is canonical. Publish with jj over HTTPS, verify quality/deploy and an actual snapshot execution.

# Pattern to copy
`tests/profiles/extended/cases/deck_machine.py` records a symbolic two-byte deck-header regression and a shared/override-resolved mutation; `tools/run_mutation.py` proves baseline PASS, mutation PORT, restored PASS.

# Non-goals
Do not change the pinned ROM or its content, add compatibility shims, duplicate complete shared case modules, weaken observations, or invent evidence. Vanilla data-pack bytes remain unchanged.

# Acceptance
Current results belong in source-bound release and profile evidence. The acceptance commands are:

- All audited declarations resolved with grounded per-routine evidence :: python3 tools/profile_audit.py --profile extended
- Composition and structural markers valid :: python3 tools/compose_profile.py check --profile extended && python3 tools/factory_blocks.py lint
- Symbolic cases and CardId widths valid :: python3 tools/lint_case_literals.py && python3 tools/lint_card_ids.py && python3 tools/lint_placement.py && python3 tools/lint_adapters.py
- Extended profile gates pass :: just extended-boundary-gate && just extended-presentation-gate && just extended-animation-gate && just extended-fixes-gate && just extended-reference-gate
- Completion evidence regenerated :: python3 tools/completion/completion.py chain
- Published progress matches tracked evidence :: python3 tools/progress/report.py check
- Repository release gate passes :: just oracle-release-gate
