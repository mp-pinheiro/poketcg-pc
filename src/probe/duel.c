#include "home/duel.h"
#include "probe.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}

static void adapt_CopyPlayerName(ProbeState *s)
{
	CopyTextResult r = CopyPlayerName(pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_CopyOpponentName(ProbeState *s)
{
	CopyTextResult r = CopyOpponentName(pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_GetTurnDuelistVariable(ProbeState *s)
{
	DuelistVarResult r = GetTurnDuelistVariable(s->a);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_GetNonTurnDuelistVariable(ProbeState *s)
{
	DuelistVarResult r = GetNonTurnDuelistVariable(s->a);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_SwapTurn(ProbeState *s)
{
	(void)s;
	SwapTurn();
}

static void adapt__GetCardIDFromDeckIndex(ProbeState *s)
{
	DeckCardResult r = _GetCardIDFromDeckIndex(s->a);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_GetCardIDFromDeckIndex(ProbeState *s)
{
	uint16_t id = GetCardIDFromDeckIndex(s->a);
	s->d = (uint8_t)(id >> 8);
	s->e = (uint8_t)id;
}

static void adapt_GetCardIDFromDeckIndex_bc(ProbeState *s)
{
	DeckCardResult r = GetCardIDFromDeckIndex_bc(s->a, s->hl);
	s->a = r.a;
	s->b = 0;
	s->c = r.a;
	s->hl = r.hl;
}

static void adapt_GetCardInDuelTempList_OnlyDeckIndex(ProbeState *s)
{
	DeckCardResult r = GetCardInDuelTempList_OnlyDeckIndex(s->a, s->hl);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_GetCardInDuelTempList(ProbeState *s)
{
	DeckEntryResult r = GetCardInDuelTempList(s->a, s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_LoadCardDataToBuffer1_FromDeckIndex(ProbeState *s)
{
	s->a = LoadCardDataToBuffer1_FromDeckIndex(s->a);
}

static void adapt_LoadCardDataToBuffer2_FromDeckIndex(ProbeState *s)
{
	s->a = LoadCardDataToBuffer2_FromDeckIndex(s->a);
}

static void adapt_SubtractHP(ProbeState *s)
{
	SubtractHPResult r = SubtractHP(s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->f = r.f;
}

static void adapt_CreateDeckCardList(ProbeState *s)
{
	CardListResult r = CreateDeckCardList(s->c, pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CreateDiscardPileCardList(ProbeState *s)
{
	CardListResult r = CreateDiscardPileCardList(s->c);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_RemoveCardFromDuelTempList(ProbeState *s)
{
	TempListResult r = RemoveCardFromDuelTempList(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_CountCardsInDuelTempList(ProbeState *s)
{
	TempListResult r = CountCardsInDuelTempList();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_FindLastCardInHand(ProbeState *s)
{
	HandListResult r = FindLastCardInHand(s->c);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CreateHandCardList(ProbeState *s)
{
	HandListResult r = CreateHandCardList(s->c);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CreateArenaOrBenchEnergyCardList(ProbeState *s)
{
	HandListResult r = CreateArenaOrBenchEnergyCardList(s->a);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_ShuffleCards(ProbeState *s)
{
	ShuffleCardsResult r = ShuffleCards(s->a, s->hl);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_SortCardsInListByID(ProbeState *s)
{
	SortResult r = SortCardsInListByID(s->b, s->c, pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_SortCardsInDuelTempListByID(ProbeState *s)
{
	SortResult r = SortCardsInDuelTempListByID(s->b, s->c, pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_SortHandCardsByID(ProbeState *s)
{
	HandSortResult r = SortHandCardsByID();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_TranslateColorToWR(ProbeState *s)
{
	s->a = TranslateColorToWR(s->a);
}

static void adapt_CountCardIDInLocation(ProbeState *s)
{
	CardCountResult r = CountCardIDInLocation(s->b, s->e, s->hl);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_CheckLoadedAttackFlag(ProbeState *s)
{
	AttackFlagResult r = CheckLoadedAttackFlag(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_GetCardDamageAndMaxHP(ProbeState *s)
{
	CardDamageResult r = GetCardDamageAndMaxHP(s->e);
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
}

static void adapt_CopyDeckData(ProbeState *s)
{
	CardListResult r = CopyDeckData(pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CountPrizes(ProbeState *s)
{
	s->a = CountPrizes();
}

static void adapt_ShuffleDeck(ProbeState *s)
{
	ShuffleDeckResult r = ShuffleDeck(s->c, s->e);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_DrawCardFromDeck(ProbeState *s)
{
	DrawCardResult r = DrawCardFromDeck();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_ReturnCardToDeck(ProbeState *s)
{
	ReturnCardToDeck(s->a);
}

static void adapt_SearchCardInDeckAndAddToHand(ProbeState *s)
{
	SearchCardInDeckAndAddToHand(s->a);
}

static void adapt_AddCardToHand(ProbeState *s)
{
	AddCardToHand(s->a);
}

static void adapt_RemoveCardFromHand(ProbeState *s)
{
	RemoveCardFromHand(s->a);
}

static void adapt_MoveHandCardToDiscardPile(ProbeState *s)
{
	MoveCardResult r = MoveHandCardToDiscardPile(s->a);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_PutCardInDiscardPile(ProbeState *s)
{
	PutCardInDiscardPile(s->a);
}

static void adapt_MoveDiscardPileCardToHand(ProbeState *s)
{
	MoveDiscardResult r = MoveDiscardPileCardToHand(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_CheckPrizeTaken(ProbeState *s)
{
	CheckPrizeResult r = CheckPrizeTaken(s->a);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_SortCardsInListByID_CheckForListTerminator(ProbeState *s)
{
	SortResult r = SortCardsInListByID_CheckForListTerminator(s->b, s->c, pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CheckIfCanEvolveInto(ProbeState *s)
{
	EvolveResult r = CheckIfCanEvolveInto(s->d, s->e);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CheckIfCanEvolveInto_BasicToStage2(ProbeState *s)
{
	EvolveResult r = CheckIfCanEvolveInto_BasicToStage2(s->d, s->e);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_EvolvePokemonCardIfPossible(ProbeState *s)
{
	EvolveResult r = EvolvePokemonCardIfPossible(s->c);
	s->a = r.a;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_EvolvePokemonCard(ProbeState *s)
{
	EvolveResult r = EvolvePokemonCard();
	s->a = r.a;
	s->c = r.c;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_ClearAllStatusConditions(ProbeState *s)
{
	(void)s;
	ClearAllStatusConditions();
}

static void adapt_PutHandCardInPlayArea(ProbeState *s)
{
	PutHandResult r = PutHandCardInPlayArea(s->a, s->e);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_PutHandPokemonCardInPlayArea(ProbeState *s)
{
	PutHandPokemonResult r = PutHandPokemonCardInPlayArea(s->a, s->f);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_EmptyPlayAreaSlot(ProbeState *s)
{
	EmptySlotResult r = EmptyPlayAreaSlot(s->e);
	s->a = r.a;
	s->d = r.d;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_MovePlayAreaCardToDiscardPile(ProbeState *s)
{
	MoveAreaResult r = MovePlayAreaCardToDiscardPile(s->e);
	s->a = r.a;
	s->d = r.d;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_SwapPlayAreaPokemon(ProbeState *s)
{
	SwapAreaResult r = SwapPlayAreaPokemon(s->d, s->e);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_SwapArenaWithBenchPokemon(ProbeState *s)
{
	SwapAreaResult r = SwapArenaWithBenchPokemon(s->e);
	s->a = r.a;
	s->d = r.d;
	s->f = r.f;
}

static void adapt_ShiftTurnPokemonToFirstPlayAreaSlots(ProbeState *s)
{
	ShiftResult r = ShiftTurnPokemonToFirstPlayAreaSlots();
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_ShiftAllPokemonToFirstPlayAreaSlots(ProbeState *s)
{
	ShiftResult r = ShiftAllPokemonToFirstPlayAreaSlots();
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_GetPlayAreaCardAttachedEnergies(ProbeState *s)
{
	EnergiesResult r = GetPlayAreaCardAttachedEnergies(s->e);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_CopyAttackDataAndDamage(ProbeState *s)
{
	AttackCopyResult r = CopyAttackDataAndDamage(s->e);
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_CopyAttackDataAndDamage_FromDeckIndex(ProbeState *s)
{
	AttackCopyResult r = CopyAttackDataAndDamage_FromDeckIndex(s->d, s->e);
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_CopyAttackDataAndDamage_FromCardID(ProbeState *s)
{
	AttackCopyResult r = CopyAttackDataAndDamage_FromCardID(s->a, s->d, s->e);
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_ReturnCarry(ProbeState *s)
{
	s->f = ReturnCarry(s->f);
}

static void adapt_LoadNonPokemonCardEffectCommands(ProbeState *s)
{
	LoadEffectResult r = LoadNonPokemonCardEffectCommands();
	s->a = r.a;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_ApplyAttachedPlusPower(ProbeState *s)
{
	PowerModifierResult r = ApplyAttachedPlusPower(s->b, pair(s->d, s->e));
	s->hl = r.de;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_ApplyAttachedDefender(ProbeState *s)
{
	PowerModifierResult r = ApplyAttachedDefender(s->b, pair(s->d, s->e));
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}

static void adapt_MoveCardToDiscardPileIfInPlayArea(ProbeState *s)
{
	DiscardIfInPlayResult r = MoveCardToDiscardPileIfInPlayArea(pair(s->d, s->e),
								     (uint8_t)(s->hl >> 8));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}
static void adapt_ApplyDamageModifiers_DamageToTarget(ProbeState *s)
{
	uint16_t de = ApplyDamageModifiers_DamageToTarget();
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
static void adapt_ApplyDamageModifiers_DamageToSelf(ProbeState *s)
{
	uint16_t de = ApplyDamageModifiers_DamageToSelf();
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
static void adapt_GetPlayAreaCardRetreatCost(ProbeState *s)
{
	s->a = GetPlayAreaCardRetreatCost();
}

static void adapt_DrawWideTextBox_WaitForInput_ReturnCarry(ProbeState *s)
{
	s->f = DrawWideTextBox_WaitForInput_ReturnCarry(s->hl);
}

static void adapt_PrintKnockedOut(ProbeState *s)
{
	s->f = PrintKnockedOut();
}
static void adapt_PrintPlayAreaCardKnockedOutIfNoHP(ProbeState *s)
{
	KnockoutCheckResult r = PrintPlayAreaCardKnockedOutIfNoHP(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_UpdateArenaCardIDsAndClearTwoTurnDuelVars(ProbeState *s)
{
	DuelRoutineResult r = UpdateArenaCardIDsAndClearTwoTurnDuelVars(
		s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_ClearNonTurnTemporaryDuelvars_ResetCarry(ProbeState *s)
{
	DuelRoutineResult r = ClearNonTurnTemporaryDuelvars_ResetCarry(
		s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_PrintKnockedOutIfHLZero(ProbeState *s)
{
	s->f = PrintKnockedOutIfHLZero(s->hl);
}

/* >>> factory GetFirstSetPrizeCard */
static void adapt_GetFirstSetPrizeCard(ProbeState *s)
{
	s->a = GetFirstSetPrizeCard(s->a);
}
/* <<< factory GetFirstSetPrizeCard */

/* >>> factory DrawCheckMenuCursor_YourOrOppPlayArea */
static void adapt_DrawCheckMenuCursor_YourOrOppPlayArea(ProbeState *s)
{
	TempListResult r = DrawCheckMenuCursor_YourOrOppPlayArea(s->a);

	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DrawCheckMenuCursor_YourOrOppPlayArea */

/* >>> factory ZeroObjectPositionsWithCopyToggleOn */
static void adapt_ZeroObjectPositionsWithCopyToggleOn(ProbeState *s)
{
	(void)s;
	ZeroObjectPositionsWithCopyToggleOn();
}
/* <<< factory ZeroObjectPositionsWithCopyToggleOn */

/* >>> factory YourOrOppPlayAreaScreen_HandleInput */
static void adapt_YourOrOppPlayAreaScreen_HandleInput(ProbeState *s)
{
	(void)s;
	YourOrOppPlayAreaScreen_HandleInput();
}
/* <<< factory YourOrOppPlayAreaScreen_HandleInput */

/* >>> factory DrawPlayArea_BenchCards */
static void adapt_DrawPlayArea_BenchCards(ProbeState *s)
{
	DrawPlayArea_BenchCards(s->c, s->d, s->e);
}
/* <<< factory DrawPlayArea_BenchCards */

/* >>> factory EraseCheckMenuCursor_YourOrOppPlayArea */
static void adapt_EraseCheckMenuCursor_YourOrOppPlayArea(ProbeState *s)
{
	TempListResult r = EraseCheckMenuCursor_YourOrOppPlayArea();

	s->a = r.a;
	s->f = r.f;
}
/* <<< factory EraseCheckMenuCursor_YourOrOppPlayArea */

/* >>> factory LoadCursorTile */
static void adapt_LoadCursorTile(ProbeState *s)
{
	(void)s;
	LoadCursorTile();
}
/* <<< factory LoadCursorTile */

/* >>> factory Func_8bf2 */
static void adapt_Func_8bf2(ProbeState *s)
{
	PrizeTileResult r = Func_8bf2(s->f, s->d, s->e, s->hl);

	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory Func_8bf2 */

/* >>> factory GetDuelInitialPrizesUpperBitsSet */
static void adapt_GetDuelInitialPrizesUpperBitsSet(ProbeState *s)
{
	(void)s;
	GetDuelInitialPrizesUpperBitsSet();
}
/* <<< factory GetDuelInitialPrizesUpperBitsSet */

/* >>> factory DrawYourOrOppPlayArea_DrawArrows */
static void adapt_DrawYourOrOppPlayArea_DrawArrows(ProbeState *s)
{
	DrawYourOrOppPlayArea_DrawArrows(s->a, s->b);
}
/* <<< factory DrawYourOrOppPlayArea_DrawArrows */

/* >>> factory DrawYourOrOppPlayArea_EraseArrows */
static void adapt_DrawYourOrOppPlayArea_EraseArrows(ProbeState *s)
{
	DrawYourOrOppPlayArea_EraseArrows();
}
/* <<< factory DrawYourOrOppPlayArea_EraseArrows */

/* >>> factory DrawYourOrOppPlayArea_RefreshArrows */
static void adapt_DrawYourOrOppPlayArea_RefreshArrows(ProbeState *s)
{
	DrawYourOrOppPlayArea_RefreshArrows(s->a);
}
/* <<< factory DrawYourOrOppPlayArea_RefreshArrows */

/* >>> factory SendAttackDataToLinkOpponent */
static void adapt_SendAttackDataToLinkOpponent(ProbeState *s)
{
	(void)s;
	SendAttackDataToLinkOpponent();
}
/* <<< factory SendAttackDataToLinkOpponent */

/* >>> factory DrawPlayArea_PrizeCards */
static void adapt_DrawPlayArea_PrizeCards(ProbeState *s)
{
	DrawPlayArea_PrizeCards(s->hl);
}
/* <<< factory DrawPlayArea_PrizeCards */

/* >>> factory _DrawPlayersPrizeAndBenchCards */
static void adapt__DrawPlayersPrizeAndBenchCards(ProbeState *s)
{
	_DrawPlayersPrizeAndBenchCards();
	(void)s;
}
/* <<< factory _DrawPlayersPrizeAndBenchCards */

/* >>> factory DrawPlayArea_HandText */
static void adapt_DrawPlayArea_HandText(ProbeState *s)
{
	DrawPlayArea_HandTextResult r = DrawPlayArea_HandText(s->b, s->c, s->hl);
	s->b = r.b; s->c = r.c; s->hl = r.hl;
}
/* <<< factory DrawPlayArea_HandText */

/* >>> factory DrawPlayArea_IconWithValue */
static void adapt_DrawPlayArea_IconWithValue(ProbeState *s)
{
	DrawPlayArea_IconWithValue(s->a, s->b, &s->hl);
}
/* <<< factory DrawPlayArea_IconWithValue */

/* >>> factory SaveDuelStateToSRAM */
static void adapt_SaveDuelStateToSRAM(ProbeState *s)
{
	(void)s;
	SaveDuelStateToSRAM();
}
/* <<< factory SaveDuelStateToSRAM */

/* >>> factory DisplayCheckMenuCursor_YourOrOppPlayArea */
static void adapt_DisplayCheckMenuCursor_YourOrOppPlayArea(ProbeState *s)
{
	TempListResult r = DisplayCheckMenuCursor_YourOrOppPlayArea();
	s->a = r.a; s->f = r.f;
}
/* <<< factory DisplayCheckMenuCursor_YourOrOppPlayArea */

/* >>> factory HandleCheckMenuInput_YourOrOppPlayArea */
static void adapt_HandleCheckMenuInput_YourOrOppPlayArea(ProbeState *s)
{
	TempListResult r = HandleCheckMenuInput_YourOrOppPlayArea();
	s->a = r.a; s->f = r.f;
}
/* <<< factory HandleCheckMenuInput_YourOrOppPlayArea */

/* >>> factory DrawYourOrOppPlayArea_Icons */
static void adapt_DrawYourOrOppPlayArea_Icons(ProbeState *s)
{
	DrawYourOrOppPlayArea_Icons(s->a);
}
/* <<< factory DrawYourOrOppPlayArea_Icons */

/* >>> factory DrawInPlayArea_Icons */
static void adapt_DrawInPlayArea_Icons(ProbeState *s)
{
	DrawInPlayArea_Icons(s->hl);
}
/* <<< factory DrawInPlayArea_Icons */

/* >>> factory DisplayUsePokemonPowerScreen_WaitForInput */
static void adapt_DisplayUsePokemonPowerScreen_WaitForInput(ProbeState *s)
{
	s->f = DisplayUsePokemonPowerScreen_WaitForInput(s->hl);
}
/* <<< factory DisplayUsePokemonPowerScreen_WaitForInput */

/* >>> factory _DrawPlayAreaToPlacePrizeCards */
static void adapt__DrawPlayAreaToPlacePrizeCards(ProbeState *s)
{
	(void)s;
	_DrawPlayAreaToPlacePrizeCards();
}
/* <<< factory _DrawPlayAreaToPlacePrizeCards */

/* >>> factory UsePokemonPower */
static void adapt_UsePokemonPower(ProbeState *s)
{
	UsePokemonPowerResult r = UsePokemonPower(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory UsePokemonPower */

/* >>> factory DrawYourOrOppPlayArea_ActiveCardGfx */
static void adapt_DrawYourOrOppPlayArea_ActiveCardGfx(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8 | s->e);
	DrawYourOrOppPlayArea_ActiveCardGfx(de);
}
/* <<< factory DrawYourOrOppPlayArea_ActiveCardGfx */

/* >>> factory _DrawYourOrOppPlayAreaScreen */
static void adapt__DrawYourOrOppPlayAreaScreen(ProbeState *s)
{
	(void)s;
	_DrawYourOrOppPlayAreaScreen();
}
/* <<< factory _DrawYourOrOppPlayAreaScreen */

/* >>> factory DrawYourOrOppPlayAreaScreen */
static void adapt_DrawYourOrOppPlayAreaScreen(ProbeState *s)
{
	DrawYourOrOppPlayAreaScreen(s->hl);
}
/* <<< factory DrawYourOrOppPlayAreaScreen */

/* >>> factory _DrawAIPeekScreen */
static void adapt__DrawAIPeekScreen(ProbeState *s)
{
	_DrawAIPeekScreen(s->b);
}
/* <<< factory _DrawAIPeekScreen */

/* >>> factory PrintPokemonsAttackText */
static void adapt_PrintPokemonsAttackText(ProbeState *s)
{
	PrintPokemonsAttackTextResult r = PrintPokemonsAttackText();
	s->hl = r.hl;
}
/* <<< factory PrintPokemonsAttackText */

/* >>> factory PrintFailedEffectText */
static void adapt_PrintFailedEffectText(ProbeState *s)
{
	PrintFailedEffectTextResult result = PrintFailedEffectText();
	s->f = result.f;
}
/* <<< factory PrintFailedEffectText */

/* >>> factory DealConfusionDamageToSelf */
static void adapt_DealConfusionDamageToSelf(ProbeState *s)
{
	DealConfusionDamageToSelfResult r = DealConfusionDamageToSelf(s->a, s->f, s->d, s->e);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DealConfusionDamageToSelf */

/* >>> factory Func_1bb4 */
static void adapt_Func_1bb4(ProbeState *s)
{
	Func_1bb4Result r = Func_1bb4(s->b, s->c,
		(uint16_t)(((uint16_t)s->d << 8) | s->e), s->hl);
	s->a = r.a;
}
/* <<< factory Func_1bb4 */


/* >>> factory DrawInPlayArea_ActiveCardGfx */
static void adapt_DrawInPlayArea_ActiveCardGfx(ProbeState *s)
{
	(void)s;
	DrawInPlayArea_ActiveCardGfx();
}
/* <<< factory DrawInPlayArea_ActiveCardGfx */

/* >>> factory DrawInPlayAreaScreen */
static void adapt_DrawInPlayAreaScreen(ProbeState *s)
{
	DrawInPlayAreaScreen();
}
/* <<< factory DrawInPlayAreaScreen */

/* >>> factory DrawDuelMainScene_PrintPokemonsAttackText */
static void adapt_DrawDuelMainScene_PrintPokemonsAttackText(ProbeState *s)
{
	PrintPokemonsAttackTextResult r = DrawDuelMainScene_PrintPokemonsAttackText();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory DrawDuelMainScene_PrintPokemonsAttackText */

/* >>> factory ProcessPlayedPokemonCard */
static void adapt_ProcessPlayedPokemonCard(ProbeState *s)
{
	DuelRoutineResult r = ProcessPlayedPokemonCard(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory ProcessPlayedPokemonCard */

/* >>> factory _SelectPrizeCards */
static void adapt__SelectPrizeCards(ProbeState *s)
{
	_SelectPrizeCards();
}
/* <<< factory _SelectPrizeCards */

/* >>> factory PlayTrainerCard */
static void adapt_PlayTrainerCard(ProbeState *s)
{
	PlayTrainerCardResult r = PlayTrainerCard(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->f = r.f;
}
/* <<< factory PlayTrainerCard */

/* >>> factory CheckSelfConfusionDamage */
static void adapt_CheckSelfConfusionDamage(ProbeState *s)
{
	CheckSelfConfusionDamageResult result = CheckSelfConfusionDamage();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory CheckSelfConfusionDamage */

/* >>> factory ApplyTransparencyIfApplicable */
static void adapt_ApplyTransparencyIfApplicable(ProbeState *s)
{
	ApplyTransparencyResult result = ApplyTransparencyIfApplicable(s->f, (uint16_t)(((uint16_t)s->d << 8) | s->e), s->hl);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory ApplyTransparencyIfApplicable */

/* >>> factory DealDamageToPlayAreaPokemon */
static void adapt_DealDamageToPlayAreaPokemon(ProbeState *s)
{
	DealDamageToPlayAreaPokemonResult r = DealDamageToPlayAreaPokemon(s->b, (uint16_t)(((uint16_t)s->d << 8u) | s->e), s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DealDamageToPlayAreaPokemon */

/* >>> factory DealDamageToPlayAreaPokemon_RegularAnim */
static void adapt_DealDamageToPlayAreaPokemon_RegularAnim(ProbeState *s)
{
	DealDamageToPlayAreaPokemonResult r = DealDamageToPlayAreaPokemon_RegularAnim(s->b, (uint16_t)(((uint16_t)s->d << 8u) | s->e), s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DealDamageToPlayAreaPokemon_RegularAnim */


/* >>> factory Func_82b6 */
static void adapt_Func_82b6(ProbeState *s)
{
	(void)s;
	Func_82b6();
}
/* <<< factory Func_82b6 */

/* >>> factory OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile */
static void adapt_OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile(ProbeState *s)
{
	OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile(s->c);
}
/* <<< factory OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile */

/* >>> factory OpenYourOrOppPlayAreaScreen_NonTurnHolderHand */
static void adapt_OpenYourOrOppPlayAreaScreen_NonTurnHolderHand(ProbeState *s)
{
	OpenYourOrOppPlayAreaScreen_NonTurnHolderHand();
}
/* <<< factory OpenYourOrOppPlayAreaScreen_NonTurnHolderHand */

const ProbeEntry probe_entries_duel[] = {
	{ "Func_82b6", adapt_Func_82b6 },
	{ "CopyPlayerName", adapt_CopyPlayerName },
	{ "CopyOpponentName", adapt_CopyOpponentName },
	{ "GetTurnDuelistVariable", adapt_GetTurnDuelistVariable },
	{ "GetNonTurnDuelistVariable", adapt_GetNonTurnDuelistVariable },
	{ "SwapTurn", adapt_SwapTurn },
	{ "_GetCardIDFromDeckIndex", adapt__GetCardIDFromDeckIndex },
	{ "GetCardIDFromDeckIndex", adapt_GetCardIDFromDeckIndex },
	{ "GetCardIDFromDeckIndex_bc", adapt_GetCardIDFromDeckIndex_bc },
	{ "GetCardInDuelTempList_OnlyDeckIndex", adapt_GetCardInDuelTempList_OnlyDeckIndex },
	{ "GetCardInDuelTempList", adapt_GetCardInDuelTempList },
	{ "LoadCardDataToBuffer1_FromDeckIndex", adapt_LoadCardDataToBuffer1_FromDeckIndex },
	{ "LoadCardDataToBuffer2_FromDeckIndex", adapt_LoadCardDataToBuffer2_FromDeckIndex },
	{ "SubtractHP", adapt_SubtractHP },
	{ "CreateDeckCardList", adapt_CreateDeckCardList },
	{ "CreateDiscardPileCardList", adapt_CreateDiscardPileCardList },
	{ "RemoveCardFromDuelTempList", adapt_RemoveCardFromDuelTempList },
	{ "CountCardsInDuelTempList", adapt_CountCardsInDuelTempList },
	{ "FindLastCardInHand", adapt_FindLastCardInHand },
	{ "CreateHandCardList", adapt_CreateHandCardList },
	{ "CreateArenaOrBenchEnergyCardList", adapt_CreateArenaOrBenchEnergyCardList },
	{ "ShuffleCards", adapt_ShuffleCards },
	{ "SortCardsInListByID", adapt_SortCardsInListByID },
	{ "SortCardsInDuelTempListByID", adapt_SortCardsInDuelTempListByID },
	{ "SortHandCardsByID", adapt_SortHandCardsByID },
	{ "TranslateColorToWR", adapt_TranslateColorToWR },
	{ "CountCardIDInLocation", adapt_CountCardIDInLocation },
	{ "CheckLoadedAttackFlag", adapt_CheckLoadedAttackFlag },
	{ "GetCardDamageAndMaxHP", adapt_GetCardDamageAndMaxHP },
	{ "CopyDeckData", adapt_CopyDeckData },
	{ "CountPrizes", adapt_CountPrizes },
	{ "ShuffleDeck", adapt_ShuffleDeck },
	{ "DrawCardFromDeck", adapt_DrawCardFromDeck },
	{ "ReturnCardToDeck", adapt_ReturnCardToDeck },
	{ "SearchCardInDeckAndAddToHand", adapt_SearchCardInDeckAndAddToHand },
	{ "AddCardToHand", adapt_AddCardToHand },
	{ "RemoveCardFromHand", adapt_RemoveCardFromHand },
	{ "MoveHandCardToDiscardPile", adapt_MoveHandCardToDiscardPile },
	{ "PutCardInDiscardPile", adapt_PutCardInDiscardPile },
	{ "MoveDiscardPileCardToHand", adapt_MoveDiscardPileCardToHand },
	{ "CheckPrizeTaken", adapt_CheckPrizeTaken },
	{ "SortCardsInListByID_CheckForListTerminator", adapt_SortCardsInListByID_CheckForListTerminator },
	{ "CheckIfCanEvolveInto", adapt_CheckIfCanEvolveInto },
	{ "CheckIfCanEvolveInto_BasicToStage2", adapt_CheckIfCanEvolveInto_BasicToStage2 },
	{ "EvolvePokemonCardIfPossible", adapt_EvolvePokemonCardIfPossible },
	{ "EvolvePokemonCard", adapt_EvolvePokemonCard },
	{ "ClearAllStatusConditions", adapt_ClearAllStatusConditions },
	{ "PutHandCardInPlayArea", adapt_PutHandCardInPlayArea },
	{ "PutHandPokemonCardInPlayArea", adapt_PutHandPokemonCardInPlayArea },
	{ "EmptyPlayAreaSlot", adapt_EmptyPlayAreaSlot },
	{ "MovePlayAreaCardToDiscardPile", adapt_MovePlayAreaCardToDiscardPile },
	{ "SwapPlayAreaPokemon", adapt_SwapPlayAreaPokemon },
	{ "SwapArenaWithBenchPokemon", adapt_SwapArenaWithBenchPokemon },
	{ "ShiftTurnPokemonToFirstPlayAreaSlots", adapt_ShiftTurnPokemonToFirstPlayAreaSlots },
	{ "ShiftAllPokemonToFirstPlayAreaSlots", adapt_ShiftAllPokemonToFirstPlayAreaSlots },
	{ "GetPlayAreaCardAttachedEnergies", adapt_GetPlayAreaCardAttachedEnergies },
	{ "CopyAttackDataAndDamage", adapt_CopyAttackDataAndDamage },
	{ "CopyAttackDataAndDamage_FromDeckIndex", adapt_CopyAttackDataAndDamage_FromDeckIndex },
	{ "CopyAttackDataAndDamage_FromCardID", adapt_CopyAttackDataAndDamage_FromCardID },
	{ "ReturnCarry", adapt_ReturnCarry },
	{ "LoadNonPokemonCardEffectCommands", adapt_LoadNonPokemonCardEffectCommands },
	{ "ApplyAttachedPlusPower", adapt_ApplyAttachedPlusPower },
	{ "ApplyAttachedDefender", adapt_ApplyAttachedDefender },
	{ "MoveCardToDiscardPileIfInPlayArea", adapt_MoveCardToDiscardPileIfInPlayArea },
	{ "ApplyDamageModifiers_DamageToTarget", adapt_ApplyDamageModifiers_DamageToTarget },
	{ "ApplyDamageModifiers_DamageToSelf", adapt_ApplyDamageModifiers_DamageToSelf },
	{ "GetPlayAreaCardRetreatCost", adapt_GetPlayAreaCardRetreatCost },
	{ "DrawWideTextBox_WaitForInput_ReturnCarry", adapt_DrawWideTextBox_WaitForInput_ReturnCarry },
	{ "PrintKnockedOut", adapt_PrintKnockedOut },
	{ "UpdateArenaCardIDsAndClearTwoTurnDuelVars", adapt_UpdateArenaCardIDsAndClearTwoTurnDuelVars },
	{ "ClearNonTurnTemporaryDuelvars_ResetCarry", adapt_ClearNonTurnTemporaryDuelvars_ResetCarry },
	{ "PrintKnockedOutIfHLZero", adapt_PrintKnockedOutIfHLZero },
	{ "PrintPlayAreaCardKnockedOutIfNoHP", adapt_PrintPlayAreaCardKnockedOutIfNoHP },
	{ "GetFirstSetPrizeCard", adapt_GetFirstSetPrizeCard },
	{ "DrawCheckMenuCursor_YourOrOppPlayArea", adapt_DrawCheckMenuCursor_YourOrOppPlayArea },
	{ "ZeroObjectPositionsWithCopyToggleOn", adapt_ZeroObjectPositionsWithCopyToggleOn },
	{ "YourOrOppPlayAreaScreen_HandleInput", adapt_YourOrOppPlayAreaScreen_HandleInput },
	{ "DrawPlayArea_BenchCards", adapt_DrawPlayArea_BenchCards },
	{ "EraseCheckMenuCursor_YourOrOppPlayArea", adapt_EraseCheckMenuCursor_YourOrOppPlayArea },
	{ "LoadCursorTile", adapt_LoadCursorTile },
	{ "Func_8bf2", adapt_Func_8bf2 },
	{ "GetDuelInitialPrizesUpperBitsSet", adapt_GetDuelInitialPrizesUpperBitsSet },
	{ "DrawYourOrOppPlayArea_DrawArrows", adapt_DrawYourOrOppPlayArea_DrawArrows },
	{ "DrawYourOrOppPlayArea_EraseArrows", adapt_DrawYourOrOppPlayArea_EraseArrows },
	{ "DrawYourOrOppPlayArea_RefreshArrows", adapt_DrawYourOrOppPlayArea_RefreshArrows },
	{ "SendAttackDataToLinkOpponent", adapt_SendAttackDataToLinkOpponent },
	{ "DrawPlayArea_PrizeCards", adapt_DrawPlayArea_PrizeCards },
	{ "_DrawPlayersPrizeAndBenchCards", adapt__DrawPlayersPrizeAndBenchCards },
	{ "DrawPlayArea_HandText", adapt_DrawPlayArea_HandText },
	{ "DrawPlayArea_IconWithValue", adapt_DrawPlayArea_IconWithValue },
	{ "SaveDuelStateToSRAM", adapt_SaveDuelStateToSRAM },
	{ "DisplayCheckMenuCursor_YourOrOppPlayArea", adapt_DisplayCheckMenuCursor_YourOrOppPlayArea },
	{ "HandleCheckMenuInput_YourOrOppPlayArea", adapt_HandleCheckMenuInput_YourOrOppPlayArea },
	{ "DrawYourOrOppPlayArea_Icons", adapt_DrawYourOrOppPlayArea_Icons },
	{ "DrawInPlayArea_Icons", adapt_DrawInPlayArea_Icons },
	{ "DisplayUsePokemonPowerScreen_WaitForInput", adapt_DisplayUsePokemonPowerScreen_WaitForInput },
	{ "_DrawPlayAreaToPlacePrizeCards", adapt__DrawPlayAreaToPlacePrizeCards },
	{ "UsePokemonPower", adapt_UsePokemonPower },
	{ "DrawYourOrOppPlayArea_ActiveCardGfx", adapt_DrawYourOrOppPlayArea_ActiveCardGfx },
	{ "_DrawYourOrOppPlayAreaScreen", adapt__DrawYourOrOppPlayAreaScreen },
	{ "DrawYourOrOppPlayAreaScreen", adapt_DrawYourOrOppPlayAreaScreen },
	{ "_DrawAIPeekScreen", adapt__DrawAIPeekScreen },
	{ "PrintPokemonsAttackText", adapt_PrintPokemonsAttackText },
	{ "PrintFailedEffectText", adapt_PrintFailedEffectText },
	{ "DealConfusionDamageToSelf", adapt_DealConfusionDamageToSelf },
	{ "Func_1bb4", adapt_Func_1bb4 },
	{ "DrawInPlayArea_ActiveCardGfx", adapt_DrawInPlayArea_ActiveCardGfx },
	{ "DrawInPlayAreaScreen", adapt_DrawInPlayAreaScreen },
	{ "DrawDuelMainScene_PrintPokemonsAttackText", adapt_DrawDuelMainScene_PrintPokemonsAttackText },
	{ "ProcessPlayedPokemonCard", adapt_ProcessPlayedPokemonCard },
	{ "_SelectPrizeCards", adapt__SelectPrizeCards },
	{ "PlayTrainerCard", adapt_PlayTrainerCard },
	{ "CheckSelfConfusionDamage", adapt_CheckSelfConfusionDamage },
	{ "ApplyTransparencyIfApplicable", adapt_ApplyTransparencyIfApplicable },
	{ "DealDamageToPlayAreaPokemon", adapt_DealDamageToPlayAreaPokemon },
	{ "DealDamageToPlayAreaPokemon_RegularAnim", adapt_DealDamageToPlayAreaPokemon_RegularAnim },
	{ "OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile", adapt_OpenYourOrOppPlayAreaScreen_TurnHolderDiscardPile },
	{ "OpenYourOrOppPlayAreaScreen_NonTurnHolderHand", adapt_OpenYourOrOppPlayAreaScreen_NonTurnHolderHand },
	{ NULL, NULL },
};
