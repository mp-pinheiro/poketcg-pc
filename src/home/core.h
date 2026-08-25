#ifndef POKETCG_HOME_CORE_H
#define POKETCG_HOME_CORE_H

#include <stdint.h>

/* >>> factory DrawHPBar */
void DrawHPBar(uint8_t d, uint8_t e);
/* <<< factory DrawHPBar */
/* >>> factory ValidateSavedDuelDataFromHL */
typedef struct { uint8_t f; uint16_t hl; } ValidateSavedDuelDataResult;
ValidateSavedDuelDataResult ValidateSavedDuelDataFromHL(uint16_t hl);
/* <<< factory ValidateSavedDuelDataFromHL */
/* >>> factory SetLineSeparation */
void SetLineSeparation(uint8_t a);
/* <<< factory SetLineSeparation */
/* >>> factory PlayAreaScreenMenuFunction */
uint8_t PlayAreaScreenMenuFunction(void);
/* <<< factory PlayAreaScreenMenuFunction */
/* >>> factory SwitchAttackPage */
void SwitchAttackPage(void);
/* <<< factory SwitchAttackPage */
/* >>> factory CopyCGBCardPalette */
void CopyCGBCardPalette(uint8_t a);
/* <<< factory CopyCGBCardPalette */
/* >>> factory CreateCardAttrBlkPacket_DataSet */
uint16_t CreateCardAttrBlkPacket_DataSet(uint16_t hl, uint8_t a, uint8_t d, uint8_t e);
/* <<< factory CreateCardAttrBlkPacket_DataSet */
/* >>> factory SaveDuelDataToDE */
void SaveDuelDataToDE(uint16_t de);
/* <<< factory SaveDuelDataToDE */
/* >>> factory LoadSavedDuelDataFromDE */
void LoadSavedDuelDataFromDE(uint16_t de);
/* <<< factory LoadSavedDuelDataFromDE */
/* >>> factory SetBGP7OrSGB2ToCardPalette */
void SetBGP7OrSGB2ToCardPalette(void);
/* <<< factory SetBGP7OrSGB2ToCardPalette */
/* >>> factory JPWriteByteToBGMap0 */
void JPWriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory JPWriteByteToBGMap0 */
/* >>> factory ZeroObjectPositionsAndToggleOAMCopy */
void ZeroObjectPositionsAndToggleOAMCopy(void);
/* <<< factory ZeroObjectPositionsAndToggleOAMCopy */
/* >>> factory LoadPlayerDeck */
void LoadPlayerDeck(void);
/* <<< factory LoadPlayerDeck */
/* >>> factory CheckSkipDelayAllowed */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} CheckSkipDelayAllowedResult;
CheckSkipDelayAllowedResult CheckSkipDelayAllowed(uint8_t f, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CheckSkipDelayAllowed */
/* >>> factory AIMakeDecision */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
} AIMakeDecisionResult;
AIMakeDecisionResult AIMakeDecision(uint8_t a);
/* <<< factory AIMakeDecision */
/* >>> factory PrintPracticeDuelDrMasonInstructions */
void PrintPracticeDuelDrMasonInstructions(uint16_t hl);
/* <<< factory PrintPracticeDuelDrMasonInstructions */
/* >>> factory PrintPracticeDuelInstructionsTextBoxLabel */
void PrintPracticeDuelInstructionsTextBoxLabel(void);
/* <<< factory PrintPracticeDuelInstructionsTextBoxLabel */
/* >>> factory SwitchCardPage */
typedef struct { uint8_t a; uint8_t carry; } CardPageResult;
CardPageResult SwitchCardPage(uint8_t a);
/* <<< factory SwitchCardPage */
/* >>> factory CardPageSwitch_00 */
CardPageResult CardPageSwitch_00(void);
/* <<< factory CardPageSwitch_00 */
/* >>> factory LoadLoaded1CardGfx */
void LoadLoaded1CardGfx(uint16_t de);
/* <<< factory LoadLoaded1CardGfx */
/* >>> factory SetSGB3ToCardPalette */
void SetSGB3ToCardPalette(void);
/* <<< factory SetSGB3ToCardPalette */
/* >>> factory LookForCardIDInPlayArea_Bank5 */
typedef struct { uint8_t a; uint8_t b; uint8_t f; } LookResult;
LookResult LookForCardIDInPlayArea_Bank5(uint8_t a, uint8_t b);
/* <<< factory LookForCardIDInPlayArea_Bank5 */
/* >>> factory ClearMemory_Bank5 */
void ClearMemory_Bank5(uint8_t a, uint16_t hl);
/* <<< factory ClearMemory_Bank5 */
/* >>> factory CheckCardPageExists */
typedef struct { uint8_t a; uint8_t zero; } CardPageExistsResult;
CardPageExistsResult CheckCardPageExists(uint16_t *hl);
/* <<< factory CheckCardPageExists */
/* >>> factory CardPageSwitch_PokemonEnd */
CardPageResult CardPageSwitch_PokemonEnd(void);
/* <<< factory CardPageSwitch_PokemonEnd */
/* >>> factory SetCardListInfoBoxText */
void SetCardListInfoBoxText(uint16_t hl);
/* <<< factory SetCardListInfoBoxText */
/* >>> factory ReturnWrongAction */
uint8_t ReturnWrongAction(uint8_t f);
/* <<< factory ReturnWrongAction */
/* >>> factory CopyListWithFFTerminatorFromHLToDE_Bank5 */
typedef struct { uint8_t a; uint8_t f; } CopyListResult;
CopyListResult CopyListWithFFTerminatorFromHLToDE_Bank5(uint16_t *hl, uint16_t *de);
/* <<< factory CopyListWithFFTerminatorFromHLToDE_Bank5 */
/* >>> factory PrintCardListHeaderAndInfoBoxTexts */
void PrintCardListHeaderAndInfoBoxTexts(void);
/* <<< factory PrintCardListHeaderAndInfoBoxTexts */
/* >>> factory LoadCardNameToTxRam2 */
void LoadCardNameToTxRam2(uint8_t a);
/* <<< factory LoadCardNameToTxRam2 */
/* >>> factory LoadCardNameToTxRam2_b */
uint8_t LoadCardNameToTxRam2_b(uint8_t a);
/* <<< factory LoadCardNameToTxRam2_b */
/* >>> factory GetAnimCoordsAndFlags */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; } AnimCoordsResult;
AnimCoordsResult GetAnimCoordsAndFlags(void);
/* <<< factory GetAnimCoordsAndFlags */
/* >>> factory PlayBufferedDuelAnimations */
typedef struct { uint8_t a; uint8_t f; } AnimBufferResult;
AnimBufferResult PlayBufferedDuelAnimations(void);
/* <<< factory PlayBufferedDuelAnimations */
/* >>> factory CheckEnergyFlagsNeededInList */
typedef struct { uint8_t a; uint8_t carry; } EnergyFlagsResult;
EnergyFlagsResult CheckEnergyFlagsNeededInList(uint8_t a);
/* <<< factory CheckEnergyFlagsNeededInList */
/* >>> factory CardPageSwitch_EnergyEnd */
CardPageResult CardPageSwitch_EnergyEnd(void);
/* <<< factory CardPageSwitch_EnergyEnd */
/* >>> factory CardPageSwitch_0c */
CardPageResult CardPageSwitch_0c(void);
/* <<< factory CardPageSwitch_0c */
/* >>> factory PlaceCardImageOAM */
uint8_t PlaceCardImageOAM(uint16_t *hl, uint16_t *de);
/* <<< factory PlaceCardImageOAM */
/* >>> factory PrintPlayAreaCardAttachedEnergies */
void PrintPlayAreaCardAttachedEnergies(uint8_t b, uint8_t c, uint8_t e);
/* <<< factory PrintPlayAreaCardAttachedEnergies */
/* >>> factory DiscardRetreatCostCards */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} DiscardRetreatCostCardsResult;

