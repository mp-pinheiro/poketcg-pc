/* --- factory LoadConsolePaletteData */
/* >>> part probe_entries_color */
const ProbeEntry probe_entries_color[] = {
    { "FadeScreenToWhite", adapt_FadeScreenToWhite },
    { "FadeScreenFromWhite.BackupPalsAndSetWhite", adapt_BackupPalsAndSetWhite },
    { "SetWhitePalettes", adapt_SetWhitePalettes },
    { "Func_10d17", adapt_Func_10d17 },
    { "Func_10d50", adapt_Func_10d50 },
    { "FadeScreenFromWhite", adapt_FadeScreenFromWhite },
    { "FadeScreenToTempPals", adapt_FadeScreenToTempPals },
    { "RestoreFirstColorInOBPals", adapt_RestoreFirstColorInOBPals },
    { "FadeDMGPalettes", adapt_FadeDMGPalettes },
    { "FadeDMGPalettes.CalculateMixPalette", adapt_CalculateMixPalette },
    { "FadeDMGPalettes.GetMixShadeValue", adapt_GetMixShadeValue },
    { "FadeOBPalIntoTemp", adapt_FadeOBPalIntoTemp },
    { "FadeBGPalIntoTemp1", adapt_FadeBGPalIntoTemp1 },
    { "FadeBGPalIntoTemp2", adapt_FadeBGPalIntoTemp2 },
    { "FadeBGPalIntoTemp3", adapt_FadeBGPalIntoTemp3 },
    { "FadePalIntoAnother.GetFadedColor", adapt_GetFadedColor },
    { "FadePalIntoAnother.FadeColor", adapt_FadeColor },
    { "FlashScreenToWhite", adapt_FlashScreenToWhite },
    { "CopyPalsToSRAMBuffer", adapt_CopyPalsToSRAMBuffer },
    { "LoadPalsFromSRAMBuffer", adapt_LoadPalsFromSRAMBuffer },
    { "Func_10d74", adapt_Func_10d74 },
    { NULL, NULL },
};
/* <<< part probe_entries_color */
