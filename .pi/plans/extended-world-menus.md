# Extended world and menu lane

## Goal
Close Extended oracle failures for auto_deck_machines, credits, give_booster_pack, input_name, mail, medal, music, print_stats, promotional_card, sfx, deck_configuration, and deck_selection by porting overlays and cases from Extended assembly, with clean checks and mutation evidence.

## Files in scope
- src/profiles/extended/home/{auto_deck_machines,credits,give_booster_pack,input_name,mail,medal,music,print_stats,promotional_card,sfx,deck_configuration,deck_selection}.{c,h} — Extended overlay implementations and signatures.
- src/profiles/extended/probe/{auto_deck_machines,credits,give_booster_pack,input_name,mail,medal,music,print_stats,promotional_card,sfx,deck_configuration,deck_selection}.c — probe adapters and tables.
- tests/profiles/extended/cases/{auto_deck_machines,credits,give_booster_pack,input_name,mail,medal,music,print_stats,promotional_card,sfx,deck_configuration,deck_selection}.py — numeric oracle cases and mutation declarations.
- docs/factory-contract.md — bus, signatures, adapters, case, and mutation contracts.

## Contracts
Use generated Extended headers and Extended assembly as truth. Keep factory markers and source-range comments. Bus access uses gb_read8, gb_write8, and rom_ptr. Adapters marshal only. Cases include required zero, poison, and boundary coverage without reserved oracle-frame RAM. Verify syntax after header or signature changes with tools/overlay_check.py. Do not add prose comments.

## Pattern to copy
Use src/profiles/extended/home/print_stats.c and tests/profiles/extended/cases/print_stats.py for current overlay and case structure.

## Non-goals
Do not edit shared src/home or src/probe files, other profiles, tools, justfile, CMake files, or another lane's overlays. Do not run forbidden global gates or version-control commands. Do not patch cases to hide incorrect C behavior.

## Acceptance
- [ ] auto_deck_machines oracle clean :: just extended-check auto_deck_machines
- [ ] credits oracle clean :: just extended-check credits
- [ ] give_booster_pack oracle clean :: just extended-check give_booster_pack
- [ ] input_name oracle clean :: just extended-check input_name
- [ ] mail oracle clean :: just extended-check mail
- [ ] medal oracle clean :: just extended-check medal
- [ ] music oracle clean :: just extended-check music
- [ ] print_stats oracle clean :: just extended-check print_stats
- [ ] promotional_card oracle clean :: just extended-check promotional_card
- [ ] sfx oracle clean :: just extended-check sfx
- [ ] deck_configuration oracle clean :: just extended-check deck_configuration
- [ ] deck_selection oracle clean :: just extended-check deck_selection
- [ ] overlay and case lint plus audit clean :: python3 tools/lint_constants.py --profile extended ... && python3 tools/lint_adapters.py ... && POKETCG_PROFILE=extended python3 tools/audit_oracle_cases.py --stage routine --only ...
- [ ] repository green check :: just extended-check auto_deck_machines credits give_booster_pack input_name mail medal music print_stats promotional_card sfx deck_configuration deck_selection
