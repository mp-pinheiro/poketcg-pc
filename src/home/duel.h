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

/* Deck-index lookup family (duel.asm:661-712, 762-777). Exit contracts derived
 * from each member's asm tail, not guessed:
 *  - _GetCardIDFromDeckIndex: a = id, hl = deck base + a
 *  - GetCardIDFromDeckIndex:   id in de, af/hl preserved
 *  - GetCardIDFromDeckIndex_bc: id in a and c, b = 0, hl preserved
 *  - GetCardInDuelTempList_OnlyDeckIndex: a = entry, hl preserved
 *  - GetCardInDuelTempList: a = entry, de = id, hl preserved */
typedef struct {
	uint8_t a;
	uint16_t hl;
} DeckCardResult;
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} DeckEntryResult;
DeckCardResult _GetCardIDFromDeckIndex(uint8_t a);
uint16_t GetCardIDFromDeckIndex(uint8_t a);
DeckCardResult GetCardIDFromDeckIndex_bc(uint8_t a, uint16_t hl);
DeckCardResult GetCardInDuelTempList_OnlyDeckIndex(uint8_t a, uint16_t hl);
DeckEntryResult GetCardInDuelTempList(uint8_t a, uint16_t hl);

/* Load deck card `a` (0-59) into wLoadedCard1/2, applying the trainer-to-Pokemon
 * conversion. Exit a is the card id's low byte (captured as `ld a, e` before the
 * register pops); every other register is restored. */
uint8_t LoadCardDataToBuffer1_FromDeckIndex(uint8_t a);
uint8_t LoadCardDataToBuffer2_FromDeckIndex(uint8_t a);

/* Subtract the 16-bit damage in de from the HP byte at hl, clamping at zero
 * (duel.asm:2011-2030). Exit a is the remaining HP; exit carry is set iff it is
 * non-zero, which is what callers branch on (knocked out when clear). */
typedef struct {
	uint8_t a;
	uint8_t f;
} SubtractHPResult;
SubtractHPResult SubtractHP(uint16_t hl, uint16_t de);

#endif
