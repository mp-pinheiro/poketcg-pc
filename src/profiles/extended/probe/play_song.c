/* >>> part includes */
#include "home/play_song.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ScriptPlaySong */
static void adapt_ScriptPlaySong(ProbeState *s)
{
	ScriptPlaySong(s->a);
}
/* <<< factory ScriptPlaySong */

/* >>> factory WaitForSongToFinish */
static void adapt_WaitForSongToFinish(ProbeState *s)
{
	WaitForSongToFinish();
	(void)s;
}
/* <<< factory WaitForSongToFinish */

/* >>> part probe_entries_play_song */
const ProbeEntry probe_entries_play_song[] = {
	{ "ScriptPlaySong", adapt_ScriptPlaySong },
	{ "WaitForSongToFinish", adapt_WaitForSongToFinish },
	{ NULL, NULL },
};
/* <<< part probe_entries_play_song */
