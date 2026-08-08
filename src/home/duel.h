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

/* Card-list builders (duel.asm:369-431). Fill wDuelTempList (FF-terminated) with
 * the turn holder's remaining deck cards or their discard pile, read backwards.
 * Exit a is the count; carry is set iff the list is empty. de exits past the
 * terminator; hl exits at the count duelvar (page + $BA / page + $ED). */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} CardListResult;
CardListResult CreateDeckCardList(uint8_t c, uint16_t de);
CardListResult CreateDiscardPileCardList(uint8_t c);

/* wDuelTempList helpers. RemoveCardFromDuelTempList (duel.asm:713-746) compacts
 * the FF-terminated list around the card id in a; all registers are pushed and
 * popped, so exit a is the remaining count and carry is set iff it is zero.
 * CountCardsInDuelTempList (747-761) returns the entry count in a. */
typedef struct {
	uint8_t a;
	uint8_t f;
} TempListResult;
TempListResult RemoveCardFromDuelTempList(uint8_t a);
TempListResult CountCardsInDuelTempList(void);

/* Hand/energy list builders. FindLastCardInHand (duel.asm:526-533) returns the
 * hand's last card pointer: b = count, hl = page + $41 + count, de = wDuelTempList.
 * CreateHandCardList (473-500) fills wDuelTempList with non-just-drawn hand cards.
 * CreateArenaOrBenchEnergyCardList (435-470) fills it with energy cards of the
 * play-area location in entry a. Both set carry iff the resulting list is empty. */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} HandListResult;
HandListResult FindLastCardInHand(uint8_t c);
HandListResult CreateHandCardList(uint8_t c);
HandListResult CreateArenaOrBenchEnergyCardList(uint8_t a);

/* ShuffleCards (duel.asm:541-563): swap a cards of the deck region at hl with
 * positions chosen by Random. Exit a is the last swapped byte; all other
 * registers are pushed and popped. */
typedef struct {
	uint8_t a;
	uint8_t f;
} ShuffleCardsResult;
ShuffleCardsResult ShuffleCards(uint8_t a, uint16_t hl);

/* SortCardsInListByID (duel.asm:589-648): selection-sort the FF-terminated deck-
 * index list at hTempListPtr_ff99 ascending by card id. SortCardsInDuelTempListByID
 * (578-587) first points that pointer at wDuelTempList. Exit a is the terminator
 * position's low byte; f is $20 (bit 7 of $FF: Z clear, H set). */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} SortResult;
SortResult SortCardsInListByID(uint8_t b, uint8_t c, uint16_t de);
SortResult SortCardsInDuelTempListByID(uint8_t b, uint8_t c, uint16_t de);

/* SortHandCardsByID (duel.asm:502-525): copy the hand to wDuelTempList, sort by
 * id, write back with the lowest id at the newest hand position. Exit a = the
 * last copied card value, b = 0, hl = page + $40, de past the list terminator. */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} HandSortResult;
HandSortResult SortHandCardsByID(void);

/* TranslateColorToWR (duel.asm:1915-1922): color index in a -> InvertedPowersOf2[a]
 * ($80 >> a). Pure ROM table read; hl/b/c/d/e preserved. */
uint8_t TranslateColorToWR(uint8_t a);

#endif
