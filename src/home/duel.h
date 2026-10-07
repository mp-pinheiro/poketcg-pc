#ifndef POKETCG_HOME_DUEL_H
#define POKETCG_HOME_DUEL_H

/* >>> part includes */
#include <stdint.h>
#include "home/card_id.h"

#include "home/process_text.h"
/* <<< part includes */

/* >>> factory CopyPlayerName */
/* Both return the asm's three live exit registers: a, de (the destination, backed
 * up onto the terminator) and hl (the source, advanced past it). */
CopyTextResult CopyPlayerName(uint16_t de);
/* <<< factory CopyPlayerName */
/* >>> factory CopyOpponentName */
CopyTextResult CopyOpponentName(uint16_t de);
/* <<< factory CopyOpponentName */

/* >>> part DuelistVarResult */
/* Duelist-variable layer (duel.asm:1316-1337): reads duelvar `a` of the current
 * turn holder / the other player. Every duel-engine routine builds on these.
 * Exit a is the byte read; exit hl is the address it was read from. */
typedef struct {
	uint8_t a;
	uint16_t hl;
} DuelistVarResult;
/* <<< part DuelistVarResult */
/* >>> factory GetTurnDuelistVariable */
DuelistVarResult GetTurnDuelistVariable(uint8_t a);
/* <<< factory GetTurnDuelistVariable */
/* >>> factory GetNonTurnDuelistVariable */
DuelistVarResult GetNonTurnDuelistVariable(uint8_t a);
/* <<< factory GetNonTurnDuelistVariable */
/* >>> factory SwapTurn */
void SwapTurn(void);
/* <<< factory SwapTurn */

/* >>> part DeckCardResult */
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
/* <<< part DeckCardResult */
/* >>> part DeckEntryResult */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} DeckEntryResult;
/* <<< part DeckEntryResult */
/* >>> factory _GetCardIDFromDeckIndex */
DeckCardResult _GetCardIDFromDeckIndex(uint8_t a);
/* <<< factory _GetCardIDFromDeckIndex */
/* >>> factory GetCardIDFromDeckIndex */
CardId GetCardIDFromDeckIndex(uint8_t a);
/* <<< factory GetCardIDFromDeckIndex */
/* >>> factory GetCardIDFromDeckIndex_bc */
DeckCardResult GetCardIDFromDeckIndex_bc(uint8_t a, uint16_t hl);
/* <<< factory GetCardIDFromDeckIndex_bc */
/* >>> factory GetCardInDuelTempList_OnlyDeckIndex */
DeckCardResult GetCardInDuelTempList_OnlyDeckIndex(uint8_t a, uint16_t hl);
/* <<< factory GetCardInDuelTempList_OnlyDeckIndex */
/* >>> factory GetCardInDuelTempList */
DeckEntryResult GetCardInDuelTempList(uint8_t a, uint16_t hl);
/* <<< factory GetCardInDuelTempList */

/* >>> factory LoadCardDataToBuffer1_FromDeckIndex */
/* Load deck card `a` (0-59) into wLoadedCard1/2, applying the trainer-to-Pokemon
 * conversion. Exit a is the card id's low byte (captured as `ld a, e` before the
 * register pops); every other register is restored. */
uint8_t LoadCardDataToBuffer1_FromDeckIndex(uint8_t a);
/* <<< factory LoadCardDataToBuffer1_FromDeckIndex */
/* >>> factory LoadCardDataToBuffer2_FromDeckIndex */
uint8_t LoadCardDataToBuffer2_FromDeckIndex(uint8_t a);
/* <<< factory LoadCardDataToBuffer2_FromDeckIndex */

/* >>> part SubtractHPResult */
/* Subtract the 16-bit damage in de from the HP byte at hl, clamping at zero
 * (duel.asm:2011-2030). Exit a is the remaining HP; exit carry is set iff it is
 * non-zero, which is what callers branch on (knocked out when clear). */
typedef struct {
	uint8_t a;
	uint8_t f;
} SubtractHPResult;
/* <<< part SubtractHPResult */
/* >>> factory SubtractHP */
SubtractHPResult SubtractHP(uint16_t hl, uint16_t de);
/* <<< factory SubtractHP */

/* >>> part CardListResult */
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
/* <<< part CardListResult */
/* >>> factory CreateDeckCardList */
CardListResult CreateDeckCardList(uint8_t c, uint16_t de);
/* <<< factory CreateDeckCardList */
/* >>> factory CreateDiscardPileCardList */
CardListResult CreateDiscardPileCardList(uint8_t c);
/* <<< factory CreateDiscardPileCardList */

/* >>> part TempListResult */
/* wDuelTempList helpers. RemoveCardFromDuelTempList (duel.asm:713-746) compacts
 * the FF-terminated list around the card id in a; all registers are pushed and
 * popped, so exit a is the remaining count and carry is set iff it is zero.
 * CountCardsInDuelTempList (747-761) returns the entry count in a. */
typedef struct {
	uint8_t a;
	uint8_t f;
} TempListResult;
/* <<< part TempListResult */
/* >>> factory RemoveCardFromDuelTempList */
TempListResult RemoveCardFromDuelTempList(uint8_t a);
/* <<< factory RemoveCardFromDuelTempList */
/* >>> factory CountCardsInDuelTempList */
TempListResult CountCardsInDuelTempList(void);
/* <<< factory CountCardsInDuelTempList */

/* >>> part HandListResult */
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
/* <<< part HandListResult */
/* >>> factory FindLastCardInHand */
HandListResult FindLastCardInHand(uint8_t c);
/* <<< factory FindLastCardInHand */
/* >>> factory CreateHandCardList */
HandListResult CreateHandCardList(uint8_t c);
/* <<< factory CreateHandCardList */
/* >>> factory CreateArenaOrBenchEnergyCardList */
HandListResult CreateArenaOrBenchEnergyCardList(uint8_t a);
/* <<< factory CreateArenaOrBenchEnergyCardList */

/* >>> part ShuffleCardsResult */
/* ShuffleCards (duel.asm:541-563): swap a cards of the deck region at hl with
 * positions chosen by Random. Exit a is the last swapped byte; all other
 * registers are pushed and popped. */
