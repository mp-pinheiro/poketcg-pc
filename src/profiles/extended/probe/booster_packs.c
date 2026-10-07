/* >>> factory AddBoosterCardToTempCardCollection */
static void adapt_AddBoosterCardToTempCardCollection(ProbeState *s)
{
	AddBoosterCardToTempCardCollectionResult result =
		AddBoosterCardToTempCardCollection();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AddBoosterCardToTempCardCollection */
/* >>> factory AddBoosterEnergyToDrawnEnergies */
static void adapt_AddBoosterEnergyToDrawnEnergies(ProbeState *s)
{
	CardId id = (CardId)(((uint16_t)s->d << 8) | s->e);
	AddBoosterEnergyToDrawnEnergiesResult result =
		AddBoosterEnergyToDrawnEnergies(id);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory AddBoosterEnergyToDrawnEnergies */
/* >>> factory GenerateTwoTypesEnergyBooster */
static void adapt_GenerateTwoTypesEnergyBooster(ProbeState *s)
{
	GenerateTwoTypesEnergyBoosterResult result = GenerateTwoTypesEnergyBooster(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory GenerateTwoTypesEnergyBooster */
/* >>> factory GenerateRandomEnergy */
static void adapt_GenerateRandomEnergy(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GenerateRandomEnergy();
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory GenerateRandomEnergy */
/* >>> factory GenerateEnergyBoosterGrassPsychic */
static void adapt_GenerateEnergyBoosterGrassPsychic(ProbeState *s)
{
	GenerateTwoTypesEnergyBoosterResult result = GenerateEnergyBoosterGrassPsychic();
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory GenerateEnergyBoosterGrassPsychic */
/* >>> factory GenerateEnergyBoosterLightningFire */
static void adapt_GenerateEnergyBoosterLightningFire(ProbeState *s)
{
	GenerateTwoTypesEnergyBoosterResult result = GenerateEnergyBoosterLightningFire();
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory GenerateEnergyBoosterLightningFire */
/* >>> factory GenerateEnergyBoosterWaterFighting */
static void adapt_GenerateEnergyBoosterWaterFighting(ProbeState *s)
{
	GenerateTwoTypesEnergyBoosterResult result = GenerateEnergyBoosterWaterFighting();
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory GenerateEnergyBoosterWaterFighting */
/* >>> factory GenerateFightingEnergy */
static void adapt_GenerateFightingEnergy(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GenerateFightingEnergy();
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory GenerateFightingEnergy */
/* >>> factory GenerateFireEnergy */
static void adapt_GenerateFireEnergy(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GenerateFireEnergy();
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory GenerateFireEnergy */
/* >>> factory GenerateGrassEnergy */
static void adapt_GenerateGrassEnergy(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GenerateGrassEnergy();
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory GenerateGrassEnergy */
/* >>> factory GenerateLightningEnergy */
static void adapt_GenerateLightningEnergy(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GenerateLightningEnergy();
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory GenerateLightningEnergy */
/* >>> factory GeneratePsychicEnergy */
static void adapt_GeneratePsychicEnergy(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GeneratePsychicEnergy();
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory GeneratePsychicEnergy */
/* >>> factory GenerateWaterEnergy */
static void adapt_GenerateWaterEnergy(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GenerateWaterEnergy();
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory GenerateWaterEnergy */
/* >>> factory GenerateRandomEnergyBooster */
static void adapt_GenerateRandomEnergyBooster(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GenerateRandomEnergyBooster();
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory GenerateRandomEnergyBooster */
/* >>> part probe_entries_booster_packs */
const ProbeEntry probe_entries_booster_packs[] = {
	{ "GetCurrentRarityAmount", adapt_GetCurrentRarityAmount },
	{ "GetBoosterCardType", adapt_GetBoosterCardType },
	{ "CalculateTypeChances", adapt_CalculateTypeChances },
	{ "UpdateBoosterCardTypesChanceByte", adapt_UpdateBoosterCardTypesChanceByte },
	{ "AppendCurrentCardToHL", adapt_AppendCurrentCardToHL },
	{ "AddBoosterCardToTempCardCollection", adapt_AddBoosterCardToTempCardCollection },
	{ "AddBoosterCardToDrawnEnergies", adapt_AddBoosterCardToDrawnEnergies },
	{ "AddBoosterEnergyToDrawnEnergies", adapt_AddBoosterEnergyToDrawnEnergies },
	{ "ZeroBoosterRarityData", adapt_ZeroBoosterRarityData },
	{ "GenerateTwoTypesEnergyBooster", adapt_GenerateTwoTypesEnergyBooster },
	{ "GenerateRandomEnergy", adapt_GenerateRandomEnergy },
	{ "GenerateEnergyBoosterGrassPsychic", adapt_GenerateEnergyBoosterGrassPsychic },
	{ "GenerateEnergyBoosterLightningFire", adapt_GenerateEnergyBoosterLightningFire },
	{ "GenerateEnergyBoosterWaterFighting", adapt_GenerateEnergyBoosterWaterFighting },
	{ "GenerateFightingEnergy", adapt_GenerateFightingEnergy },
	{ "GenerateFireEnergy", adapt_GenerateFireEnergy },
	{ "GenerateGrassEnergy", adapt_GenerateGrassEnergy },
	{ "GenerateLightningEnergy", adapt_GenerateLightningEnergy },
	{ "GeneratePsychicEnergy", adapt_GeneratePsychicEnergy },
	{ "GenerateWaterEnergy", adapt_GenerateWaterEnergy },
	{ "GenerateRandomEnergyBooster", adapt_GenerateRandomEnergyBooster },
	{ "PutEnergiesAndNonEnergiesTogether", adapt_PutEnergiesAndNonEnergiesTogether },
	{ "LoadRarityAmountsToWram", adapt_LoadRarityAmountsToWram },
	{ "DetermineBoosterCardType", adapt_DetermineBoosterCardType },
	{ "FindBoosterDataPointer", adapt_FindBoosterDataPointer },
	{ "AddBoosterCardToDrawnNonEnergies", adapt_AddBoosterCardToDrawnNonEnergies },
	{ "AddBoosterCardsToCollection", adapt_AddBoosterCardsToCollection },
	{ "GenerateBoosterEnergies", adapt_GenerateBoosterEnergies },
	{ "DetermineBoosterCard", adapt_DetermineBoosterCard },
	{ "CheckCardInSetAndRarity", adapt_CheckCardInSetAndRarity },
	{ "CheckCardAlreadyDrawn", adapt_CheckCardAlreadyDrawn },
	{ "FindCardsInSetAndRarity", adapt_FindCardsInSetAndRarity },
	{ "GenerateBoosterNonEnergies", adapt_GenerateBoosterNonEnergies },
	{ "InitBoosterData", adapt_InitBoosterData },
	{ "GenerateBoosterPack", adapt_GenerateBoosterPack },
	{ NULL, NULL },
};
/* <<< part probe_entries_booster_packs */