DiscardRetreatCostCardsResult DiscardRetreatCostCards(void);
/* <<< factory DiscardRetreatCostCards */
/* >>> factory OppAction_DrawCard */
typedef struct { uint8_t a; uint8_t f; } OppActionDrawResult;
OppActionDrawResult OppAction_DrawCard(void);
/* <<< factory OppAction_DrawCard */
/* >>> factory PrintSortNumberInCardList_SetPointer */
void PrintSortNumberInCardList_SetPointer(void);
/* <<< factory PrintSortNumberInCardList_SetPointer */
/* >>> factory PrintSortNumberInCardList */
void PrintSortNumberInCardList(void);
/* <<< factory PrintSortNumberInCardList */
/* >>> factory PrintEnergiesOfColor */
typedef struct { uint8_t a; uint8_t b; uint8_t e; } PrintEnergiesResult;
PrintEnergiesResult PrintEnergiesOfColor(uint8_t a, uint8_t b, uint8_t c, uint8_t e);
/* <<< factory PrintEnergiesOfColor */
/* >>> factory PrintCardPageWeaknessesOrResistances */
void PrintCardPageWeaknessesOrResistances(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory PrintCardPageWeaknessesOrResistances */
/* >>> factory Func_6423 */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint16_t hl;
} Func6423Result;
Func6423Result Func_6423(uint8_t b, uint8_t c);
/* <<< factory Func_6423 */
/* >>> factory InitVariablesToBeginDuel */
void InitVariablesToBeginDuel(void);
/* <<< factory InitVariablesToBeginDuel */
/* >>> factory CreateCardAttrBlkPacket */
uint16_t CreateCardAttrBlkPacket(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory CreateCardAttrBlkPacket */
/* >>> factory CardPageSwitch_PokemonAttack1Page2 */
CardPageExistsResult CardPageSwitch_PokemonAttack1Page2(uint16_t *hl);
/* <<< factory CardPageSwitch_PokemonAttack1Page2 */
/* >>> factory CardPageSwitch_PokemonAttack2Page1 */
CardPageExistsResult CardPageSwitch_PokemonAttack2Page1(void);
/* <<< factory CardPageSwitch_PokemonAttack2Page1 */
/* >>> factory AIDiscourage */
void AIDiscourage(uint8_t a);
/* <<< factory AIDiscourage */
/* >>> factory ConvertHPToDamageCounters_Bank5 */
typedef struct {
	uint8_t a;
	uint8_t f;
} ConvertHPToDamageCountersResult;

ConvertHPToDamageCountersResult ConvertHPToDamageCounters_Bank5(uint8_t a);
/* <<< factory ConvertHPToDamageCounters_Bank5 */
/* >>> factory CalculateBDividedByA_Bank5 */
typedef struct { uint8_t a; uint8_t f; } CalculateBDividedByAResult;
CalculateBDividedByAResult CalculateBDividedByA_Bank5(uint8_t a, uint8_t b);
/* <<< factory CalculateBDividedByA_Bank5 */
/* >>> factory PrintCardPageRarityIcon */
#include "home/print_text.h"
ProcessTextHeaderResult PrintCardPageRarityIcon(uint8_t a, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintCardPageRarityIcon */
/* >>> factory SetNoLineSeparation */
uint8_t SetNoLineSeparation(void);
/* <<< factory SetNoLineSeparation */
/* >>> factory AIPlayInitialBasicCards */
typedef struct { uint8_t a; uint8_t f; } AIPlayInitialBasicCardsResult;
AIPlayInitialBasicCardsResult AIPlayInitialBasicCards(void);
/* <<< factory AIPlayInitialBasicCards */
/* >>> factory CheckIfEnoughParticularAttachedEnergy */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint16_t hl;
} CheckIfEnoughParticularAttachedEnergyResult;
CheckIfEnoughParticularAttachedEnergyResult CheckIfEnoughParticularAttachedEnergy(uint8_t a, uint16_t hl, uint8_t b);
/* <<< factory CheckIfEnoughParticularAttachedEnergy */
/* >>> factory Func_14323 */
typedef struct { uint8_t f; } Func14323Result;
Func14323Result Func_14323(void);
/* <<< factory Func_14323 */
/* >>> factory CreateEnergyCardListFromHand */
typedef struct { uint8_t a; uint8_t f; } CoreCardListResult;
CoreCardListResult CreateEnergyCardListFromHand(uint8_t a);
/* <<< factory CreateEnergyCardListFromHand */
/* >>> factory LookForCardIDInHand */
CoreCardListResult LookForCardIDInHand(uint8_t a);
/* <<< factory LookForCardIDInHand */
/* >>> factory LookForCardIDInHandList_Bank5 */
CoreCardListResult LookForCardIDInHandList_Bank5(uint8_t a);
/* <<< factory LookForCardIDInHandList_Bank5 */
/* >>> factory CheckForEvolutionInDeck */
typedef struct { uint8_t a; uint8_t f; } CheckForEvolutionInDeckResult;
CheckForEvolutionInDeckResult CheckForEvolutionInDeck(uint8_t a, uint8_t f);
/* <<< factory CheckForEvolutionInDeck */
/* >>> factory LookForCardThatIsKnockedOutOnDevolution */
typedef struct { uint8_t a; uint8_t f; } LookForCardThatIsKnockedOutOnDevolutionResult;
LookForCardThatIsKnockedOutOnDevolutionResult LookForCardThatIsKnockedOutOnDevolution(uint8_t f);
/* <<< factory LookForCardThatIsKnockedOutOnDevolution */
/* >>> factory CalculateParticularAttachedEnergyNeeded */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint16_t hl; } CalculateParticularAttachedEnergyNeededResult;
CalculateParticularAttachedEnergyNeededResult CalculateParticularAttachedEnergyNeeded(uint8_t a, uint8_t b, uint16_t hl);
/* <<< factory CalculateParticularAttachedEnergyNeeded */
/* >>> factory GetAnimationData */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } AnimationDataResult;
AnimationDataResult GetAnimationData(void);
/* <<< factory GetAnimationData */
/* >>> factory CardPageSwitch_PokemonOverviewOrDescription */
CardPageResult CardPageSwitch_PokemonOverviewOrDescription(void);
/* <<< factory CardPageSwitch_PokemonOverviewOrDescription */
/* >>> factory CheckCardEvolutionInHandOrDeck */
typedef struct { uint8_t a; uint8_t f; } CheckCardEvolutionInHandOrDeckResult;
CheckCardEvolutionInHandOrDeckResult CheckCardEvolutionInHandOrDeck(uint8_t a);
/* <<< factory CheckCardEvolutionInHandOrDeck */
/* >>> factory CheckIfOpponentHasBossDeckID */
typedef struct { uint8_t a; uint8_t carry; } CheckIfOpponentHasBossDeckIDResult;
CheckIfOpponentHasBossDeckIDResult CheckIfOpponentHasBossDeckID(uint8_t a);
/* <<< factory CheckIfOpponentHasBossDeckID */
/* >>> factory RaiseAIScoreToAllMatchingIDsInBench */
uint16_t RaiseAIScoreToAllMatchingIDsInBench(uint8_t a);
/* <<< factory RaiseAIScoreToAllMatchingIDsInBench */
/* >>> factory GetDamageNumberChars */
void GetDamageNumberChars(void);
/* <<< factory GetDamageNumberChars */
/* >>> factory CardPageSwitch_PokemonAttack2Page2 */
CardPageExistsResult CardPageSwitch_PokemonAttack2Page2(void);
/* >>> factory CardPageSwitch_08 */
CardPageResult CardPageSwitch_08(void);
/* <<< factory CardPageSwitch_08 */
/* >>> factory LoadPlayAreaCardGfx */
void LoadPlayAreaCardGfx(uint8_t a, uint16_t de);
/* <<< factory LoadPlayAreaCardGfx */
/* >>> factory SetBGP6OrSGB3ToCardPalette */
void SetBGP6OrSGB3ToCardPalette(void);
/* <<< factory SetBGP6OrSGB3ToCardPalette */
/* >>> factory SetOneLineSeparation */
uint8_t SetOneLineSeparation(void);
/* <<< factory SetOneLineSeparation */
/* >>> factory _HasAlivePokemonInPlayArea */
typedef struct { uint8_t a; uint8_t f; } HasAlivePokemonInPlayAreaResult;
HasAlivePokemonInPlayAreaResult _HasAlivePokemonInPlayArea(uint8_t a);
/* <<< factory _HasAlivePokemonInPlayArea */
/* >>> factory PrintPlayAreaCardLocation */
void PrintPlayAreaCardLocation(void);
/* <<< factory PrintPlayAreaCardLocation */
/* >>> factory CheckPrintPoisoned */
uint8_t CheckPrintPoisoned(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory CheckPrintPoisoned */
/* >>> factory ResetDoFrameFunction_Bank1 */
void ResetDoFrameFunction_Bank1(void);
/* <<< factory ResetDoFrameFunction_Bank1 */
/* >>> factory OppAction_NoAction */
void OppAction_NoAction(void);
/* <<< factory OppAction_NoAction */
/* >>> factory ReturnRetreatCostCardsToArena */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} ReturnRetreatCostCardsToArenaResult;
ReturnRetreatCostCardsToArenaResult ReturnRetreatCostCardsToArena(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ReturnRetreatCostCardsToArena */
/* >>> factory FindHighestBenchScore */
typedef struct { uint8_t a; uint8_t f; } FindHighestBenchScoreResult;
FindHighestBenchScoreResult FindHighestBenchScore(void);
/* <<< factory FindHighestBenchScore */
/* >>> factory AIEncourage */
typedef struct { uint8_t a; uint8_t f; } AIEncourageResult;
AIEncourageResult AIEncourage(uint8_t a);
/* <<< factory AIEncourage */
/* >>> factory IsLoadedCard1BasicPokemon */
typedef struct { uint8_t a; uint8_t f; } IsLoadedCard1BasicPokemonResult;
IsLoadedCard1BasicPokemonResult IsLoadedCard1BasicPokemon(void);
/* <<< factory IsLoadedCard1BasicPokemon */
/* >>> factory PracticeDuel_PlayGoldeen */
typedef struct { uint8_t f; } PracticeDuelPlayGoldeenResult;
PracticeDuelPlayGoldeenResult PracticeDuel_PlayGoldeen(void);
/* <<< factory PracticeDuel_PlayGoldeen */
/* >>> factory Func_6ba2 */
void Func_6ba2(uint16_t hl);
/* <<< factory Func_6ba2 */
/* >>> factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} TwoByteNumberToTxSymbolPadResult;
TwoByteNumberToTxSymbolPadResult TwoByteNumberToTxSymbol_PadSpace_Bank1(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */
/* >>> factory DrawWideTextBox_WaitForInput_Bank1 */
WaitResult DrawWideTextBox_WaitForInput_Bank1(uint16_t hl);
/* <<< factory DrawWideTextBox_WaitForInput_Bank1 */
/* >>> factory CardPageSwitch_EnergyOrTrainerPage1 */
typedef struct {
	uint8_t a;
	uint8_t f;
} CardPageSwitchEnergyResult;
CardPageSwitchEnergyResult CardPageSwitch_EnergyOrTrainerPage1(void);
/* <<< factory CardPageSwitch_EnergyOrTrainerPage1 */
/* >>> factory CardPageSwitch_TrainerEnd */
CardPageResult CardPageSwitch_TrainerEnd(void);
/* <<< factory CardPageSwitch_TrainerEnd */
/* >>> factory CheckIfEnoughEnergiesOfType */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } CheckIfEnoughEnergiesResult;
CheckIfEnoughEnergiesResult CheckIfEnoughEnergiesOfType(uint8_t a, uint16_t hl);
/* <<< factory CheckIfEnoughEnergiesOfType */
/* >>> factory CheckIfActiveCardParalyzedOrAsleep */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } CheckIfActiveStatusResult;
CheckIfActiveStatusResult CheckIfActiveCardParalyzedOrAsleep(void);
/* <<< factory CheckIfActiveCardParalyzedOrAsleep */
/* >>> factory GetAttacksEnergyCostBits */
typedef struct { uint8_t a; } EnergyCostBitsResult;
EnergyCostBitsResult GetAttacksEnergyCostBits(uint8_t a);
/* <<< factory GetAttacksEnergyCostBits */
/* >>> factory CheckForEvolutionInList */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} CheckForEvolutionInListResult;
CheckForEvolutionInListResult CheckForEvolutionInList(uint8_t a, uint8_t f);
/* <<< factory CheckForEvolutionInList */
/* >>> factory CountNumberOfEnergyCardsAttached */
typedef struct { uint8_t a; uint8_t f; } CountNumberOfEnergyCardsAttachedResult;
CountNumberOfEnergyCardsAttachedResult CountNumberOfEnergyCardsAttached(uint8_t e);
/* <<< factory CountNumberOfEnergyCardsAttached */
/* >>> factory LookForCardIDInLocation_Bank5 */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} LookForCardIDInLocationResult;
LookForCardIDInLocationResult LookForCardIDInLocation_Bank5(uint8_t location,
	uint8_t card_id);
