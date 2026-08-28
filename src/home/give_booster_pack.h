#ifndef POKETCG_HOME_GIVE_BOOSTER_PACK_H
#define POKETCG_HOME_GIVE_BOOSTER_PACK_H

#include <stdint.h>

void _PauseMenu_Exit(void);

/* >>> factory GiveBoosterPack */
/* poketcg/src/engine/menus/give_booster_pack.asm:1. The tail is
 * `pop af / ld [wd291], a / ret`, so exit a is the byte wd291 held on entry and
 * exit f is the caller's own flags, saved by the matching `push af`. */
typedef struct { uint8_t a; uint8_t f; } GiveBoosterPackResult;
GiveBoosterPackResult GiveBoosterPack(uint8_t a, uint8_t f);
/* <<< factory GiveBoosterPack */
#endif /* POKETCG_HOME_GIVE_BOOSTER_PACK_H */
