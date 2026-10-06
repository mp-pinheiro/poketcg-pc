## Goal
Port the Extended versions of removed-link callers in the eleven assigned overlays so they compile and link without Gift Center, serial-reset, SGB, printer, Card Pop, saved-duel, or link-frame symbols.

## Files in scope
src/profiles/extended/home/deck_machine.c|h — remove Extended-deleted Gift Center routines.
src/profiles/extended/probe/deck_machine.c — remove deleted adapters and table rows.
tests/profiles/extended/cases/deck_machine.py — remove deleted contracts, cases, and mutations.
src/profiles/extended/home/map.c|h — port the Extended event table and dispatch.
src/profiles/extended/probe/map.c — remove deleted event adapter and update table.
tests/profiles/extended/cases/map.py — remove deleted event cases.
src/profiles/extended/home/scripting.c|h — port the Extended script command path.
src/profiles/extended/probe/scripting.c — remove deleted script adapters if needed.
tests/profiles/extended/cases/scripting.py — update deleted routine entries.
src/profiles/extended/home/common.c|h — prune wrappers absent from Extended.
src/profiles/extended/probe/common.c — prune absent wrapper adapters.
tests/profiles/extended/cases/common.py — prune absent wrapper entries.
src/profiles/extended/home/challenge_machine.c — use DiscardSavedDuelData.
src/profiles/extended/home/empty_screen.c — remove SGB branch.
src/profiles/extended/home/frames.c — port DoFrame dispatch without link target.
src/profiles/extended/home/game_loop.c — port GameLoop without ResetSerial.
src/profiles/extended/home/input.c — port ReadJoypad without ResetSerial.
src/profiles/extended/home/start.c — port Start without ResetSerial.
src/profiles/extended/home/time.c — port timer handler without serial path.

## Contracts
Use docs/factory-contract.md: bus accesses use gb_read8/gb_write8, exact register outputs, tabs, and existing factory markers.
Use the Extended assembly under poketcg-extended/src as behavioral truth; absent labels are deleted, not stubbed.
Only assigned overlay C, H, probe, and case files may change. Do not run link, emulator, ninja, or git checks.

## Pattern to copy
Use src/profiles/extended/home/map.c and src/profiles/extended/home/time.c existing factory blocks for bus-backed register modeling and bank restoration.

## Non-goals
Do not edit shared src/home files, other profile overlays, build files, tools, or unrelated routines. Do not preserve removed hardware paths or add compatibility shims.

## Acceptance
- [ ] Removed-name grep is empty over assigned home and probe files :: grep -rn 'GiftCenter\\|ExchangeRNG\\|ResetSerial\\|SendSGB\\|ClearSavedDuel\\|HandlePrinterMenu\\|_DoCardPop\\|_PreparePrinterConnection\\|_PrintCardList\\|_PrintDeckConfiguration\\|_ReceiveCard\\|_ReceiveDeckConfiguration\\|_RequestToPrintCard\\|_SendCard\\|_SendDeckConfiguration\\|_SetUpAndStartLinkDuel\\|LinkOpponentTurnFrameFunction\\|SerialTimerHandler\\|Func_fcad' src/profiles/extended/home/{deck_machine,map,scripting,common,challenge_machine,empty_screen,frames,game_loop,input,start,time}.{c,h} src/profiles/extended/probe/{deck_machine,map,scripting,common,challenge_machine,empty_screen,frames,game_loop,input,start,time}.c
- [ ] Every assigned translation unit passes syntax replay :: python3 tools/overlay_check.py deck_machine map scripting common challenge_machine empty_screen frames game_loop input start time
- [ ] Repository green-check item :: python3 tools/overlay_check.py deck_machine map scripting common challenge_machine empty_screen frames game_loop input start time