/* --- factory FlushPalette */
/* >>> part probe_entries_palettes */
const ProbeEntry probe_entries_palettes[] = {
	{ "FlushAllPalettes", adapt_FlushAllPalettes },
	{ "SetBGP", adapt_SetBGP },
	{ "FlushPalette0", adapt_FlushPalette0 },
	{ "FlushPalettes", adapt_FlushPalettes },
	{ "SetOBP0", adapt_SetOBP0 },
	{ "SetOBP1", adapt_SetOBP1 },
	{ "FlushPalettesIfRequested", adapt_FlushPalettesIfRequested },
	{ "CopyCGBPalettes", adapt_CopyCGBPalettes },
	{ "FlushAllCGBPalettes", adapt_FlushAllCGBPalettes },
	{ NULL, NULL },
};
/* <<< part probe_entries_palettes */
