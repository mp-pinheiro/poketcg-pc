#include "home/play_song.h"
#include "probe.h"

static void adapt_ScriptPlaySong(ProbeState *s)
{
	ScriptPlaySong(s->a);
}

static void adapt_Func_3c87(ProbeState *s)
{
	Func_3c87(s->a);
}

static void adapt_WaitForSongToFinish(ProbeState *s)
{
	WaitForSongToFinish();
	(void)s;
}

const ProbeEntry probe_entries_play_song[] = {
	{ "ScriptPlaySong", adapt_ScriptPlaySong },
	{ "Func_3c87", adapt_Func_3c87 },
	{ "WaitForSongToFinish", adapt_WaitForSongToFinish },
	{ NULL, NULL },
};
