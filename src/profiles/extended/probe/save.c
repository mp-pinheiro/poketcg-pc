/* --- factory _AddCardToCollectionAndUpdateAlbumProgress */
/* --- factory AddCardToCollectionAndUpdateAlbumProgress */
/* --- factory SaveGame */
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
	{ "SaveGeneralSaveDataFromDE", adapt_SaveGeneralSaveDataFromDE },
	{ "_SaveGeneralSaveData", adapt__SaveGeneralSaveData },
	{ "SaveAndBackupData", adapt_SaveAndBackupData },
	{ "_SaveGame", adapt__SaveGame },
	{ "SaveGeneralSaveData", adapt_SaveGeneralSaveData },
	{ "LoadGeneralSaveData", adapt_LoadGeneralSaveData },
	{ "ValidateGeneralSaveData", adapt_ValidateGeneralSaveData },
	{ NULL, NULL },
};
/* <<< part probe_entries_save */