typedef struct {
	uint8_t a;
	uint8_t f;
} ShuffleCardsResult;
/* <<< part ShuffleCardsResult */
/* >>> factory ShuffleCards */
ShuffleCardsResult ShuffleCards(uint8_t a, uint16_t hl);
/* <<< factory ShuffleCards */

/* >>> part SortResult */
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
/* <<< part SortResult */
/* >>> factory SortCardsInListByID */
SortResult SortCardsInListByID(uint8_t b, uint8_t c, uint16_t de);
/* <<< factory SortCardsInListByID */
/* >>> factory SortCardsInDuelTempListByID */
SortResult SortCardsInDuelTempListByID(uint8_t b, uint8_t c, uint16_t de);
/* <<< factory SortCardsInDuelTempListByID */

/* >>> part HandSortResult */
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
/* <<< part HandSortResult */
/* >>> factory SortHandCardsByID */
HandSortResult SortHandCardsByID(void);
/* <<< factory SortHandCardsByID */

/* >>> factory TranslateColorToWR */
/* TranslateColorToWR (duel.asm:1915-1922): color index in a -> InvertedPowersOf2[a]
 * ($80 >> a). Pure ROM table read; hl/b/c/d/e preserved. */
uint8_t TranslateColorToWR(uint8_t a);
/* <<< factory TranslateColorToWR */

/* >>> part CardLocationCountResult */
/* CountCardIDInLocation (duel.asm:1290-1315): count deck cards in location b with
 * card id e. Entry hl = the card-locations page. Exit a = count, hl = page + 60.
 * CheckLoadedAttackFlag (2331-2357): test attack-flag group (a >> 3) bit (a & 7)
 * of wLoadedAttackFlag1; carry set iff the flag is set. All other registers
 * preserved by both. */
typedef struct {
	uint8_t a;
	uint16_t hl;
} CardLocationCountResult;
/* <<< part CardLocationCountResult */
/* >>> factory CountCardIDInLocation */
CardLocationCountResult CountCardIDInLocation(uint8_t b, uint8_t e, uint16_t hl);
/* <<< factory CountCardIDInLocation */
/* >>> part AttackFlagResult */
typedef struct {
	uint8_t a;
	uint8_t f;
} AttackFlagResult;
/* <<< part AttackFlagResult */
/* >>> factory CheckLoadedAttackFlag */
AttackFlagResult CheckLoadedAttackFlag(uint8_t a);
/* <<< factory CheckLoadedAttackFlag */

/* >>> part CardDamageResult */
/* GetCardDamageAndMaxHP (duel.asm:2306-2320): arena/bench slot e. Exit a = the
 * loaded card's max HP minus its damage, c = max HP, carry = damage exceeded HP.
 * All other registers restored. */
typedef struct {
	uint8_t a;
	uint8_t c;
	uint8_t f;
} CardDamageResult;
/* <<< part CardDamageResult */
/* >>> factory GetCardDamageAndMaxHP */
CardDamageResult GetCardDamageAndMaxHP(uint8_t e);
/* <<< factory GetCardDamageAndMaxHP */

/* >>> factory CopyDeckData */
/* ---- W1-B additions ---- */

/* CopyDeckData (duel.asm:60-104): de = deck description (count,id pairs, $00-
 * terminated, then 2 name bytes). Fills wPlayerDeck/wOpponentDeck (60 bytes,
 * hWhoseTurn-selected), pre-seeding slot 59 with $00 so an under-filled deck is
 * detectable. Exit a/hl = deckBase+59's value/address; de = the 2 deck-name
 * bytes' address. The trailing `ld bc, DECK_SIZE - 1` (re-deriving hl for the
 * final check) leaves b/c at the constants 0/DECK_SIZE-1 unconditionally, not
 * loop residue -- entry c is never read at all. Carry set iff deckBase+59 is
 * still $00 (under 60 cards). */
CardListResult CopyDeckData(uint16_t de);
/* <<< factory CopyDeckData */

/* >>> factory CountPrizes */
/* CountPrizes (duel.asm:107-120): population count of the turn holder's
 * DUELVARS_PRIZES bitmask (verified exhaustively against the `rr l / adc 0`
 * carry-ring against all 256 byte values; the real game only ever stores runs of
 * low bits via PrizeBitmasks, for which this is also exactly popcount). hl/b/c/d/e
 * preserved (wrapped in push/pop). */
uint8_t CountPrizes(void);
/* <<< factory CountPrizes */

/* >>> part ShuffleDeckResult */
/* ShuffleDeck (duel.asm:124-137): shuffles DECK_SIZE - [not-in-deck] cards of the
 * turn holder's deck via ShuffleCards, tail-calling it with no push/pop of its
 * own. Exit a/f are ShuffleCards' own exit; b = the computed card count; d =
 * hWhoseTurn (clobbered before the call); c/e pass straight through untouched
 * (ShuffleCards preserves its entry c/e); hl = the computed deck-cards address. */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} ShuffleDeckResult;
/* <<< part ShuffleDeckResult */
/* >>> factory ShuffleDeck */
ShuffleDeckResult ShuffleDeck(uint8_t c, uint8_t e);
/* <<< factory ShuffleDeck */

/* >>> part DrawCardResult */
/* DrawCardFromDeck (duel.asm:142-161): draws the turn holder's top deck card,
 * marking its location CARD_LOCATION_JUST_DRAWN. Entry hl/b/c/d/e are pushed and
 * popped (fully preserved). Exit a = the drawn card's deck index on success, or
 * the (>=60) not-in-deck count on the empty-deck path; carry set iff empty. */
typedef struct {
	uint8_t a;
	uint8_t f;
} DrawCardResult;
/* <<< part DrawCardResult */
/* >>> factory DrawCardFromDeck */
DrawCardResult DrawCardFromDeck(void);
/* <<< factory DrawCardFromDeck */

/* >>> factory ReturnCardToDeck */
/* ReturnCardToDeck (duel.asm:165-180): entry a = deck index to place back on top
 * of the turn holder's deck. Every register (a,f,hl,b,c,d,e) is preserved -- the
 * routine's only effect is the WRAM write of the deck-cards slot and the card's
 * location (CARD_LOCATION_DECK). */
void ReturnCardToDeck(uint8_t a);
/* <<< factory ReturnCardToDeck */

