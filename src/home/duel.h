#ifndef POKETCG_HOME_DUEL_H
#define POKETCG_HOME_DUEL_H

#include <stdint.h>

#include "home/process_text.h"

/* Both return the asm's three live exit registers: a, de (the destination, backed
 * up onto the terminator) and hl (the source, advanced past it). */
CopyTextResult CopyPlayerName(uint16_t de);
CopyTextResult CopyOpponentName(uint16_t de);

#endif
