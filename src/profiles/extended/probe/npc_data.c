/* --- factory _GetNPCDuelConfigurations */
/* >>> part probe_entries_npc_data */
const ProbeEntry probe_entries_npc_data[] = {
	{ "GetNPCHeaderPointer", adapt_GetNPCHeaderPointer },
	{ "SetNPCOpponentNameAndPortrait", adapt_SetNPCOpponentNameAndPortrait },
	{ "GetNPCNameAndScript", adapt_GetNPCNameAndScript },
	{ "LoadNPCSpriteData", adapt_LoadNPCSpriteData },
	{ "SetNPCDeckIDAndDuelTheme", adapt_SetNPCDeckIDAndDuelTheme },
	{ "_GetChallengeMachineDuelConfigurations", adapt__GetChallengeMachineDuelConfigurations },
	{ "SetNPCDialogName", adapt_SetNPCDialogName },
	{ "SetNPCMatchStartTheme", adapt_SetNPCMatchStartTheme },
	{ NULL, NULL },
};
/* <<< part probe_entries_npc_data */