/* >>> factory SearchCardInDeckAndAddToHand */
/* SearchCardInDeckAndAddToHand (duel.asm:185-217): entry a = deck index. Wrapped
 * in push af/hl/de/bc ... pop bc/de/hl/af, so every register is preserved; the
 * routine extracts the card from the deck array (compacting the remainder) and
 * marks its location CARD_LOCATION_JUST_DRAWN. AddCardToHand is the intended
 * follow-up call. */
void SearchCardInDeckAndAddToHand(uint8_t a);
/* <<< factory SearchCardInDeckAndAddToHand */

/* >>> factory AddCardToHand */
/* AddCardToHand (duel.asm:221-242): entry a = deck index. Wrapped in
 * push af/hl/de ... pop de/hl/af (b/c untouched too), so every register is
 * preserved. Marks the card CARD_LOCATION_HAND, increments the hand count, and
 * appends the card to the end of the hand array. */
void AddCardToHand(uint8_t a);
/* <<< factory AddCardToHand */

/* >>> factory RemoveCardFromHand */
/* RemoveCardFromHand (duel.asm:246-280): entry a = deck index to remove (every
 * matching hand entry is removed, decrementing the hand count once per match).
 * Wrapped in push af/hl/bc/de ... pop de/bc/hl/af: every register preserved. */
void RemoveCardFromHand(uint8_t a);
/* <<< factory RemoveCardFromHand */

/* >>> factory PutCardInDiscardPile */
/* PutCardInDiscardPile (duel.asm:294-311): entry a = deck index. Wrapped in
 * push af/hl/de ... pop de/hl/af (b/c untouched), so every register preserved.
 * Marks the card CARD_LOCATION_DISCARD_PILE, increments the discard count, and
 * appends the card to the discard-pile array. */
void PutCardInDiscardPile(uint8_t a);
/* <<< factory PutCardInDiscardPile */

/* >>> part MoveCardResult */
/* MoveHandCardToDiscardPile (duel.asm:284-292): entry a = deck index. If the
 * card's (JUST_DRAWN-masked) location isn't CARD_LOCATION_HAND, returns early
 * with a = the masked location byte, f = the `cp CARD_LOCATION_HAND` flags, hl =
 * page:a; b/c/d/e preserved. Otherwise removes it from hand and discards it
 * (falling through into PutCardInDiscardPile): a echoes the input index, f =
 * $C0 (the `cp` that matched), hl = page:a; b/c/d/e still preserved. */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} MoveCardResult;
/* <<< part MoveCardResult */
/* >>> factory MoveHandCardToDiscardPile */
MoveCardResult MoveHandCardToDiscardPile(uint8_t a);
/* <<< factory MoveHandCardToDiscardPile */

/* >>> part MoveDiscardResult */
/* MoveDiscardPileCardToHand (duel.asm:316-346): entry a = deck index to pull
 * from the turn holder's discard pile (marks it CARD_LOCATION_JUST_DRAWN and
 * compacts the discard array). Wrapped in push hl/de/bc ... pop bc/de/hl, so
 * only a/f are real outputs: a = 0 if the discard pile was already empty, else
 * the input index echoed back; f = $80 (empty) or the final compaction `dec c`
 * flags (Z+N always, H clear, C from the last `cp` against the searched id). */
typedef struct {
	uint8_t a;
	uint8_t f;
} MoveDiscardResult;
/* <<< part MoveDiscardResult */
/* >>> factory MoveDiscardPileCardToHand */
MoveDiscardResult MoveDiscardPileCardToHand(uint8_t a);
/* <<< factory MoveDiscardPileCardToHand */

/* >>> part CheckPrizeResult */
/* CheckPrizeTaken (duel.asm:350-362): entry a = prize index (0-7). Reads
 * PowersOf2[a] (00:11B7) as a bitmask, ANDs it against the turn holder's
 * DUELVARS_PRIZES; z means the prize was drawn. Exit a = the AND result; d = the
 * complement of the mask; e = the mask itself; hl = page:DUELVARS_PRIZES; b/c
 * preserved. */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} CheckPrizeResult;
/* <<< part CheckPrizeResult */
/* >>> factory CheckPrizeTaken */
CheckPrizeResult CheckPrizeTaken(uint8_t a);
/* <<< factory CheckPrizeTaken */

/* >>> factory SortCardsInListByID_CheckForListTerminator */
/* SortCardsInListByID_CheckForListTerminator (duel.asm:650-657): the loop head
 * SortCardsInListByID jumps back to after every pass -- entering here is
 * identical to entering the top of SortCardsInListByID's own loop, so the two
 * share one C implementation and the same exit contract. */
SortResult SortCardsInListByID_CheckForListTerminator(uint8_t b, uint8_t c, uint16_t de);
/* <<< factory SortCardsInListByID_CheckForListTerminator */

/* >>> part EvolveResult */
/* CheckIfCanEvolveInto (duel.asm:879-915): d = the deck index of the candidate
 * evolution target, e = the play area slot (PLAY_AREA_*) of the card trying to
 * evolve. Compares loaded-card name fields to decide eligibility; entry de is
 * preserved (popped back); b/c are never touched. Carry set iff not eligible.
 * Exit a/f/hl vary by branch; see the .c file. c is unused (kept 0) -- only
 * meaningful for EvolvePokemonCard/EvolvePokemonCardIfPossible below, which
 * reuse this same result shape.
 * CheckIfCanEvolveInto_BasicToStage2 (922-957) additionally calls the opaque
 * LoadCardDataToBuffer1_FromName, which does not preserve b/c and reassigns de
 * outright (no push de at all in this variant) -- b/c/d/e are real but not
 * independently derivable without tracing that callee, so they are omitted
 * from CONTRACT; only a/f/hl are checked. */
typedef struct {
	uint8_t a;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} EvolveResult;
/* <<< part EvolveResult */
/* >>> factory CheckIfCanEvolveInto */
EvolveResult CheckIfCanEvolveInto(uint8_t d, uint8_t e);
/* <<< factory CheckIfCanEvolveInto */
/* >>> factory CheckIfCanEvolveInto_BasicToStage2 */
EvolveResult CheckIfCanEvolveInto_BasicToStage2(uint8_t d, uint8_t e);
/* <<< factory CheckIfCanEvolveInto_BasicToStage2 */

