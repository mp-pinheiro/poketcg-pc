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
	CardId id;
	uint16_t hl;
} DeckCardResult;
/* <<< part DeckCardResult */
/* >>> factory CountCardIDInLocation */
CardLocationCountResult CountCardIDInLocation(uint8_t b, CardId de, uint16_t hl);
/* <<< factory CountCardIDInLocation */
/* --- part CheckPrizeResult */
/* --- factory CheckPrizeTaken */
/* >>> factory CopyAttackDataAndDamage_FromCardID */
AttackCopyResult CopyAttackDataAndDamage_FromCardID(uint8_t b, uint8_t c, uint16_t de);
/* <<< factory CopyAttackDataAndDamage_FromCardID */
/* --- factory Func_8bf2 */
/* --- factory SendAttackDataToLinkOpponent */
/* --- factory _DrawPlayersPrizeAndBenchCards */
/* >>> factory DrawYourOrOppPlayArea_ActiveCardGfx */
uint16_t DrawYourOrOppPlayArea_ActiveCardGfx(uint16_t de);
/* <<< factory DrawYourOrOppPlayArea_ActiveCardGfx */
/* --- factory Func_17ed */
