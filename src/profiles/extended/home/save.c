/* >>> part includes */
#include "home/save.h"

#include "generated/rom.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_collection.h"
#include "home/core.h"
#include "home/switch_sram.h"
#include "mem.h"
#include "home/frames.h"
/* <<< part includes */
/* >>> part mapper_entry */
static const uint8_t *mapper_entry(unsigned index)
{
	return rom_ptr(WRAMToSRAMMapper_BANK, (uint16_t)(WRAM_TO_SRAM_MAPPER + index * 6u));
}
/* <<< part mapper_entry */
/* >>> part save_src_read8 */
/* Mapper sources are WRAM except for the four .EmptySRAMSlot entries ($556C), which
 * live in this file's own ROM bank. The asm reads them via the implicit code bank. */
static uint8_t save_src_read8(uint16_t addr)
{
	return addr < 0x8000 ? *rom_ptr(WRAMToSRAMMapper_BANK, addr) : gb_read8(addr);
}
/* <<< part save_src_read8 */
/* >>> factory InvalidateSaveData */
/* InvalidateSaveData:: save.asm:4-25 */
void InvalidateSaveData(void)
{
	uint8_t saved = hBankSRAM;

	BankswitchSRAM(2); /* BANK("SRAM2") */
	gb_write8(sBackupGeneralSaveData_ADDR + 0, (uint8_t)(0x08 ^ 0xFF));
	gb_write8(sBackupGeneralSaveData_ADDR + 1, (uint8_t)(0x00 ^ 0xFF));
	BankswitchSRAM(saved);

	DisableSRAM();
	EnableSRAM();
	DiscardSavedDuelData();
	DisableSRAM();
}
/* <<< factory InvalidateSaveData */
/* >>> factory UpdateAlbumProgress */
/* UpdateAlbumProgress:: save.asm:73-89. No bank switch: writes into whichever
 * SRAM bank is already selected, not sAlbumProgress's declared bank. */
void UpdateAlbumProgress(uint16_t de)
{
	AlbumProgress ap = GetCardAlbumProgress();

	EnableSRAM();
	gb_write8(wTotalNumCardsCollected_ADDR, ap.e);
	gb_write8((uint16_t)(wTotalNumCardsCollected_ADDR + 1u), ap.d);
	gb_write8(de, ap.e);
	gb_write8((uint16_t)(de + 1u), ap.d);
	gb_write8(wTotalNumCardsToCollect_ADDR, ap.c);
	gb_write8((uint16_t)(wTotalNumCardsToCollect_ADDR + 1u), ap.b);
	gb_write8((uint16_t)(de + 2u), ap.c);
	gb_write8((uint16_t)(de + 3u), ap.b);
	DisableSRAM();
}
/* <<< factory UpdateAlbumProgress */
/* >>> factory LoadAlbumProgressFromSRAM */
/* LoadAlbumProgressFromSRAM:: save.asm:346-354 */
void LoadAlbumProgressFromSRAM(uint16_t de)
{
	gb_write8(wTotalNumCardsCollected_ADDR, gb_read8(de));
	gb_write8((uint16_t)(wTotalNumCardsCollected_ADDR + 1u),
		  gb_read8((uint16_t)(de + 1u)));
	gb_write8(wTotalNumCardsToCollect_ADDR, gb_read8((uint16_t)(de + 2u)));
	gb_write8((uint16_t)(wTotalNumCardsToCollect_ADDR + 1u),
		  gb_read8((uint16_t)(de + 3u)));
}
/* <<< factory LoadAlbumProgressFromSRAM */
/* >>> factory LoadBackupSaveData */
/* LoadBackupSaveData:: save.asm:358-370 */
void LoadBackupSaveData(void)
{
	EnableSRAM();
	DiscardSavedDuelData();
	DisableSRAM();
	LoadBackupGeneralSaveData();
	LoadBackupCardAndDeckSaveData();
	LoadGeneralSaveDataFromDE(sGeneralSaveData_ADDR);
}
/* <<< factory LoadBackupSaveData */
/* --- factory _AddCardToCollectionAndUpdateAlbumProgress */
/* >>> part EV_ISHIHARA_MENT */
#define EV_ISHIHARA_MENT EVENT_ISHIHARAS_HOUSE_MENTIONED
/* <<< part EV_ISHIHARA_MENT */
/* >>> part EV_LEGENDARY */
#define EV_LEGENDARY     EVENT_RECEIVED_LEGENDARY_CARDS
/* <<< part EV_LEGENDARY */
/* >>> part EV_MEDAL_COUNT */
#define EV_MEDAL_COUNT   EVENT_MEDAL_COUNT
/* <<< part EV_MEDAL_COUNT */
/* >>> part get_event_var */
/* GetEventVar:: scripting.asm:366-382. Returns wEventVars+offset and stashes the
 * mask in wLoadedEventBits, exactly as the asm leaves it for Get/SetEventValue. */
static uint16_t get_event_var(uint8_t ev)
{
	const uint8_t *p = rom_ptr(EventVarMasks_BANK, (uint16_t)(EVENT_VAR_MASKS + (uint16_t)ev * 2u));

	gb_write8(wLoadedEventBits_ADDR, p[1]);
	return (uint16_t)(wEventVars_ADDR + p[0]);
}
/* <<< part get_event_var */
/* >>> part try_give_medal_pc_packs */
/* TryGiveMedalPCPacks:: scripting.asm:311-353. The three grants are fall-through
 * (not else-if): >=8 gives $c/$b/$a, >=7 gives $b/$a, >=3 gives $a. Returns the
 * medal count, restored from a pushed copy after the grants. */
static uint8_t try_give_medal_pc_packs(void)
{
	const uint8_t *events = rom_ptr(MedalEvents_BANK, MEDAL_EVENTS);
	uint8_t count = 0;
	int i;

	for (i = 0; i < 8; i++)
		if (get_event_value(events[i]))
			count++;

	set_event_value(EV_MEDAL_COUNT, count);
	if (count >= 8)
		try_give_pc_pack(0x0c);
	if (count >= 7)
		try_give_pc_pack(0x0b);
	if (count >= 3)
		try_give_pc_pack(0x0a);
	return count;
}
/* <<< part try_give_medal_pc_packs */
/* --- factory AddCardToCollectionAndUpdateAlbumProgress */
/* --- factory SaveGame */
/* === factory LoadBackupCardAndDeckSaveData */
/* === factory WriteBackupCardAndDeckSaveData */
