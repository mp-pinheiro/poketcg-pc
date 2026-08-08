#include "home/save.h"

#include "probe.h"

static void adapt_CopyGeneralSaveDataToSRAM(ProbeState *s)
{
	CopyGeneralSaveDataToSRAM((uint16_t)(s->d << 8 | s->e));
}

static void adapt_ValidateGeneralSaveDataFromDE(ProbeState *s)
{
	ValidateGeneralSaveDataFromDE((uint16_t)(s->d << 8 | s->e));
}

static void adapt_LoadGeneralSaveDataFromDE(ProbeState *s)
{
	LoadGeneralSaveDataFromDE((uint16_t)(s->d << 8 | s->e));
}

static void adapt_WriteDataToBackup(ProbeState *s)
{
	WriteDataToBackup(s->hl, (uint16_t)(s->b << 8 | s->c));
}

static void adapt_LoadDataFromBackup(ProbeState *s)
{
	LoadDataFromBackup(s->hl, (uint16_t)(s->b << 8 | s->c));
}

static void adapt_WriteBackupGeneralSaveData(ProbeState *s)
{
	(void)s;
	WriteBackupGeneralSaveData();
}

static void adapt_WriteBackupCardAndDeckSaveData(ProbeState *s)
{
	(void)s;
	WriteBackupCardAndDeckSaveData();
}

static void adapt_LoadBackupGeneralSaveData(ProbeState *s)
{
	(void)s;
	LoadBackupGeneralSaveData();
}

static void adapt_LoadBackupCardAndDeckSaveData(ProbeState *s)
{
	(void)s;
	LoadBackupCardAndDeckSaveData();
}

static void adapt_InvalidateSaveData(ProbeState *s)
{
	(void)s;
	InvalidateSaveData();
}

static void adapt_UpdateAlbumProgress(ProbeState *s)
{
	UpdateAlbumProgress((uint16_t)(s->d << 8 | s->e));
}

static void adapt_LoadAlbumProgressFromSRAM(ProbeState *s)
{
	LoadAlbumProgressFromSRAM((uint16_t)(s->d << 8 | s->e));
}

static void adapt_ValidateBackupGeneralSaveData(ProbeState *s)
{
	ValidateResult r = ValidateBackupGeneralSaveData();
	s->a = r.a;
	s->f = r.f;
}

static void adapt__ValidateGeneralSaveData(ProbeState *s)
{
	ValidateResult r = _ValidateGeneralSaveData();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_LoadBackupSaveData(ProbeState *s)
{
	(void)s;
	LoadBackupSaveData();
}

static void adapt__LoadGeneralSaveData(ProbeState *s)
{
	(void)s;
	_LoadGeneralSaveData();
}

static void adapt__AddCardToCollectionAndUpdateAlbumProgress(ProbeState *s)
{
	_AddCardToCollectionAndUpdateAlbumProgress(s->a);
}

static void adapt_SaveGeneralSaveDataFromDE(ProbeState *s)
{
	SaveGeneralSaveDataFromDE((uint16_t)(s->d << 8 | s->e));
}

static void adapt__SaveGeneralSaveData(ProbeState *s)
{
	(void)s;
	_SaveGeneralSaveData();
}

static void adapt_SaveAndBackupData(ProbeState *s)
{
	(void)s;
	SaveAndBackupData();
}

static void adapt__SaveGame(ProbeState *s)
{
	_SaveGame(s->c);
}

static void adapt_SaveGeneralSaveData(ProbeState *s)
{
	(void)s;
	SaveGeneralSaveData();
}

static void adapt_LoadGeneralSaveData(ProbeState *s)
{
	(void)s;
	LoadGeneralSaveData();
}

static void adapt_ValidateGeneralSaveData(ProbeState *s)
{
	ValidateResult r = ValidateGeneralSaveData();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_AddCardToCollectionAndUpdateAlbumProgress(ProbeState *s)
{
	AddCardToCollectionAndUpdateAlbumProgress(s->a);
}

static void adapt_SaveGame(ProbeState *s)
{
	(void)s;
	SaveGame();
}

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
