/* >>> factory RaiseAIScoreToAllMatchingIDsInBench */
static void adapt_RaiseAIScoreToAllMatchingIDsInBench(ProbeState *s)
{
	s->hl = RaiseAIScoreToAllMatchingIDsInBench((CardId)((uint16_t)s->b << 8 | s->c));
}
/* <<< factory RaiseAIScoreToAllMatchingIDsInBench */
/* >>> factory AIAttachEnergyInHandToCardInBench */
static void adapt_AIAttachEnergyInHandToCardInBench(ProbeState *s)
{
	CardId pokemon = (CardId)s->c;
	CardId energy = (CardId)((uint16_t)s->d << 8 | s->e);
	AIAttachEnergyInHandToCardInBenchResult r = AIAttachEnergyInHandToCardInBench(pokemon, energy);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIAttachEnergyInHandToCardInBench */
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
	{ "SetCardPalette", adapt_SetCardPalette },
	{ "SetBGP2ToCardPalette", adapt_SetBGP2ToCardPalette },
	{ "SetBGP5ToCardPalette", adapt_SetBGP5ToCardPalette },
	{ "WriteTwoByteNumberInTxSymbolFormat", adapt_WriteTwoByteNumberInTxSymbolFormat },
	{ "WriteTwoDigitNumberInTxSymbolFormat", adapt_WriteTwoDigitNumberInTxSymbolFormat },
	{ "ValidateSavedDuelData", adapt_ValidateSavedDuelData },
	{ "LoadSavedDuelData", adapt_LoadSavedDuelData },
	{ "DiscardSavedDuelData", adapt_DiscardSavedDuelData },
	{ "TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1", adapt_TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1 },
	{ "CheckIfActivePokemonCanUseAnyNonResidualAttack", adapt_CheckIfActivePokemonCanUseAnyNonResidualAttack },
/* <<< part probe_entries_core */