/* >>> factory EvolvePokemonCardIfPossible */
/* EvolvePokemonCardIfPossible (duel.asm:814-822) / EvolvePokemonCard (824-869):
 * read hTempCardIndex_ff98 (the evolution card's deck index) and
 * hTempPlayAreaLocation_ff9d (the target slot) directly; no register inputs
 * besides EvolvePokemonCardIfPossible's entry c (pass-through on the
 * ineligible branch, where the wrapped CheckIfCanEvolveInto never touches c).
 * EvolvePokemonCardIfPossible returns CheckIfCanEvolveInto's failure exit
 * unmodified (a/f/hl) if ineligible, with d/e forced to the two HRAM temps
 * read at entry (CheckIfCanEvolveInto's entry de, preserved through it) in
 * both branches. EvolvePokemonCard's exit c is always wLoadedCard2HP (the
 * `ld c, a` before the HP-delta subtraction, never touched again); on its own
 * (no d input) entry d is untouched -- only c/e/a/f/hl are real outputs there. */
EvolveResult EvolvePokemonCardIfPossible(uint8_t c);
/* <<< factory EvolvePokemonCardIfPossible */
/* >>> factory EvolvePokemonCard */
EvolveResult EvolvePokemonCard(void);
/* <<< factory EvolvePokemonCard */

/* >>> factory ClearAllStatusConditions */
/* ClearAllStatusConditions (duel.asm:962-989): zeroes the turn holder's arena
 * card's status/substatus1/substatus2/changed-weakness/changed-resistance,
 * clears substatus3 bit 0 only, and zeroes 8 bytes starting at
 * DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX. hl preserved (push/pop); a/f are
 * always 0/$80 (the `xor a` at entry, untouched after) and omitted from CONTRACT
 * to match SwapTurn's precedent for pure-WRAM-effect routines. */
void ClearAllStatusConditions(void);
/* <<< factory ClearAllStatusConditions */

/* >>> part PutHandResult */
/* PutHandCardInPlayArea (duel.asm:1058-1064): entry a = deck index (removed from
 * hand via RemoveCardFromHand, which preserves every register), e = play area
 * location offset. Writes card_locations[a] = e | CARD_LOCATION_PLAY_AREA. Exit
 * a = that written byte; f = $00 (always nonzero via `or`); hl = page:a. b/c/d/e
 * preserved. */
typedef struct {
	uint8_t a;
	uint16_t hl;
} PutHandResult;
/* <<< part PutHandResult */
/* >>> factory PutHandCardInPlayArea */
PutHandResult PutHandCardInPlayArea(uint8_t a, uint8_t e);
/* <<< factory PutHandCardInPlayArea */

/* >>> part PutHandPokemonResult */
/* PutHandPokemonCardInPlayArea (duel.asm:996-1049): entry a = deck index, f =
 * entry flags (the "already max" branch's `pop af` restores these before
 * `scf` forces C, so Z there is the caller's, not derived from the `cp`). If
 * the turn holder's play area is full (>= MAX_PLAY_AREA_POKEMON), returns
 * early with a = the input echoed back, f = (entry Z) | C, hl =
 * page:DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA. Otherwise places the card in
 * the first free slot, initializes its arena-card fields, and returns a = the
 * slot index, f = Z iff slot == 0 (arena), hl = page:(ARENA_CARD_STAGE+slot).
 * b/c/d preserved. */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} PutHandPokemonResult;
/* <<< part PutHandPokemonResult */
/* >>> factory PutHandPokemonCardInPlayArea */
PutHandPokemonResult PutHandPokemonCardInPlayArea(uint8_t a, uint8_t f);
/* <<< factory PutHandPokemonCardInPlayArea */

/* >>> part EmptySlotResult */
/* EmptyPlayAreaSlot (duel.asm:1091-1111): entry e = play area location offset.
 * Resets that slot's arena-card/hp/stage/changed-type/attached-defender/attached-
 * pluspower fields ($FF for the card, 0 for the rest). Exit a/hl = the last
 * written address (ARENA_CARD_ATTACHED_PLUSPOWER+e); d = 0 (the last `ld d,0`);
 * f = the plain 8-bit-add flags of that address computation. b/c/e preserved. */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t f;
	uint16_t hl;
} EmptySlotResult;
/* <<< part EmptySlotResult */
/* >>> part InitDuelvarResult */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } InitDuelvarResult;
/* <<< part InitDuelvarResult */
/* >>> factory EmptyPlayAreaSlot_init_duelvar */
InitDuelvarResult EmptyPlayAreaSlot_init_duelvar(uint8_t a, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory EmptyPlayAreaSlot_init_duelvar */
/* >>> part SwapDuelvarResult */
typedef struct { uint8_t a; uint8_t f; uint8_t c; uint16_t hl; } SwapDuelvarResult;
/* <<< part SwapDuelvarResult */
/* >>> factory SwapPlayAreaPokemon_swap_duelvar */
SwapDuelvarResult SwapPlayAreaPokemon_swap_duelvar(uint8_t a, uint8_t b, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory SwapPlayAreaPokemon_swap_duelvar */
/* >>> factory EmptyPlayAreaSlot */
EmptySlotResult EmptyPlayAreaSlot(uint8_t e);
/* <<< factory EmptyPlayAreaSlot */

/* >>> part MoveAreaResult */
/* MovePlayAreaCardToDiscardPile (duel.asm:1068-1087): entry e = play area
 * location offset. Empties that slot (EmptyPlayAreaSlot), decrements the
 * play-area pokemon count, then discards every card whose location equals
 * CARD_LOCATION_PLAY_AREA|e. Exit a/hl = DECK_SIZE / page:DECK_SIZE (the loop's
 * termination state); d = 0 (EmptyPlayAreaSlot's own `ld d, 0`, never
 * overwritten again); f = $C0. b/c/e preserved. */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t f;
	uint16_t hl;
} MoveAreaResult;
/* <<< part MoveAreaResult */
/* >>> factory MovePlayAreaCardToDiscardPile */
MoveAreaResult MovePlayAreaCardToDiscardPile(uint8_t e);
/* <<< factory MovePlayAreaCardToDiscardPile */

/* >>> part SwapAreaResult */
/* SwapPlayAreaPokemon (duel.asm:1148-1215): swaps the turn holder's play-area
 * cards at offsets d and e (all seven per-card duelvar fields, plus relabeling
 * every card_locations entry that pointed at either slot). Wrapped in
 * push bc/de/hl ... pop hl/de/bc, so only a/f are real outputs: a = e (no-op,
 * d==e) or DECK_SIZE (swapped); f = $C0 either way. SwapArenaWithBenchPokemon
 * (1143-1146) resets status then tail-calls this with d = PLAY_AREA_ARENA, so it
 * shares the same result shape but with d forced to 0 in CONTRACT. */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t f;
} SwapAreaResult;
/* <<< part SwapAreaResult */
/* >>> factory SwapPlayAreaPokemon */
SwapAreaResult SwapPlayAreaPokemon(uint8_t d, uint8_t e);
/* <<< factory SwapPlayAreaPokemon */
/* >>> factory SwapArenaWithBenchPokemon */
SwapAreaResult SwapArenaWithBenchPokemon(uint8_t e);
/* <<< factory SwapArenaWithBenchPokemon */

