/* --- factory _DrawPortrait */
/* --- factory LoadScene_LoadSGBPacket */
/* --- factory LoadScene_LoadCompressedSGBPacket */
/* --- factory LoadScene_SetCardPopAttrBlk */
/* --- factory LoadScene_SetGameBoyPrinterAttrBlk */
/* >>> part probe_entries_scenes */
const ProbeEntry probe_entries_scenes[] = {
	{ "SetBoosterLogoOAM", adapt_SetBoosterLogoOAM },
	{ "_LoadScene", adapt__LoadScene },
	{ "LoadBoosterGfx", adapt_LoadBoosterGfx },
	{ NULL, NULL },
};
/* <<< part probe_entries_scenes */
