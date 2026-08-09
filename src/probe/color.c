#include "home/color.h"
#include "probe.h"

static void adapt_LoadConsolePaletteData(ProbeState *s) { (void)s; LoadConsolePaletteData(); }
static void adapt_FadeScreenToWhite(ProbeState *s) { (void)s; FadeScreenToWhite(); }
static void adapt_BackupPalsAndSetWhite(ProbeState *s) { (void)s; FadeScreenFromWhite_BackupPalsAndSetWhite(); }
static void adapt_SetWhitePalettes(ProbeState *s) { (void)s; SetWhitePalettes(); }
static void adapt_Func_10d17(ProbeState *s) { (void)s; Func_10d17(); }
static void adapt_Func_10d50(ProbeState *s) { (void)s; Func_10d50(); }
static void adapt_FadeScreenFromWhite(ProbeState *s) { s->a = FadeScreenFromWhite(); }
static void adapt_FadeScreenToTempPals(ProbeState *s) { s->a = FadeScreenToTempPals(); }
static void adapt_RestoreFirstColorInOBPals(ProbeState *s) { (void)s; RestoreFirstColorInOBPals(); }
static void adapt_FadeDMGPalettes(ProbeState *s) { (void)s; FadeDMGPalettes(); }
static void adapt_CalculateMixPalette(ProbeState *s) { s->a = FadeDMGPalettes_CalculateMixPalette(s->b, s->c); }
static void adapt_GetMixShadeValue(ProbeState *s) { s->a = FadeDMGPalettes_GetMixShadeValue(s->b, s->c); }
static void adapt_FadeOBPalIntoTemp(ProbeState *s) { (void)s; FadeOBPalIntoTemp(); }
static void adapt_FadeBGPalIntoTemp1(ProbeState *s) { (void)s; FadeBGPalIntoTemp1(); }
static void adapt_FadeBGPalIntoTemp2(ProbeState *s) { (void)s; FadeBGPalIntoTemp2(); }
static void adapt_FadeBGPalIntoTemp3(ProbeState *s) { (void)s; FadeBGPalIntoTemp3(); }
static void adapt_GetFadedColor(ProbeState *s) { FadeColorResult result = FadePalIntoAnother_GetFadedColor(s->b, s->c, s->d, s->e); s->a = result.a; s->c = result.c; }
static void adapt_FadeColor(ProbeState *s) { s->a = FadePalIntoAnother_FadeColor(s->a, s->hl); }
static void adapt_FlashScreenToWhite(ProbeState *s) { FlashScreenToWhite(s->c); }
static void adapt_CopyPalsToSRAMBuffer(ProbeState *s) { (void)s; CopyPalsToSRAMBuffer(); }
static void adapt_LoadPalsFromSRAMBuffer(ProbeState *s) { (void)s; LoadPalsFromSRAMBuffer(); }
static void adapt_Func_10d74(ProbeState *s) { (void)s; Func_10d74(); }

const ProbeEntry probe_entries_color[] = {
    { "LoadConsolePaletteData", adapt_LoadConsolePaletteData },
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
