/* --- factory ValidateSavedDuelDataFromHL */
/* === factory DrawHPBar */
/* >>> factory ValidateSavedDuelData */
static void adapt_ValidateSavedDuelData(ProbeState *s)
{
	ValidateSavedDuelDataResult r = ValidateSavedDuelData(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ValidateSavedDuelData */
/* >>> factory LoadSavedDuelData */
static void adapt_LoadSavedDuelData(ProbeState *s)
{
	LoadSavedDuelData((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory LoadSavedDuelData */
/* >>> factory DiscardSavedDuelData */
static void adapt_DiscardSavedDuelData(ProbeState *s)
{
	(void)s;
	DiscardSavedDuelData();
}
/* <<< factory DiscardSavedDuelData */
/* --- factory CopyCGBCardPalette */
/* --- factory CreateCardAttrBlkPacket_DataSet */
/* --- factory LoadSavedDuelDataFromDE */
/* --- factory SetBGP7OrSGB2ToCardPalette */
/* --- factory JPWriteByteToBGMap0 */
/* --- factory SetSGB3ToCardPalette */
/* >>> factory LookForCardIDInPlayArea_Bank5 */
static void adapt_LookForCardIDInPlayArea_Bank5(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	LookResult r = LookForCardIDInPlayArea_Bank5(de, s->b);
	s->a = r.a;
	s->b = r.b;
	s->f = r.f;
}
/* <<< factory LookForCardIDInPlayArea_Bank5 */
/* >>> factory CheckEnergyFlagsNeededInList */
static void adapt_CheckEnergyFlagsNeededInList(ProbeState *s)
{
	EnergyFlagsResult r = CheckEnergyFlagsNeededInList(s->a);
	s->a = r.a;
	s->c = r.c;
	s->f = r.carry ? 0x10u : 0u;
}
/* <<< factory CheckEnergyFlagsNeededInList */
/* --- factory PlaceCardImageOAM */
/* --- factory Func_6423 */
/* --- factory CreateCardAttrBlkPacket */
/* --- factory Func_14323 */
/* >>> factory LookForCardIDInHand */
static void adapt_LookForCardIDInHand(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CoreCardListResult r = LookForCardIDInHand(de);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInHand */
/* >>> factory LookForCardIDInHandList_Bank5 */
static void adapt_LookForCardIDInHandList_Bank5(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CoreCardListResult r = LookForCardIDInHandList_Bank5(de);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInHandList_Bank5 */
/* --- factory SetBGP6OrSGB3ToCardPalette */
/* --- factory SetOBP1OrSGB3ToCardPalette */
/* --- factory ResetDoFrameFunction_Bank1 */
/* --- factory Func_6ba2 */
/* --- factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */
/* >>> factory LookForCardIDInLocation_Bank5 */
static void adapt_LookForCardIDInLocation_Bank5(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	LookForCardIDInLocationResult r =
		LookForCardIDInLocation_Bank5(s->a, de);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory LookForCardIDInLocation_Bank5 */
/* >>> factory RemoveCardIDInList */
static void adapt_RemoveCardIDInList(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	RemoveCardIDResult r = RemoveCardIDInList(&s->hl, de);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory RemoveCardIDInList */
/* >>> factory ApplyCardCGBAttributes */
static void adapt_ApplyCardCGBAttributes(ProbeState *s)
{
	ApplyCardCGBAttributesResult r = ApplyCardCGBAttributes(s->a, (uint16_t)((uint16_t)s->d << 8 | s->e));
	s->b = r.b; s->c = r.c; s->d = (uint8_t)(r.de >> 8); s->e = (uint8_t)r.de; s->hl = r.hl;
}
/* <<< factory ApplyCardCGBAttributes */
/* >>> factory SetCardPalette */
static void adapt_SetCardPalette(ProbeState *s)
{
	SetCardPalette(s->a);
}
/* <<< factory SetCardPalette */
/* >>> factory SetBGP2ToCardPalette */
static void adapt_SetBGP2ToCardPalette(ProbeState *s)
{
	(void)s;
	SetBGP2ToCardPalette();
}
/* <<< factory SetBGP2ToCardPalette */
/* >>> factory SetBGP5ToCardPalette */
static void adapt_SetBGP5ToCardPalette(ProbeState *s)
{
	(void)s;
	SetBGP5ToCardPalette();
}
/* <<< factory SetBGP5ToCardPalette */
/* >>> factory WriteTwoByteNumberInTxSymbolFormat */
static void adapt_WriteTwoByteNumberInTxSymbolFormat(ProbeState *s)
{
	WriteTwoByteNumberInTxSymbolFormat(s->a, s->b, s->c);
}
/* <<< factory WriteTwoByteNumberInTxSymbolFormat */
/* >>> factory WriteTwoDigitNumberInTxSymbolFormat */
static void adapt_WriteTwoDigitNumberInTxSymbolFormat(ProbeState *s)
{
	WriteTwoDigitNumberInTxSymbolFormat(s->a, s->b, s->c);
}
/* <<< factory WriteTwoDigitNumberInTxSymbolFormat */
/* --- factory DecideLinkDuelVariables */
/* --- factory Func_1585b */
/* --- factory ValidateSavedNonLinkDuelData */
/* >>> factory AIAttachEnergyInHandToCardInPlayArea */
static void adapt_AIAttachEnergyInHandToCardInPlayArea(ProbeState *s)
{
	AIAttachEnergyInHandToCardInPlayAreaResult r = AIAttachEnergyInHandToCardInPlayArea(
		(uint16_t)(((uint16_t)s->b << 8) | s->c),
		(uint16_t)(((uint16_t)s->d << 8) | s->e));
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIAttachEnergyInHandToCardInPlayArea */
/* --- factory WriteTwoDigitNumberInTxSymbol_PadSpace */
/* >>> factory ConvertColorToEnergyCardID */
static void adapt_ConvertColorToEnergyCardID(ProbeState *s)
{
	ConvertColorResult result = ConvertColorToEnergyCardID(s->a);
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory ConvertColorToEnergyCardID */
/* --- factory WriteOneByteNumberInTxSymbol_PadSpace */
/* --- factory DrawOpponentSelectionScreen */
/* --- factory Func_15886 */
/* --- factory Func_7364 */
/* === factory PrintPlayAreaCardHeader */
/* >>> factory TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1 */
static void adapt_TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1(ProbeState *s)
{
	TwoByteNumberToTxSymbolTrimResult r = TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1 */
/* --- factory Func_616e */
/* --- factory FlushAllPalettesOrSendPal23Packet */
/* >>> factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
static void adapt_CheckForBenchIDAtHalfHPAndCanUseSecondAttack(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult r = CheckForBenchIDAtHalfHPAndCanUseSecondAttack(de, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
/* --- factory SendCardAttrBlkPacket */
/* --- factory ApplyBGP6OrSGB3ToCardImage */
/* --- factory ApplyBGP7OrSGB2ToCardImage */
/* --- factory Func_5a81 */
/* >>> factory OppAction_TossCoinATimes */
static void adapt_OppAction_TossCoinATimes(ProbeState *s)
{
	OppAction_TossCoinATimesResult result = OppAction_TossCoinATimes(
		s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a; s->f = result.f; s->b = result.b; s->c = result.c;
	s->d = result.d; s->e = result.e; s->hl = result.hl;
}
/* <<< factory OppAction_TossCoinATimes */
/* --- factory Func_5542 */
/* --- factory CanArenaCardUseNonResidualAttack */
/* === factory OpenNonTurnHolderDiscardPileScreen */
/* >>> factory CheckIfActivePokemonCanUseAnyNonResidualAttack */
static void adapt_CheckIfActivePokemonCanUseAnyNonResidualAttack(ProbeState *s)
{
	CheckIfActivePokemonCanUseAnyNonResidualAttackResult r =
		CheckIfActivePokemonCanUseAnyNonResidualAttack(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c;
	s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory CheckIfActivePokemonCanUseAnyNonResidualAttack */
/* >>> factory OppAction_UseMetronomeAttack */
static void adapt_OppAction_UseMetronomeAttack(ProbeState *s)
{
	OppAction_UseMetronomeAttack(s->b, s->c, s->d, s->e);
}
/* <<< factory OppAction_UseMetronomeAttack */
/* --- factory RequestToPrintCards_SelectStartCard */
/* --- factory StartDuel */
/* --- factory StartDuel_VSLinkOpp */
/* --- factory SetLinkDuelTransmissionFrameFunction */
/* --- factory UnreferencedDrawCardFromDeckToHand */
/* --- factory HandleWaitingLinkOpponentMenu */
/* --- factory _ContinueDuel */
/* --- factory DoLinkOpponentTurn */
/* >>> part probe_entries_core */
const ProbeEntry probe_entries_core[] = {
	{ "PrintDeckAndHandIconsAndNumberOfCards", adapt_PrintDeckAndHandIconsAndNumberOfCards },
	{ "ApplyCardCGBAttributes", adapt_ApplyCardCGBAttributes },
	{ "SetCardPalette", adapt_SetCardPalette },
	{ "SetBGP2ToCardPalette", adapt_SetBGP2ToCardPalette },
	{ "SetBGP5ToCardPalette", adapt_SetBGP5ToCardPalette },
	{ "WriteTwoByteNumberInTxSymbolFormat", adapt_WriteTwoByteNumberInTxSymbolFormat },
	{ "WriteTwoDigitNumberInTxSymbolFormat", adapt_WriteTwoDigitNumberInTxSymbolFormat },
	{ "CheckIfEnoughEnergiesToRetreat", adapt_CheckIfEnoughEnergiesToRetreat },
	{ "DisplayAttackPage", adapt_DisplayAttackPage },
	{ "DisplayCardPage", adapt_DisplayCardPage },
	{ "DoPracticeDuelAction", adapt_DoPracticeDuelAction },
	{ "DrawDuelHorizontalSeparator", adapt_DrawDuelHorizontalSeparator },
	{ "MoveAllTurnHolderKnockedOutPokemonToDiscardPile", adapt_MoveAllTurnHolderKnockedOutPokemonToDiscardPile },
	{ "PrintSortNumberInCardList_CallFromPointer", adapt_PrintSortNumberInCardList_CallFromPointer },
	{ "CheckIfEnoughEnergiesOfType", adapt_CheckIfEnoughEnergiesOfType },
	{ "CheckIfActiveCardParalyzedOrAsleep", adapt_CheckIfActiveCardParalyzedOrAsleep },
	{ "GetAttacksEnergyCostBits", adapt_GetAttacksEnergyCostBits },
	{ "CheckForEvolutionInList", adapt_CheckForEvolutionInList },
	{ "CountNumberOfEnergyCardsAttached", adapt_CountNumberOfEnergyCardsAttached },
	{ "LookForCardIDInLocation_Bank5", adapt_LookForCardIDInLocation_Bank5 },
	{ "PrintCardNameFromCardIDInTextBox", adapt_PrintCardNameFromCardIDInTextBox },
	{ "RemoveCardIDInList", adapt_RemoveCardIDInList },
	{ "SortTempHandByIDList", adapt_SortTempHandByIDList },
	{ "HandleFailedToContinueDuel", adapt_HandleFailedToContinueDuel },
	{ "SetLineSeparation", adapt_SetLineSeparation },
	{ "PlayAreaScreenMenuFunction", adapt_PlayAreaScreenMenuFunction },
	{ "SwitchAttackPage", adapt_SwitchAttackPage },
	{ "PrintCardListHeaderAndInfoBoxTexts", adapt_PrintCardListHeaderAndInfoBoxTexts },
	{ "DrawHPBar", adapt_DrawHPBar },
	{ "ValidateSavedDuelData", adapt_ValidateSavedDuelData },
	{ "LoadSavedDuelData", adapt_LoadSavedDuelData },
	{ "DiscardSavedDuelData", adapt_DiscardSavedDuelData },
	{ "SaveDuelDataToDE", adapt_SaveDuelDataToDE },
	{ "ZeroObjectPositionsAndToggleOAMCopy", adapt_ZeroObjectPositionsAndToggleOAMCopy },
	{ "LoadPlayerDeck", adapt_LoadPlayerDeck },
	{ "CheckSkipDelayAllowed", adapt_CheckSkipDelayAllowed },
	{ "AIMakeDecision", adapt_AIMakeDecision },
	{ "PrintPracticeDuelDrMasonInstructions", adapt_PrintPracticeDuelDrMasonInstructions },
	{ "PrintPracticeDuelInstructionsTextBoxLabel", adapt_PrintPracticeDuelInstructionsTextBoxLabel },
	{ "LookForCardIDInPlayArea_Bank5", adapt_LookForCardIDInPlayArea_Bank5 },
	{ "ClearMemory_Bank5", adapt_ClearMemory_Bank5 },
	{ "SetCardListInfoBoxText", adapt_SetCardListInfoBoxText },
	{ "ReturnWrongAction", adapt_ReturnWrongAction },
	{ "CopyListWithFFTerminatorFromHLToDE_Bank5", adapt_CopyListWithFFTerminatorFromHLToDE_Bank5 },
	{ "CheckEnergyFlagsNeededInList", adapt_CheckEnergyFlagsNeededInList },
	{ "CardPageSwitch_EnergyEnd", adapt_CardPageSwitch_EnergyEnd },
	{ "CardPageSwitch_0c", adapt_CardPageSwitch_0c },
	{ "PrintPlayAreaCardAttachedEnergies", adapt_PrintPlayAreaCardAttachedEnergies },
	{ "OppAction_DrawCard", adapt_OppAction_DrawCard },
	{ "PrintSortNumberInCardList_SetPointer", adapt_PrintSortNumberInCardList_SetPointer },
	{ "PrintSortNumberInCardList", adapt_PrintSortNumberInCardList },
	{ "PrintEnergiesOfColor", adapt_PrintEnergiesOfColor },
	{ "PrintCardPageWeaknessesOrResistances", adapt_PrintCardPageWeaknessesOrResistances },
	{ "InitVariablesToBeginDuel", adapt_InitVariablesToBeginDuel },
	{ "CardPageSwitch_PokemonAttack1Page2", adapt_CardPageSwitch_PokemonAttack1Page2 },
	{ "CardPageSwitch_PokemonAttack2Page1", adapt_CardPageSwitch_PokemonAttack2Page1 },
	{ "AIDiscourage", adapt_AIDiscourage },
	{ "ConvertHPToDamageCounters_Bank5", adapt_ConvertHPToDamageCounters_Bank5 },
	{ "CalculateBDividedByA_Bank5", adapt_CalculateBDividedByA_Bank5 },
	{ "AIPlayInitialBasicCards", adapt_AIPlayInitialBasicCards },
	{ "CheckIfEnoughParticularAttachedEnergy", adapt_CheckIfEnoughParticularAttachedEnergy },
	{ "CreateEnergyCardListFromHand", adapt_CreateEnergyCardListFromHand },
	{ "CalculateParticularAttachedEnergyNeeded", adapt_CalculateParticularAttachedEnergyNeeded },
	{ "GetAnimCoordsAndFlags", adapt_GetAnimCoordsAndFlags },
	{ "PlayBufferedDuelAnimations", adapt_PlayBufferedDuelAnimations },
	{ "GetDamageNumberChars.ConvertDigitToCharTile", adapt_GetDamageNumberChars_ConvertDigitToCharTile },
	{ "SwitchCardPage", adapt_SwitchCardPage },
	{ "CardPageSwitch_00", adapt_CardPageSwitch_00 },
	{ "LoadLoaded1CardGfx", adapt_LoadLoaded1CardGfx },
	{ "CheckForEvolutionInDeck", adapt_CheckForEvolutionInDeck },
	{ "LookForCardThatIsKnockedOutOnDevolution", adapt_LookForCardThatIsKnockedOutOnDevolution },
	{ "CheckCardEvolutionInHandOrDeck", adapt_CheckCardEvolutionInHandOrDeck },
	{ "CheckIfOpponentHasBossDeckID", adapt_CheckIfOpponentHasBossDeckID },
	{ "RaiseAIScoreToAllMatchingIDsInBench", adapt_RaiseAIScoreToAllMatchingIDsInBench },
	{ "GetAnimationData", adapt_GetAnimationData },
	{ "GetDamageNumberChars", adapt_GetDamageNumberChars },
	{ "CardPageSwitch_PokemonOverviewOrDescription", adapt_CardPageSwitch_PokemonOverviewOrDescription },
	{ "CheckCardPageExists", adapt_CheckCardPageExists },
	{ "CardPageSwitch_PokemonEnd", adapt_CardPageSwitch_PokemonEnd },
	{ "CardPageSwitch_PokemonAttack2Page2", adapt_CardPageSwitch_PokemonAttack2Page2 },
	{ "CardPageSwitch_08", adapt_CardPageSwitch_08 },
	{ "LoadPlayAreaCardGfx", adapt_LoadPlayAreaCardGfx },
	{ "PrintCardPageRarityIcon", adapt_PrintCardPageRarityIcon },
	{ "SetNoLineSeparation", adapt_SetNoLineSeparation },
	{ "SetOneLineSeparation", adapt_SetOneLineSeparation },
	{ "_HasAlivePokemonInPlayArea", adapt__HasAlivePokemonInPlayArea },
	{ "CheckPrintPoisoned", adapt_CheckPrintPoisoned },
	{ "OppAction_NoAction", adapt_OppAction_NoAction },
	{ "LookForCardIDInHand", adapt_LookForCardIDInHand },
	{ "LookForCardIDInHandList_Bank5", adapt_LookForCardIDInHandList_Bank5 },
	{ "FindHighestBenchScore", adapt_FindHighestBenchScore },
	{ "AIEncourage", adapt_AIEncourage },
	{ "IsLoadedCard1BasicPokemon", adapt_IsLoadedCard1BasicPokemon },
	{ "PracticeDuel_PlayGoldeen", adapt_PracticeDuel_PlayGoldeen },
	{ "DiscardRetreatCostCards", adapt_DiscardRetreatCostCards },
	{ "ReturnRetreatCostCardsToArena", adapt_ReturnRetreatCostCardsToArena },
	{ "LoadCardNameToTxRam2", adapt_LoadCardNameToTxRam2 },
	{ "DrawWideTextBox_WaitForInput_Bank1", adapt_DrawWideTextBox_WaitForInput_Bank1 },
	{ "LoadDefendingPokemonColorWRAndPrizeCards", adapt_LoadDefendingPokemonColorWRAndPrizeCards },
	{ "CheckIfEnergyIsUseful", adapt_CheckIfEnergyIsUseful },
	{ "PickRandomBenchPokemon", adapt_PickRandomBenchPokemon },
	{ "PracticeDuel_VerifyInitialPlay", adapt_PracticeDuel_VerifyInitialPlay },
	{ "PracticeDuel_VerifyPlayerTurnActions", adapt_PracticeDuel_VerifyPlayerTurnActions },
	{ "CheckIfNoSurplusEnergyForAttack", adapt_CheckIfNoSurplusEnergyForAttack },
	{ "LoadCardNameToTxRam2_b", adapt_LoadCardNameToTxRam2_b },
	{ "ApplyStatusConditionToArenaPokemon", adapt_ApplyStatusConditionToArenaPokemon },
	{ "CheckIfNotABossDeckID", adapt_CheckIfNotABossDeckID },
	{ "AIChooseRandomlyNotToDoAction", adapt_AIChooseRandomlyNotToDoAction },
	{ "TrySetUpBossStartingPlayArea", adapt_TrySetUpBossStartingPlayArea },
	{ "CardPageSwitch_TrainerEnd", adapt_CardPageSwitch_TrainerEnd },
	{ "CardPageSwitch_TrainerPage2", adapt_CardPageSwitch_TrainerPage2 },
	{ "CardPageSwitch_EnergyOrTrainerPage1", adapt_CardPageSwitch_EnergyOrTrainerPage1 },
	{ "LoadAndValidateDuelSaveData", adapt_LoadAndValidateDuelSaveData },
	{ "PrintPlayAreaCardLocation", adapt_PrintPlayAreaCardLocation },
	{ "SetupPlayAreaScreen", adapt_SetupPlayAreaScreen },
	{ "CheckIfEnoughEnergiesForGivenAttack", adapt_CheckIfEnoughEnergiesForGivenAttack },
	{ "SaveDuelData", adapt_SaveDuelData },
	{ "SetCardListHeaderText", adapt_SetCardListHeaderText },
	{ "AIAttachEnergyInHandToCardInPlayArea", adapt_AIAttachEnergyInHandToCardInPlayArea },
	{ "GoToPreviousCardPage", adapt_GoToPreviousCardPage },
	{ "DrawWholeScreenTextBox", adapt_DrawWholeScreenTextBox },
	{ "HasAlivePokemonInPlayArea", adapt_HasAlivePokemonInPlayArea },
	{ "CardPageSwitch_PokemonAttack1Page1", adapt_CardPageSwitch_PokemonAttack1Page1 },
	{ "CheckPrintDoublePoisoned", adapt_CheckPrintDoublePoisoned },
	{ "PrintPracticeDuelLetsPlayTheGame", adapt_PrintPracticeDuelLetsPlayTheGame },
	{ "AIAttachEnergyInHandToCardInBench", adapt_AIAttachEnergyInHandToCardInBench },
	{ "DrawPracticeDuelInstructionsTextBox", adapt_DrawPracticeDuelInstructionsTextBox },
	{ "PracticeDuelVerify_Turn7Or8", adapt_PracticeDuelVerify_Turn7Or8 },
	{ "HandleDuelSetup", adapt_HandleDuelSetup },
	{ "SetDiscardPileScreenTexts", adapt_SetDiscardPileScreenTexts },
	{ "PrintAttachedEnergyToPokemon", adapt_PrintAttachedEnergyToPokemon },
	{ "PrintPokemonEvolvedIntoPokemon", adapt_PrintPokemonEvolvedIntoPokemon },
	{ "SetupDuel", adapt_SetupDuel },
	{ "PracticeDuelVerify_Turn6", adapt_PracticeDuelVerify_Turn6 },
	{ "PracticeDuelVerify_Turn4", adapt_PracticeDuelVerify_Turn4 },
	{ "ShuffleDeckAndDrawSevenCards", adapt_ShuffleDeckAndDrawSevenCards },
	{ "PrintOpponentNumberOfHandAndDeckCards", adapt_PrintOpponentNumberOfHandAndDeckCards },
	{ "PrintPlayerNumberOfHandAndDeckCards", adapt_PrintPlayerNumberOfHandAndDeckCards },
	{ "PrintDuelResultStats", adapt_PrintDuelResultStats },
	{ "ConvertColorToEnergyCardID", adapt_ConvertColorToEnergyCardID },
	{ "PrintPracticeDuelNumberedInstruction", adapt_PrintPracticeDuelNumberedInstruction },
	{ "PrintNextPracticeDuelInstruction", adapt_PrintNextPracticeDuelInstruction },
	{ "GoToFirstOrNextCardPage", adapt_GoToFirstOrNextCardPage },
	{ "PrintPracticeDuelInstructions", adapt_PrintPracticeDuelInstructions },
	{ "DisplayPreviousCardPage", adapt_DisplayPreviousCardPage },
	{ "PrintNumberOfHandAndDeckCards", adapt_PrintNumberOfHandAndDeckCards },
	{ "PrintReturnCardsToDeckDrawAgain", adapt_PrintReturnCardsToDeckDrawAgain },
	{ "PracticeDuelVerify_Turn3", adapt_PracticeDuelVerify_Turn3 },
	{ "CheckIfEnoughEnergiesToAttack", adapt_CheckIfEnoughEnergiesToAttack },
	{ "PlayTurnDuelistDrawAnimation", adapt_PlayTurnDuelistDrawAnimation },
	{ "DrawCardPageSet2AndRarityIcons", adapt_DrawCardPageSet2AndRarityIcons },
	{ "CountOppEnergyCardsInHandAndAttached", adapt_CountOppEnergyCardsInHandAndAttached },
	{ "AIPickPrizeCards", adapt_AIPickPrizeCards },
	{ "HandleAIEnergyScoringForRepeatedBenchPokemon", adapt_HandleAIEnergyScoringForRepeatedBenchPokemon },
	{ "CheckPrintCnfSlpPrz", adapt_CheckPrintCnfSlpPrz },
	{ "LoadAnimCoordsAndFlags", adapt_LoadAnimCoordsAndFlags },
	{ "PrintUsedTrainerCardDescription", adapt_PrintUsedTrainerCardDescription },
	{ "PracticeDuelVerify_Turn5", adapt_PracticeDuelVerify_Turn5 },
	{ "PracticeDuelVerify_Turn1", adapt_PracticeDuelVerify_Turn1 },
	{ "PracticeDuelVerify_Turn2", adapt_PracticeDuelVerify_Turn2 },
	{ "PracticeDuel_PlayStaryuFromBench", adapt_PracticeDuel_PlayStaryuFromBench },
	{ "DisplayDuelistTurnScreen", adapt_DisplayDuelistTurnScreen },
	{ "DrawDuelistPortraitsAndNames", adapt_DrawDuelistPortraitsAndNames },
	{ "CheckEnergyNeededForAttack", adapt_CheckEnergyNeededForAttack },
	{ "CreateDamageCharSprite", adapt_CreateDamageCharSprite },
	{ "HasAlivePokemonInBench", adapt_HasAlivePokemonInBench },
	{ "PracticeDuel_ReplaceKnockedOutPokemon", adapt_PracticeDuel_ReplaceKnockedOutPokemon },
	{ "DrawDamageAnimationArrow", adapt_DrawDamageAnimationArrow },
	{ "DrawDamageAnimationWeak", adapt_DrawDamageAnimationWeak },
	{ "DrawDamageAnimationResist", adapt_DrawDamageAnimationResist },
	{ "DrawDamageAnimationNumbers", adapt_DrawDamageAnimationNumbers },
	{ "CheckAbleToRetreat", adapt_CheckAbleToRetreat },
	{ "LookForEnergyNeededInHand", adapt_LookForEnergyNeededInHand },
	{ "CheckEnergyNeededForAttackAfterDiscard", adapt_CheckEnergyNeededForAttackAfterDiscard },
	{ "DisplayFirstOrNextCardPage", adapt_DisplayFirstOrNextCardPage },
	{ "PrintAttackOrCardDescription", adapt_PrintAttackOrCardDescription },
	{ "PrintAttackOrPkmnPowerInformation", adapt_PrintAttackOrPkmnPowerInformation },
	{ "PrintAttackOrNonPokemonCardDescription", adapt_PrintAttackOrNonPokemonCardDescription },
	{ "DisplayCardPageOnLeftOrRightPressed", adapt_DisplayCardPageOnLeftOrRightPressed },
	{ "PrintPlayAreaCardHeader", adapt_PrintPlayAreaCardHeader },
	{ "PrintPokemonCardLength", adapt_PrintPokemonCardLength },
	{ "TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1", adapt_TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1 },
	{ "PlayDeckShuffleAnimation", adapt_PlayDeckShuffleAnimation },
	{ "OppAction_6b30", adapt_OppAction_6b30 },
	{ "PrintPlayAreaCardInformation", adapt_PrintPlayAreaCardInformation },
	{ "PrintPlayAreaCardInformationAndLocation", adapt_PrintPlayAreaCardInformationAndLocation },
	{ "DisplayUsePokemonPowerScreen", adapt_DisplayUsePokemonPowerScreen },
	{ "InitAndPrintPlayAreaCardInformationAndLocation", adapt_InitAndPrintPlayAreaCardInformationAndLocation },
	{ "InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox", adapt_InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox },
	{ "PrintPlayAreaCardList", adapt_PrintPlayAreaCardList },
	{ "OppAction_UsePokemonPower", adapt_OppAction_UsePokemonPower },
	{ "PrintPlayAreaCardList_EnableLCD", adapt_PrintPlayAreaCardList_EnableLCD },
	{ "CheckIfCardCanBePlayed", adapt_CheckIfCardCanBePlayed },
	{ "OppAction_6b15", adapt_OppAction_6b15 },
	{ "OppAction_ExecutePokemonPowerEffect", adapt_OppAction_ExecutePokemonPowerEffect },
	{ "LoadSelectedCardGfx", adapt_LoadSelectedCardGfx },
	{ "AIProcessHandTrainerCards", adapt_AIProcessHandTrainerCards },
	{ "CardListFunction", adapt_CardListFunction },
	{ "CheckIfSelectedAttackIsUnusable", adapt_CheckIfSelectedAttackIsUnusable },
	{ "CheckForBenchIDAtHalfHPAndCanUseSecondAttack", adapt_CheckForBenchIDAtHalfHPAndCanUseSecondAttack },
	{ "CountNumberOfSetUpBenchPokemon", adapt_CountNumberOfSetUpBenchPokemon },
	{ "HandleLegendaryArticunoEnergyScoring", adapt_HandleLegendaryArticunoEnergyScoring },
	{ "CheckIfArenaCardIsFullyPowered", adapt_CheckIfArenaCardIsFullyPowered },
	{ "DrawLargePictureOfCard", adapt_DrawLargePictureOfCard },
	{ "DrawCardPageSurroundingBox", adapt_DrawCardPageSurroundingBox },
	{ "PrintPokemonCardPageGenericInformation", adapt_PrintPokemonCardPageGenericInformation },
	{ "DrawDuelHUD", adapt_DrawDuelHUD },
	{ "DrawDuelHUDs", adapt_DrawDuelHUDs },
	{ "DrawCardListScreenLayout", adapt_DrawCardListScreenLayout },
	{ "DisplayPracticeDuelPlayerHandScreen", adapt_DisplayPracticeDuelPlayerHandScreen },
	{ "DrawDuelMainScene", adapt_DrawDuelMainScene },
	{ "InitAndDrawCardListScreenLayout", adapt_InitAndDrawCardListScreenLayout },
	{ "RedrawTurnDuelistsDuelHUD", adapt_RedrawTurnDuelistsDuelHUD },
	{ "OppAction_DrawDuelMainScene", adapt_OppAction_DrawDuelMainScene },
	{ "InitAndDrawCardListScreenLayout_WithSelectCheckMenu", adapt_InitAndDrawCardListScreenLayout_WithSelectCheckMenu },
	{ "DisplayCardListDetails", adapt_DisplayCardListDetails },
	{ "OppAction_FinishTurnWithoutAttacking", adapt_OppAction_FinishTurnWithoutAttacking },
	{ "RedrawTurnDuelistsMainSceneOrDuelHUD", adapt_RedrawTurnDuelistsMainSceneOrDuelHUD },
	{ "DisplayNoBasicPokemonInHandScreen", adapt_DisplayNoBasicPokemonInHandScreen },
	{ "PrintAndLoadAttacksToDuelTempList", adapt_PrintAndLoadAttacksToDuelTempList },
	{ "DisplayPokemonAttackCardPage", adapt_DisplayPokemonAttackCardPage },
	{ "DisplayCardPage_PokemonAttack2Page2", adapt_DisplayCardPage_PokemonAttack2Page2 },
	{ "DisplayCardPage_PokemonAttack1Page1", adapt_DisplayCardPage_PokemonAttack1Page1 },
	{ "DisplayCardPage_PokemonAttack1Page2", adapt_DisplayCardPage_PokemonAttack1Page2 },
	{ "DisplayCardPage_PokemonAttack2Page1", adapt_DisplayCardPage_PokemonAttack2Page1 },
	{ "DisplayAttackPage_Attack1Page1", adapt_DisplayAttackPage_Attack1Page1 },
	{ "DisplayAttackPage_Attack2Page1", adapt_DisplayAttackPage_Attack2Page1 },
	{ "DisplayAttackPage_Attack2Page2", adapt_DisplayAttackPage_Attack2Page2 },
	{ "DisplayAttackPage_Attack1Page2", adapt_DisplayAttackPage_Attack1Page2 },
	{ "DisplayEnergyDiscardMenu", adapt_DisplayEnergyDiscardMenu },
	{ "DisplayEnergyDiscardScreen", adapt_DisplayEnergyDiscardScreen },
	{ "OpenAttackPage", adapt_OpenAttackPage },
	{ "HandleEnergyDiscardMenuInput", adapt_HandleEnergyDiscardMenuInput },
	{ "DisplayRetreatScreen", adapt_DisplayRetreatScreen },
	{ "PrintPracticeDuelInstructions_Fast", adapt_PrintPracticeDuelInstructions_Fast },
	{ "_DisplayCardDetailScreen", adapt__DisplayCardDetailScreen },
	{ "OpenCardPage", adapt_OpenCardPage },
	{ "OpenCardPage.input_loop", adapt_OpenCardPage_input_loop },
	{ "PracticeDuel_RepeatInstructions", adapt_PracticeDuel_RepeatInstructions },
	{ "DisplayCardDetailScreen", adapt_DisplayCardDetailScreen },
	{ "OpenCardPage_FromHand", adapt_OpenCardPage_FromHand },
	{ "OpenCardPage_FromCheckPlayArea", adapt_OpenCardPage_FromCheckPlayArea },
	{ "DisplayUsedTrainerCardDetailScreen", adapt_DisplayUsedTrainerCardDetailScreen },
	{ "DisplayNoBasicPokemonInHandScreenAndText", adapt_DisplayNoBasicPokemonInHandScreenAndText },
	{ "OpenCardPage_FromCheckHandOrDiscardPile", adapt_OpenCardPage_FromCheckHandOrDiscardPile },
	{ "CardListItemSelectionMenu", adapt_CardListItemSelectionMenu },
	{ "DisplayPlayerDrawCardScreen", adapt_DisplayPlayerDrawCardScreen },
	{ "OppAction_PlayTrainerCard", adapt_OppAction_PlayTrainerCard },
	{ "OpenActivePokemonScreen", adapt_OpenActivePokemonScreen },
	{ "DisplayPlayAreaScreenToUsePkmnPower", adapt_DisplayPlayAreaScreenToUsePkmnPower },
	{ "DisplayCardPage_PokemonOverview", adapt_DisplayCardPage_PokemonOverview },
	{ "DisplayEnergyOrTrainerCardPage", adapt_DisplayEnergyOrTrainerCardPage },
	{ "DisplayCardPage_Energy", adapt_DisplayCardPage_Energy },
	{ "DisplayCardPage_TrainerPage2", adapt_DisplayCardPage_TrainerPage2 },
	{ "DisplayCardPage_TrainerPage1", adapt_DisplayCardPage_TrainerPage1 },
	{ "PrintPracticeDuelInstructionsForCurrentTurn", adapt_PrintPracticeDuelInstructionsForCurrentTurn },
	{ "PracticeDuel_PrintTurnInstructions", adapt_PracticeDuel_PrintTurnInstructions },
	{ "_TossCoin", adapt__TossCoin },
	{ "AttemptRetreat", adapt_AttemptRetreat },
	{ "OppAction_BeginUseAttack", adapt_OppAction_BeginUseAttack },
	{ "OppAction_TossCoinATimes", adapt_OppAction_TossCoinATimes },
	{ "OppAction_AttemptRetreat", adapt_OppAction_AttemptRetreat },
	{ "PlayAttackAnimation", adapt_PlayAttackAnimation },
	{ "PlayStatusConditionQueueAnimations", adapt_PlayStatusConditionQueueAnimations },
	{ "PlayAttackAnimation_DealAttackDamageSimple", adapt_PlayAttackAnimation_DealAttackDamageSimple },
	{ "DisplayOpponentUsedAttackScreen", adapt_DisplayOpponentUsedAttackScreen },
	{ "DisplayCardList", adapt_DisplayCardList },
	{ "CheckIfCanDamageDefendingPokemon", adapt_CheckIfCanDamageDefendingPokemon },
	{ "OpenDiscardPileScreen", adapt_OpenDiscardPileScreen },
	{ "OpenTurnHolderHandScreen_Simple", adapt_OpenTurnHolderHandScreen_Simple },
	{ "OpenTurnHolderDiscardPileScreen", adapt_OpenTurnHolderDiscardPileScreen },
	{ "OpenNonTurnHolderDiscardPileScreen", adapt_OpenNonTurnHolderDiscardPileScreen },
	{ "CheckIfActivePokemonCanUseAnyNonResidualAttack", adapt_CheckIfActivePokemonCanUseAnyNonResidualAttack },
	{ "OpenNonTurnHolderHandScreen_Simple", adapt_OpenNonTurnHolderHandScreen_Simple },
	{ "DisplayPlaceInitialPokemonCardsScreen", adapt_DisplayPlaceInitialPokemonCardsScreen },
	{ "CheckDamageToMrMime", adapt_CheckDamageToMrMime },
	{ "DisplayDrawNCardsScreen", adapt_DisplayDrawNCardsScreen },
	{ "PlayShuffleAndDrawCardsAnimation", adapt_PlayShuffleAndDrawCardsAnimation },
	{ "DisplayDrawOneCardScreen", adapt_DisplayDrawOneCardScreen },
 	{ "PlayShuffleAndDrawCardsAnimation_TurnDuelist", adapt_PlayShuffleAndDrawCardsAnimation_TurnDuelist },
	{ "OppAction_ExecuteTrainerCardEffectCommands", adapt_OppAction_ExecuteTrainerCardEffectCommands },
	{ "OppAction_UseMetronomeAttack", adapt_OppAction_UseMetronomeAttack },
	{ "LookForEnergyNeededForAttackInHand", adapt_LookForEnergyNeededForAttackInHand },
	{ "PlayShuffleAndDrawCardsAnimation_BothDuelists", adapt_PlayShuffleAndDrawCardsAnimation_BothDuelists },
	{ "CheckIfDefendingPokemonCanKnockOut", adapt_CheckIfDefendingPokemonCanKnockOut },
	{ "CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHP", adapt_CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHP },
	{ "CheckIfAnyAttackKnocksOutDefendingCard", adapt_CheckIfAnyAttackKnocksOutDefendingCard },
	{ "CheckIfActiveCardCanKnockOut", adapt_CheckIfActiveCardCanKnockOut },
	{ "AISelectSpecialAttackParameters", adapt_AISelectSpecialAttackParameters },
	{ "OppAction_EvolvePokemonCard", adapt_OppAction_EvolvePokemonCard },
	{ "OppAction_PlayBasicPokemonCard", adapt_OppAction_PlayBasicPokemonCard },
	{ "OppAction_PlayEnergyCard", adapt_OppAction_PlayEnergyCard },
	{ "AITryUseAttack", adapt_AITryUseAttack },
	{ "PrintPokemonCardWeight", adapt_PrintPokemonCardWeight },
	{ "DisplayCardPage_PokemonDescription", adapt_DisplayCardPage_PokemonDescription },
	{ "PlayBetweenTurnsAnimation", adapt_PlayBetweenTurnsAnimation },
	{ "HandleSleepCheck", adapt_HandleSleepCheck },
	{ "HandlePoisonDamage", adapt_HandlePoisonDamage },
	{ "PracticeDuel_DrawSevenCards", adapt_PracticeDuel_DrawSevenCards },
	{ "PracticeDuel_DonePuttingOnBench", adapt_PracticeDuel_DonePuttingOnBench },
	{ "PracticeDuel_PutStaryuInBench", adapt_PracticeDuel_PutStaryuInBench },
	{ "ChooseInitialArenaAndBenchPokemon", adapt_ChooseInitialArenaAndBenchPokemon },
	{ "TurnDuelistTakePrizes", adapt_TurnDuelistTakePrizes },
	{ "Func_6fa5", adapt_Func_6fa5 },
	{ "Func_1cb5e", adapt_Func_1cb5e },
	{ "StartDuel_VSAIOpp", adapt_StartDuel_VSAIOpp },
	{ "OpenNonTurnHolderPlayAreaScreen", adapt_OpenNonTurnHolderPlayAreaScreen },
	{ "OpenTurnHolderPlayAreaScreen", adapt_OpenTurnHolderPlayAreaScreen },
	{ "OpenVariousPlayAreaScreens_FromSelectPresses", adapt_OpenVariousPlayAreaScreens_FromSelectPresses },
	{ "OpenPlayAreaScreenForViewing", adapt_OpenPlayAreaScreenForViewing },
	{ "OpenPlayAreaScreenForSelection", adapt_OpenPlayAreaScreenForSelection },
	{ "DisplayPlayAreaScreen", adapt_DisplayPlayAreaScreen },
	{ "SelectingBenchPokemonMenu", adapt_SelectingBenchPokemonMenu },
	{ "HandleSpecialDuelMainSceneHotkeys", adapt_HandleSpecialDuelMainSceneHotkeys },
	{ "ReplaceKnockedOutPokemon", adapt_ReplaceKnockedOutPokemon },
	{ "HandleBetweenTurnKnockOuts", adapt_HandleBetweenTurnKnockOuts },
	{ "HandleDestinyBondAndBetweenTurnKnockOuts", adapt_HandleDestinyBondAndBetweenTurnKnockOuts },
	{ "RestartPracticeDuelTurn", adapt_RestartPracticeDuelTurn },
	{ "DuelMainInterface", adapt_DuelMainInterface },
	{ "PrintDuelMenuAndHandleInput", adapt_PrintDuelMenuAndHandleInput },
	{ "DuelMenuShortcut_OpponentPlayArea", adapt_DuelMenuShortcut_OpponentPlayArea },
	{ "DuelMenuShortcut_PlayerPlayArea", adapt_DuelMenuShortcut_PlayerPlayArea },
	{ "DuelMenuShortcut_OpponentDiscardPile", adapt_DuelMenuShortcut_OpponentDiscardPile },
	{ "DuelMenuShortcut_PlayerDiscardPile", adapt_DuelMenuShortcut_PlayerDiscardPile },
	{ "DuelMenuShortcut_OpponentActivePokemon", adapt_DuelMenuShortcut_OpponentActivePokemon },
	{ "DuelMenuShortcut_PlayerActivePokemon", adapt_DuelMenuShortcut_PlayerActivePokemon },
	{ "DuelMenu_PkmnPower", adapt_DuelMenu_PkmnPower },
	{ "DuelMenu_Done", adapt_DuelMenu_Done },
	{ "DuelMenu_Retreat", adapt_DuelMenu_Retreat },
	{ "DuelMenu_Hand", adapt_DuelMenu_Hand },
	{ "OpenPlayerHandScreen", adapt_OpenPlayerHandScreen },
	{ "PlayEnergyCard", adapt_PlayEnergyCard },
	{ "ReloadCardListScreen", adapt_ReloadCardListScreen },
	{ "DuelMenu_Check", adapt_DuelMenu_Check },
	{ "DuelMenuShortcut_BothActivePokemon", adapt_DuelMenuShortcut_BothActivePokemon },
	{ "DuelMenu_Attack", adapt_DuelMenu_Attack },
	{ "OppAction_ForceSwitchActive", adapt_OppAction_ForceSwitchActive },
	{ "OppAction_UseAttack", adapt_OppAction_UseAttack },
	{ "HandleTurn", adapt_HandleTurn },
	{ "HandleBetweenTurnsEvents", adapt_HandleBetweenTurnsEvents },
	{ "OppAction_PlayAttackAnimationDealAttackDamage", adapt_OppAction_PlayAttackAnimationDealAttackDamage },
	{ "MainDuelLoop", adapt_MainDuelLoop },
	{ "TryContinueDuel", adapt_TryContinueDuel },
	{ "PlayPokemonCard", adapt_PlayPokemonCard },
	{ NULL, NULL },
};
/* <<< part probe_entries_core */
