/* >>> part includes */
#include "home/play_song.h"

#include "home/lcd_enable_frame.h"
#include "home/sound.h"
/* <<< part includes */

/* >>> factory ScriptPlaySong */
void ScriptPlaySong(uint8_t a)
{
	PlaySong(a);
}
/* <<< factory ScriptPlaySong */


/* >>> factory WaitForSongToFinish */
void WaitForSongToFinish(void)
{
	do {
		DoFrameIfLCDEnabled();
	} while (AssertSongFinished());
}
/* <<< factory WaitForSongToFinish */
