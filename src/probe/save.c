/* >>> part includes */
#include "home/save.h"

#include "probe.h"
/* <<< part includes */

/* >>> factory CopyGeneralSaveDataToSRAM */
static void adapt_CopyGeneralSaveDataToSRAM(ProbeState *s)
{
	CopyGeneralSaveDataToSRAM((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory CopyGeneralSaveDataToSRAM */

/* >>> factory ValidateGeneralSaveDataFromDE */
static void adapt_ValidateGeneralSaveDataFromDE(ProbeState *s)
{
	ValidateGeneralSaveDataFromDE((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory ValidateGeneralSaveDataFromDE */

/* >>> factory LoadGeneralSaveDataFromDE */
static void adapt_LoadGeneralSaveDataFromDE(ProbeState *s)
{
	LoadGeneralSaveDataFromDE((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory LoadGeneralSaveDataFromDE */

/* >>> factory WriteDataToBackup */
static void adapt_WriteDataToBackup(ProbeState *s)
{
	WriteDataToBackup(s->hl, (uint16_t)(s->b << 8 | s->c));
}
/* <<< factory WriteDataToBackup */

/* >>> factory LoadDataFromBackup */
static void adapt_LoadDataFromBackup(ProbeState *s)
{
	LoadDataFromBackup(s->hl, (uint16_t)(s->b << 8 | s->c));
}
/* <<< factory LoadDataFromBackup */

/* >>> factory WriteBackupGeneralSaveData */
static void adapt_WriteBackupGeneralSaveData(ProbeState *s)
{
	(void)s;
	WriteBackupGeneralSaveData();
}
/* <<< factory WriteBackupGeneralSaveData */

/* >>> factory WriteBackupCardAndDeckSaveData */
static void adapt_WriteBackupCardAndDeckSaveData(ProbeState *s)
{
	(void)s;
	WriteBackupCardAndDeckSaveData();
}
/* <<< factory WriteBackupCardAndDeckSaveData */

/* >>> factory LoadBackupGeneralSaveData */
static void adapt_LoadBackupGeneralSaveData(ProbeState *s)
{
	(void)s;
	LoadBackupGeneralSaveData();
}
/* <<< factory LoadBackupGeneralSaveData */

/* >>> factory LoadBackupCardAndDeckSaveData */
static void adapt_LoadBackupCardAndDeckSaveData(ProbeState *s)
{
	(void)s;
	LoadBackupCardAndDeckSaveData();
}
/* <<< factory LoadBackupCardAndDeckSaveData */

/* >>> factory InvalidateSaveData */
static void adapt_InvalidateSaveData(ProbeState *s)
{
	(void)s;
	InvalidateSaveData();
}
/* <<< factory InvalidateSaveData */

/* >>> factory UpdateAlbumProgress */
static void adapt_UpdateAlbumProgress(ProbeState *s)
{
	UpdateAlbumProgress((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory UpdateAlbumProgress */

/* >>> factory LoadAlbumProgressFromSRAM */
static void adapt_LoadAlbumProgressFromSRAM(ProbeState *s)
{
	LoadAlbumProgressFromSRAM((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory LoadAlbumProgressFromSRAM */

/* >>> factory ValidateBackupGeneralSaveData */
static void adapt_ValidateBackupGeneralSaveData(ProbeState *s)
{
	ValidateResult r = ValidateBackupGeneralSaveData();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ValidateBackupGeneralSaveData */

/* >>> factory _ValidateGeneralSaveData */
static void adapt__ValidateGeneralSaveData(ProbeState *s)
{
	ValidateResult r = _ValidateGeneralSaveData();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory _ValidateGeneralSaveData */

/* >>> factory LoadBackupSaveData */
static void adapt_LoadBackupSaveData(ProbeState *s)
{
	(void)s;
	LoadBackupSaveData();
}
/* <<< factory LoadBackupSaveData */

/* >>> factory _LoadGeneralSaveData */
static void adapt__LoadGeneralSaveData(ProbeState *s)
{
	(void)s;
	_LoadGeneralSaveData();
}
/* <<< factory _LoadGeneralSaveData */

/* >>> factory _AddCardToCollectionAndUpdateAlbumProgress */
static void adapt__AddCardToCollectionAndUpdateAlbumProgress(ProbeState *s)
{
	_AddCardToCollectionAndUpdateAlbumProgress(s->a);
}
/* <<< factory _AddCardToCollectionAndUpdateAlbumProgress */

/* >>> factory SaveGeneralSaveDataFromDE */
static void adapt_SaveGeneralSaveDataFromDE(ProbeState *s)
{
	SaveGeneralSaveDataFromDE((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory SaveGeneralSaveDataFromDE */

/* >>> factory _SaveGeneralSaveData */
static void adapt__SaveGeneralSaveData(ProbeState *s)
{
	(void)s;
	_SaveGeneralSaveData();
}
/* <<< factory _SaveGeneralSaveData */

/* >>> factory SaveAndBackupData */
static void adapt_SaveAndBackupData(ProbeState *s)
{
	(void)s;
	SaveAndBackupData();
}
/* <<< factory SaveAndBackupData */

/* >>> factory _SaveGame */
static void adapt__SaveGame(ProbeState *s)
{
	_SaveGame(s->c);
}
/* <<< factory _SaveGame */

/* >>> factory SaveGeneralSaveData */
static void adapt_SaveGeneralSaveData(ProbeState *s)
{
	(void)s;
	SaveGeneralSaveData();
}
/* <<< factory SaveGeneralSaveData */

/* >>> factory LoadGeneralSaveData */
static void adapt_LoadGeneralSaveData(ProbeState *s)
{
	(void)s;
	LoadGeneralSaveData();
}
/* <<< factory LoadGeneralSaveData */

/* >>> factory ValidateGeneralSaveData */
static void adapt_ValidateGeneralSaveData(ProbeState *s)
{
	ValidateResult r = ValidateGeneralSaveData();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ValidateGeneralSaveData */

/* >>> factory AddCardToCollectionAndUpdateAlbumProgress */
static void adapt_AddCardToCollectionAndUpdateAlbumProgress(ProbeState *s)
{
	AddCardToCollectionAndUpdateAlbumProgress(s->a);
}
/* <<< factory AddCardToCollectionAndUpdateAlbumProgress */

/* >>> factory SaveGame */
static void adapt_SaveGame(ProbeState *s)
{
	(void)s;
	SaveGame();
}
/* <<< factory SaveGame */

/* >>> part probe_entries_save */
const ProbeEntry probe_entries_save[] = {
	{ "CopyGeneralSaveDataToSRAM", adapt_CopyGeneralSaveDataToSRAM },
	{ "ValidateGeneralSaveDataFromDE", adapt_ValidateGeneralSaveDataFromDE },
	{ "LoadGeneralSaveDataFromDE", adapt_LoadGeneralSaveDataFromDE },
	{ "WriteDataToBackup", adapt_WriteDataToBackup },
	{ "LoadDataFromBackup", adapt_LoadDataFromBackup },
	{ "WriteBackupGeneralSaveData", adapt_WriteBackupGeneralSaveData },
	{ "WriteBackupCardAndDeckSaveData", adapt_WriteBackupCardAndDeckSaveData },
	{ "LoadBackupGeneralSaveData", adapt_LoadBackupGeneralSaveData },
	{ "LoadBackupCardAndDeckSaveData", adapt_LoadBackupCardAndDeckSaveData },
	{ "InvalidateSaveData", adapt_InvalidateSaveData },
	{ "UpdateAlbumProgress", adapt_UpdateAlbumProgress },
	{ "LoadAlbumProgressFromSRAM", adapt_LoadAlbumProgressFromSRAM },
	{ "ValidateBackupGeneralSaveData", adapt_ValidateBackupGeneralSaveData },
	{ "_ValidateGeneralSaveData", adapt__ValidateGeneralSaveData },
	{ "LoadBackupSaveData", adapt_LoadBackupSaveData },
	{ "_LoadGeneralSaveData", adapt__LoadGeneralSaveData },
	{ "_AddCardToCollectionAndUpdateAlbumProgress", adapt__AddCardToCollectionAndUpdateAlbumProgress },
	{ "SaveGeneralSaveDataFromDE", adapt_SaveGeneralSaveDataFromDE },
	{ "_SaveGeneralSaveData", adapt__SaveGeneralSaveData },
	{ "SaveAndBackupData", adapt_SaveAndBackupData },
	{ "_SaveGame", adapt__SaveGame },
	{ "SaveGeneralSaveData", adapt_SaveGeneralSaveData },
	{ "LoadGeneralSaveData", adapt_LoadGeneralSaveData },
	{ "ValidateGeneralSaveData", adapt_ValidateGeneralSaveData },
	{ "AddCardToCollectionAndUpdateAlbumProgress", adapt_AddCardToCollectionAndUpdateAlbumProgress },
	{ "SaveGame", adapt_SaveGame },
	{ NULL, NULL },
};
/* <<< part probe_entries_save */
