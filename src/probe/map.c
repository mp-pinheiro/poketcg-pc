#include "home/map.h"
#include "probe.h"

#include "generated/hram.h"

static void adapt_GetPermissionByteOfMapPosition(ProbeState *s)
{
	PermissionResult result = GetPermissionByteOfMapPosition(s->b, s->c);
	s->a = result.a;
	s->hl = result.hl;
}

static void adapt_GetPermissionOfMapPosition(ProbeState *s)
{
	s->a = GetPermissionOfMapPosition(s->b, s->c);
}

static void adapt_SetPermissionOfMapPosition(ProbeState *s)
{
	SetPermissionOfMapPosition(s->a, s->b, s->c);
}

static void adapt_UpdatePermissionOfMapPosition(ProbeState *s)
{
	s->a = UpdatePermissionOfMapPosition(s->a, s->b, s->c);
}

static void adapt_GetLoadedNPCID(ProbeState *s)
{
	PermissionResult result = GetLoadedNPCID(s->a);
	s->a = result.a;
	s->hl = result.hl;
}

static void adapt_GetItemInLoadedNPCIndex(ProbeState *s)
{
	PermissionResult result = GetItemInLoadedNPCIndex(s->a, (uint8_t)s->hl);
	s->a = result.a;
	s->hl = result.hl;
}

static void adapt_GameEvent_Overworld(ProbeState *s)
{
	s->f = GameEvent_Overworld(s->f);
}

static void adapt_CopyGfxDataFromTempBank(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);

	CopyGfxDataFromTempBank(&s->hl, &de, s->b, s->c);
	s->b = 0;
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
	s->a = hBankROM;
}

static void adapt_FindLoadedNPC(ProbeState *s)
{
	NPCSearchResult result = FindLoadedNPC();
	s->a = result.a;
	s->f = result.f;
}

static void adapt_GetNextNPCMovementByte(ProbeState *s)
{
	s->a = GetNextNPCMovementByte((uint16_t)(s->b << 8 | s->c));
}

static void adapt_GetDefaultSong(ProbeState *s)
{
	s->a = GetDefaultSong();
}

static void adapt_PlayDefaultSong(ProbeState *s)
{
	SongResult result = PlayDefaultSong();
	s->a = result.a;
	s->f = result.f;
}


/* >>> factory HandleMapWarp */

static void adapt_HandleMapWarp(ProbeState *s)
{
	HandleMapWarp();
	(void)s;
}
/* <<< factory HandleMapWarp */

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
	{ NULL, NULL },
};
