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
	{ NULL, NULL },
};
