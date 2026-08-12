#include "home/unused_save_validation.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/sram.h"

#define RRAMG_ADDR             0x0000u
#define RAMG_SRAM_ENABLE       0x0Au
#define SAVE_VALIDATION_RANGE  0x250u
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
