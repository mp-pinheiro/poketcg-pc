/* --- factory GameEvent_GiftCenter */
/* --- factory GameEvent_BattleCenter */
/* >>> part probe_entries_map */
const ProbeEntry probe_entries_map[] = {
	{ "GetPermissionByteOfMapPosition", adapt_GetPermissionByteOfMapPosition },
	{ "GetPermissionOfMapPosition", adapt_GetPermissionOfMapPosition },
	{ "SetPermissionOfMapPosition", adapt_SetPermissionOfMapPosition },
	{ "UpdatePermissionOfMapPosition", adapt_UpdatePermissionOfMapPosition },
	{ "GetLoadedNPCID", adapt_GetLoadedNPCID },
	{ "GetItemInLoadedNPCIndex", adapt_GetItemInLoadedNPCIndex },
	{ "GameEvent_Overworld", adapt_GameEvent_Overworld },
	{ "CopyGfxDataFromTempBank", adapt_CopyGfxDataFromTempBank },
	{ "FindLoadedNPC", adapt_FindLoadedNPC },
	{ "GetNextNPCMovementByte", adapt_GetNextNPCMovementByte },
	{ "GetDefaultSong", adapt_GetDefaultSong },
	{ "PlayDefaultSong", adapt_PlayDefaultSong },
	{ "HandleMapWarp", adapt_HandleMapWarp },
	{ "GetReceivedLegendaryCards", adapt_GetReceivedLegendaryCards },
	{ "OverworldDoFrameFunction", adapt_OverworldDoFrameFunction },
	{ "GameEvent_Duel", adapt_GameEvent_Duel },
	{ "GameEvent_ChallengeMachine", adapt_GameEvent_ChallengeMachine },
	{ "GameEvent_Credits", adapt_GameEvent_Credits },
	{ "GameEvent_ContinueDuel", adapt_GameEvent_ContinueDuel },
	{ "_ExecuteGameEvent", adapt__ExecuteGameEvent },
	{ "ExecuteGameEvent", adapt_ExecuteGameEvent },
	{ NULL, NULL },
};
/* <<< part probe_entries_map */