/* >>> part ShiftResult */
/* ShiftTurnPokemonToFirstPlayAreaSlots (duel.asm:1122-1137): compacts the turn
 * holder's occupied play-area slots toward the front via repeated
 * SwapPlayAreaPokemon calls. Exit a/d = MAX_PLAY_AREA_POKEMON (the scan cursor's
 * final value); e = the count of occupied slots found (the compacted write
 * cursor); f = $C0; hl = page:(ARENA_CARD+MAX_PLAY_AREA_POKEMON). b/c preserved.
 * ShiftAllPokemonToFirstPlayAreaSlots (1114-1119) does this for both duelists
 * (SwapTurn between), returning the second call's (opponent-page) result. */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} ShiftResult;
/* <<< part ShiftResult */
/* >>> factory ShiftTurnPokemonToFirstPlayAreaSlots */
ShiftResult ShiftTurnPokemonToFirstPlayAreaSlots(void);
/* <<< factory ShiftTurnPokemonToFirstPlayAreaSlots */
/* >>> factory ShiftAllPokemonToFirstPlayAreaSlots */
ShiftResult ShiftAllPokemonToFirstPlayAreaSlots(void);
/* <<< factory ShiftAllPokemonToFirstPlayAreaSlots */

/* >>> part EnergiesResult */
/* GetPlayAreaCardAttachedEnergies (duel.asm:1221-1284): entry e = play area
 * location offset (0 = arena, nonzero = that bench slot). Zeroes
 * wAttachedEnergies[8], scans all 60 card-location slots for cards at that
 * location that are energy cards, tallying by color into wAttachedEnergies (each
 * COLORLESS counts twice) and the sum into wTotalAttachedEnergies. Wrapped in
 * push hl/de/bc ... pop bc/de/hl (hl/de/bc preserved); af is not, so exit a =
 * the tallied sum. f = $C0 always -- the last flag-setting instruction is the
 * summing loop's terminating `dec c` (NUM_TYPES down to 0), not the `add [hl]`
 * before it. */
typedef struct {
	uint8_t a;
	uint8_t f;
} EnergiesResult;
/* <<< part EnergiesResult */
/* >>> factory GetPlayAreaCardAttachedEnergies */
EnergiesResult GetPlayAreaCardAttachedEnergies(uint8_t e);
/* <<< factory GetPlayAreaCardAttachedEnergies */

/* >>> part AttackCopyResult */
/* CopyAttackDataAndDamage (duel.asm:1442-1467) copies attack 1 (e==0) or attack
 * 2 (e==1) from wLoadedCard1 into wLoadedAttack (19 bytes), then wDamage/
 * wDealtDamage/wNoDamageOrEffect are (re)initialized from it. Exit a/c = 0, f =
 * $80 (the trailing `xor a`), hl/de = the two copy destinations' final addresses
 * -- all deterministic regardless of e. b preserved.
 * CopyAttackDataAndDamage_FromDeckIndex (1434-1440) / _FromCardID (1415-1427)
 * set wSelectedAttack/hTempCardIndex_ff9f from d/e (deck index) or a/d/e (card
 * ID), load the card, then tail-call CopyAttackDataAndDamage(e) -- same exit
 * shape, e passed straight through. */
