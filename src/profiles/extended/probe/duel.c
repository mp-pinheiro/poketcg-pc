/* >>> factory _GetCardIDFromDeckIndex */
static void adapt__GetCardIDFromDeckIndex(ProbeState *s)
{
	DeckCardResult r = _GetCardIDFromDeckIndex(s->a);
	s->a = r.a;
	s->d = (uint8_t)(r.id >> 8);
	s->e = (uint8_t)r.id;
	s->hl = r.hl;

}
/* <<< factory _GetCardIDFromDeckIndex */
/* >>> factory GetCardIDFromDeckIndex_bc */
static void adapt_GetCardIDFromDeckIndex_bc(ProbeState *s)
{
	DeckCardResult r = GetCardIDFromDeckIndex_bc(s->a, s->hl);
	s->a = r.a;
	s->b = (uint8_t)(r.id >> 8);
	s->c = (uint8_t)r.id;
	s->hl = r.hl;
}
/* <<< factory GetCardIDFromDeckIndex_bc */
/* >>> factory CountCardIDInLocation */
static void adapt_CountCardIDInLocation(ProbeState *s)
{
	CardLocationCountResult r = CountCardIDInLocation(s->b, pair(s->d, s->e), s->hl);
	s->a = r.a;
	s->hl = r.hl;
}
/* <<< factory CountCardIDInLocation */
/* --- factory CheckPrizeTaken */
/* >>> factory CopyAttackDataAndDamage_FromCardID */
static void adapt_CopyAttackDataAndDamage_FromCardID(ProbeState *s)
{
	AttackCopyResult r = CopyAttackDataAndDamage_FromCardID(s->b, s->c, pair(s->d, s->e));
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory CopyAttackDataAndDamage_FromCardID */
/* --- factory Func_8bf2 */
/* --- factory SendAttackDataToLinkOpponent */
/* --- factory _DrawPlayersPrizeAndBenchCards */
/* >>> factory DrawYourOrOppPlayArea_ActiveCardGfx */
static void adapt_DrawYourOrOppPlayArea_ActiveCardGfx(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8 | s->e);
	de = DrawYourOrOppPlayArea_ActiveCardGfx(de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory DrawYourOrOppPlayArea_ActiveCardGfx */
/* --- factory Func_17ed */
/* >>> part probe_entries_duel */
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
	{ "SortCardsInListByID_CheckForListTerminator", adapt_SortCardsInListByID_CheckForListTerminator },
	{ "CheckIfCanEvolveInto", adapt_CheckIfCanEvolveInto },
	{ "CheckIfCanEvolveInto_BasicToStage2", adapt_CheckIfCanEvolveInto_BasicToStage2 },
	{ "EvolvePokemonCardIfPossible", adapt_EvolvePokemonCardIfPossible },
	{ "EvolvePokemonCard", adapt_EvolvePokemonCard },
	{ "ClearAllStatusConditions", adapt_ClearAllStatusConditions },
	{ "PutHandCardInPlayArea", adapt_PutHandCardInPlayArea },
	{ "PutHandPokemonCardInPlayArea", adapt_PutHandPokemonCardInPlayArea },
	{ "EmptyPlayAreaSlot", adapt_EmptyPlayAreaSlot },
	{ "EmptyPlayAreaSlot.init_duelvar", adapt_EmptyPlayAreaSlot_init_duelvar },
	{ "SwapPlayAreaPokemon.swap_duelvar", adapt_SwapPlayAreaPokemon_swap_duelvar },
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
	{ "GetDuelInitialPrizesUpperBitsSet", adapt_GetDuelInitialPrizesUpperBitsSet },
	{ "DrawYourOrOppPlayArea_DrawArrows", adapt_DrawYourOrOppPlayArea_DrawArrows },
	{ "DrawYourOrOppPlayArea_EraseArrows", adapt_DrawYourOrOppPlayArea_EraseArrows },
	{ "DrawYourOrOppPlayArea_RefreshArrows", adapt_DrawYourOrOppPlayArea_RefreshArrows },
	{ "DrawPlayArea_PrizeCards", adapt_DrawPlayArea_PrizeCards },
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
	{ "OpenYourOrOppPlayAreaScreen_TurnHolderHand", adapt_OpenYourOrOppPlayAreaScreen_TurnHolderHand },
	{ "DealRecoilDamageToSelf", adapt_DealRecoilDamageToSelf },
	{ "DuelCheckMenu_Glossary", adapt_DuelCheckMenu_Glossary },
	{ "OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile", adapt_OpenYourOrOppPlayAreaScreen_NonTurnHolderDiscardPile },
	{ "_HandlePeekSelection", adapt__HandlePeekSelection },
	{ "_OpenDuelCheckMenu", adapt__OpenDuelCheckMenu },
	{ "DuelCheckMenu_InPlayArea", adapt_DuelCheckMenu_InPlayArea },
	{ "DuelCheckMenu_YourPlayArea", adapt_DuelCheckMenu_YourPlayArea },
	{ "OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea", adapt_OpenYourOrOppPlayAreaScreen_TurnHolderPlayArea },
	{ "OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea", adapt_OpenYourOrOppPlayAreaScreen_NonTurnHolderPlayArea },
	{ "DuelCheckMenu_OppPlayArea", adapt_DuelCheckMenu_OppPlayArea },
	{ "HandleConfusionDamageToSelf", adapt_HandleConfusionDamageToSelf },
	{ "HandleAfterDamageEffects", adapt_HandleAfterDamageEffects },
	{ "PlayAttackAnimation_DealAttackDamage", adapt_PlayAttackAnimation_DealAttackDamage },
	{ "UseAttackOrPokemonPower", adapt_UseAttackOrPokemonPower },
	{ NULL, NULL },
};
/* <<< part probe_entries_duel */
