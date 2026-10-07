# Goal
Close all listed Extended effect_functions oracle failures by correcting cases from Extended asm or correcting C where it differs, then provide clean checks, RED mutation receipts, lint, and audit.

# Files in scope
- src/profiles/extended/home/effect_functions.c: Extended routine bodies under test.
- src/profiles/extended/home/effect_functions.h: Existing signatures for affected routines.
- src/profiles/extended/probe/effect_functions.c: Existing adapters and probe rows.
- tests/profiles/extended/cases/effect_functions.py: Affected cases, contracts, and MUTATIONS.
- poketcg-extended/src: authoritative Extended asm for each routine.
- docs/factory-contract.md: C, adapter, cases, and mutation contracts.

# Contracts
- Lane setup and per-basename loop: local://extended-lane-brief.md.
- Oracle cases require numeric addresses, input keys for waits, and oracle false evidence only when live execution cannot return.
- C uses generated Extended headers and bus access rules from docs/factory-contract.md.
- Run overlay_check after every C edit, named checks while iterating, full check at end.
- Every changed C routine needs a RED run_mutation receipt; lint_constants, lint_adapters, and routine audit must be clean.

# Pattern to copy
Use existing affected-routine blocks in src/profiles/extended/home/effect_functions.c and matching adapters/cases in the same basename, preserving factory markers and asm range comments.

# Non-goals
Do not edit shared src/home or src/probe files, tools, build scripts, other overlays, unrelated basenames, or add authored comments.

# Acceptance
- [ ] All 16 listed routines are clean or have exact asm-grounded oracle-false evidence :: just extended-check effect_functions
- [ ] Every changed C routine is mutation RED :: POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/effect_functions.py --build build-ext-<lane>
- [ ] Constants and adapters lint clean :: python3 tools/lint_constants.py --profile extended src/profiles/extended/home/effect_functions.c src/profiles/extended/home/effect_functions.h src/profiles/extended/probe/effect_functions.c && python3 tools/lint_adapters.py src/profiles/extended/probe/effect_functions.c
- [ ] Oracle case audit is clean :: POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only effect_functions
- [ ] Repo acceptance is green :: just extended-check effect_functions
