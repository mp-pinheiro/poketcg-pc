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
/* --- factory AddCardToCollectionAndUpdateAlbumProgress */
/* --- factory SaveGame */
/* === factory LoadBackupCardAndDeckSaveData */
/* === factory WriteBackupCardAndDeckSaveData */