typedef struct {
	uint8_t a;
	uint8_t c;
	uint8_t f;
	uint16_t hl;
	uint16_t de;
} AttackCopyResult;
/* <<< part AttackCopyResult */
/* >>> factory CopyAttackDataAndDamage */
AttackCopyResult CopyAttackDataAndDamage(uint8_t e);
/* <<< factory CopyAttackDataAndDamage */
/* >>> factory CopyAttackDataAndDamage_FromDeckIndex */
AttackCopyResult CopyAttackDataAndDamage_FromDeckIndex(uint8_t d, uint8_t e);
/* <<< factory CopyAttackDataAndDamage_FromDeckIndex */
/* >>> factory CopyAttackDataAndDamage_FromCardID */
AttackCopyResult CopyAttackDataAndDamage_FromCardID(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory CopyAttackDataAndDamage_FromCardID */

/* >>> factory ReturnCarry */
/* ReturnCarry (duel.asm:1621-1623): `scf` -- sets carry, clears N/H, leaves Z
 * (and every other register) untouched. */
uint8_t ReturnCarry(uint8_t f);
/* <<< factory ReturnCarry */

/* >>> part LoadEffectResult */
/* LoadNonPokemonCardEffectCommands (duel.asm:1793-1803): reads
 * hTempCardIndex_ff9f, loads that deck card into wLoadedCard1, then copies its
 * 2-byte EffectCommands pointer into wLoadedAttackEffectCommands. Exit a = the
 * second copied byte; hl/de = one past each copy's source/destination (both
 * deterministic); b/c/d/e preserved. f omitted -- its last flag-setting
 * instruction is inside the opaque LoadCardDataToBuffer1_FromDeckIndex call. */
typedef struct {
	uint8_t a;
	uint16_t hl;
	uint16_t de;
} LoadEffectResult;
/* <<< part LoadEffectResult */
/* >>> factory LoadNonPokemonCardEffectCommands */
LoadEffectResult LoadNonPokemonCardEffectCommands(void);
/* <<< factory LoadNonPokemonCardEffectCommands */

/* >>> part PowerModifierResult */
/* ApplyAttachedPlusPower / ApplyAttachedDefender (duel.asm:1976-2006): entry b =
 * a CARD_LOCATION_* to search (the routines call GetTurnDuelistVariable only to
 * get h = hWhoseTurn cheaply; entry `a` is otherwise irrelevant and CountCardIDInLocation
 * resets l itself), de = the damage value to adjust. PlusPower adds 10 per
 * attached PLUSPOWER found in location b (`add hl, de` then copies the sum back
 * into de, so exit hl == exit de). Defender subtracts 20 per DEFENDER, but
 * subtracts register-by-register into e/d directly and never touches hl again
 * after HtimesL -- exit hl is the raw un-subtracted product (20 * count), and
 * exit de is the actually-adjusted damage; they differ. a/f flow through the
 * opaque HtimesL leaf and are omitted; b/c preserved (CountCardIDInLocation
 * pushes/pops them). */
typedef struct {
	uint16_t hl;
	uint16_t de;
} PowerModifierResult;
/* <<< part PowerModifierResult */
/* >>> factory ApplyAttachedPlusPower */
PowerModifierResult ApplyAttachedPlusPower(uint8_t b, uint16_t de);
/* <<< factory ApplyAttachedPlusPower */
/* >>> factory ApplyAttachedDefender */
PowerModifierResult ApplyAttachedDefender(uint8_t b, uint16_t de);
/* <<< factory ApplyAttachedDefender */

/* >>> part DiscardIfInPlayResult */
/* MoveCardToDiscardPileIfInPlayArea (duel.asm:2273-2298): entry de = the card ID
 * to discard everywhere it appears in the play area; entry `page` is the high
 * byte the caller's hl already held (hWhoseTurn in every real caller) -- the
 * scan uses it directly rather than recomputing it, while the inner
 * GetCardIDFromDeckIndex/PutCardInDiscardPile calls read the live hWhoseTurn.
 * Exit a = DECK_SIZE, b/c = the input d/e echoed back (the search id, held
 * fixed through the scan), f = $C0, hl = page:DECK_SIZE. Exit d/e (clobbered
 * every matching iteration by GetCardIDFromDeckIndex) are genuine unpredictable
 * loop residue and omitted from CONTRACT. */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t f;
	uint16_t hl;
} DiscardIfInPlayResult;
/* <<< part DiscardIfInPlayResult */
/* >>> factory MoveCardToDiscardPileIfInPlayArea */
DiscardIfInPlayResult MoveCardToDiscardPileIfInPlayArea(uint16_t de, uint8_t page);
/* <<< factory MoveCardToDiscardPileIfInPlayArea */

/* >>> factory ApplyDamageModifiers_DamageToTarget */
uint16_t ApplyDamageModifiers_DamageToTarget(void);
/* <<< factory ApplyDamageModifiers_DamageToTarget */
/* >>> factory ApplyDamageModifiers_DamageToSelf */
uint16_t ApplyDamageModifiers_DamageToSelf(void);
/* <<< factory ApplyDamageModifiers_DamageToSelf */
/* >>> factory GetPlayAreaCardRetreatCost */
uint8_t GetPlayAreaCardRetreatCost(void);
/* <<< factory GetPlayAreaCardRetreatCost */


/* >>> part KnockoutCheckResult */
typedef struct { uint8_t a, f; } KnockoutCheckResult;
/* <<< part KnockoutCheckResult */

/* >>> factory DrawWideTextBox_WaitForInput_ReturnCarry */
/* Wave 3 */
uint8_t DrawWideTextBox_WaitForInput_ReturnCarry(uint16_t hl);
/* <<< factory DrawWideTextBox_WaitForInput_ReturnCarry */
/* >>> factory PrintKnockedOut */
uint8_t PrintKnockedOut(void);
/* <<< factory PrintKnockedOut */
/* >>> factory PrintPlayAreaCardKnockedOutIfNoHP */
KnockoutCheckResult PrintPlayAreaCardKnockedOutIfNoHP(uint8_t a);
/* <<< factory PrintPlayAreaCardKnockedOutIfNoHP */

/* >>> part DuelRoutineResult */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
} DuelRoutineResult;
/* <<< part DuelRoutineResult */

