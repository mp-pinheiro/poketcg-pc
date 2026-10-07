# Goal
Close the remaining Extended oracle failures for AIMainTurnLogic in general and AIDoTurn_GeneralNoRetreat in general_no_retreat, preserving Extended assembly behavior, including the menu blink counter handling used by other AI fixture cases. Leave both basename groups at N/N clean with mutation, lint, and audit evidence.

# Files in scope
src/profiles/extended/home/general.c: AIMainTurnLogic implementation.
src/profiles/extended/home/general.h: General routine declarations if signatures change.
src/profiles/extended/probe/general.c: General probe adapters if output marshalling changes.
tests/profiles/extended/cases/general.py: General oracle cases, completion, holes, read split, and mutation.
src/profiles/extended/home/general_no_retreat.c: AIDoTurn_GeneralNoRetreat implementation.
src/profiles/extended/home/general_no_retreat.h: No-retreat routine declaration if needed.
src/profiles/extended/probe/general_no_retreat.c: No-retreat probe adapter.
tests/profiles/extended/cases/general_no_retreat.py: No-retreat oracle cases and mutation.

# Contracts
Extended asm in poketcg-extended/src is authoritative; compare vanilla only for case and call-flow patterns.
Use docs/port-contract.md and docs/factory-contract.md for bus access, flags, cases, completion, and mutation rules.
Follow local://extended-lane-brief.md setup, private build, per-basename checks, RED mutation receipts, lint, and audit requirements.
Do not edit shared src/home, src/probe, tests/cases, tools, justfile, or other overlays.

# Pattern to copy
tests/profiles/extended/cases/challenge_machine.py, especially schema migration and completion records for routines that cannot run to ret.

# Non-goals
Do not change the Extended assembly, shared implementations, generated headers, or unrelated AI basenames.
Do not add comments beyond existing factory markers and asm range comments.
Do not mask a wedge or alter cases to hide a C mismatch; use Extended-derived completions or expectations only when required.

# Acceptance
- [ ] Private Extended lane configured and incrementally built :: export POKETCG_PROFILE=extended POKETCG_BUILD=build-ext-general-ai POKETCG_NINJA_JOBS=-j2 && just extended-configure-lane && just build-extended-incremental
- [ ] General oracle group is clean :: just extended-check general
- [ ] General no-retreat oracle group is clean :: just extended-check general_no_retreat
- [ ] Constants and adapters lint clean :: python3 tools/lint_constants.py --profile extended src/profiles/extended/home/general.c src/profiles/extended/home/general.h src/profiles/extended/probe/general.c src/profiles/extended/home/general_no_retreat.c src/profiles/extended/home/general_no_retreat.h src/profiles/extended/probe/general_no_retreat.c && python3 tools/lint_adapters.py src/profiles/extended/probe/general.c src/profiles/extended/probe/general_no_retreat.c
- [ ] Oracle cases audit clean :: POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only general && POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only general_no_retreat
- [ ] Repository green check remains clean :: just extended-check-fn AIMainTurnLogic AIDoTurn_GeneralNoRetreat
