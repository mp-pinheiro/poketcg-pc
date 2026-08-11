#ifndef POKETCG_HOME_UNUSED_SAVE_VALIDATION_H
#define POKETCG_HOME_UNUSED_SAVE_VALIDATION_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} UnusedSaveValidationResult;

void StubbedUnusedSaveDataValidation(void);
UnusedSaveValidationResult UnusedCalculateSaveDataValidationByte(void);


#endif