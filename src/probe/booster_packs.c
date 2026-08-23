#include "home/booster_packs.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory GetCurrentRarityAmount */
static void adapt_GetCurrentRarityAmount(ProbeState *s)
{
	RarityAmount r = GetCurrentRarityAmount();
	s->a = r.a;
	s->hl = r.hl;
}
/* <<< factory GetCurrentRarityAmount */

/* >>> factory GetBoosterCardType */
static void adapt_GetBoosterCardType(ProbeState *s)
{
	s->a = GetBoosterCardType(s->a);
}
/* <<< factory GetBoosterCardType */

/* >>> factory CalculateTypeChances */
static void adapt_CalculateTypeChances(ProbeState *s)
{
	s->a = CalculateTypeChances();
}
/* <<< factory CalculateTypeChances */

/* >>> factory UpdateBoosterCardTypesChanceByte */
static void adapt_UpdateBoosterCardTypesChanceByte(ProbeState *s)
{
	s->a = UpdateBoosterCardTypesChanceByte();
}
/* <<< factory UpdateBoosterCardTypesChanceByte */

/* >>> factory AppendCurrentCardToHL */
static void adapt_AppendCurrentCardToHL(ProbeState *s)
{
	AppendCurrentCardToHL(&s->hl);
	s->a = 0u;
	s->f = 0x80u;
}
/* <<< factory AppendCurrentCardToHL */

/* >>> factory AddBoosterCardToTempCardCollection */
static void adapt_AddBoosterCardToTempCardCollection(ProbeState *s)
{
	uint8_t card = gb_read8(wBoosterCurrentCard_ADDR);
	uint16_t slot = (uint16_t)(wTempCardCollection_ADDR + card);
	uint8_t before = gb_read8(slot);
	AddBoosterCardToTempCardCollection();
	s->a = card;
	s->f = (uint8_t)((s->f & 0x10u) |
	                ((uint8_t)(before + 1u) == 0u ? 0x80u : 0u) |
	                ((before & 0x0fu) == 0x0fu ? 0x20u : 0u));
}
/* <<< factory AddBoosterCardToTempCardCollection */

/* >>> factory AddBoosterCardToDrawnEnergies */
static void adapt_AddBoosterCardToDrawnEnergies(ProbeState *s)
{
	AddBoosterCardToDrawnEnergiesResult result = AddBoosterCardToDrawnEnergies();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AddBoosterCardToDrawnEnergies */

/* >>> factory AddBoosterEnergyToDrawnEnergies */
static void adapt_AddBoosterEnergyToDrawnEnergies(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = AddBoosterEnergyToDrawnEnergies(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AddBoosterEnergyToDrawnEnergies */

/* >>> factory ZeroBoosterRarityData */
static void adapt_ZeroBoosterRarityData(ProbeState *s)
{
	ZeroBoosterRarityData();
	s->a = 0u;
	s->f = 0x80u;
}
/* <<< factory ZeroBoosterRarityData */

/* >>> factory GenerateTwoTypesEnergyBooster */
static void adapt_GenerateTwoTypesEnergyBooster(ProbeState *s)
{
	GenerateTwoTypesEnergyBoosterResult result = GenerateTwoTypesEnergyBooster(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory GenerateTwoTypesEnergyBooster */

/* >>> factory GenerateRandomEnergy */
static void adapt_GenerateRandomEnergy(ProbeState *s)
{
	AddBoosterEnergyToDrawnEnergiesResult result = GenerateRandomEnergy();
	s->a = result.a;
	s->f = result.f;
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
	s->hl = result.hl;
}
/* <<< factory GenerateEnergyBoosterWaterFighting */

/* >>> factory GenerateRandomEnergyBooster */
static void adapt_GenerateRandomEnergyBooster(ProbeState *s)
{
	GenerateRandomEnergyBooster();
	s->a = 0u;
	s->f = 0x80u;
}
/* <<< factory GenerateRandomEnergyBooster */

/* >>> factory PutEnergiesAndNonEnergiesTogether */
static void adapt_PutEnergiesAndNonEnergiesTogether(ProbeState *s)
{
	PutEnergiesAndNonEnergiesTogetherResult result = PutEnergiesAndNonEnergiesTogether(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory PutEnergiesAndNonEnergiesTogether */

/* >>> factory LoadRarityAmountsToWram */
static void adapt_LoadRarityAmountsToWram(ProbeState *s)
{
	(void)s;
	LoadRarityAmountsToWram();
}
/* <<< factory LoadRarityAmountsToWram */

/* >>> factory DetermineBoosterCardType */
static void adapt_DetermineBoosterCardType(ProbeState *s)
{
	s->a = DetermineBoosterCardType(s->a);
}
/* <<< factory DetermineBoosterCardType */

/* >>> factory FindBoosterDataPointer */
static void adapt_FindBoosterDataPointer(ProbeState *s)
{
	uint8_t pack = gb_read8(wBoosterPackID_ADDR);
	uint16_t pointer = FindBoosterDataPointer();
	s->a = (uint8_t)pointer;
	s->f = (pack == 0u) ? 0x80u : 0u;
	s->hl = pointer;
}
/* <<< factory FindBoosterDataPointer */

/* >>> factory AddBoosterCardToDrawnNonEnergies */
static void adapt_AddBoosterCardToDrawnNonEnergies(ProbeState *s)
{
	(void)s;
	AddBoosterCardToDrawnNonEnergies();
}
/* <<< factory AddBoosterCardToDrawnNonEnergies */

/* >>> factory AddBoosterCardsToCollection */
static void adapt_AddBoosterCardsToCollection(ProbeState *s)
{
	AddBoosterCardsToCollection();
	s->a = 0u;
	s->f = 0x80u;
}
/* <<< factory AddBoosterCardsToCollection */

/* >>> factory GenerateBoosterEnergies */
static void adapt_GenerateBoosterEnergies(ProbeState *s)
{
	(void)s;
	GenerateBoosterEnergies();
}
/* <<< factory GenerateBoosterEnergies */

/* >>> factory DetermineBoosterCard */
static void adapt_DetermineBoosterCard(ProbeState *s)
{
	DetermineBoosterCardResult r = DetermineBoosterCard(s->d, s->e);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory DetermineBoosterCard */

/* >>> factory CheckCardInSetAndRarity */
static void adapt_CheckCardInSetAndRarity(ProbeState *s)
{
	CheckCardInSetAndRarityResult r = CheckCardInSetAndRarity(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory CheckCardInSetAndRarity */

/* >>> factory CheckCardAlreadyDrawn */
static void adapt_CheckCardAlreadyDrawn(ProbeState *s)
{
	CheckCardAlreadyDrawnResult r = CheckCardAlreadyDrawn();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckCardAlreadyDrawn */

/* >>> factory FindCardsInSetAndRarity */
static void adapt_FindCardsInSetAndRarity(ProbeState *s)
{
	FindCardsInSetAndRarity();
	s->a = 0xE5u;
	s->f = 0xC0u;
	s->d = 0x00u;
	s->e = 0xE5u;
}
/* <<< factory FindCardsInSetAndRarity */

/* >>> factory GenerateBoosterNonEnergies */
static void adapt_GenerateBoosterNonEnergies(ProbeState *s)
{
	GenerateBoosterNonEnergiesResult r = GenerateBoosterNonEnergies();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory GenerateBoosterNonEnergies */

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
	{ NULL, NULL },
};
