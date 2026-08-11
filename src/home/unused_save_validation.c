#include "home/unused_save_validation.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "mem.h"

void StubbedUnusedSaveDataValidation(void)
{
}

UnusedSaveValidationResult UnusedCalculateSaveDataValidationByte(void)
{
	uint8_t bank = hBankSRAM;
	if (bank != 0)
		return (UnusedSaveValidationResult){bank, 0};

	uint8_t value = 0;
	for (uint16_t i = 0; i < 0x250u; i++)
		value = (uint8_t)(gb_read8((uint16_t)(sCardCollection_ADDR + i)) ^ value);

	gb_write8(0x0000u, 0x0Au);
	gb_write8(sUnusedSaveDataValidationByte_ADDR, value);
	return (UnusedSaveValidationResult){value, 0x80};
}
