#ifndef POKETCG_HOME_DUEL_H
#define POKETCG_HOME_DUEL_H

#include <stdint.h>

#include "home/process_text.h"

/* Both return the asm's three live exit registers: a, de (the destination, backed
 * up onto the terminator) and hl (the source, advanced past it). */
CopyTextResult CopyPlayerName(uint16_t de);
CopyTextResult CopyOpponentName(uint16_t de);

/* Duelist-variable layer (duel.asm:1316-1337): reads duelvar `a` of the current
 * turn holder / the other player. Every duel-engine routine builds on these.
 * Exit a is the byte read; exit hl is the address it was read from. */
typedef struct {
	uint8_t a;
	uint16_t hl;
} DuelistVarResult;
DuelistVarResult GetTurnDuelistVariable(uint8_t a);
DuelistVarResult GetNonTurnDuelistVariable(uint8_t a);
void SwapTurn(void);

#endif