/* <<< factory LookForCardIDInLocation_Bank5 */
/* >>> factory LoadDefendingPokemonColorWRAndPrizeCards */
void LoadDefendingPokemonColorWRAndPrizeCards(void);
/* <<< factory LoadDefendingPokemonColorWRAndPrizeCards */
/* >>> factory CheckIfEnergyIsUseful */
typedef struct { uint8_t f; } CheckIfEnergyIsUsefulResult;
CheckIfEnergyIsUsefulResult CheckIfEnergyIsUseful(uint8_t a);
/* <<< factory CheckIfEnergyIsUseful */
/* >>> factory PickRandomBenchPokemon */
uint8_t PickRandomBenchPokemon(void);
/* <<< factory PickRandomBenchPokemon */
/* >>> factory PracticeDuel_VerifyPlayerTurnActions */
typedef struct { uint8_t f; } PracticeDuelTurnActionsResult;
PracticeDuelTurnActionsResult PracticeDuel_VerifyPlayerTurnActions(void);
/* <<< factory PracticeDuel_VerifyPlayerTurnActions */
/* >>> factory PrintCardNameFromCardIDInTextBox */
void PrintCardNameFromCardIDInTextBox(uint16_t hl);
/* <<< factory PrintCardNameFromCardIDInTextBox */
/* >>> factory RemoveCardIDInList */
typedef struct { uint8_t a; uint8_t f; } RemoveCardIDResult;
RemoveCardIDResult RemoveCardIDInList(uint16_t *hl, uint8_t e);
/* <<< factory RemoveCardIDInList */
/* >>> factory SortTempHandByIDList */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} SortTempHandResult;
SortTempHandResult SortTempHandByIDList(void);
/* <<< factory SortTempHandByIDList */
/* >>> factory HandleFailedToContinueDuel */
uint8_t HandleFailedToContinueDuel(uint16_t hl);
/* <<< factory HandleFailedToContinueDuel */
/* >>> factory ApplyCardCGBAttributes */
void ApplyCardCGBAttributes(uint16_t de);
/* <<< factory ApplyCardCGBAttributes */
/* >>> factory ApplyStatusConditionToArenaPokemon */
uint8_t ApplyStatusConditionToArenaPokemon(uint16_t *hl, uint8_t d, uint8_t *e);
/* <<< factory ApplyStatusConditionToArenaPokemon */
/* >>> factory CheckIfEnoughEnergiesToRetreat */
typedef struct { uint8_t a; uint8_t f; } EnoughRetreatEnergiesResult;
EnoughRetreatEnergiesResult CheckIfEnoughEnergiesToRetreat(void);
/* <<< factory CheckIfEnoughEnergiesToRetreat */
/* >>> factory DecideLinkDuelVariables */
uint8_t DecideLinkDuelVariables(void);
/* <<< factory DecideLinkDuelVariables */
/* >>> factory DisplayAttackPage */
void DisplayAttackPage(void);
/* <<< factory DisplayAttackPage */
/* >>> factory DisplayCardPage */
void DisplayCardPage(void);
/* <<< factory DisplayCardPage */
/* >>> factory DoPracticeDuelAction */
uint8_t DoPracticeDuelAction(uint8_t a);
/* <<< factory DoPracticeDuelAction */
/* >>> factory DrawDuelHorizontalSeparator */
void DrawDuelHorizontalSeparator(void);
/* <<< factory DrawDuelHorizontalSeparator */
/* >>> factory MoveAllTurnHolderKnockedOutPokemonToDiscardPile */
void MoveAllTurnHolderKnockedOutPokemonToDiscardPile(void);
/* <<< factory MoveAllTurnHolderKnockedOutPokemonToDiscardPile */
/* >>> factory PrintSortNumberInCardList_CallFromPointer */
void PrintSortNumberInCardList_CallFromPointer(void);
/* <<< factory PrintSortNumberInCardList_CallFromPointer */
/* >>> factory PracticeDuel_VerifyInitialPlay */
typedef struct { uint8_t f; } PracticeDuelInitialPlayResult;
PracticeDuelInitialPlayResult PracticeDuel_VerifyInitialPlay(void);
/* <<< factory PracticeDuel_VerifyInitialPlay */
/* >>> factory CheckIfNoSurplusEnergyForAttack */
typedef struct { uint8_t a; uint8_t f; } CheckIfNoSurplusEnergyResult;
CheckIfNoSurplusEnergyResult CheckIfNoSurplusEnergyForAttack(void);
/* <<< factory CheckIfNoSurplusEnergyForAttack */
/* >>> factory Func_1585b */
typedef struct { uint8_t a; uint8_t f; } Func1585bResult;
Func1585bResult Func_1585b(uint16_t hl);
/* <<< factory Func_1585b */
/* >>> factory CheckIfNotABossDeckID */
typedef struct { uint8_t a; uint8_t carry; } CheckIfNotABossDeckIDResult;
CheckIfNotABossDeckIDResult CheckIfNotABossDeckID(void);
/* <<< factory CheckIfNotABossDeckID */
/* >>> factory AIChooseRandomlyNotToDoAction */
typedef struct { uint8_t a; uint8_t f; } AIChooseRandomlyNotToDoActionResult;
AIChooseRandomlyNotToDoActionResult AIChooseRandomlyNotToDoAction(void);
/* <<< factory AIChooseRandomlyNotToDoAction */
/* >>> factory TrySetUpBossStartingPlayArea */
typedef struct { uint8_t a; uint8_t f; } TrySetUpBossStartingPlayAreaResult;
TrySetUpBossStartingPlayAreaResult TrySetUpBossStartingPlayArea(void);
/* <<< factory TrySetUpBossStartingPlayArea */
/* >>> factory CardPageSwitch_TrainerPage2 */
typedef struct { uint16_t hl; uint8_t a; uint8_t zero; } TrainerPageResult;
TrainerPageResult CardPageSwitch_TrainerPage2(void);
/* <<< factory CardPageSwitch_TrainerPage2 */
/* >>> factory LoadAndValidateDuelSaveData */
uint8_t LoadAndValidateDuelSaveData(void);
/* <<< factory LoadAndValidateDuelSaveData */
/* >>> factory ValidateSavedNonLinkDuelData */
uint8_t ValidateSavedNonLinkDuelData(void);
/* <<< factory ValidateSavedNonLinkDuelData */
/* >>> factory SetupPlayAreaScreen */
void SetupPlayAreaScreen(void);
/* <<< factory SetupPlayAreaScreen */
/* >>> factory CheckIfEnoughEnergiesForGivenAttack */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CheckIfEnoughEnergiesForGivenAttackResult;

