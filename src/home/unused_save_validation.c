#include "home/unused_save_validation.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/sram.h"

#define RRAMG_ADDR             0x0000u
#define RAMG_SRAM_ENABLE       0x0Au
#define SAVE_VALIDATION_RANGE  0x250u

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/credits_sequence_commands.h"
#include "home/duel_core.h"
#include "home/input.h"
#include "home/process_text.h"
#include "home/tiles.h"
#include "mem.h"
#define RRAMB_ADDR 0x4000u
#define RRTCREG_ADDR 0xA000u
#define CONSOLE_SGB 0x01u
#define SGB_DEFAULT_PALETTE 0xE4u
#define YourDataWasDestroyedSomehowText 0x00a3u
/* <<< factory statics */

/* >>> factory StubbedUnusedSaveDataValidation */
/* unused_save_validation.asm:6-7 */
void StubbedUnusedSaveDataValidation(void)
{
}
/* <<< factory StubbedUnusedSaveDataValidation */

/* >>> factory UnusedCalculateSaveDataValidationByte */
/* unused_save_validation.asm:71-96 */
UnusedCalculateSaveDataValidationByteResult UnusedCalculateSaveDataValidationByte(void)
{
	uint8_t bank = hBankSRAM;
	if (bank != 0u)
		return (UnusedCalculateSaveDataValidationByteResult){bank, 0x00u};

	uint8_t checksum = 0u;
	for (uint16_t i = 0; i < SAVE_VALIDATION_RANGE; i++)
		checksum ^= gb_read8((uint16_t)(sCardCollection_ADDR + i));

	gb_write8(RRAMG_ADDR, RAMG_SRAM_ENABLE);
	gb_write8(sUnusedSaveDataValidationByte_ADDR, checksum);
	return (UnusedCalculateSaveDataValidationByteResult){checksum, 0x80u};
}
/* <<< factory UnusedCalculateSaveDataValidationByte */

/* >>> factory UnusedSaveDataValidation */
void UnusedSaveDataValidation(void)
{
	if (gb_read8(0xFF81u) != 0u)
		return;
}
/* <<< factory UnusedSaveDataValidation */