/* >>> factory UpdateArenaCardIDsAndClearTwoTurnDuelVars */
DuelRoutineResult UpdateArenaCardIDsAndClearTwoTurnDuelVars(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory UpdateArenaCardIDsAndClearTwoTurnDuelVars */
/* >>> factory ClearNonTurnTemporaryDuelvars_ResetCarry */
DuelRoutineResult ClearNonTurnTemporaryDuelvars_ResetCarry(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ClearNonTurnTemporaryDuelvars_ResetCarry */
/* >>> factory PrintKnockedOutIfHLZero */
uint8_t PrintKnockedOutIfHLZero(uint16_t hl);
/* <<< factory PrintKnockedOutIfHLZero */


/* >>> factory GetFirstSetPrizeCard */
uint8_t GetFirstSetPrizeCard(uint8_t a);
/* <<< factory GetFirstSetPrizeCard */
/* >>> factory DrawCheckMenuCursor_YourOrOppPlayArea */
TempListResult DrawCheckMenuCursor_YourOrOppPlayArea(uint8_t a);
/* <<< factory DrawCheckMenuCursor_YourOrOppPlayArea */
/* >>> factory ZeroObjectPositionsWithCopyToggleOn */
void ZeroObjectPositionsWithCopyToggleOn(void);
/* <<< factory ZeroObjectPositionsWithCopyToggleOn */
/* >>> factory YourOrOppPlayAreaScreen_HandleInput */
typedef struct { uint8_t a; uint8_t f; } YourOrOppPlayAreaScreenInputResult;
YourOrOppPlayAreaScreenInputResult YourOrOppPlayAreaScreen_HandleInput(void);
void YourOrOppPlayAreaScreen_DrawCursor(void);
/* <<< factory YourOrOppPlayAreaScreen_HandleInput */
/* >>> factory DrawPlayArea_BenchCards */
void DrawPlayArea_BenchCards(uint8_t c, uint8_t d, uint8_t e);
/* <<< factory DrawPlayArea_BenchCards */
/* >>> factory EraseCheckMenuCursor_YourOrOppPlayArea */
TempListResult EraseCheckMenuCursor_YourOrOppPlayArea(void);
/* <<< factory EraseCheckMenuCursor_YourOrOppPlayArea */
/* >>> factory LoadCursorTile */
void LoadCursorTile(void);
/* <<< factory LoadCursorTile */
/* >>> factory Func_8bf2 */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} PrizeTileResult;
PrizeTileResult Func_8bf2(uint8_t f, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory Func_8bf2 */
/* >>> factory GetDuelInitialPrizesUpperBitsSet */
void GetDuelInitialPrizesUpperBitsSet(void);
/* <<< factory GetDuelInitialPrizesUpperBitsSet */
/* >>> factory DrawYourOrOppPlayArea_DrawArrows */
void DrawYourOrOppPlayArea_DrawArrows(uint8_t a, uint8_t b);
/* <<< factory DrawYourOrOppPlayArea_DrawArrows */
/* >>> factory DrawYourOrOppPlayArea_EraseArrows */
void DrawYourOrOppPlayArea_EraseArrows(void);
/* <<< factory DrawYourOrOppPlayArea_EraseArrows */
/* >>> factory DrawYourOrOppPlayArea_RefreshArrows */
void DrawYourOrOppPlayArea_RefreshArrows(uint8_t a);
/* <<< factory DrawYourOrOppPlayArea_RefreshArrows */
/* >>> factory SendAttackDataToLinkOpponent */
void SendAttackDataToLinkOpponent(void);
/* <<< factory SendAttackDataToLinkOpponent */
/* >>> factory DrawPlayArea_PrizeCards */
void DrawPlayArea_PrizeCards(uint16_t hl);
/* <<< factory DrawPlayArea_PrizeCards */
/* >>> factory _DrawPlayersPrizeAndBenchCards */
void _DrawPlayersPrizeAndBenchCards(void);
/* <<< factory _DrawPlayersPrizeAndBenchCards */
/* >>> factory DrawPlayArea_HandText */
typedef struct { uint8_t b; uint8_t c; uint16_t hl; } DrawPlayArea_HandTextResult;
DrawPlayArea_HandTextResult DrawPlayArea_HandText(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory DrawPlayArea_HandText */
/* >>> factory DrawPlayArea_IconWithValue */
void DrawPlayArea_IconWithValue(uint8_t a, uint8_t b, uint16_t *hl);
/* <<< factory DrawPlayArea_IconWithValue */
/* >>> factory SaveDuelStateToSRAM */
void SaveDuelStateToSRAM(void);
/* <<< factory SaveDuelStateToSRAM */
/* >>> factory DisplayCheckMenuCursor_YourOrOppPlayArea */
TempListResult DisplayCheckMenuCursor_YourOrOppPlayArea(void);
/* <<< factory DisplayCheckMenuCursor_YourOrOppPlayArea */
/* >>> factory HandleCheckMenuInput_YourOrOppPlayArea */
TempListResult HandleCheckMenuInput_YourOrOppPlayArea(void);
/* <<< factory HandleCheckMenuInput_YourOrOppPlayArea */
/* >>> factory DrawYourOrOppPlayArea_Icons */
void DrawYourOrOppPlayArea_Icons(uint8_t a);
/* <<< factory DrawYourOrOppPlayArea_Icons */
/* >>> factory DrawInPlayArea_Icons */
void DrawInPlayArea_Icons(uint16_t hl);
/* <<< factory DrawInPlayArea_Icons */
/* >>> factory DisplayUsePokemonPowerScreen_WaitForInput */
uint8_t DisplayUsePokemonPowerScreen_WaitForInput(uint16_t hl);
/* <<< factory DisplayUsePokemonPowerScreen_WaitForInput */
/* >>> factory _DrawPlayAreaToPlacePrizeCards */
void _DrawPlayAreaToPlacePrizeCards(void);
/* <<< factory _DrawPlayAreaToPlacePrizeCards */
/* >>> factory UsePokemonPower */
typedef struct { uint8_t a, f, b, c, d, e; uint16_t hl; } UsePokemonPowerResult;
UsePokemonPowerResult UsePokemonPower(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory UsePokemonPower */
/* >>> factory DrawYourOrOppPlayArea_ActiveCardGfx */
void DrawYourOrOppPlayArea_ActiveCardGfx(uint16_t de);
/* <<< factory DrawYourOrOppPlayArea_ActiveCardGfx */
/* >>> factory _DrawYourOrOppPlayAreaScreen */
void _DrawYourOrOppPlayAreaScreen(void);
/* <<< factory _DrawYourOrOppPlayAreaScreen */
/* >>> factory DrawYourOrOppPlayAreaScreen */
void DrawYourOrOppPlayAreaScreen(uint16_t hl);
/* <<< factory DrawYourOrOppPlayAreaScreen */
/* >>> factory _DrawAIPeekScreen */
void _DrawAIPeekScreen(uint8_t b);
/* <<< factory _DrawAIPeekScreen */
/* >>> factory PrintPokemonsAttackText */
typedef struct { uint8_t a; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } PrintPokemonsAttackTextResult;
PrintPokemonsAttackTextResult PrintPokemonsAttackText(void);
/* <<< factory PrintPokemonsAttackText */
/* >>> factory PrintFailedEffectText */
typedef struct { uint8_t f; } PrintFailedEffectTextResult;
PrintFailedEffectTextResult PrintFailedEffectText(void);
/* <<< factory PrintFailedEffectText */
/* >>> factory DealConfusionDamageToSelf */
typedef struct { uint8_t a; uint8_t f; } DealConfusionDamageToSelfResult;
DealConfusionDamageToSelfResult DealConfusionDamageToSelf(uint8_t a, uint8_t f, uint8_t d, uint8_t e);
/* <<< factory DealConfusionDamageToSelf */
/* >>> factory Func_1bb4 */
typedef struct { uint8_t a; } Func_1bb4Result;
Func_1bb4Result Func_1bb4(uint8_t b, uint8_t c, uint16_t de, uint16_t hl);
/* <<< factory Func_1bb4 */
/* >>> factory DrawInPlayArea_ActiveCardGfx */
void DrawInPlayArea_ActiveCardGfx(void);
/* <<< factory DrawInPlayArea_ActiveCardGfx */
/* >>> factory DrawInPlayAreaScreen */
void DrawInPlayAreaScreen(void);
/* <<< factory DrawInPlayAreaScreen */
/* >>> factory DrawDuelMainScene_PrintPokemonsAttackText */
PrintPokemonsAttackTextResult DrawDuelMainScene_PrintPokemonsAttackText(void);
/* <<< factory DrawDuelMainScene_PrintPokemonsAttackText */
/* >>> factory ProcessPlayedPokemonCard */
DuelRoutineResult ProcessPlayedPokemonCard(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ProcessPlayedPokemonCard */
/* >>> factory _SelectPrizeCards */
void _SelectPrizeCards(void);
/* <<< factory _SelectPrizeCards */
/* >>> factory PlayTrainerCard */
typedef struct { uint8_t f; } PlayTrainerCardResult;
PlayTrainerCardResult PlayTrainerCard(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PlayTrainerCard */
/* >>> factory CheckSelfConfusionDamage */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} CheckSelfConfusionDamageResult;
CheckSelfConfusionDamageResult CheckSelfConfusionDamage(void);
/* <<< factory CheckSelfConfusionDamage */
/* >>> factory ApplyTransparencyIfApplicable */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} ApplyTransparencyResult;
ApplyTransparencyResult ApplyTransparencyIfApplicable(uint8_t initial_f, uint16_t de, uint16_t hl);
/* <<< factory ApplyTransparencyIfApplicable */
/* >>> factory DealDamageToPlayAreaPokemon */
typedef struct { uint8_t a, f; } DealDamageToPlayAreaPokemonResult;
DealDamageToPlayAreaPokemonResult DealDamageToPlayAreaPokemon(uint8_t b, uint16_t de, uint16_t hl);
/* <<< factory DealDamageToPlayAreaPokemon */
/* >>> factory DealDamageToPlayAreaPokemon_RegularAnim */
DealDamageToPlayAreaPokemonResult DealDamageToPlayAreaPokemon_RegularAnim(uint8_t b, uint16_t de, uint16_t hl);
/* <<< factory DealDamageToPlayAreaPokemon_RegularAnim */
/* >>> factory Func_82b6 */
void Func_82b6(void);
/* <<< factory Func_82b6 */
/* >>> factory OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile */
void OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile(uint8_t c);
/* <<< factory OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile */
/* >>> factory OpenYourOrOppPlayAreaScreen_NonTurnHolderHand */
void OpenYourOrOppPlayAreaScreen_NonTurnHolderHand(void);
/* <<< factory OpenYourOrOppPlayAreaScreen_NonTurnHolderHand */
/* >>> factory OpenYourOrOppPlayAreaScreen_TurnHolderHand */
uint8_t OpenYourOrOppPlayAreaScreen_TurnHolderHand(void);
/* <<< factory OpenYourOrOppPlayAreaScreen_TurnHolderHand */
/* >>> factory DealRecoilDamageToSelf */
DealConfusionDamageToSelfResult DealRecoilDamageToSelf(uint8_t a, uint8_t f, uint8_t d, uint8_t e);
/* <<< factory DealRecoilDamageToSelf */
/* >>> factory DuelCheckMenu_Glossary */
void DuelCheckMenu_Glossary(void);
/* <<< factory DuelCheckMenu_Glossary */
/* >>> factory OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile */
void OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile(uint8_t c);
/* <<< factory OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile */
/* >>> factory _HandlePeekSelection */
/* _HandlePeekSelection (engine/menus/duel.asm:1376) has one exit, the
 * .ShowSelectedCard tail: a = [wce5c], with bit 7 set when the pending turn swap
 * fired, and f from that tail's own flag setter -- $80 on the no-swap path (the
 * `or a` that tested the zero wIsSwapTurnPending left Z, and `ld a, [wce5c]`
 * does not touch flags), $00 on the swap path (`or $80` can never be zero).
 * Every other register is jump-table and callee residue, so none is declared. */
typedef struct {
	uint8_t a;
	uint8_t f;
} HandlePeekSelectionResult;
HandlePeekSelectionResult _HandlePeekSelection(void);
/* <<< factory _HandlePeekSelection */
/* >>> factory _OpenDuelCheckMenu */
void _OpenDuelCheckMenu(void);
/* <<< factory _OpenDuelCheckMenu */
/* >>> factory DuelCheckMenu_InPlayArea */
void DuelCheckMenu_InPlayArea(void);
/* <<< factory DuelCheckMenu_InPlayArea */
/* >>> factory DuelCheckMenu_YourPlayArea */
void DuelCheckMenu_YourPlayArea(void);
/* <<< factory DuelCheckMenu_YourPlayArea */
/* >>> factory OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea */
void OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea(void);
/* <<< factory OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea */
/* >>> factory OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea */
void OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea(void);
/* <<< factory OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea */
/* >>> factory DuelCheckMenu_OppPlayArea */
void DuelCheckMenu_OppPlayArea(void);
/* <<< factory DuelCheckMenu_OppPlayArea */
/* >>> factory HandleConfusionDamageToSelf */
typedef struct { uint8_t a; uint8_t f; } HandleConfusionDamageToSelfResult;
HandleConfusionDamageToSelfResult HandleConfusionDamageToSelf(void);
/* <<< factory HandleConfusionDamageToSelf */
/* >>> factory HandleAfterDamageEffects */
typedef struct { uint8_t a; uint8_t f; } HandleAfterDamageEffectsResult;
HandleAfterDamageEffectsResult HandleAfterDamageEffects(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory HandleAfterDamageEffects */
/* >>> factory Func_17ed */
HandleAfterDamageEffectsResult Func_17ed(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory Func_17ed */
/* >>> factory PlayAttackAnimation_DealAttackDamage */
HandleAfterDamageEffectsResult PlayAttackAnimation_DealAttackDamage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PlayAttackAnimation_DealAttackDamage */
/* >>> factory UseAttackOrPokemonPower */
DuelRoutineResult UseAttackOrPokemonPower(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory UseAttackOrPokemonPower */
#endif