CheckIfEnoughEnergiesForGivenAttackResult CheckIfEnoughEnergiesForGivenAttack(uint8_t d, uint8_t e);
/* <<< factory CheckIfEnoughEnergiesForGivenAttack */
/* >>> factory SaveDuelData */
void SaveDuelData(void);
/* <<< factory SaveDuelData */
/* >>> factory SetCardListHeaderText */
void SetCardListHeaderText(uint16_t de, uint16_t hl);
/* <<< factory SetCardListHeaderText */
/* >>> factory AIAttachEnergyInHandToCardInPlayArea */
typedef struct { uint8_t a; uint8_t f; } AIAttachEnergyInHandToCardInPlayAreaResult;
AIAttachEnergyInHandToCardInPlayAreaResult AIAttachEnergyInHandToCardInPlayArea(uint8_t d, uint8_t e);
/* <<< factory AIAttachEnergyInHandToCardInPlayArea */
/* >>> factory GoToPreviousCardPage */
typedef struct { uint8_t a; uint8_t f; uint8_t b; } CardPageNavigationResult;
CardPageNavigationResult GoToPreviousCardPage(void);
/* <<< factory GoToPreviousCardPage */
/* >>> factory DrawWholeScreenTextBox */
void DrawWholeScreenTextBox(uint16_t hl);
/* <<< factory DrawWholeScreenTextBox */
/* >>> factory HasAlivePokemonInPlayArea */
HasAlivePokemonInPlayAreaResult HasAlivePokemonInPlayArea(void);
/* <<< factory HasAlivePokemonInPlayArea */
/* >>> factory CardPageSwitch_PokemonAttack1Page1 */
CardPageExistsResult CardPageSwitch_PokemonAttack1Page1(void);
/* <<< factory CardPageSwitch_PokemonAttack1Page1 */
/* >>> factory CheckPrintDoublePoisoned */
uint8_t CheckPrintDoublePoisoned(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory CheckPrintDoublePoisoned */
/* >>> factory PrintPracticeDuelLetsPlayTheGame */
void PrintPracticeDuelLetsPlayTheGame(void);
/* <<< factory PrintPracticeDuelLetsPlayTheGame */
/* >>> factory AIAttachEnergyInHandToCardInBench */
typedef struct { uint8_t a; uint8_t f; } AIAttachEnergyInHandToCardInBenchResult;
AIAttachEnergyInHandToCardInBenchResult AIAttachEnergyInHandToCardInBench(uint8_t d, uint8_t e);
/* <<< factory AIAttachEnergyInHandToCardInBench */
/* >>> factory DrawPracticeDuelInstructionsTextBox */
void DrawPracticeDuelInstructionsTextBox(void);
/* <<< factory DrawPracticeDuelInstructionsTextBox */
/* >>> factory PracticeDuelVerify_Turn7Or8 */
typedef struct { uint8_t f; } PracticeDuelVerifyTurn7Or8Result;
PracticeDuelVerifyTurn7Or8Result PracticeDuelVerify_Turn7Or8(void);
/* <<< factory PracticeDuelVerify_Turn7Or8 */
/* >>> factory SetDiscardPileScreenTexts */
void SetDiscardPileScreenTexts(void);
/* <<< factory SetDiscardPileScreenTexts */
/* >>> factory PrintAttachedEnergyToPokemon */
void PrintAttachedEnergyToPokemon(void);
/* <<< factory PrintAttachedEnergyToPokemon */
/* >>> factory PrintPokemonEvolvedIntoPokemon */
void PrintPokemonEvolvedIntoPokemon(void);
/* <<< factory PrintPokemonEvolvedIntoPokemon */
/* >>> factory SetupDuel */
void SetupDuel(void);
/* <<< factory SetupDuel */
/* >>> factory PracticeDuelVerify_Turn6 */
typedef struct { uint8_t f; } PracticeDuelVerifyTurn6Result;
PracticeDuelVerifyTurn6Result PracticeDuelVerify_Turn6(void);
/* <<< factory PracticeDuelVerify_Turn6 */
/* >>> factory PracticeDuelVerify_Turn4 */
typedef struct { uint8_t f; } PracticeDuelVerifyTurn4Result;
PracticeDuelVerifyTurn4Result PracticeDuelVerify_Turn4(void);
/* <<< factory PracticeDuelVerify_Turn4 */
/* >>> factory ShuffleDeckAndDrawSevenCards */
typedef struct { uint8_t a; uint8_t f; } ShuffleDeckAndDrawSevenCardsResult;
ShuffleDeckAndDrawSevenCardsResult ShuffleDeckAndDrawSevenCards(void);
/* <<< factory ShuffleDeckAndDrawSevenCards */
/* >>> factory WriteTwoDigitNumberInTxSymbol_PadSpace */
void WriteTwoDigitNumberInTxSymbol_PadSpace(
	uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory WriteTwoDigitNumberInTxSymbol_PadSpace */
/* >>> factory PrintOpponentNumberOfHandAndDeckCards */
void PrintOpponentNumberOfHandAndDeckCards(void);
/* <<< factory PrintOpponentNumberOfHandAndDeckCards */
/* >>> factory PrintPlayerNumberOfHandAndDeckCards */
void PrintPlayerNumberOfHandAndDeckCards(void);
/* <<< factory PrintPlayerNumberOfHandAndDeckCards */
/* >>> factory PrintDuelResultStats */
void PrintDuelResultStats(void);
/* <<< factory PrintDuelResultStats */
/* >>> factory ConvertColorToEnergyCardID */
uint8_t ConvertColorToEnergyCardID(uint8_t a);
/* <<< factory ConvertColorToEnergyCardID */
/* >>> factory WriteOneByteNumberInTxSymbol_PadSpace */
void WriteOneByteNumberInTxSymbol_PadSpace(
	uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory WriteOneByteNumberInTxSymbol_PadSpace */
/* >>> factory PrintPracticeDuelNumberedInstruction */
typedef struct {
	uint16_t hl;
} PrintPracticeDuelNumberedInstructionResult;
PrintPracticeDuelNumberedInstructionResult PrintPracticeDuelNumberedInstruction(uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintPracticeDuelNumberedInstruction */
/* >>> factory PrintNextPracticeDuelInstruction */
void PrintNextPracticeDuelInstruction(void);
/* <<< factory PrintNextPracticeDuelInstruction */
/* >>> factory GoToFirstOrNextCardPage */
CardPageNavigationResult GoToFirstOrNextCardPage(void);
/* <<< factory GoToFirstOrNextCardPage */
/* >>> factory PrintPracticeDuelInstructions */
void PrintPracticeDuelInstructions(uint16_t hl);
/* <<< factory PrintPracticeDuelInstructions */
/* >>> factory DisplayPreviousCardPage */
void DisplayPreviousCardPage(void);
/* <<< factory DisplayPreviousCardPage */
/* >>> factory PrintNumberOfHandAndDeckCards */
void PrintNumberOfHandAndDeckCards(void);
/* <<< factory PrintNumberOfHandAndDeckCards */
/* >>> factory PrintReturnCardsToDeckDrawAgain */
typedef struct { uint8_t a, b, c, f; uint16_t hl, de; } PrintReturnCardsToDeckDrawAgainResult;
PrintReturnCardsToDeckDrawAgainResult PrintReturnCardsToDeckDrawAgain(void);
/* <<< factory PrintReturnCardsToDeckDrawAgain */
/* >>> factory PracticeDuelVerify_Turn3 */
typedef struct { uint8_t a; uint8_t f; } PracticeDuelVerifyTurn3Result;
PracticeDuelVerifyTurn3Result PracticeDuelVerify_Turn3(void);
/* <<< factory PracticeDuelVerify_Turn3 */
/* >>> factory CheckIfEnoughEnergiesToAttack */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; } CheckIfEnoughEnergiesToAttackResult;
CheckIfEnoughEnergiesToAttackResult CheckIfEnoughEnergiesToAttack(void);
/* <<< factory CheckIfEnoughEnergiesToAttack */
/* >>> factory PlayTurnDuelistDrawAnimation */
typedef struct { uint8_t e; uint8_t f; } PlayTurnDuelistDrawAnimationResult;
PlayTurnDuelistDrawAnimationResult PlayTurnDuelistDrawAnimation(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint16_t hl);
/* <<< factory PlayTurnDuelistDrawAnimation */
/* >>> factory DrawCardPageSet2AndRarityIcons */
typedef struct { uint16_t hl; } DrawCardPageSet2AndRarityIconsResult;
DrawCardPageSet2AndRarityIconsResult DrawCardPageSet2AndRarityIcons(void);
/* <<< factory DrawCardPageSet2AndRarityIcons */
/* >>> factory CountOppEnergyCardsInHandAndAttached */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } CountOppEnergyCardsInHandAndAttachedResult;
CountOppEnergyCardsInHandAndAttachedResult CountOppEnergyCardsInHandAndAttached(void);
/* <<< factory CountOppEnergyCardsInHandAndAttached */
/* >>> factory AIPickPrizeCards */
void AIPickPrizeCards(void);
/* <<< factory AIPickPrizeCards */
/* >>> factory HandleAIEnergyScoringForRepeatedBenchPokemon */
typedef struct { uint8_t a; uint8_t f; } HandleAIEnergyScoringForRepeatedBenchPokemonResult;
HandleAIEnergyScoringForRepeatedBenchPokemonResult HandleAIEnergyScoringForRepeatedBenchPokemon(void);
/* <<< factory HandleAIEnergyScoringForRepeatedBenchPokemon */
/* >>> factory CheckPrintCnfSlpPrz */
void CheckPrintCnfSlpPrz(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory CheckPrintCnfSlpPrz */
/* >>> factory LoadAnimCoordsAndFlags */
void LoadAnimCoordsAndFlags(void);
/* <<< factory LoadAnimCoordsAndFlags */
/* >>> factory PrintUsedTrainerCardDescription */
void PrintUsedTrainerCardDescription(void);
/* <<< factory PrintUsedTrainerCardDescription */
/* >>> factory PracticeDuelVerify_Turn5 */
typedef struct { uint8_t f; } PracticeDuelVerifyTurn5Result;
PracticeDuelVerifyTurn5Result PracticeDuelVerify_Turn5(void);
/* <<< factory PracticeDuelVerify_Turn5 */
/* >>> factory PracticeDuelVerify_Turn1 */
typedef struct { uint8_t f; } PracticeDuelVerify_Turn1Result;
PracticeDuelVerify_Turn1Result PracticeDuelVerify_Turn1(void);
/* <<< factory PracticeDuelVerify_Turn1 */
/* >>> factory PracticeDuelVerify_Turn2 */
typedef struct { uint8_t f; } PracticeDuelVerify_Turn2Result;
PracticeDuelVerify_Turn2Result PracticeDuelVerify_Turn2(void);
/* <<< factory PracticeDuelVerify_Turn2 */
/* >>> factory PracticeDuel_PlayStaryuFromBench */
typedef struct { uint8_t f; } PracticeDuel_PlayStaryuFromBenchResult;
PracticeDuel_PlayStaryuFromBenchResult PracticeDuel_PlayStaryuFromBench(void);
/* <<< factory PracticeDuel_PlayStaryuFromBench */
/* >>> factory DisplayDuelistTurnScreen */
void DisplayDuelistTurnScreen(void);
/* <<< factory DisplayDuelistTurnScreen */
/* >>> factory DrawDuelistPortraitsAndNames */
void DrawDuelistPortraitsAndNames(void);
/* <<< factory DrawDuelistPortraitsAndNames */
/* >>> factory CheckEnergyNeededForAttack */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CheckEnergyNeededForAttackResult;
CheckEnergyNeededForAttackResult CheckEnergyNeededForAttack(void);
/* <<< factory CheckEnergyNeededForAttack */
/* >>> factory CreateDamageCharSprite */
void CreateDamageCharSprite(uint8_t a, uint8_t f, uint16_t de);
/* <<< factory CreateDamageCharSprite */
/* >>> factory HasAlivePokemonInBench */
HasAlivePokemonInPlayAreaResult HasAlivePokemonInBench(void);
/* <<< factory HasAlivePokemonInBench */
/* >>> factory DrawOpponentSelectionScreen */
void DrawOpponentSelectionScreen(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DrawOpponentSelectionScreen */
/* >>> factory PracticeDuel_ReplaceKnockedOutPokemon */
void PracticeDuel_ReplaceKnockedOutPokemon(void);
/* <<< factory PracticeDuel_ReplaceKnockedOutPokemon */
/* >>> factory DrawDamageAnimationArrow */
void DrawDamageAnimationArrow(uint8_t f);
/* <<< factory DrawDamageAnimationArrow */
/* >>> factory DrawDamageAnimationWeak */
void DrawDamageAnimationWeak(void);
/* <<< factory DrawDamageAnimationWeak */
/* >>> factory DrawDamageAnimationResist */
void DrawDamageAnimationResist(void);
/* <<< factory DrawDamageAnimationResist */
/* >>> factory DrawDamageAnimationNumbers */
void DrawDamageAnimationNumbers(void);
/* <<< factory DrawDamageAnimationNumbers */
/* >>> factory Func_15886 */
CoreCardListResult Func_15886(uint16_t hl);
/* <<< factory Func_15886 */
/* >>> factory CheckAbleToRetreat */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } CheckAbleToRetreatResult;
CheckAbleToRetreatResult CheckAbleToRetreat(void);
/* <<< factory CheckAbleToRetreat */
/* >>> factory LookForEnergyNeededInHand */
uint8_t LookForEnergyNeededInHand(void);
/* <<< factory LookForEnergyNeededInHand */
/* >>> factory Func_7364 */
typedef struct { uint8_t a; uint8_t f; } Func_7364Result;
Func_7364Result Func_7364(void);
/* <<< factory Func_7364 */
/* >>> factory CheckEnergyNeededForAttackAfterDiscard */
typedef struct { uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint8_t f; } CheckEnergyNeededForAttackAfterDiscardResult;
CheckEnergyNeededForAttackAfterDiscardResult CheckEnergyNeededForAttackAfterDiscard(void);
/* <<< factory CheckEnergyNeededForAttackAfterDiscard */
/* >>> factory DisplayFirstOrNextCardPage */
CardPageNavigationResult DisplayFirstOrNextCardPage(uint8_t b);
/* <<< factory DisplayFirstOrNextCardPage */
/* >>> factory PrintAttackOrCardDescription */
typedef struct { uint8_t a; uint8_t d; uint8_t e; uint8_t f; uint16_t hl; } PrintAttackOrCardDescriptionResult;
PrintAttackOrCardDescriptionResult PrintAttackOrCardDescription(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory PrintAttackOrCardDescription */
/* >>> factory PrintAttackOrPkmnPowerInformation */
typedef struct { uint8_t a; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint8_t f; uint16_t hl; } PrintAttackOrPkmnPowerInformationResult;
PrintAttackOrPkmnPowerInformationResult PrintAttackOrPkmnPowerInformation(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintAttackOrPkmnPowerInformation */
/* >>> factory PrintAttackOrNonPokemonCardDescription */
PrintAttackOrCardDescriptionResult PrintAttackOrNonPokemonCardDescription(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory PrintAttackOrNonPokemonCardDescription */
/* >>> factory DisplayCardPageOnLeftOrRightPressed */
void DisplayCardPageOnLeftOrRightPressed(uint8_t a);
/* <<< factory DisplayCardPageOnLeftOrRightPressed */
/* >>> factory PrintPlayAreaCardHeader */
void PrintPlayAreaCardHeader(void);
/* <<< factory PrintPlayAreaCardHeader */
/* >>> factory PrintPokemonCardLength */
void PrintPokemonCardLength(uint16_t hl, uint8_t b, uint8_t c);
/* <<< factory PrintPokemonCardLength */
/* >>> factory PlayDeckShuffleAnimation */
uint8_t PlayDeckShuffleAnimation(void);
/* <<< factory PlayDeckShuffleAnimation */
/* >>> factory OppAction_6b30 */
uint8_t OppAction_6b30(void);
/* <<< factory OppAction_6b30 */
/* >>> factory PrintPlayAreaCardInformation */
typedef struct { uint16_t hl; } PrintPlayAreaCardInformationResult;
PrintPlayAreaCardInformationResult PrintPlayAreaCardInformation(void);
/* <<< factory PrintPlayAreaCardInformation */
/* >>> factory PrintPlayAreaCardInformationAndLocation */
void PrintPlayAreaCardInformationAndLocation(void);
/* <<< factory PrintPlayAreaCardInformationAndLocation */
/* >>> factory DisplayUsePokemonPowerScreen */
void DisplayUsePokemonPowerScreen(void);
/* <<< factory DisplayUsePokemonPowerScreen */
/* >>> factory InitAndPrintPlayAreaCardInformationAndLocation */
void InitAndPrintPlayAreaCardInformationAndLocation(void);
/* <<< factory InitAndPrintPlayAreaCardInformationAndLocation */
/* >>> factory InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox */
void InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox(void);
/* <<< factory InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox */
/* >>> factory PrintPlayAreaCardList */
void PrintPlayAreaCardList(void);
/* <<< factory PrintPlayAreaCardList */
/* >>> factory OppAction_UsePokemonPower */
void OppAction_UsePokemonPower(void);
/* <<< factory OppAction_UsePokemonPower */
/* >>> factory Func_616e */
void Func_616e(uint8_t a);
/* <<< factory Func_616e */
/* >>> factory PrintPlayAreaCardList_EnableLCD */
typedef struct { uint8_t a; } NumPlayAreaItemsResult;
NumPlayAreaItemsResult PrintPlayAreaCardList_EnableLCD(void);
/* <<< factory PrintPlayAreaCardList_EnableLCD */
/* >>> factory FlushAllPalettesOrSendPal23Packet */
void FlushAllPalettesOrSendPal23Packet(void);
/* <<< factory FlushAllPalettesOrSendPal23Packet */
/* >>> factory CheckIfCardCanBePlayed */
typedef struct {
	uint8_t a;
	uint8_t f;
} CheckIfCardCanBePlayedResult;
CheckIfCardCanBePlayedResult CheckIfCardCanBePlayed(uint8_t a);
/* <<< factory CheckIfCardCanBePlayed */
/* >>> factory OppAction_6b15 */
typedef struct { uint8_t a; uint8_t f; uint8_t c; uint16_t hl; } OppAction_6b15Result;
OppAction_6b15Result OppAction_6b15(void);
/* <<< factory OppAction_6b15 */
/* >>> factory OppAction_ExecutePokemonPowerEffect */
typedef struct { uint8_t a; uint8_t f; uint8_t c; uint16_t hl; } OppAction_ExecutePokemonPowerEffectResult;
OppAction_ExecutePokemonPowerEffectResult OppAction_ExecutePokemonPowerEffect(void);
/* <<< factory OppAction_ExecutePokemonPowerEffect */
/* >>> factory LoadSelectedCardGfx */
void LoadSelectedCardGfx(void);
/* <<< factory LoadSelectedCardGfx */
/* >>> factory AIProcessHandTrainerCards */
typedef struct { uint8_t a; uint8_t f; } AIProcessHandTrainerCardsWrapResult;
AIProcessHandTrainerCardsWrapResult AIProcessHandTrainerCards(uint8_t a);
/* <<< factory AIProcessHandTrainerCards */
/* >>> factory CardListFunction */
typedef struct { uint8_t a; uint8_t f; } CardListFunctionResult;
CardListFunctionResult CardListFunction(void);
/* <<< factory CardListFunction */
/* >>> factory CheckIfSelectedAttackIsUnusable */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CheckIfSelectedAttackIsUnusableResult;
CheckIfSelectedAttackIsUnusableResult CheckIfSelectedAttackIsUnusable(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CheckIfSelectedAttackIsUnusable */
/* >>> factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult;
CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult CheckForBenchIDAtHalfHPAndCanUseSecondAttack(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
/* >>> factory CountNumberOfSetUpBenchPokemon */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CountNumberOfSetUpBenchPokemonResult;
CountNumberOfSetUpBenchPokemonResult CountNumberOfSetUpBenchPokemon(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CountNumberOfSetUpBenchPokemon */
/* >>> factory HandleLegendaryArticunoEnergyScoring */
void HandleLegendaryArticunoEnergyScoring(void);
/* <<< factory HandleLegendaryArticunoEnergyScoring */
/* >>> factory CheckIfArenaCardIsFullyPowered */
typedef struct { uint8_t a; uint8_t f; } CheckIfArenaCardIsFullyPoweredResult;
CheckIfArenaCardIsFullyPoweredResult CheckIfArenaCardIsFullyPowered(void);
/* <<< factory CheckIfArenaCardIsFullyPowered */
/* >>> factory SendCardAttrBlkPacket */
typedef struct { uint8_t a, f, b, c, d, e; uint16_t hl; } SendCardAttrBlkPacketResult;
SendCardAttrBlkPacketResult SendCardAttrBlkPacket(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory SendCardAttrBlkPacket */
/* >>> factory ApplyBGP6OrSGB3ToCardImage */
SendCardAttrBlkPacketResult ApplyBGP6OrSGB3ToCardImage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ApplyBGP6OrSGB3ToCardImage */
/* >>> factory DrawLargePictureOfCard */
void DrawLargePictureOfCard(void);
/* <<< factory DrawLargePictureOfCard */
/* >>> factory DrawCardPageSurroundingBox */
void DrawCardPageSurroundingBox(void);
/* <<< factory DrawCardPageSurroundingBox */
/* >>> factory PrintPokemonCardPageGenericInformation */
typedef struct { uint16_t hl; } PrintPokemonCardPageGenericInformationResult;
PrintPokemonCardPageGenericInformationResult PrintPokemonCardPageGenericInformation(void);
/* <<< factory PrintPokemonCardPageGenericInformation */
/* >>> factory DrawDuelHUD */
void DrawDuelHUD(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory DrawDuelHUD */
/* >>> factory DrawDuelHUDs */
void DrawDuelHUDs(void);
/* <<< factory DrawDuelHUDs */
/* >>> factory DrawCardListScreenLayout */
typedef struct { uint8_t a, f; } DrawCardListScreenLayoutResult;
DrawCardListScreenLayoutResult DrawCardListScreenLayout(void);
/* <<< factory DrawCardListScreenLayout */
/* >>> factory ApplyBGP7OrSGB2ToCardImage */
SendCardAttrBlkPacketResult ApplyBGP7OrSGB2ToCardImage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ApplyBGP7OrSGB2ToCardImage */
/* >>> factory DisplayPracticeDuelPlayerHandScreen */
void DisplayPracticeDuelPlayerHandScreen(void);
/* <<< factory DisplayPracticeDuelPlayerHandScreen */
/* >>> factory DrawDuelMainScene */
void DrawDuelMainScene(void);
/* <<< factory DrawDuelMainScene */
/* >>> factory InitAndDrawCardListScreenLayout */
DrawCardListScreenLayoutResult InitAndDrawCardListScreenLayout(void);
/* <<< factory InitAndDrawCardListScreenLayout */
/* >>> factory RedrawTurnDuelistsDuelHUD */
void RedrawTurnDuelistsDuelHUD(void);
/* <<< factory RedrawTurnDuelistsDuelHUD */
/* >>> factory OppAction_DrawDuelMainScene */
void OppAction_DrawDuelMainScene(void);
/* <<< factory OppAction_DrawDuelMainScene */
/* >>> factory InitAndDrawCardListScreenLayout_WithSelectCheckMenu */
DrawCardListScreenLayoutResult InitAndDrawCardListScreenLayout_WithSelectCheckMenu(void);
/* <<< factory InitAndDrawCardListScreenLayout_WithSelectCheckMenu */
/* >>> factory DisplayCardListDetails */
typedef struct { uint8_t a; uint8_t f; } DisplayCardListDetailsResult;
DisplayCardListDetailsResult DisplayCardListDetails(void);
/* <<< factory DisplayCardListDetails */
/* >>> factory OppAction_FinishTurnWithoutAttacking */
void OppAction_FinishTurnWithoutAttacking(void);
/* <<< factory OppAction_FinishTurnWithoutAttacking */
/* >>> factory RedrawTurnDuelistsMainSceneOrDuelHUD */
void RedrawTurnDuelistsMainSceneOrDuelHUD(void);
/* <<< factory RedrawTurnDuelistsMainSceneOrDuelHUD */
/* >>> factory DisplayNoBasicPokemonInHandScreen */
void DisplayNoBasicPokemonInHandScreen(void);
/* <<< factory DisplayNoBasicPokemonInHandScreen */
/* >>> factory PrintAndLoadAttacksToDuelTempList */
uint8_t PrintAndLoadAttacksToDuelTempList(void);
/* <<< factory PrintAndLoadAttacksToDuelTempList */
/* >>> factory DisplayPokemonAttackCardPage */
void DisplayPokemonAttackCardPage(uint8_t b, uint8_t c, uint8_t d, uint16_t de, uint16_t hl);
/* <<< factory DisplayPokemonAttackCardPage */
/* >>> factory DisplayCardPage_PokemonAttack2Page2 */
void DisplayCardPage_PokemonAttack2Page2(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory DisplayCardPage_PokemonAttack2Page2 */
/* >>> factory DisplayCardPage_PokemonAttack1Page1 */
void DisplayCardPage_PokemonAttack1Page1(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory DisplayCardPage_PokemonAttack1Page1 */
/* >>> factory DisplayCardPage_PokemonAttack1Page2 */
void DisplayCardPage_PokemonAttack1Page2(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory DisplayCardPage_PokemonAttack1Page2 */
/* >>> factory DisplayCardPage_PokemonAttack2Page1 */
void DisplayCardPage_PokemonAttack2Page1(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory DisplayCardPage_PokemonAttack2Page1 */
/* >>> factory DisplayAttackPage_Attack1Page1 */
void DisplayAttackPage_Attack1Page1(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory DisplayAttackPage_Attack1Page1 */
/* >>> factory DisplayAttackPage_Attack2Page1 */
void DisplayAttackPage_Attack2Page1(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory DisplayAttackPage_Attack2Page1 */
/* >>> factory DisplayAttackPage_Attack2Page2 */
void DisplayAttackPage_Attack2Page2(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory DisplayAttackPage_Attack2Page2 */
/* >>> factory DisplayAttackPage_Attack1Page2 */
void DisplayAttackPage_Attack1Page2(uint8_t b, uint8_t c, uint8_t d);
/* <<< factory DisplayAttackPage_Attack1Page2 */
/* >>> factory DisplayEnergyDiscardMenu */
void DisplayEnergyDiscardMenu(void);
/* <<< factory DisplayEnergyDiscardMenu */
/* >>> factory DisplayEnergyDiscardScreen */
void DisplayEnergyDiscardScreen(uint8_t a);
/* <<< factory DisplayEnergyDiscardScreen */
/* >>> factory OpenAttackPage */
void OpenAttackPage(void);
/* <<< factory OpenAttackPage */
/* >>> factory HandleEnergyDiscardMenuInput */
typedef struct {
	uint8_t a;
	uint8_t f;
} HandleEnergyDiscardMenuInputResult;
HandleEnergyDiscardMenuInputResult HandleEnergyDiscardMenuInput(void);
/* <<< factory HandleEnergyDiscardMenuInput */
/* >>> factory DisplayRetreatScreen */
void DisplayRetreatScreen(uint8_t a);
/* <<< factory DisplayRetreatScreen */
/* >>> factory PrintPracticeDuelInstructions_Fast */
void PrintPracticeDuelInstructions_Fast(uint16_t hl);
/* <<< factory PrintPracticeDuelInstructions_Fast */
#endif
