/* --- factory GetScriptArgs5AfterPointer */
/* >>> factory ScriptCommand_JumpIfCardInCollection */
static void adapt_ScriptCommand_JumpIfCardInCollection(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfCardInCollection(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfCardInCollection */
/* >>> factory ScriptCommand_GiveCard */
static void adapt_ScriptCommand_GiveCard(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_GiveCard(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_GiveCard */
/* >>> factory ScriptCommand_TakeCard */
static void adapt_ScriptCommand_TakeCard(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_TakeCard(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_TakeCard */
/* >>> factory ScriptCommand_SetSpriteAttributes */
static void adapt_ScriptCommand_SetSpriteAttributes(ProbeState *s)
{
	SetSpriteAttributesResult r = ScriptCommand_SetSpriteAttributes(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetSpriteAttributes */
/* --- factory ScriptCommand_BattleCenter */
/* >>> factory SetNextScript */
static void adapt_SetNextScript(ProbeState *s)
{
	s->hl = SetNextScript(s->a, (uint16_t)(((uint16_t)s->b << 8) | s->c));
}
/* <<< factory SetNextScript */
/* >>> factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
static void adapt_ScriptCommand_RemoveAllEnergyCardsFromCollection(ProbeState *s)
{
	ScriptCommand_RemoveAllEnergyCardsResult r =
		ScriptCommand_RemoveAllEnergyCardsFromCollection(s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
/* >>> factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
static void adapt_ScriptCommand_JumpIfAnyEnergyCardsInCollection(ProbeState *s)
{
	ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult r =
		ScriptCommand_JumpIfAnyEnergyCardsInCollection();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
/* >>> factory ScriptCommand_JumpIfCardOwned */
static void adapt_ScriptCommand_JumpIfCardOwned(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfCardOwned(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfCardOwned */
/* --- factory Func_c998 */
/* --- factory ScriptCommand_GiftCenter */
/* >>> factory ScriptCommand_ShowCardReceivedScreen */
static void adapt_ScriptCommand_ShowCardReceivedScreen(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_ShowCardReceivedScreen(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_ShowCardReceivedScreen */
/* --- factory Script_GiftCenterClerk */
/* >>> factory ScriptCommand_JumpIfMan1RequestedCardOwned */
static void adapt_ScriptCommand_JumpIfMan1RequestedCardOwned(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfMan1RequestedCardOwned(s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfMan1RequestedCardOwned */
/* >>> factory ScriptCommand_JumpIfMan1RequestedCardInCollection */
static void adapt_ScriptCommand_JumpIfMan1RequestedCardInCollection(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfMan1RequestedCardInCollection(s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfMan1RequestedCardInCollection */
/* >>> part probe_entries_scripting */
const ProbeEntry probe_entries_scripting[] = {
	{ "Func_c9bc", adapt_Func_c9bc },
	{ "CallMapScriptPointerIfExists", adapt_CallMapScriptPointerIfExists },
	{ "IncreaseScriptPointer", adapt_IncreaseScriptPointer },
	{ "SetScriptPointer", adapt_SetScriptPointer },
	{ "GetScriptArgsAfterPointer", adapt_GetScriptArgsAfterPointer },
	{ "GetEventVar", adapt_GetEventVar },
	{ "IncreaseScriptPointerBy1", adapt_IncreaseScriptPointerBy1 },
	{ "IncreaseScriptPointerBy2", adapt_IncreaseScriptPointerBy2 },
	{ "IncreaseScriptPointerBy4", adapt_IncreaseScriptPointerBy4 },
	{ "IncreaseScriptPointerBy3", adapt_IncreaseScriptPointerBy3 },
	{ "SetScriptControlByteFail", adapt_SetScriptControlByteFail },
	{ "IncreaseScriptPointerBy5", adapt_IncreaseScriptPointerBy5 },
	{ "IncreaseScriptPointerBy6", adapt_IncreaseScriptPointerBy6 },
	{ "IncreaseScriptPointerBy7", adapt_IncreaseScriptPointerBy7 },
	{ "GetScriptArgs2AfterPointer", adapt_GetScriptArgs2AfterPointer },
	{ "GetScriptArgs3AfterPointer", adapt_GetScriptArgs3AfterPointer },
	{ "SetScriptControlBytePass", adapt_SetScriptControlBytePass },
	{ "ScriptCommand_JumpIfCardInCollection", adapt_ScriptCommand_JumpIfCardInCollection },
	{ "ScriptCommand_GiveCard", adapt_ScriptCommand_GiveCard },
	{ "ScriptCommand_TakeCard", adapt_ScriptCommand_TakeCard },
	{ "ScriptCommand_PauseSong", adapt_ScriptCommand_PauseSong },
	{ "ScriptCommand_ResumeSong", adapt_ScriptCommand_ResumeSong },
	{ "ScriptCommand_nop", adapt_ScriptCommand_nop },
	{ "ScriptCommand_OverrideSong", adapt_ScriptCommand_OverrideSong },
	{ "ScriptCommand_SetDefaultSong", adapt_ScriptCommand_SetDefaultSong },
	{ "ScriptCommand_RecordMasterWin", adapt_ScriptCommand_RecordMasterWin },
	{ "ScriptCommand_ChallengeMachine", adapt_ScriptCommand_ChallengeMachine },
	{ "ScriptCommand_PlaySong", adapt_ScriptCommand_PlaySong },
	{ "ScriptCommand_PlaySFX", adapt_ScriptCommand_PlaySFX },
	{ "ScriptCommand_PlayDefaultSong", adapt_ScriptCommand_PlayDefaultSong },
	{ "ScriptCommand_SetSpriteAttributes", adapt_ScriptCommand_SetSpriteAttributes },
	{ "ScriptCommand_DoFrames", adapt_ScriptCommand_DoFrames },
	{ "ScriptCommand_EndScript", adapt_ScriptCommand_EndScript },
	{ "SetNPCDuelParams", adapt_SetNPCDuelParams },
	{ "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot", adapt_ScriptCommand_LoadCurrentMapNameIntoTxRamSlot },
	{ "ScriptCommand_EnterMap", adapt_ScriptCommand_EnterMap },
	{ "GetScriptArgs1AfterPointer", adapt_GetScriptArgs1AfterPointer },
	{ "SetNextScript", adapt_SetNextScript },
	{ "SetEventValue", adapt_SetEventValue },
	{ "MaxOutEventValue", adapt_MaxOutEventValue },
	{ "ZeroOutEventValue", adapt_ZeroOutEventValue },
	{ "ClearEvents", adapt_ClearEvents },
	{ "ScriptCommand_Jump", adapt_ScriptCommand_Jump },
	{ "ScriptCommand_MaxOutEventValue", adapt_ScriptCommand_MaxOutEventValue },
	{ "ScriptCommand_ZeroOutEventValue", adapt_ScriptCommand_ZeroOutEventValue },
	{ "ScriptCommand_SetEventValue", adapt_ScriptCommand_SetEventValue },
	{ "ScriptCommand_TryGivePCPack", adapt_ScriptCommand_TryGivePCPack },
	{ "ScriptCommand_SetActiveNPCCoords", adapt_ScriptCommand_SetActiveNPCCoords },
	{ "ScriptCommand_JumpIfEnoughCardsOwned", adapt_ScriptCommand_JumpIfEnoughCardsOwned },
	{ "ScriptCommand_RemoveAllEnergyCardsFromCollection", adapt_ScriptCommand_RemoveAllEnergyCardsFromCollection },
	{ "ScriptCommand_JumpIfAnyEnergyCardsInCollection", adapt_ScriptCommand_JumpIfAnyEnergyCardsInCollection },
	{ "ScriptCommand_JumpBasedOnFightingClubPupilStatus", adapt_ScriptCommand_JumpBasedOnFightingClubPupilStatus },
	{ "GetEventValue", adapt_GetEventValue },
	{ "GetEventValueBC", adapt_GetEventValueBC },
	{ "ScriptCommand_JumpIfEventEqual", adapt_ScriptCommand_JumpIfEventEqual },
	{ "ScriptCommand_JumpIfEventZero", adapt_ScriptCommand_JumpIfEventZero },
	{ "ScriptCommand_JumpIfEventGreaterOrEqual", adapt_ScriptCommand_JumpIfEventGreaterOrEqual },
	{ "ScriptCommand_JumpIfEventLessThan", adapt_ScriptCommand_JumpIfEventLessThan },
	{ "ScriptCommand_JumpIfEventNotEqual", adapt_ScriptCommand_JumpIfEventNotEqual },
	{ "ScriptCommand_JumpIfEventNonzero", adapt_ScriptCommand_JumpIfEventNonzero },
	{ "ScriptCommand_JumpIfEventTrue", adapt_ScriptCommand_JumpIfEventTrue },
	{ "ScriptCommand_JumpIfEventFalse", adapt_ScriptCommand_JumpIfEventFalse },
	{ "ScriptCommand_WalkPlayerToMasonLaboratory", adapt_ScriptCommand_WalkPlayerToMasonLaboratory },
	{ "ScriptCommand_IncrementEventValue", adapt_ScriptCommand_IncrementEventValue },
	{ "ScriptCommand_JumpIfPlayerCoordsMatch", adapt_ScriptCommand_JumpIfPlayerCoordsMatch },
	{ "ScriptCommand_JumpIfActiveNPCCoordsMatch", adapt_ScriptCommand_JumpIfActiveNPCCoordsMatch },
	{ "SetNextNPCAndScript", adapt_SetNextNPCAndScript },
	{ "ExecuteNPCMovement", adapt_ExecuteNPCMovement },
	{ "Func_cdd1", adapt_Func_cdd1 },
	{ "ScriptCommand_JumpIfCardOwned", adapt_ScriptCommand_JumpIfCardOwned },
	{ "ScriptCommand_WaitForSongToFinish", adapt_ScriptCommand_WaitForSongToFinish },
	{ "ScriptCommand_SaveGame", adapt_ScriptCommand_SaveGame },
	{ "ScriptCommand_MoveActiveNPC", adapt_ScriptCommand_MoveActiveNPC },
	{ "ScriptCommand_SetNextNPCAndScript", adapt_ScriptCommand_SetNextNPCAndScript },
	{ "ScriptCommand_SetActiveNPCDirection", adapt_ScriptCommand_SetActiveNPCDirection },
	{ "ScriptCommand_PlayCredits", adapt_ScriptCommand_PlayCredits },
	{ "ScriptCommand_PickChallengeHallOpponent", adapt_ScriptCommand_PickChallengeHallOpponent },
	{ "ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot", adapt_ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot },
	{ "DetermineImakuniRoom", adapt_DetermineImakuniRoom },
	{ "ScriptCommand_SetPlayerDirection", adapt_ScriptCommand_SetPlayerDirection },
	{ "ScriptCommand_UnloadActiveNPC", adapt_ScriptCommand_UnloadActiveNPC },
	{ "ScriptCommand_ReplaceMapBlocks", adapt_ScriptCommand_ReplaceMapBlocks },
	{ "ScriptCommand_GiveStarterDeck", adapt_ScriptCommand_GiveStarterDeck },
	{ "ScriptCommand_FlashScreen", adapt_ScriptCommand_FlashScreen },
	{ "ScriptCommand_MoveActiveNPCByDirection", adapt_ScriptCommand_MoveActiveNPCByDirection },
	{ "ScriptCommand_UnloadChallengeHallNPC", adapt_ScriptCommand_UnloadChallengeHallNPC },
	{ "DetermineChallengeHallEvent", adapt_DetermineChallengeHallEvent },
	{ "DetermineImakuniAndChallengeHall", adapt_DetermineImakuniAndChallengeHall },
	{ "ScriptCommand_SetChallengeHallNPCCoords", adapt_ScriptCommand_SetChallengeHallNPCCoords },
	{ "LoadOverworld", adapt_LoadOverworld },
	{ "TryGiveMedalPCPacks", adapt_TryGiveMedalPCPacks },
	{ "GetByteAfterCall", adapt_GetByteAfterCall },
	{ "ScriptCommand_TryGiveMedalPCPacks", adapt_ScriptCommand_TryGiveMedalPCPacks },
	{ "ScriptCommand_SetDialogNPC", adapt_ScriptCommand_SetDialogNPC },
	{ "ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot", adapt_ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot },
	{ "ScriptCommand_StartDuel", adapt_ScriptCommand_StartDuel },
	{ "ScriptCommand_StartChallengeHallDuel", adapt_ScriptCommand_StartChallengeHallDuel },
	{ "ScriptCommand_AskQuestionJump", adapt_ScriptCommand_AskQuestionJump },
	{ "ScriptCommand_AskQuestionJumpDefaultYes", adapt_ScriptCommand_AskQuestionJumpDefaultYes },
	{ "ScriptCommand_JumpIfNPCLoaded", adapt_ScriptCommand_JumpIfNPCLoaded },
	{ "Func_c9c7", adapt_Func_c9c7 },
	{ "Func_c9b8", adapt_Func_c9b8 },
	{ "ScriptCommand_CloseTextBox", adapt_ScriptCommand_CloseTextBox },
	{ "ScriptCommand_PrintText", adapt_ScriptCommand_PrintText },
	{ "Func_c9c0", adapt_Func_c9c0 },
	{ "Script_LegendaryCardRightSpark", adapt_Script_LegendaryCardRightSpark },
	{ "ScriptCommand_PrintNPCText", adapt_ScriptCommand_PrintNPCText },
	{ "Func_cc32", adapt_Func_cc32 },
	{ "ScriptCommand_CloseAdvancedTextBox", adapt_ScriptCommand_CloseAdvancedTextBox },
	{ "ScriptCommand_PrintVariableNPCText", adapt_ScriptCommand_PrintVariableNPCText },
	{ "ScriptCommand_PrintVariableText", adapt_ScriptCommand_PrintVariableText },
	{ "ScriptCommand_PrintTextQuitFully", adapt_ScriptCommand_PrintTextQuitFully },
	{ "ScriptCommand_QuitScriptFully", adapt_ScriptCommand_QuitScriptFully },
	{ "PrintInteractableObjectText", adapt_PrintInteractableObjectText },
	{ "Func_c943", adapt_Func_c943 },
	{ "ScriptCommand_MovePlayer", adapt_ScriptCommand_MovePlayer },
	{ "ScriptCommand_ChooseStarterDeckMultichoice", adapt_ScriptCommand_ChooseStarterDeckMultichoice },
	{ "ScriptCommand_ShowSamNormalMultichoice", adapt_ScriptCommand_ShowSamNormalMultichoice },
	{ "ScriptCommand_ShowSamRulesMultichoice", adapt_ScriptCommand_ShowSamRulesMultichoice },
	{ "ScriptCommand_ChooseDeckToDuelAgainstMultichoice", adapt_ScriptCommand_ChooseDeckToDuelAgainstMultichoice },
	{ "ShowMultichoiceTextbox", adapt_ShowMultichoiceTextbox },
	{ "ScriptCommand_GiveOneOfEachTrainerBooster", adapt_ScriptCommand_GiveOneOfEachTrainerBooster },
	{ "ScriptCommand_ShowCardReceivedScreen", adapt_ScriptCommand_ShowCardReceivedScreen },
	{ "ScriptCommand_ShowMedalReceivedScreen", adapt_ScriptCommand_ShowMedalReceivedScreen },
	{ "ScriptCommand_GiveBoosterPacks", adapt_ScriptCommand_GiveBoosterPacks },
	{ "Script_Clerk10", adapt_Script_Clerk10 },
	{ "Script_LegendaryCardBottomLeft", adapt_Script_LegendaryCardBottomLeft },
	{ "Script_LegendaryCardTopRight", adapt_Script_LegendaryCardTopRight },
	{ "Script_LegendaryCardTopLeft", adapt_Script_LegendaryCardTopLeft },
	{ "Script_LegendaryCardBottomRight", adapt_Script_LegendaryCardBottomRight },
	{ "Script_LegendaryCardLeftSpark", adapt_Script_LegendaryCardLeftSpark },
	{ "Script_Torch", adapt_Script_Torch },
	{ "Script_Woman2", adapt_Script_Woman2 },
	{ "ScriptCommand_OpenDeckMachine", adapt_ScriptCommand_OpenDeckMachine },
	{ "ExecuteArbitraryNPCMovementFromStack", adapt_ExecuteArbitraryNPCMovementFromStack },
	{ "ScriptCommand_MoveChallengeHallNPC", adapt_ScriptCommand_MoveChallengeHallNPC },
	{ "ScriptCommand_MoveArbitraryNPC", adapt_ScriptCommand_MoveArbitraryNPC },
	{ "MaxStackEventValue", adapt_MaxStackEventValue },
	{ "SetStackEventFalse", adapt_SetStackEventFalse },
	{ "SetStackEventValue", adapt_SetStackEventValue },
	{ "SetStackEventZero", adapt_SetStackEventZero },
	{ "GetStackEventValue", adapt_GetStackEventValue },
	{ "RST20", adapt_RST20 },
	{ "ScriptCommand_OpenMenu", adapt_ScriptCommand_OpenMenu },
	{ "ScriptCommand_PrintTextForChallengeCup", adapt_ScriptCommand_PrintTextForChallengeCup },
	{ "ScriptCommand_PickNextMan1RequestedCard", adapt_ScriptCommand_PickNextMan1RequestedCard },
	{ "ScriptCommand_JumpIfMan1RequestedCardOwned", adapt_ScriptCommand_JumpIfMan1RequestedCardOwned },
	{ "ScriptCommand_JumpIfMan1RequestedCardInCollection", adapt_ScriptCommand_JumpIfMan1RequestedCardInCollection },
	{ "ScriptCommand_RemoveMan1RequestedCardFromCollection", adapt_ScriptCommand_RemoveMan1RequestedCardFromCollection },
	{ "ScriptCommand_PickChallengeCupPrizeCard", adapt_ScriptCommand_PickChallengeCupPrizeCard },
	{ "ScriptCommand_PickLegendaryCard", adapt_ScriptCommand_PickLegendaryCard },
	{ "Func_d4fb", adapt_Func_d4fb },
	{ NULL, NULL },
};
/* <<< part probe_entries_scripting */
