#include "home/play_song.h"
#include "probe.h"

static void adapt_ScriptPlaySong(ProbeState *s)
{
	ScriptPlaySong(s->a);
}

static void adapt_WaitForSongToFinish(ProbeState *s)
{
	WaitForSongToFinish();
	(void)s;
}

const ProbeEntry probe_entries_play_song[] = {
	{ "ScriptPlaySong", adapt_ScriptPlaySong },
	{ "WaitForSongToFinish", adapt_WaitForSongToFinish },
	{ NULL, NULL },
};
