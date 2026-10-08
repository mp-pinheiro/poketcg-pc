/* --- factory ValidateSavedDuelDataFromHL */
/* --- factory CopyCGBCardPalette */
/* --- factory CreateCardAttrBlkPacket_DataSet */
/* --- factory LoadSavedDuelDataFromDE */
/* --- factory SetBGP7OrSGB2ToCardPalette */
/* --- factory JPWriteByteToBGMap0 */
/* === factory SaveDuelDataToDE */
/* >>> factory LoadSavedDuelData */
typedef struct { uint8_t f; uint16_t hl; } ValidateSavedDuelDataResult;
ValidateSavedDuelDataResult ValidateSavedDuelData(uint16_t hl);
void LoadSavedDuelData(uint16_t de);
/* <<< factory LoadSavedDuelData */
/* >>> factory DiscardSavedDuelData */
void DiscardSavedDuelData(void);
/* <<< factory DiscardSavedDuelData */
/* >>> factory WriteTwoByteNumberInTxSymbolFormat */
void WriteTwoByteNumberInTxSymbolFormat(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory WriteTwoByteNumberInTxSymbolFormat */
/* >>> factory WriteTwoDigitNumberInTxSymbolFormat */
void WriteTwoDigitNumberInTxSymbolFormat(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory WriteTwoDigitNumberInTxSymbolFormat */
/* --- factory SetSGB3ToCardPalette */
/* >>> factory LookForCardIDInPlayArea_Bank5 */
typedef struct { uint8_t a; uint8_t b; uint8_t f; } LookResult;
LookResult LookForCardIDInPlayArea_Bank5(uint16_t de, uint8_t b);
/* <<< factory LookForCardIDInPlayArea_Bank5 */
/* >>> factory CheckEnergyFlagsNeededInList */
typedef struct { uint8_t a; uint8_t carry; uint8_t c; } EnergyFlagsResult;
EnergyFlagsResult CheckEnergyFlagsNeededInList(uint8_t a);
/* <<< factory CheckEnergyFlagsNeededInList */
/* --- factory PlaceCardImageOAM */
/* --- factory Func_6423 */
/* --- factory CreateCardAttrBlkPacket */
/* --- factory Func_14323 */
/* >>> factory LookForCardIDInHand */
CoreCardListResult LookForCardIDInHand(CardId de);
/* <<< factory LookForCardIDInHand */
/* >>> factory LookForCardIDInHandList_Bank5 */
CoreCardListResult LookForCardIDInHandList_Bank5(CardId de);
/* <<< factory LookForCardIDInHandList_Bank5 */
/* --- factory SetBGP6OrSGB3ToCardPalette */
/* --- factory SetOBP1OrSGB3ToCardPalette */
/* --- factory ResetDoFrameFunction_Bank1 */
/* --- factory Func_6ba2 */
/* --- factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */
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
	CardId card_id);
/* <<< factory LookForCardIDInLocation_Bank5 */
/* >>> factory RemoveCardIDInList */
typedef struct { uint8_t a; uint8_t f; } RemoveCardIDResult;
RemoveCardIDResult RemoveCardIDInList(uint16_t *hl, CardId de);
/* <<< factory RemoveCardIDInList */
/* >>> factory ApplyCardCGBAttributes */
/* duel/core.asm:4120-4126: FillRectangle's exit -- b 8, c 0, hl past the image. */
typedef struct { uint8_t b; uint8_t c; uint16_t de; uint16_t hl; } ApplyCardCGBAttributesResult;
ApplyCardCGBAttributesResult ApplyCardCGBAttributes(uint8_t a, uint16_t de);
/* <<< factory ApplyCardCGBAttributes */
/* >>> factory SetCardPalette */
void SetCardPalette(uint8_t a);
/* <<< factory SetCardPalette */
/* >>> factory SetBGP2ToCardPalette */
void SetBGP2ToCardPalette(void);
/* <<< factory SetBGP2ToCardPalette */
/* >>> factory SetBGP5ToCardPalette */
void SetBGP5ToCardPalette(void);
/* <<< factory SetBGP5ToCardPalette */
/* --- factory DecideLinkDuelVariables */
/* --- factory Func_1585b */
/* --- factory ValidateSavedNonLinkDuelData */
/* >>> factory AIAttachEnergyInHandToCardInPlayArea */
typedef struct { uint8_t a; uint8_t f; } AIAttachEnergyInHandToCardInPlayAreaResult;
AIAttachEnergyInHandToCardInPlayAreaResult AIAttachEnergyInHandToCardInPlayArea(CardId bc, CardId de);
/* <<< factory AIAttachEnergyInHandToCardInPlayArea */
/* --- factory WriteTwoDigitNumberInTxSymbol_PadSpace */
/* >>> factory ConvertColorToEnergyCardID */
typedef struct { uint8_t a; uint8_t d; uint8_t e; } ConvertColorResult;
ConvertColorResult ConvertColorToEnergyCardID(uint8_t a);
/* <<< factory ConvertColorToEnergyCardID */
/* --- factory WriteOneByteNumberInTxSymbol_PadSpace */
/* --- factory DrawOpponentSelectionScreen */
/* --- factory Func_15886 */
/* --- factory Func_7364 */
/* === factory PrintPlayAreaCardHeader */
/* >>> factory TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1 */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} TwoByteNumberToTxSymbolTrimResult;
TwoByteNumberToTxSymbolTrimResult TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1(uint16_t hl);
/* <<< factory TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1 */
/* --- factory Func_616e */
/* --- factory FlushAllPalettesOrSendPal23Packet */
/* >>> factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult;
CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult CheckForBenchIDAtHalfHPAndCanUseSecondAttack(uint16_t de, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
/* --- factory SendCardAttrBlkPacket */
/* --- factory ApplyBGP6OrSGB3ToCardImage */
/* --- factory ApplyBGP7OrSGB2ToCardImage */
/* --- factory Func_5a81 */
/* >>> factory OppAction_TossCoinATimes */
typedef struct { uint8_t a, f, b, c, d, e; uint16_t hl; } OppAction_TossCoinATimesResult;
OppAction_TossCoinATimesResult OppAction_TossCoinATimes(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory OppAction_TossCoinATimes */
/* --- factory Func_5542 */
/* --- factory CanArenaCardUseNonResidualAttack */
/* === factory OpenNonTurnHolderDiscardPileScreen */
/* >>> factory CheckIfActivePokemonCanUseAnyNonResidualAttack */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CheckIfActivePokemonCanUseAnyNonResidualAttackResult;
CheckIfActivePokemonCanUseAnyNonResidualAttackResult CheckIfActivePokemonCanUseAnyNonResidualAttack(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CheckIfActivePokemonCanUseAnyNonResidualAttack */
/* >>> factory OppAction_UseMetronomeAttack */
void OppAction_UseMetronomeAttack(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory OppAction_UseMetronomeAttack */
/* --- factory RequestToPrintCards_SelectStartCard */
/* --- factory StartDuel */
/* --- factory StartDuel_VSLinkOpp */
/* --- factory SetLinkDuelTransmissionFrameFunction */
/* --- factory UnreferencedDrawCardFromDeckToHand */
/* --- factory HandleWaitingLinkOpponentMenu */
/* --- factory _ContinueDuel */
/* --- factory DoLinkOpponentTurn */
