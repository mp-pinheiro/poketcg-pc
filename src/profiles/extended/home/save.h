#ifndef POKETCG_HOME_SAVE_H
#define POKETCG_HOME_SAVE_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory CopyGeneralSaveDataToSRAM */
void CopyGeneralSaveDataToSRAM(uint16_t de);
/* <<< factory CopyGeneralSaveDataToSRAM */
/* >>> factory ValidateGeneralSaveDataFromDE */
void ValidateGeneralSaveDataFromDE(uint16_t de);
/* <<< factory ValidateGeneralSaveDataFromDE */
/* >>> factory LoadGeneralSaveDataFromDE */
void LoadGeneralSaveDataFromDE(uint16_t de);
/* <<< factory LoadGeneralSaveDataFromDE */
/* >>> factory WriteDataToBackup */
void WriteDataToBackup(uint16_t hl, uint16_t bc);
/* <<< factory WriteDataToBackup */
/* >>> factory LoadDataFromBackup */
void LoadDataFromBackup(uint16_t hl, uint16_t bc);
/* <<< factory LoadDataFromBackup */
/* >>> factory WriteBackupGeneralSaveData */
void WriteBackupGeneralSaveData(void);
/* <<< factory WriteBackupGeneralSaveData */
/* >>> factory WriteBackupCardAndDeckSaveData */
void WriteBackupCardAndDeckSaveData(void);
/* <<< factory WriteBackupCardAndDeckSaveData */
/* >>> factory LoadBackupGeneralSaveData */
void LoadBackupGeneralSaveData(void);
/* <<< factory LoadBackupGeneralSaveData */
/* >>> factory LoadBackupCardAndDeckSaveData */
void LoadBackupCardAndDeckSaveData(void);
/* <<< factory LoadBackupCardAndDeckSaveData */

/* >>> part ValidateResult */
typedef struct {
	uint8_t a;
	uint8_t f;
} ValidateResult;
/* <<< part ValidateResult */

/* >>> factory InvalidateSaveData */
void InvalidateSaveData(void);
/* <<< factory InvalidateSaveData */
/* >>> factory UpdateAlbumProgress */
void UpdateAlbumProgress(uint16_t de);
/* <<< factory UpdateAlbumProgress */
/* >>> factory LoadAlbumProgressFromSRAM */
void LoadAlbumProgressFromSRAM(uint16_t de);
/* <<< factory LoadAlbumProgressFromSRAM */
/* >>> factory LoadBackupSaveData */
void LoadBackupSaveData(void);
/* <<< factory LoadBackupSaveData */
/* >>> factory _LoadGeneralSaveData */
void _LoadGeneralSaveData(void);
/* <<< factory _LoadGeneralSaveData */
/* >>> factory ValidateBackupGeneralSaveData */
ValidateResult ValidateBackupGeneralSaveData(void);
/* <<< factory ValidateBackupGeneralSaveData */
/* >>> factory SaveGeneralSaveDataFromDE */
void SaveGeneralSaveDataFromDE(uint16_t de);
/* <<< factory SaveGeneralSaveDataFromDE */
/* >>> factory SaveAndBackupData */
void SaveAndBackupData(void);
/* <<< factory SaveAndBackupData */
/* >>> factory _SaveGeneralSaveData */
void _SaveGeneralSaveData(void);
/* <<< factory _SaveGeneralSaveData */
/* >>> factory _SaveGame */
void _SaveGame(uint8_t c);
/* <<< factory _SaveGame */
/* >>> factory _ValidateGeneralSaveData */
ValidateResult _ValidateGeneralSaveData(void);
/* <<< factory _ValidateGeneralSaveData */
/* >>> factory SaveGeneralSaveData */
void SaveGeneralSaveData(void);
/* <<< factory SaveGeneralSaveData */
/* >>> factory LoadGeneralSaveData */
void LoadGeneralSaveData(void);
/* <<< factory LoadGeneralSaveData */
/* >>> factory ValidateGeneralSaveData */
ValidateResult ValidateGeneralSaveData(void);
/* <<< factory ValidateGeneralSaveData */

#endif /* POKETCG_HOME_SAVE_H */
