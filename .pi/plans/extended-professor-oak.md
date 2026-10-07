# Goal
Bring the Extended `AIDecide_ProfessorOak` overlay and case coverage to oracle parity for the extended-fixes Wonders of Science fixture, including Extended deck-specific scoring and fixed basic-Pokemon hand scoring.

# Files in scope
- `src/profiles/extended/home/trainer_cards.c`: Professor Oak C body and any owned scoring helper corrections.
- `src/profiles/extended/probe/trainer_cards.c`: existing Professor Oak marshal adapter; inspect only unless signature changes.
- `tests/profiles/extended/cases/trainer_cards.py`: add and configure the extended-fixes entry fixture and mutation case ids.
- `tests/profiles/extended/fixtures/extended-fixes-aidecide-professor-oak-entry.json`: captured entry fixture input.
- `poketcg-extended/src/engine/duel/ai/trainer_cards.asm`: authoritative Extended implementation and callees.

# Contracts
- Follow `local://extended-lane-brief.md` for lane setup, overlay-only edits, fixture holes/LCDC, callee reporting, no extra comments, and report format.
- Follow `docs/factory-contract.md` for bus access, numeric Python addresses, case shape, and RED mutations.
- Run `python3 tools/overlay_check.py trainer_cards` after each C edit; use `just extended-check-fn AIDecide_ProfessorOak` while iterating and `just extended-check trainer_cards` at the end.

# Pattern to copy
Imitate `_PROFESSOR_OAK` fixture construction and `_fixture_case` split-read handling in `tests/profiles/extended/cases/energy.py` and nearby trainer-card cases, preserving numeric addresses and generated-header symbols in C.

# Non-goals
Do not edit shared vanilla files, tools, generated files, other basenames, or callees outside `trainer_cards`; do not change fixture data, hide live oracle failures, seed reserved frame ranges, or add authored comments.

# Acceptance
- [ ] New extended-fixes case is present with required holes/LCDC/read splits and compares `a`, `f` :: `python3 -c "from tests.profiles.extended.cases import trainer_cards; assert any('extended-fixes-aidecide-professor-oak-entry' in repr(x) for x in trainer_cards.CASES['AIDecide_ProfessorOak'])"
- [ ] Professor Oak oracle parity :: `just extended-check-fn AIDecide_ProfessorOak`
- [ ] Whole trainer_cards parity :: `just extended-check trainer_cards`
- [ ] Constants and adapter lint :: `python3 tools/lint_constants.py --profile extended src/profiles/extended/home/trainer_cards.c src/profiles/extended/home/trainer_cards.h src/profiles/extended/probe/trainer_cards.c && python3 tools/lint_adapters.py src/profiles/extended/probe/trainer_cards.c`
- [ ] Case audit :: `POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only trainer_cards`
- [ ] Professor Oak mutation RED :: `python3 tools/run_mutation.py AIDecide_ProfessorOak tests/profiles/extended/cases/trainer_cards.py --build build-ext-LaneAIOak --index <n>`
- [ ] Repository green-check item :: `just extended-check trainer_cards`
