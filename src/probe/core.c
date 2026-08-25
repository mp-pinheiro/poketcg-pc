#include "home/core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DrawHPBar */
static void adapt_DrawHPBar(ProbeState *s)
{
	DrawHPBar(s->d, s->e);
}
/* <<< factory DrawHPBar */
static void adapt_ValidateSavedDuelDataFromHL(ProbeState *s)
{
	ValidateSavedDuelDataResult r = ValidateSavedDuelDataFromHL(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ValidateSavedDuelDataFromHL */
/* >>> factory SetLineSeparation */
static void adapt_SetLineSeparation(ProbeState *s)
{
	SetLineSeparation(s->a);
}
/* <<< factory SetLineSeparation */

/* >>> factory PlayAreaScreenMenuFunction */
static void adapt_PlayAreaScreenMenuFunction(ProbeState *s)
{
	s->f = PlayAreaScreenMenuFunction();
}
/* <<< factory PlayAreaScreenMenuFunction */

/* >>> factory SwitchAttackPage */
static void adapt_SwitchAttackPage(ProbeState *s)
{
	(void)s;
	SwitchAttackPage();
}
/* <<< factory SwitchAttackPage */

/* >>> factory CopyCGBCardPalette */
static void adapt_CopyCGBCardPalette(ProbeState *s)
{
	CopyCGBCardPalette(s->a);
}
/* <<< factory CopyCGBCardPalette */

/* >>> factory CreateCardAttrBlkPacket_DataSet */
static void adapt_CreateCardAttrBlkPacket_DataSet(ProbeState *s)
{
	s->hl = CreateCardAttrBlkPacket_DataSet(s->hl, s->a, s->d, s->e);
}
/* <<< factory CreateCardAttrBlkPacket_DataSet */

/* >>> factory SaveDuelDataToDE */
static void adapt_SaveDuelDataToDE(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	SaveDuelDataToDE(de);
}
/* <<< factory SaveDuelDataToDE */

/* >>> factory LoadSavedDuelDataFromDE */
static void adapt_LoadSavedDuelDataFromDE(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	LoadSavedDuelDataFromDE(de);
}
/* <<< factory LoadSavedDuelDataFromDE */

/* >>> factory SetBGP7OrSGB2ToCardPalette */
static void adapt_SetBGP7OrSGB2ToCardPalette(ProbeState *s)
{
	(void)s;
	SetBGP7OrSGB2ToCardPalette();
}
/* <<< factory SetBGP7OrSGB2ToCardPalette */

/* >>> factory JPWriteByteToBGMap0 */
static void adapt_JPWriteByteToBGMap0(ProbeState *s)
{
	JPWriteByteToBGMap0(s->a, s->b, s->c);
}
/* <<< factory JPWriteByteToBGMap0 */


/* >>> factory ZeroObjectPositionsAndToggleOAMCopy */
static void adapt_ZeroObjectPositionsAndToggleOAMCopy(ProbeState *s)
{
	(void)s;
	ZeroObjectPositionsAndToggleOAMCopy();
}
/* <<< factory ZeroObjectPositionsAndToggleOAMCopy */

/* >>> factory LoadPlayerDeck */
static void adapt_LoadPlayerDeck(ProbeState *s)
{
	(void)s;
	LoadPlayerDeck();
}
/* <<< factory LoadPlayerDeck */
/* >>> factory CheckSkipDelayAllowed */
static void adapt_CheckSkipDelayAllowed(ProbeState *s)
{
	CheckSkipDelayAllowedResult r = CheckSkipDelayAllowed(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckSkipDelayAllowed */

/* >>> factory AIMakeDecision */
static void adapt_AIMakeDecision(ProbeState *s)
{
	AIMakeDecisionResult r = AIMakeDecision(s->a);
	s->f = r.f;
}
/* <<< factory AIMakeDecision */

/* >>> factory PrintPracticeDuelDrMasonInstructions */
static void adapt_PrintPracticeDuelDrMasonInstructions(ProbeState *s)
{
	PrintPracticeDuelDrMasonInstructions(s->hl);
}
/* <<< factory PrintPracticeDuelDrMasonInstructions */

/* >>> factory PrintPracticeDuelInstructionsTextBoxLabel */
static void adapt_PrintPracticeDuelInstructionsTextBoxLabel(ProbeState *s)
{
	(void)s;
	PrintPracticeDuelInstructionsTextBoxLabel();
}
/* <<< factory PrintPracticeDuelInstructionsTextBoxLabel */

/* >>> factory SwitchCardPage */
static void adapt_SwitchCardPage(ProbeState *s)
{
	CardPageResult r = SwitchCardPage(s->a);
	s->a = r.a;
}
/* <<< factory SwitchCardPage */



/* >>> factory CardPageSwitch_00 */
static void adapt_CardPageSwitch_00(ProbeState *s)
{
	CardPageResult r = CardPageSwitch_00();
	s->a = r.a;
}
/* <<< factory CardPageSwitch_00 */



/* >>> factory LoadLoaded1CardGfx */
static void adapt_LoadLoaded1CardGfx(ProbeState *s)
{
	LoadLoaded1CardGfx((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory LoadLoaded1CardGfx */

/* >>> factory SetSGB3ToCardPalette */
static void adapt_SetSGB3ToCardPalette(ProbeState *s)
{
	SetSGB3ToCardPalette();
}
/* <<< factory SetSGB3ToCardPalette */


/* >>> factory LookForCardIDInPlayArea_Bank5 */
static void adapt_LookForCardIDInPlayArea_Bank5(ProbeState *s)
{
	LookResult r = LookForCardIDInPlayArea_Bank5(s->a, s->b);
	s->a = r.a;
	s->b = r.b;
	s->f = r.f;
}
/* <<< factory LookForCardIDInPlayArea_Bank5 */

/* >>> factory ClearMemory_Bank5 */
static void adapt_ClearMemory_Bank5(ProbeState *s)
{
	ClearMemory_Bank5(s->a, s->hl);
}
/* <<< factory ClearMemory_Bank5 */

/* >>> factory CheckCardPageExists */
static void adapt_CheckCardPageExists(ProbeState *s)
{
	CardPageExistsResult r = CheckCardPageExists(&s->hl);
	s->a = r.a;
	s->f = r.zero ? (uint8_t)0x80u : (uint8_t)0x00u;
}
/* <<< factory CheckCardPageExists */


/* >>> factory CardPageSwitch_PokemonEnd */
static void adapt_CardPageSwitch_PokemonEnd(ProbeState *s)
{
	CardPageResult r = CardPageSwitch_PokemonEnd();
	s->a = r.a;
	s->f = (uint8_t)((s->f & 0x80u) | (r.carry ? 0x10u : 0u));
}
/* <<< factory CardPageSwitch_PokemonEnd */


/* >>> factory SetCardListInfoBoxText */
static void adapt_SetCardListInfoBoxText(ProbeState *s)
{
	SetCardListInfoBoxText(s->hl);
}
/* <<< factory SetCardListInfoBoxText */

/* >>> factory PrintCardListHeaderAndInfoBoxTexts */
static void adapt_PrintCardListHeaderAndInfoBoxTexts(ProbeState *s)
{
	(void)s;
	PrintCardListHeaderAndInfoBoxTexts();
}
/* <<< factory PrintCardListHeaderAndInfoBoxTexts */

/* >>> factory LoadCardNameToTxRam2 */
static void adapt_LoadCardNameToTxRam2(ProbeState *s)
{
	LoadCardNameToTxRam2(s->a);
}
/* <<< factory LoadCardNameToTxRam2 */




/* >>> factory LoadCardNameToTxRam2_b */
static void adapt_LoadCardNameToTxRam2_b(ProbeState *s)
{
	s->a = LoadCardNameToTxRam2_b(s->a);
}
/* <<< factory LoadCardNameToTxRam2_b */




/* >>> factory GetAnimCoordsAndFlags */
static void adapt_GetAnimCoordsAndFlags(ProbeState *s)
{
	AnimCoordsResult r = GetAnimCoordsAndFlags();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory GetAnimCoordsAndFlags */


/* >>> factory PlayBufferedDuelAnimations */
static void adapt_PlayBufferedDuelAnimations(ProbeState *s)
{
	AnimBufferResult r = PlayBufferedDuelAnimations();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PlayBufferedDuelAnimations */
/* >>> factory ReturnWrongAction */
static void adapt_ReturnWrongAction(ProbeState *s)
{
	s->f = ReturnWrongAction(s->f);
}
/* <<< factory ReturnWrongAction */

/* >>> factory HandleFailedToContinueDuel */
static void adapt_HandleFailedToContinueDuel(ProbeState *s)
{
	s->f = HandleFailedToContinueDuel(s->hl);
}
/* <<< factory HandleFailedToContinueDuel */


/* >>> factory CopyListWithFFTerminatorFromHLToDE_Bank5 */
static void adapt_CopyListWithFFTerminatorFromHLToDE_Bank5(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	CopyListResult r = CopyListWithFFTerminatorFromHLToDE_Bank5(&s->hl, &de);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory CopyListWithFFTerminatorFromHLToDE_Bank5 */

/* >>> factory CheckEnergyFlagsNeededInList */
static void adapt_CheckEnergyFlagsNeededInList(ProbeState *s)
{
	EnergyFlagsResult r = CheckEnergyFlagsNeededInList(s->a);
	s->a = r.a;
	s->f = r.carry ? 0x10u : 0u;
}
/* <<< factory CheckEnergyFlagsNeededInList */
/* >>> factory CardPageSwitch_EnergyEnd */
static void adapt_CardPageSwitch_EnergyEnd(ProbeState *s)
{
	CardPageResult r = CardPageSwitch_EnergyEnd();
	s->a = r.a;
	s->f = (uint8_t)((s->f & 0x80u) | (r.carry ? 0x10u : 0u));
}
/* <<< factory CardPageSwitch_EnergyEnd */

/* >>> factory CardPageSwitch_0c */
static void adapt_CardPageSwitch_0c(ProbeState *s)
{
	CardPageResult r = CardPageSwitch_0c();
	s->a = r.a;
	s->f = (uint8_t)((s->f & 0x80u) | (r.carry ? 0x10u : 0u));
}
/* <<< factory CardPageSwitch_0c */

/* >>> factory PlaceCardImageOAM */
static void adapt_PlaceCardImageOAM(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	s->a = PlaceCardImageOAM(&s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory PlaceCardImageOAM */

/* >>> factory PrintPlayAreaCardAttachedEnergies */
static void adapt_PrintPlayAreaCardAttachedEnergies(ProbeState *s)
{
	PrintPlayAreaCardAttachedEnergies(s->b, s->c, s->e);
}
/* <<< factory PrintPlayAreaCardAttachedEnergies */

/* >>> factory DiscardRetreatCostCards */
static void adapt_DiscardRetreatCostCards(ProbeState *s)
{
	DiscardRetreatCostCardsResult r = DiscardRetreatCostCards();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DiscardRetreatCostCards */


/* >>> factory OppAction_DrawCard */
static void adapt_OppAction_DrawCard(ProbeState *s)
{
	OppActionDrawResult r = OppAction_DrawCard();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory OppAction_DrawCard */

/* >>> factory PrintSortNumberInCardList_SetPointer */
static void adapt_PrintSortNumberInCardList_SetPointer(ProbeState *s)
{
	PrintSortNumberInCardList_SetPointer();
}
/* <<< factory PrintSortNumberInCardList_SetPointer */

/* >>> factory PrintSortNumberInCardList */
static void adapt_PrintSortNumberInCardList(ProbeState *s)
{
	PrintSortNumberInCardList();
}
/* <<< factory PrintSortNumberInCardList */

/* >>> factory PrintEnergiesOfColor */
static void adapt_PrintEnergiesOfColor(ProbeState *s)
{
	PrintEnergiesResult r = PrintEnergiesOfColor(s->a, s->b, s->c, s->e);
	s->a = r.a;
	s->b = r.b;
	s->e = r.e;
}
/* <<< factory PrintEnergiesOfColor */

/* >>> factory PrintCardPageWeaknessesOrResistances */
static void adapt_PrintCardPageWeaknessesOrResistances(ProbeState *s)
{
	PrintCardPageWeaknessesOrResistances(s->a, s->b, s->c);
}
/* <<< factory PrintCardPageWeaknessesOrResistances */

/* >>> factory Func_6423 */
static void adapt_Func_6423(ProbeState *s)
{
	Func6423Result r = Func_6423(s->b, s->c);
	s->a = r.a;
	s->b = r.b;
	s->hl = r.hl;
}
/* <<< factory Func_6423 */

/* >>> factory InitVariablesToBeginDuel */
static void adapt_InitVariablesToBeginDuel(ProbeState *s)
{
	(void)s;
	InitVariablesToBeginDuel();
}
/* <<< factory InitVariablesToBeginDuel */

/* >>> factory CreateCardAttrBlkPacket */
static void adapt_CreateCardAttrBlkPacket(ProbeState *s)
{
	s->hl = CreateCardAttrBlkPacket(s->a, s->d, s->e);
	s->a = 0u;
	s->f = 0x80u;
}
/* <<< factory CreateCardAttrBlkPacket */

/* >>> factory CardPageSwitch_PokemonAttack1Page2 */
static void adapt_CardPageSwitch_PokemonAttack1Page2(ProbeState *s)
{
	CardPageExistsResult r = CardPageSwitch_PokemonAttack1Page2(&s->hl);
	s->a = r.a;
	s->f = r.zero ? 0x80u : 0x00u;
}
/* <<< factory CardPageSwitch_PokemonAttack1Page2 */

/* >>> factory CardPageSwitch_PokemonAttack2Page1 */
static void adapt_CardPageSwitch_PokemonAttack2Page1(ProbeState *s)
{
	CardPageExistsResult r = CardPageSwitch_PokemonAttack2Page1();
	s->a = r.a;
	s->f = r.zero ? 0x80u : 0x00u;
}
/* <<< factory CardPageSwitch_PokemonAttack2Page1 */

/* >>> factory AIDiscourage */
static void adapt_AIDiscourage(ProbeState *s)
{
	AIDiscourage(s->a);
}
/* <<< factory AIDiscourage */

/* >>> factory ConvertHPToDamageCounters_Bank5 */
static void adapt_ConvertHPToDamageCounters_Bank5(ProbeState *s)
{
	ConvertHPToDamageCountersResult r = ConvertHPToDamageCounters_Bank5(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ConvertHPToDamageCounters_Bank5 */

/* >>> factory CalculateBDividedByA_Bank5 */
static void adapt_CalculateBDividedByA_Bank5(ProbeState *s)
{
	CalculateBDividedByAResult r = CalculateBDividedByA_Bank5(s->a, s->b);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CalculateBDividedByA_Bank5 */

/* >>> factory PrintCardPageRarityIcon */
static void adapt_PrintCardPageRarityIcon(ProbeState *s)
{
	ProcessTextHeaderResult r = PrintCardPageRarityIcon(s->a, s->d, s->e, s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PrintCardPageRarityIcon */



/* >>> factory SetNoLineSeparation */
static void adapt_SetNoLineSeparation(ProbeState *s)
{
	s->a = SetNoLineSeparation();
}
/* <<< factory SetNoLineSeparation */



/* >>> factory AIPlayInitialBasicCards */
static void adapt_AIPlayInitialBasicCards(ProbeState *s)
{
	AIPlayInitialBasicCardsResult r = AIPlayInitialBasicCards();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIPlayInitialBasicCards */

/* >>> factory CheckIfEnoughParticularAttachedEnergy */
static void adapt_CheckIfEnoughParticularAttachedEnergy(ProbeState *s)
{
	CheckIfEnoughParticularAttachedEnergyResult r =
		CheckIfEnoughParticularAttachedEnergy(s->a, s->hl, s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->hl = r.hl;
}
/* <<< factory CheckIfEnoughParticularAttachedEnergy */

/* >>> factory Func_14323 */
static void adapt_Func_14323(ProbeState *s)
{
	s->f = Func_14323().f;
}
/* <<< factory Func_14323 */

/* >>> factory CreateEnergyCardListFromHand */
static void adapt_CreateEnergyCardListFromHand(ProbeState *s)
{
	CoreCardListResult r = CreateEnergyCardListFromHand(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CreateEnergyCardListFromHand */

/* >>> factory LookForCardIDInHand */
static void adapt_LookForCardIDInHand(ProbeState *s)
{
	CoreCardListResult r = LookForCardIDInHand(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInHand */


/* >>> factory LookForCardIDInHandList_Bank5 */
static void adapt_LookForCardIDInHandList_Bank5(ProbeState *s)
{
	CoreCardListResult r = LookForCardIDInHandList_Bank5(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory LookForCardIDInHandList_Bank5 */


/* >>> factory CheckForEvolutionInDeck */
static void adapt_CheckForEvolutionInDeck(ProbeState *s)
{ CheckForEvolutionInDeckResult r = CheckForEvolutionInDeck(s->a, s->f); s->a = r.a; s->f = r.f; }
/* <<< factory CheckForEvolutionInDeck */


/* >>> factory LookForCardThatIsKnockedOutOnDevolution */
static void adapt_LookForCardThatIsKnockedOutOnDevolution(ProbeState *s)
{ LookForCardThatIsKnockedOutOnDevolutionResult r=LookForCardThatIsKnockedOutOnDevolution(s->f); s->a=r.a; s->f=r.f; }
/* <<< factory LookForCardThatIsKnockedOutOnDevolution */


/* >>> factory CalculateParticularAttachedEnergyNeeded */
static void adapt_CalculateParticularAttachedEnergyNeeded(ProbeState *s)
{ CalculateParticularAttachedEnergyNeededResult r = CalculateParticularAttachedEnergyNeeded(s->a, s->b, s->hl); s->a = r.a; s->f = r.f; s->b = r.b; s->hl = r.hl; }
/* <<< factory CalculateParticularAttachedEnergyNeeded */

/* >>> factory GetAnimationData */
static void adapt_GetAnimationData(ProbeState *s)
{
	uint8_t z = (uint8_t)(s->f & 0x80u);
	AnimationDataResult r = GetAnimationData();
	s->a = r.a;
	s->f = (uint8_t)(z | r.f);
	s->hl = r.hl;
}
/* <<< factory GetAnimationData */


/* >>> factory CardPageSwitch_PokemonOverviewOrDescription */
static void adapt_CardPageSwitch_PokemonOverviewOrDescription(ProbeState *s)
{
	CardPageResult r = CardPageSwitch_PokemonOverviewOrDescription();
	s->a = r.a;
}
/* <<< factory CardPageSwitch_PokemonOverviewOrDescription */



/* >>> factory CheckCardEvolutionInHandOrDeck */
static void adapt_CheckCardEvolutionInHandOrDeck(ProbeState *s)
{
	CheckCardEvolutionInHandOrDeckResult r = CheckCardEvolutionInHandOrDeck(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckCardEvolutionInHandOrDeck */

/* >>> factory CheckIfOpponentHasBossDeckID */
static void adapt_CheckIfOpponentHasBossDeckID(ProbeState *s)
{
	CheckIfOpponentHasBossDeckIDResult r = CheckIfOpponentHasBossDeckID(s->a);
	s->a = r.a;
	s->f = r.carry ? (uint8_t)((s->f & 0x80u) | 0x10u) : (s->a == 0u ? 0x80u : 0u);
}
/* <<< factory CheckIfOpponentHasBossDeckID */


/* >>> factory RaiseAIScoreToAllMatchingIDsInBench */
static void adapt_RaiseAIScoreToAllMatchingIDsInBench(ProbeState *s)
{
	s->hl = RaiseAIScoreToAllMatchingIDsInBench(s->a);
}
/* <<< factory RaiseAIScoreToAllMatchingIDsInBench */


/* >>> factory GetDamageNumberChars */
static void adapt_GetDamageNumberChars(ProbeState *s)
{
	(void)s;
	GetDamageNumberChars();
}
/* <<< factory GetDamageNumberChars */

/* >>> factory CardPageSwitch_PokemonAttack2Page2 */
static void adapt_CardPageSwitch_PokemonAttack2Page2(ProbeState *s)
{
	CardPageExistsResult r = CardPageSwitch_PokemonAttack2Page2();
	s->a = r.a;
	s->f = r.zero ? 0x80u : 0x00u;
}
/* <<< factory CardPageSwitch_PokemonAttack2Page2 */

/* >>> factory CardPageSwitch_08 */
static void adapt_CardPageSwitch_08(ProbeState *s)
{
	CardPageResult r = CardPageSwitch_08();
	s->a = r.a;
	s->f = (uint8_t)((s->f & 0x80u) | (r.carry ? 0x10u : 0u));
}
/* <<< factory CardPageSwitch_08 */

/* >>> factory LoadPlayAreaCardGfx */
static void adapt_LoadPlayAreaCardGfx(ProbeState *s)
{
	LoadPlayAreaCardGfx(s->a, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory LoadPlayAreaCardGfx */

/* >>> factory SetBGP6OrSGB3ToCardPalette */
static void adapt_SetBGP6OrSGB3ToCardPalette(ProbeState *s)
{
	(void)s;
	SetBGP6OrSGB3ToCardPalette();
}
/* <<< factory SetBGP6OrSGB3ToCardPalette */

/* >>> factory SetOneLineSeparation */
static void adapt_SetOneLineSeparation(ProbeState *s)
{
	s->a = SetOneLineSeparation();
}
/* <<< factory SetOneLineSeparation */


/* >>> factory _HasAlivePokemonInPlayArea */
static void adapt__HasAlivePokemonInPlayArea(ProbeState *s)
{
	HasAlivePokemonInPlayAreaResult r = _HasAlivePokemonInPlayArea(s->a);
	s->a = r.a;
	s->f = (uint8_t)((s->f & 0x80u) | r.f);
}
/* <<< factory _HasAlivePokemonInPlayArea */

/* >>> factory PrintPlayAreaCardLocation */
static void adapt_PrintPlayAreaCardLocation(ProbeState *s)
{
	(void)s;
	PrintPlayAreaCardLocation();
}
/* <<< factory PrintPlayAreaCardLocation */


/* >>> factory CheckPrintPoisoned */
static void adapt_CheckPrintPoisoned(ProbeState *s)
{
	s->a = CheckPrintPoisoned(s->a, s->b, s->c);
}
/* <<< factory CheckPrintPoisoned */

/* >>> factory ResetDoFrameFunction_Bank1 */
static void adapt_ResetDoFrameFunction_Bank1(ProbeState *s)
{
	ResetDoFrameFunction_Bank1();
	s->a = 0u;
	s->f = 0x80u;
	s->hl = (uint16_t)(wDoFrameFunction_ADDR + 1u);
}
/* <<< factory ResetDoFrameFunction_Bank1 */

/* >>> factory OppAction_NoAction */
static void adapt_OppAction_NoAction(ProbeState *s)
{
	(void)s;
	OppAction_NoAction();
}
/* <<< factory OppAction_NoAction */

/* >>> factory ReturnRetreatCostCardsToArena */
static void adapt_ReturnRetreatCostCardsToArena(ProbeState *s)
{
	ReturnRetreatCostCardsToArenaResult r =
		ReturnRetreatCostCardsToArena(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ReturnRetreatCostCardsToArena */


/* >>> factory FindHighestBenchScore */
static void adapt_FindHighestBenchScore(ProbeState *s)
{
	FindHighestBenchScoreResult r = FindHighestBenchScore();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory FindHighestBenchScore */

/* >>> factory AIEncourage */
static void adapt_AIEncourage(ProbeState *s)
{
	AIEncourageResult r = AIEncourage(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIEncourage */
/* >>> factory Func_6ba2 */
static void adapt_Func_6ba2(ProbeState *s)
{
	Func_6ba2(s->hl);
}
/* <<< factory Func_6ba2 */


/* >>> factory IsLoadedCard1BasicPokemon */
static void adapt_IsLoadedCard1BasicPokemon(ProbeState *s)
{
	IsLoadedCard1BasicPokemonResult r = IsLoadedCard1BasicPokemon();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory IsLoadedCard1BasicPokemon */

/* >>> factory PracticeDuel_PlayGoldeen */
static void adapt_PracticeDuel_PlayGoldeen(ProbeState *s)
{
	s->f = PracticeDuel_PlayGoldeen().f;
}
/* <<< factory PracticeDuel_PlayGoldeen */

/* >>> factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */
static void adapt_TwoByteNumberToTxSymbol_PadSpace_Bank1(ProbeState *s)
{
	TwoByteNumberToTxSymbolPadResult r =
		TwoByteNumberToTxSymbol_PadSpace_Bank1(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */

/* >>> factory DrawWideTextBox_WaitForInput_Bank1 */
static void adapt_DrawWideTextBox_WaitForInput_Bank1(ProbeState *s)
{
	WaitResult r = DrawWideTextBox_WaitForInput_Bank1(s->hl);
	s->f = r.f;
}
/* <<< factory DrawWideTextBox_WaitForInput_Bank1 */


/* >>> factory CardPageSwitch_EnergyOrTrainerPage1 */
static void adapt_CardPageSwitch_EnergyOrTrainerPage1(ProbeState *s)
{
	CardPageSwitchEnergyResult r = CardPageSwitch_EnergyOrTrainerPage1();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CardPageSwitch_EnergyOrTrainerPage1 */

/* >>> factory CardPageSwitch_TrainerEnd */
static void adapt_CardPageSwitch_TrainerEnd(ProbeState *s)
{
	uint8_t z = (uint8_t)(s->f & 0x80u);
	CardPageResult r = CardPageSwitch_TrainerEnd();
	s->a = r.a;
	s->f = (uint8_t)(z | 0x10u);
}
/* <<< factory CardPageSwitch_TrainerEnd */

/* >>> factory CheckIfEnoughEnergiesOfType */
static void adapt_CheckIfEnoughEnergiesOfType(ProbeState *s)
{
	CheckIfEnoughEnergiesResult r = CheckIfEnoughEnergiesOfType(s->a, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckIfEnoughEnergiesOfType */
/* >>> factory CheckIfActiveCardParalyzedOrAsleep */
static void adapt_CheckIfActiveCardParalyzedOrAsleep(ProbeState *s)
{
	CheckIfActiveStatusResult r = CheckIfActiveCardParalyzedOrAsleep();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckIfActiveCardParalyzedOrAsleep */
/* >>> factory GetAttacksEnergyCostBits */
static void adapt_GetAttacksEnergyCostBits(ProbeState *s)
{
	s->a = GetAttacksEnergyCostBits(s->a).a;
}
/* <<< factory GetAttacksEnergyCostBits */
/* >>> factory CheckForEvolutionInList */
static void adapt_CheckForEvolutionInList(ProbeState *s)
{
	CheckForEvolutionInListResult r = CheckForEvolutionInList(s->a, s->f);
	s->a = r.a;
	s->b = r.b;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckForEvolutionInList */
/* >>> factory CountNumberOfEnergyCardsAttached */
static void adapt_CountNumberOfEnergyCardsAttached(ProbeState *s)
{
	CountNumberOfEnergyCardsAttachedResult r =
		CountNumberOfEnergyCardsAttached(s->e);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CountNumberOfEnergyCardsAttached */
/* >>> factory LookForCardIDInLocation_Bank5 */
static void adapt_LookForCardIDInLocation_Bank5(ProbeState *s)
{
	LookForCardIDInLocationResult r =
		LookForCardIDInLocation_Bank5(s->a, s->e);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory LookForCardIDInLocation_Bank5 */
/* >>> factory LoadDefendingPokemonColorWRAndPrizeCards */
static void adapt_LoadDefendingPokemonColorWRAndPrizeCards(ProbeState *s)
{
	(void)s;
	LoadDefendingPokemonColorWRAndPrizeCards();
}
/* <<< factory LoadDefendingPokemonColorWRAndPrizeCards */

/* >>> factory CheckIfEnergyIsUseful */
static void adapt_CheckIfEnergyIsUseful(ProbeState *s)
{
	CheckIfEnergyIsUsefulResult r = CheckIfEnergyIsUseful(s->a);
	s->f = r.f;
}
/* <<< factory CheckIfEnergyIsUseful */

/* >>> factory PickRandomBenchPokemon */
static void adapt_PickRandomBenchPokemon(ProbeState *s)
{
	s->a = PickRandomBenchPokemon();
}
/* <<< factory PickRandomBenchPokemon */

/* >>> factory PracticeDuel_VerifyPlayerTurnActions */
static void adapt_PracticeDuel_VerifyPlayerTurnActions(ProbeState *s)
{
	s->f = PracticeDuel_VerifyPlayerTurnActions().f;
}
/* <<< factory PracticeDuel_VerifyPlayerTurnActions */

/* >>> factory PrintCardNameFromCardIDInTextBox */
static void adapt_PrintCardNameFromCardIDInTextBox(ProbeState *s)
{
	PrintCardNameFromCardIDInTextBox(s->hl);
}
/* <<< factory PrintCardNameFromCardIDInTextBox */
/* >>> factory RemoveCardIDInList */
static void adapt_RemoveCardIDInList(ProbeState *s)
{
	RemoveCardIDResult r = RemoveCardIDInList(&s->hl, s->e);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory RemoveCardIDInList */
/* >>> factory SortTempHandByIDList */
static void adapt_SortTempHandByIDList(ProbeState *s)
{
	SortTempHandResult r = SortTempHandByIDList();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory SortTempHandByIDList */
/* >>> factory ApplyCardCGBAttributes */
static void adapt_ApplyCardCGBAttributes(ProbeState *s)
{
	ApplyCardCGBAttributes((uint16_t)((uint16_t)s->d << 8 | s->e));
}
/* <<< factory ApplyCardCGBAttributes */
/* >>> factory ApplyStatusConditionToArenaPokemon */
static void adapt_ApplyStatusConditionToArenaPokemon(ProbeState *s)
{
	s->a = ApplyStatusConditionToArenaPokemon(&s->hl, s->d, &s->e);
}
/* <<< factory ApplyStatusConditionToArenaPokemon */

/* >>> factory CheckIfEnoughEnergiesToRetreat */
static void adapt_CheckIfEnoughEnergiesToRetreat(ProbeState *s)
{
	EnoughRetreatEnergiesResult r = CheckIfEnoughEnergiesToRetreat();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfEnoughEnergiesToRetreat */
/* >>> factory DecideLinkDuelVariables */
static void adapt_DecideLinkDuelVariables(ProbeState *s)
{
	s->f = DecideLinkDuelVariables();
}
/* <<< factory DecideLinkDuelVariables */
/* >>> factory DisplayAttackPage */
static void adapt_DisplayAttackPage(ProbeState *s)
{
	DisplayAttackPage();
}
/* <<< factory DisplayAttackPage */
/* >>> factory DisplayCardPage */
static void adapt_DisplayCardPage(ProbeState *s)
{
	DisplayCardPage();
}
/* <<< factory DisplayCardPage */
/* >>> factory DoPracticeDuelAction */
static void adapt_DoPracticeDuelAction(ProbeState *s)
{
	s->f = DoPracticeDuelAction(s->a);
}
/* <<< factory DoPracticeDuelAction */
/* >>> factory DrawDuelHorizontalSeparator */
static void adapt_DrawDuelHorizontalSeparator(ProbeState *s)
{
	DrawDuelHorizontalSeparator();
}
/* <<< factory DrawDuelHorizontalSeparator */
/* >>> factory MoveAllTurnHolderKnockedOutPokemonToDiscardPile */
static void adapt_MoveAllTurnHolderKnockedOutPokemonToDiscardPile(ProbeState *s)
{
	MoveAllTurnHolderKnockedOutPokemonToDiscardPile();
}
/* <<< factory MoveAllTurnHolderKnockedOutPokemonToDiscardPile */
/* >>> factory PrintSortNumberInCardList_CallFromPointer */
static void adapt_PrintSortNumberInCardList_CallFromPointer(ProbeState *s)
{
	PrintSortNumberInCardList_CallFromPointer();
}
/* <<< factory PrintSortNumberInCardList_CallFromPointer */
/* >>> factory PracticeDuel_VerifyInitialPlay */
static void adapt_PracticeDuel_VerifyInitialPlay(ProbeState *s)
{
	s->f = PracticeDuel_VerifyInitialPlay().f;
}
/* <<< factory PracticeDuel_VerifyInitialPlay */

/* >>> factory CheckIfNoSurplusEnergyForAttack */
static void adapt_CheckIfNoSurplusEnergyForAttack(ProbeState *s)
{
	CheckIfNoSurplusEnergyResult r = CheckIfNoSurplusEnergyForAttack();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfNoSurplusEnergyForAttack */

/* >>> factory Func_1585b */
static void adapt_Func_1585b(ProbeState *s)
{
	Func1585bResult r = Func_1585b(s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_1585b */

/* >>> factory CheckIfNotABossDeckID */
static void adapt_CheckIfNotABossDeckID(ProbeState *s)
{
	CheckIfNotABossDeckIDResult r = CheckIfNotABossDeckID();
	s->a = r.a;
}
/* <<< factory CheckIfNotABossDeckID */

/* >>> factory AIChooseRandomlyNotToDoAction */
static void adapt_AIChooseRandomlyNotToDoAction(ProbeState *s)
{
	AIChooseRandomlyNotToDoActionResult r = AIChooseRandomlyNotToDoAction();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIChooseRandomlyNotToDoAction */

/* >>> factory TrySetUpBossStartingPlayArea */
static void adapt_TrySetUpBossStartingPlayArea(ProbeState *s)
{
	TrySetUpBossStartingPlayAreaResult r = TrySetUpBossStartingPlayArea();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory TrySetUpBossStartingPlayArea */

/* >>> factory CardPageSwitch_TrainerPage2 */
static void adapt_CardPageSwitch_TrainerPage2(ProbeState *s)
{
	TrainerPageResult r = CardPageSwitch_TrainerPage2();
	s->hl = r.hl;
	s->a = r.a;
	s->f = r.zero ? 0x80u : 0x00u;
}
/* <<< factory CardPageSwitch_TrainerPage2 */

/* >>> factory LoadAndValidateDuelSaveData */
static void adapt_LoadAndValidateDuelSaveData(ProbeState *s)
{
	s->f = LoadAndValidateDuelSaveData();
}
/* <<< factory LoadAndValidateDuelSaveData */

/* >>> factory ValidateSavedNonLinkDuelData */
static void adapt_ValidateSavedNonLinkDuelData(ProbeState *s)
{
	s->f = ValidateSavedNonLinkDuelData();
}
/* <<< factory ValidateSavedNonLinkDuelData */

/* >>> factory SetupPlayAreaScreen */
static void adapt_SetupPlayAreaScreen(ProbeState *s)
{
	SetupPlayAreaScreen();
}
/* <<< factory SetupPlayAreaScreen */

/* >>> factory CheckIfEnoughEnergiesForGivenAttack */
static void adapt_CheckIfEnoughEnergiesForGivenAttack(ProbeState *s)
{
	CheckIfEnoughEnergiesForGivenAttackResult r = CheckIfEnoughEnergiesForGivenAttack(s->d, s->e);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CheckIfEnoughEnergiesForGivenAttack */

/* >>> factory SaveDuelData */
static void adapt_SaveDuelData(ProbeState *s)
{
	(void)s;
	SaveDuelData();
}
/* <<< factory SaveDuelData */

/* >>> factory SetCardListHeaderText */
static void adapt_SetCardListHeaderText(ProbeState *s)
{
	SetCardListHeaderText((uint16_t)((uint16_t)s->d << 8 | s->e), s->hl);
}
/* <<< factory SetCardListHeaderText */

/* >>> factory AIAttachEnergyInHandToCardInPlayArea */
static void adapt_AIAttachEnergyInHandToCardInPlayArea(ProbeState *s)
{
	AIAttachEnergyInHandToCardInPlayAreaResult r = AIAttachEnergyInHandToCardInPlayArea(s->d, s->e);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIAttachEnergyInHandToCardInPlayArea */

/* >>> factory GoToPreviousCardPage */
static void adapt_GoToPreviousCardPage(ProbeState *s)
{
	CardPageNavigationResult r = GoToPreviousCardPage();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
}
/* <<< factory GoToPreviousCardPage */

/* >>> factory DrawWholeScreenTextBox */
static void adapt_DrawWholeScreenTextBox(ProbeState *s)
{
	DrawWholeScreenTextBox(s->hl);
}
/* <<< factory DrawWholeScreenTextBox */

/* >>> factory HasAlivePokemonInPlayArea */
static void adapt_HasAlivePokemonInPlayArea(ProbeState *s)
{
	HasAlivePokemonInPlayAreaResult r = HasAlivePokemonInPlayArea();
	s->a = r.a;
	s->f = (uint8_t)((s->f & 0x80u) | r.f);
}
/* <<< factory HasAlivePokemonInPlayArea */

/* >>> factory CardPageSwitch_PokemonAttack1Page1 */
static void adapt_CardPageSwitch_PokemonAttack1Page1(ProbeState *s)
{
	CardPageExistsResult r = CardPageSwitch_PokemonAttack1Page1();
	s->a = r.a;
	s->f = r.zero ? 0x80u : 0x00u;
}
/* <<< factory CardPageSwitch_PokemonAttack1Page1 */

/* >>> factory CheckPrintDoublePoisoned */
static void adapt_CheckPrintDoublePoisoned(ProbeState *s)
{
	s->a = CheckPrintDoublePoisoned(s->a, s->b, s->c);
}
/* <<< factory CheckPrintDoublePoisoned */

/* >>> factory PrintPracticeDuelLetsPlayTheGame */
static void adapt_PrintPracticeDuelLetsPlayTheGame(ProbeState *s)
{
	PrintPracticeDuelLetsPlayTheGame();
}
/* <<< factory PrintPracticeDuelLetsPlayTheGame */

/* >>> factory AIAttachEnergyInHandToCardInBench */
static void adapt_AIAttachEnergyInHandToCardInBench(ProbeState *s)
{
	AIAttachEnergyInHandToCardInBenchResult r = AIAttachEnergyInHandToCardInBench(s->d, s->e);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIAttachEnergyInHandToCardInBench */

/* >>> factory DrawPracticeDuelInstructionsTextBox */
static void adapt_DrawPracticeDuelInstructionsTextBox(ProbeState *s)
{
	(void)s;
	DrawPracticeDuelInstructionsTextBox();
}
/* <<< factory DrawPracticeDuelInstructionsTextBox */

/* >>> factory PracticeDuelVerify_Turn7Or8 */
static void adapt_PracticeDuelVerify_Turn7Or8(ProbeState *s)
{
	PracticeDuelVerifyTurn7Or8Result r = PracticeDuelVerify_Turn7Or8();
	s->f = r.f;
}
/* <<< factory PracticeDuelVerify_Turn7Or8 */

/* >>> factory SetDiscardPileScreenTexts */
static void adapt_SetDiscardPileScreenTexts(ProbeState *s)
{
	SetDiscardPileScreenTexts();
}
/* <<< factory SetDiscardPileScreenTexts */

/* >>> factory PrintAttachedEnergyToPokemon */
static void adapt_PrintAttachedEnergyToPokemon(ProbeState *s)
{
	(void)s;
	PrintAttachedEnergyToPokemon();
}
/* <<< factory PrintAttachedEnergyToPokemon */

/* >>> factory PrintPokemonEvolvedIntoPokemon */
static void adapt_PrintPokemonEvolvedIntoPokemon(ProbeState *s)
{
	(void)s;
	PrintPokemonEvolvedIntoPokemon();
}
/* <<< factory PrintPokemonEvolvedIntoPokemon */

/* >>> factory SetupDuel */
static void adapt_SetupDuel(ProbeState *s)
{
	(void)s;
	SetupDuel();
}
/* <<< factory SetupDuel */

/* >>> factory PracticeDuelVerify_Turn6 */
static void adapt_PracticeDuelVerify_Turn6(ProbeState *s)
{
	PracticeDuelVerifyTurn6Result r = PracticeDuelVerify_Turn6();
	s->f = r.f;
}
/* <<< factory PracticeDuelVerify_Turn6 */

/* >>> factory PracticeDuelVerify_Turn4 */
static void adapt_PracticeDuelVerify_Turn4(ProbeState *s)
{
	s->f = PracticeDuelVerify_Turn4().f;
}
/* <<< factory PracticeDuelVerify_Turn4 */

/* >>> factory ShuffleDeckAndDrawSevenCards */
static void adapt_ShuffleDeckAndDrawSevenCards(ProbeState *s)
{
	ShuffleDeckAndDrawSevenCardsResult r = ShuffleDeckAndDrawSevenCards();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ShuffleDeckAndDrawSevenCards */

/* >>> factory WriteTwoDigitNumberInTxSymbol_PadSpace */
static void adapt_WriteTwoDigitNumberInTxSymbol_PadSpace(ProbeState *s)
{
	WriteTwoDigitNumberInTxSymbol_PadSpace(s->a, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory WriteTwoDigitNumberInTxSymbol_PadSpace */

/* >>> factory PrintOpponentNumberOfHandAndDeckCards */
static void adapt_PrintOpponentNumberOfHandAndDeckCards(ProbeState *s)
{
	(void)s;
	PrintOpponentNumberOfHandAndDeckCards();
}
/* <<< factory PrintOpponentNumberOfHandAndDeckCards */

/* >>> factory PrintPlayerNumberOfHandAndDeckCards */
static void adapt_PrintPlayerNumberOfHandAndDeckCards(ProbeState *s)
{
	(void)s;
	PrintPlayerNumberOfHandAndDeckCards();
}
/* <<< factory PrintPlayerNumberOfHandAndDeckCards */

/* >>> factory PrintDuelResultStats */
static void adapt_PrintDuelResultStats(ProbeState *s)
{
	(void)s;
	PrintDuelResultStats();
}
/* <<< factory PrintDuelResultStats */

/* >>> factory ConvertColorToEnergyCardID */
static void adapt_ConvertColorToEnergyCardID(ProbeState *s)
{
	s->a = ConvertColorToEnergyCardID(s->a);
}
/* <<< factory ConvertColorToEnergyCardID */

/* >>> factory WriteOneByteNumberInTxSymbol_PadSpace */
static void adapt_WriteOneByteNumberInTxSymbol_PadSpace(ProbeState *s)
{
	WriteOneByteNumberInTxSymbol_PadSpace(s->a, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory WriteOneByteNumberInTxSymbol_PadSpace */

/* >>> factory PrintPracticeDuelNumberedInstruction */
static void adapt_PrintPracticeDuelNumberedInstruction(ProbeState *s)
{
	PrintPracticeDuelNumberedInstructionResult result = PrintPracticeDuelNumberedInstruction(s->d, s->e, s->hl);
	s->hl = result.hl;
}
/* <<< factory PrintPracticeDuelNumberedInstruction */

/* >>> factory PrintNextPracticeDuelInstruction */
static void adapt_PrintNextPracticeDuelInstruction(ProbeState *s)
{
	(void)s;
	PrintNextPracticeDuelInstruction();
}
/* <<< factory PrintNextPracticeDuelInstruction */

/* >>> factory GoToFirstOrNextCardPage */
static void adapt_GoToFirstOrNextCardPage(ProbeState *s)
{
	CardPageNavigationResult r = GoToFirstOrNextCardPage();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
}
/* <<< factory GoToFirstOrNextCardPage */

/* >>> factory PrintPracticeDuelInstructions */
static void adapt_PrintPracticeDuelInstructions(ProbeState *s)
{
	PrintPracticeDuelInstructions(s->hl);
}
/* <<< factory PrintPracticeDuelInstructions */

/* >>> factory DisplayPreviousCardPage */
static void adapt_DisplayPreviousCardPage(ProbeState *s)
{
	DisplayPreviousCardPage();
	(void)s;
}
/* <<< factory DisplayPreviousCardPage */

/* >>> factory PrintNumberOfHandAndDeckCards */
static void adapt_PrintNumberOfHandAndDeckCards(ProbeState *s)
{
	(void)s;
	PrintNumberOfHandAndDeckCards();
}
/* <<< factory PrintNumberOfHandAndDeckCards */

/* >>> factory PrintReturnCardsToDeckDrawAgain */
static void adapt_PrintReturnCardsToDeckDrawAgain(ProbeState *s)
{
	PrintReturnCardsToDeckDrawAgainResult r = PrintReturnCardsToDeckDrawAgain();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory PrintReturnCardsToDeckDrawAgain */

/* >>> factory PracticeDuelVerify_Turn3 */
static void adapt_PracticeDuelVerify_Turn3(ProbeState *s)
{
	PracticeDuelVerifyTurn3Result r = PracticeDuelVerify_Turn3();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PracticeDuelVerify_Turn3 */

/* >>> factory CheckIfEnoughEnergiesToAttack */
static void adapt_CheckIfEnoughEnergiesToAttack(ProbeState *s)
{
	CheckIfEnoughEnergiesToAttackResult r = CheckIfEnoughEnergiesToAttack();
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory CheckIfEnoughEnergiesToAttack */

/* >>> factory PlayTurnDuelistDrawAnimation */
static void adapt_PlayTurnDuelistDrawAnimation(ProbeState *s)
{
	PlayTurnDuelistDrawAnimationResult r = PlayTurnDuelistDrawAnimation(s->f, s->b, s->c, s->d, s->hl);
	s->e = r.e;
	s->f = r.f;
}
/* <<< factory PlayTurnDuelistDrawAnimation */

/* >>> factory DrawCardPageSet2AndRarityIcons */
static void adapt_DrawCardPageSet2AndRarityIcons(ProbeState *s)
{
	DrawCardPageSet2AndRarityIconsResult r = DrawCardPageSet2AndRarityIcons();
	s->hl = r.hl;
}
/* <<< factory DrawCardPageSet2AndRarityIcons */

/* >>> factory CountOppEnergyCardsInHandAndAttached */
static void adapt_CountOppEnergyCardsInHandAndAttached(ProbeState *s)
{
	CountOppEnergyCardsInHandAndAttachedResult r = CountOppEnergyCardsInHandAndAttached();
	s->a = r.a; s->f = r.f; s->hl = r.hl;
}
/* <<< factory CountOppEnergyCardsInHandAndAttached */

/* >>> factory AIPickPrizeCards */
static void adapt_AIPickPrizeCards(ProbeState *s)
{
	AIPickPrizeCards();
	(void)s;
}
/* <<< factory AIPickPrizeCards */

/* >>> factory HandleAIEnergyScoringForRepeatedBenchPokemon */
static void adapt_HandleAIEnergyScoringForRepeatedBenchPokemon(ProbeState *s)
{
	HandleAIEnergyScoringForRepeatedBenchPokemonResult r = HandleAIEnergyScoringForRepeatedBenchPokemon();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleAIEnergyScoringForRepeatedBenchPokemon */

/* >>> factory CheckPrintCnfSlpPrz */
static void adapt_CheckPrintCnfSlpPrz(ProbeState *s)
{
	CheckPrintCnfSlpPrz(s->a, s->b, s->c);
}
/* <<< factory CheckPrintCnfSlpPrz */

/* >>> factory LoadAnimCoordsAndFlags */
static void adapt_LoadAnimCoordsAndFlags(ProbeState *s)
{
	(void)s;
	LoadAnimCoordsAndFlags();
}
/* <<< factory LoadAnimCoordsAndFlags */

/* >>> factory PrintUsedTrainerCardDescription */
static void adapt_PrintUsedTrainerCardDescription(ProbeState *s)
{
	(void)s;
	PrintUsedTrainerCardDescription();
}
/* <<< factory PrintUsedTrainerCardDescription */

/* >>> factory PracticeDuelVerify_Turn5 */
static void adapt_PracticeDuelVerify_Turn5(ProbeState *s)
{
	(void)s;
	PracticeDuelVerifyTurn5Result r = PracticeDuelVerify_Turn5();
	s->f = r.f;
}
/* <<< factory PracticeDuelVerify_Turn5 */

/* >>> factory PracticeDuelVerify_Turn1 */
static void adapt_PracticeDuelVerify_Turn1(ProbeState *s)
{
	s->f = PracticeDuelVerify_Turn1().f;
}
/* <<< factory PracticeDuelVerify_Turn1 */

/* >>> factory PracticeDuelVerify_Turn2 */
static void adapt_PracticeDuelVerify_Turn2(ProbeState *s)
{
	s->f = PracticeDuelVerify_Turn2().f;
}
/* <<< factory PracticeDuelVerify_Turn2 */

/* >>> factory PracticeDuel_PlayStaryuFromBench */
static void adapt_PracticeDuel_PlayStaryuFromBench(ProbeState *s)
{
	PracticeDuel_PlayStaryuFromBenchResult r = PracticeDuel_PlayStaryuFromBench();
	s->f = r.f;
}
/* <<< factory PracticeDuel_PlayStaryuFromBench */

/* >>> factory DisplayDuelistTurnScreen */
static void adapt_DisplayDuelistTurnScreen(ProbeState *s)
{
	(void)s;
	DisplayDuelistTurnScreen();
}
/* <<< factory DisplayDuelistTurnScreen */

/* >>> factory DrawDuelistPortraitsAndNames */
static void adapt_DrawDuelistPortraitsAndNames(ProbeState *s)
{
	(void)s;
	DrawDuelistPortraitsAndNames();
}
/* <<< factory DrawDuelistPortraitsAndNames */

/* >>> factory CheckEnergyNeededForAttack */
static void adapt_CheckEnergyNeededForAttack(ProbeState *s)
{
	CheckEnergyNeededForAttackResult r = CheckEnergyNeededForAttack();
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory CheckEnergyNeededForAttack */

/* >>> factory CreateDamageCharSprite */
static void adapt_CreateDamageCharSprite(ProbeState *s)
{
	CreateDamageCharSprite(s->a, s->f, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory CreateDamageCharSprite */

/* >>> factory HasAlivePokemonInBench */
static void adapt_HasAlivePokemonInBench(ProbeState *s)
{
	HasAlivePokemonInPlayAreaResult r = HasAlivePokemonInBench();
	s->a = r.a; s->f = r.f;
}
/* <<< factory HasAlivePokemonInBench */

/* >>> factory DrawOpponentSelectionScreen */
static void adapt_DrawOpponentSelectionScreen(ProbeState *s)
{
	DrawOpponentSelectionScreen(s->f, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory DrawOpponentSelectionScreen */

/* >>> factory PracticeDuel_ReplaceKnockedOutPokemon */
static void adapt_PracticeDuel_ReplaceKnockedOutPokemon(ProbeState *s)
{
	(void)s;
	PracticeDuel_ReplaceKnockedOutPokemon();
}
/* <<< factory PracticeDuel_ReplaceKnockedOutPokemon */

/* >>> factory DrawDamageAnimationArrow */
static void adapt_DrawDamageAnimationArrow(ProbeState *s)
{
	DrawDamageAnimationArrow(s->f);
}
/* <<< factory DrawDamageAnimationArrow */

/* >>> factory DrawDamageAnimationWeak */
static void adapt_DrawDamageAnimationWeak(ProbeState *s)
{
	DrawDamageAnimationWeak();
}
/* <<< factory DrawDamageAnimationWeak */

/* >>> factory DrawDamageAnimationResist */
static void adapt_DrawDamageAnimationResist(ProbeState *s)
{
	DrawDamageAnimationResist();
}
/* <<< factory DrawDamageAnimationResist */

/* >>> factory DrawDamageAnimationNumbers */
static void adapt_DrawDamageAnimationNumbers(ProbeState *s)
{
	DrawDamageAnimationNumbers();
}
/* <<< factory DrawDamageAnimationNumbers */

/* >>> factory Func_15886 */
static void adapt_Func_15886(ProbeState *s)
{
	CoreCardListResult r = Func_15886(s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_15886 */

/* >>> factory CheckAbleToRetreat */
static void adapt_CheckAbleToRetreat(ProbeState *s)
{
	CheckAbleToRetreatResult r = CheckAbleToRetreat();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckAbleToRetreat */

/* >>> factory LookForEnergyNeededInHand */
static void adapt_LookForEnergyNeededInHand(ProbeState *s)
{
	uint8_t r = LookForEnergyNeededInHand();
	s->f = r;
}
/* <<< factory LookForEnergyNeededInHand */

/* >>> factory Func_7364 */
static void adapt_Func_7364(ProbeState *s)
{
	Func_7364Result r = Func_7364();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_7364 */

/* >>> factory CheckEnergyNeededForAttackAfterDiscard */
static void adapt_CheckEnergyNeededForAttackAfterDiscard(ProbeState *s)
{
	CheckEnergyNeededForAttackAfterDiscardResult r = CheckEnergyNeededForAttackAfterDiscard();
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
}
/* <<< factory CheckEnergyNeededForAttackAfterDiscard */

/* >>> factory DisplayFirstOrNextCardPage */
static void adapt_DisplayFirstOrNextCardPage(ProbeState *s)
{
	CardPageNavigationResult r = DisplayFirstOrNextCardPage(s->b);
	s->a = r.a; s->f = r.f; s->b = r.b;
}
/* <<< factory DisplayFirstOrNextCardPage */

/* >>> factory PrintAttackOrCardDescription */
static void adapt_PrintAttackOrCardDescription(ProbeState *s)
{
	PrintAttackOrCardDescriptionResult r = PrintAttackOrCardDescription(s->hl, s->d, s->e);
	s->a = r.a; s->hl = r.hl;
}
/* <<< factory PrintAttackOrCardDescription */

/* >>> factory PrintAttackOrPkmnPowerInformation */
static void adapt_PrintAttackOrPkmnPowerInformation(ProbeState *s)
{
	PrintAttackOrPkmnPowerInformationResult r = PrintAttackOrPkmnPowerInformation(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->f = r.f; s->hl = r.hl;
}
/* <<< factory PrintAttackOrPkmnPowerInformation */

/* >>> factory PrintAttackOrNonPokemonCardDescription */
static void adapt_PrintAttackOrNonPokemonCardDescription(ProbeState *s)
{
	PrintAttackOrCardDescriptionResult r = PrintAttackOrNonPokemonCardDescription(s->hl, s->d, s->e);
	s->a = r.a; s->f = r.f; s->hl = r.hl;
}
/* <<< factory PrintAttackOrNonPokemonCardDescription */

/* >>> factory DisplayCardPageOnLeftOrRightPressed */
static void adapt_DisplayCardPageOnLeftOrRightPressed(ProbeState *s)
{
	DisplayCardPageOnLeftOrRightPressed(s->a);
}
/* <<< factory DisplayCardPageOnLeftOrRightPressed */

/* >>> factory PrintPlayAreaCardHeader */
static void adapt_PrintPlayAreaCardHeader(ProbeState *s)
{
	(void)s;
	PrintPlayAreaCardHeader();
}
/* <<< factory PrintPlayAreaCardHeader */

/* >>> factory PrintPokemonCardLength */
static void adapt_PrintPokemonCardLength(ProbeState *s)
{
	PrintPokemonCardLength(s->hl, s->b, s->c);
}
/* <<< factory PrintPokemonCardLength */

/* >>> factory PlayDeckShuffleAnimation */
static void adapt_PlayDeckShuffleAnimation(ProbeState *s)
{
	s->a = PlayDeckShuffleAnimation();
}
/* <<< factory PlayDeckShuffleAnimation */

/* >>> factory OppAction_6b30 */
static void adapt_OppAction_6b30(ProbeState *s)
{
	s->a = OppAction_6b30();
}
/* <<< factory OppAction_6b30 */

/* >>> factory PrintPlayAreaCardInformation */
static void adapt_PrintPlayAreaCardInformation(ProbeState *s)
{
	PrintPlayAreaCardInformationResult r = PrintPlayAreaCardInformation();
	s->hl = r.hl;
}
/* <<< factory PrintPlayAreaCardInformation */

/* >>> factory PrintPlayAreaCardInformationAndLocation */
static void adapt_PrintPlayAreaCardInformationAndLocation(ProbeState *s)
{
	(void)s;
	PrintPlayAreaCardInformationAndLocation();
}
/* <<< factory PrintPlayAreaCardInformationAndLocation */

/* >>> factory DisplayUsePokemonPowerScreen */
static void adapt_DisplayUsePokemonPowerScreen(ProbeState *s)
{
	(void)s;
	DisplayUsePokemonPowerScreen();
}
/* <<< factory DisplayUsePokemonPowerScreen */

/* >>> factory InitAndPrintPlayAreaCardInformationAndLocation */
static void adapt_InitAndPrintPlayAreaCardInformationAndLocation(ProbeState *s)
{
	(void)s;
	InitAndPrintPlayAreaCardInformationAndLocation();
}
/* <<< factory InitAndPrintPlayAreaCardInformationAndLocation */

/* >>> factory InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox */
static void adapt_InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox(ProbeState *s)
{
	(void)s;
	InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox();
}
/* <<< factory InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox */

/* >>> factory PrintPlayAreaCardList */
static void adapt_PrintPlayAreaCardList(ProbeState *s)
{
	(void)s;
	PrintPlayAreaCardList();
}
/* <<< factory PrintPlayAreaCardList */

/* >>> factory OppAction_UsePokemonPower */
static void adapt_OppAction_UsePokemonPower(ProbeState *s)
{
	(void)s;
	OppAction_UsePokemonPower();
}
/* <<< factory OppAction_UsePokemonPower */

/* >>> factory Func_616e */
static void adapt_Func_616e(ProbeState *s)
{
	Func_616e(s->a);
}
/* <<< factory Func_616e */

/* >>> factory PrintPlayAreaCardList_EnableLCD */
static void adapt_PrintPlayAreaCardList_EnableLCD(ProbeState *s)
{
	s->a = PrintPlayAreaCardList_EnableLCD().a;
}
/* <<< factory PrintPlayAreaCardList_EnableLCD */

/* >>> factory FlushAllPalettesOrSendPal23Packet */
static void adapt_FlushAllPalettesOrSendPal23Packet(ProbeState *s)
{
	FlushAllPalettesOrSendPal23Packet();
}
/* <<< factory FlushAllPalettesOrSendPal23Packet */

/* >>> factory CheckIfCardCanBePlayed */
static void adapt_CheckIfCardCanBePlayed(ProbeState *s)
{
	CheckIfCardCanBePlayedResult r = CheckIfCardCanBePlayed(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfCardCanBePlayed */

/* >>> factory OppAction_6b15 */
static void adapt_OppAction_6b15(ProbeState *s)
{
	OppAction_6b15Result r = OppAction_6b15();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory OppAction_6b15 */

/* >>> factory OppAction_ExecutePokemonPowerEffect */
static void adapt_OppAction_ExecutePokemonPowerEffect(ProbeState *s)
{
	OppAction_ExecutePokemonPowerEffectResult r = OppAction_ExecutePokemonPowerEffect();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory OppAction_ExecutePokemonPowerEffect */

/* >>> factory LoadSelectedCardGfx */
static void adapt_LoadSelectedCardGfx(ProbeState *s)
{
	(void)s;
	LoadSelectedCardGfx();
}
/* <<< factory LoadSelectedCardGfx */

/* >>> factory AIProcessHandTrainerCards */
static void adapt_AIProcessHandTrainerCards(ProbeState *s)
{
	AIProcessHandTrainerCardsWrapResult r = AIProcessHandTrainerCards(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIProcessHandTrainerCards */

/* >>> factory CardListFunction */
static void adapt_CardListFunction(ProbeState *s)
{
	CardListFunctionResult r = CardListFunction();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CardListFunction */

/* >>> factory CheckIfSelectedAttackIsUnusable */
static void adapt_CheckIfSelectedAttackIsUnusable(ProbeState *s)
{
	CheckIfSelectedAttackIsUnusableResult r = CheckIfSelectedAttackIsUnusable(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CheckIfSelectedAttackIsUnusable */

/* >>> factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
static void adapt_CheckForBenchIDAtHalfHPAndCanUseSecondAttack(ProbeState *s)
{
	CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult r = CheckForBenchIDAtHalfHPAndCanUseSecondAttack(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */

/* >>> factory CountNumberOfSetUpBenchPokemon */
static void adapt_CountNumberOfSetUpBenchPokemon(ProbeState *s)
{
	CountNumberOfSetUpBenchPokemonResult r = CountNumberOfSetUpBenchPokemon(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory CountNumberOfSetUpBenchPokemon */

/* >>> factory HandleLegendaryArticunoEnergyScoring */
static void adapt_HandleLegendaryArticunoEnergyScoring(ProbeState *s)
{
	(void)s;
	HandleLegendaryArticunoEnergyScoring();
}
/* <<< factory HandleLegendaryArticunoEnergyScoring */

/* >>> factory CheckIfArenaCardIsFullyPowered */
static void adapt_CheckIfArenaCardIsFullyPowered(ProbeState *s)
{
	CheckIfArenaCardIsFullyPoweredResult r = CheckIfArenaCardIsFullyPowered();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfArenaCardIsFullyPowered */

/* >>> factory SendCardAttrBlkPacket */
static void adapt_SendCardAttrBlkPacket(ProbeState *s)
{
	SendCardAttrBlkPacketResult r = SendCardAttrBlkPacket(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory SendCardAttrBlkPacket */

/* >>> factory ApplyBGP6OrSGB3ToCardImage */
static void adapt_ApplyBGP6OrSGB3ToCardImage(ProbeState *s)
{
	SendCardAttrBlkPacketResult r = ApplyBGP6OrSGB3ToCardImage(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ApplyBGP6OrSGB3ToCardImage */

/* >>> factory DrawLargePictureOfCard */
static void adapt_DrawLargePictureOfCard(ProbeState *s)
{
	(void)s;
	DrawLargePictureOfCard();
}
/* <<< factory DrawLargePictureOfCard */

/* >>> factory DrawCardPageSurroundingBox */
static void adapt_DrawCardPageSurroundingBox(ProbeState *s)
{
	DrawCardPageSurroundingBox();
	(void)s;
}
/* <<< factory DrawCardPageSurroundingBox */

/* >>> factory PrintPokemonCardPageGenericInformation */
static void adapt_PrintPokemonCardPageGenericInformation(ProbeState *s)
{
	PrintPokemonCardPageGenericInformationResult r = PrintPokemonCardPageGenericInformation();
	s->hl = r.hl;
}
/* <<< factory PrintPokemonCardPageGenericInformation */

/* >>> factory DrawDuelHUD */
static void adapt_DrawDuelHUD(ProbeState *s)
{
	DrawDuelHUD(s->b, s->c, s->d, s->e);
}
/* <<< factory DrawDuelHUD */

/* >>> factory DrawDuelHUDs */
static void adapt_DrawDuelHUDs(ProbeState *s)
{
	(void)s;
	DrawDuelHUDs();
}
/* <<< factory DrawDuelHUDs */

/* >>> factory DrawCardListScreenLayout */
static void adapt_DrawCardListScreenLayout(ProbeState *s)
{
	DrawCardListScreenLayoutResult r = DrawCardListScreenLayout();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DrawCardListScreenLayout */

/* >>> factory ApplyBGP7OrSGB2ToCardImage */
static void adapt_ApplyBGP7OrSGB2ToCardImage(ProbeState *s)
{
	SendCardAttrBlkPacketResult r = ApplyBGP7OrSGB2ToCardImage(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ApplyBGP7OrSGB2ToCardImage */

/* >>> factory DisplayPracticeDuelPlayerHandScreen */
static void adapt_DisplayPracticeDuelPlayerHandScreen(ProbeState *s)
{
	(void)s;
	DisplayPracticeDuelPlayerHandScreen();
}
/* <<< factory DisplayPracticeDuelPlayerHandScreen */

/* >>> factory DrawDuelMainScene */
static void adapt_DrawDuelMainScene(ProbeState *s)
{
	(void)s;
	DrawDuelMainScene();
}
/* <<< factory DrawDuelMainScene */

/* >>> factory InitAndDrawCardListScreenLayout */
static void adapt_InitAndDrawCardListScreenLayout(ProbeState *s)
{
	DrawCardListScreenLayoutResult r = InitAndDrawCardListScreenLayout();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory InitAndDrawCardListScreenLayout */

/* >>> factory RedrawTurnDuelistsDuelHUD */
static void adapt_RedrawTurnDuelistsDuelHUD(ProbeState *s)
{
	(void)s;
	RedrawTurnDuelistsDuelHUD();
}
/* <<< factory RedrawTurnDuelistsDuelHUD */

/* >>> factory OppAction_DrawDuelMainScene */
static void adapt_OppAction_DrawDuelMainScene(ProbeState *s)
{
	(void)s;
	OppAction_DrawDuelMainScene();
}
/* <<< factory OppAction_DrawDuelMainScene */

/* >>> factory InitAndDrawCardListScreenLayout_WithSelectCheckMenu */
static void adapt_InitAndDrawCardListScreenLayout_WithSelectCheckMenu(ProbeState *s)
{
	DrawCardListScreenLayoutResult result = InitAndDrawCardListScreenLayout_WithSelectCheckMenu();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory InitAndDrawCardListScreenLayout_WithSelectCheckMenu */

/* >>> factory DisplayCardListDetails */
static void adapt_DisplayCardListDetails(ProbeState *s)
{
	(void)s;
	DisplayCardListDetailsResult r = DisplayCardListDetails();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DisplayCardListDetails */

/* >>> factory OppAction_FinishTurnWithoutAttacking */
static void adapt_OppAction_FinishTurnWithoutAttacking(ProbeState *s)
{
	(void)s;
	OppAction_FinishTurnWithoutAttacking();
}
/* <<< factory OppAction_FinishTurnWithoutAttacking */

/* >>> factory RedrawTurnDuelistsMainSceneOrDuelHUD */
static void adapt_RedrawTurnDuelistsMainSceneOrDuelHUD(ProbeState *s)
{
	(void)s;
	RedrawTurnDuelistsMainSceneOrDuelHUD();
}
/* <<< factory RedrawTurnDuelistsMainSceneOrDuelHUD */

/* >>> factory DisplayNoBasicPokemonInHandScreen */
static void adapt_DisplayNoBasicPokemonInHandScreen(ProbeState *s)
{
	(void)s;
	DisplayNoBasicPokemonInHandScreen();
}
/* <<< factory DisplayNoBasicPokemonInHandScreen */

/* >>> factory PrintAndLoadAttacksToDuelTempList */
static void adapt_PrintAndLoadAttacksToDuelTempList(ProbeState *s)
{
	s->a = PrintAndLoadAttacksToDuelTempList();
}
/* <<< factory PrintAndLoadAttacksToDuelTempList */

/* >>> factory DisplayPokemonAttackCardPage */
static void adapt_DisplayPokemonAttackCardPage(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8 | s->e);
	DisplayPokemonAttackCardPage(s->b, s->c, s->d, de, s->hl);
}
/* <<< factory DisplayPokemonAttackCardPage */

/* >>> factory DisplayCardPage_PokemonAttack2Page2 */
static void adapt_DisplayCardPage_PokemonAttack2Page2(ProbeState *s)
{
	DisplayCardPage_PokemonAttack2Page2(s->b, s->c, s->d);
}
/* <<< factory DisplayCardPage_PokemonAttack2Page2 */

const ProbeEntry probe_entries_core[] = {
	{ "ApplyCardCGBAttributes", adapt_ApplyCardCGBAttributes },
	{ "CheckIfEnoughEnergiesToRetreat", adapt_CheckIfEnoughEnergiesToRetreat },
	{ "DecideLinkDuelVariables", adapt_DecideLinkDuelVariables },
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
	{ "Func_6ba2", adapt_Func_6ba2 },
	{ "SetLineSeparation", adapt_SetLineSeparation },
	{ "PlayAreaScreenMenuFunction", adapt_PlayAreaScreenMenuFunction },
	{ "SwitchAttackPage", adapt_SwitchAttackPage },
	{ "PrintCardListHeaderAndInfoBoxTexts", adapt_PrintCardListHeaderAndInfoBoxTexts },
	{ "DrawHPBar", adapt_DrawHPBar },
	{ "ValidateSavedDuelDataFromHL", adapt_ValidateSavedDuelDataFromHL },
	{ "CopyCGBCardPalette", adapt_CopyCGBCardPalette },
	{ "CreateCardAttrBlkPacket_DataSet", adapt_CreateCardAttrBlkPacket_DataSet },
	{ "SaveDuelDataToDE", adapt_SaveDuelDataToDE },
	{ "LoadSavedDuelDataFromDE", adapt_LoadSavedDuelDataFromDE },
	{ "SetBGP7OrSGB2ToCardPalette", adapt_SetBGP7OrSGB2ToCardPalette },
	{ "ZeroObjectPositionsAndToggleOAMCopy", adapt_ZeroObjectPositionsAndToggleOAMCopy },
	{ "LoadPlayerDeck", adapt_LoadPlayerDeck },
	{ "CheckSkipDelayAllowed", adapt_CheckSkipDelayAllowed },
	{ "AIMakeDecision", adapt_AIMakeDecision },
	{ "PrintPracticeDuelDrMasonInstructions", adapt_PrintPracticeDuelDrMasonInstructions },
	{ "PrintPracticeDuelInstructionsTextBoxLabel", adapt_PrintPracticeDuelInstructionsTextBoxLabel },
	{ "LoadLoaded1CardGfx", adapt_LoadLoaded1CardGfx },
	{ "LookForCardIDInPlayArea_Bank5", adapt_LookForCardIDInPlayArea_Bank5 },
	{ "ClearMemory_Bank5", adapt_ClearMemory_Bank5 },
	{ "SetCardListInfoBoxText", adapt_SetCardListInfoBoxText },
	{ "ReturnWrongAction", adapt_ReturnWrongAction },
	{ "CopyListWithFFTerminatorFromHLToDE_Bank5", adapt_CopyListWithFFTerminatorFromHLToDE_Bank5 },
	{ "CheckEnergyFlagsNeededInList", adapt_CheckEnergyFlagsNeededInList },
	{ "CardPageSwitch_EnergyEnd", adapt_CardPageSwitch_EnergyEnd },
	{ "CardPageSwitch_0c", adapt_CardPageSwitch_0c },
	{ "PlaceCardImageOAM", adapt_PlaceCardImageOAM },
	{ "PrintPlayAreaCardAttachedEnergies", adapt_PrintPlayAreaCardAttachedEnergies },
	{ "OppAction_DrawCard", adapt_OppAction_DrawCard },
	{ "PrintSortNumberInCardList_SetPointer", adapt_PrintSortNumberInCardList_SetPointer },
	{ "PrintSortNumberInCardList", adapt_PrintSortNumberInCardList },
	{ "PrintEnergiesOfColor", adapt_PrintEnergiesOfColor },
	{ "PrintCardPageWeaknessesOrResistances", adapt_PrintCardPageWeaknessesOrResistances },
	{ "Func_6423", adapt_Func_6423 },
	{ "InitVariablesToBeginDuel", adapt_InitVariablesToBeginDuel },
	{ "SetSGB3ToCardPalette", adapt_SetSGB3ToCardPalette },
	{ "CreateCardAttrBlkPacket", adapt_CreateCardAttrBlkPacket },
	{ "CardPageSwitch_PokemonAttack1Page2", adapt_CardPageSwitch_PokemonAttack1Page2 },
	{ "CardPageSwitch_PokemonAttack2Page1", adapt_CardPageSwitch_PokemonAttack2Page1 },
	{ "AIDiscourage", adapt_AIDiscourage },
	{ "ConvertHPToDamageCounters_Bank5", adapt_ConvertHPToDamageCounters_Bank5 },
	{ "CalculateBDividedByA_Bank5", adapt_CalculateBDividedByA_Bank5 },
	{ "JPWriteByteToBGMap0", adapt_JPWriteByteToBGMap0 },
	{ "AIPlayInitialBasicCards", adapt_AIPlayInitialBasicCards },
	{ "CheckIfEnoughParticularAttachedEnergy", adapt_CheckIfEnoughParticularAttachedEnergy },
	{ "Func_14323", adapt_Func_14323 },
	{ "CreateEnergyCardListFromHand", adapt_CreateEnergyCardListFromHand },
	{ "CalculateParticularAttachedEnergyNeeded", adapt_CalculateParticularAttachedEnergyNeeded },
	{ "GetAnimCoordsAndFlags", adapt_GetAnimCoordsAndFlags },
	{ "PlayBufferedDuelAnimations", adapt_PlayBufferedDuelAnimations },
	{ "SwitchCardPage", adapt_SwitchCardPage },
	{ "CardPageSwitch_00", adapt_CardPageSwitch_00 },
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
	{ "SetBGP6OrSGB3ToCardPalette", adapt_SetBGP6OrSGB3ToCardPalette },
	{ "PrintCardPageRarityIcon", adapt_PrintCardPageRarityIcon },
	{ "SetNoLineSeparation", adapt_SetNoLineSeparation },
	{ "SetOneLineSeparation", adapt_SetOneLineSeparation },
	{ "_HasAlivePokemonInPlayArea", adapt__HasAlivePokemonInPlayArea },
	{ "CheckPrintPoisoned", adapt_CheckPrintPoisoned },
	{ "ResetDoFrameFunction_Bank1", adapt_ResetDoFrameFunction_Bank1 },
	{ "OppAction_NoAction", adapt_OppAction_NoAction },
	{ "LookForCardIDInHand", adapt_LookForCardIDInHand },
	{ "LookForCardIDInHandList_Bank5", adapt_LookForCardIDInHandList_Bank5 },
	{ "FindHighestBenchScore", adapt_FindHighestBenchScore },
	{ "AIEncourage", adapt_AIEncourage },
	{ "IsLoadedCard1BasicPokemon", adapt_IsLoadedCard1BasicPokemon },
	{ "PracticeDuel_PlayGoldeen", adapt_PracticeDuel_PlayGoldeen },
	{ "DiscardRetreatCostCards", adapt_DiscardRetreatCostCards },
	{ "ReturnRetreatCostCardsToArena", adapt_ReturnRetreatCostCardsToArena },
	{ "TwoByteNumberToTxSymbol_PadSpace_Bank1", adapt_TwoByteNumberToTxSymbol_PadSpace_Bank1 },
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
	{ "Func_1585b", adapt_Func_1585b },
	{ "CheckIfNotABossDeckID", adapt_CheckIfNotABossDeckID },
	{ "AIChooseRandomlyNotToDoAction", adapt_AIChooseRandomlyNotToDoAction },
	{ "TrySetUpBossStartingPlayArea", adapt_TrySetUpBossStartingPlayArea },
	{ "CardPageSwitch_TrainerEnd", adapt_CardPageSwitch_TrainerEnd },
	{ "CardPageSwitch_TrainerPage2", adapt_CardPageSwitch_TrainerPage2 },
	{ "CardPageSwitch_EnergyOrTrainerPage1", adapt_CardPageSwitch_EnergyOrTrainerPage1 },
	{ "LoadAndValidateDuelSaveData", adapt_LoadAndValidateDuelSaveData },
	{ "ValidateSavedNonLinkDuelData", adapt_ValidateSavedNonLinkDuelData },
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
	{ "SetDiscardPileScreenTexts", adapt_SetDiscardPileScreenTexts },
	{ "PrintAttachedEnergyToPokemon", adapt_PrintAttachedEnergyToPokemon },
	{ "PrintPokemonEvolvedIntoPokemon", adapt_PrintPokemonEvolvedIntoPokemon },
	{ "SetupDuel", adapt_SetupDuel },
	{ "PracticeDuelVerify_Turn6", adapt_PracticeDuelVerify_Turn6 },
	{ "PracticeDuelVerify_Turn4", adapt_PracticeDuelVerify_Turn4 },
	{ "ShuffleDeckAndDrawSevenCards", adapt_ShuffleDeckAndDrawSevenCards },
	{ "WriteTwoDigitNumberInTxSymbol_PadSpace", adapt_WriteTwoDigitNumberInTxSymbol_PadSpace },
	{ "PrintOpponentNumberOfHandAndDeckCards", adapt_PrintOpponentNumberOfHandAndDeckCards },
	{ "PrintPlayerNumberOfHandAndDeckCards", adapt_PrintPlayerNumberOfHandAndDeckCards },
	{ "PrintDuelResultStats", adapt_PrintDuelResultStats },
	{ "ConvertColorToEnergyCardID", adapt_ConvertColorToEnergyCardID },
	{ "WriteOneByteNumberInTxSymbol_PadSpace", adapt_WriteOneByteNumberInTxSymbol_PadSpace },
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
	{ "DrawOpponentSelectionScreen", adapt_DrawOpponentSelectionScreen },
	{ "PracticeDuel_ReplaceKnockedOutPokemon", adapt_PracticeDuel_ReplaceKnockedOutPokemon },
	{ "DrawDamageAnimationArrow", adapt_DrawDamageAnimationArrow },
	{ "DrawDamageAnimationWeak", adapt_DrawDamageAnimationWeak },
	{ "DrawDamageAnimationResist", adapt_DrawDamageAnimationResist },
	{ "DrawDamageAnimationNumbers", adapt_DrawDamageAnimationNumbers },
	{ "Func_15886", adapt_Func_15886 },
	{ "CheckAbleToRetreat", adapt_CheckAbleToRetreat },
	{ "LookForEnergyNeededInHand", adapt_LookForEnergyNeededInHand },
	{ "Func_7364", adapt_Func_7364 },
	{ "CheckEnergyNeededForAttackAfterDiscard", adapt_CheckEnergyNeededForAttackAfterDiscard },
	{ "DisplayFirstOrNextCardPage", adapt_DisplayFirstOrNextCardPage },
	{ "PrintAttackOrCardDescription", adapt_PrintAttackOrCardDescription },
	{ "PrintAttackOrPkmnPowerInformation", adapt_PrintAttackOrPkmnPowerInformation },
	{ "PrintAttackOrNonPokemonCardDescription", adapt_PrintAttackOrNonPokemonCardDescription },
	{ "DisplayCardPageOnLeftOrRightPressed", adapt_DisplayCardPageOnLeftOrRightPressed },
	{ "PrintPlayAreaCardHeader", adapt_PrintPlayAreaCardHeader },
	{ "PrintPokemonCardLength", adapt_PrintPokemonCardLength },
	{ "PlayDeckShuffleAnimation", adapt_PlayDeckShuffleAnimation },
	{ "OppAction_6b30", adapt_OppAction_6b30 },
	{ "PrintPlayAreaCardInformation", adapt_PrintPlayAreaCardInformation },
	{ "PrintPlayAreaCardInformationAndLocation", adapt_PrintPlayAreaCardInformationAndLocation },
	{ "DisplayUsePokemonPowerScreen", adapt_DisplayUsePokemonPowerScreen },
	{ "InitAndPrintPlayAreaCardInformationAndLocation", adapt_InitAndPrintPlayAreaCardInformationAndLocation },
	{ "InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox", adapt_InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox },
	{ "PrintPlayAreaCardList", adapt_PrintPlayAreaCardList },
	{ "OppAction_UsePokemonPower", adapt_OppAction_UsePokemonPower },
	{ "Func_616e", adapt_Func_616e },
	{ "PrintPlayAreaCardList_EnableLCD", adapt_PrintPlayAreaCardList_EnableLCD },
	{ "FlushAllPalettesOrSendPal23Packet", adapt_FlushAllPalettesOrSendPal23Packet },
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
	{ "SendCardAttrBlkPacket", adapt_SendCardAttrBlkPacket },
	{ "ApplyBGP6OrSGB3ToCardImage", adapt_ApplyBGP6OrSGB3ToCardImage },
	{ "DrawLargePictureOfCard", adapt_DrawLargePictureOfCard },
	{ "DrawCardPageSurroundingBox", adapt_DrawCardPageSurroundingBox },
	{ "PrintPokemonCardPageGenericInformation", adapt_PrintPokemonCardPageGenericInformation },
	{ "DrawDuelHUD", adapt_DrawDuelHUD },
	{ "DrawDuelHUDs", adapt_DrawDuelHUDs },
	{ "DrawCardListScreenLayout", adapt_DrawCardListScreenLayout },
	{ "ApplyBGP7OrSGB2ToCardImage", adapt_ApplyBGP7OrSGB2ToCardImage },
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
	{ NULL, NULL },
};
