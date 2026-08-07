#ifndef POKETCG_HOME_SAVE_H
#define POKETCG_HOME_SAVE_H

#include <stdint.h>

void CopyGeneralSaveDataToSRAM(uint16_t de);
void ValidateGeneralSaveDataFromDE(uint16_t de);
void LoadGeneralSaveDataFromDE(uint16_t de);
void WriteDataToBackup(uint16_t hl, uint16_t bc);
void LoadDataFromBackup(uint16_t hl, uint16_t bc);
void WriteBackupGeneralSaveData(void);
void WriteBackupCardAndDeckSaveData(void);
void LoadBackupGeneralSaveData(void);
void LoadBackupCardAndDeckSaveData(void);

typedef struct {
	uint8_t a;
	uint8_t f;
} ValidateResult;

void InvalidateSaveData(void);
void UpdateAlbumProgress(uint16_t de);
void LoadAlbumProgressFromSRAM(uint16_t de);
void LoadBackupSaveData(void);
void _LoadGeneralSaveData(void);
void _AddCardToCollectionAndUpdateAlbumProgress(uint8_t a);
ValidateResult ValidateBackupGeneralSaveData(void);
ValidateResult _ValidateGeneralSaveData(void);

#endif /* POKETCG_HOME_SAVE_H */
