/* >>> part includes */
#include "home/color.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory FadeScreenToWhite */
static void adapt_FadeScreenToWhite(ProbeState *s) { (void)s; FadeScreenToWhite(); }
/* <<< factory FadeScreenToWhite */
/* >>> factory FadeScreenFromWhite_BackupPalsAndSetWhite */
static void adapt_BackupPalsAndSetWhite(ProbeState *s) { (void)s; FadeScreenFromWhite_BackupPalsAndSetWhite(); }
/* <<< factory FadeScreenFromWhite_BackupPalsAndSetWhite */
/* >>> factory SetWhitePalettes */
static void adapt_SetWhitePalettes(ProbeState *s) { (void)s; SetWhitePalettes(); }
/* <<< factory SetWhitePalettes */
/* >>> factory Func_10d17 */
static void adapt_Func_10d17(ProbeState *s) { (void)s; Func_10d17(); }
/* <<< factory Func_10d17 */
/* >>> factory Func_10d50 */
static void adapt_Func_10d50(ProbeState *s) { (void)s; Func_10d50(); }
/* <<< factory Func_10d50 */
/* >>> factory FadeScreenFromWhite */
static void adapt_FadeScreenFromWhite(ProbeState *s) { s->a = FadeScreenFromWhite(); }
/* <<< factory FadeScreenFromWhite */
/* >>> factory FadeScreenToTempPals */
static void adapt_FadeScreenToTempPals(ProbeState *s) { s->a = FadeScreenToTempPals(); }
/* <<< factory FadeScreenToTempPals */
/* >>> factory RestoreFirstColorInOBPals */
static void adapt_RestoreFirstColorInOBPals(ProbeState *s) { (void)s; RestoreFirstColorInOBPals(); }
/* <<< factory RestoreFirstColorInOBPals */
/* >>> factory FadeDMGPalettes */
static void adapt_FadeDMGPalettes(ProbeState *s) { (void)s; FadeDMGPalettes(); }
/* <<< factory FadeDMGPalettes */
/* >>> factory FadeDMGPalettes_CalculateMixPalette */
static void adapt_CalculateMixPalette(ProbeState *s) { s->a = FadeDMGPalettes_CalculateMixPalette(s->b, s->c); }
/* <<< factory FadeDMGPalettes_CalculateMixPalette */
/* >>> factory FadeDMGPalettes_GetMixShadeValue */
static void adapt_GetMixShadeValue(ProbeState *s) { s->a = FadeDMGPalettes_GetMixShadeValue(s->b, s->c); }
/* <<< factory FadeDMGPalettes_GetMixShadeValue */
/* >>> factory FadeOBPalIntoTemp */
static void adapt_FadeOBPalIntoTemp(ProbeState *s) { (void)s; FadeOBPalIntoTemp(); }
/* <<< factory FadeOBPalIntoTemp */
/* >>> factory FadeBGPalIntoTemp1 */
static void adapt_FadeBGPalIntoTemp1(ProbeState *s) { (void)s; FadeBGPalIntoTemp1(); }
/* <<< factory FadeBGPalIntoTemp1 */
/* >>> factory FadeBGPalIntoTemp2 */
static void adapt_FadeBGPalIntoTemp2(ProbeState *s) { (void)s; FadeBGPalIntoTemp2(); }
/* <<< factory FadeBGPalIntoTemp2 */
/* >>> factory FadeBGPalIntoTemp3 */
static void adapt_FadeBGPalIntoTemp3(ProbeState *s) { (void)s; FadeBGPalIntoTemp3(); }
/* <<< factory FadeBGPalIntoTemp3 */
/* >>> factory FadePalIntoAnother_GetFadedColor */
static void adapt_GetFadedColor(ProbeState *s) { FadeColorResult result = FadePalIntoAnother_GetFadedColor(s->b, s->c, s->d, s->e); s->a = result.a; s->c = result.c; }
/* <<< factory FadePalIntoAnother_GetFadedColor */
/* >>> factory FadePalIntoAnother_FadeColor */
static void adapt_FadeColor(ProbeState *s) { s->a = FadePalIntoAnother_FadeColor(s->a, s->hl); }
/* <<< factory FadePalIntoAnother_FadeColor */
/* >>> factory FlashScreenToWhite */
static void adapt_FlashScreenToWhite(ProbeState *s) { FlashScreenToWhite(s->c); }
/* <<< factory FlashScreenToWhite */
/* >>> factory CopyPalsToSRAMBuffer */
static void adapt_CopyPalsToSRAMBuffer(ProbeState *s) { (void)s; CopyPalsToSRAMBuffer(); }
/* <<< factory CopyPalsToSRAMBuffer */
/* >>> factory LoadPalsFromSRAMBuffer */
static void adapt_LoadPalsFromSRAMBuffer(ProbeState *s) { (void)s; LoadPalsFromSRAMBuffer(); }
/* <<< factory LoadPalsFromSRAMBuffer */
/* >>> factory Func_10d74 */
static void adapt_Func_10d74(ProbeState *s) { (void)s; Func_10d74(); }
/* <<< factory Func_10d74 */

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
