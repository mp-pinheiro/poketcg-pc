# Goal
Port the Extended `process_text`, `print_text`, `write_number`, `text_box`, `copy_card_name`, and `naming` basenames into their overlay trios and Extended cases so every Extended routine in scope matches the ROM oracle, passes audits and mutation checks, and advances the new-game completion verification.

# Files in scope
src/profiles/extended/home/process_text.c and .h: Extended text processing bodies and declarations.
src/profiles/extended/probe/process_text.c: Extended process_text adapters and table.
tests/profiles/extended/cases/process_text.py: Extended process_text oracle cases and mutations.
src/profiles/extended/home/print_text.c and .h: Extended text printing bodies and declarations.
src/profiles/extended/probe/print_text.c: Extended print_text adapters and table.
tests/profiles/extended/cases/print_text.py: Extended print_text oracle cases and mutations.
src/profiles/extended/home/write_number.c and .h: Extended number formatting bodies and declarations.
src/profiles/extended/probe/write_number.c: Extended write_number adapters and table.
tests/profiles/extended/cases/write_number.py: Extended write_number oracle cases and mutations.
src/profiles/extended/home/text_box.c and .h: Extended text box bodies and declarations.
src/profiles/extended/probe/text_box.c: Extended text_box adapters and table.
tests/profiles/extended/cases/text_box.py: Extended text_box oracle cases and mutations.
src/profiles/extended/home/copy_card_name.c and .h, probe/copy_card_name.c, tests/profiles/extended/cases/copy_card_name.py: Extended card-name overlay quartet.
src/profiles/extended/home/naming.c and .h, probe/naming.c, tests/profiles/extended/cases/naming.py: Extended naming overlay quartet.

# Contracts
Use the Extended asm under `poketcg-extended/src/**` as truth. Follow `docs/factory-contract.md` for bus access, numeric case addresses, adapter marshalling, preservation, and mutations. Run `just extended-check <basename>`, `lint_constants.py --profile extended`, `lint_adapters.py`, and `audit_oracle_cases.py --stage routine --only <basename>` per the lane brief.

# Pattern to copy
Use `src/profiles/extended/home/glossary.c`, `src/profiles/extended/probe/glossary.c`, and `tests/profiles/extended/cases/glossary.py` as the existing overlay, adapter, and case structure.

# Non-goals
Do not edit shared `src/home` or `src/probe`, vanilla cases, tools, build configuration, justfile, or another lane's overlays. Do not patch cross-lane callees or add stubs and shims.

# Acceptance
- [ ] Each target basename oracle-diffs clean :: `just extended-check <basename>`
- [ ] Target overlay constants and adapters lint clean :: `python3 tools/lint_constants.py --profile extended <files> && python3 tools/lint_adapters.py <probe>`
- [ ] Target cases pass the routine audit :: `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only <basename>`
- [ ] Every changed C body has a RED mutation :: `POKETCG_PROFILE=extended python3 tools/run_mutation.py <Fn> tests/profiles/extended/cases/<basename>.py --build build-ext-LaneText`
- [ ] New-game completion evidence is recorded :: `POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-LaneText python3 tools/completion/session.py verify new-game --no-publish`
